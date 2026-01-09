"""
Particle effects system
"""
import pygame

class Particle:
    """Visual particle effect"""
    
    def __init__(self, x, y, color, dx, dy, lifetime):
        """
        Args:
            x, y: Starting position
            color: RGB tuple
            dx, dy: Velocity
            lifetime: Number of frames before particle disappears
        """
        self.x = x
        self.y = y
        self.color = color
        self.dx = dx
        self.dy = dy
        self.lifetime = lifetime
        self.age = 0
        
    def update(self):
        """Update particle position and age. Returns True if still alive"""
        self.x += self.dx
        self.y += self.dy
        self.dy += 0.3  # Gravity effect
        self.age += 1
        return self.age < self.lifetime
        
    def draw(self, surface, camera_x, camera_y):
        """Render particle to screen"""
        # Fade out over lifetime
        alpha = int(255 * (1 - self.age / self.lifetime))
        size = max(1, 4 - self.age // 5)
        
        screen_x = int(self.x - camera_x)
        screen_y = int(self.y - camera_y)
        
        pygame.draw.circle(surface, self.color, (screen_x, screen_y), size)