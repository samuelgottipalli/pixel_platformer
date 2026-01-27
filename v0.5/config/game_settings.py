"""
Game Settings Manager
Handles video settings, audio settings, and controls configuration
Saves/loads settings to JSON file
"""

import json
import os
import pygame


class GameSettings:
    """Manages all game settings"""
    
    # Supported resolutions (width, height, scale_factor)
    RESOLUTIONS = [
        (1280, 720, 1.0, "1280x720 (Native)"),
        (1600, 900, 1.25, "1600x900"),
        (1920, 1080, 1.5, "1920x1080 (HD)"),
        (2560, 1440, 2.0, "2560x1440 (2K)"),
    ]
    
    # Default settings
    DEFAULTS = {
        'video': {
            'resolution_index': 0,  # 1280x720
            'fullscreen': False,
            'vsync': True,
        },
        'audio': {
            'music_enabled': True,
            'music_volume': 70,  # 0-100
            'sfx_enabled': True,
            'sfx_volume': 80,  # 0-100
        },
        'controls': {
            # Key bindings (future)
            'move_left': pygame.K_LEFT,
            'move_right': pygame.K_RIGHT,
            'jump': pygame.K_SPACE,
            'shoot': pygame.K_z,
            'melee': pygame.K_x,
        }
    }
    
    def __init__(self, settings_file='data/settings.json'):
        """Initialize settings manager"""
        self.settings_file = settings_file
        self.settings = self._load_settings()
        
        # Create display info
        self._update_display_info()
    
    def _load_settings(self):
        """Load settings from file or create defaults"""
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r') as f:
                    loaded = json.load(f)
                    # Merge with defaults (in case new settings added)
                    settings = self.DEFAULTS.copy()
                    for category in loaded:
                        if category in settings:
                            settings[category].update(loaded[category])
                    return settings
            except Exception as e:
                print(f"Error loading settings: {e}")
                return self.DEFAULTS.copy()
        else:
            # Create data directory if needed
            os.makedirs('data', exist_ok=True)
            return self.DEFAULTS.copy()
    
    def save_settings(self):
        """Save current settings to file"""
        try:
            os.makedirs('data', exist_ok=True)
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving settings: {e}")
            return False
    
    def _update_display_info(self):
        """Update display information based on current settings"""
        res_idx = self.settings['video']['resolution_index']
        if 0 <= res_idx < len(self.RESOLUTIONS):
            width, height, scale, name = self.RESOLUTIONS[res_idx]
            self.width = width
            self.height = height
            self.scale_factor = scale
            self.resolution_name = name
        else:
            # Fallback to native
            self.width = 1280
            self.height = 720
            self.scale_factor = 1.0
            self.resolution_name = "1280x720 (Native)"
    
    # ========================================================================
    # VIDEO SETTINGS
    # ========================================================================
    
    def get_resolution(self):
        """Get current resolution as (width, height)"""
        return (self.width, self.height)
    
    def get_scale_factor(self):
        """Get current UI scale factor"""
        return self.scale_factor
    
    def get_resolution_name(self):
        """Get current resolution display name"""
        return self.resolution_name
    
    def set_resolution(self, resolution_index):
        """Set resolution by index"""
        if 0 <= resolution_index < len(self.RESOLUTIONS):
            self.settings['video']['resolution_index'] = resolution_index
            self._update_display_info()
            return True
        return False
    
    def cycle_resolution(self, direction=1):
        """Cycle through resolutions. direction: 1=next, -1=previous"""
        current = self.settings['video']['resolution_index']
        new_index = (current + direction) % len(self.RESOLUTIONS)
        self.set_resolution(new_index)
        return new_index
    
    def get_fullscreen(self):
        """Check if fullscreen is enabled"""
        return self.settings['video']['fullscreen']
    
    def set_fullscreen(self, enabled):
        """Enable/disable fullscreen"""
        self.settings['video']['fullscreen'] = enabled
    
    def toggle_fullscreen(self):
        """Toggle fullscreen mode"""
        current = self.settings['video']['fullscreen']
        self.settings['video']['fullscreen'] = not current
        return self.settings['video']['fullscreen']
    
    def get_vsync(self):
        """Check if vsync is enabled"""
        return self.settings['video']['vsync']
    
    # ========================================================================
    # AUDIO SETTINGS
    # ========================================================================
    
    def get_music_enabled(self):
        """Check if music is enabled"""
        return self.settings['audio']['music_enabled']
    
    def set_music_enabled(self, enabled):
        """Enable/disable music"""
        self.settings['audio']['music_enabled'] = enabled
    
    def toggle_music(self):
        """Toggle music on/off"""
        current = self.settings['audio']['music_enabled']
        self.settings['audio']['music_enabled'] = not current
        return self.settings['audio']['music_enabled']
    
    def get_music_volume(self):
        """Get music volume (0-100)"""
        return self.settings['audio']['music_volume']
    
    def set_music_volume(self, volume):
        """Set music volume (0-100)"""
        self.settings['audio']['music_volume'] = max(0, min(100, volume))
    
    def get_sfx_enabled(self):
        """Check if sound effects are enabled"""
        return self.settings['audio']['sfx_enabled']
    
    def set_sfx_enabled(self, enabled):
        """Enable/disable sound effects"""
        self.settings['audio']['sfx_enabled'] = enabled
    
    def toggle_sfx(self):
        """Toggle sound effects on/off"""
        current = self.settings['audio']['sfx_enabled']
        self.settings['audio']['sfx_enabled'] = not current
        return self.settings['audio']['sfx_enabled']
    
    def get_sfx_volume(self):
        """Get sound effects volume (0-100)"""
        return self.settings['audio']['sfx_volume']
    
    def set_sfx_volume(self, volume):
        """Set sound effects volume (0-100)"""
        self.settings['audio']['sfx_volume'] = max(0, min(100, volume))
    
    # ========================================================================
    # PYGAME INTEGRATION
    # ========================================================================
    
    def apply_video_settings(self, screen):
        """Apply video settings to pygame display. Returns new screen surface."""
        flags = pygame.DOUBLEBUF
        
        if self.get_fullscreen():
            flags |= pygame.FULLSCREEN
        
        # Create new display with current settings
        new_screen = pygame.display.set_mode(
            (self.width, self.height),
            flags
        )
        
        return new_screen
    
    def get_display_flags(self):
        """Get pygame display flags based on settings"""
        flags = pygame.DOUBLEBUF
        
        if self.get_fullscreen():
            flags |= pygame.FULLSCREEN
        
        return flags
    
    # ========================================================================
    # UTILITY
    # ========================================================================
    
    def reset_to_defaults(self):
        """Reset all settings to defaults"""
        self.settings = self.DEFAULTS.copy()
        self._update_display_info()
        self.save_settings()
    
    def get_resolution_list(self):
        """Get list of available resolutions for display"""
        return [name for _, _, _, name in self.RESOLUTIONS]
    
    def __repr__(self):
        """String representation for debugging"""
        return f"GameSettings(res={self.resolution_name}, fullscreen={self.get_fullscreen()}, music={self.get_music_volume()}%, sfx={self.get_sfx_volume()}%)"
