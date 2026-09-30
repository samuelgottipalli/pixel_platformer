"""
Section-based level generator for Acts 2-4.

A level is a left-to-right sequence of hand-designed *sections* (stairs, pits
with floating platforms, tree canopies, climbable towers, turret nests...),
each parameterized by a difficulty value `d` (0 = gentle .. 1 = hardest):
gaps widen, enemies multiply and health pickups thin out as `d` rises.

Every generated level is validated with tools/level_checker.py (real player
physics): the exit must be reachable, and coins are fixed with
tools/fix_coins.py so all of them can be collected. A level that fails is
regenerated with the next seed.

Levels are written as JSON to levels/data/actN/. Existing files are NOT
overwritten unless --force is given, so edits made in the level builder
are safe.

CLI:
    python tools/level_generator.py              # create missing Act 2-4 levels
    python tools/level_generator.py --force 14   # regenerate level 14
"""

import os
import random
import sys

if __package__ in (None, ""):  # run as a script: make the game importable
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

T = 32          # tile size
G = 640         # ground top (y)
PORTAL_H = 64

# ---------------------------------------------------------------------------
# Content plan (names from the original Act 2-4 design)
# ---------------------------------------------------------------------------

ACTS = [
    {
        "number": 2, "name": "Nature's Fury", "theme": "NATURE",
        "levels": [
            ("Forest Entrance", 0.30, ["flat", "stairs", "pit", "spikes", "canopy", "flat"]),
            ("Canopy Heights", 0.36, ["canopy", "pit", "canopy", "moving", "canopy", "stairs"]),
            ("Root Systems", 0.42, ["tunnel", "stairs", "tunnel", "pit", "tunnel", "turrets"]),
            ("Ancient Grove", 0.48, ["turrets", "canopy", "spikes", "tower", "pit", "canopy"]),
            ("Nature's Heart", 0.55, ["stairs", "canopy", "moving", "tunnel", "turrets", "spikes", "tower"]),
        ],
        "boss": ("Forest Guardian", "forest"),
    },
    {
        "number": 3, "name": "Cosmic Voyage", "theme": "SPACE",
        "levels": [
            ("Launch Sequence", 0.55, ["flat", "tower", "turrets", "moving", "stairs", "pit"]),
            ("Zero Gravity", 0.60, ["asteroids", "moving", "asteroids", "pit", "asteroids", "stairs"]),
            ("Asteroid Belt", 0.65, ["asteroids", "asteroids", "turrets", "asteroids", "moving", "asteroids"]),
            ("Space Station", 0.70, ["tower", "turrets", "tunnel", "spikes", "tower", "turrets"]),
            ("Solar Flare", 0.75, ["spikes", "moving", "asteroids", "turrets", "spikes", "spire", "asteroids"]),
        ],
        "boss": ("Void Sentinel", "void"),
    },
    {
        "number": 4, "name": "Depths Unknown", "theme": "UNDERGROUND",
        "levels": [
            ("Underground Descent", 0.75, ["stairs", "tunnel", "pit", "spikes", "tunnel", "spire"], "UNDERGROUND"),
            ("Crystal Caverns", 0.80, ["tower", "tunnel", "pit", "turrets", "spikes", "tower"], "UNDERGROUND"),
            ("Submerged Ruins", 0.85, ["pit", "moving", "tunnel", "turrets", "pit", "spikes"], "UNDERWATER"),
            ("Abyssal Trench", 0.90, ["pit", "moving", "pit", "tunnel", "asteroids", "spire"], "UNDERWATER"),
            ("The Core", 0.95, ["tower", "asteroids", "spikes", "turrets", "tunnel", "moving", "spire"],
             "UNDERGROUND"),
        ],
        "boss": ("Ancient Evil", "ancient"),
    },
]

# Level-specific physics (by global level index)
LEVEL_OPTIONS = {
    14: {"gravity": 0.55},   # Zero Gravity: floaty, long jumps
    21: {"water": True},     # Submerged Ruins: swimming, oxygen, currents
    22: {"water": True},     # Abyssal Trench
}

