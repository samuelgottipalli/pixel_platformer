"""
Enemy entity
"""

import math

import pygame

from config.settings import (CYAN, ENEMY_BASE_DAMAGE, ENEMY_BASE_HEALTH,
                             ENEMY_FLYING_SPEED, ENEMY_GROUND_SPEED,
                             ENEMY_SHOOT_COOLDOWN, GRAVITY, MAX_FALL_SPEED,
                             ORANGE, RED, WHITE)
from utils.enums import EnemyType


class Enemy:
    """Enemy entity with AI behavior"""

    def __init__(self, x, y, enemy_type, patrol_distance=200):
        """
        Args:
            x, y: Starting position
            enemy_type: Type string ('ground', 'flying', 'turret')
            patrol_distance: Distance to patrol in pixels
        """
        self.x = x
        self.y = y
        self.start_x = x
        self.start_y = y
        self.type = enemy_type
        self.width = 32
        self.height = 32
        self.health = ENEMY_BASE_HEALTH
        self.damage = ENEMY_BASE_DAMAGE
        self.direction = 1
        self.patrol_distance = patrol_distance
        self.dy = 0
        self.dead = False
        self.shoot_timer = 0
        self.shoot_cooldown = ENEMY_SHOOT_COOLDOWN

        # Set speed based on type
        if self.type == EnemyType.GROUND.value:
            self.speed = ENEMY_GROUND_SPEED
        elif self.type == EnemyType.FLYING.value:
            self.speed = ENEMY_FLYING_SPEED
        else:
            self.speed = 0

    def update(self, tiles):
        """Update enemy AI and movement"""
        if self.dead:
            return

        if self.type == EnemyType.GROUND.value:
            self._update_ground_enemy(tiles)
        elif self.type == EnemyType.FLYING.value:
            self._update_flying_enemy()
        elif self.type == EnemyType.TURRET.value:
            self._update_turret()

    def _update_ground_enemy(self, tiles):
        """Update ground patrolling enemy"""
        self.x += self.direction * self.speed

        # Turn around at patrol bounds
        if abs(self.x - self.start_x) > self.patrol_distance:
            self.direction *= -1

        # Apply gravity
        self.dy += GRAVITY
        self.dy = min(self.dy, MAX_FALL_SPEED)
        self.y += self.dy

        # Check ground collision
        for tile in tiles:
            if tile.get("solid", True) and self.get_rect().colliderect(tile["rect"]):
                if self.dy > 0:
                    self.y = tile["rect"].top - self.height
                    self.dy = 0

    def _update_flying_enemy(self):
        """Update flying enemy with sine wave pattern"""
        self.x += self.direction * self.speed
        self.y = self.start_y + math.sin(pygame.time.get_ticks() / 500) * 50

        if abs(self.x - self.start_x) > self.patrol_distance:
            self.direction *= -1

    def _update_turret(self):
        """Update stationary turret enemy"""
        self.shoot_timer += 1

    def take_damage(self, damage):
        """Take damage and die if health depletes"""
        self.health -= damage
        if self.health <= 0:
            self.dead = True

    def can_shoot(self):
        """Check if turret can shoot (cooldown expired)"""
        return self.shoot_timer >= self.shoot_cooldown

    def reset_shoot_timer(self):
        """Reset shoot cooldown"""
        self.shoot_timer = 0

    def get_rect(self):
        """Get collision rectangle"""
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, surface, camera_x, camera_y):
        """Render enemy to screen with distinct patterns"""
        from utils.textures import TextureManager

        if self.dead:
            return

        rect = pygame.Rect(
            self.x - camera_x, self.y - camera_y, self.width, self.height
        )

        # Different patterns per enemy type
        if self.type == EnemyType.GROUND.value:
            # GROUND: Horizontal stripes
            TextureManager.draw_striped_rect(
                surface, rect, RED, (255, 100, 100), stripe_width=4, vertical=False
            )
        elif self.type == EnemyType.FLYING.value:
            # FLYING: Diagonal lines
            TextureManager.draw_diagonal_lines(
                surface, rect, CYAN, (150, 255, 255), spacing=8, line_width=2
            )
        elif self.type == EnemyType.TURRET.value:
            # TURRET: Checkered
            TextureManager.draw_checkered_rect(
                surface, rect, ORANGE, (255, 200, 100), check_size=8
            )

        # Thick border
        pygame.draw.rect(surface, WHITE, rect, 3)

        # Eyes with X pattern for enemies
        pygame.draw.line(
            surface, WHITE, (rect.x + 8, rect.y + 8), (rect.x + 14, rect.y + 14), 2
        )
        pygame.draw.line(
            surface, WHITE, (rect.x + 14, rect.y + 8), (rect.x + 8, rect.y + 14), 2
        )
        pygame.draw.line(
            surface, WHITE, (rect.x + 18, rect.y + 8), (rect.x + 24, rect.y + 14), 2
        )
        pygame.draw.line(
            surface, WHITE, (rect.x + 24, rect.y + 8), (rect.x + 18, rect.y + 14), 2
        )
