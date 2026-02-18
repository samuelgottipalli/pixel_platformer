"""
Explosive Projectile
Timed bomb that explodes after a delay
"""

import pygame
import math

from config.settings import GRAVITY, RED, ORANGE, YELLOW, WHITE


class ExplosiveProjectile:
    """
    Throwable explosive with timed detonation
    """
    
    def __init__(self, x, y, direction, throw_speed=6, fuse_time=2.0, damage=30, radius=50):
        """
        Initialize explosive
        
        Args:
            x, y: Starting position
            direction: Throw direction (1 or -1)
            throw_speed: Initial horizontal velocity
            fuse_time: Time until explosion in seconds
            damage: Explosion damage
            radius: Explosion radius in pixels
        """
        self.x = x
        self.y = y
        self.width = 12
        self.height = 12
        
        # Physics
        self.dx = direction * throw_speed
        self.dy = -4  # Initial upward arc
        
        # Explosion properties
        self.fuse_time = fuse_time
        self.fuse_timer = fuse_time * 60  # Convert to frames (60 FPS)
        self.damage = damage
        self.radius = radius
        
        # State
        self.active = True
        self.exploded = False
        self.explosion_timer = 0
        self.explosion_duration = 15  # frames
        
    def update(self, tiles):
        """Update explosive physics and timer"""
        if self.exploded:
            # Explosion animation
            self.explosion_timer += 1
            if self.explosion_timer >= self.explosion_duration:
                self.active = False
            return
        
        # Update fuse timer
        self.fuse_timer -= 1
        if self.fuse_timer <= 0:
            self._explode()
            return
        
        # Apply gravity
        self.dy += GRAVITY * 0.5  # Half gravity for arc
        
        # Update position
        self.x += self.dx
        self.y += self.dy
        
        # Apply friction
        self.dx *= 0.98
        
        # Check collision with tiles
        self._check_collision(tiles)
    
    def _check_collision(self, tiles):
        """Check collision with tiles"""
        bomb_rect = self.get_rect()
        
        for tile in tiles:
            if tile.get("solid", True) and bomb_rect.colliderect(tile["rect"]):
                # Hit ground/wall - explode immediately
                self._explode()
                return
    
    def _explode(self):
        """Trigger explosion"""
        self.exploded = True
        self.explosion_timer = 0
    
    def get_rect(self):
        """Get collision rectangle"""
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def get_explosion_rect(self):
        """Get explosion damage area"""
        if self.exploded:
            return pygame.Rect(
                self.x - self.radius,
                self.y - self.radius,
                self.radius * 2,
                self.radius * 2
            )
        return None
    
    def is_exploding(self):
        """Check if currently in explosion state"""
        return self.exploded and self.explosion_timer < self.explosion_duration
    
    def draw(self, surface, camera_x, camera_y):
        """Draw explosive or explosion"""
        if self.exploded:
            self._draw_explosion(surface, camera_x, camera_y)
        else:
            self._draw_bomb(surface, camera_x, camera_y)
    
    def _draw_bomb(self, surface, camera_x, camera_y):
        """Draw the bomb projectile"""
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y
        
        # Bomb body (circle)
        center = (int(screen_x + self.width // 2), int(screen_y + self.height // 2))
        radius = self.width // 2
        
        # Flash red when fuse is low
        if self.fuse_timer < 60:  # Less than 1 second
            if self.fuse_timer % 10 < 5:
                color = RED
            else:
                color = ORANGE
        else:
            color = (80, 80, 80)  # Dark gray
        
        pygame.draw.circle(surface, color, center, radius)
        pygame.draw.circle(surface, WHITE, center, radius, 1)
        
        # Fuse (small line)
        fuse_end_x = center[0]
        fuse_end_y = center[1] - radius - 3
        pygame.draw.line(surface, ORANGE, center, (fuse_end_x, fuse_end_y), 2)
        
        # Spark at fuse tip
        if self.fuse_timer % 4 < 2:
            pygame.draw.circle(surface, YELLOW, (fuse_end_x, fuse_end_y), 2)
    
    def _draw_explosion(self, surface, camera_x, camera_y):
        """Draw explosion animation"""
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y
        
        # Explosion grows then shrinks
        progress = self.explosion_timer / self.explosion_duration
        
        if progress < 0.3:
            # Growing phase
            size_mult = progress / 0.3
        else:
            # Shrinking phase
            size_mult = 1.0 - ((progress - 0.3) / 0.7)
        
        current_radius = int(self.radius * size_mult)
        
        # Draw multiple circles for explosion effect
        if current_radius > 0:
            # Outer ring (red)
            pygame.draw.circle(
                surface,
                RED,
                (int(screen_x), int(screen_y)),
                current_radius,
                3
            )
            
            # Middle ring (orange)
            mid_radius = int(current_radius * 0.7)
            if mid_radius > 0:
                pygame.draw.circle(
                    surface,
                    ORANGE,
                    (int(screen_x), int(screen_y)),
                    mid_radius,
                    2
                )
            
            # Inner ring (yellow)
            inner_radius = int(current_radius * 0.4)
            if inner_radius > 0:
                pygame.draw.circle(
                    surface,
                    YELLOW,
                    (int(screen_x), int(screen_y)),
                    inner_radius
                )
