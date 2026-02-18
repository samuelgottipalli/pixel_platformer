"""
UI Components - Buttons, Screens, Popups  
UPDATED: Popup and Screen use LayoutManager for responsive positioning
"""

import pygame
from config.settings import UI_BG, UI_BORDER, UI_HIGHLIGHT, UI_TEXT, UI_TEXT_DIM, WHITE, BLACK, SCREEN_WIDTH, SCREEN_HEIGHT
from config.layout_manager import get_screen_size, get_ui_element


class Icon:
    """Icon rendering helper"""
    BACK_ARROW = "back"
    SETTINGS = "settings"
    
    @staticmethod
    def draw(surface, icon_type, x, y, size, color=WHITE):
        """Draw icon"""
        if icon_type == Icon.BACK_ARROW:
            # Draw left arrow
            points = [(x + size, y), (x, y + size // 2), (x + size, y + size)]
            pygame.draw.lines(surface, color, False, points, 3)
        elif icon_type == Icon.SETTINGS:
            # Draw gear icon (simplified)
            center = (x + size // 2, y + size // 2)
            pygame.draw.circle(surface, color, center, size // 3, 2)


class Button:
    """Interactive button component"""
    
    def __init__(self, x, y, width, height, text, text_color=UI_TEXT):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.text_color = text_color
        self.hovered = False
        self.is_selected = False
        
    def check_hover(self, mouse_pos):
        """Check if mouse is hovering over button"""
        if mouse_pos:
            self.hovered = self.rect.collidepoint(mouse_pos)
        return self.hovered
    
    def check_click(self, mouse_pos, mouse_pressed):
        """Check if button was clicked"""
        if mouse_pos and mouse_pressed[0]:
            return self.rect.collidepoint(mouse_pos)
        return False
    
    def draw(self, surface, font):
        """Render button"""
        color = UI_HIGHLIGHT if (self.hovered or self.is_selected) else UI_BORDER
        pygame.draw.rect(surface, UI_BG, self.rect)
        pygame.draw.rect(surface, color, self.rect, 2)
        
        text_surf = font.render(self.text, True, self.text_color)
        text_x = self.rect.centerx - text_surf.get_width() // 2
        text_y = self.rect.centery - text_surf.get_height() // 2
        surface.blit(text_surf, (text_x, text_y))


class IconButton:
    """Button with icon and text"""
    
    def __init__(self, x, y, width, height, icon_type, text, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.icon_type = icon_type
        self.text = text
        self.font = font
        self.hovered = False
        
    def check_hover(self, mouse_pos):
        """Check if mouse is hovering"""
        if mouse_pos:
            self.hovered = self.rect.collidepoint(mouse_pos)
        return self.hovered
    
    def check_click(self, mouse_pos, mouse_pressed):
        """Check if clicked"""
        if mouse_pos and mouse_pressed[0]:
            return self.rect.collidepoint(mouse_pos)
        return False
    
    def draw(self, surface):
        """Draw button with icon"""
        color = UI_HIGHLIGHT if self.hovered else UI_BORDER
        pygame.draw.rect(surface, UI_BG, self.rect)
        pygame.draw.rect(surface, color, self.rect, 2, border_radius=5)
        
        # Draw icon
        Icon.draw(surface, self.icon_type, 
                 self.rect.x + 10, 
                 self.rect.y + self.rect.height // 2 - 10,
                 20, UI_TEXT if self.hovered else UI_TEXT_DIM)
        
        # Draw text
        text_surf = self.font.render(self.text, True, UI_TEXT if self.hovered else UI_TEXT_DIM)
        text_x = self.rect.x + 40
        text_y = self.rect.y + self.rect.height // 2 - text_surf.get_height() // 2
        surface.blit(text_surf, (text_x, text_y))


class TextBox:
    """Reusable text display box"""
    
    def __init__(self, x, y, width, height, border_color=UI_BORDER):
        self.rect = pygame.Rect(x, y, width, height)
        self.border_color = border_color
        self.bg_color = UI_BG
        
    def draw(self, surface, lines, font, text_color=UI_TEXT):
        """Draw box with multiple lines of text"""
        # Draw box
        pygame.draw.rect(surface, self.bg_color, self.rect, border_radius=5)
        pygame.draw.rect(surface, self.border_color, self.rect, 2, border_radius=5)
        
        # Draw text lines
        line_height = 30
        start_y = self.rect.y + 20
        for i, line in enumerate(lines):
            text_surf = font.render(line, True, text_color)
            text_x = self.rect.x + self.rect.width // 2 - text_surf.get_width() // 2
            text_y = start_y + i * line_height
            surface.blit(text_surf, (text_x, text_y))


class SelectableBox:
    """Box with selectable/unlocked state (for level selection, etc)"""
    
    def __init__(self, x, y, width, height, label, is_unlocked=True):
        self.rect = pygame.Rect(x, y, width, height)
        self.label = label
        self.is_unlocked = is_unlocked
        self.is_selected = False
        self.is_hovered = False
        
    def check_hover(self, mouse_pos):
        """Check if mouse is over box"""
        self.is_hovered = self.rect.collidepoint(mouse_pos) if mouse_pos else False
        return self.is_hovered
    
    def draw(self, surface, font_large, font_small):
        """Draw box with locked/unlocked appearance"""
        is_active = (self.is_selected or self.is_hovered) and self.is_unlocked
        
        # Colors based on state
        if not self.is_unlocked:
            border_color = UI_TEXT_DIM
            text_color = UI_TEXT_DIM
            icon = "🔒"
            icon_color = (150, 150, 150)
        elif is_active:
            border_color = UI_HIGHLIGHT
            text_color = UI_HIGHLIGHT
            icon = "✓"
            icon_color = UI_HIGHLIGHT
        else:
            border_color = UI_BORDER
            text_color = UI_TEXT
            icon = ""
            icon_color = UI_TEXT
        
        # Draw box
        pygame.draw.rect(surface, UI_BG, self.rect, border_radius=8)
        pygame.draw.rect(surface, border_color, self.rect, 3, border_radius=8)
        
        # Draw icon
        Icon.draw(surface, icon, self.rect.x + 15, self.rect.y + 15, 20, icon_color)
        
        # Draw label
        label_surf = font_small.render(self.label, True, text_color)
        surface.blit(label_surf, (self.rect.x + 50, self.rect.y + self.rect.height // 2 - 10))


class ButtonGroup:
    """Manages a group of buttons for navigation"""
    
    def __init__(self, buttons, orientation='vertical', spacing=55):
        self.buttons = buttons
        self.orientation = orientation
        self.spacing = spacing
        self.selected_index = 0
        
    def navigate_up(self):
        """Move selection up"""
        self.selected_index = (self.selected_index - 1) % len(self.buttons)
        self._update_selection()
        
    def navigate_down(self):
        """Move selection down"""
        self.selected_index = (self.selected_index + 1) % len(self.buttons)
        self._update_selection()
        
    def navigate_left(self):
        """Move selection left (for horizontal groups)"""
        if self.orientation == 'horizontal':
            self.selected_index = (self.selected_index - 1) % len(self.buttons)
            self._update_selection()
    
    def navigate_right(self):
        """Move selection right (for horizontal groups)"""
        if self.orientation == 'horizontal':
            self.selected_index = (self.selected_index + 1) % len(self.buttons)
            self._update_selection()
    
    def _update_selection(self):
        """Update button selection states"""
        for i, button in enumerate(self.buttons):
            button.is_selected = (i == self.selected_index)
    
    def check_hover(self, mouse_pos):
        """Update hover states and selection"""
        for i, button in enumerate(self.buttons):
            if button.check_hover(mouse_pos):
                self.selected_index = i
                self._update_selection()
    
    def check_click(self, mouse_pos, mouse_pressed):
        """Check which button was clicked"""
        for i, button in enumerate(self.buttons):
            if button.check_click(mouse_pos, mouse_pressed):
                return i
        return -1
    
    def draw(self, surface):
        """Draw all buttons"""
        for button in self.buttons:
            button.draw(surface)
    
    def get_selected(self):
        """Get currently selected button index"""
        return self.selected_index
    
    def set_selected(self, index):
        """Set selected button by index"""
        if 0 <= index < len(self.buttons):
            self.selected_index = index
            self._update_selection()


class Screen:
    """Base screen layout with optional back/options buttons - USES LAYOUT MANAGER"""
    
    def __init__(self, title, font_large, font_medium, font_small, font_tiny, 
                 show_back=False, show_options=False):
        self.title = title
        self.font_large = font_large
        self.font_medium = font_medium
        self.font_small = font_small
        self.font_tiny = font_tiny
        
        # Get screen size from layout
        screen_width, screen_height = get_screen_size()
        
        # Back button (bottom left)
        self.back_button = None
        if show_back:
            self.back_button = Button(
                20, screen_height - 60, 120, 40, 
                "Back", UI_TEXT_DIM
            )
        
        # Options button (bottom right)
        self.options_button = None
        if show_options:
            self.options_button = Button(
                screen_width - 140, screen_height - 60, 120, 40,
                "Options", UI_TEXT_DIM
            )
    
    def update_button_hover(self, mouse_pos):
        """Update button hover states"""
        if self.back_button:
            self.back_button.check_hover(mouse_pos)
        if self.options_button:
            self.options_button.check_hover(mouse_pos)
    
    def check_back_click(self, mouse_pos, mouse_pressed):
        """Check if back button was clicked"""
        if self.back_button:
            return self.back_button.check_click(mouse_pos, mouse_pressed)
        return False
    
    def check_options_click(self, mouse_pos, mouse_pressed):
        """Check if options button was clicked"""
        if self.options_button:
            return self.options_button.check_click(mouse_pos, mouse_pressed)
        return False
    
    def draw_buttons(self, surface):
        """Draw back/options buttons"""
        if self.back_button:
            self.back_button.draw(surface, self.font_small)
        if self.options_button:
            self.options_button.draw(surface, self.font_small)
    
    def draw_title(self, surface, y=100):
        """Draw screen title"""
        screen_width, _ = get_screen_size()
        title_surf = self.font_large.render(self.title, True, UI_HIGHLIGHT)
        title_x = screen_width // 2 - title_surf.get_width() // 2
        surface.blit(title_surf, (title_x, y))
    
    def draw_subtitle(self, surface, text, y=140):
        """Draw subtitle text"""
        screen_width, _ = get_screen_size()
        subtitle_surf = self.font_small.render(text, True, UI_TEXT_DIM)
        subtitle_x = screen_width // 2 - subtitle_surf.get_width() // 2
        surface.blit(subtitle_surf, (subtitle_x, y))
    
    def draw_hint(self, surface, text, y=None):
        """Draw hint text at bottom of screen"""
        screen_width, screen_height = get_screen_size()
        if y is None:
            y = screen_height - 60
        hint_surf = self.font_tiny.render(text, True, UI_TEXT_DIM)
        hint_x = screen_width // 2 - hint_surf.get_width() // 2
        surface.blit(hint_surf, (hint_x, y))
    
    def draw_background(self, surface):
        """Draw screen background"""
        surface.fill(BLACK)


class LayoutHelper:
    """Helper for positioning UI elements"""
    
    @staticmethod
    def center_x(width):
        """Get X position to center element"""
        screen_width, _ = get_screen_size()
        return screen_width // 2 - width // 2
    
    @staticmethod
    def center_y(height):
        """Get Y position to center element"""
        _, screen_height = get_screen_size()
        return screen_height // 2 - height // 2
    
    @staticmethod
    def create_vertical_layout(start_y, count, spacing=55):
        """Create Y positions for vertical button layout"""
        return [start_y + i * spacing for i in range(count)]
    
    @staticmethod
    def create_horizontal_layout(start_x, count, spacing=120):
        """Create X positions for horizontal button layout"""
        return [start_x + i * spacing for i in range(count)]
    
    @staticmethod
    def create_grid_layout(start_x, start_y, cols, rows, spacing_x=120, spacing_y=80):
        """Create positions for grid layout"""
        positions = []
        for row in range(rows):
            for col in range(cols):
                x = start_x + col * spacing_x
                y = start_y + row * spacing_y
                positions.append((x, y))
        return positions


class Popup:
    """Reusable popup message overlay - NOW WITH LAYOUT MANAGER"""
    
    def __init__(self, message, duration=120):
        self.message = message
        self.duration = duration
        self.timer = duration
        self.active = True
        
        # Get dimensions from layout
        popup_width = get_ui_element('popup', 'width')
        popup_height = get_ui_element('popup', 'height')
        
        self.width = popup_width if popup_width else 600
        self.height = popup_height if popup_height else 150
        
    def update(self):
        """Update popup timer"""
        if self.timer > 0:
            self.timer -= 1
        if self.timer <= 0:
            self.active = False
    
    def draw(self, surface, font):
        """Draw popup overlay"""
        if not self.active:
            return
        
        # Get screen size for centering
        screen_width, screen_height = get_screen_size()
        
        # Center position
        overlay_x = screen_width // 2 - self.width // 2
        overlay_y = screen_height // 2 - self.height // 2
        
        # Semi-transparent overlay
        overlay = pygame.Surface((self.width, self.height))
        overlay.fill((40, 40, 40))
        overlay.set_alpha(230)
        
        # Border
        border_rect = pygame.Rect(overlay_x - 2, overlay_y - 2, self.width + 4, self.height + 4)
        pygame.draw.rect(surface, (200, 100, 100), border_rect, 3)
        
        surface.blit(overlay, (overlay_x, overlay_y))
        
        # Word-wrap message
        words = self.message.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            test_surf = font.render(test_line, True, WHITE)
            if test_surf.get_width() < self.width - 50:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        if current_line:
            lines.append(' '.join(current_line))
        
        # Draw centered text
        total_height = len(lines) * 35
        start_y = overlay_y + self.height // 2 - total_height // 2
        
        for i, line in enumerate(lines):
            text_surf = font.render(line, True, WHITE)
            text_x = overlay_x + self.width // 2 - text_surf.get_width() // 2
            text_y = start_y + i * 35
            surface.blit(text_surf, (text_x, text_y))
    
    def is_active(self):
        """Check if popup is still active"""
        return self.active
