"""
Menu screens with modern, clean design
"""
import pygame
from config.settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE, YELLOW, CYAN, 
    GRAY, CHARACTER_COLORS, UI_BG, UI_BORDER, UI_HIGHLIGHT, UI_TEXT, UI_TEXT_DIM
)

class Menu:
    """Handles all menu screens with modern, clean design"""
    
    def __init__(self, font_large, font_medium, font_small):
        """Initialize with cleaner, smaller fonts"""
        self.font_large = pygame.font.Font(None, 52)      # Title font
        self.font_medium = pygame.font.Font(None, 32)     # Button/option font
        self.font_small = pygame.font.Font(None, 22)      # Info font
        self.font_tiny = pygame.font.Font(None, 18)       # Hint font
        
    def draw_main_menu(self, surface, selection):
        """Draw main menu with modern design"""
        surface.fill(BLACK)
        
        # Title
        title = self.font_large.render("RETRO PLATFORMER", True, UI_HIGHLIGHT)
        surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))
        
        # Subtitle
        subtitle = self.font_small.render("2D Side-Scrolling Action", True, UI_TEXT_DIM)
        surface.blit(subtitle, (SCREEN_WIDTH // 2 - subtitle.get_width() // 2, 160))
        
        # Menu options
        options = ["New Game", "Load Game", "Controls", "Level Map", "Quit"]
        start_y = 260
        
        for i, option in enumerate(options):
            y = start_y + i * 55
            is_selected = i == selection
            
            # Draw button
            self._draw_button(surface, option, y, is_selected)
        
        # Controls hint
        hint = self.font_tiny.render("↑↓ Navigate   ENTER Select   ESC Back", True, UI_TEXT_DIM)
        surface.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, SCREEN_HEIGHT - 35))
    
    def _draw_button(self, surface, text, y, selected):
        """Helper to draw a modern button"""
        button_width = 280
        button_height = 40
        button_x = SCREEN_WIDTH // 2 - button_width // 2
        button_rect = pygame.Rect(button_x, y - 8, button_width, button_height)
        
        if selected:
            pygame.draw.rect(surface, UI_HIGHLIGHT, button_rect, border_radius=5)
            pygame.draw.rect(surface, WHITE, button_rect, 2, border_radius=5)
            text_color = BLACK
        else:
            pygame.draw.rect(surface, UI_BG, button_rect, border_radius=5)
            pygame.draw.rect(surface, UI_BORDER, button_rect, 1, border_radius=5)
            text_color = UI_TEXT
        
        text_surface = self.font_medium.render(text, True, text_color)
        surface.blit(text_surface, (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, y))
        
    def draw_char_select(self, surface, player_name, char_selection):
        """Draw character selection screen"""
        surface.fill(BLACK)
        
        # Title
        title = self.font_large.render("CHARACTER SELECT", True, UI_HIGHLIGHT)
        surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 80))
        
        # Name input
        name_label = self.font_small.render("Enter Name:", True, UI_TEXT_DIM)
        surface.blit(name_label, (SCREEN_WIDTH // 2 - name_label.get_width() // 2, 160))
        
        name_text = self.font_medium.render(f"{player_name}_", True, WHITE)
        surface.blit(name_text, (SCREEN_WIDTH // 2 - name_text.get_width() // 2, 190))
        
        # Characters
        char_y = 280
        for i in range(4):
            x = SCREEN_WIDTH // 2 - 250 + i * 120
            
            # Character preview
            rect = pygame.Rect(x, char_y, 56, 96)
            pygame.draw.rect(surface, CHARACTER_COLORS[i], rect, border_radius=5)
            
            if i == char_selection:
                pygame.draw.rect(surface, YELLOW, rect, 3, border_radius=5)
            else:
                pygame.draw.rect(surface, UI_BORDER, rect, 1, border_radius=5)
            
            # Eyes
            pygame.draw.circle(surface, WHITE, (x + 20, char_y + 30), 6)
            pygame.draw.circle(surface, BLACK, (x + 22, char_y + 30), 3)
        
        # Instructions
        inst1 = self.font_tiny.render("Type name   ←→ Select character   ENTER Start", True, UI_TEXT_DIM)
        surface.blit(inst1, (SCREEN_WIDTH // 2 - inst1.get_width() // 2, SCREEN_HEIGHT - 50))
        
    def draw_pause_menu(self, surface, selection=0):
        """Draw pause menu overlay"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        surface.blit(overlay, (0, 0))
        
        # Paused text
        text = self.font_large.render("PAUSED", True, YELLOW)
        surface.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 
                           SCREEN_HEIGHT // 2 - 120))
        
        # Menu options
        options = ["Resume", "Return to Menu", "Quit Game"]
        for i, option in enumerate(options):
            y = SCREEN_HEIGHT // 2 - 30 + i * 55
            self._draw_button(surface, option, y, i == selection)
        
        inst = self.font_tiny.render("↑↓ Navigate   ENTER Select", True, UI_TEXT_DIM)
        surface.blit(inst, (SCREEN_WIDTH // 2 - inst.get_width() // 2, 
                           SCREEN_HEIGHT // 2 + 120))
        
    def draw_profile_select(self, surface, profiles, selection):
        """Draw profile selection screen"""
        surface.fill(BLACK)
        
        # Title
        title = self.font_large.render("SELECT PROFILE", True, UI_HIGHLIGHT)
        surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 80))
        
        if not profiles:
            text = self.font_medium.render("No saved profiles found", True, UI_TEXT)
            surface.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 250))
            
            inst = self.font_tiny.render("Press ESC to go back", True, UI_TEXT_DIM)
            surface.blit(inst, (SCREEN_WIDTH // 2 - inst.get_width() // 2, 350))
        else:
            # Display profiles
            y_start = 180
            for i, profile in enumerate(profiles):
                y = y_start + i * 70
                is_selected = i == selection
                
                # Profile box
                box_width = 500
                box_height = 60
                box_x = SCREEN_WIDTH // 2 - box_width // 2
                box_rect = pygame.Rect(box_x, y, box_width, box_height)
                
                if is_selected:
                    pygame.draw.rect(surface, UI_HIGHLIGHT, box_rect, border_radius=5)
                    pygame.draw.rect(surface, WHITE, box_rect, 2, border_radius=5)
                    name_color = BLACK
                    stats_color = (40, 40, 40)
                else:
                    pygame.draw.rect(surface, UI_BG, box_rect, border_radius=5)
                    pygame.draw.rect(surface, UI_BORDER, box_rect, 1, border_radius=5)
                    name_color = UI_TEXT
                    stats_color = UI_TEXT_DIM
                
                # Name
                name_text = self.font_medium.render(
                    f"{profile.name} - Char {profile.character + 1}", 
                    True, name_color
                )
                surface.blit(name_text, (box_x + 15, y + 8))
                
                # Stats
                stats_text = self.font_tiny.render(
                    f"Score: {profile.total_score}  |  Levels: {profile.levels_completed}  |  Coins: {profile.coins_collected}",
                    True, stats_color
                )
                surface.blit(stats_text, (box_x + 15, y + 36))
            
            # Instructions
            inst = self.font_tiny.render("↑↓ Select   ENTER Load   ESC Back", True, UI_TEXT_DIM)
            surface.blit(inst, (SCREEN_WIDTH // 2 - inst.get_width() // 2, SCREEN_HEIGHT - 40))
    
    def draw_game_over(self, surface, score):
        """Draw game over screen"""
        surface.fill(BLACK)
        
        text = self.font_large.render("GAME OVER", True, RED)
        surface.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 
                           SCREEN_HEIGHT // 2 - 80))
        
        score_text = self.font_medium.render(f"Final Score: {score}", True, WHITE)
        surface.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 
                                 SCREEN_HEIGHT // 2))
        
        inst = self.font_tiny.render("Press ENTER to return to menu", True, UI_TEXT_DIM)
        surface.blit(inst, (SCREEN_WIDTH // 2 - inst.get_width() // 2, 
                           SCREEN_HEIGHT // 2 + 80))
    
    def draw_controls_screen(self, surface):
        """Draw controls reference screen"""
        surface.fill(BLACK)
        
        # Title
        title = self.font_large.render("CONTROLS", True, UI_HIGHLIGHT)
        surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))
        
        # Two columns
        col1_x = 120
        col2_x = 660
        start_y = 140
        
        # Movement
        self._draw_control_section(surface, col1_x, start_y, "Movement", [
            ("WASD / Arrows", "Move"),
            ("Space", "Jump"),
            ("Space (airborne)", "Double Jump"),
            ("Space (on wall)", "Wall Jump"),
        ])
        
        # Combat
        self._draw_control_section(surface, col2_x, start_y, "Combat", [
            ("Z", "Shoot"),
            ("X", "Melee Attack"),
            ("U", "Upgrade Weapon"),
        ])
        
        # System
        self._draw_control_section(surface, col1_x, start_y + 250, "System", [
            ("P / ESC", "Pause"),
            ("F1", "Toggle Controls"),
            ("F3", "Debug Info"),
            ("F5", "Quick Save"),
        ])
        
        # Hint
        hint = self.font_tiny.render("Press ESC to return", True, UI_TEXT_DIM)
        surface.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, SCREEN_HEIGHT - 40))
    
    def _draw_control_section(self, surface, x, y, title, controls):
        """Helper to draw a control section"""
        # Section title
        title_text = self.font_medium.render(title, True, UI_HIGHLIGHT)
        surface.blit(title_text, (x, y))
        
        # Controls
        y += 40
        for key, action in controls:
            key_text = self.font_small.render(key, True, YELLOW)
            action_text = self.font_small.render(f"— {action}", True, UI_TEXT)
            surface.blit(key_text, (x, y))
            surface.blit(action_text, (x + 170, y))
            y += 32
    
    def draw_level_map_screen(self, surface):
        """Draw level map screen"""
        surface.fill(BLACK)
        
        # Title
        title = self.font_large.render("LEVEL MAP", True, UI_HIGHLIGHT)
        surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 40))
        
        # Act 1 info
        act_title = self.font_medium.render("ACT 1 - FREE VERSION", True, CYAN)
        surface.blit(act_title, (100, 120))
        
        playtime = self.font_small.render("Approx. 2 hours of gameplay", True, UI_TEXT_DIM)
        surface.blit(playtime, (120, 155))
        
        # Levels
        levels = [
            "Level 0: Tutorial - Training Facility",
            "Level 1: The Awakening",
            "Level 2: Rising Conflict", 
            "Level 3: The Ascent",
            "Level 4: Deep Dive",
            "Level 5: Convergence",
            "Level 6: BOSS - Guardian's Lair"
        ]
        
        y = 200
        for i, level in enumerate(levels):
            if "BOSS" in level:
                color = YELLOW
            else:
                color = UI_TEXT
            text = self.font_small.render(level, True, color)
            surface.blit(text, (140, y))
            y += 35
        
        # Future content
        future_y = 470
        future_title = self.font_medium.render("ACTS 2-4 - COMING SOON", True, UI_TEXT_DIM)
        surface.blit(future_title, (100, future_y))
        
        price = self.font_small.render("$1.99 for 6+ hours of additional content", True, UI_TEXT_DIM)
        surface.blit(price, (120, future_y + 35))
        
        # Hint
        hint = self.font_tiny.render("Press ESC to return", True, UI_TEXT_DIM)
        surface.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, SCREEN_HEIGHT - 40))
