"""
Projectile entity
"""

import pygame
import math

from config.settings import WHITE


class Projectile:
    """Projectile fired by player or enemies"""

    def __init__(self, x, y, direction, speed, damage, color, angle=None):
        """
        Args:
            x, y: Starting position
            direction: 1 for right, -1 for left (used if angle is None)
            speed: Pixels per frame
            damage: Damage dealt on hit
            color: RGB tuple
            angle: Optional angle in radians for aimed shots (turrets, bosses)
        """
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = speed
        self.damage = damage
        self.color = color
        self.angle = angle  # NEW - for angled shots
        self.width = 12
        self.height = 6
        self.active = True

        # Add lifetime to prevent projectiles from living forever
        self.lifetime = 180  # 3 seconds at 60 FPS
        self.age = 0

    def update(self, tiles):
        """Update projectile position and check tile collision"""
        # Age tracking
        self.age += 1
        if self.age >= self.lifetime:
            self.active = False
            return

        # Movement - check if angled or horizontal
        if self.angle is not None:
            # Angle-based movement (for turrets and bosses)
            self.x += math.cos(self.angle) * self.speed
            self.y += math.sin(self.angle) * self.speed
        else:
            # Horizontal movement (for player)
            self.x += self.direction * self.speed

        # Check collision with solid tiles
        for tile in tiles:
            if tile.get("solid", True) and self.get_rect().colliderect(tile["rect"]):
                self.active = False
                return

    def get_rect(self):
        """Get collision rectangle"""
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, surface, camera_x, camera_y):
        """Render projectile to screen"""
        rect = pygame.Rect(
            self.x - camera_x, self.y - camera_y, self.width, self.height
        )

        # Draw filled rectangle
        pygame.draw.rect(surface, self.color, rect)
        # Draw white border
        pygame.draw.rect(surface, WHITE, rect, 1)
