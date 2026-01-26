"""
Icon System - Programmatically drawn icons for consistent display
Replaces unicode characters that don't render properly
"""

import pygame
from config.settings import UI_HIGHLIGHT, UI_TEXT_DIM, WHITE, BLACK


class IconRenderer:
    """Renders icons programmatically for cross-platform compatibility"""
    
    @staticmethod
    def draw_checkmark(surface, x, y, size=20, color=(100, 255, 100)):
        """Draw checkmark icon"""
        # Checkmark path
        points = [
            (x + size * 0.2, y + size * 0.5),
            (x + size * 0.4, y + size * 0.7),
            (x + size * 0.8, y + size * 0.3)
        ]
        pygame.draw.lines(surface, color, False, points, 3)
    
    @staticmethod
    def draw_lock(surface, x, y, size=20, color=(150, 150, 150)):
        """Draw lock icon"""
        # Lock body (rectangle)
        body_rect = pygame.Rect(x + size * 0.25, y + size * 0.5, 
                               size * 0.5, size * 0.4)
        pygame.draw.rect(surface, color, body_rect, border_radius=2)
        
        # Lock shackle (arc)
        shackle_rect = pygame.Rect(x + size * 0.3, y + size * 0.2,
                                   size * 0.4, size * 0.4)
        pygame.draw.arc(surface, color, shackle_rect, 0, 3.14159, 3)
    
    @staticmethod
    def draw_back_arrow(surface, x, y, size=20, color=WHITE):
        """Draw back arrow (left arrow)"""
        # Arrow shaft
        pygame.draw.line(surface, color, 
                        (x + size * 0.8, y + size * 0.5),
                        (x + size * 0.2, y + size * 0.5), 3)
        
        # Arrow head
        points = [
            (x + size * 0.2, y + size * 0.5),
            (x + size * 0.4, y + size * 0.3),
        ]
        pygame.draw.line(surface, color, points[0], points[1], 3)
        
        points = [
            (x + size * 0.2, y + size * 0.5),
            (x + size * 0.4, y + size * 0.7),
        ]
        pygame.draw.line(surface, color, points[0], points[1], 3)
    
    @staticmethod
    def draw_settings_gear(surface, x, y, size=20, color=WHITE):
        """Draw settings gear icon"""
        center = (x + size // 2, y + size // 2)
        outer_radius = size // 2
        inner_radius = size // 3
        
        # Draw gear teeth (8 teeth)
        for i in range(8):
            angle = i * 3.14159 / 4
            # Outer point
            ox = center[0] + outer_radius * pygame.math.Vector2(1, 0).rotate_rad(angle).x
            oy = center[1] + outer_radius * pygame.math.Vector2(1, 0).rotate_rad(angle).y
            # Inner point
            ix = center[0] + (inner_radius + 2) * pygame.math.Vector2(1, 0).rotate_rad(angle).x
            iy = center[1] + (inner_radius + 2) * pygame.math.Vector2(1, 0).rotate_rad(angle).y
            
            pygame.draw.line(surface, color, (ox, oy), (ix, iy), 2)
        
        # Center circle
        pygame.draw.circle(surface, color, center, inner_radius, 2)
        pygame.draw.circle(surface, BLACK, center, inner_radius - 3)
    
    @staticmethod
    def draw_up_arrow(surface, x, y, size=20, color=WHITE):
        """Draw up arrow"""
        # Arrow shaft
        pygame.draw.line(surface, color,
                        (x + size * 0.5, y + size * 0.2),
                        (x + size * 0.5, y + size * 0.8), 3)
        
        # Arrow head
        points = [
            (x + size * 0.5, y + size * 0.2),
            (x + size * 0.3, y + size * 0.4),
        ]
        pygame.draw.line(surface, color, points[0], points[1], 3)
        
        points = [
            (x + size * 0.5, y + size * 0.2),
            (x + size * 0.7, y + size * 0.4),
        ]
        pygame.draw.line(surface, color, points[0], points[1], 3)
    
    @staticmethod
    def draw_down_arrow(surface, x, y, size=20, color=WHITE):
        """Draw down arrow"""
        # Arrow shaft
        pygame.draw.line(surface, color,
                        (x + size * 0.5, y + size * 0.2),
                        (x + size * 0.5, y + size * 0.8), 3)
        
        # Arrow head
        points = [
            (x + size * 0.5, y + size * 0.8),
            (x + size * 0.3, y + size * 0.6),
        ]
        pygame.draw.line(surface, color, points[0], points[1], 3)
        
        points = [
            (x + size * 0.5, y + size * 0.8),
            (x + size * 0.7, y + size * 0.6),
        ]
        pygame.draw.line(surface, color, points[0], points[1], 3)
    
    @staticmethod
    def draw_left_arrow(surface, x, y, size=20, color=WHITE):
        """Draw left arrow"""
        # Arrow shaft
        pygame.draw.line(surface, color,
                        (x + size * 0.2, y + size * 0.5),
                        (x + size * 0.8, y + size * 0.5), 3)
        
        # Arrow head
        points = [
            (x + size * 0.2, y + size * 0.5),
            (x + size * 0.4, y + size * 0.3),
        ]
        pygame.draw.line(surface, color, points[0], points[1], 3)
        
        points = [
            (x + size * 0.2, y + size * 0.5),
            (x + size * 0.4, y + size * 0.7),
        ]
        pygame.draw.line(surface, color, points[0], points[1], 3)
    
    @staticmethod
    def draw_right_arrow(surface, x, y, size=20, color=WHITE):
        """Draw right arrow"""
        # Arrow shaft
        pygame.draw.line(surface, color,
                        (x + size * 0.2, y + size * 0.5),
                        (x + size * 0.8, y + size * 0.5), 3)
        
        # Arrow head
        points = [
            (x + size * 0.8, y + size * 0.5),
            (x + size * 0.6, y + size * 0.3),
        ]
        pygame.draw.line(surface, color, points[0], points[1], 3)
        
        points = [
            (x + size * 0.8, y + size * 0.5),
            (x + size * 0.6, y + size * 0.7),
        ]
        pygame.draw.line(surface, color, points[0], points[1], 3)
    
    @staticmethod
    def draw_play(surface, x, y, size=20, color=WHITE):
        """Draw play icon (triangle)"""
        points = [
            (x + size * 0.3, y + size * 0.2),
            (x + size * 0.3, y + size * 0.8),
            (x + size * 0.7, y + size * 0.5)
        ]
        pygame.draw.polygon(surface, color, points)
    
    @staticmethod
    def draw_pause(surface, x, y, size=20, color=WHITE):
        """Draw pause icon (two bars)"""
        bar_width = size * 0.25
        bar_height = size * 0.6
        
        # Left bar
        pygame.draw.rect(surface, color,
                        (x + size * 0.25, y + size * 0.2, bar_width, bar_height))
        
        # Right bar
        pygame.draw.rect(surface, color,
                        (x + size * 0.5, y + size * 0.2, bar_width, bar_height))
    
    @staticmethod
    def draw_cross(surface, x, y, size=20, color=(220, 80, 80)):
        """Draw X/cross icon"""
        # Line 1
        pygame.draw.line(surface, color,
                        (x + size * 0.3, y + size * 0.3),
                        (x + size * 0.7, y + size * 0.7), 3)
        
        # Line 2
        pygame.draw.line(surface, color,
                        (x + size * 0.7, y + size * 0.3),
                        (x + size * 0.3, y + size * 0.7), 3)
    
    @staticmethod
    def draw_home(surface, x, y, size=20, color=WHITE):
        """Draw home icon"""
        # Roof
        points = [
            (x + size * 0.2, y + size * 0.5),
            (x + size * 0.5, y + size * 0.2),
            (x + size * 0.8, y + size * 0.5)
        ]
        pygame.draw.lines(surface, color, False, points, 3)
        
        # House body
        body_rect = pygame.Rect(x + size * 0.25, y + size * 0.45,
                               size * 0.5, size * 0.4)
        pygame.draw.rect(surface, color, body_rect, 2)
    
    @staticmethod
    def draw_trophy(surface, x, y, size=20, color=(255, 215, 0)):
        """Draw trophy icon"""
        # Cup
        points = [
            (x + size * 0.3, y + size * 0.3),
            (x + size * 0.35, y + size * 0.6),
            (x + size * 0.65, y + size * 0.6),
            (x + size * 0.7, y + size * 0.3)
        ]
        pygame.draw.lines(surface, color, False, points, 2)
        
        # Base
        pygame.draw.line(surface, color,
                        (x + size * 0.4, y + size * 0.7),
                        (x + size * 0.6, y + size * 0.7), 2)
        
        # Stem
        pygame.draw.line(surface, color,
                        (x + size * 0.5, y + size * 0.6),
                        (x + size * 0.5, y + size * 0.7), 2)
    
    @staticmethod
    def draw_star(surface, x, y, size=20, color=(255, 215, 0)):
        """Draw star icon"""
        # 5-point star
        points = []
        for i in range(5):
            # Outer point
            angle = i * 2 * 3.14159 / 5 - 3.14159 / 2
            ox = x + size * 0.5 + size * 0.4 * pygame.math.Vector2(1, 0).rotate_rad(angle).x
            oy = y + size * 0.5 + size * 0.4 * pygame.math.Vector2(1, 0).rotate_rad(angle).y
            points.append((ox, oy))
            
            # Inner point
            angle = (i * 2 + 1) * 3.14159 / 5 - 3.14159 / 2
            ix = x + size * 0.5 + size * 0.2 * pygame.math.Vector2(1, 0).rotate_rad(angle).x
            iy = y + size * 0.5 + size * 0.2 * pygame.math.Vector2(1, 0).rotate_rad(angle).y
            points.append((ix, iy))
        
        pygame.draw.polygon(surface, color, points)
    
    @staticmethod
    def draw_info(surface, x, y, size=20, color=WHITE):
        """Draw info icon (i in circle)"""
        center = (x + size // 2, y + size // 2)
        radius = size // 2
        
        # Circle
        pygame.draw.circle(surface, color, center, radius, 2)
        
        # Dot
        pygame.draw.circle(surface, color, (center[0], center[1] - size * 0.2), 2)
        
        # Line
        pygame.draw.line(surface, color,
                        (center[0], center[1] - size * 0.05),
                        (center[0], center[1] + size * 0.3), 3)


class Icon:
    """Icon wrapper for easy use in UI"""
    
    CHECKMARK = "checkmark"
    LOCK = "lock"
    BACK_ARROW = "back_arrow"
    SETTINGS = "settings"
    UP_ARROW = "up_arrow"
    DOWN_ARROW = "down_arrow"
    LEFT_ARROW = "left_arrow"
    RIGHT_ARROW = "right_arrow"
    PLAY = "play"
    PAUSE = "pause"
    CROSS = "cross"
    HOME = "home"
    TROPHY = "trophy"
    STAR = "star"
    INFO = "info"
    
    @staticmethod
    def draw(surface, icon_type, x, y, size=20, color=None):
        """Draw icon by type"""
        # Default colors
        if color is None:
            color_map = {
                Icon.CHECKMARK: (100, 255, 100),
                Icon.LOCK: (150, 150, 150),
                Icon.BACK_ARROW: WHITE,
                Icon.SETTINGS: WHITE,
                Icon.CROSS: (220, 80, 80),
                Icon.TROPHY: (255, 215, 0),
                Icon.STAR: (255, 215, 0),
            }
            color = color_map.get(icon_type, WHITE)
        
        # Draw icon
        if icon_type == Icon.CHECKMARK:
            IconRenderer.draw_checkmark(surface, x, y, size, color)
        elif icon_type == Icon.LOCK:
            IconRenderer.draw_lock(surface, x, y, size, color)
        elif icon_type == Icon.BACK_ARROW:
            IconRenderer.draw_back_arrow(surface, x, y, size, color)
        elif icon_type == Icon.SETTINGS:
            IconRenderer.draw_settings_gear(surface, x, y, size, color)
        elif icon_type == Icon.UP_ARROW:
            IconRenderer.draw_up_arrow(surface, x, y, size, color)
        elif icon_type == Icon.DOWN_ARROW:
            IconRenderer.draw_down_arrow(surface, x, y, size, color)
        elif icon_type == Icon.LEFT_ARROW:
            IconRenderer.draw_left_arrow(surface, x, y, size, color)
        elif icon_type == Icon.RIGHT_ARROW:
            IconRenderer.draw_right_arrow(surface, x, y, size, color)
        elif icon_type == Icon.PLAY:
            IconRenderer.draw_play(surface, x, y, size, color)
        elif icon_type == Icon.PAUSE:
            IconRenderer.draw_pause(surface, x, y, size, color)
        elif icon_type == Icon.CROSS:
            IconRenderer.draw_cross(surface, x, y, size, color)
        elif icon_type == Icon.HOME:
            IconRenderer.draw_home(surface, x, y, size, color)
        elif icon_type == Icon.TROPHY:
            IconRenderer.draw_trophy(surface, x, y, size, color)
        elif icon_type == Icon.STAR:
            IconRenderer.draw_star(surface, x, y, size, color)
        elif icon_type == Icon.INFO:
            IconRenderer.draw_info(surface, x, y, size, color)
