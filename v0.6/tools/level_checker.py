"""
Level reachability checker.

Explores a level with the real Player physics: from every spot the player can
stand on, it tries a fixed set of input scripts (jumps, double jumps, drops,
wall climbs) and records where the player lands. A level is completable if
some explored trajectory touches the exit portal.

Hazard damage and enemies are ignored (the player can tank a few hits);
moving platforms are approximated as static platforms along their path.

CLI:  python tools/level_checker.py          (every level)
      python tools/level_checker.py 3 5      (just levels 3 and 5)
"""

import os
import sys

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import time  # noqa: E402

import pygame  # noqa: E402

if __package__ in (None, ""):  # run as a script: make the game importable
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BUCKET = 48          # x-resolution of standing spots
SIM_FRAMES = 160     # max frames per input script
NEAR_X = 420         # only tiles within this x-distance are simulated


class _Keys:
    def __init__(self):
        self.down = set()

    def __getitem__(self, key):
        return key in self.down


def _scripts():
    """Input scripts: each is (direction, list of jump frames, style)"""
    scripts = [(0, [0], "plain"), (0, [0, 14], "plain")]
    for d in (-1, 1):
        for second in (None, 6, 12, 18):
            scripts.append((d, [0] if second is None else [0, second], "plain"))
        scripts.append((d, [0, 12], "late"))      # straight up, then steer
        scripts.append((d, [], "walk"))           # walk / drop off an edge
        scripts.append((d, [], "drop_jump"))      # drop off, then air jumps
        scripts.append((d, [0], "climb"))         # wall-jump up a wall
        scripts.append((d, [0], "climb_drop"))    # climb, then let go over the top
        scripts.append((d, [0], "zigzag"))        # bounce between two walls
    return scripts


SCRIPTS = _scripts()


