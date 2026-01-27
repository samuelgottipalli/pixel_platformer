"""
Hazard objects (spikes, falling blocks, moving platforms)
"""

import pygame

from config.settings import BLUE, GRAVITY, GRAY, RED, SCREEN_HEIGHT, WHITE
from utils.enums import HazardType


class Hazard:
    """Environmental hazard"""

    def __init__(self, x, y, hazard_type, width=32, height=32):
        """
        Args:
            x, y: Position
            hazard_type: HazardType string
            width, height: Size in pixels
        """
        self.x = x
        self.y = y
        self.start_x = x
        self.start_y = y
        self.type = hazard_type
        self.width = width
        self.height = height
        self.damage = 1

        # Falling block state
        self.dy = 0
        self.falling = False
        self.respawn_timer = 0

        # Moving platform state
        self.direction = 1
        self.move_distance = 150
        self.speed = 2

    def update(self, player_rect):
        """
        Update hazard behavior
        Args:
            player_rect: Player collision rectangle for trigger detection
        """
        if self.type == HazardType.FALLING_BLOCK.value:
            self._update_falling_block(player_rect)
        elif self.type == HazardType.MOVING_PLATFORM.value:
            self._update_moving_platform()

    def _update_falling_block(self, player_rect):
        """Update falling block behavior"""
        if not self.falling and player_rect.colliderect(self.get_trigger_rect()):
            self.falling = True

        if self.falling:
            self.dy += GRAVITY
            self.y += self.dy

        # Respawn after falling off screen
        if self.y > SCREEN_HEIGHT + 100:
            self.respawn_timer += 1
            if self.respawn_timer > 300:
                self.y = self.start_y
                self.dy = 0
                self.falling = False
                self.respawn_timer = 0

    def _update_moving_platform(self):
        """Update moving platform behavior"""
        self.x += self.direction * self.speed
        if abs(self.x - self.start_x) > self.move_distance:
            self.direction *= -1

    def get_rect(self):
        """Get collision rectangle"""
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def get_trigger_rect(self):
        """Get trigger zone for falling blocks"""
        return pygame.Rect(self.x - 50, self.y - 100, self.width + 100, 100)

    def draw(self, surface, camera_x, camera_y):
        """Render hazard with high-contrast patterns"""
        from utils.textures import TextureManager

        rect = pygame.Rect(
            self.x - camera_x, self.y - camera_y, self.width, self.height
        )

        if self.type == HazardType.SPIKE.value:
            # Draw spikes with WARNING pattern (diagonal stripes)
            base = pygame.Rect(rect.x, rect.bottom - 8, rect.width, 8)
            TextureManager.draw_diagonal_lines(
                surface, base, (100, 0, 0), (255, 255, 0), spacing=6, line_width=2
            )

            # Triangle spike
            points = [
                (rect.left, rect.bottom),
                (rect.centerx, rect.top),
                (rect.right, rect.bottom),
            ]
            pygame.draw.polygon(surface, RED, points)
            pygame.draw.polygon(surface, (255, 255, 0), points, 3)  # Yellow outline

            # Add exclamation mark
            pygame.draw.line(
                surface,
                WHITE,
                (rect.centerx, rect.top + 8),
                (rect.centerx, rect.centery),
                2,
            )
            pygame.draw.circle(surface, WHITE, (rect.centerx, rect.centery + 6), 2)

        elif self.type == HazardType.FALLING_BLOCK.value:
            color = GRAY if not self.falling else RED
            # Checkered pattern
            TextureManager.draw_checkered_rect(
                surface, rect, color, (150, 150, 150), check_size=8
            )
            pygame.draw.rect(surface, WHITE, rect, 3)

            # Draw cracks if about to fall
            if not self.falling:
                pygame.draw.line(
                    surface,
                    (255, 255, 0),
                    (rect.left + 8, rect.top),
                    (rect.left + 12, rect.bottom),
                    2,
                )
                pygame.draw.line(
                    surface,
                    (255, 255, 0),
                    (rect.right - 12, rect.top),
                    (rect.right - 8, rect.bottom),
                    2,
                )

        elif self.type == HazardType.MOVING_PLATFORM.value:
            # Dotted pattern for moving platforms
            TextureManager.draw_dotted_rect(
                surface, rect, BLUE, (150, 200, 255), dot_size=3, spacing=10
            )
            pygame.draw.rect(surface, WHITE, rect, 3)

            # Arrow showing direction
            arrow_x = rect.centerx + (self.direction * 8)
            points = [
                (arrow_x, rect.centery),
                (arrow_x - self.direction * 6, rect.centery - 4),
                (arrow_x - self.direction * 6, rect.centery + 4),
            ]
            pygame.draw.polygon(surface, WHITE, points)
