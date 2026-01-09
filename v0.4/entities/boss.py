"""
Boss entity system - Multi-phase boss fights
"""

import math
import random

import pygame

from config.settings import (CYAN, GRAVITY, MAX_FALL_SPEED, ORANGE, PURPLE,
                             RED, WHITE, YELLOW)


class Boss:
    """
    Boss entity with multi-phase combat

    Features:
    - Multiple health phases
    - Different attack patterns per phase
    - Invulnerability periods
    - Visual feedback
    """

    def __init__(self, x, y, boss_type="guardian", difficulty="NORMAL"):
        """
        Args:
            x, y: Starting position
            boss_type: Type of boss ('guardian', 'forest', 'void', 'ancient')
            difficulty: Game difficulty ('EASY', 'NORMAL', 'HARD')
        """
        self.x = x
        self.y = y
        self.start_x = x
        self.start_y = y
        self.type = boss_type
        self.difficulty = difficulty

        # Size
        self.width = 96
        self.height = 96

        # Health system
        self.max_health = self._get_max_health()
        self.health = self.max_health
        self.phase = 1
        self.max_phases = 3

        # Combat state
        self.invulnerable = False
        self.invuln_timer = 0
        self.damage_flash = 0
        self.dead = False
        self.defeated = False

        # Movement
        self.dx = 0
        self.dy = 0
        self.speed = 2
        self.floating = True  # Most bosses float

        # Attack system
        self.attack_timer = 0
        self.attack_cooldown = 120  # 2 seconds
        self.current_attack = None
        self.attack_state = 0

        # Animation
        self.animation_timer = 0
        self.float_offset = 0

        # Colors based on type
        self.colors = self._get_boss_colors()

    def _get_max_health(self):
        """Calculate max health based on difficulty"""
        base_health = {"guardian": 300, "forest": 400, "void": 500, "ancient": 600}.get(
            self.type, 300
        )

        # Adjust for difficulty
        multipliers = {"EASY": 0.7, "NORMAL": 1.0, "HARD": 1.5}
        return int(base_health * multipliers.get(self.difficulty, 1.0))

    def _get_boss_colors(self):
        """Get color scheme for boss type"""
        schemes = {
            "guardian": {"primary": CYAN, "secondary": PURPLE, "accent": WHITE},
            "forest": {
                "primary": (50, 150, 50),
                "secondary": (100, 200, 100),
                "accent": YELLOW,
            },
            "void": {"primary": PURPLE, "secondary": (100, 0, 150), "accent": CYAN},
            "ancient": {"primary": RED, "secondary": ORANGE, "accent": YELLOW},
        }
        return schemes.get(self.type, schemes["guardian"])

    def update(self, player, tiles, current_time):
        """
        Update boss AI and combat
        Args:
            player: Player object
            tiles: Level tiles
            current_time: Current game time in ms
        """
        if self.dead or self.defeated:
            return

        # Update phase based on health
        self._update_phase()

        # Update timers
        self._update_timers()

        # Movement AI
        self._update_movement(player)

        # Attack AI
        self._update_attacks(player, current_time)

        # Animation
        self._update_animation(current_time)

    def _update_phase(self):
        """Update combat phase based on health"""
        health_percent = self.health / self.max_health

        if health_percent > 0.66:
            new_phase = 1
        elif health_percent > 0.33:
            new_phase = 2
        else:
            new_phase = 3

        # Phase transition
        if new_phase > self.phase:
            self.phase = new_phase
            self._on_phase_change()

    def _on_phase_change(self):
        """Handle phase transition"""
        # Become invulnerable briefly
        self.invulnerable = True
        self.invuln_timer = 120  # 2 seconds

        # Speed up attacks
        self.attack_cooldown = max(60, self.attack_cooldown - 20)

        # Speed up movement
        self.speed += 0.5

    def _update_timers(self):
        """Update all timers"""
        if self.invuln_timer > 0:
            self.invuln_timer -= 1
            if self.invuln_timer == 0:
                self.invulnerable = False

        if self.damage_flash > 0:
            self.damage_flash -= 1

        self.attack_timer += 1

    def _update_movement(self, player):
        """Update boss movement patterns"""
        if self.floating:
            # Floating movement pattern
            self._floating_movement(player)
        else:
            # Ground-based movement
            self._ground_movement(player)

    def _floating_movement(self, player):
        """Floating boss movement (most bosses)"""
        # Move toward player horizontally
        if self.x < player.x - 100:
            self.dx = self.speed
        elif self.x > player.x + 100:
            self.dx = -self.speed
        else:
            self.dx *= 0.9

        self.x += self.dx

        # Sine wave vertical movement
        self.float_offset = math.sin(pygame.time.get_ticks() / 300) * 30
        self.y = self.start_y + self.float_offset

    def _ground_movement(self, player):
        """Ground boss movement"""
        # Chase player
        if self.x < player.x - 50:
            self.dx = self.speed
        elif self.x > player.x + 50:
            self.dx = -self.speed
        else:
            self.dx *= 0.9

        self.x += self.dx

        # Apply gravity
        self.dy += GRAVITY
        self.dy = min(self.dy, MAX_FALL_SPEED)
        self.y += self.dy

    def _update_attacks(self, player, current_time):
        """Update boss attacks"""
        if self.attack_timer < self.attack_cooldown:
            return

        # Choose attack based on phase and distance to player
        distance = abs(self.x - player.x)

        if self.phase == 1:
            # Phase 1: Simple projectile attacks
            attack = "projectile"
        elif self.phase == 2:
            # Phase 2: Projectile + spread attack
            attack = "projectile" if distance > 200 else "projectile_spread"
        else:
            # Phase 3: All attacks
            if distance > 300:
                attack = "projectile_spread"
            elif distance > 150:
                attack = "projectile"
            else:
                attack = "slam"

        self.current_attack = attack
        self.attack_state = 0
        self.attack_timer = 0

    def _update_animation(self, current_time):
        """Update visual animations"""
        self.animation_timer = (self.animation_timer + 1) % 360

    def take_damage(self, damage):
        """
        Take damage from player
        Args:
            damage: Amount of damage
        Returns:
            True if damage was dealt, False if invulnerable
        """
        if self.invulnerable or self.dead:
            return False

        self.health -= damage
        self.damage_flash = 10

        # Brief invulnerability after hit
        self.invulnerable = True
        self.invuln_timer = 15  # 0.25 seconds

        if self.health <= 0:
            self.dead = True
            self.defeated = True

        return True

    def get_rect(self):
        """Get collision rectangle"""
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def get_projectile_spawn_point(self):
        """Get point where projectiles spawn"""
        return (self.x + self.width // 2, self.y + self.height // 2)

    def get_current_attack(self):
        """Get current attack pattern"""
        return self.current_attack

    def draw(self, surface, camera_x, camera_y):
        """Render boss to screen"""
        if self.dead and not self.defeated:
            return

        screen_x = self.x - camera_x
        screen_y = self.y - camera_y

        # Flash white when damaged
        if self.damage_flash > 0 and self.damage_flash % 4 < 2:
            color = WHITE
        else:
            color = self.colors["primary"]

        # Invulnerability effect
        if self.invulnerable and self.invuln_timer % 10 < 5:
            color = self.colors["accent"]

        # Main body
        rect = pygame.Rect(screen_x, screen_y, self.width, self.height)
        pygame.draw.rect(surface, color, rect)
        pygame.draw.rect(surface, WHITE, rect, 3)

        # Phase indicators (glowing cores)
        core_size = 8
        for i in range(self.phase):
            core_x = screen_x + self.width // 2 - 15 + i * 15
            core_y = screen_y + self.height // 2
            pygame.draw.circle(
                surface, self.colors["accent"], (core_x, core_y), core_size
            )

        # Eyes
        if not self.dead:
            eye_y = screen_y + 30
            eye_color = RED if self.phase == 3 else self.colors["secondary"]
            pygame.draw.circle(surface, WHITE, (screen_x + 30, eye_y), 8)
            pygame.draw.circle(surface, eye_color, (screen_x + 32, eye_y), 6)
            pygame.draw.circle(surface, WHITE, (screen_x + 66, eye_y), 8)
            pygame.draw.circle(surface, eye_color, (screen_x + 64, eye_y), 6)

    def draw_health_bar(self, surface):
        """Draw boss health bar at top of screen"""
        bar_width = 600
        bar_height = 30
        bar_x = (surface.get_width() - bar_width) // 2
        bar_y = 20

        # Background
        pygame.draw.rect(surface, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))

        # Health bar
        health_percent = max(0, self.health / self.max_health)
        health_width = int(bar_width * health_percent)

        # Color based on health
        if health_percent > 0.66:
            bar_color = (0, 255, 0)
        elif health_percent > 0.33:
            bar_color = YELLOW
        else:
            bar_color = RED

        pygame.draw.rect(surface, bar_color, (bar_x, bar_y, health_width, bar_height))

        # Border
        pygame.draw.rect(surface, WHITE, (bar_x, bar_y, bar_width, bar_height), 3)

        # Phase markers
        phase_marker_x1 = bar_x + bar_width // 3
        phase_marker_x2 = bar_x + 2 * bar_width // 3
        pygame.draw.line(
            surface,
            WHITE,
            (phase_marker_x1, bar_y),
            (phase_marker_x1, bar_y + bar_height),
            2,
        )
        pygame.draw.line(
            surface,
            WHITE,
            (phase_marker_x2, bar_y),
            (phase_marker_x2, bar_y + bar_height),
            2,
        )

        # Text
        font = pygame.font.Font(None, 24)
        text = font.render(f"BOSS: {self.health}/{self.max_health}", True, WHITE)
        text_x = bar_x + bar_width // 2 - text.get_width() // 2
        text_y = bar_y + 5
        surface.blit(text, (text_x, text_y))

        # Phase indicator
        phase_text = font.render(f"PHASE {self.phase}/{self.max_phases}", True, YELLOW)
        surface.blit(phase_text, (bar_x + bar_width + 20, bar_y + 5))


class BossProjectile:
    """Projectile fired by boss"""

    def __init__(self, x, y, angle, speed, damage, color):
        """
        Args:
            x, y: Starting position
            angle: Direction in radians
            speed: Pixels per frame
            damage: Damage dealt
            color: RGB tuple
        """
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        self.damage = damage
        self.color = color
        self.width = 16
        self.height = 16
        self.active = True
        self.lifetime = 300  # 5 seconds
        self.age = 0

    def update(self, tiles):
        """Update projectile"""
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        self.age += 1

        if self.age >= self.lifetime:
            self.active = False

        # Check tile collision
        for tile in tiles:
            if tile.get("solid", True) and self.get_rect().colliderect(tile["rect"]):
                self.active = False

    def get_rect(self):
        """Get collision rectangle"""
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, surface, camera_x, camera_y):
        """Render projectile"""
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y

        # Glowing projectile
        pygame.draw.circle(
            surface,
            self.color,
            (int(screen_x + self.width // 2), int(screen_y + self.height // 2)),
            self.width // 2,
        )
        pygame.draw.circle(
            surface,
            WHITE,
            (int(screen_x + self.width // 2), int(screen_y + self.height // 2)),
            self.width // 2,
            2,
        )
