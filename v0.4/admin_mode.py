"""
Admin Testing Mode
Quick level testing without character selection or save system
Usage: python admin_mode.py
"""

import os
import sys

import pygame

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import controls
from config.settings import (BLACK, CYAN, FPS, SCREEN_HEIGHT, SCREEN_WIDTH,
                             WHITE, YELLOW)
from core.camera import Camera
from entities.player import Player
from levels.level import Level
from levels.level_loader import LevelLoader
from ui.hud import HUD
from utils.enums import GameState


class AdminMode:
    """Admin testing mode - quick level access for development"""

    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Admin Mode - Level Testing")
        self.clock = pygame.time.Clock()
        self.running = True

        # Fonts
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)

        # UI
        self.hud = HUD(self.font_small)

        # Load all levels
        self.levels = LevelLoader.create_default_levels()
        self.level_count = len(self.levels)

        # State
        self.state = GameState.MENU
        self.selected_level = 0
        self.selected_difficulty = 1  # 0=Easy, 1=Normal, 2=Hard

        # Game objects (initialized when level starts)
        self.player = None
        self.level = None
        self.camera = Camera()
        self.projectiles = []
        self.particles = []

        # Input tracking
        self.jump_pressed = False

    def run(self):
        """Main admin mode loop"""
        while self.running:
            self._handle_events()
            self._update()
            self._draw()
            self.clock.tick(FPS)

        pygame.quit()

    def _handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if self.state == GameState.MENU:
                self._handle_menu_events(event)
            elif self.state == GameState.PLAYING:
                self._handle_game_events(event)

    def _handle_menu_events(self, event):
        """Handle level selection menu"""
        if event.type == pygame.KEYDOWN:
            # Level selection
            if event.key == pygame.K_UP:
                self.selected_level = (self.selected_level - 1) % self.level_count
            elif event.key == pygame.K_DOWN:
                self.selected_level = (self.selected_level + 1) % self.level_count
            # Difficulty selection
            elif event.key == pygame.K_LEFT:
                self.selected_difficulty = (self.selected_difficulty - 1) % 3
            elif event.key == pygame.K_RIGHT:
                self.selected_difficulty = (self.selected_difficulty + 1) % 3
            # Start level
            elif event.key == pygame.K_RETURN:
                self._start_level(self.selected_level)
            # Quick number keys
            elif pygame.K_0 <= event.key <= pygame.K_9:
                level_num = event.key - pygame.K_0
                if level_num < self.level_count:
                    self.selected_level = level_num
                    self._start_level(level_num)
            # Quit
            elif event.key == pygame.K_ESCAPE:
                self.running = False

    def _handle_game_events(self, event):
        """Handle in-game events"""
        if event.type == pygame.KEYDOWN:
            # Return to menu
            if event.key == pygame.K_ESCAPE:
                self.state = GameState.MENU
            # Quick restart
            elif event.key == pygame.K_r:
                self._start_level(self.selected_level)
            # Next level
            elif event.key == pygame.K_n:
                next_level = (self.selected_level + 1) % self.level_count
                self.selected_level = next_level
                self._start_level(next_level)
            # Previous level
            elif event.key == pygame.K_p:
                prev_level = (self.selected_level - 1) % self.level_count
                self.selected_level = prev_level
                self._start_level(prev_level)

    def _start_level(self, level_index):
        """Start a specific level"""
        if 0 <= level_index < self.level_count:
            # Create fresh player
            self.player = Player(100, 100, 0)  # Default character

            # Set difficulty-based lives
            difficulties = ["EASY", "NORMAL", "HARD"]
            difficulty = difficulties[self.selected_difficulty]
            if difficulty == "EASY":
                self.player.lives = 5
            elif difficulty == "NORMAL":
                self.player.lives = 3
            else:  # HARD
                self.player.lives = 1

            # Load level
            self.level = Level(self.levels[level_index])
            self.player.x = self.level.spawn_x
            self.player.y = self.level.spawn_y

            # Reset game objects
            self.projectiles = []
            self.particles = []

            # Start playing
            self.state = GameState.PLAYING

            print(
                f"✓ Admin Mode: Started Level {level_index} on {difficulty} difficulty"
            )

    def _update(self):
        """Update game state"""
        if self.state == GameState.PLAYING:
            self._update_game()

    def _update_game(self):
        """Update game logic"""
        keys = pygame.key.get_pressed()

        # Handle player input
        self._handle_player_input(keys)

        # Update player
        self.player.update(keys, self.level.tiles, self.level.hazards)

        # Update camera
        self.camera.update(
            self.player.x + self.player.width // 2,
            self.player.y + self.player.height // 2,
            self.level.width,
            self.level.height,
        )

        # Update collectibles
        self._update_collectibles()

        # Update enemies
        self._update_enemies()

        # Update projectiles
        self._update_projectiles()

        # Check death
        if self.player.y > SCREEN_HEIGHT + 100:
            self.player.die()
            if self.player.lives < 0:
                # Auto-restart in admin mode
                self._start_level(self.selected_level)

    def _handle_player_input(self, keys):
        """Handle player action input"""
        # Jump
        if controls.check_key_pressed(keys, controls.JUMP):
            if not self.jump_pressed:
                self.player.jump()
                self.jump_pressed = True
        else:
            self.jump_pressed = False

        # Shoot
        if controls.check_key_pressed(keys, controls.SHOOT):
            if self.player.shoot():
                self._create_projectile()

        # Melee
        if controls.check_key_pressed(keys, controls.MELEE):
            self.player.melee_attack()

        # Upgrade weapon (free in admin mode)
        if controls.check_key_pressed(keys, controls.UPGRADE_WEAPON):
            if self.player.weapon_level < 4:
                self.player.weapon_level += 1

    def _create_projectile(self):
        """Create projectile from player"""
        from entities.projectile import Projectile

        damage = self.player.weapon_level
        speed = 8 + self.player.weapon_level
        proj = Projectile(
            self.player.x + (self.player.width if self.player.direction > 0 else 0),
            self.player.y + self.player.height // 2,
            self.player.direction,
            speed,
            damage,
            CYAN,
        )
        self.projectiles.append(proj)

    def _update_collectibles(self):
        """Update coins, power-ups, keys"""
        for coin in self.level.coins:
            if not coin.collected:
                coin.update()
                if self.player.get_rect().colliderect(coin.get_rect()):
                    coin.collected = True
                    self.player.coins += coin.value

        for powerup in self.level.powerups:
            if not powerup.collected:
                powerup.update()
                if self.player.get_rect().colliderect(powerup.get_rect()):
                    powerup.collected = True
                    self.player.add_powerup(powerup.type)

        for key in self.level.keys:
            if not key.collected:
                if self.player.get_rect().colliderect(key.get_rect()):
                    key.collected = True
                    self.player.keys.append(key.color)

    def _update_enemies(self):
        """Update enemies"""
        for enemy in self.level.enemies:
            if not enemy.dead:
                enemy.update(self.level.tiles)

                # Check collision with player
                if self.player.get_rect().colliderect(enemy.get_rect()):
                    # Simple stomp or damage
                    if self.player.dy > 0:
                        enemy.take_damage(2)
                        self.player.dy = -10
                    else:
                        self.player.take_damage(enemy.damage)

    def _update_projectiles(self):
        """Update projectiles"""
        for proj in self.projectiles[:]:
            proj.update(self.level.tiles)

            if not proj.active:
                self.projectiles.remove(proj)
                continue

            # Check enemy collision
            for enemy in self.level.enemies:
                if not enemy.dead and proj.get_rect().colliderect(enemy.get_rect()):
                    enemy.take_damage(proj.damage)
                    proj.active = False
                    break

    def _draw(self):
        """Draw current state"""
        if self.state == GameState.MENU:
            self._draw_menu()
        elif self.state == GameState.PLAYING:
            self._draw_game()

        pygame.display.flip()

    def _draw_menu(self):
        """Draw level selection menu"""
        self.screen.fill(BLACK)

        # Title
        title = self.font_large.render("ADMIN MODE", True, YELLOW)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))

        subtitle = self.font_small.render("Level Testing & Development", True, WHITE)
        self.screen.blit(subtitle, (SCREEN_WIDTH // 2 - subtitle.get_width() // 2, 120))

        # Difficulty selection
        diff_label = self.font_small.render("Difficulty:", True, WHITE)
        self.screen.blit(diff_label, (100, 200))

        difficulties = ["EASY (5 Lives)", "NORMAL (3 Lives)", "HARD (1 Life)"]
        for i, diff in enumerate(difficulties):
            color = YELLOW if i == self.selected_difficulty else WHITE
            text = self.font_small.render(diff, True, color)
            self.screen.blit(text, (100, 240 + i * 40))

        # Level list
        list_y = 380
        self.screen.blit(
            self.font_medium.render("Select Level:", True, CYAN), (100, list_y)
        )

        # Show 10 levels at a time
        start_idx = max(0, self.selected_level - 5)
        end_idx = min(self.level_count, start_idx + 10)

        for i in range(start_idx, end_idx):
            color = YELLOW if i == self.selected_level else WHITE
            level_info = f"[{i}] Level {i}"

            # Add level info if available
            if i < len(self.levels):
                width = self.levels[i].get("width", "N/A")
                level_info += f" - {width}px"

            text = self.font_small.render(level_info, True, color)
            self.screen.blit(text, (120, list_y + 50 + (i - start_idx) * 35))

        # Controls
        controls_y = SCREEN_HEIGHT - 180
        controls = [
            "UP/DOWN: Select Level  |  LEFT/RIGHT: Change Difficulty",
            "ENTER: Start Level  |  0-9: Quick Jump to Level",
            "ESC: Quit Admin Mode",
        ]
        for i, control in enumerate(controls):
            text = self.font_small.render(control, True, (150, 150, 150))
            self.screen.blit(
                text, (SCREEN_WIDTH // 2 - text.get_width() // 2, controls_y + i * 35)
            )

    def _draw_game(self):
        """Draw game world"""
        # Background
        self.screen.fill(self.level.get_background_color())

        # Draw tiles
        self._draw_tiles()

        # Draw game objects
        self._draw_hazards()
        self._draw_collectibles()
        self._draw_portals()
        self._draw_enemies()
        self._draw_projectiles()

        # Draw player
        self.player.draw(self.screen, self.camera.x, self.camera.y)

        # Draw HUD
        self.hud.draw(self.screen, self.player, self.selected_level)

        # Draw admin overlay
        self._draw_admin_overlay()

    def _draw_tiles(self):
        """Draw level tiles"""
        from utils.collision import is_rect_on_screen

        for tile in self.level.tiles:
            if is_rect_on_screen(
                tile["rect"], self.camera.x, self.camera.y, SCREEN_WIDTH, SCREEN_HEIGHT
            ):
                rect = self.camera.apply_rect(tile["rect"])
                pygame.draw.rect(self.screen, tile["color"], rect)
                pygame.draw.rect(self.screen, WHITE, rect, 1)

    def _draw_hazards(self):
        """Draw hazards"""
        for hazard in self.level.hazards:
            hazard.draw(self.screen, self.camera.x, self.camera.y)

    def _draw_collectibles(self):
        """Draw coins, power-ups, keys"""
        for coin in self.level.coins:
            if not coin.collected:
                coin.draw(self.screen, self.camera.x, self.camera.y)

        for powerup in self.level.powerups:
            if not powerup.collected:
                powerup.draw(self.screen, self.camera.x, self.camera.y)

        for key in self.level.keys:
            if not key.collected:
                key.draw(self.screen, self.camera.x, self.camera.y)

    def _draw_portals(self):
        """Draw portals"""
        for portal in self.level.portals:
            portal.draw(self.screen, self.camera.x, self.camera.y)

    def _draw_enemies(self):
        """Draw enemies"""
        for enemy in self.level.enemies:
            enemy.draw(self.screen, self.camera.x, self.camera.y)

    def _draw_projectiles(self):
        """Draw projectiles"""
        for proj in self.projectiles:
            proj.draw(self.screen, self.camera.x, self.camera.y)

    def _draw_admin_overlay(self):
        """Draw admin mode overlay"""
        # Admin controls
        controls = [
            f"ADMIN MODE - Level {self.selected_level}",
            "ESC: Menu | R: Restart | N: Next | P: Previous",
        ]

        y = 10
        for control in controls:
            text = self.font_small.render(control, True, YELLOW)
            # Semi-transparent background
            bg = pygame.Surface((text.get_width() + 10, text.get_height() + 5))
            bg.set_alpha(128)
            bg.fill(BLACK)
            self.screen.blit(bg, (SCREEN_WIDTH - text.get_width() - 15, y))
            self.screen.blit(text, (SCREEN_WIDTH - text.get_width() - 10, y + 2))
            y += 35


def main():
    """Entry point for admin mode"""
    print("=" * 60)
    print("ADMIN MODE - Level Testing")
    print("=" * 60)
    print("Quick access to any level for testing")
    print("No save system, profiles, or character selection")
    print()

    admin = AdminMode()
    admin.run()


if __name__ == "__main__":
    main()
