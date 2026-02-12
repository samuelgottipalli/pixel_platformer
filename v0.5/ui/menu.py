"""
Refactored Menu System Using Modular Components
Cleaner, more maintainable menu code with reusable components
"""

import pygame
from config.layout_manager import get_screen_size, get_ui_element, get_font_size
from config.settings import (
    BLACK,
    CHARACTER_COLORS,
    CYAN,
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
        from config.layout_manager import get_font_size

        # Get font sizes from layout (with fallbacks)
        large_size = get_font_size('large') or 52
        medium_size = get_font_size('medium') or 32
        small_size = get_font_size('small') or 22
        tiny_size = get_font_size('tiny') or 18

        self.font_large = pygame.font.Font(None, large_size)
        self.font_medium = pygame.font.Font(None, medium_size)
        self.font_small = pygame.font.Font(None, small_size)
        self.font_tiny = pygame.font.Font(None, tiny_size)

        # Button groups for each screen
        self.main_buttons = self._create_main_buttons()
        self.pause_buttons = self._create_pause_buttons()
        self.char_buttons = self._create_char_buttons()
        self.options_buttons = self._create_options_buttons()

        # Settings screen components (persistent)
        self.settings_components = None
        self._init_settings_components()

    # ========================================================================
    # BUTTON GROUP INITIALIZATION
    # ========================================================================

    def _create_main_buttons(self):
        """Create button rectangles for main menu"""
        from config.layout_manager import get_ui_element, get_screen_size

        buttons = []
        screen_width, _ = get_screen_size()

        # Get layout values
        button_width = get_ui_element("main_menu", "button_width") or 280
        button_height = get_ui_element("main_menu", "button_height") or 40
        button_start_y = get_ui_element("main_menu", "button_start_y") or 240
        button_spacing = get_ui_element("main_menu", "button_spacing") or 55

        button_x = screen_width // 2 - button_width // 2

        for i in range(
            6
        ):  # New Game, Continue, Level Map, Achievements, Options, Logout
            y = button_start_y + i * button_spacing
            buttons.append(pygame.Rect(button_x, y - 8, button_width, button_height))
        return buttons

    def _create_pause_buttons(self):
        """Create button rectangles for pause menu"""
        from config.layout_manager import get_ui_element, get_screen_size

        buttons = []
        screen_width, screen_height = get_screen_size()

        # Get layout values
        button_width = get_ui_element("pause_menu", "button_width") or 300
        button_height = get_ui_element("pause_menu", "button_height") or 40
        button_start_y = get_ui_element("pause_menu", "button_start_y") or (
            screen_height // 2 - 50
        )
        button_spacing = get_ui_element("pause_menu", "button_spacing") or 55

        button_x = screen_width // 2 - button_width // 2

        for i in range(3):  # Resume, Return to Menu, Logout
            y = button_start_y + i * button_spacing
            buttons.append(pygame.Rect(button_x, y - 8, button_width, button_height))
        return buttons

    def _create_char_buttons(self):
        """Create button rectangles for character selection"""
        from config.layout_manager import get_ui_element, get_screen_size

        buttons = []
        screen_width, _ = get_screen_size()

        # Get layout values
        char_y = get_ui_element("char_select", "char_start_y") or 280
        char_spacing = get_ui_element("char_select", "char_spacing") or 120
        char_width = get_ui_element("char_select", "char_width") or 56
        char_height = get_ui_element("char_select", "char_height") or 96

        for i in range(4):
            x = screen_width // 2 - 250 + i * char_spacing
            buttons.append(pygame.Rect(x, char_y, char_width, char_height))
        return buttons

    def _create_options_buttons(self):
        """Create button rectangles for options menu"""
        from config.layout_manager import get_ui_element, get_screen_size

        buttons = []
        screen_width, _ = get_screen_size()

        # Get layout values
        button_width = get_ui_element('main_menu', 'button_width') or 280
        button_height = get_ui_element('main_menu', 'button_height') or 40
        button_start_y = 220  # Options menu specific
        button_spacing = get_ui_element('main_menu', 'button_spacing') or 55

        button_x = screen_width // 2 - button_width // 2

        for i in range(4):  # Controls, Settings, Credits, Back
            y = button_start_y + i * button_spacing
            buttons.append(pygame.Rect(button_x, y - 8, button_width, button_height))
        return buttons

    def _init_settings_components(self):
        """Initialize settings screen components"""
        from ui.settings_components import Slider, Toggle, Dropdown

        self.settings_components = {
            'res_dropdown': Dropdown(400, 195, 300, 30, [], 0, "Resolution"),
            'fullscreen_toggle': Toggle(400, 245, 60, 30, False, "Fullscreen"),
            'music_toggle': Toggle(400, 365, 60, 30, True, "Music"),
            'music_slider': Slider(400, 420, 200, 0, 100, 70, "Music Volume"),
            'sfx_toggle': Toggle(400, 465, 60, 30, True, "SFX"),
            'sfx_slider': Slider(400, 520, 200, 0, 100, 80, "SFX Volume"),
            'colorblind_toggle': Toggle(400, 585, 60, 30, True, "Colorblind"),
        }

    # ========================================================================
    # MAIN MENU
    # ========================================================================

    def draw_main_menu(self, surface, current_profile, selection, mouse_pos=None):
        """Draw main menu using components"""
        screen_width, screen_height = get_screen_size()
        surface.fill(BLACK)

        if current_profile:
            profile_text = self.font_small.render(
                f"Profile: {current_profile.name}", True, UI_TEXT_DIM
            )
            surface.blit(profile_text, (20, 20))

        title = self.font_large.render("RETRO PLATFORMER", True, UI_HIGHLIGHT)
        surface.blit(title, (screen_width // 2 - title.get_width() // 2, 100))

        options = ["New Game", "Continue", "Level Map", "Achievements", "Options", "Logout"]
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
            hint, (screen_width // 2 - hint.get_width() // 2, screen_height - 60)
        )

        return None

    # ========================================================================
    # PROFILE SELECT
    # ========================================================================

    def draw_profile_select(self, surface, profiles, selection, scroll_offset, mouse_pos=None):
        """Draw profile selection screen"""
        screen_width, screen_height = get_screen_size()
        surface.fill(BLACK)

        title = self.font_large.render("SELECT PROFILE", True, UI_HIGHLIGHT)
        surface.blit(title, (screen_width // 2 - title.get_width() // 2, 60))

        if not profiles:
            msg = self.font_medium.render("No profiles found", True, UI_TEXT)
            surface.blit(msg, (screen_width // 2 - msg.get_width() // 2, 200))

            inst1 = self.font_small.render(
                "Press N to create new profile", True, UI_HIGHLIGHT
            )
            surface.blit(inst1, (screen_width // 2 - inst1.get_width() // 2, 280))
        else:
            y_start = 160
            box_height = 60
            box_spacing = 10
            item_height = box_height + box_spacing
            visible_items = 5  # Show 5 profiles at a time

            for i, profile in enumerate(profiles):
                # Calculate y position with scroll offset
                y = y_start + i * item_height - scroll_offset

                # Skip if not visible
                if y < y_start - item_height or y > y_start + visible_items * item_height:
                    continue

                is_selected = i == selection
                box_width = 500
                box_x = screen_width // 2 - box_width // 2
                box_rect = pygame.Rect(box_x, y, box_width, box_height)

                # Check mouse hover
                if mouse_pos and box_rect.collidepoint(mouse_pos):
                    is_selected = True

                box_color = UI_HIGHLIGHT if is_selected else UI_BORDER
                pygame.draw.rect(surface, box_color, box_rect, 2)

                if is_selected:
                    fill_rect = pygame.Rect(box_x + 2, y + 2, box_width - 4, box_height - 4)
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

            # Draw scroll indicators
            if len(profiles) > visible_items:
                indicator_x = screen_width // 2

                # Up arrow
                if scroll_offset > 0:
                    arrow_up = self.font_medium.render("▲", True, UI_HIGHLIGHT)
                    surface.blit(
                        arrow_up, (indicator_x - arrow_up.get_width() // 2, y_start - 30)
                    )

                # Down arrow
                max_scroll = max(
                    0, len(profiles) * item_height - visible_items * item_height
                )
                if scroll_offset < max_scroll:
                    arrow_down = self.font_medium.render("▼", True, UI_HIGHLIGHT)
                    arrow_y = y_start + visible_items * item_height + 10
                    surface.blit(
                        arrow_down, (indicator_x - arrow_down.get_width() // 2, arrow_y)
                    )

            inst1 = self.font_tiny.render(
                "UP/DOWN Navigate   ENTER/L Load   D Delete   N New", True, UI_TEXT_DIM
            )
            surface.blit(
                inst1, (screen_width // 2 - inst1.get_width() // 2, screen_height - 100)
            )

        # Two buttons at bottom: New Profile and Quit
        button_y = screen_height - 160 if profiles else 350
        # New Profile button
        self._draw_button(surface, "New Profile (N)", button_y, False)

        # Quit button
        quit_button_y = button_y + 60
        self._draw_button(surface, "Quit Game (Q)", quit_button_y, False)

        # Updated hint at very bottom
        hint = self.font_tiny.render(
            "ESC/Q Quit Game", True, UI_TEXT_DIM
        )
        surface.blit(
            hint, (screen_width // 2 - hint.get_width() // 2, screen_height - 60)
        )

        return None

    # ========================================================================
    # DIFFICULTY SELECT
    # ========================================================================

    def draw_difficulty_select(self, surface, selection, mouse_pos=None):
        """Draw difficulty selection"""
        screen_width, screen_height = get_screen_size()
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
        surface.blit(subtitle, (screen_width // 2 - subtitle.get_width() // 2, 140))

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
            box_x = screen_width // 2 - box_width // 2
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
            hint, (screen_width // 2 - hint.get_width() // 2, screen_height - 40)
        )

        screen.draw_buttons(surface)
        return screen

    # ========================================================================
    # CHARACTER SELECT
    # ========================================================================

    def draw_char_select(self, surface, player_name, char_selection, mouse_pos=None):
        """Draw character selection"""
        screen_width, screen_height = get_screen_size()
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
        surface.blit(name_label, (screen_width // 2 - name_label.get_width() // 2, 160))

        name_text = self.font_medium.render(f"{player_name}_", True, WHITE)
        surface.blit(name_text, (screen_width // 2 - name_text.get_width() // 2, 190))

        char_y = 280
        for i in range(4):
            x = screen_width // 2 - 250 + i * 120
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
            inst, (screen_width // 2 - inst.get_width() // 2, screen_height - 50)
        )

        screen.draw_buttons(surface)
        return screen

    # ========================================================================
    # OPTIONS MENU
    # ========================================================================

    def draw_options_menu(self, surface, selection, mouse_pos=None):
        """Draw options menu"""
        screen_width, screen_height = get_screen_size()
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
            hint, (screen_width // 2 - hint.get_width() // 2, screen_height - 60)
        )

        screen.draw_buttons(surface)
        return screen

    # ========================================================================
    # PAUSE MENU
    # ========================================================================

    def draw_pause_menu(self, surface, selection, mouse_pos=None):
        """Draw pause menu overlay"""
        screen_width, screen_height = get_screen_size()
        # Semi-transparent overlay
        overlay = pygame.Surface((screen_width, screen_height))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        surface.blit(overlay, (0, 0))

        # Options button top-right
        options_btn = IconButton(
            screen_width - 140, 20, 120, 40, Icon.SETTINGS, "Options", self.font_tiny
        )
        options_btn.check_hover(mouse_pos)
        options_btn.draw(surface)

        text = self.font_large.render("PAUSED", True, YELLOW)
        surface.blit(
            text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 - 140)
        )

        options = ["Resume", "Save & Return to Menu", "Save & Logout"]
        for i, option in enumerate(options):
            y = screen_height // 2 - 50 + i * 55
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
            hint, (screen_width // 2 - hint.get_width() // 2, screen_height // 2 + 140)
        )

        # Return options button for click detection
        return options_btn

    # ========================================================================
    # LEVEL MAP
    # ========================================================================

    def draw_level_map_screen(self, surface, current_profile, mouse_pos=None):
        """Draw level map with all levels"""
        screen_width, screen_height = get_screen_size()
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
        surface.blit(subtitle, (screen_width // 2 - subtitle.get_width() // 2, 130))

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
            inst, (screen_width // 2 - inst.get_width() // 2, screen_height - 100)
        )

        hint = self.font_tiny.render("ESC/Back Button to return", True, UI_TEXT_DIM)
        surface.blit(
            hint, (screen_width // 2 - hint.get_width() // 2, screen_height - 60)
        )

        screen.draw_buttons(surface)
        return screen

    # ========================================================================
    # CONTROLS SCREEN
    # ========================================================================

    def draw_controls_screen(self, surface, mouse_pos=None):
        """Draw controls screen"""
        screen_width, screen_height = get_screen_size()
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
            hint, (screen_width // 2 - hint.get_width() // 2, screen_height - 50)
        )

        screen.draw_buttons(surface)
        return screen

    # ========================================================================
    # SETTINGS SCREEN
    # ========================================================================

    def draw_settings_screen(self, surface, game_settings, mouse_pos=None):
        """Draw functional settings screen with video and audio controls"""
        screen_width, screen_height = get_screen_size()
        screen = Screen("SETTINGS", self.font_large, self.font_medium,
                    self.font_small, self.font_tiny,
                    show_back=True, show_options=False)

        screen.draw_background(surface)
        screen.update_button_hover(mouse_pos)
        screen.draw_title(surface, 60)

        # Update components with current settings
        components = self.settings_components

        # Update resolution dropdown options and selection
        components['res_dropdown'].options = game_settings.get_resolution_list()
        components['res_dropdown'].selected_index = game_settings.settings['video']['resolution_index']

        # Update toggles
        components['fullscreen_toggle'].enabled = game_settings.get_fullscreen()
        components['music_toggle'].enabled = game_settings.get_music_enabled()
        components['sfx_toggle'].enabled = game_settings.get_sfx_enabled()

        # Update sliders
        components['music_slider'].current_value = game_settings.get_music_volume()
        components['sfx_slider'].current_value = game_settings.get_sfx_volume()

        # VIDEO SETTINGS Section
        video_title = self.font_medium.render("VIDEO", True, UI_HIGHLIGHT)
        surface.blit(video_title, (150, 150))

        # Resolution
        res_label = self.font_small.render("Resolution:", True, UI_TEXT)
        surface.blit(res_label, (150, 200))

        # Fullscreen
        fs_label = self.font_small.render("Fullscreen:", True, UI_TEXT)
        surface.blit(fs_label, (150, 250))
        components['fullscreen_toggle'].check_hover(mouse_pos)
        components['fullscreen_toggle'].draw(surface, self.font_tiny)

        # AUDIO SETTINGS Section
        audio_title = self.font_medium.render("AUDIO", True, UI_HIGHLIGHT)
        surface.blit(audio_title, (150, 320))

        # Music toggle
        music_label = self.font_small.render("Music:", True, UI_TEXT)
        surface.blit(music_label, (150, 370))
        components['music_toggle'].check_hover(mouse_pos)
        components['music_toggle'].draw(surface, self.font_tiny)

        # Music volume
        music_vol_label = self.font_small.render("Music Volume:", True, UI_TEXT)
        surface.blit(music_vol_label, (150, 420))
        components['music_slider'].check_hover(mouse_pos)
        components['music_slider'].draw(surface, self.font_tiny)

        # SFX toggle
        sfx_label = self.font_small.render("Sound Effects:", True, UI_TEXT)
        surface.blit(sfx_label, (150, 470))
        components['sfx_toggle'].check_hover(mouse_pos)
        components['sfx_toggle'].draw(surface, self.font_tiny)

        # SFX volume
        sfx_vol_label = self.font_small.render("SFX Volume:", True, UI_TEXT)
        surface.blit(sfx_vol_label, (150, 520))
        components['sfx_slider'].check_hover(mouse_pos)
        components['sfx_slider'].draw(surface, self.font_tiny)

        # ACCESSIBILITY SETTINGS Section
        access_title = self.font_medium.render("ACCESSIBILITY", True, UI_HIGHLIGHT)
        surface.blit(access_title, (150, 560))

        # Colorblind mode toggle
        cb_label = self.font_small.render("Colorblind Mode:", True, UI_TEXT)
        surface.blit(cb_label, (150, 590))

        components['colorblind_toggle'].enabled = game_settings.get_colorblind_mode()
        components['colorblind_toggle'].check_hover(mouse_pos)
        components['colorblind_toggle'].draw(surface, self.font_tiny)

        # Description
        cb_desc = self.font_tiny.render(
            "Adds visual patterns to help distinguish objects", True, UI_TEXT_DIM
        )
        surface.blit(cb_desc, (150, 615))

        # Instructions
        hint = self.font_tiny.render(
            "Click to adjust   Changes save automatically   ESC/Back to return",
            True, UI_TEXT_DIM
        )
        surface.blit(hint, (screen_width // 2 - hint.get_width() // 2, screen_height - 60))

        # Draw restart warning if resolution changed
        if hasattr(game_settings, "_resolution_changed"):
            warning = self.font_small.render(
                "⚠ Resolution change requires restart to take effect", True, (255, 200, 0)
            )
            surface.blit(warning, (150, 580))

        screen.draw_buttons(surface)

        # DRAW DROPDOWN LAST (so it appears on top)
        components['res_dropdown'].check_hover(mouse_pos)
        components['res_dropdown'].draw(surface, self.font_tiny)

        return screen

    # ========================================================================
    # CREDITS SCREEN
    # ========================================================================

    def draw_credits_screen(self, surface, mouse_pos=None):
        """Draw credits screen"""
        screen_width, screen_height = get_screen_size()
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
                surface.blit(text1, (screen_width// 2 - text1.get_width() // 2, y))
            if line2:
                y += 25
                text2 = self.font_small.render(
                    line2, True, UI_TEXT if not line1 else UI_TEXT_DIM
                )
                surface.blit(text2, (screen_width// 2 - text2.get_width() // 2, y))
            y += 30

        version = self.font_tiny.render("Version 0.4 Alpha", True, UI_TEXT_DIM)
        surface.blit(
            version, (screen_width // 2 - version.get_width() // 2, screen_height - 100)
        )

        hint = self.font_tiny.render("ESC/Back Button to return", True, UI_TEXT_DIM)
        surface.blit(
            hint, (screen_width // 2 - hint.get_width() // 2, screen_height - 60)
        )

        screen.draw_buttons(surface)
        return screen

    # ========================================================================
    # GAME OVER / VICTORY
    # ========================================================================

    def draw_game_over(self, surface, score):
        """Draw game over screen"""
        screen_width, screen_height = get_screen_size()
        surface.fill(BLACK)
        text = self.font_large.render("GAME OVER", True, (220, 80, 80))
        surface.blit(
            text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 - 100)
        )

        score_text = self.font_medium.render(f"Final Score: {score}", True, WHITE)
        surface.blit(
            score_text,
            (screen_width // 2 - score_text.get_width() // 2, screen_height // 2),
        )

        inst = self.font_tiny.render("ENTER to return to menu", True, UI_TEXT_DIM)
        surface.blit(
            inst, (screen_width // 2 - inst.get_width() // 2, screen_height // 2 + 100)
        )

        return None

    def draw_victory(self, surface, score):
        """Draw victory screen"""
        screen_width, screen_height = get_screen_size()
        surface.fill(BLACK)
        text = self.font_large.render("VICTORY!", True, (100, 255, 100))
        surface.blit(
            text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 - 100)
        )

        score_text = self.font_medium.render(f"Final Score: {score}", True, WHITE)
        surface.blit(
            score_text,
            (screen_width // 2 - score_text.get_width() // 2, screen_height // 2),
        )

        inst = self.font_tiny.render("ENTER to return to menu", True, UI_TEXT_DIM)
        surface.blit(
            inst, (screen_width // 2 - inst.get_width() // 2, screen_height // 2 + 100)
        )

        return None

    # ========================================================================
    # UTILITY METHODS
    # ========================================================================

    def check_button_click(self, buttons, mouse_pos, mouse_pressed):
        """Check if any button was clicked"""
        screen_width, screen_height = get_screen_size()
        if not mouse_pressed[0]:
            return -1
        for i, button in enumerate(buttons):
            if button.collidepoint(mouse_pos):
                return i
        return -1

    def _draw_button(self, surface, text, y, is_selected):
        """Helper to draw a consistent button"""
        screen_width, screen_height = get_screen_size()
        button_width = 280
        button_height = 40
        x = screen_width// 2 - button_width // 2
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

    def refresh_buttons(self):
        """Recreate all button rectangles - call this after resolution change"""
        self.main_buttons = self._create_main_buttons()
        self.pause_buttons = self._create_pause_buttons()
        self.char_buttons = self._create_char_buttons()
        self.options_buttons = self._create_options_buttons()
        
        # Also refresh fonts
        from config.layout_manager import get_font_size
        
        large_size = get_font_size('large') or 52
        medium_size = get_font_size('medium') or 32
        small_size = get_font_size('small') or 22
        tiny_size = get_font_size('tiny') or 18
        
        self.font_large = pygame.font.Font(None, large_size)
        self.font_medium = pygame.font.Font(None, medium_size)
        self.font_small = pygame.font.Font(None, small_size)
        self.font_tiny = pygame.font.Font(None, tiny_size)

    # ========================================================================
    # ACHIEVEMENTS SCREEN
    # ========================================================================

    def draw_achievements_screen(self, surface, achievement_manager, mouse_pos=None):
        """Draw achievements screen with back button"""
        from ui.achievement_ui import AchievementScreen
        from ui.components import Screen

        # Create screen with back button
        screen = Screen(
            "ACHIEVEMENTS",
            self.font_large,
            self.font_medium,
            self.font_small,
            self.font_tiny,
            show_back=True,
            show_options=False,
        )

        screen.draw_background(surface)
        screen.update_button_hover(mouse_pos)

        # Create achievement screen if needed
        if not hasattr(self, "achievement_screen"):
            self.achievement_screen = AchievementScreen(
                self.font_large, self.font_medium, self.font_small, self.font_tiny
            )

        # Draw achievement content (without title since Screen draws it)
        self.achievement_screen.draw_content(surface, achievement_manager, mouse_pos)

        # Draw back button
        screen.draw_buttons(surface)

        return screen

    def get_profile_quit_button_rect(self, profiles):
        """Get quit button rectangle for profile select screen"""
        screen_width, screen_height = get_screen_size()
        button_width = 280
        button_height = 40
        button_x = screen_width // 2 - button_width // 2
        button_y = screen_height - 160 if profiles else 350
        quit_button_y = button_y + 60
        return pygame.Rect(button_x, quit_button_y - 8, button_width, button_height)
