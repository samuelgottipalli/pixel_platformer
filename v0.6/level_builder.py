"""
Level Builder - edit the game's levels (levels/data/*/level_NN.json).

Run:  python level_builder.py            (opens the first level)
      python level_builder.py 12         (opens level 12)

Tools (keys or click the toolbar):
  1 Tile   2 Coin   3 Enemy   4 Hazard   5 Power-up   6 Portal   7 Spawn   8 Erase
  T              cycle the variant of the current tool (enemy / hazard / power-up type)
  Left mouse     place (drag to paint tiles/coins)     Right mouse   erase (drag)
  Arrows / WASD  scroll (hold Shift for faster)         Mouse wheel   scroll sideways
  Z              zoom (100% / 75% / 50%)                Minimap       click to jump
  PgUp / PgDn    previous / next level                  N             new level at the end of the act
  Ctrl+S save    Ctrl+Z undo    Tab  change theme     R  rename level
  C  check the level (exit reachable? which coins can't be collected?)
  F  fix coins automatically (moves unreachable coins to reachable spots)
  P  save and playtest this level in the game
  H  help      Esc / Q  quit
"""

import copy
import os
import subprocess
import sys

GAME_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, GAME_DIR)
os.chdir(GAME_DIR)
for _stream in (sys.stdout, sys.stderr):
    if _stream and hasattr(_stream, "reconfigure"):
        _stream.reconfigure(errors="replace")

import pygame  # noqa: E402

from config.settings import (  # noqa: E402
    CYAN, GRAY, GREEN, ORANGE, PURPLE, RED, THEME_TILE_COLORS, TILE_OUTLINE,
    UI_BG, UI_BORDER, UI_HIGHLIGHT, UI_SELECTED_BG, UI_TEXT, UI_TEXT_DIM, WHITE, YELLOW,
    update_screen_size,
)
from levels.level_loader import LevelLoader  # noqa: E402

W, H = 1280, 720
TILE = 32
GROUND = 640
TOOLBAR_H, STATUS_H, MINIMAP_H = 44, 28, 44
CANVAS_TOP, CANVAS_BOTTOM = TOOLBAR_H, H - STATUS_H - MINIMAP_H
THEMES = list(THEME_TILE_COLORS)

TOOLS = [
    ("tile", "Tile", None),
    ("coin", "Coin", None),
    ("enemy", "Enemy", ["ground", "flying", "turret"]),
    ("hazard", "Hazard", ["spike", "falling_block", "moving_platform"]),
    ("powerup", "Power-up", ["health", "double_jump", "speed", "invincible"]),
    ("portal", "Portal", None),
    ("spawn", "Spawn", None),
    ("erase", "Erase", None),
]
SIZES = {  # footprint of each object in level units
    "coin": (16, 16), "enemy": (32, 32), "hazard": (32, 32), "moving_platform": (96, 32),
    "powerup": (24, 24), "portal": (48, 64), "spawn": (28, 48),
}
ENEMY_COLORS = {"ground": RED, "flying": CYAN, "turret": ORANGE}
POWERUP_COLORS = {"health": GREEN, "double_jump": CYAN, "speed": YELLOW, "invincible": PURPLE}


