"""
Move collectibles the player can't reach - coins and power-ups inside or
between bricks, or floating where no jump reaches - to the nearest spot the
player can actually reach.

Reachability comes from tools/level_checker.py (real player physics). An
item that can't be collected is moved into a standing spot's body height,
keeping its x position when a reachable platform is directly above/below it
so rows and arcs keep their shape. Coins with no reachable spot nearby are
removed; power-ups are always moved (never removed).

CLI:  python tools/fix_coins.py              (all levels, writes the JSON files)
      python tools/fix_coins.py act1/level_03.json
"""

import os
import sys

if __package__ in (None, ""):  # run as a script: make the game importable
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame  # noqa: E402

PLAYER_WIDTH = 28
KEEP_X_RANGE = 40      # reuse an item's x if a spot is this close horizontally

# key in level data -> (item size, checker attribute of reached indexes, max move, removable)
ITEMS = {
    "coins": (16, "coins_seen", 700, True),
    "powerups": (24, "powerups_seen", 100000, False),
}


def _solid_rects(level_data, tile_size=32):
    return [pygame.Rect(t["x"], t["y"], tile_size, tile_size)
            for t in level_data["tiles"] if t.get("solid", True)]


def fix_collectibles(level_data, verbose=False):
    """
    Fix coin and power-up placement in level_data (modified in place).
    Returns {"coins": (moved, removed), "powerups": (moved, removed)}.
    """
    from tools.level_checker import LevelChecker

    tiles = _solid_rects(level_data)
    stats = {key: [0, 0] for key in ITEMS}

    for attempt in range(2):
        checker = LevelChecker(level_data).check()
        spots = list(checker.spot_positions.values())
        # every item placed so far (both kinds), so moved items don't overlap
        taken = []
        bad = {}
        for key, (size, seen_attr, _, _) in ITEMS.items():
            seen = getattr(checker, seen_attr)
            items = level_data.get(key, [])
            bad[key] = [i for i, item in enumerate(items)
                        if i not in seen
                        or pygame.Rect(item["x"], item["y"], size, size).collidelist(tiles) != -1]
            taken += [pygame.Rect(item["x"], item["y"], size, size).inflate(8, 8)
                      for i, item in enumerate(items) if i not in bad[key]]
        if not any(bad.values()):
            break

        for key, (size, _, max_move, removable) in ITEMS.items():
            items = level_data.get(key, [])
            keep = []
            for i, item in enumerate(items):
                if i not in bad[key]:
                    keep.append(item)
                    continue
                best = None
                for px, py in spots:
                    keep_x = attempt == 0 and abs((px + PLAYER_WIDTH / 2) - (item["x"] + size / 2)) <= KEEP_X_RANGE
                    x = item["x"] if keep_x else int(px) + (PLAYER_WIDTH - size) // 2
                    y = int(py) + 48 - size - 8  # low in a standing player's body
                    rect = pygame.Rect(x, y, size, size)
                    if rect.collidelist(tiles) != -1 or rect.collidelist(taken) != -1:
                        continue
                    cost = abs(x - item["x"]) * 2 + abs(y - item["y"])  # prefer vertical moves
                    if cost <= max_move and (best is None or cost < best[0]):
                        best = (cost, x, y)
                if best is None:
                    if removable:
                        stats[key][1] += 1
                        if verbose:
                            print(f"   removed {key[:-1]} at ({item['x']}, {item['y']})")
                    else:
                        keep.append(item)  # nowhere better; leave it
                    continue
                _, x, y = best
                if verbose:
                    print(f"   moved {key[:-1]} ({item['x']}, {item['y']}) -> ({x}, {y})")
                keep.append(dict(item, x=x, y=y))
                taken.append(pygame.Rect(x, y, size, size).inflate(8, 8))
                stats[key][0] += 1
            items[:] = keep
    return {key: tuple(v) for key, v in stats.items()}


def fix_coins(level_data, verbose=False):
    """Fix coins and power-ups; returns (moved, removed) totals (older API)"""
    stats = fix_collectibles(level_data, verbose)
    return sum(m for m, _ in stats.values()), sum(r for _, r in stats.values())


def main():
    game_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(game_dir)
    sys.stdout.reconfigure(errors="replace")
    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    pygame.init()
    pygame.display.set_mode((1280, 720))
    from config.settings import update_screen_size
    from levels.level_loader import LevelLoader

    update_screen_size(1280, 720)
    files = sys.argv[1:] or [lvl["file"] for act in LevelLoader.load_acts() for lvl in act["levels"]]
    for filename in files:
        data = LevelLoader.load_from_file(filename)
        stats = fix_collectibles(data)
        if any(sum(v) for v in stats.values()):
            LevelLoader.save_to_file(data, filename)
        print(f"{filename}: coins moved/removed {stats['coins']}, power-ups moved {stats['powerups'][0]}")


if __name__ == "__main__":
    main()
