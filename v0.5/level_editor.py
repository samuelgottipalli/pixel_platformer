"""
Simple Level Editor Tool
Run this separately from the main game: python level_editor.py
"""

import json
import sys

import pygame

from config.settings import (BLACK, BLUE, CYAN, FPS, GRAY, GREEN, ORANGE,
                             PURPLE, RED, SCREEN_HEIGHT, SCREEN_WIDTH,
                             TILE_SIZE, WHITE, YELLOW)


class LevelEditor:
    """Simple visual level editor"""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Level Editor")
        self.clock = pygame.time.Clock()
        self.running = True

        # Editor state
        self.camera_x = 0
        self.camera_y = 0
        self.grid_size = TILE_SIZE
        self.level_width = 3200
        self.level_height = 720

        # Current tool
        self.mode = "tile"  # 'tile', 'enemy', 'coin', 'powerup', 'key', 'hazard', 'portal', 'spawn'
        self.selected_enemy_type = "ground"
        self.selected_hazard_type = "spike"
        self.selected_powerup_type = "health"
        self.selected_theme = "SCIFI"
        self.time_limit = "medium"  # 'short', 'medium', 'long', 'none'

        # Level data
        self.tiles = []
        self.enemies = []
        self.coins = []
        self.powerups = []
        self.keys = []
        self.hazards = []
        self.portals = []
        self.spawn_x = 100
        self.spawn_y = 500

        # Fonts
        self.font = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 18)

        # UI
        self.show_help = True

    def run(self):
        """Main editor loop"""
        while self.running:
            self._handle_events()
            self._update()
            self._draw()
            self.clock.tick(FPS)

        pygame.quit()

    def _handle_events(self):
        """Handle input events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                self._handle_keypress(event.key)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse_click(event.button, event.pos)

    def _handle_keypress(self, key):
        """Handle keyboard input"""
        # Mode selection
        if key == pygame.K_1:
            self.mode = "tile"
        elif key == pygame.K_2:
            self.mode = "enemy"
        elif key == pygame.K_3:
            self.mode = "coin"
        elif key == pygame.K_4:
            self.mode = "powerup"
        elif key == pygame.K_5:
            self.mode = "hazard"
        elif key == pygame.K_6:
            self.mode = "portal"
        elif key == pygame.K_7:
            self.mode = "key"
        elif key == pygame.K_8:
            self.mode = "spawn"

        # Sub-selections
        elif key == pygame.K_e and self.mode == "enemy":
            types = ["ground", "flying", "turret"]
            idx = (types.index(self.selected_enemy_type) + 1) % len(types)
            self.selected_enemy_type = types[idx]
        elif key == pygame.K_h and self.mode == "hazard":
            types = ["spike", "falling_block", "moving_platform"]
            idx = (types.index(self.selected_hazard_type) + 1) % len(types)
            self.selected_hazard_type = types[idx]
        elif key == pygame.K_p and self.mode == "powerup":
            types = ["health", "speed", "invincible", "double_jump"]
            idx = (types.index(self.selected_powerup_type) + 1) % len(types)
            self.selected_powerup_type = types[idx]

        # Theme selection
        elif key == pygame.K_t:
            themes = ["SCIFI", "NATURE", "SPACE", "UNDERGROUND", "UNDERWATER"]
            idx = (themes.index(self.selected_theme) + 1) % len(themes)
            self.selected_theme = themes[idx]

        # Time limit
        elif key == pygame.K_l:
            limits = ["short", "medium", "long", "none"]
            idx = (limits.index(self.time_limit) + 1) % len(limits)
            self.time_limit = limits[idx]

        # Save/Load
        elif key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
            self._save_level()
        elif key == pygame.K_o and pygame.key.get_mods() & pygame.KMOD_CTRL:
            self._load_level()

        # Clear
        elif key == pygame.K_c and pygame.key.get_mods() & pygame.KMOD_CTRL:
            self._clear_all()

        # Help toggle
        elif key == pygame.K_F1:
            self.show_help = not self.show_help

        # Camera movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.camera_x -= 10
        if keys[pygame.K_RIGHT]:
            self.camera_x += 10
        if keys[pygame.K_UP]:
            self.camera_y -= 10
        if keys[pygame.K_DOWN]:
            self.camera_y += 10

        # Clamp camera
        self.camera_x = max(0, min(self.camera_x, self.level_width - SCREEN_WIDTH))
        self.camera_y = max(0, min(self.camera_y, self.level_height - SCREEN_HEIGHT))

    def _handle_mouse_click(self, button, pos):
        """Handle mouse clicks"""
        # Convert screen to world coordinates
        world_x = pos[0] + self.camera_x
        world_y = pos[1] + self.camera_y

        # Snap to grid
        grid_x = (world_x // self.grid_size) * self.grid_size
        grid_y = (world_y // self.grid_size) * self.grid_size

        if button == 1:  # Left click - place
            self._place_object(grid_x, grid_y)
        elif button == 3:  # Right click - remove
            self._remove_object(grid_x, grid_y)

    def _place_object(self, x, y):
        """Place object at position"""
        if self.mode == "tile":
            # Check if tile already exists
            for tile in self.tiles:
                if tile["x"] == x and tile["y"] == y:
                    return
            self.tiles.append({"x": x, "y": y, "solid": True})

        elif self.mode == "enemy":
            self.enemies.append(
                {"x": x, "y": y, "type": self.selected_enemy_type, "patrol": 200}
            )

        elif self.mode == "coin":
            self.coins.append({"x": x, "y": y, "value": 1})

        elif self.mode == "powerup":
            self.powerups.append({"x": x, "y": y, "type": self.selected_powerup_type})

        elif self.mode == "hazard":
            width = 96 if self.selected_hazard_type == "moving_platform" else 32
            self.hazards.append(
                {
                    "x": x,
                    "y": y,
                    "type": self.selected_hazard_type,
                    "width": width,
                    "height": 32,
                }
            )

        elif self.mode == "portal":
            dest = len(self.portals)  # Default to next level
            self.portals.append({"x": x, "y": y, "dest": dest})

        elif self.mode == "key":
            colors = [[255, 0, 0], [0, 255, 0], [0, 0, 255], [255, 255, 0]]
            color = colors[len(self.keys) % len(colors)]
            self.keys.append({"x": x, "y": y, "color": color})

        elif self.mode == "spawn":
            self.spawn_x = x
            self.spawn_y = y

    def _remove_object(self, x, y):
        """Remove object at position"""
        tolerance = self.grid_size

        if self.mode == "tile":
            self.tiles = [
                t
                for t in self.tiles
                if not (abs(t["x"] - x) < tolerance and abs(t["y"] - y) < tolerance)
            ]
        elif self.mode == "enemy":
            self.enemies = [
                e
                for e in self.enemies
                if not (abs(e["x"] - x) < tolerance and abs(e["y"] - y) < tolerance)
            ]
        elif self.mode == "coin":
            self.coins = [
                c
                for c in self.coins
                if not (abs(c["x"] - x) < tolerance and abs(c["y"] - y) < tolerance)
            ]
        elif self.mode == "powerup":
            self.powerups = [
                p
                for p in self.powerups
                if not (abs(p["x"] - x) < tolerance and abs(p["y"] - y) < tolerance)
            ]
        elif self.mode == "hazard":
            self.hazards = [
                h
                for h in self.hazards
                if not (abs(h["x"] - x) < tolerance and abs(h["y"] - y) < tolerance)
            ]
        elif self.mode == "portal":
            self.portals = [
                p
                for p in self.portals
                if not (abs(p["x"] - x) < tolerance and abs(p["y"] - y) < tolerance)
            ]
        elif self.mode == "key":
            self.keys = [
                k
                for k in self.keys
                if not (abs(k["x"] - x) < tolerance and abs(k["y"] - y) < tolerance)
            ]

    def _update(self):
        """Update editor state"""
        pass

    def _draw(self):
        """Draw editor"""
        self.screen.fill(BLACK)

        # Draw grid
        self._draw_grid()

        # Draw objects
        self._draw_tiles()
        self._draw_enemies()
        self._draw_coins()
        self._draw_powerups()
        self._draw_hazards()
        self._draw_portals()
        self._draw_keys()
        self._draw_spawn()

        # Draw UI
        self._draw_ui()

        if self.show_help:
            self._draw_help()

        pygame.display.flip()

    def _draw_grid(self):
        """Draw grid lines"""
        for x in range(0, self.level_width, self.grid_size):
            screen_x = x - self.camera_x
            if -self.grid_size < screen_x < SCREEN_WIDTH:
                pygame.draw.line(
                    self.screen, (30, 30, 30), (screen_x, 0), (screen_x, SCREEN_HEIGHT)
                )
        for y in range(0, self.level_height, self.grid_size):
            screen_y = y - self.camera_y
            if -self.grid_size < screen_y < SCREEN_HEIGHT:
                pygame.draw.line(
                    self.screen, (30, 30, 30), (0, screen_y), (SCREEN_WIDTH, screen_y)
                )

    def _draw_tiles(self):
        """Draw tiles"""
        for tile in self.tiles:
            x = tile["x"] - self.camera_x
            y = tile["y"] - self.camera_y
            if (
                -self.grid_size < x < SCREEN_WIDTH
                and -self.grid_size < y < SCREEN_HEIGHT
            ):
                pygame.draw.rect(
                    self.screen, GRAY, (x, y, self.grid_size, self.grid_size)
                )
                pygame.draw.rect(
                    self.screen, WHITE, (x, y, self.grid_size, self.grid_size), 1
                )

    def _draw_enemies(self):
        """Draw enemies"""
        colors = {"ground": RED, "flying": CYAN, "turret": ORANGE}
        for enemy in self.enemies:
            x = enemy["x"] - self.camera_x
            y = enemy["y"] - self.camera_y
            if (
                -self.grid_size < x < SCREEN_WIDTH
                and -self.grid_size < y < SCREEN_HEIGHT
            ):
                color = colors.get(enemy["type"], RED)
                pygame.draw.rect(
                    self.screen, color, (x, y, self.grid_size, self.grid_size)
                )
                pygame.draw.rect(
                    self.screen, WHITE, (x, y, self.grid_size, self.grid_size), 2
                )

    def _draw_coins(self):
        """Draw coins"""
        for coin in self.coins:
            x = coin["x"] - self.camera_x + self.grid_size // 2
            y = coin["y"] - self.camera_y + self.grid_size // 2
            if (
                -self.grid_size < x < SCREEN_WIDTH
                and -self.grid_size < y < SCREEN_HEIGHT
            ):
                pygame.draw.circle(self.screen, YELLOW, (x, y), 10)

    def _draw_powerups(self):
        """Draw powerups"""
        for powerup in self.powerups:
            x = powerup["x"] - self.camera_x
            y = powerup["y"] - self.camera_y
            if (
                -self.grid_size < x < SCREEN_WIDTH
                and -self.grid_size < y < SCREEN_HEIGHT
            ):
                pygame.draw.rect(self.screen, GREEN, (x + 4, y + 4, 24, 24))

    def _draw_hazards(self):
        """Draw hazards"""
        for hazard in self.hazards:
            x = hazard["x"] - self.camera_x
            y = hazard["y"] - self.camera_y
            w = hazard.get("width", 32)
            h = hazard.get("height", 32)
            if -w < x < SCREEN_WIDTH and -h < y < SCREEN_HEIGHT:
                if hazard["type"] == "spike":
                    points = [(x, y + h), (x + w // 2, y), (x + w, y + h)]
                    pygame.draw.polygon(self.screen, RED, points)
                elif hazard["type"] == "moving_platform":
                    pygame.draw.rect(self.screen, BLUE, (x, y, w, h))
                else:
                    pygame.draw.rect(self.screen, ORANGE, (x, y, w, h))

    def _draw_portals(self):
        """Draw portals"""
        for portal in self.portals:
            x = portal["x"] - self.camera_x
            y = portal["y"] - self.camera_y
            if -48 < x < SCREEN_WIDTH and -64 < y < SCREEN_HEIGHT:
                pygame.draw.ellipse(self.screen, PURPLE, (x, y, 48, 64), 3)

    def _draw_keys(self):
        """Draw keys"""
        for key in self.keys:
            x = key["x"] - self.camera_x
            y = key["y"] - self.camera_y
            if (
                -self.grid_size < x < SCREEN_WIDTH
                and -self.grid_size < y < SCREEN_HEIGHT
            ):
                color = tuple(key["color"])
                pygame.draw.circle(self.screen, color, (x + 12, y + 12), 8)

    def _draw_spawn(self):
        """Draw spawn point"""
        x = self.spawn_x - self.camera_x
        y = self.spawn_y - self.camera_y
        if -self.grid_size < x < SCREEN_WIDTH and -self.grid_size < y < SCREEN_HEIGHT:
            pygame.draw.circle(self.screen, GREEN, (x + 16, y + 16), 16, 3)
            pygame.draw.line(self.screen, GREEN, (x + 16, y), (x + 16, y + 32), 2)
            pygame.draw.line(self.screen, GREEN, (x, y + 16), (x + 32, y + 16), 2)

    def _draw_ui(self):
        """Draw UI panel"""
        # Mode indicator
        mode_text = self.font.render(f"Mode: {self.mode.upper()}", True, YELLOW)
        self.screen.blit(mode_text, (10, 10))

        # Sub-mode
        if self.mode == "enemy":
            sub_text = self.font_small.render(
                f"Type: {self.selected_enemy_type} (E to cycle)", True, WHITE
            )
            self.screen.blit(sub_text, (10, 35))
        elif self.mode == "hazard":
            sub_text = self.font_small.render(
                f"Type: {self.selected_hazard_type} (H to cycle)", True, WHITE
            )
            self.screen.blit(sub_text, (10, 35))
        elif self.mode == "powerup":
            sub_text = self.font_small.render(
                f"Type: {self.selected_powerup_type} (P to cycle)", True, WHITE
            )
            self.screen.blit(sub_text, (10, 35))

        # Theme
        theme_text = self.font_small.render(
            f"Theme: {self.selected_theme} (T to change)", True, CYAN
        )
        self.screen.blit(theme_text, (10, 60))

        # Time limit
        time_text = self.font_small.render(
            f"Time Limit: {self.time_limit} (L to change)", True, CYAN
        )
        self.screen.blit(time_text, (10, 80))

        # Object counts
        count_y = SCREEN_HEIGHT - 150
        counts = [
            f"Tiles: {len(self.tiles)}",
            f"Enemies: {len(self.enemies)}",
            f"Coins: {len(self.coins)}",
            f"Powerups: {len(self.powerups)}",
            f"Hazards: {len(self.hazards)}",
            f"Portals: {len(self.portals)}",
        ]
        for i, count in enumerate(counts):
            text = self.font_small.render(count, True, WHITE)
            self.screen.blit(text, (10, count_y + i * 20))

    def _draw_help(self):
        """Draw help overlay"""
        # Semi-transparent background
        overlay = pygame.Surface((400, 500))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (SCREEN_WIDTH - 420, 20))

        help_text = [
            "=== HELP (F1 to toggle) ===",
            "",
            "MODES (Number Keys):",
            "1 - Tile (ground/platforms)",
            "2 - Enemy",
            "3 - Coin",
            "4 - Powerup",
            "5 - Hazard",
            "6 - Portal",
            "7 - Key",
            "8 - Spawn Point",
            "",
            "CONTROLS:",
            "Left Click - Place object",
            "Right Click - Remove object",
            "Arrow Keys - Move camera",
            "",
            "SUB-OPTIONS:",
            "E - Cycle enemy type",
            "H - Cycle hazard type",
            "P - Cycle powerup type",
            "T - Change theme",
            "L - Change time limit",
            "",
            "FILE:",
            "Ctrl+S - Save level",
            "Ctrl+O - Load level",
            "Ctrl+C - Clear all",
        ]

        y = 30
        for line in help_text:
            if line.startswith("==="):
                color = YELLOW
            elif line.startswith(("MODES", "CONTROLS", "SUB", "FILE")):
                color = CYAN
            else:
                color = WHITE
            text = self.font_small.render(line, True, color)
            self.screen.blit(text, (SCREEN_WIDTH - 410, y))
            y += 20

    def _save_level(self):
        """Save level to JSON file"""
        filename = input("Enter filename (without .json): ")
        if not filename:
            filename = "custom_level"

        level_data = {
            "width": self.level_width,
            "height": self.level_height,
            "theme": self.selected_theme,
            "spawn_x": self.spawn_x,
            "spawn_y": self.spawn_y,
            "time_limit": self.time_limit,
            "tiles": self.tiles,
            "enemies": self.enemies,
            "coins": self.coins,
            "powerups": self.powerups,
            "keys": self.keys,
            "hazards": self.hazards,
            "portals": self.portals,
        }

        try:
            import os

            os.makedirs("levels/data", exist_ok=True)
            filepath = f"levels/data/{filename}.json"
            with open(filepath, "w") as f:
                json.dump(level_data, f, indent=2)
            print(f"✓ Level saved to {filepath}")
        except Exception as e:
            print(f"✗ Error saving level: {e}")

    def _load_level(self):
        """Load level from JSON file"""
        filename = input("Enter filename (without .json): ")
        if not filename:
            return

        try:
            filepath = f"levels/data/{filename}.json"
            with open(filepath, "r") as f:
                level_data = json.load(f)

            self.level_width = level_data.get("width", 3200)
            self.level_height = level_data.get("height", 720)
            self.selected_theme = level_data.get("theme", "SCIFI")
            self.spawn_x = level_data.get("spawn_x", 100)
            self.spawn_y = level_data.get("spawn_y", 500)
            self.time_limit = level_data.get("time_limit", "medium")
            self.tiles = level_data.get("tiles", [])
            self.enemies = level_data.get("enemies", [])
            self.coins = level_data.get("coins", [])
            self.powerups = level_data.get("powerups", [])
            self.keys = level_data.get("keys", [])
            self.hazards = level_data.get("hazards", [])
            self.portals = level_data.get("portals", [])

            print(f"✓ Level loaded from {filepath}")
        except Exception as e:
            print(f"✗ Error loading level: {e}")

    def _clear_all(self):
        """Clear all objects"""
        confirm = input("Clear all objects? (y/n): ")
        if confirm.lower() == "y":
            self.tiles = []
            self.enemies = []
            self.coins = []
            self.powerups = []
            self.keys = []
            self.hazards = []
            self.portals = []
            print("✓ All objects cleared")


if __name__ == "__main__":
    print("=" * 60)
    print("LEVEL EDITOR")
    print("=" * 60)
    print("Press F1 in the editor to see controls")
    print()

    editor = LevelEditor()
    editor.run()
