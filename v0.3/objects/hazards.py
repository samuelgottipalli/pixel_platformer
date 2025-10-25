"""
Hazard objects (spikes, falling blocks, moving platforms)
"""
import pygame
from utils.enums import HazardType
from config.settings import GRAVITY, WHITE, RED, GRAY, BLUE, SCREEN_HEIGHT

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
        """Render hazard to screen"""
        rect = pygame.Rect(
            self.x - camera_x, 
            self.y - camera_y,
            self.width, 
            self.height
        )
        
        if self.type == HazardType.SPIKE.value:
            # Draw spikes
            points = [
                (rect.left, rect.bottom),
                (rect.centerx, rect.top),
                (rect.right, rect.bottom)
            ]
            pygame.draw.polygon(surface, RED, points)
            pygame.draw.polygon(surface, WHITE, points, 2)
            
        elif self.type == HazardType.FALLING_BLOCK.value:
            color = GRAY if not self.falling else RED
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, WHITE, rect, 2)
            
            # Draw cracks if about to fall
            if not self.falling:
                pygame.draw.line(surface, RED, 
                               (rect.left + 8, rect.top), 
                               (rect.left + 12, rect.bottom), 1)
                pygame.draw.line(surface, RED, 
                               (rect.right - 12, rect.top), 
                               (rect.right - 8, rect.bottom), 1)
            
        elif self.type == HazardType.MOVING_PLATFORM.value:
            pygame.draw.rect(surface, BLUE, rect)
            pygame.draw.rect(surface, WHITE, rect, 2)
            
            # Draw direction indicator
            if self.direction > 0:
                pygame.draw.line(surface, WHITE, 
                               (rect.right - 8, rect.centery), 
                               (rect.right - 4, rect.centery), 2)