class LevelChecker:
    def __init__(self, level_data):
        from config.layout_manager import LayoutManager, get_object_size
        from objects.portal import Portal

        scale = LayoutManager.scale_position  # level data is in 1280x720 units

        self.data = level_data
        self.height = LayoutManager.scale_dimension(level_data.get("height", 720))
        tile = get_object_size("tile")["size"]
        self.tiles = [
            {"rect": pygame.Rect(*scale(t["x"], t["y"]), tile, tile), "solid": t.get("solid", True)}
            for t in level_data["tiles"]
        ]
        plat = get_object_size("moving_platform")
        for h in level_data.get("hazards", []):
            if h["type"] == "moving_platform":
                hx, hy = scale(h["x"], h["y"])
                for off in range(-150, 151, 50):  # moving platforms travel +-150px
                    self.tiles.append({"rect": pygame.Rect(hx + off, hy, plat["width"], plat["height"]),
                                       "solid": True})
        self.tiles = [t for t in self.tiles if t["solid"]]
        self.tiles.sort(key=lambda t: t["rect"].x)
        self.tile_xs = [t["rect"].x for t in self.tiles]
        self.near_x = int(NEAR_X * LayoutManager.get_scale_factor())
        self.portals = [Portal(*scale(p["x"], p["y"]), p["dest"]).get_rect()
                        for p in level_data.get("portals", [])]
        coin = get_object_size("coin")
        self.coins = [pygame.Rect(*scale(c["x"], c["y"]), coin["width"], coin["height"])
                      for c in level_data.get("coins", [])]
        self.coins_seen = set()
        self.portal_reached = False
        self.spots = set()
        self.spot_positions = {}  # spot key -> (x, y) where the player stood

    # -- simulation -------------------------------------------------------
    def _near_tiles(self, x):
        import bisect
        lo = bisect.bisect_left(self.tile_xs, x - self.near_x)
        hi = bisect.bisect_right(self.tile_xs, x + self.near_x)
        return self.tiles[lo:hi]

    def _new_player(self, x, y):
        from entities.player import Player
        p = Player(x, y)
        return p

    def _touch(self, rect):
        for i, c in enumerate(self.coins):
            if i not in self.coins_seen and rect.colliderect(c):
                self.coins_seen.add(i)
        if not self.portal_reached and any(rect.colliderect(p) for p in self.portals):
            self.portal_reached = True

    def _run(self, x, y, script):
        """Run one input script from a standing spot; return landing spots"""
        from config.controls import MOVE_LEFT, MOVE_RIGHT
        direction, jumps, style = script
        keys = _Keys()
        p = self._new_player(x, y)
        p.on_ground = True
        tiles = self._near_tiles(x)
        landed = []
        last_jump = -10
        left_ground_at = None
        was_on_wall = False
        off_wall_frames = 0
        cleared_wall = False  # climb scripts stop wall-jumping after topping a wall
        for f in range(SIM_FRAMES):
            if f % 8 == 0:
                tiles = self._near_tiles(p.x)
            d = direction
            if style == "late" and f < 8:
                d = 0
            if style == "climb_drop" and cleared_wall:
                d = 0
            keys.down = set()
            if d < 0:
                keys.down.add(MOVE_LEFT[0])
            elif d > 0:
                keys.down.add(MOVE_RIGHT[0])

            jump = f in jumps
            if p.on_wall:
                was_on_wall, off_wall_frames = True, 0
            elif was_on_wall:
                off_wall_frames += 1
                if off_wall_frames > 6:
                    cleared_wall = True
            if (style in ("climb", "climb_drop") and not cleared_wall and p.on_wall and not p.on_ground
                    and f - last_jump >= 3):
                jump = True
            if style == "zigzag" and p.on_wall and not p.on_ground and f - last_jump >= 3:
                jump = True
                direction = -direction
            if style == "drop_jump":
                if left_ground_at is None and not p.on_ground and f > 0:
                    left_ground_at = f
                if left_ground_at is not None and f - left_ground_at in (2, 14):
                    jump = True
            if jump and p.jump():
                last_jump = f

            p.update(keys, tiles, [])
            rect = p.get_rect()
            self._touch(rect)
            if p.y > self.height + 100:
                break
            if p.on_ground and f > 0:
                landed.append((p.x, p.y))
                if style not in ("walk",) and f > last_jump + 2 and (jumps or style != "drop_jump"):
                    # Landed after the airborne part; walking scripts keep going
                    if style in ("plain", "late", "climb", "climb_drop", "zigzag") and f > 3:
                        break
        return landed

    def _spot_key(self, x, y):
        return (int(x) // BUCKET, int(round(y)))

    def check(self, max_spots=4000):
        """Explore from spawn. Returns self for chaining."""
        from config.layout_manager import LayoutManager
        sx, sy = LayoutManager.scale_position(self.data.get("spawn_x", 100), self.data.get("spawn_y", 500))
        frontier = []
        for x, y in self._run(sx, sy, (0, [], "walk")):
            frontier.append((x, y))
        while frontier and len(self.spots) < max_spots:
            x, y = frontier.pop()
            key = self._spot_key(x, y)
            if key in self.spots:
                continue
            self.spots.add(key)
            self.spot_positions[key] = (x, y)
            for script in SCRIPTS:
                for lx, ly in self._run(x, y, script):
                    if self._spot_key(lx, ly) not in self.spots:
                        frontier.append((lx, ly))
        return self

    def coin_coverage(self):
        return len(self.coins_seen) / len(self.coins) if self.coins else 1.0

    def unreachable_coins(self):
        return [(c.x, c.y) for i, c in enumerate(self.coins) if i not in self.coins_seen]


def check_level(level_data):
    return LevelChecker(level_data).check()


def init_headless(game_dir):
    """Prepare a process to check levels without a window"""
    os.chdir(game_dir)
    if game_dir not in sys.path:
        sys.path.insert(0, game_dir)
    pygame.init()
    pygame.display.set_mode((1280, 720))
    from config.settings import update_screen_size
    update_screen_size(1280, 720)  # the game always renders at 1280x720


def check_level_file(args):
    """
    Worker for parallel checks: (game_dir, index, filename) ->
    dict with the results (picklable, for multiprocessing).
    """
    game_dir, index, filename = args
    init_headless(game_dir)
    from levels.level_loader import LevelLoader
    data = LevelLoader.fix_spike_positions(LevelLoader.load_from_file(filename))
    start = time.time()
    c = check_level(data)
    return {
        "index": index, "file": filename, "name": data.get("name", ""),
        "has_portal": bool(c.portals), "portal_reached": c.portal_reached,
        "coins_seen": len(c.coins_seen), "coins": len(c.coins),
        "coverage": c.coin_coverage(), "unreachable": c.unreachable_coins(),
        "spots": len(c.spots), "seconds": time.time() - start,
    }


def check_all(game_dir, only=None, processes=None):
    """Check every level (or indexes in `only`) in parallel; results in level order"""
    import multiprocessing
    from levels.level_loader import LevelLoader
    files = [lvl["file"] for act in LevelLoader.load_acts() for lvl in act["levels"]]
    jobs = [(game_dir, i, f) for i, f in enumerate(files) if not only or i in only]
    with multiprocessing.Pool(processes or min(len(jobs), os.cpu_count() or 2)) as pool:
        return pool.map(check_level_file, jobs)


def main():
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.stdout.reconfigure(errors="replace")
    init_headless(here)
    only = [int(a) for a in sys.argv[1:]]
    for r in check_all(here, only):
        portal = "REACHABLE" if r["portal_reached"] else "UNREACHABLE" if r["has_portal"] else "n/a (boss)"
        print(f"Level {r['index']} {r['name']}: portal {portal} | coins {r['coins_seen']}/{r['coins']}"
              f" | spots {r['spots']} | {r['seconds']:.1f}s")
        if r["unreachable"]:
            print("   unreachable coins (x,y):", r["unreachable"][:25], "..." if len(r["unreachable"]) > 25 else "")


if __name__ == "__main__":
    main()