# Share of "ground" enemies replaced by the newer types, per act
ENEMY_MIX = {
    2: {"charger": 0.30},
    3: {"hopper": 0.30, "charger": 0.20},
    4: {"charger": 0.30, "hopper": 0.30},
}

AREA_NAMES = {
    "flat": {"NATURE": "Forest Floor", "SPACE": "Hangar Deck", "UNDERGROUND": "Cave Floor", "UNDERWATER": "Sea Bed"},
    "stairs": {"NATURE": "Mossy Steps", "SPACE": "Gantry", "UNDERGROUND": "Rock Ledges", "UNDERWATER": "Coral Steps"},
    "pit": {"NATURE": "Ravine", "SPACE": "Breach", "UNDERGROUND": "Chasm", "UNDERWATER": "Sunken Gap"},
    "moving": {"NATURE": "River Crossing", "SPACE": "Cargo Lift", "UNDERGROUND": "Mine Cart Gap",
               "UNDERWATER": "Current"},
    "spikes": {"NATURE": "Thorn Patch", "SPACE": "Plasma Vents", "UNDERGROUND": "Crystal Spikes",
               "UNDERWATER": "Urchin Field"},
    "canopy": {"NATURE": "Canopy Walk"},
    "tunnel": {"NATURE": "Root Tunnels", "SPACE": "Maintenance Duct", "UNDERGROUND": "Narrow Passage",
               "UNDERWATER": "Sunken Corridor"},
    "tower": {"NATURE": "Hollow Tree", "SPACE": "Reactor Shaft", "UNDERGROUND": "Mine Shaft",
              "UNDERWATER": "Ruined Tower"},
    "spire": {"NATURE": "Great Trunk", "SPACE": "Antenna Mast", "UNDERGROUND": "Stone Pillar",
              "UNDERWATER": "Kelp Pillar"},
    "turrets": {"NATURE": "Sentry Glade", "SPACE": "Defense Grid", "UNDERGROUND": "Guard Post",
                "UNDERWATER": "Sentry Reef"},
    "asteroids": {"SPACE": "Asteroid Field", "UNDERWATER": "Floating Ruins", "UNDERGROUND": "Floating Rocks",
                  "NATURE": "Floating Islands"},
}


