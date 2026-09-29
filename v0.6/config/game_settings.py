"""
Game Settings Manager
Handles video settings, audio settings, and controls configuration
Saves/loads settings to JSON file
"""

import copy
import json
import os
import pygame

# The game always renders at this size; the window (or fullscreen) is a
# scaled view of it. Mouse positions are mapped back automatically.
LOGICAL_WIDTH, LOGICAL_HEIGHT = 1280, 720


class GameSettings:
    """Manages all game settings"""

    # Window sizes offered in Settings (width, height, scale_factor, name).
    # The game itself always renders at 1280x720 and is scaled to the window.
    RESOLUTIONS = [
        (1280, 720, 1.0, "1280x720"),
        (1600, 900, 1.25, "1600x900"),
        (1920, 1080, 1.5, "1920x1080 (HD)"),
        (2560, 1440, 2.0, "2560x1440 (2K)"),
    ]

    # Default settings
    DEFAULTS = {
        "video": {
            "resolution_index": 0,  # 1280x720
            "fullscreen": False,
            "vsync": True,
        },
        "audio": {
            "music_enabled": True,
            "music_volume": 70,  # 0-100
            "sfx_enabled": True,
            "sfx_volume": 80,  # 0-100
        },
        "accessibility": {
            "colorblind_mode": False,  # Default OFF for accessibility
        },
        "controls": {
            # Key bindings (future)
            "move_left": pygame.K_LEFT,
            "move_right": pygame.K_RIGHT,
            "jump": pygame.K_SPACE,
            "shoot": pygame.K_z,
            "melee": pygame.K_x,
        },
    }

    def __init__(self, settings_file="data/settings.json"):
        """Initialize settings manager"""
        self.settings_file = settings_file

        # Detect native resolution
        self._detect_native_resolution()

        # Build resolution list with native highlighted
        self.RESOLUTIONS = self._build_resolution_list()

        # Load settings
        self.settings = self._load_settings()

        # Create display info
        self._update_display_info()
        self._resolution_changed = False

    def _detect_native_resolution(self):
        """Detect native screen resolution"""
        try:
            display_info = pygame.display.Info()
            self.native_width = display_info.current_w
            self.native_height = display_info.current_h
        except:
            self.native_width = 1920
            self.native_height = 1080

    def _build_resolution_list(self):
        """Build resolution list with native resolution highlighted"""
        resolutions = []
        native_found = False

        for width, height, scale, name in self.RESOLUTIONS:
            if width == self.native_width and height == self.native_height:
                name = f"{name} (Native)"
                native_found = True

            resolutions.append((width, height, scale, name))

        # If native not in list, add it
        if not native_found:
            scale = self.native_height / 720.0
            name = f"{self.native_width}x{self.native_height} (Native)"

            inserted = False
            for i, (w, h, s, n) in enumerate(resolutions):
                if self.native_width < w:
                    resolutions.insert(
                        i, (self.native_width, self.native_height, scale, name)
                    )
                    inserted = True
                    break

            if not inserted:
                resolutions.append((self.native_width, self.native_height, scale, name))

        return resolutions

    def get_native_resolution_index(self):
        """Get index of native resolution in list"""
        for i, (w, h, scale, name) in enumerate(self.RESOLUTIONS):
            if w == self.native_width and h == self.native_height:
                return i
        return 0

    def _load_settings(self):
        """Load settings from file or create defaults"""
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, "r") as f:
                    loaded = json.load(f)
                    # Merge with defaults (in case new settings added)
                    settings = copy.deepcopy(self.DEFAULTS)
                    for category in loaded:
                        if category in settings:
                            settings[category].update(loaded[category])
                    return settings
            except Exception as e:
                print(f"Error loading settings: {e}")
                return copy.deepcopy(self.DEFAULTS)
        else:
            # Create data directory if needed
            os.makedirs('data', exist_ok=True)
            return copy.deepcopy(self.DEFAULTS)

    def save_settings(self):
        """Save current settings to file"""
        try:
            os.makedirs("data", exist_ok=True)
            with open(self.settings_file, "w") as f:
                json.dump(self.settings, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving settings: {e}")
            return False

    def _update_display_info(self):
        """Update display information based on current settings"""
        res_idx = self.settings["video"]["resolution_index"]
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
            old_index = self.settings["video"]["resolution_index"]
            self.settings["video"]["resolution_index"] = resolution_index
            self._update_display_info()

            # Flag that resolution changed (requires restart)
            if old_index != resolution_index:
                self._resolution_changed = True

            return True
        return False

    def cycle_resolution(self, direction=1):
        """Cycle through resolutions"""
        current = self.settings["video"]["resolution_index"]
        new_index = (current + direction) % len(self.RESOLUTIONS)
        self.set_resolution(new_index)
        return new_index

    def get_fullscreen(self):
        """Check if fullscreen is enabled"""
        return self.settings["video"]["fullscreen"]

    def set_fullscreen(self, enabled):
        """Enable/disable fullscreen"""
        self.settings["video"]["fullscreen"] = enabled

    def toggle_fullscreen(self):
        """Toggle fullscreen mode"""
        current = self.settings["video"]["fullscreen"]
        self.settings["video"]["fullscreen"] = not current
        return self.settings["video"]["fullscreen"]

    def get_vsync(self):
        """Check if vsync is enabled"""
        return self.settings["video"]["vsync"]

    # ========================================================================
    # AUDIO SETTINGS
    # ========================================================================

    def get_music_enabled(self):
        """Check if music is enabled"""
        return self.settings["audio"]["music_enabled"]

    def set_music_enabled(self, enabled):
        """Enable/disable music"""
        self.settings["audio"]["music_enabled"] = enabled

    def toggle_music(self):
        """Toggle music on/off"""
        current = self.settings["audio"]["music_enabled"]
        self.settings["audio"]["music_enabled"] = not current
        return self.settings["audio"]["music_enabled"]

    def get_music_volume(self):
        """Get music volume (0-100)"""
        return self.settings["audio"]["music_volume"]

    def set_music_volume(self, volume):
        """Set music volume (0-100)"""
        self.settings["audio"]["music_volume"] = max(0, min(100, volume))

    def get_sfx_enabled(self):
        """Check if sound effects are enabled"""
        return self.settings["audio"]["sfx_enabled"]

    def set_sfx_enabled(self, enabled):
        """Enable/disable sound effects"""
        self.settings["audio"]["sfx_enabled"] = enabled

    def toggle_sfx(self):
        """Toggle sound effects on/off"""
        current = self.settings["audio"]["sfx_enabled"]
        self.settings["audio"]["sfx_enabled"] = not current
        return self.settings["audio"]["sfx_enabled"]

    def get_sfx_volume(self):
        """Get sound effects volume (0-100)"""
        return self.settings["audio"]["sfx_volume"]

    def set_sfx_volume(self, volume):
        """Set sound effects volume (0-100)"""
        self.settings["audio"]["sfx_volume"] = max(0, min(100, volume))

    # ========================================================================
    # PYGAME INTEGRATION
    # ========================================================================

    def create_display(self):
        """
        Create the game display once: a 1280x720 surface that SDL scales to
        the window (or the whole screen in fullscreen). Call once at startup;
        later changes go through apply_video_settings().
        """
        # Smooth (linear) scaling so text stays readable at non-2x sizes
        os.environ.setdefault("SDL_RENDER_SCALE_QUALITY", "1")
        flags = pygame.SCALED | pygame.RESIZABLE
        if self.get_fullscreen():
            flags |= pygame.FULLSCREEN
        try:
            screen = pygame.display.set_mode((LOGICAL_WIDTH, LOGICAL_HEIGHT), flags)
            self._scaled = True
        except pygame.error:
            # No GPU renderer available (e.g. headless tests): plain 1280x720
            # window. Resizing it would resize the drawing surface, so don't.
            screen = pygame.display.set_mode((LOGICAL_WIDTH, LOGICAL_HEIGHT))
            self._scaled = False
        self._apply_window_size()
        return screen

    def apply_video_settings(self, screen=None):
        """Apply fullscreen and window-size settings to the existing display"""
        if getattr(self, "_scaled", False) and pygame.display.is_fullscreen() != self.get_fullscreen():
            pygame.display.toggle_fullscreen()
        self._apply_window_size()
        return pygame.display.get_surface()

    def _apply_window_size(self):
        """
        Size and center the window for the selected resolution. The window is
        shrunk (keeping 16:9) if it would not fit on screen with its title bar
        and the taskbar visible.
        """
        if self.get_fullscreen() or not getattr(self, "_scaled", False):
            return
        try:
            from pygame._sdl2 import video
            window = video.Window.from_display_module()
        except Exception:
            return  # Older pygame / headless: keep the default window
        max_w, max_h = self._usable_screen_area()
        fit = min(1.0, max_w / self.width, max_h / self.height)
        window.size = (int(self.width * fit), int(self.height * fit))
        window.position = video.WINDOWPOS_CENTERED

    @staticmethod
    def _usable_screen_area():
        """Largest window client area that fits with the title bar and taskbar showing"""
        title_bar, border = 40, 16
        try:
            import ctypes
            from ctypes import wintypes

            rect = wintypes.RECT()
            SPI_GETWORKAREA = 0x0030
            if ctypes.windll.user32.SystemParametersInfoW(SPI_GETWORKAREA, 0, ctypes.byref(rect), 0):
                return rect.right - rect.left - border, rect.bottom - rect.top - title_bar - border
        except (AttributeError, OSError):
            pass  # Not Windows
        try:
            width, height = pygame.display.get_desktop_sizes()[0]
        except (pygame.error, IndexError):
            width, height = 1920, 1080
        return width - border, height - 80 - title_bar

    def get_display_flags(self):
        """Get pygame display flags based on settings"""
        flags = pygame.SCALED | pygame.RESIZABLE
        if self.get_fullscreen():
            flags |= pygame.FULLSCREEN
        return flags

    # ========================================================================
    # UTILITY
    # ========================================================================

    def reset_to_defaults(self):
        """Reset all settings to defaults"""
        self.settings = copy.deepcopy(self.DEFAULTS)
        self._update_display_info()
        self.save_settings()

    def get_resolution_list(self):
        """Get list of available resolutions for display"""
        return [name for _, _, _, name in self.RESOLUTIONS]

    def clear_resolution_changed_flag(self):
        """Clear resolution changed flag"""
        self._resolution_changed = False

    # ========================================================================
    # ACCESSIBILITY SETTINGS
    # ========================================================================


    def get_colorblind_mode(self):
        """Check if colorblind mode is enabled"""
        return self.settings["accessibility"]["colorblind_mode"]

    def set_colorblind_mode(self, enabled):
        """Enable/disable colorblind mode"""
        self.settings["accessibility"]["colorblind_mode"] = enabled

    def toggle_colorblind_mode(self):
        """Toggle colorblind mode on/off"""
        current = self.settings["accessibility"]["colorblind_mode"]
        self.settings["accessibility"]["colorblind_mode"] = not current
        return self.settings["accessibility"]["colorblind_mode"]

    def __repr__(self):
        """String representation for debugging"""
        return f"GameSettings(res={self.resolution_name}, fullscreen={self.get_fullscreen()}, music={self.get_music_volume()}%, sfx={self.get_sfx_volume()}%)"
