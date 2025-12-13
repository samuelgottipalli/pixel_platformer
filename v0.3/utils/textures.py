import pygame
import math

class TextureManager:
    """Creates patterns and textures for game objects"""
    
    @staticmethod
    def draw_striped_rect(surface, rect, base_color, stripe_color, stripe_width=4, vertical=True):
        """Draw rectangle with stripes"""
        pygame.draw.rect(surface, base_color, rect)
        
        if vertical:
            for x in range(rect.left, rect.right, stripe_width * 2):
                stripe_rect = pygame.Rect(x, rect.top, stripe_width, rect.height)
                pygame.draw.rect(surface, stripe_color, stripe_rect)
        else:
            for y in range(rect.top, rect.bottom, stripe_width * 2):
                stripe_rect = pygame.Rect(rect.left, y, rect.width, stripe_width)
                pygame.draw.rect(surface, stripe_color, stripe_rect)
    
    @staticmethod
    def draw_checkered_rect(surface, rect, color1, color2, check_size=8):
        """Draw rectangle with checkerboard pattern"""
        for y in range(rect.top, rect.bottom, check_size):
            for x in range(rect.left, rect.right, check_size):
                # Alternate colors in checkerboard pattern
                row = (y - rect.top) // check_size
                col = (x - rect.left) // check_size
                color = color1 if (row + col) % 2 == 0 else color2
                
                check_rect = pygame.Rect(x, y, 
                                        min(check_size, rect.right - x),
                                        min(check_size, rect.bottom - y))
                pygame.draw.rect(surface, color, check_rect)
    
    @staticmethod
    def draw_dotted_rect(surface, rect, base_color, dot_color, dot_size=2, spacing=6):
        """Draw rectangle with dot pattern"""
        pygame.draw.rect(surface, base_color, rect)
        
        for y in range(rect.top + spacing//2, rect.bottom, spacing):
            for x in range(rect.left + spacing//2, rect.right, spacing):
                pygame.draw.circle(surface, dot_color, (x, y), dot_size)
    
    @staticmethod
    def draw_brick_wall(surface, rect, mortar_color, brick_color):
        """Draw brick wall pattern"""
        brick_height = 16
        brick_width = 32
        mortar_width = 2
        
        y = rect.top
        row = 0
        while y < rect.bottom:
            x = rect.left
            # Offset every other row for brick pattern
            if row % 2 == 1:
                x -= brick_width // 2
            
            while x < rect.right:
                brick_rect = pygame.Rect(x, y, brick_width, brick_height)
                # Clip to boundaries
                brick_rect = brick_rect.clip(rect)
                if brick_rect.width > 0 and brick_rect.height > 0:
                    pygame.draw.rect(surface, brick_color, brick_rect)
                    pygame.draw.rect(surface, mortar_color, brick_rect, mortar_width)
                
                x += brick_width + mortar_width
            
            y += brick_height + mortar_width
            row += 1
    
    @staticmethod
    def draw_diagonal_lines(surface, rect, base_color, line_color, spacing=8, line_width=2):
        """Draw diagonal line pattern"""
        pygame.draw.rect(surface, base_color, rect)
        
        # Draw diagonal lines from top-left to bottom-right
        for offset in range(-rect.height, rect.width, spacing):
            start_x = rect.left + offset
            start_y = rect.top
            end_x = rect.left + offset + rect.height
            end_y = rect.bottom
            
            pygame.draw.line(surface, line_color, (start_x, start_y), (end_x, end_y), line_width)
    
    @staticmethod
    def draw_grid_rect(surface, rect, base_color, grid_color, grid_size=16):
        """Draw rectangle with grid pattern"""
        pygame.draw.rect(surface, base_color, rect)
        
        # Vertical lines
        for x in range(rect.left, rect.right, grid_size):
            pygame.draw.line(surface, grid_color, (x, rect.top), (x, rect.bottom), 1)
        
        # Horizontal lines
        for y in range(rect.top, rect.bottom, grid_size):
            pygame.draw.line(surface, grid_color, (rect.left, y), (rect.right, y), 1)
