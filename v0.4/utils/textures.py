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


class BackgroundManager:
    """Manages themed backgrounds with parallax scrolling"""
    
    @staticmethod
    def draw_scifi_background(surface, camera_x, camera_y, screen_width, screen_height):
        """Sci-fi tech background with grid and circuit lines"""
        # Base color
        surface.fill((20, 20, 40))
        
        # Layer 1: Large grid (far background, slow parallax)
        grid_offset_x = (camera_x // 4) % 64
        grid_offset_y = (camera_y // 4) % 64
        
        for x in range(-64, screen_width + 64, 64):
            for y in range(-64, screen_height + 64, 64):
                adj_x = x - grid_offset_x
                adj_y = y - grid_offset_y
                # Vertical line
                pygame.draw.line(surface, (40, 40, 80), 
                               (adj_x, 0), (adj_x, screen_height), 1)
                # Horizontal line
                pygame.draw.line(surface, (40, 40, 80), 
                               (0, adj_y), (screen_width, adj_y), 1)
        
        # Layer 2: Circuit board nodes (medium parallax)
        node_offset_x = (camera_x // 2) % 128
        node_offset_y = (camera_y // 2) % 128
        
        for x in range(-128, screen_width + 128, 128):
            for y in range(-128, screen_height + 128, 128):
                adj_x = x - node_offset_x
                adj_y = y - node_offset_y
                # Small tech circles
                pygame.draw.circle(surface, (60, 60, 120), (adj_x, adj_y), 4, 1)
                pygame.draw.circle(surface, (40, 40, 80), (adj_x, adj_y), 8, 1)
    
    @staticmethod
    def draw_nature_background(surface, camera_x, camera_y, screen_width, screen_height):
        """Nature background with tree silhouettes and leaves"""
        # Base color
        surface.fill((40, 60, 40))
        
        # Layer 1: Mountain silhouettes (very slow parallax)
        mountain_offset = (camera_x // 8) % screen_width
        for i in range(3):
            x_offset = -mountain_offset + (i * screen_width // 3)
            # Triangle mountains
            points = [
                (x_offset, screen_height),
                (x_offset + 150, screen_height - 120),
                (x_offset + 300, screen_height)
            ]
            pygame.draw.polygon(surface, (30, 50, 30), points)
        
        # Layer 2: Diagonal texture (medium parallax)
        line_offset_x = (camera_x // 3) % 32
        for x in range(-100, screen_width + 100, 32):
            adj_x = x - line_offset_x
            pygame.draw.line(surface, (50, 70, 50), 
                           (adj_x, 0), (adj_x + screen_height, screen_height), 1)
        
        # Layer 3: Leaf dots (fast parallax)
        leaf_offset_x = (camera_x // 2) % 80
        leaf_offset_y = (camera_y // 2) % 80
        
        import random
        random.seed(42)  # Consistent pattern
        for _ in range(50):
            x = random.randint(0, screen_width)
            y = random.randint(0, screen_height)
            adj_x = (x - leaf_offset_x) % screen_width
            adj_y = (y - leaf_offset_y) % screen_height
            # Small leaf dots
            pygame.draw.circle(surface, (60, 80, 60), (adj_x, adj_y), 2)
    
    @staticmethod
    def draw_space_background(surface, camera_x, camera_y, screen_width, screen_height):
        """Space background with stars and nebula effect"""
        # Base color
        surface.fill((10, 10, 20))
        
        # Layer 1: Nebula clouds (very slow parallax)
        cloud_offset_x = (camera_x // 10) % 200
        cloud_offset_y = (camera_y // 10) % 200
        
        for i in range(5):
            x = (i * 250 - cloud_offset_x) % screen_width
            y = (i * 150 - cloud_offset_y) % screen_height
            # Draw nebula blob
            pygame.draw.circle(surface, (30, 20, 50), (x, y), 80)
            pygame.draw.circle(surface, (20, 15, 35), (x + 20, y + 20), 60)
        
        # Layer 2: Medium stars (medium parallax)
        star_offset_x = (camera_x // 3) % screen_width
        star_offset_y = (camera_y // 3) % screen_height
        
        import random
        random.seed(123)
        for _ in range(100):
            x = random.randint(0, screen_width)
            y = random.randint(0, screen_height)
            adj_x = (x - star_offset_x) % screen_width
            adj_y = (y - star_offset_y) % screen_height
            size = random.choice([1, 2, 3])
            pygame.draw.circle(surface, (200, 200, 255), (adj_x, adj_y), size)
        
        # Layer 3: Close stars (fast parallax)
        close_star_offset_x = (camera_x // 2) % screen_width
        close_star_offset_y = (camera_y // 2) % screen_height
        
        random.seed(456)
        for _ in range(50):
            x = random.randint(0, screen_width)
            y = random.randint(0, screen_height)
            adj_x = (x - close_star_offset_x) % screen_width
            adj_y = (y - close_star_offset_y) % screen_height
            # Twinkling effect based on position
            if ((adj_x + adj_y) // 50) % 2 == 0:
                pygame.draw.circle(surface, WHITE, (adj_x, adj_y), 2)
    
    @staticmethod
    def draw_underground_background(surface, camera_x, camera_y, screen_width, screen_height):
        """Underground cave background with rock texture"""
        # Base color
        surface.fill((30, 20, 15))
        
        # Layer 1: Rock strata lines (slow parallax)
        strata_offset = (camera_y // 5) % 40
        
        for y in range(-40, screen_height + 40, 40):
            adj_y = y - strata_offset
            # Wavy horizontal lines
            points = []
            for x in range(0, screen_width + 20, 20):
                import math
                wave = math.sin((x + camera_x // 3) / 50) * 10
                points.append((x, adj_y + wave))
            if len(points) > 1:
                pygame.draw.lines(surface, (50, 35, 25), False, points, 2)
        
        # Layer 2: Rock dots (medium parallax)
        rock_offset_x = (camera_x // 3) % 60
        rock_offset_y = (camera_y // 3) % 60
        
        import random
        random.seed(789)
        for _ in range(80):
            x = random.randint(0, screen_width)
            y = random.randint(0, screen_height)
            adj_x = (x - rock_offset_x) % screen_width
            adj_y = (y - rock_offset_y) % screen_height
            size = random.choice([2, 3, 4])
            pygame.draw.circle(surface, (60, 45, 35), (adj_x, adj_y), size)
        
        # Layer 3: Stalactite shadows (fast parallax)
        stalactite_offset = (camera_x // 2) % 150
        
        for x in range(-150, screen_width + 150, 150):
            adj_x = x - stalactite_offset
            # Triangle pointing down
            points = [(adj_x, 0), (adj_x - 20, 60), (adj_x + 20, 60)]
            pygame.draw.polygon(surface, (25, 18, 13), points)
    
    @staticmethod
    def draw_underwater_background(surface, camera_x, camera_y, screen_width, screen_height):
        """Underwater background with caustic light patterns"""
        # Base color
        surface.fill((15, 30, 50))
        
        # Layer 1: Light rays from surface (very slow parallax)
        ray_offset = (camera_x // 8) % 200
        
        for i in range(5):
            x = i * 250 - ray_offset
            # Light ray
            points = [
                (x, 0),
                (x + 30, screen_height),
                (x + 50, screen_height),
                (x + 20, 0)
            ]
            pygame.draw.polygon(surface, (25, 45, 70), points)
        
        # Layer 2: Caustic patterns (medium parallax)
        import math
        caustic_offset_x = (camera_x // 3) % 100
        caustic_offset_y = ((camera_y // 3) + pygame.time.get_ticks() // 50) % 100
        
        for x in range(-100, screen_width + 100, 100):
            for y in range(-100, screen_height + 100, 100):
                adj_x = x - caustic_offset_x
                adj_y = y - caustic_offset_y
                # Wavy caustic lines
                wave_x = math.sin((adj_y + pygame.time.get_ticks() / 500) / 20) * 30
                pygame.draw.circle(surface, (30, 50, 80), 
                                 (adj_x + int(wave_x), adj_y), 25, 1)
        
        # Layer 3: Bubbles (fast parallax)
        bubble_offset_x = (camera_x // 2) % screen_width
        bubble_offset_y = ((camera_y // 2) - pygame.time.get_ticks() // 20) % screen_height
        
        import random
        random.seed(101112)
        for _ in range(30):
            x = random.randint(0, screen_width)
            y = random.randint(0, screen_height)
            adj_x = (x - bubble_offset_x) % screen_width
            adj_y = (y + bubble_offset_y) % screen_height  # Bubbles rise
            size = random.choice([3, 4, 5])
            pygame.draw.circle(surface, (50, 80, 120), (adj_x, adj_y), size, 1)
