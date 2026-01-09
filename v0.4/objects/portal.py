"""
Portal object for level transitions
"""

import math

import pygame

from config.settings import PURPLE


class Portal:
    """Portal for transitioning between levels"""

    def __init__(self, x, y, destination_level, color=None, required_keys=None):
        """
        Args:
            x, y: Position
            destination_level: Index of destination level
            color: RGB tuple (default: purple)
            required_keys: List of key colors needed to unlock (optional)
        """
        self.x = x
        self.y = y
        self.width = 48
        self.height = 64
        self.destination = destination_level
        self.color = color if color else PURPLE
        self.required_keys = required_keys if required_keys else []
        self.animation_offset = 0
        self.locked = len(self.required_keys) > 0

    def update(self):
        """Update portal animation"""
        self.animation_offset = (self.animation_offset + 1) % 360

    def check_unlock(self, player_keys):
        """
        Check if player has required keys to unlock portal
        Args:
            player_keys: List of key colors player has collected
        Returns:
            True if unlocked or no keys required
        """
        if not self.locked:
            return True

        for required_key in self.required_keys:
            if required_key not in player_keys:
                return False

        self.locked = False
        return True

    def get_rect(self):
        """Get collision rectangle"""
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, surface, camera_x, camera_y):
        """Render portal with animation"""
        x = self.x - camera_x
        y = self.y - camera_y

        # Animated portal effect with multiple layers
        for i in range(3):
            offset = math.sin(math.radians(self.animation_offset + i * 120)) * 8
            rect = pygame.Rect(x + offset, y, self.width - abs(offset) * 2, self.height)
            color = tuple(max(0, c - i * 60) for c in self.color)
            pygame.draw.ellipse(surface, color, rect)

        # Draw lock symbol if locked
        if self.locked:
            from config.settings import BLACK, YELLOW

            lock_x = x + self.width // 2
            lock_y = y + self.height // 2

            # Lock body
            pygame.draw.rect(surface, YELLOW, (lock_x - 8, lock_y, 16, 12))
            # Lock shackle
            pygame.draw.arc(
                surface, YELLOW, (lock_x - 6, lock_y - 10, 12, 12), 0, 3.14, 3
            )
            # Keyhole
            pygame.draw.circle(surface, BLACK, (lock_x, lock_y + 6), 2)
