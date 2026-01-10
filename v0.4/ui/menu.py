"""
Menu screens - Complete version with Controls and Level Map
"""

import pygame

from config.settings import (BLACK, CHARACTER_COLORS, CYAN, GRAY,
                             SCREEN_HEIGHT, SCREEN_WIDTH, UI_BG, UI_BORDER,
                             UI_HIGHLIGHT, UI_TEXT, UI_TEXT_DIM, WHITE, YELLOW)


class Menu:
    """Handles all menu screens"""

    def __init__(self, font_large, font_medium, font_small):
        """Initialize with cleaner, smaller fonts"""
        self.font_large = pygame.font.Font(None, 52)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 22)
        self.font_tiny = pygame.font.Font(None, 18)

        # Button definitions for mouse handling
        self.main_buttons = self._create_main_buttons()
        self.pause_buttons = self._create_pause_buttons()
        self.char_buttons = self._create_char_buttons()
        self.options_buttons = self._create_options_buttons()

    def _create_main_buttons(self):
        """Create button rectangles for main menu (NOW 5 buttons)"""
        buttons = []
        button_width = 280
        button_height = 40
        button_x = SCREEN_WIDTH // 2 - button_width // 2
        start_y = 240
        for i in range(5):  # New Game, Continue, Level Map, Options, Quit
            y = start_y + i * 55
            buttons.append(pygame.Rect(button_x, y - 8, button_width, button_height))
        return buttons

    def _create_pause_buttons(self):
        """Create button rectangles for pause menu (NOW 3 BUTTONS)"""
        buttons = []
        button_width = 300
        button_height = 40
        button_x = SCREEN_WIDTH // 2 - button_width // 2
        start_y = SCREEN_HEIGHT // 2 - 50
        for i in range(3):  # Resume, Return to Menu, Logout
            y = start_y + i * 55
            buttons.append(pygame.Rect(button_x, y - 8, button_width, button_height))
        return buttons

    def _create_char_buttons(self):
        """Create button rectangles for character selection"""
        buttons = []
        char_y = 280
        for i in range(4):
            x = SCREEN_WIDTH // 2 - 250 + i * 120
            buttons.append(pygame.Rect(x, char_y, 56, 96))
        return buttons

    def _create_options_buttons(self):
        """Create button rectangles for options menu"""
        buttons = []
        button_width = 280
        button_height = 40
        button_x = SCREEN_WIDTH // 2 - button_width // 2
        start_y = 220
        for i in range(4):  # Controls, Settings, Credits, Back
            y = start_y + i * 55
            buttons.append(pygame.Rect(button_x, y - 8, button_width, button_height))
        return buttons

    def check_button_click(self, buttons, mouse_pos, mouse_pressed):
        """Check if any button was clicked"""
        if not mouse_pressed[0]:  # Left click
            return -1

        for i, button in enumerate(buttons):
            if button.collidepoint(mouse_pos):
                return i
        return -1

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

    def draw_main_menu(self, surface, current_profile, selection, mouse_pos=None):
        """
        Draw main menu (after profile selected)
        Shows current profile name at top
        Options: New Game, Continue, Level Map, Options, Quit
        """
        surface.fill(BLACK)

        # Show current profile
        if current_profile:
            profile_text = self.font_small.render(
                f"Profile: {current_profile.name}", True, UI_TEXT_DIM
            )
            surface.blit(profile_text, (20, 20))

        # Title
        title = self.font_large.render("RETRO PLATFORMER", True, UI_HIGHLIGHT)
        surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))

        # Menu options
        options = ["New Game", "Continue", "Level Map", "Options", "Quit"]
        for i, option in enumerate(options):
            y = 240 + i * 55
            is_selected = i == selection

            # Check mouse hover
            if mouse_pos:
                button = self.main_buttons[i]
                if button.collidepoint(mouse_pos):
                    is_selected = True

            self._draw_button(surface, option, y, is_selected)

        # Hint
        hint = self.font_tiny.render(
            "↑↓ Navigate   ENTER Select   ESC Logout", True, UI_TEXT_DIM
        )
        surface.blit(
            hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, SCREEN_HEIGHT - 60)
        )

    def draw_options_menu(self, surface, selection, mouse_pos=None):
        """Draw options menu"""
        surface.fill(BLACK)

        # Title
        title = self.font_large.render("OPTIONS", True, UI_HIGHLIGHT)
        surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))

        # Options
        options = ["Controls", "Settings", "Credits", "Back to Menu"]
        for i, option in enumerate(options):
            y = 220 + i * 55
            is_selected = i == selection

            # Check mouse hover
            if mouse_pos:
                button = self.options_buttons[i]
                if button.collidepoint(mouse_pos):
                    is_selected = True

            self._draw_button(surface, option, y, is_selected)

        # Hint
        hint = self.font_tiny.render(
            "↑↓ Navigate   ENTER Select   ESC Back", True, UI_TEXT_DIM
        )
        surface.blit(
            hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, SCREEN_HEIGHT - 60)
        )

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
        surface.blit(
            hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, SCREEN_HEIGHT - 40)
        )

    def draw_settings_screen(self, surface, mouse_pos=None):
        """Draw settings screen - PLACEHOLDER for Phase 3"""
        surface.fill(BLACK)

        # Title
        title = self.font_large.render("SETTINGS", True, UI_HIGHLIGHT)
        surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))

        # Placeholder text
        msg1 = self.font_medium.render("Settings Coming Soon", True, UI_TEXT)
        surface.blit(msg1, (SCREEN_WIDTH // 2 - msg1.get_width() // 2, 250))

        msg2 = self.font_small.render("(Planned for Phase 3)", True, UI_TEXT_DIM)
        surface.blit(msg2, (SCREEN_WIDTH // 2 - msg2.get_width() // 2, 310))

        # Future features list
        features = [
            "• Sound Volume",
            "• Music Volume",
            "• Screen Resolution",
            "• Fullscreen Toggle",
            "• Key Rebinding",
        ]
        y_start = 370
        for i, feature in enumerate(features):
            feature_text = self.font_tiny.render(feature, True, UI_TEXT_DIM)
            surface.blit(feature_text, (SCREEN_WIDTH // 2 - 80, y_start + i * 25))

        # Back instruction
        back_text = self.font_tiny.render("ESC to go back", True, UI_HIGHLIGHT)
        surface.blit(
            back_text,
            (SCREEN_WIDTH // 2 - back_text.get_width() // 2, SCREEN_HEIGHT - 60),
        )

    def draw_credits_screen(self, surface, mouse_pos=None):
        """Draw credits screen - PLACEHOLDER for Phase 3"""
        surface.fill(BLACK)

        # Title
        title = self.font_large.render("CREDITS", True, UI_HIGHLIGHT)
        surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 80))

        # Credits
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

        # Version
        version_text = self.font_tiny.render("Version 0.4 Alpha", True, UI_TEXT_DIM)
        surface.blit(
            version_text,
            (SCREEN_WIDTH // 2 - version_text.get_width() // 2, SCREEN_HEIGHT - 100),
        )

        # Back instruction
        back_text = self.font_tiny.render("ESC to go back", True, UI_HIGHLIGHT)
        surface.blit(
            back_text,
            (SCREEN_WIDTH // 2 - back_text.get_width() // 2, SCREEN_HEIGHT - 60),
        )

    def draw_level_map_screen(self, surface, current_profile, mouse_pos=None):
        """
        Draw level map/selection screen
        Shows all levels with locked/unlocked status
        """
        surface.fill(BLACK)

        # Title
        title = self.font_large.render("LEVEL MAP", True, UI_HIGHLIGHT)
        surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 60))

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

        # Determine unlocked count
        unlocked_count = 0
        if current_profile:
            # current_profile might be a tuple from mouse_pos parameter confusion
            # Fix by checking if it's actually a profile object
            if hasattr(current_profile, 'levels_completed'):
                unlocked_count = current_profile.levels_completed
            else:
                unlocked_count = 0

        # Subtitle
        subtitle = self.font_small.render(
            f"Unlocked: {unlocked_count} / {len(level_names)}", True, UI_TEXT
        )
        surface.blit(subtitle, (SCREEN_WIDTH // 2 - subtitle.get_width() // 2, 130))

        # Draw level list
        y_start = 200
        for i, level_name in enumerate(level_names):
            y = y_start + i * 50
            
            # Check if unlocked
            is_unlocked = i < unlocked_count
            
            # Choose colors
            if is_unlocked:
                name_color = UI_HIGHLIGHT
                icon = "✓"
                icon_color = (100, 255, 100)
            else:
                name_color = UI_TEXT_DIM
                icon = "🔒"
                icon_color = (150, 150, 150)
            
            # Draw icon
            icon_text = self.font_small.render(icon, True, icon_color)
            surface.blit(icon_text, (200, y))
            
            # Draw level name
            name_text = self.font_small.render(level_name, True, name_color)
            surface.blit(name_text, (250, y))

        # Instructions
        if unlocked_count > 0:
            inst1 = self.font_tiny.render(
                "Level selection coming in Phase 3", True, UI_TEXT_DIM
            )
            surface.blit(inst1, (SCREEN_WIDTH // 2 - inst1.get_width() // 2, SCREEN_HEIGHT - 100))
        else:
            inst1 = self.font_tiny.render(
                "Complete levels to unlock them here", True, UI_TEXT_DIM
            )
            surface.blit(inst1, (SCREEN_WIDTH // 2 - inst1.get_width() // 2, SCREEN_HEIGHT - 100))

        # Back instruction
        inst2 = self.font_tiny.render("ESC to go back", True, UI_HIGHLIGHT)
        surface.blit(inst2, (SCREEN_WIDTH // 2 - inst2.get_width() // 2, SCREEN_HEIGHT - 60))

    def draw_difficulty_select(self, surface, selection, mouse_pos=None):
        """Draw difficulty selection screen"""
        surface.fill(BLACK)

        # Title
        title = self.font_large.render("SELECT DIFFICULTY", True, UI_HIGHLIGHT)
        surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 80))

        # Subtitle
        subtitle = self.font_small.render(
            "Choose your challenge level", True, UI_TEXT_DIM
        )
        surface.blit(subtitle, (SCREEN_WIDTH // 2 - subtitle.get_width() // 2, 140))

        # Difficulty options
        difficulties = [
            ("EASY", "5 Lives • More Resources • 2x Time", (100, 200, 100)),
            ("NORMAL", "3 Lives • Balanced Challenge • Standard", WHITE),
            ("HARD", "1 Life • Extreme Challenge • 2x Score", (220, 80, 80)),
        ]

        y_start = 220
        for i, (name, desc, color) in enumerate(difficulties):
            y = y_start + i * 120
            is_selected = i == selection

            # Button box
            box_width = 500
            box_height = 100
            box_x = SCREEN_WIDTH // 2 - box_width // 2
            box_rect = pygame.Rect(box_x, y, box_width, box_height)

            # Check mouse hover
            if mouse_pos and box_rect.collidepoint(mouse_pos):
                is_selected = True

            if is_selected:
                pygame.draw.rect(surface, UI_HIGHLIGHT, box_rect, border_radius=8)
                pygame.draw.rect(surface, color, box_rect, 3, border_radius=8)
                name_color = BLACK
                desc_color = (40, 40, 40)
            else:
                pygame.draw.rect(surface, UI_BG, box_rect, border_radius=8)
                pygame.draw.rect(surface, color, box_rect, 2, border_radius=8)
                name_color = color
                desc_color = UI_TEXT_DIM

            # Difficulty name
            name_text = self.font_medium.render(name, True, name_color)
            name_x = box_x + box_width // 2 - name_text.get_width() // 2
            surface.blit(name_text, (name_x, y + 25))

            # Description
            desc_text = self.font_tiny.render(desc, True, desc_color)
            desc_x = box_x + box_width // 2 - desc_text.get_width() // 2
            surface.blit(desc_text, (desc_x, y + 60))

        # Instructions
        hint = self.font_tiny.render(
            "↑↓ Select   ENTER Confirm   ESC Back   Mouse Click", True, UI_TEXT_DIM
        )
        surface.blit(
            hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, SCREEN_HEIGHT - 40)
        )

    def draw_char_select(self, surface, player_name, char_selection, mouse_pos=None):
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

            rect = pygame.Rect(x, char_y, 56, 96)
            is_selected = i == char_selection

            # Check mouse hover
            if mouse_pos:
                button = self.char_buttons[i]
                if button.collidepoint(mouse_pos):
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
        inst = self.font_tiny.render(
            "Type name   ←→ Select   ENTER Start   Mouse Click", True, UI_TEXT_DIM
        )
        surface.blit(
            inst, (SCREEN_WIDTH // 2 - inst.get_width() // 2, SCREEN_HEIGHT - 50)
        )

    def draw_pause_menu(self, surface, selection, mouse_pos=None):
        """Draw pause menu overlay"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        surface.blit(overlay, (0, 0))

        # Paused text
        text = self.font_large.render("PAUSED", True, YELLOW)
        surface.blit(
            text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 140)
        )

        # Options (NOW 3 OPTIONS)
        options = ["Resume", "Save & Return to Menu", "Save & Logout"]
        for i, option in enumerate(options):
            y = SCREEN_HEIGHT // 2 - 50 + i * 55
            is_selected = i == selection

            # Check mouse hover
            if mouse_pos:
                button = self.pause_buttons[i]
                if button.collidepoint(mouse_pos):
                    is_selected = True

            self._draw_button(surface, option, y, is_selected)

        hint = self.font_tiny.render("↑↓ Navigate   ENTER Select", True, UI_TEXT_DIM)
        surface.blit(
            hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, SCREEN_HEIGHT // 2 + 140)
        )

    def draw_profile_select(self, surface, profiles, selection, mouse_pos=None):
        """
        Draw profile selection screen - FIRST SCREEN
        Options: New Profile (N) or Load Profile (L/Enter)
        """
        surface.fill(BLACK)

        # Title
        title = self.font_large.render("SELECT PROFILE", True, UI_HIGHLIGHT)
        surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 60))

        # Instructions
        if not profiles:
            msg = self.font_medium.render("No profiles found", True, UI_TEXT)
            surface.blit(msg, (SCREEN_WIDTH // 2 - msg.get_width() // 2, 200))

            inst1 = self.font_small.render(
                "Press N to create new profile", True, UI_HIGHLIGHT
            )
            surface.blit(inst1, (SCREEN_WIDTH // 2 - inst1.get_width() // 2, 280))
        else:
            # Show profile list
            y_start = 160
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

                # Draw box
                box_color = UI_HIGHLIGHT if is_selected else UI_BORDER
                pygame.draw.rect(surface, box_color, box_rect, 2)
                if is_selected:
                    fill_rect = pygame.Rect(
                        box_x + 2, y + 2, box_width - 4, box_height - 4
                    )
                    fill_surface = pygame.Surface((box_width - 4, box_height - 4))
                    fill_surface.set_alpha(30)
                    fill_surface.fill(UI_HIGHLIGHT)
                    surface.blit(fill_surface, (box_x + 2, y + 2))

                # Profile name
                name_text = self.font_medium.render(profile.name, True, UI_TEXT)
                surface.blit(name_text, (box_x + 20, y + 8))

                # Stats
                stats_text = self.font_tiny.render(
                    f"Levels: {profile.levels_completed}  Score: {profile.total_score}  Coins: {profile.coins_collected}",
                    True,
                    UI_TEXT_DIM,
                )
                surface.blit(stats_text, (box_x + 20, y + 35))

            # Instructions at bottom
            inst1 = self.font_tiny.render(
                "↑↓ Navigate   ENTER/L Load Profile   D Delete   N New Profile",
                True,
                UI_TEXT_DIM,
            )
            surface.blit(
                inst1, (SCREEN_WIDTH // 2 - inst1.get_width() // 2, SCREEN_HEIGHT - 80)
            )

        # New Profile button always visible
        button_y = SCREEN_HEIGHT - 120 if profiles else 350
        self._draw_button(surface, "New Profile (N)", button_y, False)

    def draw_game_over(self, surface, score):
        """Draw game over screen"""
        surface.fill(BLACK)

        text = self.font_large.render("GAME OVER", True, (220, 80, 80))
        surface.blit(
            text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 100)
        )

        score_text = self.font_medium.render(f"Final Score: {score}", True, WHITE)
        surface.blit(
            score_text,
            (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2),
        )

        inst = self.font_tiny.render("ENTER to return to menu", True, UI_TEXT_DIM)
        surface.blit(
            inst, (SCREEN_WIDTH // 2 - inst.get_width() // 2, SCREEN_HEIGHT // 2 + 100)
        )

    def draw_victory(self, surface, score):
        """Draw victory screen"""
        surface.fill(BLACK)

        text = self.font_large.render("VICTORY!", True, YELLOW)
        surface.blit(
            text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 100)
        )

        score_text = self.font_medium.render(f"Final Score: {score}", True, WHITE)
        surface.blit(
            score_text,
            (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2),
        )

        inst = self.font_tiny.render("ENTER to return to menu", True, UI_TEXT_DIM)
        surface.blit(
            inst, (SCREEN_WIDTH // 2 - inst.get_width() // 2, SCREEN_HEIGHT // 2 + 100)
        )
