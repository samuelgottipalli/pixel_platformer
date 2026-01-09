"""
Projectile entity
"""

import pygame

from config.settings import WHITE


class Projectile:
    """Projectile fired by player or enemies"""

    def __init__(self, x, y, direction, speed, damage, color):
        """
        Args:
            x, y: Starting position
            direction: 1 for right, -1 for left
            speed: Pixels per frame
            damage: Damage dealt on hit
            color: RGB tuple
        """
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = speed
        self.damage = damage
        self.color = color
        self.width = 12
        self.height = 6
        self.active = True

    def update(self, tiles):
        """Update projectile position and check tile collision"""
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
        pygame.draw.rect(surface, self.color, rect)
        pygame.draw.rect(surface, WHITE, rect, 1)
