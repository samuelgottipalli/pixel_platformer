"""
Menu screens with modern design and full mouse support
"""
import pygame
from config.settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE, YELLOW, CYAN, 
    GRAY, CHARACTER_COLORS, UI_BG, UI_BORDER, UI_HIGHLIGHT, UI_TEXT, UI_TEXT_DIM
)

class Menu:
    """Handles all menu screens with modern design and mouse support"""
    
    def __init__(self, font_large, font_medium, font_small):
        """Initialize with cleaner, smaller fonts"""
        self.font_large = pygame.font.Font(None, 52)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 22)
        self.font_tiny = pygame.font.Font(None, 18)
        
    def _draw_button(self, surface, text, y, is_selected):
        """Helper to draw a consistent button"""
        button_width = 280
        button_height = 40
        x = SCREEN_WIDTH // 2 - button_width // 2
        
        # Button background
        button_rect = pygame.Rect(x, y - 8, button_width, button_height)
        
        if is_selected:
            pygame.draw.rect(surface, UI_HIGHLIGHT, button_rect, border_radius=5)
            pygame.draw.rect(surface, WHITE, button_rect, 2, border_radius=5)
            text_color = BLACK
        else:
            pygame.draw.rect(surface, UI_BG, button_rect, border_radius=5)
            pygame.draw.rect(surface, UI_BORDER, button_rect, 1, border_radius=5)
            text_color = UI_TEXT
        
        # Button text
        text_surf = self.font_medium.render(text, True, text_color)
        text_x = x + button_width // 2 - text_surf.get_width() // 2
        text_y = y
        surface.blit(text_surf, (text_x, text_y))
        
    def draw_main_menu(self, surface, selection, mouse_pos=None):
        """Draw main menu with mouse support"""
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
            
            # Check mouse hover
            if mouse_pos:
                button_width = 280
                button_height = 40
                button_x = SCREEN_WIDTH // 2 - button_width // 2
                button_rect = pygame.Rect(button_x, y - 8, button_width, button_height)
                if button_rect.collidepoint(mouse_pos):
                    is_selected = True
            
            self._draw_button(surface, option, y, is_selected)
        
        # Controls hint
        hint = self.font_tiny.render("↑↓ Navigate   ENTER Select   Mouse Click", True, UI_TEXT_DIM)
        surface.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, SCREEN_HEIGHT - 35))
    
    def draw_difficulty_select(self, surface, selection, mouse_pos=None):
        """Draw difficulty selection screen"""
        surface.fill(BLACK)
        
        # Title
        title = self.font_large.render("SELECT DIFFICULTY", True, UI_HIGHLIGHT)
        surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))
        
        # Difficulty options
        difficulties = [
            ("EASY", "More lives, more resources"),
            ("NORMAL", "Balanced challenge"),
            ("HARD", "For skilled players")
        ]
        
        start_y = 240
        for i, (diff, desc) in enumerate(difficulties):
            y = start_y + i * 80
            is_selected = i == selection
            
            # Check mouse hover
            if mouse_pos:
                button_width = 280
                button_height = 60
                button_x = SCREEN_WIDTH // 2 - button_width // 2
                button_rect = pygame.Rect(button_x, y - 8, button_width, button_height)
                if button_rect.collidepoint(mouse_pos):
                    is_selected = True
            
            # Draw difficulty button (larger)
            button_width = 280
            button_height = 60
            x = SCREEN_WIDTH // 2 - button_width // 2
            button_rect = pygame.Rect(x, y - 8, button_width, button_height)
            
            if is_selected:
                pygame.draw.rect(surface, UI_HIGHLIGHT, button_rect, border_radius=5)
                pygame.draw.rect(surface, WHITE, button_rect, 2, border_radius=5)
                title_color = BLACK
                desc_color = (40, 40, 40)
            else:
                pygame.draw.rect(surface, UI_BG, button_rect, border_radius=5)
                pygame.draw.rect(surface, UI_BORDER, button_rect, 1, border_radius=5)
                title_color = UI_TEXT
                desc_color = UI_TEXT_DIM
            
            # Difficulty name
            diff_text = self.font_medium.render(diff, True, title_color)
            surface.blit(diff_text, (x + button_width // 2 - diff_text.get_width() // 2, y))
            
            # Description
            desc_text = self.font_tiny.render(desc, True, desc_color)
            surface.blit(desc_text, (x + button_width // 2 - desc_text.get_width() // 2, y + 30))
        
        # Controls hint
        hint = self.font_tiny.render("↑↓ Select   ENTER Continue   ESC Back   Mouse Click", True, UI_TEXT_DIM)
        surface.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, SCREEN_HEIGHT - 40))
    
    def draw_char_select(self, surface, player_name, char_selection, mouse_pos=None):
        """Draw character selection screen with mouse support"""
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
            
            rect = pygame.Rect(x, char_y, 56, 96)
            is_selected = i == char_selection
            
            # Check mouse hover
            if mouse_pos and rect.collidepoint(mouse_pos):
                is_selected = True
            
            pygame.draw.rect(surface, CHARACTER_COLORS[i], rect, border_radius=5)
            
            if is_selected:
                pygame.draw.rect(surface, YELLOW, rect, 3, border_radius=5)
            else:
                pygame.draw.rect(surface, UI_BORDER, rect, 1, border_radius=5)
            
            # Eyes
            pygame.draw.circle(surface, WHITE, (x + 20, char_y + 30), 6)
            pygame.draw.circle(surface, BLACK, (x + 22, char_y + 30), 3)
        
        # Instructions
        inst = self.font_tiny.render("Type name   ←→ Select   ENTER Start   Mouse Click", True, UI_TEXT_DIM)
        surface.blit(inst, (SCREEN_WIDTH // 2 - inst.get_width() // 2, SCREEN_HEIGHT - 50))
    
    def draw_pause_menu(self, surface, selection=0, mouse_pos=None):
        """Draw pause menu with mouse support"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        surface.blit(overlay, (0, 0))
        
        # Paused text
        text = self.font_large.render("PAUSED", True, YELLOW)
        surface.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 120))
        
        # Options
        options = ["Resume", "Return to Menu", "Quit Game"]
        for i, option in enumerate(options):
            y = SCREEN_HEIGHT // 2 - 30 + i * 55
            is_selected = i == selection
            
            # Check mouse hover
            if mouse_pos:
                button_width = 280
                button_height = 40
                button_x = SCREEN_WIDTH // 2 - button_width // 2
                button_rect = pygame.Rect(button_x, y - 8, button_width, button_height)
                if button_rect.collidepoint(mouse_pos):
                    is_selected = True
            
            self._draw_button(surface, option, y, is_selected)
        
        hint = self.font_tiny.render("↑↓ Navigate   ENTER Select   Mouse Click", True, UI_TEXT_DIM)
        surface.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, SCREEN_HEIGHT // 2 + 120))
    
    def draw_profile_select(self, surface, profiles, selection, mouse_pos=None):
        """Draw profile selection with mouse support"""
        surface.fill(BLACK)
        
        # Title
        title = self.font_large.render("SELECT PROFILE", True, UI_HIGHLIGHT)
        surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 80))
        
        if not profiles:
            text = self.font_medium.render("No saved profiles", True, UI_TEXT)
            surface.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 250))
            
            inst = self.font_tiny.render("ESC to go back", True, UI_TEXT_DIM)
            surface.blit(inst, (SCREEN_WIDTH // 2 - inst.get_width() // 2, 350))
        else:
            y_start = 180
            for i, profile in enumerate(profiles):
                y = y_start + i * 70
                is_selected = i == selection
                
                # Profile box
                box_width = 500
                box_height = 60
                box_x = SCREEN_WIDTH // 2 - box_width // 2
                box_rect = pygame.Rect(box_x, y, box_width, box_height)
                
                # Check mouse hover
                if mouse_pos and box_rect.collidepoint(mouse_pos):
                    is_selected = True
                
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
            
            inst = self.font_tiny.render("↑↓ Select   ENTER Load   ESC Back   Mouse Click", True, UI_TEXT_DIM)
            surface.blit(inst, (SCREEN_WIDTH // 2 - inst.get_width() // 2, SCREEN_HEIGHT - 40))
    
    def draw_controls_screen(self, surface, mouse_pos=None):
        """Draw controls/keybindings screen"""
        surface.fill(BLACK)
        
        # Title
        title = self.font_large.render("CONTROLS", True, UI_HIGHLIGHT)
        surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 60))
        
        # Two-column layout
        left_x = 200
        right_x = 700
        y_start = 150
        line_height = 35
        
        # Left column - Movement
        section_y = y_start
        section_title = self.font_medium.render("MOVEMENT", True, UI_HIGHLIGHT)
        surface.blit(section_title, (left_x, section_y))
        
        controls_left = [
            ("WASD / Arrows", "Move"),
            ("Space", "Jump"),
            ("Space (air)", "Double Jump"),
            ("Space (wall)", "Wall Jump"),
        ]
        
        for i, (key, action) in enumerate(controls_left):
            y = section_y + 40 + i * line_height
            key_text = self.font_small.render(key, True, CYAN)
            action_text = self.font_tiny.render(action, True, UI_TEXT_DIM)
            surface.blit(key_text, (left_x, y))
            surface.blit(action_text, (left_x + 150, y + 3))
        
        # Right column - Combat
        section_y = y_start
        section_title = self.font_medium.render("COMBAT", True, UI_HIGHLIGHT)
        surface.blit(section_title, (right_x, section_y))
        
        controls_right = [
            ("Z", "Shoot"),
            ("X", "Melee Attack"),
            ("U", "Upgrade Weapon"),
        ]
        
        for i, (key, action) in enumerate(controls_right):
            y = section_y + 40 + i * line_height
            key_text = self.font_small.render(key, True, CYAN)
            action_text = self.font_tiny.render(action, True, UI_TEXT_DIM)
            surface.blit(key_text, (right_x, y))
            surface.blit(action_text, (right_x + 150, y + 3))
        
        # System controls (bottom left)
        section_y = y_start + 220
        section_title = self.font_medium.render("SYSTEM", True, UI_HIGHLIGHT)
        surface.blit(section_title, (left_x, section_y))
        
        controls_system = [
            ("P / ESC", "Pause"),
            ("F1", "Toggle Controls"),
            ("F3", "Debug Info"),
            ("F5", "Quick Save"),
        ]
        
        for i, (key, action) in enumerate(controls_system):
            y = section_y + 40 + i * line_height
            key_text = self.font_small.render(key, True, CYAN)
            action_text = self.font_tiny.render(action, True, UI_TEXT_DIM)
            surface.blit(key_text, (left_x, y))
            surface.blit(action_text, (left_x + 150, y + 3))
        
        # Back hint
        hint = self.font_tiny.render("ESC to return to menu", True, UI_TEXT_DIM)
        surface.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, SCREEN_HEIGHT - 40))
    
    def draw_level_map_screen(self, surface, mouse_pos=None):
        """Draw level map/progression screen"""
        surface.fill(BLACK)
        
        # Title
        title = self.font_large.render("LEVEL MAP", True, UI_HIGHLIGHT)
        surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 60))
        
        # Act 1 header
        act_title = self.font_medium.render("ACT 1 - FREE VERSION", True, CYAN)
        surface.blit(act_title, (200, 130))
        
        # Levels
        levels = [
            "Level 0: Training Facility (Tutorial)",
            "Level 1: The Awakening",
            "Level 2: Rising Conflict",
            "Level 3: The Ascent",
            "Level 4: Deep Dive",
            "Level 5: Convergence",
            "Level 6: BOSS - Guardian's Lair",
        ]
        
        y_start = 170
        for i, level in enumerate(levels):
            y = y_start + i * 30
            if "BOSS" in level:
                color = YELLOW
                level_text = self.font_small.render(level, True, color)
            else:
                color = UI_TEXT
                level_text = self.font_small.render(level, True, color)
            surface.blit(level_text, (220, y))
        
        # Future acts (grayed out)
        future_y = y_start + len(levels) * 30 + 40
        future_title = self.font_medium.render("ACTS 2-4", True, UI_TEXT_DIM)
        surface.blit(future_title, (200, future_y))
        
        coming_soon = self.font_tiny.render("Coming Soon - $1.99 (6+ hours more content)", True, UI_TEXT_DIM)
        surface.blit(coming_soon, (220, future_y + 35))
        
        # Back hint
        hint = self.font_tiny.render("ESC to return to menu", True, UI_TEXT_DIM)
        surface.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, SCREEN_HEIGHT - 40))
    
    def draw_game_over(self, surface, score):
        """Draw game over screen"""
        surface.fill(BLACK)
        
        text = self.font_large.render("GAME OVER", True, RED)
        surface.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
        
        score_text = self.font_medium.render(f"Final Score: {score}", True, WHITE)
        surface.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
        
        inst = self.font_tiny.render("ENTER to return to menu", True, UI_TEXT_DIM)
        surface.blit(inst, (SCREEN_WIDTH // 2 - inst.get_width() // 2, SCREEN_HEIGHT // 2 + 100))
    
    def draw_victory(self, surface, score):
        """Draw victory screen"""
        surface.fill(BLACK)
        
        text = self.font_large.render("VICTORY!", True, YELLOW)
        surface.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
        
        score_text = self.font_medium.render(f"Final Score: {score}", True, WHITE)
        surface.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
        
        inst = self.font_tiny.render("ENTER to return to menu", True, UI_TEXT_DIM)
        surface.blit(inst, (SCREEN_WIDTH // 2 - inst.get_width() // 2, SCREEN_HEIGHT // 2 + 100))
