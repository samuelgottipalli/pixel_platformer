"""
Refactored Menu System Using Modular Components
Cleaner, more maintainable menu code with reusable components
"""

import pygame
from config.settings import (BLACK, CHARACTER_COLORS, CYAN, SCREEN_HEIGHT,
                             SCREEN_WIDTH, UI_BG, UI_BORDER, UI_HIGHLIGHT,
                             UI_TEXT, UI_TEXT_DIM, WHITE, YELLOW)
from ui.components import (Button, ButtonGroup, LayoutHelper, Popup, Screen,
                           SelectableBox, TextBox)


class MenuManager:
    """Manages all menu screens using modular components"""
    
    def __init__(self, font_large, font_medium, font_small):
        # Fonts
        self.font_large = pygame.font.Font(None, 52)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 22)
        self.font_tiny = pygame.font.Font(None, 18)
        
        # Button groups for each screen
        self.main_menu_buttons = None
        self.options_buttons = None
        self.pause_buttons = None
        self.char_buttons = None
        
        # Initialize button groups
        self._init_main_menu()
        self._init_options_menu()
        self._init_pause_menu()
        self._init_char_select()
    
    # ========================================================================
    # BUTTON GROUP INITIALIZATION
    # ========================================================================
    
    def _init_main_menu(self):
        """Initialize main menu buttons"""
        button_width = 280
        button_height = 40
        x = LayoutHelper.center_x(button_width)
        y_positions = LayoutHelper.create_vertical_layout(240, 5, 55)
        
        options = ["New Game", "Continue", "Level Map", "Options", "Quit"]
        buttons = []
        for i, (option, y) in enumerate(zip(options, y_positions)):
            btn = Button(x, y - 8, button_width, button_height, option, self.font_medium)
            buttons.append(btn)
        
        self.main_menu_buttons = ButtonGroup(buttons)
        self.main_menu_buttons.set_selected(0)
    
    def _init_options_menu(self):
        """Initialize options menu buttons"""
        button_width = 280
        button_height = 40
        x = LayoutHelper.center_x(button_width)
        y_positions = LayoutHelper.create_vertical_layout(220, 4, 55)
        
        options = ["Controls", "Settings", "Credits", "Back to Menu"]
        buttons = []
        for option, y in zip(options, y_positions):
            btn = Button(x, y - 8, button_width, button_height, option, self.font_medium)
            buttons.append(btn)
        
        self.options_buttons = ButtonGroup(buttons)
        self.options_buttons.set_selected(0)
    
    def _init_pause_menu(self):
        """Initialize pause menu buttons"""
        button_width = 300
        button_height = 40
        x = LayoutHelper.center_x(button_width)
        y_positions = LayoutHelper.create_vertical_layout(SCREEN_HEIGHT // 2 - 50, 3, 55)
        
        options = ["Resume", "Save & Return to Menu", "Save & Logout"]
        buttons = []
        for option, y in zip(options, y_positions):
            btn = Button(x, y - 8, button_width, button_height, option, self.font_medium)
            buttons.append(btn)
        
        self.pause_buttons = ButtonGroup(buttons)
    
    def _init_char_select(self):
        """Initialize character selection buttons"""
        char_y = 280
        x_positions = LayoutHelper.create_horizontal_layout(
            SCREEN_WIDTH // 2 - 250, 4, 120
        )
        
        buttons = []
        for x in x_positions:
            btn = Button(x, char_y, 56, 96, "", self.font_small)
            buttons.append(btn)
        
        self.char_buttons = ButtonGroup(buttons, orientation='horizontal')
    
    # ========================================================================
    # MAIN MENU
    # ========================================================================
    
    def draw_main_menu(self, surface, current_profile, selection, mouse_pos=None):
        """Draw main menu using components"""
        screen = Screen("RETRO PLATFORMER", self.font_large, self.font_medium,
                       self.font_small, self.font_tiny)
        screen.draw_background(surface)
        
        # Profile name
        if current_profile:
            profile_text = self.font_small.render(
                f"Profile: {current_profile.name}", True, UI_TEXT_DIM
            )
            surface.blit(profile_text, (20, 20))
        
        # Title
        screen.draw_title(surface, 100)
        
        # Update button group selection
        self.main_menu_buttons.set_selected(selection)
        self.main_menu_buttons.check_hover(mouse_pos)
        
        # Draw buttons
        self.main_menu_buttons.draw(surface)
        
        # Hint
        screen.draw_hint(surface, "↑↓ Navigate   ENTER Select   ESC Logout")
    
    # ========================================================================
    # PROFILE SELECT
    # ========================================================================
    
    def draw_profile_select(self, surface, profiles, selection, mouse_pos=None):
        """Draw profile selection screen"""
        screen = Screen("SELECT PROFILE", self.font_large, self.font_medium,
                       self.font_small, self.font_tiny)
        screen.draw_background(surface)
        screen.draw_title(surface, 60)
        
        if not profiles:
            # No profiles
            msg = self.font_medium.render("No profiles found", True, UI_TEXT)
            surface.blit(msg, (SCREEN_WIDTH // 2 - msg.get_width() // 2, 200))
            
            inst = self.font_small.render(
                "Press N to create new profile", True, UI_HIGHLIGHT
            )
            surface.blit(inst, (SCREEN_WIDTH // 2 - inst.get_width() // 2, 280))
        else:
            # Profile list
            y_start = 160
            for i, profile in enumerate(profiles):
                y = y_start + i * 70
                is_selected = i == selection
                
                # Profile box
                box = SelectableBox(
                    SCREEN_WIDTH // 2 - 250, y, 500, 60,
                    f"{profile.name} - Lvl {profile.levels_completed}",
                    is_unlocked=True
                )
                box.is_selected = is_selected
                box.check_hover(mouse_pos)
                
                # Draw custom profile box
                self._draw_profile_box(surface, box, profile)
            
            # Instructions
            screen.draw_hint(surface,
                "↑↓ Navigate   ENTER/L Load   D Delete   N New Profile",
                SCREEN_HEIGHT - 80)
        
        # New Profile button
        button_y = SCREEN_HEIGHT - 120 if profiles else 350
        new_btn = Button(
            LayoutHelper.center_x(280), button_y - 8,
            280, 40, "New Profile (N)", self.font_medium
        )
        new_btn.draw(surface)
    
    def _draw_profile_box(self, surface, box, profile):
        """Custom profile box drawing"""
        is_active = box.is_selected or box.is_hovered
        
        # Box colors
        border_color = UI_HIGHLIGHT if is_active else UI_BORDER
        
        pygame.draw.rect(surface, UI_BG, box.rect, border_radius=5)
        pygame.draw.rect(surface, border_color, box.rect, 2, border_radius=5)
        
        # Highlight
        if is_active:
            fill_surf = pygame.Surface((box.rect.width - 4, box.rect.height - 4))
            fill_surf.set_alpha(30)
            fill_surf.fill(UI_HIGHLIGHT)
            surface.blit(fill_surf, (box.rect.x + 2, box.rect.y + 2))
        
        # Profile name
        name_text = self.font_medium.render(profile.name, True, UI_TEXT)
        surface.blit(name_text, (box.rect.x + 20, box.rect.y + 8))
        
        # Stats
        stats_text = self.font_tiny.render(
            f"Levels: {profile.levels_completed}  Score: {profile.total_score}  Coins: {profile.coins_collected}",
            True, UI_TEXT_DIM
        )
        surface.blit(stats_text, (box.rect.x + 20, box.rect.y + 35))
    
    # ========================================================================
    # DIFFICULTY SELECT
    # ========================================================================
    
    def draw_difficulty_select(self, surface, selection, mouse_pos=None):
        """Draw difficulty selection"""
        screen = Screen("SELECT DIFFICULTY", self.font_large, self.font_medium,
                       self.font_small, self.font_tiny)
        screen.draw_background(surface)
        screen.draw_title(surface)
        screen.draw_subtitle(surface, "Choose your challenge level")
        
        # Difficulty boxes
        difficulties = [
            ("EASY", "5 Lives • More Resources • 2x Time", (100, 200, 100)),
            ("NORMAL", "3 Lives • Balanced Challenge • Standard", WHITE),
            ("HARD", "1 Life • Extreme Challenge • 2x Score", (220, 80, 80)),
        ]
        
        y_positions = LayoutHelper.create_vertical_layout(220, 3, 120)
        
        for i, ((name, desc, color), y) in enumerate(zip(difficulties, y_positions)):
            is_selected = i == selection
            
            # Check hover
            box_rect = pygame.Rect(
                LayoutHelper.center_x(500), y, 500, 100
            )
            is_hovered = box_rect.collidepoint(mouse_pos) if mouse_pos else False
            is_active = is_selected or is_hovered
            
            # Draw box
            self._draw_difficulty_box(surface, box_rect, name, desc, color, is_active)
        
        screen.draw_hint(surface,
            "↑↓ Select   ENTER Confirm   ESC Back   Mouse Click",
            SCREEN_HEIGHT - 40)
    
    def _draw_difficulty_box(self, surface, rect, name, desc, color, is_active):
        """Draw individual difficulty box"""
        if is_active:
            pygame.draw.rect(surface, UI_HIGHLIGHT, rect, border_radius=8)
            pygame.draw.rect(surface, color, rect, 3, border_radius=8)
            name_color = BLACK
            desc_color = (40, 40, 40)
        else:
            pygame.draw.rect(surface, UI_BG, rect, border_radius=8)
            pygame.draw.rect(surface, color, rect, 2, border_radius=8)
            name_color = color
            desc_color = UI_TEXT_DIM
        
        # Name
        name_surf = self.font_medium.render(name, True, name_color)
        name_x = rect.x + rect.width // 2 - name_surf.get_width() // 2
        surface.blit(name_surf, (name_x, rect.y + 25))
        
        # Description
        desc_surf = self.font_tiny.render(desc, True, desc_color)
        desc_x = rect.x + rect.width // 2 - desc_surf.get_width() // 2
        surface.blit(desc_surf, (desc_x, rect.y + 60))
    
    # ========================================================================
    # CHARACTER SELECT
    # ========================================================================
    
    def draw_char_select(self, surface, player_name, char_selection, mouse_pos=None):
        """Draw character selection"""
        screen = Screen("CHARACTER SELECT", self.font_large, self.font_medium,
                       self.font_small, self.font_tiny)
        screen.draw_background(surface)
        screen.draw_title(surface)
        
        # Name input
        name_label = self.font_small.render("Enter Name:", True, UI_TEXT_DIM)
        surface.blit(name_label, (SCREEN_WIDTH // 2 - name_label.get_width() // 2, 160))
        
        name_text = self.font_medium.render(f"{player_name}_", True, WHITE)
        surface.blit(name_text, (SCREEN_WIDTH // 2 - name_text.get_width() // 2, 190))
        
        # Characters
        self.char_buttons.set_selected(char_selection)
        self.char_buttons.check_hover(mouse_pos)
        
        for i, button in enumerate(self.char_buttons.buttons):
            is_active = button.is_selected or button.is_hovered
            
            # Character box
            pygame.draw.rect(surface, CHARACTER_COLORS[i], button.rect, border_radius=5)
            
            border_color = YELLOW if is_active else UI_BORDER
            border_width = 3 if is_active else 1
            pygame.draw.rect(surface, border_color, button.rect, border_width, border_radius=5)
            
            # Eyes
            pygame.draw.circle(surface, WHITE, (button.rect.x + 20, button.rect.y + 30), 6)
            pygame.draw.circle(surface, BLACK, (button.rect.x + 22, button.rect.y + 30), 3)
        
        screen.draw_hint(surface,
            "Type name   ←→ Select   ENTER Start   Mouse Click",
            SCREEN_HEIGHT - 50)
    
    # ========================================================================
    # OPTIONS MENU
    # ========================================================================
    
    def draw_options_menu(self, surface, selection, mouse_pos=None):
        """Draw options menu"""
        screen = Screen("OPTIONS", self.font_large, self.font_medium,
                       self.font_small, self.font_tiny)
        screen.draw_background(surface)
        screen.draw_title(surface, 100)
        
        self.options_buttons.set_selected(selection)
        self.options_buttons.check_hover(mouse_pos)
        self.options_buttons.draw(surface)
        
        screen.draw_hint(surface, "↑↓ Navigate   ENTER Select   ESC Back")
    
    # ========================================================================
    # PAUSE MENU
    # ========================================================================
    
    def draw_pause_menu(self, surface, selection, mouse_pos=None):
        """Draw pause menu overlay"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        surface.blit(overlay, (0, 0))
        
        # Title
        text = self.font_large.render("PAUSED", True, YELLOW)
        surface.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 
                           SCREEN_HEIGHT // 2 - 140))
        
        # Buttons
        self.pause_buttons.set_selected(selection)
        self.pause_buttons.check_hover(mouse_pos)
        self.pause_buttons.draw(surface)
        
        # Hint
        hint = self.font_tiny.render("↑↓ Navigate   ENTER Select", True, UI_TEXT_DIM)
        surface.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2,
                           SCREEN_HEIGHT // 2 + 140))
    
    # ========================================================================
    # LEVEL MAP
    # ========================================================================
    
    def draw_level_map_screen(self, surface, current_profile, mouse_pos=None):
        """Draw level map with all levels"""
        screen = Screen("LEVEL MAP", self.font_large, self.font_medium,
                       self.font_small, self.font_tiny)
        screen.draw_background(surface)
        screen.draw_title(surface, 60)
        
        # Level names
        level_names = [
            "Tutorial: Training Facility",
            "Level 1: The Awakening",
            "Level 2: Rising Conflict",
            "Level 3: The Ascent",
            "Level 4: Deep Dive",
            "Level 5: Convergence",
            "Level 6: Guardian's Lair (BOSS)",
        ]
        
        # Get unlocked count
        unlocked_count = 0
        if current_profile and hasattr(current_profile, 'levels_completed'):
            unlocked_count = current_profile.levels_completed
        
        # Subtitle
        subtitle = self.font_small.render(
            f"Unlocked: {unlocked_count} / {len(level_names)}", True, UI_TEXT
        )
        surface.blit(subtitle, (SCREEN_WIDTH // 2 - subtitle.get_width() // 2, 130))
        
        # Level list
        y_positions = LayoutHelper.create_vertical_layout(200, len(level_names), 50)
        
        for i, (level_name, y) in enumerate(zip(level_names, y_positions)):
            is_unlocked = i < unlocked_count
            
            # Icon and color
            if is_unlocked:
                icon = "✓"
                icon_color = (100, 255, 100)
                name_color = UI_HIGHLIGHT
            else:
                icon = "🔒"
                icon_color = (150, 150, 150)
                name_color = UI_TEXT_DIM
            
            # Draw icon
            icon_surf = self.font_small.render(icon, True, icon_color)
            surface.blit(icon_surf, (200, y))
            
            # Draw level name
            name_surf = self.font_small.render(level_name, True, name_color)
            surface.blit(name_surf, (250, y))
        
        # Instructions
        if unlocked_count > 0:
            inst = self.font_tiny.render(
                "Level selection coming in Phase 3", True, UI_TEXT_DIM
            )
        else:
            inst = self.font_tiny.render(
                "Complete levels to unlock them here", True, UI_TEXT_DIM
            )
        surface.blit(inst, (SCREEN_WIDTH // 2 - inst.get_width() // 2, SCREEN_HEIGHT - 100))
        
        screen.draw_hint(surface, "ESC to go back")
    
    # ========================================================================
    # PLACEHOLDER SCREENS
    # ========================================================================
    
    def draw_controls_screen(self, surface, mouse_pos=None):
        """Draw controls screen"""
        screen = Screen("CONTROLS", self.font_large, self.font_medium,
                       self.font_small, self.font_tiny)
        screen.draw_background(surface)
        screen.draw_title(surface, 60)
        
        # Two columns
        controls_data = [
            # Left column - Movement
            ("MOVEMENT", [
                ("WASD / Arrows", "Move"),
                ("Space", "Jump"),
                ("Space (air)", "Double Jump"),
                ("Space (wall)", "Wall Jump"),
            ]),
            # Right column - Combat
            ("COMBAT", [
                ("Z", "Shoot"),
                ("X", "Melee Attack"),
                ("Stomp", "Jump on Enemy"),
            ]),
            # Left column continues - System
            ("SYSTEM", [
                ("P / ESC", "Pause"),
                ("F1", "Toggle Controls"),
                ("F5", "Quick Save"),
            ])
        ]
        
        # Draw in columns
        self._draw_controls_columns(surface, controls_data)
        
        screen.draw_hint(surface, "ESC to go back")
    
    def _draw_controls_columns(self, surface, controls_data):
        """Draw controls in two-column layout"""
        col_positions = [200, 700]
        y_start = 150
        
        col_index = 0
        section_y = y_start
        
        for section_title, controls in controls_data:
            x = col_positions[col_index]
            
            # Section title
            title_surf = self.font_medium.render(section_title, True, UI_HIGHLIGHT)
            surface.blit(title_surf, (x, section_y))
            
            # Controls
            for i, (key, action) in enumerate(controls):
                y = section_y + 40 + i * 35
                key_surf = self.font_small.render(key, True, CYAN)
                action_surf = self.font_tiny.render(action, True, UI_TEXT_DIM)
                surface.blit(key_surf, (x, y))
                surface.blit(action_surf, (x + 150, y + 3))
            
            # Next section position
            section_y += 40 + len(controls) * 35 + 40
            
            # Switch columns if needed
            if section_y > 500:
                col_index = 1
                section_y = y_start
    
    def draw_settings_screen(self, surface, mouse_pos=None):
        """Draw settings placeholder"""
        screen = Screen("SETTINGS", self.font_large, self.font_medium,
                       self.font_small, self.font_tiny)
        screen.draw_background(surface)
        screen.draw_title(surface, 100)
        
        msg = self.font_medium.render("Settings Coming Soon", True, UI_TEXT)
        surface.blit(msg, (SCREEN_WIDTH // 2 - msg.get_width() // 2, 250))
        
        msg2 = self.font_small.render("(Planned for Phase 3)", True, UI_TEXT_DIM)
        surface.blit(msg2, (SCREEN_WIDTH // 2 - msg2.get_width() // 2, 310))
        
        # Feature list
        features = [
            "• Sound Volume",
            "• Music Volume",
            "• Screen Resolution",
            "• Fullscreen Toggle",
            "• Key Rebinding"
        ]
        for i, feature in enumerate(features):
            feat_surf = self.font_tiny.render(feature, True, UI_TEXT_DIM)
            surface.blit(feat_surf, (SCREEN_WIDTH // 2 - 80, 370 + i * 25))
        
        screen.draw_hint(surface, "ESC to go back")
    
    def draw_credits_screen(self, surface, mouse_pos=None):
        """Draw credits screen"""
        screen = Screen("CREDITS", self.font_large, self.font_medium,
                       self.font_small, self.font_tiny)
        screen.draw_background(surface)
        screen.draw_title(surface, 80)
        
        credits = [
            ("Created by", ""),
            ("Your Name Here", ""),
            ("", ""),
            ("Programming", ""),
            ("Game Design & Development", ""),
            ("", ""),
            ("Special Thanks", ""),
            ("Claude (Anthropic)", ""),
            ("", ""),
            ("Inspired by", ""),
            ("Super Mario Bros", "Metroid"),
            ("Celeste", "Shovel Knight"),
            ("", ""),
            ("Built with", ""),
            ("Python & Pygame", ""),
        ]
        
        y = 150
        for line1, line2 in credits:
            if line1:
                text1 = self.font_small.render(
                    line1, True, UI_TEXT if not line2 else UI_TEXT_DIM
                )
                surface.blit(text1, (SCREEN_WIDTH // 2 - text1.get_width() // 2, y))
            if line2:
                y += 25
                text2 = self.font_small.render(
                    line2, True, UI_TEXT if not line1 else UI_TEXT_DIM
                )
                surface.blit(text2, (SCREEN_WIDTH // 2 - text2.get_width() // 2, y))
            y += 30
        
        version = self.font_tiny.render("Version 0.4 Alpha", True, UI_TEXT_DIM)
        surface.blit(version, (SCREEN_WIDTH // 2 - version.get_width() // 2, 
                              SCREEN_HEIGHT - 100))
        
        screen.draw_hint(surface, "ESC to go back")
    
    # ========================================================================
    # GAME OVER / VICTORY
    # ========================================================================
    
    def draw_game_over(self, surface, score):
        """Draw game over screen"""
        surface.fill(BLACK)
        
        text = self.font_large.render("GAME OVER", True, (220, 80, 80))
        surface.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 
                           SCREEN_HEIGHT // 2 - 100))
        
        score_text = self.font_medium.render(f"Final Score: {score}", True, WHITE)
        surface.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2,
                                 SCREEN_HEIGHT // 2))
        
        inst = self.font_tiny.render("ENTER to return to menu", True, UI_TEXT_DIM)
        surface.blit(inst, (SCREEN_WIDTH // 2 - inst.get_width() // 2,
                           SCREEN_HEIGHT // 2 + 100))
    
    def draw_victory(self, surface, score):
        """Draw victory screen"""
        surface.fill(BLACK)
        
        text = self.font_large.render("VICTORY!", True, (100, 255, 100))
        surface.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2,
                           SCREEN_HEIGHT // 2 - 100))
        
        score_text = self.font_medium.render(f"Final Score: {score}", True, WHITE)
        surface.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2,
                                 SCREEN_HEIGHT // 2))
        
        inst = self.font_tiny.render("ENTER to return to menu", True, UI_TEXT_DIM)
        surface.blit(inst, (SCREEN_WIDTH // 2 - inst.get_width() // 2,
                           SCREEN_HEIGHT // 2 + 100))
    
    # ========================================================================
    # UTILITY METHODS
    # ========================================================================
    
    def check_button_click(self, button_group, mouse_pos, mouse_pressed):
        """Check button clicks for a button group"""
        return button_group.check_click(mouse_pos, mouse_pressed)
