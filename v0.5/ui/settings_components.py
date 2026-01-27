"""
Settings UI Components
Sliders, toggles, and dropdowns for settings screen
"""

import pygame
from config.settings import UI_BG, UI_BORDER, UI_HIGHLIGHT, UI_TEXT, UI_TEXT_DIM, WHITE, BLACK


class Slider:
    """Horizontal slider for volume/value adjustment"""
    
    def __init__(self, x, y, width, min_value=0, max_value=100, current_value=50, label=""):
        self.rect = pygame.Rect(x, y, width, 20)
        self.min_value = min_value
        self.max_value = max_value
        self.current_value = current_value
        self.label = label
        self.dragging = False
        self.is_hovered = False
        
        # Slider dimensions
        self.track_height = 6
        self.handle_width = 16
        self.handle_height = 20
    
    def get_value(self):
        """Get current slider value"""
        return self.current_value
    
    def set_value(self, value):
        """Set slider value"""
        self.current_value = max(self.min_value, min(self.max_value, value))
    
    def _get_handle_x(self):
        """Calculate handle X position based on current value"""
        value_range = self.max_value - self.min_value
        if value_range == 0:
            return self.rect.x
        
        ratio = (self.current_value - self.min_value) / value_range
        return self.rect.x + int(ratio * (self.rect.width - self.handle_width))
    
    def _get_handle_rect(self):
        """Get handle rectangle"""
        handle_x = self._get_handle_x()
        handle_y = self.rect.y + (self.track_height - self.handle_height) // 2
        return pygame.Rect(handle_x, handle_y, self.handle_width, self.handle_height)
    
    def check_hover(self, mouse_pos):
        """Check if mouse is over slider"""
        if mouse_pos:
            handle_rect = self._get_handle_rect()
            self.is_hovered = handle_rect.collidepoint(mouse_pos)
            return self.is_hovered
        return False
    
    def start_drag(self, mouse_pos):
        """Start dragging slider"""
        if mouse_pos:
            handle_rect = self._get_handle_rect()
            if handle_rect.collidepoint(mouse_pos):
                self.dragging = True
                return True
        return False
    
    def update_drag(self, mouse_pos):
        """Update slider value during drag"""
        if self.dragging and mouse_pos:
            # Calculate new value based on mouse X position
            relative_x = mouse_pos[0] - self.rect.x
            ratio = relative_x / self.rect.width
            ratio = max(0.0, min(1.0, ratio))
            
            value_range = self.max_value - self.min_value
            new_value = self.min_value + int(ratio * value_range)
            self.current_value = max(self.min_value, min(self.max_value, new_value))
    
    def stop_drag(self):
        """Stop dragging slider"""
        self.dragging = False
    
    def draw(self, surface, font):
        """Draw slider"""
        # Track
        track_y = self.rect.y + (20 - self.track_height) // 2
        track_rect = pygame.Rect(self.rect.x, track_y, self.rect.width, self.track_height)
        pygame.draw.rect(surface, UI_BG, track_rect, border_radius=3)
        pygame.draw.rect(surface, UI_BORDER, track_rect, 1, border_radius=3)
        
        # Filled portion
        handle_x = self._get_handle_x()
        filled_width = handle_x - self.rect.x + self.handle_width // 2
        if filled_width > 0:
            filled_rect = pygame.Rect(self.rect.x, track_y, filled_width, self.track_height)
            pygame.draw.rect(surface, UI_HIGHLIGHT, filled_rect, border_radius=3)
        
        # Handle
        handle_rect = self._get_handle_rect()
        handle_color = WHITE if self.is_hovered or self.dragging else UI_BORDER
        pygame.draw.rect(surface, handle_color, handle_rect, border_radius=4)
        pygame.draw.rect(surface, UI_TEXT, handle_rect, 2, border_radius=4)
        
        # Value text
        value_text = font.render(f"{self.current_value}%", True, UI_TEXT)
        text_x = self.rect.x + self.rect.width + 10
        text_y = self.rect.y
        surface.blit(value_text, (text_x, text_y))


class Toggle:
    """Toggle switch for on/off settings"""
    
    def __init__(self, x, y, width=60, height=30, enabled=True, label=""):
        self.rect = pygame.Rect(x, y, width, height)
        self.enabled = enabled
        self.label = label
        self.is_hovered = False
    
    def is_enabled(self):
        """Check if toggle is enabled"""
        return self.enabled
    
    def set_enabled(self, enabled):
        """Set toggle state"""
        self.enabled = enabled
    
    def toggle(self):
        """Toggle on/off"""
        self.enabled = not self.enabled
        return self.enabled
    
    def check_hover(self, mouse_pos):
        """Check if mouse is over toggle"""
        if mouse_pos:
            self.is_hovered = self.rect.collidepoint(mouse_pos)
            return self.is_hovered
        return False
    
    def check_click(self, mouse_pos, mouse_pressed):
        """Check if toggle was clicked"""
        if mouse_pressed[0] and mouse_pos:
            if self.rect.collidepoint(mouse_pos):
                self.toggle()
                return True
        return False
    
    def draw(self, surface, font):
        """Draw toggle switch"""
        # Background
        bg_color = UI_HIGHLIGHT if self.enabled else UI_BG
        border_color = WHITE if self.is_hovered else UI_BORDER
        
        pygame.draw.rect(surface, bg_color, self.rect, border_radius=15)
        pygame.draw.rect(surface, border_color, self.rect, 2, border_radius=15)
        
        # Switch knob
        knob_radius = self.rect.height // 2 - 4
        if self.enabled:
            knob_x = self.rect.right - knob_radius - 6
        else:
            knob_x = self.rect.left + knob_radius + 6
        
        knob_y = self.rect.centery
        knob_color = WHITE if self.enabled else UI_TEXT_DIM
        
        pygame.draw.circle(surface, knob_color, (knob_x, knob_y), knob_radius)
        pygame.draw.circle(surface, UI_TEXT, (knob_x, knob_y), knob_radius, 2)
        
        # State text
        state_text = "ON" if self.enabled else "OFF"
        text_surf = font.render(state_text, True, UI_TEXT)
        text_x = self.rect.x + self.rect.width + 10
        text_y = self.rect.y + self.rect.height // 2 - text_surf.get_height() // 2
        surface.blit(text_surf, (text_x, text_y))


