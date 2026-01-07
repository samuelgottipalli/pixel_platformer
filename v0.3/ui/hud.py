"""
In-game HUD with clean design and level/area info
"""
import pygame
from config.settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, RED, GREEN, YELLOW, CYAN, GRAY,
    UI_BG, UI_BORDER, UI_TEXT, UI_TEXT_DIM
)

class HUD:
    """Displays game information with modern, clean design"""
    
    def __init__(self, font_small):
        """Initialize HUD with cleaner fonts"""
        self.font = pygame.font.Font(None, 20)        # Stats font
        self.font_large = pygame.font.Font(None, 24)  # Level name font
        
    def draw(self, surface, player, current_level, area_name="", level_name=""):
        """
        Draw HUD elements
        Args:
            surface: Pygame surface to draw on
            player: Player object
            current_level: Current level number
            area_name: Current area name (e.g., "Area 2: Tower Climb")
            level_name: Current level name (e.g., "Level 1: The Awakening")
        """
        self._draw_health_bar(surface, player)
        self._draw_stats(surface, player)
        self._draw_level_info(surface, current_level, area_name, level_name)
        
    def _draw_health_bar(self, surface, player):
        """Draw compact health bar"""
        health_width = 150
        health_height = 16
        x, y = 15, 15
        
        # Background
        pygame.draw.rect(surface, (60, 0, 0), (x, y, health_width, health_height), border_radius=3)
        
        # Current health
        health_percent = player.health / player.max_health
        health_color = GREEN if health_percent > 0.5 else (YELLOW if health_percent > 0.25 else RED)
        pygame.draw.rect(surface, health_color, 
                        (x, y, health_width * health_percent, health_height), border_radius=3)
        
        # Border
        pygame.draw.rect(surface, UI_BORDER, (x, y, health_width, health_height), 1, border_radius=3)
        
        # Health text
        health_text = self.font.render(f"HP {player.health}/{player.max_health}", True, WHITE)
        surface.blit(health_text, (x + health_width + 8, y))
        
    def _draw_stats(self, surface, player):
        """Draw compact player statistics"""
        stats = [
            (f"Lives: {player.lives}", 15, 40, WHITE),
            (f"Coins: {player.coins}", 15, 60, YELLOW),
            (f"Score: {player.score}", 15, 80, WHITE),
            (f"Weapon Lv{player.weapon_level}", 15, 100, CYAN),
        ]
        
        for text_str, x, y, color in stats:
            text = self.font.render(text_str, True, color)
            surface.blit(text, (x, y))
            
    def _draw_level_info(self, surface, current_level, area_name, level_name):
        """Draw level and area information at top center"""
        # Get act and level info
        act_num = 1  # For now, all levels are Act 1
        
        # Act + Level name
        if level_name:
            level_text = self.font_large.render(f"ACT {act_num} - {level_name}", True, CYAN)
            surface.blit(level_text, (SCREEN_WIDTH // 2 - level_text.get_width() // 2, 8))
        
        # Area name
        if area_name:
            area_text = self.font.render(area_name, True, UI_TEXT_DIM)
            surface.blit(area_text, (SCREEN_WIDTH // 2 - area_text.get_width() // 2, 32))
    
    def draw_message(self, surface, message, duration_frames):
        """Draw temporary message in center of screen"""
        font_large = pygame.font.Font(None, 48)
        text = font_large.render(message, True, YELLOW)
        
        x = SCREEN_WIDTH // 2 - text.get_width() // 2
        y = SCREEN_HEIGHT // 2 - text.get_height() // 2
        
        # Shadow for readability
        shadow = font_large.render(message, True, BLACK)
        surface.blit(shadow, (x + 2, y + 2))
        surface.blit(text, (x, y))
    
    def draw_controls_overlay(self, surface):
        """Draw toggleable controls overlay (F1 to show/hide)"""
        # Background
        overlay = pygame.Surface((280, 260))
        overlay.set_alpha(220)
        overlay.fill(UI_BG)
        overlay_x = SCREEN_WIDTH - 295
        overlay_y = 15
        surface.blit(overlay, (overlay_x, overlay_y))
        
        # Border
        pygame.draw.rect(surface, UI_BORDER, 
                        (overlay_x, overlay_y, 280, 260), 2, border_radius=5)
        
        # Title
        title = self.font_large.render("Controls (F1)", True, CYAN)
        surface.blit(title, (overlay_x + 10, overlay_y + 8))
        
        # Controls
        controls = [
            "WASD/↑↓←→ — Move",
            "Space — Jump",
            "Z — Shoot",
            "X — Melee",
            "U — Upgrade",
            "",
            "P/ESC — Pause",
            "F1 — Hide Controls",
            "F3 — Debug Info",
            "F5 — Quick Save"
        ]
        
        y = overlay_y + 38
        for ctrl in controls:
            if ctrl:
                text = self.font.render(ctrl, True, UI_TEXT)
            else:
                # Separator
                pygame.draw.line(surface, UI_BORDER, 
                               (overlay_x + 10, y + 5), 
                               (overlay_x + 270, y + 5), 1)
            if ctrl:
                surface.blit(text, (overlay_x + 10, y))
            y += 22
