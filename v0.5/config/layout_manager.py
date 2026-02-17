"""
Layout Manager - Resolution-Based Layout System
Loads layout configurations for different resolutions
"""

import json
import os


class LayoutManager:
    """Manages layout configurations for different resolutions"""
    
    _instance = None
    _current_layout = None
    _current_resolution = None
    
    def __new__(cls):
        """Singleton pattern - only one layout manager instance"""
        if cls._instance is None:
            cls._instance = super(LayoutManager, cls).__new__(cls)
        return cls._instance
    
    @classmethod
    def load_layout(cls, width, height):
        """
        Load layout configuration for given resolution
        
        Args:
            width: Screen width
            height: Screen height
            
        Returns:
            True if layout loaded successfully
        """
        # Check if already loaded
        if cls._current_resolution == (width, height):
            return True
        
        # Try to load exact match first
        layout_file = f"config/layouts/layout_{width}x{height}.json"
        
        if not os.path.exists(layout_file):
            # Fallback to base resolution
            print(f"Warning: Layout file {layout_file} not found, using 1280x720")
            layout_file = "config/layouts/layout_1280x720.json"
        
        try:
            with open(layout_file, 'r') as f:
                cls._current_layout = json.load(f)
                cls._current_resolution = (width, height)
                print(f"✓ Loaded layout: {width}x{height}")
                return True
        except Exception as e:
            print(f"Error loading layout: {e}")
            return False
    
    @classmethod
    def get(cls, *path):
        """
        Get value from layout configuration
        
        Args:
            *path: Nested keys to access (e.g., 'ui', 'main_menu', 'title_y')
            
        Returns:
            Value from layout config, or None if not found
            
        Example:
            LayoutManager.get('fonts', 'large')  # Returns font size
            LayoutManager.get('game_objects', 'player', 'width')  # Returns player width
        """
        # if cls._current_layout is None:
        #     # Auto-load default layout
        #     cls.load_layout(1280, 720)
        
        value = cls._current_layout
        for key in path:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                print(f"Warning: Layout path not found: {' -> '.join(path)}")
                return None
        
        return value
    
    @classmethod
    def get_screen_size(cls):
        """Get current screen dimensions"""
        return (
            cls.get('screen', 'width'),
            cls.get('screen', 'height')
        )

    @classmethod
    def get_font_size(cls, size_name):
        """
        Get font size for given name
        
        Args:
            size_name: 'large', 'medium', 'small', or 'tiny'
            
        Returns:
            Font size in pixels
        """
        return cls.get('fonts', size_name)

    @classmethod
    def get_object_size(cls, object_type):
        """
        Get size of game object
        
        Args:
            object_type: 'player', 'enemy', 'tile', etc.
            
        Returns:
            Dictionary with 'width' and 'height' (or 'size' for tiles)
        """
        return cls.get('game_objects', object_type)
    
    @classmethod
    def get_ui_element(cls, screen_name, element_name):
        """
        Get UI element configuration
        
        Args:
            screen_name: 'main_menu', 'pause_menu', 'hud', etc.
            element_name: Specific element within that screen
            
        Returns:
            Element configuration value
        """
        return cls.get('ui', screen_name, element_name)
    
    @classmethod
    def scale_position(cls, x, y):
        """
        Scale a position from base resolution to current resolution
        Used when loading level data or hardcoded positions
        
        Args:
            x, y: Position in base resolution (1280x720)
            
        Returns:
            (scaled_x, scaled_y) in current resolution
        """
        scale_factor = cls.get('resolution', 'scale_factor')
        if scale_factor is None:
            scale_factor = 1.0
        
        return (int(x * scale_factor), int(y * scale_factor))
    
    @classmethod
    def scale_dimension(cls, width, height=None):
        """
        Scale a dimension from base resolution to current resolution
        
        Args:
            width: Width (or size if height is None)
            height: Height (optional)
            
        Returns:
            Scaled (width, height) or just scaled width if height is None
        """
        scale_factor = cls.get('resolution', 'scale_factor')
        if scale_factor is None:
            scale_factor = 1.0
        
        if height is None:
            return int(width * scale_factor)
        else:
            return (int(width * scale_factor), int(height * scale_factor))
    
    @classmethod
    def get_scale_factor(cls):
        """Get current scale factor"""
        factor = cls.get('resolution', 'scale_factor')
        return factor if factor is not None else 1.0
    
    @classmethod
    def reload(cls):
        """Reload current layout (useful after resolution change)"""
        if cls._current_resolution:
            width, height = cls._current_resolution
            cls._current_layout = None
            cls._current_resolution = None
            return cls.load_layout(width, height)
        return False


# Convenience functions for global access
def get_layout(*path):
    """Shorthand for LayoutManager.get()"""
    return LayoutManager.get(*path)


def get_screen_size():
    """Shorthand for LayoutManager.get_screen_size()"""
    return LayoutManager.get_screen_size()

def get_scale_factor():
    """Shorthand for LayoutManager.get_scale_factor()"""
    return LayoutManager.get_scale_factor()


def get_font_size(size_name):
    """Shorthand for LayoutManager.get_font_size()"""
    return LayoutManager.get_font_size(size_name)


def get_object_size(object_type):
    """Shorthand for LayoutManager.get_object_size()"""
    return LayoutManager.get_object_size(object_type)


def get_ui_element(screen_name, element_name):
    """Shorthand for LayoutManager.get_ui_element()"""
    return LayoutManager.get_ui_element(screen_name, element_name)