class LevelBuilder:
    def __init__(self, start_index=0):
        pygame.init()
        os.environ.setdefault("SDL_RENDER_SCALE_QUALITY", "1")
        try:
            self.screen = pygame.display.set_mode((W, H), pygame.SCALED | pygame.RESIZABLE)
        except pygame.error:
            self.screen = pygame.display.set_mode((W, H))
        update_screen_size(W, H)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 22)
        self.font_big = pygame.font.Font(None, 30)

        self.acts = LevelLoader.load_acts()
        self.files = [lvl["file"] for act in self.acts for lvl in act["levels"]]
        self.tool = 0
        self.variant = {name: 0 for name, _, _ in TOOLS}
        self.zoom = 1.0
        self.cam_x = 0
        self.cam_y = 0
        self.undo_stack = []
        self.stroke_active = False
        self.message = ""
        self.message_timer = 0
        self.check_result = None
        self.show_help = False
        self.confirm = None  # pending confirmation: ("quit" | "switch", arg)
        self.text_input = None  # renaming
        self.running = True
        self.open_level(max(0, min(start_index, len(self.files) - 1)))

    # --- level management --------------------------------------------------
    def open_level(self, index):
        self.index = index
        self.data = LevelLoader.load_from_file(self.files[index])
        for key in ("tiles", "enemies", "hazards", "coins", "powerups", "keys", "portals"):
            self.data.setdefault(key, [])
        self.dirty = False
        self.undo_stack = []
        self.check_result = None
        self.cam_x, self.cam_y = 0, 0
        self.say(f"Opened {self.files[index]}")

    def act_of(self, index):
        for act in self.acts:
            if any(lvl["index"] == index for lvl in act["levels"]):
                return act
        return self.acts[-1]

    def save(self):
        right = max([t["x"] + TILE for t in self.data["tiles"]] + [1280])
        self.data["width"] = max(right, 1280)
        LevelLoader.save_to_file(self.data, self.files[self.index])
        self.dirty = False
        self.say(f"Saved {self.files[self.index]}")

    def new_level(self):
        """Append a new level (ground + portal) to the current level's act"""
        act = self.act_of(self.index)
        if any(lvl.get("boss") for lvl in act["levels"]):
            self.say("This act ends with a boss; add levels in the builder's act before it by editing acts.json")
        new_index = len(self.files)
        filename = f"act{act['number']}/level_{new_index:02d}.json"
        data = {
            "name": "New Level", "width": 3200, "height": 720, "theme": act.get("theme", "SCIFI"),
            "spawn_x": 100, "spawn_y": 500, "time_limit": "medium",
            "tiles": [{"x": x, "y": GROUND, "solid": True} for x in range(0, 3200, TILE)],
            "enemies": [], "hazards": [], "coins": [], "powerups": [], "keys": [],
            "portals": [{"x": 3000, "y": GROUND - 64, "dest": new_index + 1}],
        }
        LevelLoader.save_to_file(data, filename)
        raw_acts = LevelLoader.load_acts()
        for a in raw_acts:
            if a["number"] == act["number"]:
                a["levels"].append({"file": filename})
        LevelLoader.save_acts(raw_acts)
        self.acts = LevelLoader.load_acts()
        self.files = [lvl["file"] for a in self.acts for lvl in a["levels"]]
        self.open_level(self.files.index(filename))
        self.say(f"Created {filename} (appended to Act {act['number']}; check portal destinations)")

    # --- coordinates ---------------------------------------------------------
    def to_screen(self, x, y):
        return (int((x - self.cam_x) * self.zoom), int((y - self.cam_y) * self.zoom) + CANVAS_TOP)

    def to_world(self, sx, sy):
        return (sx / self.zoom + self.cam_x, (sy - CANVAS_TOP) / self.zoom + self.cam_y)

    def screen_rect(self, x, y, w, h):
        sx, sy = self.to_screen(x, y)
        return pygame.Rect(sx, sy, max(1, int(w * self.zoom)), max(1, int(h * self.zoom)))

    # --- editing ---------------------------------------------------------------
    def snapshot(self):
        self.undo_stack.append(copy.deepcopy(self.data))
        del self.undo_stack[:-60]

    def undo(self):
        if self.undo_stack:
            self.data = self.undo_stack.pop()
            self.dirty = True
            self.check_result = None
            self.say("Undo")

    def place(self, wx, wy):
        name = TOOLS[self.tool][0]
        variant = TOOLS[self.tool][2][self.variant[name]] if TOOLS[self.tool][2] else None
        gx, gy = int(wx // TILE * TILE), int(wy // TILE * TILE)
        d = self.data
        if name == "tile":
            if not any(t["x"] == gx and t["y"] == gy for t in d["tiles"]):
                d["tiles"].append({"x": gx, "y": gy, "solid": True})
                return True
        elif name == "coin":
            cx, cy = int(wx // 16 * 16), int(wy // 16 * 16)
            if not any(abs(c["x"] - cx) < 16 and abs(c["y"] - cy) < 16 for c in d["coins"]):
                d["coins"].append({"x": cx, "y": cy, "value": 1})
                return True
        elif name == "enemy":
            e = {"x": gx, "y": gy, "type": variant}
            if variant != "turret":
                e["patrol"] = 120
            d["enemies"].append(e)
            return True
        elif name == "hazard":
            h = {"x": gx, "y": gy, "type": variant}
            if variant == "moving_platform":
                h["width"] = 96
            d["hazards"].append(h)
            return True
        elif name == "powerup":
            d["powerups"].append({"x": gx + 4, "y": gy + 4, "type": variant})
            return True
        elif name == "portal":
            d["portals"] = [{"x": gx, "y": gy - 32, "dest": self.index + 1}]
            return True
        elif name == "spawn":
            d["spawn_x"], d["spawn_y"] = gx, gy - 16
            return True
        return False

    def erase(self, wx, wy):
        point = (wx, wy)
        d = self.data
        for key in ("coins", "powerups", "enemies", "hazards", "portals", "tiles"):
            for obj in reversed(d[key]):
                if self.object_rect(key, obj).collidepoint(point):
                    d[key].remove(obj)
                    return True
        return False

    @staticmethod
    def object_rect(key, obj):
        if key == "tiles":
            return pygame.Rect(obj["x"], obj["y"], TILE, TILE)
        if key == "coins":
            size = SIZES["coin"]
        elif key == "hazards":
            size = SIZES["moving_platform"] if obj["type"] == "moving_platform" else SIZES["hazard"]
        elif key == "portals":
            size = SIZES["portal"]
        elif key == "powerups":
            size = SIZES["powerup"]
        else:
            size = SIZES["enemy"]
        return pygame.Rect(obj["x"], obj["y"], *size)

    # --- tools ---------------------------------------------------------------
    def run_check(self):
        from tools.level_checker import check_level
        self.say("Checking level (exit reachable? coins collectible?)...")
        self.draw()
        pygame.display.flip()
        data = LevelLoader.fix_spike_positions(copy.deepcopy(self.data))
        result = check_level(data)
        self.check_result = {
            "portal": result.portal_reached, "has_portal": bool(result.portals),
            "bad_coins": result.unreachable_coins(),
            "spots": list(result.spot_positions.values()),
        }
        portal = ("exit REACHABLE" if result.portal_reached else "exit UNREACHABLE") if result.portals else "no exit"
        self.say(f"Check: {portal}, {len(result.coins_seen)}/{len(result.coins)} coins collectible "
                 f"(red = unreachable, green = where the player can stand)", 600)

    def run_fix_coins(self):
        from tools.fix_coins import fix_coins
        self.say("Fixing coins...")
        self.draw()
        pygame.display.flip()
        self.snapshot()
        moved, removed = fix_coins(self.data)
        self.dirty = self.dirty or bool(moved or removed)
        self.check_result = None
        self.say(f"Coins fixed: moved {moved}, removed {removed}", 400)

    def playtest(self):
        self.save()
        subprocess.Popen([sys.executable, os.path.join(GAME_DIR, "main.py"), "--playtest", str(self.index)],
                         cwd=GAME_DIR)
        self.say(f"Playtest started for level {self.index} (close the game window to come back)")

    def say(self, text, frames=240):
        self.message, self.message_timer = text, frames

    # --- input -----------------------------------------------------------------
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.request_quit()
            elif event.type == pygame.KEYDOWN:
                self.handle_key(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_down(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.stroke_active = False
            elif event.type == pygame.MOUSEMOTION and self.stroke_active:
                self.paint(event.pos, event.buttons, dragging=True)
            elif event.type == pygame.MOUSEWHEEL:
                self.cam_x = max(0, self.cam_x - event.y * 128 / self.zoom + event.x * 128 / self.zoom)

    def handle_key(self, event):
        ctrl = event.mod & pygame.KMOD_CTRL
        if self.text_input is not None:
            if event.key == pygame.K_RETURN:
                self.data["name"] = self.text_input.strip() or self.data.get("name", "")
                self.text_input, self.dirty = None, True
            elif event.key == pygame.K_ESCAPE:
                self.text_input = None
            elif event.key == pygame.K_BACKSPACE:
                self.text_input = self.text_input[:-1]
            elif event.unicode and event.unicode.isprintable() and len(self.text_input) < 30:
                self.text_input += event.unicode
            return
        if self.confirm:
            kind, arg = self.confirm
            self.confirm = None
            if event.key in (pygame.K_y, pygame.K_RETURN):
                if kind == "quit":
                    self.running = False
                else:
                    self.open_level(arg)
            else:
                self.say("Cancelled")
            return
        if ctrl and event.key == pygame.K_s:
            self.save()
        elif ctrl and event.key == pygame.K_z:
            self.undo()
        elif pygame.K_1 <= event.key <= pygame.K_8:
            self.tool = event.key - pygame.K_1
        elif event.key == pygame.K_t:
            name, _, variants = TOOLS[self.tool]
            if variants:
                self.variant[name] = (self.variant[name] + 1) % len(variants)
        elif event.key == pygame.K_z:
            self.zoom = {1.0: 0.75, 0.75: 0.5, 0.5: 1.0}[self.zoom]
        elif event.key == pygame.K_TAB:
            theme = self.data.get("theme", "SCIFI")
            self.data["theme"] = THEMES[(THEMES.index(theme) + 1) % len(THEMES)] if theme in THEMES else THEMES[0]
            self.dirty = True
        elif event.key == pygame.K_r:
            self.text_input = self.data.get("name", "")
        elif event.key == pygame.K_PAGEDOWN:
            self.switch_level(self.index + 1)
        elif event.key == pygame.K_PAGEUP:
            self.switch_level(self.index - 1)
        elif event.key == pygame.K_n:
            self.new_level()
        elif event.key == pygame.K_c:
            self.run_check()
        elif event.key == pygame.K_f:
            self.run_fix_coins()
        elif event.key == pygame.K_p:
            self.playtest()
        elif event.key == pygame.K_h:
            self.show_help = not self.show_help
        elif event.key in (pygame.K_ESCAPE, pygame.K_q):
            self.request_quit()

    def switch_level(self, index):
        if not 0 <= index < len(self.files):
            return
        if self.dirty:
            self.confirm = ("switch", index)
            self.say("Unsaved changes - press Y to discard and switch, any other key to stay", 100000)
        else:
            self.open_level(index)

    def request_quit(self):
        if self.dirty:
            self.confirm = ("quit", None)
            self.say("Unsaved changes - press Y to quit without saving (Ctrl+S saves), any other key to stay", 100000)
        else:
            self.running = False

    def handle_mouse_down(self, event):
        x, y = event.pos
        if y < TOOLBAR_H:
            for i, rect in enumerate(self.toolbar_rects()):
                if rect.collidepoint(event.pos):
                    if event.button == 1:
                        self.tool = i
                    name, _, variants = TOOLS[i]
                    if event.button == 3 and variants:
                        self.variant[name] = (self.variant[name] + 1) % len(variants)
            return
        if y >= H - STATUS_H - MINIMAP_H and y < H - STATUS_H:
            width = max(self.data.get("width", 1280), 1280)
            self.cam_x = max(0, x / W * width - W / self.zoom / 2)
            return
        if event.button in (1, 3):
            self.snapshot()
            self.stroke_active = True
            buttons = (event.button == 1, False, event.button == 3)
            if not self.paint(event.pos, buttons):
                self.undo_stack.pop()  # nothing changed

    def paint(self, pos, buttons, dragging=False):
        if not CANVAS_TOP <= pos[1] < CANVAS_BOTTOM:
            return False
        wx, wy = self.to_world(*pos)
        changed = False
        erasing = buttons[2] or TOOLS[self.tool][0] == "erase"
        if erasing:
            changed = self.erase(wx, wy)
        elif buttons[0]:
            # Tiles and coins paint while dragging; other objects place once per click
            if not dragging or TOOLS[self.tool][0] in ("tile", "coin"):
                changed = self.place(wx, wy)
        if changed:
            self.dirty = True
            self.check_result = None
        return changed

    def update(self):
        keys = pygame.key.get_pressed()
        speed = (40 if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT] else 14) / self.zoom
        if self.text_input is None and not self.confirm:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.cam_x = max(0, self.cam_x - speed)
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.cam_x += speed
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.cam_y = max(-200, self.cam_y - speed)
            if keys[pygame.K_DOWN] or keys[pygame.K_s] and not pygame.key.get_mods() & pygame.KMOD_CTRL:
                self.cam_y = min(400, self.cam_y + speed)
        if self.message_timer > 0:
            self.message_timer -= 1

    # --- drawing ---------------------------------------------------------------
    def toolbar_rects(self):
        return [pygame.Rect(8 + i * 112, 6, 106, 32) for i in range(len(TOOLS))]

    def draw(self):
        self.screen.fill((16, 16, 26))
        self.draw_level()
        self.draw_toolbar()
        self.draw_minimap()
        self.draw_status()
        if self.show_help:
            self.draw_help()

    def draw_level(self):
        d = self.data
        canvas = pygame.Rect(0, CANVAS_TOP, W, CANVAS_BOTTOM - CANVAS_TOP)
        self.screen.set_clip(canvas)
        # grid
        step = TILE * self.zoom
        ox = -(self.cam_x * self.zoom) % step
        for i in range(int(W / step) + 2):
            x = ox + i * step
            pygame.draw.line(self.screen, (26, 26, 40), (x, CANVAS_TOP), (x, CANVAS_BOTTOM))
        # level bounds
        top_left = self.to_screen(0, 0)
        bottom_right = self.to_screen(d.get("width", 1280), 720)
        pygame.draw.rect(self.screen, (60, 60, 90),
                         pygame.Rect(top_left, (bottom_right[0] - top_left[0], bottom_right[1] - top_left[1])), 1)
        # areas
        for area in d.get("areas", []):
            sx, _ = self.to_screen(area["start"], 0)
            pygame.draw.line(self.screen, (50, 50, 80), (sx, CANVAS_TOP), (sx, CANVAS_BOTTOM))
            self.screen.blit(self.font.render(area["name"], True, (90, 90, 130)), (sx + 4, CANVAS_TOP + 4))

        tile_color = THEME_TILE_COLORS.get(d.get("theme", "SCIFI"), (100, 100, 120))
        view_left, _ = self.to_world(0, CANVAS_TOP)
        view_right, _ = self.to_world(W, CANVAS_TOP)
        for t in d["tiles"]:
            if view_left - TILE <= t["x"] <= view_right:
                r = self.screen_rect(t["x"], t["y"], TILE, TILE)
                pygame.draw.rect(self.screen, tile_color, r)
                pygame.draw.rect(self.screen, TILE_OUTLINE, r, 1)
        for h in d["hazards"]:
            if h["type"] == "moving_platform":
                r = self.screen_rect(h["x"] - 150, h["y"], 96 + 300, 32)
                pygame.draw.rect(self.screen, (40, 70, 90), r, 1)  # travel range
                pygame.draw.rect(self.screen, CYAN, self.screen_rect(h["x"], h["y"], 96, 32))
            elif h["type"] == "spike":
                r = self.screen_rect(h["x"], min(h["y"], 608), 32, 32)
                pygame.draw.polygon(self.screen, RED, [r.bottomleft, r.midtop, r.bottomright])
            else:
                pygame.draw.rect(self.screen, ORANGE, self.screen_rect(h["x"], h["y"], 32, 32))
        bad = {(c[0], c[1]) for c in self.check_result["bad_coins"]} if self.check_result else set()
        for c in d["coins"]:
            r = self.screen_rect(c["x"], c["y"], 16, 16)
            color = RED if (c["x"], c["y"]) in bad else YELLOW
            pygame.draw.circle(self.screen, color, r.center, max(2, r.width // 2))
            if (c["x"], c["y"]) in bad:
                pygame.draw.circle(self.screen, RED, r.center, r.width + 6, 2)
        for p in d["powerups"]:
            pygame.draw.rect(self.screen, POWERUP_COLORS.get(p["type"], GREEN), self.screen_rect(p["x"], p["y"], 24, 24))
        for e in d["enemies"]:
            r = self.screen_rect(e["x"], e["y"], 32, 32)
            color = ENEMY_COLORS.get(e["type"], RED)
            pygame.draw.rect(self.screen, color, r, 2)
            if e["type"] != "turret" and e.get("patrol"):
                pr = self.screen_rect(e["x"] - e["patrol"], e["y"] + 14, 2 * e["patrol"] + 32, 4)
                pygame.draw.rect(self.screen, color, pr, 1)
            self.screen.blit(self.font.render(e["type"][0].upper(), True, color), (r.x + 4, r.y + 4))
        for p in d["portals"]:
            r = self.screen_rect(p["x"], p["y"], 48, 64)
            pygame.draw.rect(self.screen, PURPLE, r, 3)
            self.screen.blit(self.font.render(f"-> {p['dest']}", True, PURPLE), (r.x, r.y - 16))
        r = self.screen_rect(d.get("spawn_x", 100), d.get("spawn_y", 500), 28, 48)
        pygame.draw.rect(self.screen, WHITE, r, 2)
        self.screen.blit(self.font.render("START", True, WHITE), (r.x - 8, r.y - 16))
        if self.check_result:
            for x, y in self.check_result["spots"]:
                if view_left - 50 <= x <= view_right:
                    sr = self.screen_rect(x, y + 44, 28, 4)
                    pygame.draw.rect(self.screen, (60, 160, 90), sr)
        # cursor preview
        mx, my = pygame.mouse.get_pos()
        if CANVAS_TOP <= my < CANVAS_BOTTOM:
            wx, wy = self.to_world(mx, my)
            grid = 16 if TOOLS[self.tool][0] == "coin" else TILE
            r = self.screen_rect(int(wx // grid * grid), int(wy // grid * grid), grid, grid)
            pygame.draw.rect(self.screen, UI_HIGHLIGHT, r, 1)
        self.screen.set_clip(None)

    def draw_toolbar(self):
        pygame.draw.rect(self.screen, UI_BG, (0, 0, W, TOOLBAR_H))
        for i, (rect, (name, label, variants)) in enumerate(zip(self.toolbar_rects(), TOOLS)):
            active = i == self.tool
            pygame.draw.rect(self.screen, UI_SELECTED_BG if active else UI_BG, rect, border_radius=5)
            pygame.draw.rect(self.screen, UI_HIGHLIGHT if active else UI_BORDER, rect, 2, border_radius=5)
            text = f"{i + 1} {label}"
            if variants:
                text = f"{i + 1} {variants[self.variant[name]].replace('_', ' ')}"
            surf = self.font.render(text, True, UI_HIGHLIGHT if active else UI_TEXT)
            self.screen.blit(surf, (rect.centerx - surf.get_width() // 2, rect.centery - surf.get_height() // 2))
        title = f"{'*' if self.dirty else ''}L{self.index} {self.data.get('name', '')} [{self.data.get('theme', '')}]"
        if self.text_input is not None:
            title = f"Rename: {self.text_input}_  (Enter to keep, Esc to cancel)"
        surf = self.font_big.render(title, True, YELLOW if self.dirty else UI_TEXT)
        self.screen.blit(surf, (W - surf.get_width() - 12, 12))

    def draw_minimap(self):
        top = H - STATUS_H - MINIMAP_H
        pygame.draw.rect(self.screen, (12, 12, 20), (0, top, W, MINIMAP_H))
        width = max(self.data.get("width", 1280), 1280)
        sx, sy = W / width, MINIMAP_H / 720
        for t in self.data["tiles"]:
            self.screen.fill((90, 90, 120), (int(t["x"] * sx), top + int(t["y"] * sy), max(1, int(TILE * sx)), 2))
        for c in self.data["coins"]:
            self.screen.fill(YELLOW, (int(c["x"] * sx), top + int(c["y"] * sy), 1, 1))
        view = pygame.Rect(int(self.cam_x * sx), top, int(W / self.zoom * sx), MINIMAP_H)
        pygame.draw.rect(self.screen, UI_HIGHLIGHT, view, 1)

    def draw_status(self):
        pygame.draw.rect(self.screen, UI_BG, (0, H - STATUS_H, W, STATUS_H))
        mx, my = pygame.mouse.get_pos()
        wx, wy = self.to_world(mx, my)
        d = self.data
        info = (f"x {int(wx)}  y {int(wy)}   zoom {int(self.zoom * 100)}%   tiles {len(d['tiles'])}  "
                f"coins {len(d['coins'])}  enemies {len(d['enemies'])}   H: help")
        self.screen.blit(self.font.render(info, True, UI_TEXT_DIM), (10, H - STATUS_H + 6))
        if self.message_timer > 0:
            surf = self.font.render(self.message, True, YELLOW)
            self.screen.blit(surf, (W - surf.get_width() - 10, H - STATUS_H + 6))

    def draw_help(self):
        lines = [line for line in __doc__.strip().splitlines()[4:] if line.strip()]
        box = pygame.Rect(140, 80, 1000, 34 + 24 * len(lines))
        overlay = pygame.Surface(box.size)
        overlay.fill((20, 20, 32))
        overlay.set_alpha(235)
        self.screen.blit(overlay, box.topleft)
        pygame.draw.rect(self.screen, UI_HIGHLIGHT, box, 2)
        for i, line in enumerate(lines):
            self.screen.blit(self.font.render(line, True, UI_TEXT), (box.x + 16, box.y + 16 + i * 24))

    def run(self):
        pygame.display.set_caption("Level Builder")
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()


def main():
    start = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 0
    LevelBuilder(start).run()


if __name__ == "__main__":
    main()
