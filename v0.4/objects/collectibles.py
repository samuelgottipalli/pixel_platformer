"""
Collectible objects (coins, keys, power-ups)
"""

import math

import pygame

from config.settings import CYAN, ORANGE, PURPLE, RED, WHITE, YELLOW
from utils.enums import PowerUpType


class Coin:
    """Collectible coin"""

    def __init__(self, x, y, value=1):
        """
        Args:
            x, y: Position
            value: Coin value (1, 5, 10, etc.)
        """
        self.x = x
        self.y = y
        self.value = value
        self.width = 20
        self.height = 20
        self.collected = False
        self.rotation = 0

    def update(self):
        """Animate coin rotation"""
        self.rotation = (self.rotation + 5) % 360

    def get_rect(self):
        """Get collision rectangle"""
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, surface, camera_x, camera_y):
        """Render coin with star pattern"""
        width = abs(math.cos(math.radians(self.rotation))) * self.width
        screen_x = self.x - camera_x + (self.width - width) / 2
        screen_y = self.y - camera_y

        # Draw coin as star shape instead of circle
        center = (int(screen_x + width / 2), int(screen_y + self.height / 2))
        radius = int(self.height / 2)

        # 8-point star
        points = []
        for i in range(16):
            angle = (i * math.pi / 8) + (self.rotation * math.pi / 180)
            r = radius if i % 2 == 0 else radius * 0.5
            x = center[0] + r * math.cos(angle)
            y = center[1] + r * math.sin(angle)
            points.append((x, y))

        pygame.draw.polygon(surface, YELLOW, points)
        pygame.draw.polygon(surface, ORANGE, points, 2)

        # Value indicator (dots in center)
        for i in range(min(self.value, 5)):
            offset = (i - 2) * 3
            pygame.draw.circle(surface, WHITE, (center[0] + offset, center[1]), 2)


class Key:
    """Collectible key for unlocking doors/portals"""

    def __init__(self, x, y, color):
        """
        Args:
            x, y: Position
            color: RGB tuple for key color
        """
        self.x = x
        self.y = y
        self.color = color
        self.width = 24
        self.height = 24
        self.collected = False

    def get_rect(self):
        """Get collision rectangle"""
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, surface, camera_x, camera_y):
        """Render key"""
        x = self.x - camera_x
        y = self.y - camera_y

        # Key head (circle)
        pygame.draw.circle(surface, self.color, (int(x + 8), int(y + 8)), 6)
        # Key shaft
        pygame.draw.rect(surface, self.color, (x + 8, y + 8, 12, 4))
        # Key teeth
        pygame.draw.rect(surface, self.color, (x + 16, y + 6, 2, 4))
        pygame.draw.rect(surface, self.color, (x + 16, y + 10, 2, 4))


class PowerUp:
    """Power-up collectible"""

    def __init__(self, x, y, ptype):
        """
        Args:
            x, y: Position
            ptype: PowerUpType string ('health', 'double_jump', etc.)
        """
        self.x = x
        self.y = y
        self.type = ptype
        self.width = 24
        self.height = 24
        self.collected = False
        self.float_offset = 0

    def update(self):
        """Animate floating effect"""
        self.float_offset = math.sin(pygame.time.get_ticks() / 200) * 5

    def get_rect(self):
        """Get collision rectangle"""
        return pygame.Rect(self.x, self.y + self.float_offset, self.width, self.height)

    def draw(self, surface, camera_x, camera_y):
        """Render power-up with distinct shape per type"""
        from utils.textures import TextureManager

        rect = pygame.Rect(
            self.x - camera_x,
            self.y + self.float_offset - camera_y,
            self.width,
            self.height,
        )

        colors = {
            PowerUpType.HEALTH.value: RED,
            PowerUpType.DOUBLE_JUMP.value: CYAN,
            PowerUpType.SPEED.value: YELLOW,
            PowerUpType.INVINCIBLE.value: PURPLE,
        }
        color = colors.get(self.type, WHITE)

        # Different pattern per type
        if self.type == PowerUpType.HEALTH.value:
            # HEALTH: Plus sign with cross pattern
            TextureManager.draw_checkered_rect(
                surface, rect, color, (255, 100, 100), check_size=6
            )
        elif self.type == PowerUpType.SPEED.value:
            # SPEED: Lightning stripes
            TextureManager.draw_diagonal_lines(
                surface, rect, color, (255, 255, 150), spacing=6
            )
        elif self.type == PowerUpType.DOUBLE_JUMP.value:
            # DOUBLE JUMP: Dotted
            TextureManager.draw_dotted_rect(
                surface, rect, color, (150, 255, 255), dot_size=3, spacing=8
            )
        elif self.type == PowerUpType.INVINCIBLE.value:
            # INVINCIBLE: Grid
            TextureManager.draw_grid_rect(
                surface, rect, color, (255, 150, 255), grid_size=8
            )

        pygame.draw.rect(surface, WHITE, rect, 3)

        # Large icon in center
        cx, cy = rect.centerx, rect.centery
        if self.type == PowerUpType.HEALTH.value:
            # Cross
            pygame.draw.line(surface, WHITE, (cx, cy - 8), (cx, cy + 8), 4)
            pygame.draw.line(surface, WHITE, (cx - 8, cy), (cx + 8, cy), 4)
        elif self.type == PowerUpType.SPEED.value:
            # Lightning bolt
            points = [(cx - 6, cy - 8), (cx + 4, cy), (cx - 4, cy), (cx + 6, cy + 8)]
            pygame.draw.lines(surface, WHITE, False, points, 3)
        elif self.type == PowerUpType.DOUBLE_JUMP.value:
            # Up arrows
            pygame.draw.polygon(
                surface, WHITE, [(cx, cy - 6), (cx - 6, cy), (cx + 6, cy)]
            )
            pygame.draw.polygon(
                surface, WHITE, [(cx, cy + 2), (cx - 6, cy + 8), (cx + 6, cy + 8)]
            )
