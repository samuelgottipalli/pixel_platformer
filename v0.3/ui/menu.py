"""
Menu screens (main menu, character select, pause, game over)
"""
import pygame
from config.settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE, YELLOW, CYAN, 
    GRAY, CHARACTER_COLORS
)

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
        
    def draw_main_menu(self, surface, selection):
        """
        Draw main menu
        Args:
            surface: Pygame surface
            selection: Currently selected option index
        """
        surface.fill(BLACK)
        
        # Title
        title = self.font_large.render("RETRO PLATFORMER", True, CYAN)
        surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 150))
        
        # Menu options
        options = ["New Game", "Load Game", "Quit"]
        for i, option in enumerate(options):
            color = YELLOW if i == selection else WHITE
            text = self.font_medium.render(option, True, color)
            surface.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 
                               350 + i * 80))
        
        # Instructions
        inst = self.font_small.render("Use Arrow Keys and ENTER", True, GRAY)
        surface.blit(inst, (SCREEN_WIDTH // 2 - inst.get_width() // 2, 600))
        
    def draw_char_select(self, surface, player_name, char_selection):
        """
        Draw character selection screen
        Args:
            surface: Pygame surface
            player_name: Player name being entered
            char_selection: Currently selected character index
        """
        surface.fill(BLACK)
        
        # Title
        title = self.font_large.render("CHARACTER SELECT", True, CYAN)
        surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))
        
        # Name input
        name_text = self.font_medium.render(f"Name: {player_name}_", True, WHITE)
        surface.blit(name_text, (SCREEN_WIDTH // 2 - name_text.get_width() // 2, 200))
        
        # Characters
        for i in range(4):
            x = SCREEN_WIDTH // 2 - 250 + i * 120
            y = 350
            
            # Draw character preview
            rect = pygame.Rect(x, y, 56, 96)
            pygame.draw.rect(surface, CHARACTER_COLORS[i], rect)
            pygame.draw.rect(surface, YELLOW if i == char_selection else WHITE, 
                           rect, 3)
            
            # Eyes
            pygame.draw.circle(surface, WHITE, (x + 20, y + 24), 8)
            pygame.draw.circle(surface, BLACK, (x + 24, y + 24), 4)
        
        # Instructions
        inst1 = self.font_small.render(
            "Type your name, use Arrow Keys to select character", True, GRAY
        )
        inst2 = self.font_small.render("Press ENTER to start", True, GRAY)
        surface.blit(inst1, (SCREEN_WIDTH // 2 - inst1.get_width() // 2, 520))
        surface.blit(inst2, (SCREEN_WIDTH // 2 - inst2.get_width() // 2, 560))
        
    def draw_pause_menu(self, surface, selection=0):
        """
        Draw pause menu overlay
        Args:
            surface: Pygame surface
            selection: Currently selected option
        """
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        surface.blit(overlay, (0, 0))
        
        # Paused text
        text = self.font_large.render("PAUSED", True, YELLOW)
        surface.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 
                           SCREEN_HEIGHT // 2 - 150))
        
        # Menu options
        options = ["Resume", "Return to Main Menu", "Quit Game"]
        for i, option in enumerate(options):
            color = YELLOW if i == selection else WHITE
            option_text = self.font_medium.render(option, True, color)
            surface.blit(option_text, (SCREEN_WIDTH // 2 - option_text.get_width() // 2, 
                                      SCREEN_HEIGHT // 2 - 50 + i * 60))
        
        inst = self.font_small.render("Arrow Keys + ENTER to select", True, GRAY)
        surface.blit(inst, (SCREEN_WIDTH // 2 - inst.get_width() // 2, 
                           SCREEN_HEIGHT // 2 + 150))
        
    def draw_profile_select(self, surface, profiles, selection):
        """
        Draw profile selection screen
        Args:
            surface: Pygame surface
            profiles: List of PlayerProfile objects
            selection: Currently selected profile index
        """
        surface.fill(BLACK)
        
        # Title
        title = self.font_large.render("SELECT PROFILE", True, CYAN)
        surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))
        
        if not profiles:
            # No profiles exist
            text = self.font_medium.render("No saved profiles found", True, WHITE)
            surface.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 300))
            
            inst = self.font_small.render("Press ESC to go back", True, GRAY)
            surface.blit(inst, (SCREEN_WIDTH // 2 - inst.get_width() // 2, 400))
        else:
            # Display profiles
            y_start = 200
            for i, profile in enumerate(profiles):
                color = YELLOW if i == selection else WHITE
                
                # Profile name and character
                name_text = self.font_medium.render(
                    f"{profile.name} - Character {profile.character + 1}", 
                    True, color
                )
                surface.blit(name_text, (SCREEN_WIDTH // 2 - name_text.get_width() // 2, 
                                        y_start + i * 80))
                
                # Stats
                stats_text = self.font_small.render(
                    f"Score: {profile.total_score}  |  Levels: {profile.levels_completed}  |  Coins: {profile.coins_collected}",
                    True, WHITE
                )
                surface.blit(stats_text, (SCREEN_WIDTH // 2 - stats_text.get_width() // 2, 
                                         y_start + i * 80 + 35))
            
            # Instructions
            inst = self.font_small.render("Arrow Keys + ENTER to select  |  ESC to go back", True, GRAY)
            surface.blit(inst, (SCREEN_WIDTH // 2 - inst.get_width() // 2, 550))
        """
        Draw game over screen
        Args:
            surface: Pygame surface
            score: Final score
        """
        surface.fill(BLACK)
        
        text = self.font_large.render("GAME OVER", True, (255, 0, 0))
        surface.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 
                           SCREEN_HEIGHT // 2 - 100))
        
        score_text = self.font_medium.render(f"Final Score: {score}", True, WHITE)
        surface.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 
                                 SCREEN_HEIGHT // 2))
        
        inst = self.font_small.render("Press ENTER to return to menu", True, GRAY)
        surface.blit(inst, (SCREEN_WIDTH // 2 - inst.get_width() // 2, 
                           SCREEN_HEIGHT // 2 + 100))
        

    def draw_difficulty_select(self, surface, selection):
        """
        Draw difficulty selection screen
        Args:
            surface: Pygame surface
            selection: Currently selected difficulty (0=Easy, 1=Normal, 2=Hard)
        """
        surface.fill((0, 0, 0))  # BLACK
        
        # Title
        title = self.font_large.render("SELECT DIFFICULTY", True, (0, 255, 255))  # CYAN
        surface.blit(title, (640 - title.get_width() // 2, 100))
        
        # Difficulty options with descriptions
        difficulties = [
            ("EASY", "5 Lives • More Resources • Forgiving", (0, 255, 0)),      # GREEN
            ("NORMAL", "3 Lives • Balanced Challenge", (255, 255, 255)),        # WHITE
            ("HARD", "1 Life • Extreme Challenge • 2x Score", (255, 0, 0))     # RED
        ]
        
        y_start = 250
        for i, (name, desc, color) in enumerate(difficulties):
            # Highlight selected
            text_color = (255, 255, 0) if i == selection else color  # YELLOW if selected
            
            # Difficulty name
            name_text = self.font_large.render(name, True, text_color)
            surface.blit(name_text, (640 - name_text.get_width() // 2, y_start + i * 120))
            
            # Description
            desc_text = self.font_small.render(desc, True, (200, 200, 200))  # GRAY
            surface.blit(desc_text, (640 - desc_text.get_width() // 2, y_start + i * 120 + 50))
            
            # Selection indicator
            if i == selection:
                indicator = self.font_medium.render(">>>", True, (255, 255, 0))  # YELLOW
                surface.blit(indicator, (200, y_start + i * 120 + 10))
                surface.blit(indicator, (1000, y_start + i * 120 + 10))
        
        # Instructions
        inst = self.font_small.render("Arrow Keys to Select • ENTER to Continue • ESC to Go Back", 
                                    True, (100, 100, 100))  # GRAY
        surface.blit(inst, (640 - inst.get_width() // 2, 600))

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