class LevelBuilder:
    """Accumulates level objects while sections are laid out left to right"""

    def __init__(self, rng, d, theme, enemy_mix=None, water=False):
        self.rng, self.d, self.theme = rng, d, theme
        self.enemy_mix = enemy_mix or {}
        self.water = water
        self.air_pockets, self.currents = [], []
        self.tiles, self.enemies, self.hazards = [], [], []
        self.coins, self.powerups, self.areas = [], [], []
        self.x = 0
        self._occupied = set()
        self.sections_since_health = 0

    # --- primitives --------------------------------------------------------
    def tile(self, x, y):
        key = (x, y)
        if key not in self._occupied:
            self._occupied.add(key)
            self.tiles.append({"x": x, "y": y, "solid": True})

    def row(self, x, y, count):
        for i in range(count):
            self.tile(x + i * T, y)

    def col(self, x, y_top, y_bottom):
        for y in range(y_top, y_bottom + 1, T):
            self.tile(x, y)

    def ground(self, x0, x1):
        self.row(x0, G, max(0, (x1 - x0) // T))

    def coin_row(self, x0, y, count, spacing=48, value=1):
        for i in range(count):
            self.coins.append({"x": x0 + i * spacing, "y": y, "value": value})

    def coins_over(self, x, width_tiles, top, value=1):
        """A short row of coins floating just above a platform"""
        n = max(1, min(4, width_tiles))
        spacing = (width_tiles * T) // (n + 1)
        for i in range(n):
            self.coins.append({"x": x + spacing * (i + 1) - 8, "y": top - 34, "value": value})

    def enemy(self, kind, x, y, patrol=120):
        if kind == "ground":
            roll = self.rng.random()
            for variant, share in self.enemy_mix.items():
                if roll < share:
                    kind = variant
                    break
                roll -= share
        e = {"x": x, "y": y, "type": kind}
        if kind != "turret":
            e["patrol"] = patrol
        self.enemies.append(e)

    def spikes(self, x, count):
        for i in range(count):
            self.hazards.append({"x": x + i * T, "y": G, "type": "spike"})

    def maybe_health(self, x, y):
        """Health pickups get rarer as difficulty rises"""
        self.sections_since_health += 1
        if self.sections_since_health >= 2 + int(self.d * 2):
            self.powerups.append({"x": x, "y": y, "type": "health"})
            self.sections_since_health = 0

    def gap(self):
        """Horizontal gap between platforms: wider at higher difficulty"""
        return self.rng.randint(64, 96 + int(self.d * 64)) // 8 * 8

    def count(self, low, high):
        """Enemy count scaled by difficulty"""
        return low + int(round(self.d * (high - low)))

    def air_pocket(self, x, y, w=160, h=128):
        self.air_pockets.append({"x": x, "y": y, "w": w, "h": h})

    def current(self, x, y, w, h, dx):
        self.currents.append({"x": x, "y": y, "w": w, "h": h, "dx": dx})

    def area(self, kind, x0, x1):
        name = AREA_NAMES.get(kind, {}).get(self.theme) or AREA_NAMES.get(kind, {}).get("NATURE", kind.title())
        self.areas.append({"start": x0, "end": x1, "name": name})

    # --- sections ------------------------------------------------------------
    # Each section starts at self.x with the player on the ground and ends
    # with the player back on the ground at the new self.x.

    def s_flat(self):
        x0, w = self.x, self.rng.choice([768, 896, 1024])
        self.ground(x0, x0 + w)
        for i in range(self.count(1, 3)):
            self.enemy("ground", x0 + 200 + i * 250, G - 32, 100)
        for cx in range(x0 + 150, x0 + w - 100, 180):
            if self.rng.random() < 0.5:
                self.col(cx, G - 64, G - 32)  # crate stack to hop over
                self.coins.append({"x": cx + 8, "y": G - 110, "value": 1})
        self.coin_row(x0 + 96, G - 40, (w - 192) // 96, spacing=96)
        self.maybe_health(x0 + w - 150, G - 40)
        self.x = x0 + w

    def s_stairs(self):
        x0 = self.x
        steps = self.rng.randint(4, 6)
        rise = self.rng.choice([64, 80, 96])
        pitch = self.rng.choice([128, 160])
        w = 2 * steps * pitch + 256
        self.ground(x0, x0 + w)
        for i in range(steps):
            for side in (0, 1):
                x = x0 + 128 + i * pitch if side == 0 else x0 + w - 128 - (i + 1) * pitch
                y = G - rise * (i + 1)
                self.row(x, y, 3)
                self.coins_over(x, 3, y)
        top_x = x0 + 128 + (steps - 1) * pitch
        if self.d > 0.4:
            self.enemy("turret", top_x + 32, G - rise * steps - 32)
        self.enemy("ground", x0 + w // 2, G - 32, 150)
        self.x = x0 + w

    def s_pit(self):
        x0 = self.x
        self.ground(x0, x0 + 128)
        x = x0 + 128
        y = G - 64
        for _ in range(self.rng.randint(4, 7)):
            x += self.gap()
            y = max(G - 288, min(G - 32, y + self.rng.choice([-96, -64, -32, 0, 32, 64])))
            width = self.rng.randint(2, 4)
            self.row(x, y, width)
            self.coins_over(x, width, y)
            if self.rng.random() < 0.3 + self.d * 0.3:
                self.enemy("flying", x, y - 110, 120)
            x += width * T
        x += self.gap()
        x = x // T * T
        self.ground(x, x + 192)
        self.maybe_health(x + 64, G - 40)
        self.x = x + 192

    def s_moving(self):
        x0 = self.x
        self.ground(x0, x0 + 160)
        pit = 416
        center = x0 + 160 + pit // 2
        self.hazards.append({"x": center - 48, "y": G - 32, "type": "moving_platform", "width": 96})
        self.coin_row(center - 64, G - 110, 3, spacing=48, value=2)
        if self.d > 0.5:
            self.enemy("flying", center - 16, G - 220, 180)
        x = x0 + 160 + pit
        self.ground(x, x + 224)
        self.enemy("ground", x + 96, G - 32, 60)
        self.x = x + 224

    def s_spikes(self):
        x0, w = self.x, self.rng.choice([1024, 1152])
        self.ground(x0, x0 + w)
        x = x0 + 160
        while x < x0 + w - 256:
            run = self.rng.randint(2, 3 + int(self.d))
            self.spikes(x, run)
            if run >= 3 or self.rng.random() < 0.5:
                self.row(x, G - 128, run)  # stepping ledge above the spikes
                self.coins_over(x, run, G - 128, value=2)
            else:
                self.coins.append({"x": x + run * 16 - 8, "y": G - 150, "value": 2})
            x += run * T + self.rng.choice([160, 192, 224])
            if self.d > 0.55 and self.rng.random() < 0.5:
                self.enemy("ground", x - 96, G - 32, 40)
        self.x = x0 + w

    def s_canopy(self):
        """Trees: trunks to climb (wall jump) with canopies joined by branches"""
        x0 = self.x
        trees = self.rng.randint(3, 4)
        x = x0 + 128
        tops = []
        for i in range(trees):
            top = G - self.rng.choice([224, 256, 288, 320])
            self.col(x, top + T, G - T)                     # trunk
            self.row(x - 96, top, 7)                         # canopy
            self.row(x - 224, top + 96 + 32 * (i % 2), 2)    # side branch to start climbing
            self.coins_over(x - 96, 7, top, value=2)
            tops.append((x, top))
            if self.d > 0.35 and i % 2 == 1:
                self.enemy("ground", x - 64, top - 32, 60)
            x += 352 + self.gap()
        for (xa, ya), (xb, yb) in zip(tops, tops[1:]):
            mid = (xa + 128 + xb - 96) // 2 // T * T
            self.row(mid - 32, min(ya, yb) + 32, 2)          # branch between canopies
        end = x
        self.ground(x0, end + 128)
        self.enemy("flying", x0 + 400, G - 360, 200)
        self.maybe_health(end, G - 40)
        self.x = end + 128

    def s_tunnel(self):
        x0, w = self.x, self.rng.choice([1024, 1280])
        self.ground(x0, x0 + w)
        ceiling = G - 192
        self.row(x0 + 96, ceiling, (w - 192) // T)
        for i in range(self.count(1, 3)):
            self.enemy("ground", x0 + 250 + i * 300, G - 32, 120)
        for i in range(self.count(0, 3)):
            self.hazards.append({"x": x0 + 350 + i * 280, "y": ceiling + T, "type": "falling_block"})
        self.coin_row(x0 + 160, G - 40, (w - 320) // 64, spacing=64)
        self.maybe_health(x0 + w - 200, G - 40)
        self.x = x0 + w

    def s_tower(self):
        """Enter at the bottom, zigzag up the ledges, exit over the right wall"""
        x0 = self.x
        levels = 4 + int(self.d * 3)
        top = G - 80 * levels - 16
        left, right = x0 + 128, x0 + 128 + 320
        self.ground(x0, right + T)
        self.col(left, top - 96, G - 128)       # left wall, doorway at the bottom
        self.col(right, top + 64, G - T)        # right wall, open at the top
        for i in range(levels):
            y = G - 80 * (i + 1)
            x = left + T if i % 2 == 0 else right - 3 * T
            self.row(x, y, 3)
            self.coins.append({"x": x + 40, "y": y - 30, "value": 2})
        self.row(right - 3 * T, top, 8)          # exit ledge over the wall
        self.enemy("flying", left + 120, G - 200, 60)
        # stairs back down to the ground
        x, y = right + 5 * T, top
        while y < G - 96:
            x += 96
            y += 80
            self.row(x, y, 2)
        x += 128
        self.ground(right, x + 128)
        if self.d > 0.5:
            self.enemy("turret", right + 96, top - 32)
        self.x = x + 128

    def s_spire(self):
        """
        One tall column to wall-jump up its left face. Rest ledges are on the
        far (right) side for the way down: ledges on the climbing face would
        block the wall-jump climb from below.
        """
        x0 = self.x
        height = self.rng.choice([352, 416, 480])
        col_x = x0 + 320
        self.ground(x0, x0 + 896)
        self.col(col_x, G - height, G - T)
        for y in range(G - 128, G - height + 64, -128):
            self.tile(col_x + T, y)
            self.coins.append({"x": col_x - 22, "y": y - 30, "value": 2})  # along the climb
        self.coins.append({"x": col_x + 8, "y": G - height - 48, "value": 5})
        self.enemy("ground", x0 + 600, G - 32, 120)
        self.x = x0 + 896

    def s_turrets(self):
        x0, w = self.x, 1152
        self.ground(x0, x0 + w)
        for i in range(self.rng.randint(2, 3)):
            x = x0 + 192 + i * 352
            y = G - self.rng.choice([128, 160, 192])
            self.row(x, y, 4)
            self.enemy("turret", x + 48, y - 32)
            self.coins_over(x, 4, y, value=2)
            self.col(x + 224, G - 64, G - T)     # cover on the ground
        for i in range(self.count(1, 3)):
            self.enemy("ground", x0 + 300 + i * 300, G - 32, 90)
        self.maybe_health(x0 + w - 128, G - 40)
        self.x = x0 + w

    def s_asteroids(self):
        """Scattered small floating rocks over a pit, some moving"""
        x0 = self.x
        self.ground(x0, x0 + 128)
        x, y = x0 + 128, G - 96
        for i in range(self.rng.randint(6, 9)):
            x += self.gap() - 16
            y = max(G - 320, min(G - 64, y + self.rng.choice([-80, -48, 0, 48, 80])))
            if i % 4 == 3:
                self.hazards.append({"x": x + 110, "y": y, "type": "moving_platform", "width": 96})
                self.coins.append({"x": x + 150, "y": y - 40, "value": 2})
                x += 416 - 96
                continue
            width = self.rng.randint(1, 2)
            self.row(x, y, width)
            self.coins_over(x, width, y, value=2)
            if self.rng.random() < self.d * 0.5:
                self.enemy("flying", x, y - 120, 100)
            x += width * T
        x = (x + self.gap()) // T * T
        self.ground(x, x + 224)
        self.maybe_health(x + 64, G - 40)
        self.x = x + 224

    def exit(self, dest):
        x0 = self.x
        self.ground(x0, x0 + 640)
        self.row(x0 + 256, G - 96, 8)
        self.enemy("ground", x0 + 96, G - 32, 60)
        self.area("flat", x0, x0 + 640)
        self.areas[-1]["name"] = "Exit"
        portal = {"x": x0 + 352, "y": G - 96 - PORTAL_H, "dest": dest}
        self.x = x0 + 640
        return portal


def build_level(name, index, d, theme, sections, seed, act=None):
    """Generate one level's data dict"""
    options = LEVEL_OPTIONS.get(index, {})
    water = options.get("water", False)
    b = LevelBuilder(random.Random(seed), d, theme, ENEMY_MIX.get(act), water)
    b.ground(0, 512)
    b.coin_row(160, G - 40, 4, spacing=64)
    b.area("flat", 0, 512)
    b.areas[-1]["name"] = "Start"
    b.x = 512
    if water:
        b.air_pocket(200, G - 200)
    for n, kind in enumerate(sections):
        start = b.x
        getattr(b, "s_" + kind)()
        b.area(kind, start, b.x)
        if water:
            # an air pocket in every section, near its middle, above the path
            b.air_pocket((start + b.x) // 2 - 80, G - 240)
            if kind in ("moving", "pit"):
                b.current(start + 160, G - 320, b.x - start - 320, 280, 1.5)    # helps you across
            elif kind == "tunnel":
                b.current(start + 96, G - 160, b.x - start - 192, 160, -1.2)    # pushes back
    portal = b.exit(index + 1)
    data = {
        "name": name,
        "width": b.x,
        "height": 720,
        "theme": theme,
        "spawn_x": 100,
        "spawn_y": 500,
        "time_limit": "medium",
        "tiles": b.tiles,
        "enemies": b.enemies,
        "hazards": b.hazards,
        "coins": b.coins,
        "powerups": b.powerups,
        "keys": [],
        "portals": [portal],
        "areas": b.areas,
    }
    data.update({k: v for k, v in options.items()})
    if water:
        data["air_pockets"] = b.air_pockets
        data["currents"] = b.currents
    return data


def build_boss_arena(name, boss, theme, seed):
    """Single-screen arena: floor, walls, a few platforms and two health pickups"""
    rng = random.Random(seed)
    b = LevelBuilder(rng, 1.0, theme)
    b.ground(0, 1280)
    b.col(0, 0, G - T)
    b.col(1248, 0, G - T)
    layouts = [
        [(160, 540, 3), (1024, 540, 3), (320, 440, 3), (864, 440, 3), (576, 340, 4), (576, 540, 4)],
        [(128, 520, 4), (1024, 520, 4), (448, 420, 3), (736, 420, 3), (256, 320, 2), (960, 320, 2)],
        [(192, 540, 2), (1056, 540, 2), (384, 460, 3), (800, 460, 3), (576, 380, 4), (576, 250, 2)],
    ]
    for x, y, n in layouts[seed % len(layouts)]:
        b.row(x, y, n)
    b.powerups += [{"x": 100, "y": G - 60, "type": "health"}, {"x": 1150, "y": G - 60, "type": "health"}]
    return {
        "name": name, "boss": boss, "width": 1280, "height": 720, "theme": theme,
        "spawn_x": 200, "spawn_y": 580, "time_limit": "none",
        "tiles": b.tiles, "enemies": [], "hazards": [], "coins": [], "powerups": b.powerups,
        "keys": [], "portals": [], "areas": [{"start": 0, "end": 1280, "name": "Boss Arena"}],
    }


def generate(force=False, only=None, verbose=True):
    """Create (or with force, recreate) Act 2-4 levels and register them in acts.json"""
    from levels.level_loader import LevelLoader
    from tools.fix_coins import fix_coins
    from tools.level_checker import check_level

    acts = LevelLoader.load_acts()
    acts = [a for a in acts if a["number"] == 1]
    act1 = acts[0]
    index = len(act1["levels"])
    for spec in ACTS:
        files = []
        plans = [(name, d, spec.get("theme"), secs) if len(entry) == 3 else (name, d, entry[3], secs)
                 for entry in spec["levels"] for name, d, secs in [entry[:3]]]
        plans.append(spec["boss"])
        for plan in plans:
            filename = f"act{spec['number']}/level_{index:02d}.json"
            files.append(filename)
            exists = os.path.exists(os.path.join("levels", "data", filename))
            if (exists and not force) or (only and index not in only):
                index += 1
                continue
            if len(plan) == 2:  # boss arena
                name, boss = plan
                data = build_boss_arena(name, boss, spec["theme"], index)
            else:
                name, d, theme, sections = plan
                for attempt in range(40):
                    data = build_level(name, index, d, theme, sections, seed=index * 100 + attempt,
                                       act=spec["number"])
                    fix_coins(data)
                    result = check_level(data)
                    if result.portal_reached and not result.unreachable_coins():
                        break
                else:
                    raise RuntimeError(f"Could not generate a completable level {index} ({name})")
                if verbose:
                    print(f"  level {index:2d} {name:22s} d={d:.2f} width={data['width']:5d} "
                          f"coins={len(data['coins']):3d} enemies={len(data['enemies']):2d} (seed attempt {attempt})")
            LevelLoader.save_to_file(data, filename)
            index += 1
        acts.append({"number": spec["number"], "name": spec["name"], "theme": spec["theme"], "levels": files})
    LevelLoader.save_acts(acts)


def main():
    game_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.stdout.reconfigure(errors="replace")
    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    from tools.level_checker import init_headless
    init_headless(game_dir)
    args = sys.argv[1:]
    force = "--force" in args
    only = [int(a) for a in args if a.isdigit()]
    generate(force=force, only=only)
    print("acts.json updated")


if __name__ == "__main__":
    main()
