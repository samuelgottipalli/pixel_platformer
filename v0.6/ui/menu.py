"""
Refactored Menu System Using Modular Components
Cleaner, more maintainable menu code with reusable components
"""

import pygame
from config.layout_manager import get_screen_size, get_ui_element, get_font_size, get_scale_factor
from config.settings import (
    GRAY, GREEN, RED, UI_SELECTED_BG,
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

        # Get font sizes from layout (with fallbacks)
        large_size = get_font_size('large') or 52
        medium_size = get_font_size('medium') or 32
        small_size = get_font_size('small') or 22
        tiny_size = get_font_size('tiny') or 18

        self.font_large = pygame.font.Font(None, large_size)
        self.font_medium = pygame.font.Font(None, medium_size)
        self.font_small = pygame.font.Font(None, small_size)
        self.font_tiny = pygame.font.Font(None, tiny_size)

        # Screen dimensions and scale factor
        self.screen_width, self.screen_height = get_screen_size()
        self.scale_factor = get_scale_factor()

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

    # Every clickable element on a screen comes from one of these functions,
    # used both to draw it and to hit-test mouse clicks, so they always match.

    def _button_column(self, screen_name, count, width=280, height=40, start_y=240, spacing=55):
        """Centered column of button rects using layout values for screen_name"""
        start_y = get_ui_element(screen_name, "button_start_y") or start_y
        spacing = get_ui_element(screen_name, "button_spacing") or spacing
        width = get_ui_element(screen_name, "button_width") or width
        height = get_ui_element(screen_name, "button_height") or height
        x = self.screen_width // 2 - width // 2
        return [pygame.Rect(x, start_y + i * spacing - 8, width, height) for i in range(count)]

    def _create_main_buttons(self):
        """New Game, Continue, Level Map, Achievements, Options, Logout"""
        return self._button_column("main_menu", 6)

    def _create_pause_buttons(self):
        """Shop, Resume, Save & Return to Menu, Save & Logout"""
        return self._button_column("pause_menu", 4, width=300)

    def _create_char_buttons(self):
        """Character swatches on the character select screen"""
        char_y = get_ui_element("char_select", "char_start_y") or 280
        char_spacing = get_ui_element("char_select", "char_spacing") or 120
        char_width = get_ui_element("char_select", "char_width") or 56
        char_height = get_ui_element("char_select", "char_height") or 96
        return [
            pygame.Rect(self.screen_width // 2 - 250 + i * char_spacing, char_y, char_width, char_height)
            for i in range(4)
        ]

    def _create_options_buttons(self):
        """Controls, Settings, Credits, Back"""
        return self._button_column("options_menu", 4)

    def get_difficulty_rects(self):
        """Easy / Normal / Hard boxes"""
        start_y = get_ui_element("difficulty_select", "button_start_y") or 200
        spacing = get_ui_element("difficulty_select", "button_spacing") or 120
        box_width, box_height = 500, 100
        x = self.screen_width // 2 - box_width // 2
        return [pygame.Rect(x, start_y + i * spacing, box_width, box_height) for i in range(3)]

    PROFILE_LIST_Y = 140
    PROFILE_ITEM_HEIGHT = 70  # 60px box + 10px gap
    PROFILE_VISIBLE = 5

    def get_profile_box_rects(self, profiles, scroll_offset):
        """(index, rect) for each profile box currently visible in the list"""
        box_width, box_height = 500, 60
        x = self.screen_width // 2 - box_width // 2
        top = self.PROFILE_LIST_Y
        bottom = top + self.PROFILE_VISIBLE * self.PROFILE_ITEM_HEIGHT
        rects = []
        for i in range(len(profiles)):
            y = top + i * self.PROFILE_ITEM_HEIGHT - scroll_offset
            if top <= y and y + box_height <= bottom:
                rects.append((i, pygame.Rect(x, y, box_width, box_height)))
        return rects

    def get_profile_action_rects(self, profiles):
        """(New Profile rect, Quit rect): side by side under the list"""
        width, height, gap = 280, 40, 20
        y = 560 if profiles else 350
        center = self.screen_width // 2
        return (
            pygame.Rect(center - gap // 2 - width, y, width, height),
            pygame.Rect(center + gap // 2, y, width, height),
        )

    def _init_settings_components(self):
        """Initialize settings screen components"""
        from ui.settings_components import Slider, Toggle, Dropdown

        self.settings_components = {
            'res_dropdown': Dropdown(400, 175, 300, 30, [], 0, "Resolution"),
            'fullscreen_toggle': Toggle(400, 217, 60, 30, False, "Fullscreen"),
            'music_toggle': Toggle(400, 307, 60, 30, True, "Music"),
            'music_slider': Slider(400, 354, 200, 0, 100, 70, "Music Volume"),
            'sfx_toggle': Toggle(400, 391, 60, 30, True, "SFX"),
            'sfx_slider': Slider(400, 438, 200, 0, 100, 80, "SFX Volume"),
            'colorblind_toggle': Toggle(400, 531, 60, 30, True, "Colorblind"),
        }

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
        surface.blit(title, (self.screen_width // 2 - title.get_width() // 2, 100))

        options = ["New Game", "Continue", "Level Map", "Achievements", "Options", "Logout"]
        for i, (option, rect) in enumerate(zip(options, self.main_buttons)):
            hovered = mouse_pos is not None and rect.collidepoint(mouse_pos)
            self._draw_button(surface, option, rect, i == selection or hovered)

        hint = self.font_tiny.render(
            "UP/DOWN Navigate   ENTER Select   ESC Logout", True, UI_TEXT_DIM
        )
        surface.blit(
            hint, (self.screen_width // 2 - hint.get_width() // 2, self.screen_height - 60)
        )

        return None

    # ========================================================================
    # PROFILE SELECT
    # ========================================================================

    def draw_profile_select(self, surface, profiles, selection, scroll_offset, mouse_pos=None):
        """Draw profile selection screen"""
        surface.fill(BLACK)

        title = self.font_large.render("SELECT PROFILE", True, UI_HIGHLIGHT)
        surface.blit(title, (self.screen_width // 2 - title.get_width() // 2, 60 * self.scale_factor))

        if not profiles:
            msg = self.font_medium.render("No profiles found", True, UI_TEXT)
            surface.blit(msg, (self.screen_width // 2 - msg.get_width() // 2, 200 * self.scale_factor))
            inst1 = self.font_small.render(
                "Press N to create new profile", True, UI_HIGHLIGHT
            )
            surface.blit(inst1, (self.screen_width // 2 - inst1.get_width() // 2, 280 * self.scale_factor))
        else:
            y_start = self.PROFILE_LIST_Y
            item_height = self.PROFILE_ITEM_HEIGHT
            visible_items = self.PROFILE_VISIBLE

            for i, box_rect in self.get_profile_box_rects(profiles, scroll_offset):
                profile = profiles[i]
                box_x, y = box_rect.x, box_rect.y
                box_width, box_height = box_rect.width, box_rect.height
                is_selected = i == selection or (
                    mouse_pos is not None and box_rect.collidepoint(mouse_pos)
                )

                box_color = UI_HIGHLIGHT if is_selected else UI_BORDER
                pygame.draw.rect(surface, box_color, box_rect, 2)

                if is_selected:
                    fill_surface = pygame.Surface((box_width - 4, box_height - 4))
                    fill_surface.set_alpha(30)
                    fill_surface.fill(UI_HIGHLIGHT)
                    surface.blit(fill_surface, (box_x + 2, y + 2))

                name_text = self.font_medium.render(profile.name, True, UI_TEXT)
                surface.blit(name_text, (box_x + 20, y + 8))

                stats_text = self.font_tiny.render(
                    f"Levels: {profile.levels_completed}  Score: {profile.total_score}  Coins: {profile.total_coins_collected}",
                    True,
                    UI_TEXT_DIM,
                )
                surface.blit(stats_text, (box_x + 20, y + 35))

            # Draw scroll indicators
            if len(profiles) > visible_items:
                indicator_x = self.screen_width // 2

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
                    arrow_y = y_start + visible_items * item_height - 2
                    surface.blit(
                        arrow_down, (indicator_x - arrow_down.get_width() // 2, arrow_y)
                    )

        # New Profile and Quit buttons side by side
        new_rect, quit_rect = self.get_profile_action_rects(profiles)
        for label, rect in (("New Profile (N)", new_rect), ("Quit Game (Q)", quit_rect)):
            hovered = mouse_pos is not None and rect.collidepoint(mouse_pos)
            self._draw_button(surface, label, rect, hovered)

        hint_text = "ESC/Q Quit Game"
        if profiles:
            hint_text = "UP/DOWN Navigate   ENTER/L Load   D Delete   N New   ESC/Q Quit"
        hint = self.font_tiny.render(hint_text, True, UI_TEXT_DIM)
        surface.blit(
            hint, (self.screen_width // 2 - hint.get_width() // 2, new_rect.bottom + 40)
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
            ("EASY", "5 Lives - More Resources - 2x Time", GREEN),
            ("NORMAL", "3 Lives - Balanced Challenge - Standard", WHITE),
            ("HARD", "1 Life - Extreme Challenge - 2x Score", RED),
        ]

        for i, ((name, desc, color), box_rect) in enumerate(zip(difficulties, self.get_difficulty_rects())):
            y, box_x, box_width = box_rect.y, box_rect.x, box_rect.width
            is_selected = i == selection

            if mouse_pos and box_rect.collidepoint(mouse_pos):
                is_selected = True

            if is_selected:
                pygame.draw.rect(surface, UI_SELECTED_BG, box_rect, border_radius=8)
                pygame.draw.rect(surface, color, box_rect, 4, border_radius=8)
                name_color = color
                desc_color = UI_TEXT
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

        for i, rect in enumerate(self.char_buttons):
            x, char_y = rect.x, rect.y
            is_selected = i == char_selection or (
                mouse_pos is not None and rect.collidepoint(mouse_pos)
            )

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
        for i, (option, rect) in enumerate(zip(options, self.options_buttons)):
            hovered = mouse_pos is not None and rect.collidepoint(mouse_pos)
            self._draw_button(surface, option, rect, i == selection or hovered)

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
        title_y = get_ui_element("pause_menu", "title_y") or 150
        surface.blit(text, (screen_width // 2 - text.get_width() // 2, title_y))

        options = ["Shop", "Resume", "Save & Return to Menu", "Save & Logout"]
        for i, (option, rect) in enumerate(zip(options, self.pause_buttons)):
            hovered = mouse_pos is not None and rect.collidepoint(mouse_pos)
            self._draw_button(surface, option, rect, i == selection or hovered)

        hint = self.font_tiny.render(
            "UP/DOWN Navigate   ENTER Select   ESC/P Resume", True, UI_TEXT_DIM
        )
        surface.blit(
            hint, (screen_width // 2 - hint.get_width() // 2, self.pause_buttons[-1].bottom + 30)
        )

        # Return options button for click detection
        return options_btn

    # ========================================================================
    # LEVEL MAP
    # ========================================================================

    def get_level_map_row_rects(self, count):
        """Clickable level rows on the level map (shared by draw and input)"""
        screen_width, _ = get_screen_size()
        row_width, row_height = 560, 42
        x = screen_width // 2 - row_width // 2
        return [
            pygame.Rect(x, y - 8, row_width, row_height)
            for y in LayoutHelper.create_vertical_layout(215, count, 52)
        ]

    def get_level_map_act_tab_rects(self, count):
        """Clickable act tabs on the level map"""
        screen_width, _ = get_screen_size()
        tab_width, tab_height, gap = 170, 40, 14
        total = count * tab_width + (count - 1) * gap
        x0 = screen_width // 2 - total // 2
        return [pygame.Rect(x0 + i * (tab_width + gap), 110, tab_width, tab_height) for i in range(count)]

    @staticmethod
    def act_of_level(acts, level_index):
        """Index into acts of the act containing a global level index"""
        for i, act in enumerate(acts):
            if any(level["index"] == level_index for level in act["levels"]):
                return i
        return 0

    def draw_level_map_screen(self, surface, acts, current_profile, selection=0, mouse_pos=None):
        """
        Draw level map: one act at a time (tabs), levels unlocking in order.
        A level is playable once the level before it is completed (the
        tutorial is always open); `selection` is a global level index.
        """
        from levels.level_names import level_title

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
        screen.draw_title(surface, 50)

        total_levels = sum(len(act["levels"]) for act in acts)
        completed = current_profile.levels_completed if current_profile else 0
        playable = min(total_levels, completed + 1)
        shown = self.act_of_level(acts, selection)

        # Act tabs (locked acts are dimmed)
        for i, (act, rect) in enumerate(zip(acts, self.get_level_map_act_tab_rects(len(acts)))):
            unlocked = act["levels"][0]["index"] < playable
            active = i == shown
            pygame.draw.rect(surface, UI_SELECTED_BG if active else UI_BG, rect, border_radius=6)
            pygame.draw.rect(surface, UI_HIGHLIGHT if active else UI_BORDER, rect, 2, border_radius=6)
            color = UI_HIGHLIGHT if active else (UI_TEXT if unlocked else UI_TEXT_DIM)
            label = self.font_small.render(f"ACT {act['number']}" + ("" if unlocked else "  (locked)"), True, color)
            surface.blit(label, (rect.centerx - label.get_width() // 2, rect.centery - label.get_height() // 2))

        act = acts[shown]
        act_done = sum(1 for level in act["levels"] if level["index"] < completed)
        subtitle = self.font_small.render(
            f"{act['name']}  -  {act_done} / {len(act['levels'])} completed", True, UI_TEXT
        )
        surface.blit(subtitle, (screen_width // 2 - subtitle.get_width() // 2, 168))

        rows = self.get_level_map_row_rects(len(act["levels"]))
        for level, rect in zip(act["levels"], rows):
            i = level["index"]
            if i < completed:
                icon_type, icon_color, name_color = Icon.CHECKMARK, GREEN, UI_TEXT
            elif i < playable:
                icon_type, icon_color, name_color = Icon.PLAY, YELLOW, UI_TEXT
            else:
                icon_type, icon_color, name_color = Icon.LOCK, GRAY, UI_TEXT_DIM

            hovered = mouse_pos and i < playable and rect.collidepoint(mouse_pos)
            if i == selection or hovered:
                pygame.draw.rect(surface, UI_SELECTED_BG, rect, border_radius=6)
                pygame.draw.rect(surface, UI_HIGHLIGHT, rect, 2, border_radius=6)
                if i < playable:
                    name_color = UI_HIGHLIGHT

            Icon.draw(surface, icon_type, rect.x + 16, rect.y + 11, 20, icon_color)
            name_surf = self.font_small.render(level_title(level, mark_boss=True), True, name_color)
            surface.blit(name_surf, (rect.x + 56, rect.y + rect.height // 2 - name_surf.get_height() // 2))

        inst = self.font_tiny.render(
            "LEFT/RIGHT: Act  |  UP/DOWN: Level  |  ENTER or Click: Play  |  Complete a level to unlock the next",
            True,
            UI_TEXT_DIM,
        )
        surface.blit(inst, (screen_width // 2 - inst.get_width() // 2, screen_height - 90))

        hint = self.font_tiny.render("ESC/Back Button to return", True, UI_TEXT_DIM)
        surface.blit(hint, (screen_width // 2 - hint.get_width() // 2, screen_height - 60))

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
            ("1 - 5", "Switch Weapon"),
            ("Pause > Shop", "Buy Weapons"),
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
        surface.blit(video_title, (150, 130))

        # Resolution
        res_label = self.font_small.render("Resolution:", True, UI_TEXT)
        surface.blit(res_label, (150, 180))

        # Fullscreen
        fs_label = self.font_small.render("Fullscreen:", True, UI_TEXT)
        surface.blit(fs_label, (150, 222))
        components['fullscreen_toggle'].check_hover(mouse_pos)
        components['fullscreen_toggle'].draw(surface, self.font_tiny)

        # AUDIO SETTINGS Section
        audio_title = self.font_medium.render("AUDIO", True, UI_HIGHLIGHT)
        surface.blit(audio_title, (150, 268))

        # Music toggle
        music_label = self.font_small.render("Music:", True, UI_TEXT)
        surface.blit(music_label, (150, 312))
        components['music_toggle'].check_hover(mouse_pos)
        components['music_toggle'].draw(surface, self.font_tiny)

        # Music volume
        music_vol_label = self.font_small.render("Music Volume:", True, UI_TEXT)
        surface.blit(music_vol_label, (150, 354))
        components['music_slider'].check_hover(mouse_pos)
        components['music_slider'].draw(surface, self.font_tiny)

        # SFX toggle
        sfx_label = self.font_small.render("Sound Effects:", True, UI_TEXT)
        surface.blit(sfx_label, (150, 396))
        components['sfx_toggle'].check_hover(mouse_pos)
        components['sfx_toggle'].draw(surface, self.font_tiny)

        # SFX volume
        sfx_vol_label = self.font_small.render("SFX Volume:", True, UI_TEXT)
        surface.blit(sfx_vol_label, (150, 438))
        components['sfx_slider'].check_hover(mouse_pos)
        components['sfx_slider'].draw(surface, self.font_tiny)

        # ACCESSIBILITY SETTINGS Section
        access_title = self.font_medium.render("ACCESSIBILITY", True, UI_HIGHLIGHT)
        surface.blit(access_title, (150, 490))

        # Colorblind mode toggle
        cb_label = self.font_small.render("Colorblind Mode:", True, UI_TEXT)
        surface.blit(cb_label, (150, 536))

        components['colorblind_toggle'].enabled = game_settings.get_colorblind_mode()
        components['colorblind_toggle'].check_hover(mouse_pos)
        components['colorblind_toggle'].draw(surface, self.font_tiny)

        # Description
        cb_desc = self.font_tiny.render(
            "Adds visual patterns to help distinguish objects", True, UI_TEXT_DIM
        )
        surface.blit(cb_desc, (150, 572))

        # Instructions
        hint = self.font_tiny.render(
            "Click to adjust   Changes save automatically   ESC/Back to return",
            True, UI_TEXT_DIM
        )
        surface.blit(hint, (screen_width // 2 - hint.get_width() // 2, screen_height - 60))

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
                y += 20
                text2 = self.font_small.render(
                    line2, True, UI_TEXT if not line1 else UI_TEXT_DIM
                )
                surface.blit(text2, (screen_width// 2 - text2.get_width() // 2, y))
            y += 25
        from os import getcwd, sep
        version = self.font_tiny.render(
            f"Version {getcwd().split(sep)[-1]} Alpha", True, UI_TEXT_DIM
        )
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
        text = self.font_large.render("GAME OVER", True, RED)
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
        text = self.font_large.render("VICTORY!", True, GREEN)
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
        if not mouse_pressed[0]:
            return -1
        for i, button in enumerate(buttons):
            if button.collidepoint(mouse_pos):
                return i
        return -1

    def _draw_button(self, surface, text, button_rect, is_selected):
        """Draw a button in exactly the rect used for its click detection"""
        button_width, button_height = button_rect.width, button_rect.height

        # Draw button background and border
        if is_selected:
            pygame.draw.rect(surface, UI_SELECTED_BG, button_rect, border_radius=5)
            pygame.draw.rect(surface, UI_HIGHLIGHT, button_rect, 2, border_radius=5)
            text_color = UI_HIGHLIGHT
        else:
            pygame.draw.rect(surface, UI_BG, button_rect, border_radius=5)
            pygame.draw.rect(surface, UI_BORDER, button_rect, 1, border_radius=5)
            text_color = UI_TEXT

        # Draw text CENTERED IN THE RECT (not at y!)
        text_surf = self.font_medium.render(text, True, text_color)
        text_x = button_rect.x + button_width // 2 - text_surf.get_width() // 2
        text_y = button_rect.y + button_height // 2 - text_surf.get_height() // 2  # ← FIX: Center in rect!
        surface.blit(text_surf, (text_x, text_y))

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
        return self.get_profile_action_rects(profiles)[1]
