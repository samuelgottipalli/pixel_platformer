"""
Audio Manager - Sprint 2
Handles all music and sound effects with volume control
Integrates with game settings
"""

import os
import pygame


class AudioManager:
    """Manages all game audio (music and sound effects)"""

    def __init__(self, settings):
        """Initialize audio system"""
        self.settings = settings

        # Initialize pygame mixer
        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            self.audio_available = True
        except:
            print("Audio system not available")
            self.audio_available = False
            return

        # Music tracks
        self.music_tracks = {
            'menu': None,
            'level': None,
            'boss': None,
            'victory': None,
            'game_over': None,
        }

        # Sound effects
        self.sound_effects = {
            'jump': None,
            'double_jump': None,
            'shoot': None,
            'melee': None,
            'enemy_hit': None,
            'enemy_death': None,
            'player_hurt': None,
            'coin': None,
            'powerup': None,
            'key': None,
            'portal': None,
            'menu_select': None,
            'menu_navigate': None,
            'boss_hit': None,
            'explosion': None,
        }

        # Current music track
        self.current_music = None
        self.music_fadein_ms = 1000  # 1 second fade in

        # Load audio files
        self._load_audio_files()

        # Apply initial settings
        self.update_volumes()

    def _load_audio_files(self):
        """Load all audio files from assets/audio directory"""
        if not self.audio_available:
            return

        # Create audio directory if it doesn't exist
        os.makedirs('assets/audio/music', exist_ok=True)
        os.makedirs('assets/audio/sfx', exist_ok=True)

        # Try to load music files
        music_files = {
            "menu": "assets/audio/music/menu_theme.ogg",
            "level": "assets/audio/music/level_theme.ogg",
            "boss": "assets/audio/music/boss_theme.ogg",
            "victory": "assets/audio/music/victory_theme.ogg",
            "game_over": "assets/audio/music/game_over_theme.ogg",
        }

        for track_name, filepath in music_files.items():
            if os.path.exists(filepath):
                self.music_tracks[track_name] = filepath

        # Try to load sound effect files
        sfx_files = {
            'jump': 'assets/audio/sfx/jump.wav',
            'double_jump': 'assets/audio/sfx/double_jump.wav',
            'shoot': 'assets/audio/sfx/shoot.wav',
            'melee': 'assets/audio/sfx/melee.wav',
            'enemy_hit': 'assets/audio/sfx/enemy_hit.wav',
            'enemy_death': 'assets/audio/sfx/enemy_death.wav',
            'player_hurt': 'assets/audio/sfx/player_hurt.wav',
            'player_die': 'assets/audio/sfx/player_die.wav',
            'player_heal': 'assets/audio/sfx/player_heal.wav',
            'coin': 'assets/audio/sfx/coin.wav',
            'powerup': 'assets/audio/sfx/powerup.wav',
            'key': 'assets/audio/sfx/key.wav',
            'portal': 'assets/audio/sfx/portal.wav',
            'menu_select': 'assets/audio/sfx/menu_select.wav',
            'menu_navigate': 'assets/audio/sfx/menu_navigate.wav',
            'boss_hit': 'assets/audio/sfx/boss_hit.wav',
            'explosion': 'assets/audio/sfx/explosion.wav',
        }

        for sfx_name, filepath in sfx_files.items():
            if os.path.exists(filepath):
                try:
                    self.sound_effects[sfx_name] = pygame.mixer.Sound(filepath)
                except:
                    print(f"Failed to load sound: {filepath}")

    # ========================================================================
    # MUSIC CONTROL
    # ========================================================================

    def play_music(self, track_name, loop=True, fadein=True):
        """Play music track"""
        if not self.audio_available:
            return

        if not self.settings.get_music_enabled():
            return

        # Don't restart if already playing
        if self.current_music == track_name and pygame.mixer.music.get_busy():
            return

        # Get track path
        track_path = self.music_tracks.get(track_name)
        if not track_path or not os.path.exists(track_path):
            return

        try:
            # Stop current music
            pygame.mixer.music.stop()

            # Load and play new track
            pygame.mixer.music.load(track_path)

            loops = -1 if loop else 0
            if fadein:
                pygame.mixer.music.play(loops, fade_ms=self.music_fadein_ms)
            else:
                pygame.mixer.music.play(loops)

            self.current_music = track_name

            # Set volume
            self.update_music_volume()

        except Exception as e:
            print(f"Failed to play music {track_name}: {e}")

    def stop_music(self, fadeout_ms=1000):
        """Stop current music"""
        if not self.audio_available:
            return

        try:
            pygame.mixer.music.fadeout(fadeout_ms)
            self.current_music = None
        except:
            pass

    def pause_music(self):
        """Pause current music"""
        if not self.audio_available:
            return

        try:
            pygame.mixer.music.pause()
        except:
            pass

    def unpause_music(self):
        """Resume paused music"""
        if not self.audio_available:
            return

        try:
            pygame.mixer.music.unpause()
        except:
            pass

    def update_music_volume(self):
        """Update music volume from settings"""
        if not self.audio_available:
            return

        if self.settings.get_music_enabled():
            volume = self.settings.get_music_volume() / 100.0
            pygame.mixer.music.set_volume(volume)
        else:
            pygame.mixer.music.set_volume(0.0)

    # ========================================================================
    # SOUND EFFECTS
    # ========================================================================

    def play_sfx(self, sfx_name):
        """Play sound effect"""
        if not self.audio_available:
            return

        if not self.settings.get_sfx_enabled():
            return

        sound = self.sound_effects.get(sfx_name)
        if sound:
            try:
                # Set volume
                volume = self.settings.get_sfx_volume() / 100.0
                sound.set_volume(volume)
                sound.play()
            except Exception as e:
                print(f"Failed to play sound {sfx_name}: {e}")

    def update_sfx_volume(self):
        """Update all sound effect volumes"""
        if not self.audio_available:
            return

        volume = self.settings.get_sfx_volume() / 100.0 if self.settings.get_sfx_enabled() else 0.0

        for sound in self.sound_effects.values():
            if sound:
                sound.set_volume(volume)

    # ========================================================================
    # SETTINGS INTEGRATION
    # ========================================================================

    def update_volumes(self):
        """Update all volumes from settings"""
        self.update_music_volume()
        self.update_sfx_volume()

    def toggle_music(self):
        """Toggle music on/off"""
        enabled = self.settings.toggle_music()
        if enabled and self.current_music:
            self.update_music_volume()
        else:
            pygame.mixer.music.set_volume(0.0)
        return enabled

    def toggle_sfx(self):
        """Toggle sound effects on/off"""
        enabled = self.settings.toggle_sfx()
        self.update_sfx_volume()
        return enabled

    # ========================================================================
    # CONVENIENCE METHODS
    # ========================================================================

    def play_menu_music(self):
        """Play menu background music"""
        self.play_music('menu', loop=True)

    def play_level_music(self):
        """Play level background music"""
        self.play_music('level', loop=True)

    def play_boss_music(self):
        """Play boss battle music"""
        self.play_music('boss', loop=True)

    def play_victory_music(self):
        """Play victory music"""
        self.play_music('victory', loop=False)

    def play_game_over_music(self):
        """Play game over music"""
        self.play_music('game_over', loop=False)

    # Menu sounds
    def menu_navigate(self):
        """Play menu navigation sound"""
        self.play_sfx('menu_navigate')

    def menu_select(self):
        """Play menu selection sound"""
        self.play_sfx('menu_select')

    # Player sounds
    def player_jump(self):
        """Play jump sound"""
        self.play_sfx('jump')

    def player_double_jump(self):
        """Play double jump sound"""
        self.play_sfx('double_jump')

    def player_shoot(self):
        """Play shoot sound"""
        self.play_sfx('shoot')

    def player_melee(self):
        """Play melee attack sound"""
        self.play_sfx('melee')

    def player_hurt(self):
        """Play player damage sound"""
        self.play_sfx('player_hurt')

    def player_die(self):
        """Play player death sound"""
        self.play_sfx('player_die')
    
    def player_heal(self):
        """Play player healing sound"""
        self.play_sfx('player_heal')

    # Collectible sounds
    def collect_coin(self):
        """Play coin collection sound"""
        self.play_sfx('coin')

    def collect_powerup(self):
        """Play powerup collection sound"""
        self.play_sfx('powerup')

    def collect_key(self):
        """Play key collection sound"""
        self.play_sfx('key')

    # Enemy sounds
    def enemy_hit(self):
        """Play enemy hit sound"""
        self.play_sfx('enemy_hit')

    def enemy_death(self):
        """Play enemy death sound"""
        self.play_sfx('enemy_death')

    # Boss sounds
    def boss_hit(self):
        """Play boss hit sound"""
        self.play_sfx('boss_hit')

    # Other sounds
    def portal_enter(self):
        """Play portal sound"""
        self.play_sfx('portal')

    def explosion(self):
        """Play explosion sound"""
        self.play_sfx('explosion')

    # ========================================================================
    # CLEANUP
    # ========================================================================

    def cleanup(self):
        """Clean up audio resources"""
        if self.audio_available:
            pygame.mixer.music.stop()
            pygame.mixer.quit()
