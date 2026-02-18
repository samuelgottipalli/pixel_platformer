"""
Reusable UI Components for Menu System
Provides modular buttons, text elements, and layout helpers
"""

import pygame
from config.settings import (BLACK, CYAN, GRAY, SCREEN_HEIGHT, SCREEN_WIDTH,
                             UI_BG, UI_BORDER, UI_HIGHLIGHT, UI_TEXT,
                             UI_TEXT_DIM, WHITE, YELLOW)


class Button:
    """Reusable button component"""
    
    def __init__(self, x, y, width, height, text, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.is_hovered = False
        self.is_selected = False
        
    def check_hover(self, mouse_pos):
        """Check if mouse is over button"""
        self.is_hovered = self.rect.collidepoint(mouse_pos) if mouse_pos else False
        return self.is_hovered
    
    def check_click(self, mouse_pos, mouse_pressed):
        """Check if button was clicked"""
        if mouse_pressed[0] and self.rect.collidepoint(mouse_pos):
            return True
        return False
    
    def draw(self, surface, custom_colors=None):
        """Draw button with selection/hover state"""
        is_active = self.is_selected or self.is_hovered
        
        # Default colors
        bg_color = UI_HIGHLIGHT if is_active else UI_BG
        border_color = WHITE if is_active else UI_BORDER
        text_color = BLACK if is_active else UI_TEXT
        border_width = 2 if is_active else 1
        
        # Apply custom colors if provided
        if custom_colors:
            bg_color = custom_colors.get('bg', bg_color)
            border_color = custom_colors.get('border', border_color)
            text_color = custom_colors.get('text', text_color)
        
        # Draw button
        pygame.draw.rect(surface, bg_color, self.rect, border_radius=5)
        pygame.draw.rect(surface, border_color, self.rect, border_width, border_radius=5)
        
        # Draw text
        text_surf = self.font.render(self.text, True, text_color)
        text_x = self.rect.x + self.rect.width // 2 - text_surf.get_width() // 2
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
            icon_color = (100, 255, 100)
        else:
            border_color = UI_BORDER
            text_color = UI_TEXT
            icon = "✓"
            icon_color = (100, 200, 100)
        
        # Draw box
        pygame.draw.rect(surface, UI_BG, self.rect, border_radius=8)
        pygame.draw.rect(surface, border_color, self.rect, 2, border_radius=8)
        
        # Highlight if active
        if is_active:
            fill_rect = pygame.Rect(self.rect.x + 2, self.rect.y + 2,
                                   self.rect.width - 4, self.rect.height - 4)
            fill_surface = pygame.Surface((fill_rect.width, fill_rect.height))
            fill_surface.set_alpha(30)
            fill_surface.fill(UI_HIGHLIGHT)
            surface.blit(fill_surface, (fill_rect.x, fill_rect.y))
        
        # Draw icon
        icon_surf = font_small.render(icon, True, icon_color)
        surface.blit(icon_surf, (self.rect.x + 15, self.rect.y + self.rect.height // 2 - 10))
        
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
    """Base class for reusable screen layouts"""
    
    def __init__(self, title, font_large, font_medium, font_small, font_tiny):
        self.title = title
        self.font_large = font_large
        self.font_medium = font_medium
        self.font_small = font_small
        self.font_tiny = font_tiny
        self.components = []
        
    def add_component(self, component):
        """Add a UI component to the screen"""
        self.components.append(component)
        
    def draw_title(self, surface, y=80):
        """Draw screen title"""
        title_surf = self.font_large.render(self.title, True, UI_HIGHLIGHT)
        title_x = SCREEN_WIDTH // 2 - title_surf.get_width() // 2
        surface.blit(title_surf, (title_x, y))
    
    def draw_subtitle(self, surface, text, y=140):
        """Draw subtitle text"""
        subtitle_surf = self.font_small.render(text, True, UI_TEXT_DIM)
        subtitle_x = SCREEN_WIDTH // 2 - subtitle_surf.get_width() // 2
        surface.blit(subtitle_surf, (subtitle_x, y))
    
    def draw_hint(self, surface, text, y=None):
        """Draw hint text at bottom of screen"""
        if y is None:
            y = SCREEN_HEIGHT - 60
        hint_surf = self.font_tiny.render(text, True, UI_TEXT_DIM)
        hint_x = SCREEN_WIDTH // 2 - hint_surf.get_width() // 2
        surface.blit(hint_surf, (hint_x, y))
    
    def draw_background(self, surface):
        """Draw screen background"""
        surface.fill(BLACK)


class LayoutHelper:
    """Helper for positioning UI elements"""
    
    @staticmethod
    def center_x(width):
        """Get X position to center element"""
        return SCREEN_WIDTH // 2 - width // 2
    
    @staticmethod
    def center_y(height):
        """Get Y position to center element"""
        return SCREEN_HEIGHT // 2 - height // 2
    
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
    """Reusable popup message overlay"""
    
    def __init__(self, message, duration=120, width=600, height=150):
        self.message = message
        self.duration = duration
        self.timer = duration
        self.width = width
        self.height = height
        self.active = True
        
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
        
        # Center position
        overlay_x = SCREEN_WIDTH // 2 - self.width // 2
        overlay_y = SCREEN_HEIGHT // 2 - self.height // 2
        
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