class Dropdown:
    """Dropdown menu for selecting options"""
    
    def __init__(self, x, y, width, height, options, selected_index=0, label=""):
        self.rect = pygame.Rect(x, y, width, height)
        self.options = options
        self.selected_index = selected_index
        self.label = label
        self.is_hovered = False
        self.is_open = False
        self.hover_index = -1
    
    def get_selected(self):
        """Get selected option text"""
        if 0 <= self.selected_index < len(self.options):
            return self.options[self.selected_index]
        return ""
    
    def get_selected_index(self):
        """Get selected option index"""
        return self.selected_index
    
    def set_selected(self, index):
        """Set selected option by index"""
        if 0 <= index < len(self.options):
            self.selected_index = index
    
    def check_hover(self, mouse_pos):
        """Check if mouse is over dropdown"""
        if mouse_pos:
            self.is_hovered = self.rect.collidepoint(mouse_pos)
            
            # Check hover on dropdown items if open
            if self.is_open:
                for i in range(len(self.options)):
                    item_y = self.rect.y + self.rect.height + i * self.rect.height
                    item_rect = pygame.Rect(self.rect.x, item_y, self.rect.width, self.rect.height)
                    if item_rect.collidepoint(mouse_pos):
                        self.hover_index = i
                        return True
                self.hover_index = -1
            
            return self.is_hovered
        return False
    
    def check_click(self, mouse_pos, mouse_pressed):
        """Check if dropdown was clicked"""
        if mouse_pressed[0] and mouse_pos:
            # Click on main button
            if self.rect.collidepoint(mouse_pos):
                self.is_open = not self.is_open
                return True
            
            # Click on dropdown item
            if self.is_open:
                for i in range(len(self.options)):
                    item_y = self.rect.y + self.rect.height + i * self.rect.height
                    item_rect = pygame.Rect(self.rect.x, item_y, self.rect.width, self.rect.height)
                    if item_rect.collidepoint(mouse_pos):
                        self.selected_index = i
                        self.is_open = False
                        return True
        
        return False
    
    def cycle(self, direction=1):
        """Cycle through options. direction: 1=next, -1=previous"""
        self.selected_index = (self.selected_index + direction) % len(self.options)
        return self.selected_index
    
    def draw(self, surface, font):
        """Draw dropdown menu"""
        # Main button
        bg_color = UI_HIGHLIGHT if self.is_hovered else UI_BG
        border_color = WHITE if self.is_hovered else UI_BORDER
        
        pygame.draw.rect(surface, bg_color, self.rect, border_radius=5)
        pygame.draw.rect(surface, border_color, self.rect, 2, border_radius=5)
        
        # Selected text
        selected_text = self.get_selected()
        text_surf = font.render(selected_text, True, UI_TEXT if not self.is_hovered else BLACK)
        text_x = self.rect.x + 10
        text_y = self.rect.y + self.rect.height // 2 - text_surf.get_height() // 2
        surface.blit(text_surf, (text_x, text_y))
        
        # Arrow indicator
        arrow = "▼" if not self.is_open else "▲"
        arrow_surf = font.render(arrow, True, UI_TEXT if not self.is_hovered else BLACK)
        arrow_x = self.rect.right - arrow_surf.get_width() - 10
        arrow_y = self.rect.y + self.rect.height // 2 - arrow_surf.get_height() // 2
        surface.blit(arrow_surf, (arrow_x, arrow_y))
        
        # Dropdown items (if open)
        if self.is_open:
            for i, option in enumerate(self.options):
                item_y = self.rect.y + self.rect.height + i * self.rect.height
                item_rect = pygame.Rect(self.rect.x, item_y, self.rect.width, self.rect.height)
                
                # Highlight hovered item
                is_hovered = (i == self.hover_index)
                item_bg = UI_HIGHLIGHT if is_hovered else UI_BG
                item_text_color = BLACK if is_hovered else UI_TEXT
                
                pygame.draw.rect(surface, item_bg, item_rect)
                pygame.draw.rect(surface, UI_BORDER, item_rect, 1)
                
                # Option text
                option_surf = font.render(option, True, item_text_color)
                option_x = item_rect.x + 10
                option_y = item_rect.y + item_rect.height // 2 - option_surf.get_height() // 2
                surface.blit(option_surf, (option_x, option_y))
