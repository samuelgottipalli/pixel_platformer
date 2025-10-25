"""
Collectible objects (coins, keys, power-ups)
"""
import pygame
import math
from config.settings import (
    WHITE, YELLOW, ORANGE, RED, CYAN, PURPLE
)
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
        """Render spinning coin"""
        width = abs(math.cos(math.radians(self.rotation))) * self.width
        rect = pygame.Rect(
            self.x - camera_x + (self.width - width) / 2,
            self.y - camera_y, 
            width, 
            self.height
        )
        pygame.draw.ellipse(surface, YELLOW, rect)
        pygame.draw.ellipse(surface, ORANGE, rect, 2)

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
        return pygame.Rect(self.x, self.y + self.float_offset, 
                          self.width, self.height)
        
    def draw(self, surface, camera_x, camera_y):
        """Render power-up"""
        colors = {
            PowerUpType.HEALTH.value: RED,
            PowerUpType.DOUBLE_JUMP.value: CYAN,
            PowerUpType.SPEED.value: YELLOW,
            PowerUpType.INVINCIBLE.value: PURPLE
        }
        color = colors.get(self.type, WHITE)
        
        rect = pygame.Rect(
            self.x - camera_x, 
            self.y + self.float_offset - camera_y,
            self.width, 
            self.height
        )
        pygame.draw.rect(surface, color, rect)
        pygame.draw.rect(surface, WHITE, rect, 2)
        
        # Draw icon based on type
        cx, cy = rect.centerx, rect.centery
        if self.type == PowerUpType.HEALTH.value:
            # Cross/plus symbol
            pygame.draw.line(surface, WHITE, (cx, cy-6), (cx, cy+6), 3)
            pygame.draw.line(surface, WHITE, (cx-6, cy), (cx+6, cy), 3)
        elif self.type == PowerUpType.SPEED.value:
            # Lightning bolt shape
            points = [(cx-4, cy-6), (cx+2, cy), (cx-2, cy), (cx+4, cy+6)]
            pygame.draw.lines(surface, WHITE, False, points, 2)
        elif self.type == PowerUpType.DOUBLE_JUMP.value:
            # Up arrows
            pygame.draw.line(surface, WHITE, (cx, cy-4), (cx-4, cy), 2)
            pygame.draw.line(surface, WHITE, (cx, cy-4), (cx+4, cy), 2)
            pygame.draw.line(surface, WHITE, (cx, cy+2), (cx-4, cy+6), 2)
            pygame.draw.line(surface, WHITE, (cx, cy+2), (cx+4, cy+6), 2)