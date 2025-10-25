"""
In-game HUD (Heads-Up Display)
"""
import pygame
from config.settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, RED, GREEN, YELLOW, CYAN, GRAY
)

class HUD:
    """Displays game information on screen"""
    
    def __init__(self, font_small):
        """
        Args:
            font_small: Pygame font for HUD text
        """
        self.font = font_small
        
    def draw(self, surface, player, current_level):
        """
        Draw HUD elements
        Args:
            surface: Pygame surface to draw on
            player: Player object
            current_level: Current level number
        """
        self._draw_health_bar(surface, player)
        self._draw_stats(surface, player, current_level)
        self._draw_controls(surface)
        
    def _draw_health_bar(self, surface, player):
        """Draw player health bar"""
        health_width = 200
        health_height = 20
        x, y = 20, 20
        
        # Background (red)
        pygame.draw.rect(surface, RED, (x, y, health_width, health_height))
        
        # Current health (green)
        health_percent = player.health / player.max_health
        pygame.draw.rect(surface, GREEN, 
                        (x, y, health_width * health_percent, health_height))
        
        # Border
        pygame.draw.rect(surface, WHITE, (x, y, health_width, health_height), 2)
        
        # Health text
        health_text = self.font.render(
            f"HP: {player.health}/{player.max_health}", 
            True, WHITE
        )
        surface.blit(health_text, (x + health_width + 10, y))
        
    def _draw_stats(self, surface, player, current_level):
        """Draw player statistics"""
        stats = [
            (f"Lives: {player.lives}", 20, 50),
            (f"Coins: {player.coins}", 20, 80),
            (f"Score: {player.score}", 20, 110),
            (f"Weapon Lv: {player.weapon_level}", 20, 140),
            (f"Level: {current_level + 1}", SCREEN_WIDTH - 150, 20)
        ]
        
        for text_str, x, y in stats:
            if "Coins" in text_str:
                color = YELLOW
            elif "Weapon" in text_str:
                color = CYAN
            else:
                color = WHITE
                
            text = self.font.render(text_str, True, color)
            surface.blit(text, (x, y))
            
    def _draw_controls(self, surface):
        """Draw control hints"""
        controls = [
            "WASD/Arrows: Move",
            "Space: Jump",
            "Z: Shoot",
            "X: Melee",
            "U: Upgrade",
            "P/ESC: Pause",
            "F5: Save"
        ]
        
        y_start = SCREEN_HEIGHT - 230
        for i, ctrl in enumerate(controls):
            text = self.font.render(ctrl, True, GRAY)
            text.set_alpha(128)  # Semi-transparent
            surface.blit(text, (SCREEN_WIDTH - 220, y_start + i * 30))
            
    def draw_message(self, surface, message, duration_frames):
        """
        Draw temporary message in center of screen
        Args:
            surface: Pygame surface
            message: Message text
            duration_frames: How long to show (for fading)
        """
        font_large = pygame.font.Font(None, 64)
        text = font_large.render(message, True, YELLOW)
        
        x = SCREEN_WIDTH // 2 - text.get_width() // 2
        y = SCREEN_HEIGHT // 2 - text.get_height() // 2
        
        # Add shadow for readability
        shadow = font_large.render(message, True, (0, 0, 0))
        surface.blit(shadow, (x + 2, y + 2))
        surface.blit(text, (x, y))