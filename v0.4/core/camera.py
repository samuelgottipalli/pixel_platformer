"""
Camera system for smooth scrolling
"""
from config.settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Camera:
    """Smooth scrolling camera that follows player"""
    
    def __init__(self):
        self.x = 0
        self.y = 0
        self.smoothing = 0.1  # Lower = smoother but slower
        
    def update(self, target_x, target_y, level_width, level_height):
        """
        Update camera position to follow target
        Args:
            target_x, target_y: Target position (usually player center)
            level_width, level_height: Level boundaries
        """
        # Calculate target camera position (center on target)
        target_camera_x = target_x - SCREEN_WIDTH // 2
        target_camera_y = target_y - SCREEN_HEIGHT // 2
        
        # Smooth camera movement
        self.x += (target_camera_x - self.x) * self.smoothing
        self.y += (target_camera_y - self.y) * self.smoothing
        
        # Clamp camera to level boundaries
        self.x = max(0, min(self.x, level_width - SCREEN_WIDTH))
        self.y = max(0, min(self.y, level_height - SCREEN_HEIGHT))
        
    def apply(self, x, y):
        """
        Apply camera offset to world coordinates
        Args:
            x, y: World coordinates
        Returns:
            Screen coordinates (x, y)
        """
        return int(x - self.x), int(y - self.y)
        
    def apply_rect(self, rect):
        """
        Apply camera offset to rectangle
        Args:
            rect: pygame.Rect in world coordinates
        Returns:
            New pygame.Rect in screen coordinates
        """
        import pygame
        return pygame.Rect(rect.x - self.x, rect.y - self.y, rect.width, rect.height)