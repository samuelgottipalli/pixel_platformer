"""
Refactored Menu System Using Modular Components
Cleaner, more maintainable menu code with reusable components
"""

import pygame
from config.settings import (
    BLACK,
    CHARACTER_COLORS,
    CYAN,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    UI_BG,
    UI_BORDER,
    UI_HIGHLIGHT,
    UI_TEXT,
    UI_TEXT_DIM,
    WHITE,
    YELLOW,
)
from ui.components import IconButton, LayoutHelper, Screen
from ui.icons import Icon


class Menu:
    """Manages all menu screens using modular components"""

    def __init__(self, font_large, font_medium, font_small):
        # Fonts
        self.font_large = pygame.font.Font(None, 52)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 22)
        self.font_tiny = pygame.font.Font(None, 18)

        # Button groups for each screen
        self.main_buttons = self._create_main_buttons()
        self.pause_buttons = self._create_pause_buttons()
        self.char_buttons = self._create_char_buttons()
        self.options_buttons = self._create_options_buttons()

        # # Initialize button groups
        # self._init_main_menu()
        # self._init_options_menu()
        # self._init_pause_menu()
        # self._init_char_select()

    # ========================================================================
    # BUTTON GROUP INITIALIZATION
    # ========================================================================

    def _create_main_buttons(self):
        """Create button rectangles for main menu"""
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
        """Create button rectangles for pause menu"""
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

    # ========================================================================
    # MAIN MENU
    # ========================================================================

    def draw_main_menu(self, surface, current_profile, selection, mouse_pos=None):
        """Draw main menu using components"""
        surface.fill(BLACK)

        if current_profile:
            profile_text = self.font_small.render(
                f"Profile: {current_profile.name}", True, UI_TEXT_DIM
            )
            surface.blit(profile_text, (20, 20))

        title = self.font_large.render("RETRO PLATFORMER", True, UI_HIGHLIGHT)
        surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))

        options = ["New Game", "Continue", "Level Map", "Options", "Quit"]
        for i, option in enumerate(options):
            y = 240 + i * 55
            is_selected = i == selection
            if mouse_pos:
                button = self.main_buttons[i]
                if button.collidepoint(mouse_pos):
                    is_selected = True
            self._draw_button(surface, option, y, is_selected)

        hint = self.font_tiny.render(
            "UP/DOWN Navigate   ENTER Select   ESC Logout", True, UI_TEXT_DIM
        )
        surface.blit(
            hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, SCREEN_HEIGHT - 60)
        )

        return None

    # ========================================================================
    # PROFILE SELECT
    # ========================================================================

    def draw_profile_select(self, surface, profiles, selection, mouse_pos=None):
        """Draw profile selection screen"""
        surface.fill(BLACK)

        title = self.font_large.render("SELECT PROFILE", True, UI_HIGHLIGHT)
        surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 60))

        if not profiles:
            msg = self.font_medium.render("No profiles found", True, UI_TEXT)
            surface.blit(msg, (SCREEN_WIDTH // 2 - msg.get_width() // 2, 200))

            inst1 = self.font_small.render(
                "Press N to create new profile", True, UI_HIGHLIGHT
            )
            surface.blit(inst1, (SCREEN_WIDTH // 2 - inst1.get_width() // 2, 280))
        else:
            y_start = 160
            for i, profile in enumerate(profiles):
                y = y_start + i * 70
                is_selected = i == selection
                box_width = 500
                box_height = 60
                box_x = SCREEN_WIDTH // 2 - box_width // 2
                box_rect = pygame.Rect(box_x, y, box_width, box_height)

                if mouse_pos and box_rect.collidepoint(mouse_pos):
                    is_selected = True

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

                name_text = self.font_medium.render(profile.name, True, UI_TEXT)
                surface.blit(name_text, (box_x + 20, y + 8))

                stats_text = self.font_tiny.render(
                    f"Levels: {profile.levels_completed}  Score: {profile.total_score}  Coins: {profile.coins_collected}",
                    True,
                    UI_TEXT_DIM,
                )
                surface.blit(stats_text, (box_x + 20, y + 35))

            inst1 = self.font_tiny.render(
                "UP/DOWN Navigate   ENTER/L Load   D Delete   N New", True, UI_TEXT_DIM
            )
            surface.blit(
                inst1, (SCREEN_WIDTH // 2 - inst1.get_width() // 2, SCREEN_HEIGHT - 80)
            )

        button_y = SCREEN_HEIGHT - 120 if profiles else 350
        self._draw_button(surface, "New Profile (N)", button_y, False)

        return None

    # ========================================================================
    # DIFFICULTY SELECT
    # ========================================================================

    def draw_difficulty_select(self, surface, selection, mouse_pos=None):
        """Draw difficulty selection"""
        screen = Screen(
            "SELECT DIFFICULTY",
            self.font_large,
            self.font_medium,
            self.font_small,
            self.font_tiny,
            show_back=True,
            show_options=True,
        )

        screen.draw_background(surface)
        screen.update_button_hover(mouse_pos)
        screen.draw_title(surface, 80)

        subtitle = self.font_small.render(
            "Choose your challenge level", True, UI_TEXT_DIM
        )
        surface.blit(subtitle, (SCREEN_WIDTH // 2 - subtitle.get_width() // 2, 140))

        difficulties = [
            ("EASY", "5 Lives - More Resources - 2x Time", (100, 200, 100)),
            ("NORMAL", "3 Lives - Balanced Challenge - Standard", WHITE),
            ("HARD", "1 Life - Extreme Challenge - 2x Score", (220, 80, 80)),
        ]

        y_start = 220
        for i, (name, desc, color) in enumerate(difficulties):
            y = y_start + i * 120
            is_selected = i == selection
            box_width = 500
            box_height = 100
            box_x = SCREEN_WIDTH // 2 - box_width // 2
            box_rect = pygame.Rect(box_x, y, box_width, box_height)

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

            name_text = self.font_medium.render(name, True, name_color)
            name_x = box_x + box_width // 2 - name_text.get_width() // 2
            surface.blit(name_text, (name_x, y + 25))

            desc_text = self.font_tiny.render(desc, True, desc_color)
            desc_x = box_x + box_width // 2 - desc_text.get_width() // 2
            surface.blit(desc_text, (desc_x, y + 60))

        hint = self.font_tiny.render(
            "UP/DOWN Select   ENTER Confirm   ESC/Back Button", True, UI_TEXT_DIM
        )
        surface.blit(
            hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, SCREEN_HEIGHT - 40)
        )

        screen.draw_buttons(surface)
        return screen

    # ========================================================================
    # CHARACTER SELECT
    # ========================================================================

    def draw_char_select(self, surface, player_name, char_selection, mouse_pos=None):
        """Draw character selection"""
        screen = Screen(
            "CHARACTER SELECT",
            self.font_large,
            self.font_medium,
            self.font_small,
            self.font_tiny,
            show_back=True,
            show_options=True,
        )

        screen.draw_background(surface)
        screen.update_button_hover(mouse_pos)
        screen.draw_title(surface, 80)

        name_label = self.font_small.render("Enter Name:", True, UI_TEXT_DIM)
        surface.blit(name_label, (SCREEN_WIDTH // 2 - name_label.get_width() // 2, 160))

        name_text = self.font_medium.render(f"{player_name}_", True, WHITE)
        surface.blit(name_text, (SCREEN_WIDTH // 2 - name_text.get_width() // 2, 190))

        char_y = 280
        for i in range(4):
            x = SCREEN_WIDTH // 2 - 250 + i * 120
            rect = pygame.Rect(x, char_y, 56, 96)
            is_selected = i == char_selection

            if mouse_pos:
                button = self.char_buttons[i]
                if button.collidepoint(mouse_pos):
                    is_selected = True

            pygame.draw.rect(surface, CHARACTER_COLORS[i], rect, border_radius=5)

            if is_selected:
                pygame.draw.rect(surface, YELLOW, rect, 3, border_radius=5)
            else:
                pygame.draw.rect(surface, UI_BORDER, rect, 1, border_radius=5)

            pygame.draw.circle(surface, WHITE, (x + 20, char_y + 30), 6)
            pygame.draw.circle(surface, BLACK, (x + 22, char_y + 30), 3)

        inst = self.font_tiny.render(
            "Type name   LEFT/RIGHT Select   ENTER Start", True, UI_TEXT_DIM
        )
        surface.blit(
            inst, (SCREEN_WIDTH // 2 - inst.get_width() // 2, SCREEN_HEIGHT - 50)
        )

        screen.draw_buttons(surface)
        return screen

    # ========================================================================
    # OPTIONS MENU
    # ========================================================================

    def draw_options_menu(self, surface, selection, mouse_pos=None):
        """Draw options menu"""
        screen = Screen(
            "OPTIONS",
            self.font_large,
            self.font_medium,
            self.font_small,
            self.font_tiny,
            show_back=True,
            show_options=False,
        )

        screen.draw_background(surface)
        screen.update_button_hover(mouse_pos)
        screen.draw_title(surface, 100)

        options = ["Controls", "Settings", "Credits", "Back to Menu"]
        for i, option in enumerate(options):
            y = 220 + i * 55
            is_selected = i == selection
            if mouse_pos:
                button = self.options_buttons[i]
                if button.collidepoint(mouse_pos):
                    is_selected = True
            self._draw_button(surface, option, y, is_selected)

        hint = self.font_tiny.render(
            "UP/DOWN Navigate   ENTER Select   ESC/Back Button", True, UI_TEXT_DIM
        )
        surface.blit(
            hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, SCREEN_HEIGHT - 60)
        )

        screen.draw_buttons(surface)
        return screen

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

        # Options button top-right
        options_btn = IconButton(
            SCREEN_WIDTH - 140, 20, 120, 40, Icon.SETTINGS, "Options", self.font_tiny
        )
        options_btn.check_hover(mouse_pos)
        options_btn.draw(surface)

        text = self.font_large.render("PAUSED", True, YELLOW)
        surface.blit(
            text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 140)
        )

        options = ["Resume", "Save & Return to Menu", "Save & Logout"]
        for i, option in enumerate(options):
            y = SCREEN_HEIGHT // 2 - 50 + i * 55
            is_selected = i == selection
            if mouse_pos:
                button = self.pause_buttons[i]
                if button.collidepoint(mouse_pos):
                    is_selected = True
            self._draw_button(surface, option, y, is_selected)

        hint = self.font_tiny.render(
            "UP/DOWN Navigate   ENTER Select", True, UI_TEXT_DIM
        )
        surface.blit(
            hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, SCREEN_HEIGHT // 2 + 140)
        )

        # Return options button for click detection
        return options_btn

    # ========================================================================
    # LEVEL MAP
    # ========================================================================

    def draw_level_map_screen(self, surface, current_profile, mouse_pos=None):
        """Draw level map with all levels"""
        screen = Screen(
            "LEVEL MAP",
            self.font_large,
            self.font_medium,
            self.font_small,
            self.font_tiny,
            show_back=True,
            show_options=True,
        )

        screen.draw_background(surface)
        screen.update_button_hover(mouse_pos)
        screen.draw_title(surface, 60)

        level_names = [
            "Tutorial: Training Facility",
            "Level 1: The Awakening",
            "Level 2: Rising Conflict",
            "Level 3: The Ascent",
            "Level 4: Deep Dive",
            "Level 5: Convergence",
            "Level 6: Guardian's Lair (BOSS)",
        ]

        unlocked_count = 0
        if current_profile and hasattr(current_profile, "levels_completed"):
            unlocked_count = current_profile.levels_completed

        subtitle = self.font_small.render(
            f"Unlocked: {unlocked_count} / {len(level_names)}", True, UI_TEXT
        )
        surface.blit(subtitle, (SCREEN_WIDTH // 2 - subtitle.get_width() // 2, 130))

        y_positions = LayoutHelper.create_vertical_layout(200, len(level_names), 50)

        for i, (level_name, y) in enumerate(zip(level_names, y_positions)):
            is_unlocked = i < unlocked_count

            if is_unlocked:
                icon_type = Icon.CHECKMARK
                icon_color = (100, 255, 100)
                name_color = UI_HIGHLIGHT
            else:
                icon_type = Icon.LOCK
                icon_color = (150, 150, 150)
                name_color = UI_TEXT_DIM

            Icon.draw(surface, icon_type, 200, y, 20, icon_color)
            name_surf = self.font_small.render(level_name, True, name_color)
            surface.blit(name_surf, (250, y))

        if unlocked_count > 0:
            inst = self.font_tiny.render(
                "Level selection coming in Phase 3", True, UI_TEXT_DIM
            )
        else:
            inst = self.font_tiny.render(
                "Complete levels to unlock them here", True, UI_TEXT_DIM
            )
        surface.blit(
            inst, (SCREEN_WIDTH // 2 - inst.get_width() // 2, SCREEN_HEIGHT - 100)
        )

        hint = self.font_tiny.render("ESC/Back Button to return", True, UI_TEXT_DIM)
        surface.blit(
            hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, SCREEN_HEIGHT - 60)
        )

        screen.draw_buttons(surface)
        return screen

    # ========================================================================
    # PLACEHOLDER SCREENS
    # ========================================================================

    def draw_controls_screen(self, surface, mouse_pos=None):
        """Draw controls screen"""
        screen = Screen(
            "CONTROLS",
            self.font_large,
            self.font_medium,
            self.font_small,
            self.font_tiny,
            show_back=True,
            show_options=False,
        )

        screen.draw_background(surface)
        screen.update_button_hover(mouse_pos)
        screen.draw_title(surface, 60)

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
            ("Stomp", "Jump on Enemy"),
        ]

        for i, (key, action) in enumerate(controls_right):
            y = section_y + 40 + i * line_height
            key_text = self.font_small.render(key, True, CYAN)
            action_text = self.font_tiny.render(action, True, UI_TEXT_DIM)
            surface.blit(key_text, (right_x, y))
            surface.blit(action_text, (right_x + 150, y + 3))

        # System controls
        section_y = y_start + 180
        section_title = self.font_medium.render("SYSTEM", True, UI_HIGHLIGHT)
        surface.blit(section_title, (left_x, section_y))

        controls_system = [
            ("P / ESC", "Pause"),
            ("F1", "Toggle Controls"),
            ("F5", "Quick Save"),
        ]

        for i, (key, action) in enumerate(controls_system):
            y = section_y + 40 + i * line_height
            key_text = self.font_small.render(key, True, CYAN)
            action_text = self.font_tiny.render(action, True, UI_TEXT_DIM)
            surface.blit(key_text, (left_x, y))
            surface.blit(action_text, (left_x + 150, y + 3))

        hint = self.font_tiny.render("ESC/Back Button to return", True, UI_TEXT_DIM)
        surface.blit(
            hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, SCREEN_HEIGHT - 50)
        )

        screen.draw_buttons(surface)
        return screen

    def draw_settings_screen(self, surface, mouse_pos=None):
        """Draw settings placeholder"""
        screen = Screen(
            "SETTINGS",
            self.font_large,
            self.font_medium,
            self.font_small,
            self.font_tiny,
            show_back=True,
            show_options=False,
        )

        screen.draw_background(surface)
        screen.update_button_hover(mouse_pos)
        screen.draw_title(surface, 100)

        msg = self.font_medium.render("Settings Coming Soon", True, UI_TEXT)
        surface.blit(msg, (SCREEN_WIDTH // 2 - msg.get_width() // 2, 250))

        msg2 = self.font_small.render("(Planned for Phase 3)", True, UI_TEXT_DIM)
        surface.blit(msg2, (SCREEN_WIDTH // 2 - msg2.get_width() // 2, 310))

        features = [
            "Sound Volume",
            "Music Volume",
            "Screen Resolution",
            "Fullscreen Toggle",
            "Key Rebinding",
        ]
        for i, feature in enumerate(features):
            feat_surf = self.font_tiny.render(f"- {feature}", True, UI_TEXT_DIM)
            surface.blit(feat_surf, (SCREEN_WIDTH // 2 - 80, 370 + i * 25))

        hint = self.font_tiny.render("ESC/Back Button to return", True, UI_TEXT_DIM)
        surface.blit(
            hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, SCREEN_HEIGHT - 60)
        )

        screen.draw_buttons(surface)
        return screen

    def draw_credits_screen(self, surface, mouse_pos=None):
        """Draw credits screen"""
        screen = Screen(
            "CREDITS",
            self.font_large,
            self.font_medium,
            self.font_small,
            self.font_tiny,
            show_back=True,
            show_options=False,
        )

        screen.draw_background(surface)
        screen.update_button_hover(mouse_pos)
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
        surface.blit(
            version, (SCREEN_WIDTH // 2 - version.get_width() // 2, SCREEN_HEIGHT - 100)
        )

        hint = self.font_tiny.render("ESC/Back Button to return", True, UI_TEXT_DIM)
        surface.blit(
            hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, SCREEN_HEIGHT - 60)
        )

        screen.draw_buttons(surface)
        return screen

    # ========================================================================
    # GAME OVER / VICTORY
    # ========================================================================

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

        return None

    def draw_victory(self, surface, score):
        """Draw victory screen"""
        surface.fill(BLACK)
        text = self.font_large.render("VICTORY!", True, (100, 255, 100))
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

        return None

    # ========================================================================
    # UTILITY METHODS
    # ========================================================================

    def check_button_click(self, buttons, mouse_pos, mouse_pressed):
        """Check if any button was clicked"""
        if not mouse_pressed[0]:
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
        button_rect = pygame.Rect(x, y - 8, button_width, button_height)

        if is_selected:
            pygame.draw.rect(surface, UI_HIGHLIGHT, button_rect, border_radius=5)
            pygame.draw.rect(surface, WHITE, button_rect, 2, border_radius=5)
            text_color = BLACK
        else:
            pygame.draw.rect(surface, UI_BG, button_rect, border_radius=5)
            pygame.draw.rect(surface, UI_BORDER, button_rect, 1, border_radius=5)
            text_color = UI_TEXT

        text_surf = self.font_medium.render(text, True, text_color)
        text_x = x + button_width // 2 - text_surf.get_width() // 2
        text_y = y
        surface.blit(text_surf, (text_x, text_y))
