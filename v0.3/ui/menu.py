"""
Menu screens (main menu, character select, pause, game over)
"""
import pygame
from config.settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE, YELLOW, CYAN, RED,
    GRAY, CHARACTER_COLORS
)


class Button:
    """Clickable button"""
    def __init__(self, x, y, width, height, text, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.hovered = False
    
    def update(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)
    
    def draw(self, surface, selected=False):
        # Color based on state
        if self.hovered:
            bg_color = (80, 80, 120)
            border_color = YELLOW
        elif selected:
            bg_color = (60, 60, 100)
            border_color = CYAN
        else:
            bg_color = (40, 40, 60)
            border_color = GRAY
        
        pygame.draw.rect(surface, bg_color, self.rect)
        pygame.draw.rect(surface, border_color, self.rect, 3)
        
        text_surf = self.font.render(self.text, True, WHITE)
        text_x = self.rect.centerx - text_surf.get_width() // 2
        text_y = self.rect.centery - text_surf.get_height() // 2
        surface.blit(text_surf, (text_x, text_y))
    
    def is_clicked(self, mouse_pos, mouse_pressed):
        return self.rect.collidepoint(mouse_pos) and mouse_pressed


class Menu:
    """Handles all menu screens"""
    
    def __init__(self, font_large, font_medium, font_small):
        """
        Args:
            font_large, font_medium, font_small: Pygame fonts
        """
        self.font_large = font_large
        self.font_medium = font_medium
        self.font_small = font_small
        self._create_buttons()

    def _create_buttons(self):
        """Create all menu buttons"""
        center_x = SCREEN_WIDTH // 2
        btn_width = 300
        btn_height = 60
        
        # Main menu buttons
        self.main_buttons = [
            Button(center_x - btn_width//2, 350, btn_width, btn_height, "New Game", self.font_medium),
            Button(center_x - btn_width//2, 430, btn_width, btn_height, "Load Game", self.font_medium),
            Button(center_x - btn_width//2, 510, btn_width, btn_height, "Quit", self.font_medium)
        ]
        
        # Pause menu buttons
        self.pause_buttons = [
            Button(center_x - btn_width//2, 300, btn_width, btn_height, "Resume", self.font_medium),
            Button(center_x - btn_width//2, 380, btn_width, btn_height, "Main Menu", self.font_medium),
            Button(center_x - btn_width//2, 460, btn_width, btn_height, "Quit Game", self.font_medium)
        ]

        # Difficulty buttons
        self.difficulty_buttons = [
            Button(center_x - btn_width//2, 250, btn_width, btn_height, "EASY", self.font_medium),
            Button(center_x - btn_width//2, 350, btn_width, btn_height, "NORMAL", self.font_medium),
            Button(center_x - btn_width//2, 450, btn_width, btn_height, "HARD", self.font_medium)
        ]
        
        # Character select buttons
        self.char_buttons = [
            Button(center_x - 240 + i * 120, 350, 96, 96, "", self.font_small)
            for i in range(4)
        ]
        self.start_button = Button(center_x - 100, 520, 200, 50, "START", self.font_medium)
        self.back_button = Button(50, 50, 120, 40, "< BACK", self.font_small)
    
    def check_button_click(self, buttons, mouse_pos, mouse_pressed):
        """Return index of clicked button or -1"""
        for i, btn in enumerate(buttons):
            if btn.is_clicked(mouse_pos, mouse_pressed):
                return i
        return -1
    
    def draw_main_menu(self, surface, selection, mouse_pos=None):
        """
        Draw main menu
        Args:
            surface: Pygame surface
            selection: Currently selected option index
            mouse_pos: Current mouse position (optional)
        """
        surface.fill(BLACK)
        
        # Title
        title = self.font_large.render("RETRO PLATFORMER", True, CYAN)
        surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 150))
        
        # Buttons
        if mouse_pos:
            for btn in self.main_buttons:
                btn.update(mouse_pos)
        
        for i, btn in enumerate(self.main_buttons):
            btn.draw(surface, selected=(i == selection))
        
        # Instructions
        inst = self.font_small.render("Arrow Keys + ENTER  or  Click with Mouse", True, GRAY)
        surface.blit(inst, (SCREEN_WIDTH // 2 - inst.get_width() // 2, 600))
        
    def draw_char_select(self, surface, player_name, char_selection, mouse_pos=None):
        """Draw character selection with buttons"""
        surface.fill(BLACK)
        
        # Back button
        if mouse_pos:
            self.back_button.update(mouse_pos)
        self.back_button.draw(surface)
        
        # Title
        title = self.font_large.render("CHARACTER SELECT", True, CYAN)
        surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))
        
        # Name input box
        name_box = pygame.Rect(340, 190, 600, 60)
        pygame.draw.rect(surface, (40, 40, 60), name_box)
        pygame.draw.rect(surface, CYAN, name_box, 2)
        name_text = self.font_medium.render(f"{player_name}_", True, WHITE)
        surface.blit(name_text, (360, 205))
        
        # Character buttons
        if mouse_pos:
            for btn in self.char_buttons:
                btn.update(mouse_pos)
        
        for i, btn in enumerate(self.char_buttons):
            # Draw character preview inside button
            is_selected = (i == char_selection)
            if btn.hovered:
                border = YELLOW
                bg = (80, 80, 120)
            elif is_selected:
                border = CYAN
                bg = (60, 60, 100)
            else:
                border = GRAY
                bg = (40, 40, 60)
            
            pygame.draw.rect(surface, bg, btn.rect)
            pygame.draw.rect(surface, border, btn.rect, 3)
            
            # Character inside
            char_rect = pygame.Rect(btn.rect.x + 20, btn.rect.y + 10, 56, 76)
            pygame.draw.rect(surface, CHARACTER_COLORS[i], char_rect)
            pygame.draw.circle(surface, WHITE, (char_rect.x + 20, char_rect.y + 24), 8)
            pygame.draw.circle(surface, BLACK, (char_rect.x + 24, char_rect.y + 24), 4)
        
        # Start button
        if mouse_pos:
            self.start_button.update(mouse_pos)
        self.start_button.draw(surface, selected=False)
        
        # Instructions
        inst = self.font_small.render("Type name, click character, then START", True, GRAY)
        surface.blit(inst, (SCREEN_WIDTH // 2 - inst.get_width() // 2, 580))
        
    def draw_pause_menu(self, surface, selection=0, mouse_pos=None):
        """
        Draw pause menu overlay
        Args:
            surface: Pygame surface
            selection: Currently selected option
            mouse_pos: Current mouse position (optional)
        """
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        surface.blit(overlay, (0, 0))
        
        # Paused text
        text = self.font_large.render("PAUSED", True, YELLOW)
        surface.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 180))
        
        # Buttons
        if mouse_pos:
            for btn in self.pause_buttons:
                btn.update(mouse_pos)
        
        for i, btn in enumerate(self.pause_buttons):
            btn.draw(surface, selected=(i == selection))
        
        inst = self.font_small.render("Arrow Keys + ENTER  or  Click", True, GRAY)
        surface.blit(inst, (SCREEN_WIDTH // 2 - inst.get_width() // 2, 580))
        
    def draw_profile_select(self, surface, profiles, selection, mouse_pos=None):
        """
        Draw profile selection screen
        Args:
            surface: Pygame surface
            profiles: List of PlayerProfile objects
            selection: Currently selected profile index
        """
        surface.fill(BLACK)
        
        # Back button
        if mouse_pos:
            self.back_button.update(mouse_pos)
        self.back_button.draw(surface)
        
        # Title
        title = self.font_large.render("LOAD GAME", True, CYAN)
        surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))
        
        if not profiles:
            text = self.font_medium.render("No saved games", True, WHITE)
            surface.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 250))
        else:
            # Create buttons for each profile
            y_start = 150
            for i, profile in enumerate(profiles):
                y = y_start + i * 100
                
                # Profile box
                box = pygame.Rect(150, y - 10, 780, 90)
                if mouse_pos and box.collidepoint(mouse_pos):
                    bg = (60, 60, 100)
                elif i == selection:
                    bg = (40, 40, 80)
                else:
                    bg = (30, 30, 50)
                
                pygame.draw.rect(surface, bg, box)
                pygame.draw.rect(surface, CYAN if i == selection else GRAY, box, 2)
                
                # Profile info
                name_text = self.font_medium.render(
                    f"{profile.name} - Char {profile.character + 1}", 
                    True, YELLOW if i == selection else WHITE
                )
                surface.blit(name_text, (200, y))
                
                stats_text = self.font_small.render(
                    f"Score: {profile.total_score} | Lvl: {profile.levels_completed} | Coins: {profile.coins_collected}",
                    True, GRAY
                )
                surface.blit(stats_text, (200, y + 35))
                
                # Load button
                load_btn = Button(750, y + 10, 80, 40, "LOAD", self.font_small)
                if mouse_pos:
                    load_btn.update(mouse_pos)
                load_btn.draw(surface)
                
                # Delete button
                del_btn = Button(840, y + 10, 80, 40, "DEL", self.font_small)
                if mouse_pos:
                    del_btn.update(mouse_pos)
                del_btn.draw(surface)
        
        inst = self.font_small.render("Click to select • L: Load • D: Delete • ESC: Back", True, GRAY)
        surface.blit(inst, (SCREEN_WIDTH // 2 - inst.get_width() // 2, 580))
    
    def draw_game_over(self, surface, score):
        """
        Draw game over screen
        Args:
            surface: Pygame surface
            score: Final score
        """
        surface.fill(BLACK)
        
        # Game Over text
        text = self.font_large.render("GAME OVER", True, RED)
        surface.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 
                           SCREEN_HEIGHT // 2 - 100))
        
        # Score
        score_text = self.font_medium.render(f"Final Score: {score}", True, WHITE)
        surface.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 
                                 SCREEN_HEIGHT // 2))
        
        # Instructions
        inst = self.font_small.render("Press ENTER to return to menu", True, GRAY)
        surface.blit(inst, (SCREEN_WIDTH // 2 - inst.get_width() // 2, 
                           SCREEN_HEIGHT // 2 + 100))
        

    def draw_difficulty_select(self, surface, selection, mouse_pos=None):
        """
        Draw difficulty selection screen
        Args:
            surface: Pygame surface
            selection: Currently selected difficulty (0=Easy, 1=Normal, 2=Hard)
            mouse_pos: Current mouse position (optional)
        """
        surface.fill(BLACK)
    
        # Back button
        if mouse_pos:
            self.back_button.update(mouse_pos)
        self.back_button.draw(surface)
        
        # Title
        title = self.font_large.render("SELECT DIFFICULTY", True, CYAN)
        surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))
        
        # Difficulty descriptions
        descriptions = [
            ("5 Lives • More Resources • Forgiving", (0, 255, 0)),      # GREEN
            ("3 Lives • Balanced Challenge • Standard", WHITE),
            ("1 Life • Extreme Challenge • 2x Score", RED)
        ]
        
        # Update and draw buttons
        if mouse_pos:
            for btn in self.difficulty_buttons:
                btn.update(mouse_pos)
        
        for i, (btn, (desc, color)) in enumerate(zip(self.difficulty_buttons, descriptions)):
            btn.draw(surface, selected=(i == selection))
            
            # Description below button
            desc_text = self.font_small.render(desc, True, color)
            desc_x = SCREEN_WIDTH // 2 - desc_text.get_width() // 2
            desc_y = btn.rect.bottom + 10
            surface.blit(desc_text, (desc_x, desc_y))
        
        # Instructions
        inst = self.font_small.render("Arrow Keys + ENTER  or  Click to Select", True, GRAY)
        surface.blit(inst, (SCREEN_WIDTH // 2 - inst.get_width() // 2, 600))

    def draw_victory(self, surface, score):
        """
        Draw victory/game complete screen
        Args:
            surface: Pygame surface
            score: Final score
        """
        surface.fill((0, 0, 0))  # BLACK
        
        # Victory text
        victory = self.font_large.render("VICTORY!", True, (255, 215, 0))  # GOLD
        surface.blit(victory, (640 - victory.get_width() // 2, 200))
        
        # Congratulations
        congrats = self.font_medium.render("You completed Act 1!", True, (255, 255, 255))  # WHITE
        surface.blit(congrats, (640 - congrats.get_width() // 2, 300))
        
        # Score
        score_text = self.font_medium.render(f"Final Score: {score}", True, (0, 255, 255))  # CYAN
        surface.blit(score_text, (640 - score_text.get_width() // 2, 380))
        
        # Message
        msg = self.font_small.render("Your progress has been saved to the hall of champions!", 
                                    True, (200, 200, 200))  # GRAY
        surface.blit(msg, (640 - msg.get_width() // 2, 460))
        
        # Continue
        cont = self.font_small.render("Press ENTER to return to menu", True, (100, 100, 100))  # GRAY
        surface.blit(cont, (640 - cont.get_width() // 2, 550))