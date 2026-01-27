"""
Main game class - handles game loop and state management
"""

import random

import pygame

from config import controls
from config.game_settings import GameSettings
from config.settings import (
    CYAN,
    FPS,
    SCORE_COIN,
    SCORE_ENEMY_HIT,
    SCORE_ENEMY_KILL,
    SCORE_KEY,
    SCORE_MELEE_HIT,
    SCORE_POWERUP,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    WHITE,
    YELLOW,
)
from core.camera import Camera
from entities.boss import Boss
from entities.boss_attacks import BossAttackEffect, BossAttackManager
from entities.particle import Particle
from entities.player import Player
from entities.projectile import Projectile
from levels.level import Level
from levels.level_loader import LevelLoader
from save_system.difficulty_completion_tracker import DifficultyCompletionTracker
from save_system.profile_manager import PlayerProfile, ProfileManager
from save_system.save_manager import SaveManager
from ui.hud import HUD
from ui.menu import Menu
from ui.components import Popup
from utils.enums import GameState


class Game:
    """Main game class"""

    def __init__(self):
        """Initialize game"""
        pygame.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Retro Pixel Platformer")
        self.clock = pygame.time.Clock()
        self.running = True

        # Game settings
        self.settings = GameSettings()

        # On first run, suggest native resolution
        if not os.path.exists("data/settings.json"):
            native_idx = self.settings.get_native_resolution_index()
            self.settings.set_resolution(native_idx)
            self.settings.save_settings()

        # Apply video settings at startup
        self.screen = self.settings.apply_video_settings(self.screen)

        # Track if settings changed (needs restart)
        self.settings_changed = False

        # Fonts
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)

        # UI
        self.menu = Menu(self.font_large, self.font_medium, self.font_small)
        self.hud = HUD(self.font_small)
        self.popup = None

        # Game state - START AT PROFILE SELECT
        self.state = GameState.PROFILE_SELECT

        # Menu selections
        self.menu_selection = 0  # Main menu selection (0=New Game, 1=Continue, 2=Level Map, 3=Options, 4=Quit)
        self.options_selection = (
            0  # Options menu (0=Controls, 1=Settings, 2=Credits, 3=Back)
        )
        self.pause_selection = 0
        self.profile_selection = 0
        self.level_selection = 0  # For level select screen
        self.player_name = ""
        self.char_selection = 0

        # Profile management
        self.profiles = ProfileManager.load_profiles()
        self.current_profile = None  # Selected profile
        self.profile_action = None  # 'new' or 'load'

        self.player = None
        self.current_level_index = 0
        self.level = None
        self.camera = Camera()
        self.difficulty = "NORMAL"  # EASY, NORMAL, HARD
        self.difficulty_selection = 1  # Default to Normal (0=Easy, 1=Normal, 2=Hard)
        self.difficulty_manager = None

        # Load levels
        self.levels = LevelLoader.create_default_levels()

        # Game objects
        self.projectiles = []
        self.particles = []

        # Input state tracking
        self.jump_pressed = False
        self.pause_pressed = False

        # Debug mode
        self.debug_mode = False
        self.debug_toggle_pressed = False

        # Mouse position
        self.mouse_pos = pygame.mouse.get_pos()

        # Boss system
        self.boss = None
        self.boss_projectiles = []
        self.boss_effects = []
        self.boss_defeated = False

        # UI enhancements
        self.show_controls = False
        self.controls_toggle_pressed = False

        # Popup message system
        self.show_popup = False
        self.popup_message = ""
        self.popup_timer = 0

        # Store current screen for back/options button detection
        self.current_screen = None
        self.previous_state = None  # For returning from options

    def run(self):
        """Main game loop"""
        while self.running:
            self._handle_events()
            self._update()
            self._draw()
            self.clock.tick(FPS)

        pygame.quit()

    def _show_popup(self, message, duration=120):
        """Show popup using Popup component"""
        from ui.components import Popup

        self.popup = Popup(message, duration)

    def _handle_mouse_click(self):
        """Handle mouse clicks on buttons"""
        mouse_pressed = pygame.mouse.get_pressed()
        if not mouse_pressed[0]:  # Left click
            return

        # Check back/options buttons on current screen FIRST
        if self.current_screen:
            if hasattr(self.current_screen, "check_back_click"):
                if self.current_screen.check_back_click(self.mouse_pos, mouse_pressed):
                    self._handle_back_button()
                    return

            if hasattr(self.current_screen, "check_options_click"):
                if self.current_screen.check_options_click(
                    self.mouse_pos, mouse_pressed
                ):
                    self._handle_options_button()
                    return

        # Check pause menu options button
        if self.state == GameState.PAUSED and self.current_screen:
            if hasattr(self.current_screen, "check_click"):
                if self.current_screen.check_click(self.mouse_pos, mouse_pressed):
                    self.previous_state = GameState.PLAYING
                    self.state = GameState.OPTIONS
                    self.options_selection = 0
                    return

        if self.state == GameState.PROFILE_SELECT:
            # Check profile boxes
            if self.profiles:
                y_start = 160
                for i in range(len(self.profiles)):
                    y = y_start + i * 70
                    box_width = 500
                    box_height = 60
                    box_x = SCREEN_WIDTH // 2 - box_width // 2
                    box_rect = pygame.Rect(box_x, y, box_width, box_height)
                    if box_rect.collidepoint(self.mouse_pos):
                        self.profile_selection = i
                        self._load_selected_profile_to_menu()
                        return
            # Check New Profile button
            button_y = SCREEN_HEIGHT - 120 if self.profiles else 350
            button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 140, button_y - 8, 280, 40)
            if button_rect.collidepoint(self.mouse_pos):
                self.profile_action = "new"
                self.player_name = ""
                self.char_selection = 0
                self.state = GameState.CHAR_SELECT
        elif self.state == GameState.MENU:
            idx = self.menu.check_button_click(
                self.menu.main_buttons, self.mouse_pos, mouse_pressed
            )
            if idx >= 0:
                self.menu_selection = idx
                self._handle_menu_selection()

        elif self.state == GameState.OPTIONS:
            idx = self.menu.check_button_click(
                self.menu.options_buttons, self.mouse_pos, mouse_pressed
            )
            if idx >= 0:
                self.options_selection = idx
                self._handle_options_selection()

        elif self.state == GameState.DIFFICULTY_SELECT:
            # Check difficulty selection boxes
            mouse_x, mouse_y = self.mouse_pos
            y_start = 220
            box_width = 500
            box_height = 100
            box_x = SCREEN_WIDTH // 2 - box_width // 2
            for i in range(3):
                y = y_start + i * 120
                box_rect = pygame.Rect(box_x, y, box_width, box_height)
                if box_rect.collidepoint(mouse_x, mouse_y):
                    self.difficulty_selection = i
                    self._start_new_game()
                    break

        elif self.state == GameState.CHAR_SELECT:
            idx = self.menu.check_button_click(
                self.menu.char_buttons, self.mouse_pos, mouse_pressed
            )
            if idx >= 0:
                self.char_selection = idx
                # Auto-start if name entered
                if len(self.player_name) > 0:
                    self._create_new_profile()

        elif self.state == GameState.PAUSED:
            idx = self.menu.check_button_click(
                self.menu.pause_buttons, self.mouse_pos, mouse_pressed
            )
            if idx >= 0:
                self.pause_selection = idx
                self._handle_pause_selection()

    def _handle_back_button(self):
        """Handle back button click based on current state"""
        if self.state == GameState.DIFFICULTY_SELECT:
            self.state = GameState.MENU
        elif self.state == GameState.CHAR_SELECT:
            self.state = GameState.PROFILE_SELECT
        elif self.state == GameState.OPTIONS:
            if self.previous_state:
                self.state = self.previous_state
                self.previous_state = None
            else:
                self.state = GameState.MENU
        elif self.state == GameState.CONTROLS:
            self.state = GameState.OPTIONS
        elif self.state == GameState.SETTINGS:
            self.state = GameState.OPTIONS
        elif self.state == GameState.CREDITS:
            self.state = GameState.OPTIONS
        elif self.state == GameState.LEVEL_MAP:
            self.state = GameState.MENU

    def _handle_options_button(self):
        """Handle options button click - opens options menu"""
        self.previous_state = self.state
        self.state = GameState.OPTIONS
        self.options_selection = 0

    def _handle_events(self):
        """Handle pygame events"""
        self.mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._handle_mouse_click()

            # Route to appropriate handler based on state
            if self.state == GameState.PROFILE_SELECT:
                self._handle_profile_select_events(event)
            elif self.state == GameState.MENU:
                self._handle_menu_events(event)
            elif self.state == GameState.DIFFICULTY_SELECT:
                self._handle_difficulty_select_events(event)
            elif self.state == GameState.CHAR_SELECT:
                self._handle_char_select_events(event)
            elif self.state == GameState.OPTIONS:
                self._handle_options_events(event)
            elif self.state == GameState.CONTROLS:
                self._handle_controls_events(event)
            elif self.state == GameState.SETTINGS:
                self._handle_settings_events(event)
            elif self.state == GameState.CREDITS:
                self._handle_credits_events(event)
            elif self.state == GameState.LEVEL_MAP:
                self._handle_level_map_events(event)
            elif self.state == GameState.PAUSED:
                self._handle_pause_events(event)
            elif self.state == GameState.GAME_OVER:
                self._handle_game_over_events(event)
            elif self.state == GameState.VICTORY:
                self._handle_victory_events(event)

    def _handle_difficulty_select_events(self, event):
        """Handle difficulty selection input"""
        if event.type == pygame.KEYDOWN:
            if controls.check_key_event(event, controls.MENU_UP):
                self.difficulty_selection = (self.difficulty_selection - 1) % 3
            elif controls.check_key_event(event, controls.MENU_DOWN):
                self.difficulty_selection = (self.difficulty_selection + 1) % 3
            elif controls.check_key_event(event, controls.MENU_SELECT):
                self.state = GameState.PLAYING
                self._start_new_game()
            elif event.key == pygame.K_ESCAPE:
                self.state = GameState.MENU

    def _start_new_game(self):
        """Start new game with selected difficulty"""
        from utils.difficulty_manager import DifficultyManager

        # Set difficulty
        difficulties = ["EASY", "NORMAL", "HARD"]
        self.difficulty = difficulties[self.difficulty_selection]

        # Initialize difficulty manager
        self.difficulty_manager = DifficultyManager(self.difficulty, len(self.levels))

        # Create player with current profile's character
        lives = self.difficulty_manager.get_lives(0)
        self.player = Player(100, 100, self.current_profile.character)
        self.player.lives = lives

        # Start from level 0
        self._load_level(0)
        self.state = GameState.PLAYING

    def _apply_difficulty_selection(self):
        """Apply selected difficulty and proceed to character select"""
        difficulties = ["EASY", "NORMAL", "HARD"]
        self.difficulty = difficulties[self.difficulty_selection]
        # Initialize player with current profile's character
        self.player = Player(100, 100, self.current_profile.character)

        # Set difficulty-based lives
        self.difficulty_manager = DifficultyManager(self.difficulty, len(self.levels))
        self.player.lives = self.difficulty_manager.get_lives(0)

        # Start from level 0
        self._load_level(0)
        self.state = GameState.PLAYING

    def _handle_controls_events(self, event):
        """Handle controls screen input"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.state = GameState.OPTIONS  # Back to options

    def _handle_level_map_events(self, event):
        """Handle level map screen input
        Show completed levels
        Allow selecting them to replay
        Track completions per difficulty
        """
        if event.type == pygame.KEYDOWN:
            if controls.check_key_event(event, controls.MENU_UP):
                # Navigate unlocked levels
                pass
            elif controls.check_key_event(event, controls.MENU_SELECT):
                # Start selected level
                self._start_from_level_select()
            elif event.key == pygame.K_ESCAPE:
                self.state = GameState.MENU

    def _handle_menu_events(self, event):
        """Handle main menu input
            Main menu options:
        0 = New Game (start from Level 0)
        1 = Continue Game (load saved game)
        2 = Level Map (select unlocked levels)
        3 = Options
        4 = Quit
        """
        if event.type == pygame.KEYDOWN:
            if controls.check_key_event(event, controls.MENU_UP):
                self.menu_selection = (self.menu_selection - 1) % 5
            elif controls.check_key_event(event, controls.MENU_DOWN):
                self.menu_selection = (self.menu_selection + 1) % 5
            elif controls.check_key_event(event, controls.MENU_SELECT):
                self._handle_menu_selection()
            elif event.key == pygame.K_ESCAPE:
                # ESC from main menu returns to profile select (logout)
                self.current_profile = None
                self.state = GameState.PROFILE_SELECT

    def _handle_menu_selection(self):
        """Handle menu option selection"""
        if self.menu_selection == 0:  # New Game
            self.state = GameState.DIFFICULTY_SELECT
            self.difficulty_selection = 1  # Default to Normal

        elif self.menu_selection == 1:  # Continue Game
            save_data = SaveManager.load_game(self.current_profile.name)
            if save_data:
                # Load from save
                self.player = Player(100, 100, self.current_profile.character)
                self.current_level_index = save_data["current_level"]
                self.difficulty = save_data.get("difficulty", "NORMAL")
                SaveManager.apply_save_to_player(self.player, save_data)

                # Initialize difficulty manager
                from utils.difficulty_manager import DifficultyManager

                self.difficulty_manager = DifficultyManager(
                    self.difficulty, len(self.levels)
                )

                self._load_level(self.current_level_index)
                self.state = GameState.PLAYING
            else:
                # NO SAVE FILE - Show popup instead of going to difficulty select
                self._show_popup("No saved game found! Start a new game.")
                # Stay on menu, don't change state

        elif self.menu_selection == 2:  # Level Map
            self.state = GameState.LEVEL_MAP
            self.level_selection = 0

        elif self.menu_selection == 3:  # Options
            self.state = GameState.OPTIONS
            self.options_selection = 0

        elif self.menu_selection == 4:  # Quit
            self.running = False

    def _handle_options_events(self, event):
        """
        Options submenu:
        0 = Controls
        1 = Settings (placeholder)
        2 = Credits (placeholder)
        3 = Back to Main Menu
        """
        if event.type == pygame.KEYDOWN:
            if controls.check_key_event(event, controls.MENU_UP):
                self.options_selection = (self.options_selection - 1) % 4
            elif controls.check_key_event(event, controls.MENU_DOWN):
                self.options_selection = (self.options_selection + 1) % 4
            elif controls.check_key_event(event, controls.MENU_SELECT):
                self._handle_options_selection()
            elif event.key == pygame.K_ESCAPE:
                self.state = GameState.MENU

    def _handle_options_selection(self):
        if self.options_selection == 0:  # Controls
            self.state = GameState.CONTROLS
        elif self.options_selection == 1:  # Settings (placeholder)
            self.state = GameState.SETTINGS
        elif self.options_selection == 2:  # Credits (placeholder)
            self.state = GameState.CREDITS
        elif self.options_selection == 3:  # Back
            self.state = GameState.MENU

    def _handle_settings_events(self, event):
        """Handle settings screen - PLACEHOLDER"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.state = GameState.OPTIONS

    def _handle_credits_events(self, event):
        """Handle credits screen - PLACEHOLDER"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.state = GameState.OPTIONS

    def _handle_profile_select_events(self, event):
        """Handle profile selection inputTwo options:
        - New Profile (N key or button)
        - Load Profile (L key or select from list)
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_n:  # New profile
                self.profile_action = "new"
                self.player_name = ""
                self.char_selection = 0
                self.state = GameState.CHAR_SELECT  # Go to create character

            elif event.key == pygame.K_l and self.profiles:  # Load Profile (L key)
                self._load_selected_profile_to_menu()

            elif controls.check_key_event(event, controls.MENU_UP):
                if self.profiles:
                    self.profile_selection = (self.profile_selection - 1) % len(
                        self.profiles
                    )

            elif controls.check_key_event(event, controls.MENU_DOWN):
                if self.profiles:
                    self.profile_selection = (self.profile_selection + 1) % len(
                        self.profiles
                    )

            elif (
                controls.check_key_event(event, controls.MENU_SELECT) and self.profiles
            ):
                # Enter key loads selected profile
                self._load_selected_profile_to_menu()

            elif event.key == pygame.K_d and self.profiles:  # Delete profile
                self._delete_selected_profile()

    def _load_selected_profile_to_menu(self):
        """Load selected profile and go to main menu"""
        if self.profiles:
            self.current_profile = self.profiles[self.profile_selection]
            self.state = GameState.MENU
            self.menu_selection = 0

    def _delete_selected_profile(self):
        """Delete the currently selected profile"""
        if not self.profiles:
            return

        profile = self.profiles[self.profile_selection]
        SaveManager.delete_save(profile.name)
        ProfileManager.delete_profile(profile.name)
        self.profiles = ProfileManager.load_profiles()

        if self.profile_selection >= len(self.profiles):
            self.profile_selection = max(0, len(self.profiles) - 1)

    def _load_selected_profile(self):
        """Load the selected profile"""
        self.current_profile = self.profiles[self.profile_selection]
        self.player = Player(100, 100, self.current_profile.character)

        save_data = SaveManager.load_game(self.current_profile.name)
        if save_data:
            self.current_level_index = save_data["current_level"]
            SaveManager.apply_save_to_player(self.player, save_data)
        else:
            self.current_level_index = 0

        self._load_level(self.current_level_index)
        self.state = GameState.PLAYING

    def _handle_char_select_events(self, event):
        """Handle character selection input
        When creating NEW profile:
        - Enter name
        - Select character
        - RETURN creates profile and goes to MENU
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.char_selection = (self.char_selection - 1) % 4
            elif event.key == pygame.K_RIGHT:
                self.char_selection = (self.char_selection + 1) % 4
            elif event.key == pygame.K_BACKSPACE:
                self.player_name = self.player_name[:-1]
            elif event.key == pygame.K_RETURN and len(self.player_name) > 0:
                self._create_new_profile()
            elif event.key == pygame.K_ESCAPE:
                self.state = GameState.PROFILE_SELECT
            elif event.unicode.isalnum() and len(self.player_name) < 15:
                self.player_name += event.unicode

    def _create_new_profile(self):
        """Create new player profile and go to main menu"""
        # Check for duplicate name
        for profile in self.profiles:
            if profile.name.lower() == self.player_name.lower():
                # Show popup for duplicate name
                self._show_popup(f"Profile '{self.player_name}' already exists!")
                return  # Don't create, stay on char select screen

        # Create profile
        self.current_profile = PlayerProfile(
            name=self.player_name,
            character=self.char_selection,
            total_score=0,
            levels_completed=0,
            coins_collected=0,
        )
        self.profiles.append(self.current_profile)
        ProfileManager.save_profiles(self.profiles)

        # Go to main menu (profile now selected)
        self.state = GameState.MENU
        self.menu_selection = 0

    def _handle_pause_events(self, event):
        """Handle pause menu input"""
        if event.type == pygame.KEYDOWN:
            if controls.check_key_event(event, controls.MENU_UP):
                self.pause_selection = (self.pause_selection - 1) % 3
            elif controls.check_key_event(event, controls.MENU_DOWN):
                self.pause_selection = (self.pause_selection + 1) % 3
            elif controls.check_key_event(event, controls.MENU_SELECT):
                self._handle_pause_selection()

    def _handle_pause_selection(self):
        """Handle pause menu option selection"""
        if self.pause_selection == 0:  # Resume
            self.state = GameState.PLAYING
        elif self.pause_selection == 1:  # Return to Main Menu
            self._save_game()  # Auto-save before returning
            self.state = GameState.MENU
            self.menu_selection = 0
        elif self.pause_selection == 2:  # Quit to Profile Select
            self._save_game()
            self.current_profile = None
            self.state = GameState.PROFILE_SELECT  # Return to profile select

    def _handle_victory_events(self, event):
        """Handle victory screen input"""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.state = GameState.MENU  # Stay with current profile

    def _handle_game_over_events(self, event):
        """Handle game over screen input"""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            if self.current_profile:
                SaveManager.delete_save(self.current_profile.name)
            self.state = GameState.MENU  # Stay with current profile

    def _update(self):
        """Update game state"""
        # Update popup timer
        if self.show_popup:
            self.popup.update()

        if self.state == GameState.PLAYING:
            self._update_game()

            if self.boss and not self.boss.defeated:
                self._update_boss()

    def _update_boss(self):
        """Update boss fight logic"""
        from entities.boss_attacks import BossAttackEffect, BossAttackManager

        # Update boss
        current_time = pygame.time.get_ticks()
        self.boss.update(self.player, self.level.tiles, current_time)

        # Execute boss attacks
        if self.boss.current_attack and self.boss.attack_state == 0:
            new_attacks = BossAttackManager.execute_attack(
                self.boss, self.boss.current_attack, self.player, current_time
            )

            # Process new attacks
            for attack in new_attacks:
                if isinstance(attack, dict):
                    # It's an effect
                    effect = BossAttackEffect(attack)
                    self.boss_effects.append(effect)
                else:
                    # It's a projectile
                    self.boss_projectiles.append(attack)

            self.boss.attack_state = 1
            self.boss.current_attack = None

        # Update boss projectiles
        for proj in self.boss_projectiles[:]:
            proj.update(self.level.tiles)
            if not proj.active:
                self.boss_projectiles.remove(proj)
                continue

            # Check player collision
            if self.player.get_rect().colliderect(proj.get_rect()):
                if not self.player.invincible:
                    self.player.take_damage(proj.damage)
                proj.active = False

        # Update boss effects
        for effect in self.boss_effects[:]:
            effect.update(self.boss)
            if not effect.active:
                self.boss_effects.remove(effect)
                continue

            # Check player collision with effects
            if effect.type != "minion_spawn":
                damage_rect = effect.get_damage_rect()
                if self.player.get_rect().colliderect(damage_rect):
                    if not self.player.invincible:
                        self.player.take_damage(effect.damage)

        # Check player attacks on boss
        if self.player.melee_active:
            if self.player.get_melee_rect().colliderect(self.boss.get_rect()):
                if self.boss.take_damage(self.player.weapon_level + 2):
                    self.player.score += 50

        # Check player projectiles on boss
        for proj in self.projectiles[:]:
            if proj.get_rect().colliderect(self.boss.get_rect()):
                if self.boss.take_damage(proj.damage):
                    self.player.score += 25
                proj.active = False

        # Check if boss defeated
        if self.boss.defeated and not self.boss_defeated:
            self._on_boss_defeated()

    def _on_boss_defeated(self):
        """Handle boss defeat"""
        self.boss_defeated = True
        self.player.score += 1000

        # Spawn portal to next level
        from objects.portal import Portal

        portal = Portal(
            self.boss.x + self.boss.width // 2 - 24,
            self.boss.y + self.boss.height,
            self.current_level_index + 1,
            (255, 215, 0),  # Gold portal
        )
        self.level.portals.append(portal)

        # Victory particles
        for _ in range(50):
            self.particles.append(
                Particle(
                    self.boss.x + self.boss.width // 2,
                    self.boss.y + self.boss.height // 2,
                    YELLOW,
                    random.uniform(-8, 8),
                    random.uniform(-8, 8),
                    60,
                )
            )

    def _update_game(self):
        """Update game logic"""
        keys = pygame.key.get_pressed()

        # Handle player input
        self._handle_player_input(keys)

        # Update player
        self.player.update(keys, self.level.tiles, self.level.hazards)

        # Update camera
        self.camera.update(
            self.player.x + self.player.width // 2,
            self.player.y + self.player.height // 2,
            self.level.width,
            self.level.height,
        )

        # Update boss (if exists)
        if self.boss and not self.boss.defeated:
            self._update_boss()

        # Update level objects
        self._update_collectibles()
        self._update_portals()
        self._update_enemies()
        self._update_hazards()
        self._update_projectiles()
        self._update_particles()

        # Check death
        if self.player.y > SCREEN_HEIGHT + 100:
            self.player.die()

        # Check game over
        if self.player.lives < 0:
            self._game_over()

    def _handle_player_input(self, keys):
        """Handle player action input"""
        # Jump
        if controls.check_key_pressed(keys, controls.JUMP):
            if not self.jump_pressed:
                if self.player.jump():
                    self._create_jump_particles()
                self.jump_pressed = True
        else:
            self.jump_pressed = False

        # Shoot
        if controls.check_key_pressed(keys, controls.SHOOT):
            if self.player.shoot():
                self._create_projectile()

        # Melee
        if controls.check_key_pressed(keys, controls.MELEE):
            self.player.melee_attack()

        # Upgrade weapon
        if controls.check_key_pressed(keys, controls.UPGRADE_WEAPON):
            self.player.upgrade_weapon()

        # Save game
        if controls.check_key_pressed(keys, controls.SAVE_GAME):
            self._save_game()

        # Pause
        if controls.check_key_pressed(keys, controls.PAUSE):
            if not self.pause_pressed:
                self.state = GameState.PAUSED
                self.pause_pressed = True
        else:
            self.pause_pressed = False

        # Debug mode toggle (F3 key)
        if controls.check_key_pressed(keys, controls.DEBUG_TOGGLE):
            if not self.debug_toggle_pressed:
                self.debug_mode = not self.debug_mode
                print(f"Debug mode: {'ON' if self.debug_mode else 'OFF'}")
                self.debug_toggle_pressed = True
        else:
            self.debug_toggle_pressed = False

        # Toggle controls (F1)
        if controls.check_key_pressed(keys, controls.TOGGLE_CONTROLS):
            if not self.controls_toggle_pressed:
                self.show_controls = not self.show_controls
                self.controls_toggle_pressed = True
        else:
            self.controls_toggle_pressed = False

    def _create_jump_particles(self):
        """Create particles for jump effect"""
        for _ in range(5):
            self.particles.append(
                Particle(
                    self.player.x + self.player.width // 2,
                    self.player.y + self.player.height,
                    WHITE,
                    random.uniform(-2, 2),
                    random.uniform(-1, 1),
                    20,
                )
            )

    def _create_projectile(self):
        """Create projectile from player"""
        damage = self.player.weapon_level
        speed = 8 + self.player.weapon_level
        proj = Projectile(
            self.player.x + (self.player.width if self.player.direction > 0 else 0),
            self.player.y + self.player.height // 2,
            self.player.direction,
            speed,
            damage,
            CYAN,
        )
        self.projectiles.append(proj)

    def _update_collectibles(self):
        """Update coins, power-ups, keys"""
        # Coins
        for coin in self.level.coins:
            if not coin.collected:
                coin.update()
                if self.player.get_rect().colliderect(coin.get_rect()):
                    coin.collected = True
                    self.player.coins += coin.value
                    self.player.score += coin.value * SCORE_COIN
                    self._create_coin_particles(coin)

        # Power-ups
        for powerup in self.level.powerups:
            if not powerup.collected:
                powerup.update()
                if self.player.get_rect().colliderect(powerup.get_rect()):
                    powerup.collected = True
                    self.player.add_powerup(powerup.type)
                    self.player.score += SCORE_POWERUP

        # Keys
        for key in self.level.keys:
            if not key.collected:
                if self.player.get_rect().colliderect(key.get_rect()):
                    key.collected = True
                    self.player.keys.append(key.color)
                    self.player.score += SCORE_KEY

    def _create_coin_particles(self, coin):
        """Create particles when coin is collected"""
        for _ in range(8):
            self.particles.append(
                Particle(
                    coin.x + coin.width // 2,
                    coin.y + coin.height // 2,
                    YELLOW,
                    random.uniform(-3, 3),
                    random.uniform(-3, 3),
                    30,
                )
            )

    def _update_portals(self):
        """Update portals and handle level transitions"""
        for portal in self.level.portals:
            portal.update()
            if self.player.get_rect().colliderect(portal.get_rect()):
                if portal.check_unlock(self.player.keys):
                    self._transition_to_level(portal.destination)

    def _update_enemies(self):
        """Update enemies and check collisions"""
        for enemy in self.level.enemies:
            if not enemy.dead:
                enemy.update(self.level.tiles)

                # Check collision with player
                if self.player.get_rect().colliderect(enemy.get_rect()):
                    self._handle_enemy_player_collision(enemy)

                # Check melee attack
                if self.player.melee_active:
                    if self.player.get_melee_rect().colliderect(enemy.get_rect()):
                        enemy.take_damage(self.player.weapon_level + 1)
                        self.player.score += SCORE_MELEE_HIT
                        if enemy.dead:
                            self._create_enemy_death_particles(enemy)

    def _handle_enemy_player_collision(self, enemy):
        """Handle collision between player and enemy"""
        # Check if player is stomping
        if (
            self.player.dy > 0
            and self.player.y + self.player.height - 10 < enemy.y + enemy.height // 2
        ):
            enemy.take_damage(2)
            self.player.dy = -10
            self.player.score += SCORE_ENEMY_KILL
            if enemy.dead:
                self._create_enemy_death_particles(enemy)
        else:
            self.player.take_damage(enemy.damage)

    def _create_enemy_death_particles(self, enemy):
        """Create particles when enemy dies"""
        from config.settings import RED

        for _ in range(15):
            self.particles.append(
                Particle(
                    enemy.x + enemy.width // 2,
                    enemy.y + enemy.height // 2,
                    RED,
                    random.uniform(-4, 4),
                    random.uniform(-4, 4),
                    40,
                )
            )

    def _update_hazards(self):
        """Update hazards and check platform collisions"""
        for hazard in self.level.hazards:
            hazard.update(self.player.get_rect())

            # Moving platform collision
            if hazard.type == "moving_platform":
                if self.player.dy > 0:
                    platform_top = pygame.Rect(hazard.x, hazard.y - 5, hazard.width, 10)
                    if self.player.get_rect().colliderect(platform_top):
                        self.player.y = hazard.y - self.player.height
                        self.player.dy = 0
                        self.player.on_ground = True
                        self.player.x += hazard.direction * hazard.speed

    def _update_projectiles(self):
        """Update projectiles and check collisions"""
        for proj in self.projectiles[:]:
            proj.update(self.level.tiles)

            if not proj.active:
                self.projectiles.remove(proj)
                continue

            # Check enemy collision
            for enemy in self.level.enemies:
                if not enemy.dead and proj.get_rect().colliderect(enemy.get_rect()):
                    enemy.take_damage(proj.damage)
                    proj.active = False
                    self.player.score += SCORE_ENEMY_HIT
                    if enemy.dead:
                        self._create_enemy_death_particles(enemy)
                    break

    def _update_particles(self):
        """Update particle effects"""
        self.particles = [p for p in self.particles if p.update()]

    def _load_level(self, level_index):
        """Load level by index"""
        if 0 <= level_index < len(self.levels):
            self.current_level_index = level_index
            self.level = Level(self.levels[level_index])

            if self.player:
                self.player.x = self.level.spawn_x
                self.player.y = self.level.spawn_y

            self.projectiles = []
            self.particles = []

            # Check if this is a boss level and spawn boss
            self._check_and_spawn_boss()

    def _check_and_spawn_boss(self):
        """Check if current level has a boss and spawn it"""
        from entities.boss import Boss

        # Boss levels: 6, 12, 18, 24 (every 6 levels after tutorial)
        boss_levels = {6: "guardian", 12: "forest", 18: "void", 24: "ancient"}

        if self.current_level_index in boss_levels:
            boss_type = boss_levels[self.current_level_index]
            # Spawn boss at center-top of screen
            from config.settings import SCREEN_WIDTH

            self.boss = Boss(
                SCREEN_WIDTH // 2 - 48,  # Center horizontally
                100,  # Near top of screen
                boss_type,
                self.difficulty,
            )
            self.boss_defeated = False
            self.boss_projectiles = []
            self.boss_effects = []
            print(f"✓ Boss spawned: {boss_type}")
        else:
            self.boss = None
            self.boss_defeated = False

    def _transition_to_level(self, level_index):
        """Transition to new level"""
        # Update profile stats
        if self.current_profile:
            ProfileManager.update_profile_stats(
                self.current_profile,
                self.player.score,
                self.player.coins,
                level_completed=True,
            )
            ProfileManager.save_profiles(self.profiles)

        # CHECK FOR VICTORY - Act 1 complete after Level 6 boss
        if self.current_level_index == 6 and level_index > 6:
            # Player beat the boss on level 6, game complete!
            self._game_complete()
            return

        # Otherwise, continue to next level
        self._load_level(level_index)

    def _save_game(self):
        """Save current game state"""
        if self.current_profile and self.player:
            SaveManager.save_game(
                self.current_profile.name, self.player, self.current_level_index
            )

    def _game_over(self):
        """Handle game over"""
        self.state = GameState.GAME_OVER

        # Update final profile stats
        if self.current_profile:
            ProfileManager.update_profile_stats(
                self.current_profile, self.player.score, self.player.coins
            )
            ProfileManager.save_profiles(self.profiles)

    def _game_complete(self):
        """Handle game completion (victory)"""
        self.state = GameState.VICTORY

        # Mark difficulty as completed
        if self.current_profile:
            DifficultyCompletionTracker.mark_difficulty_complete(
                self.current_profile.name, self.difficulty
            )

            # Save completed game stats and delete active profile
            ProfileManager.save_completed_game(self.current_profile, self.player.score)
            ProfileManager.delete_profile(self.current_profile.name)
            SaveManager.delete_save(self.current_profile.name)

            # Reload profiles list
            self.profiles = ProfileManager.load_profiles()

    def _draw(self):
        """Draw current game state"""
        self.current_screen = None  # Reset at start

        # Create temporary surface for game rendering
        if self.settings.get_fullscreen():
            # Render to a surface at game resolution
            game_surface = pygame.Surface((1280, 720))
            render_target = game_surface
        else:
            render_target = self.screen

        # Draw to render target
        if self.state == GameState.PROFILE_SELECT:
            self.current_screen = self.menu.draw_profile_select(
                self.screen, self.profiles, self.profile_selection, self.mouse_pos
            )
        elif self.state == GameState.MENU:
            self.current_screen = self.menu.draw_main_menu(
                self.screen, self.current_profile, self.menu_selection, self.mouse_pos
            )
        elif self.state == GameState.DIFFICULTY_SELECT:
            self.current_screen = self.menu.draw_difficulty_select(
                self.screen, self.difficulty_selection, self.mouse_pos
            )
        elif self.state == GameState.CHAR_SELECT:
            self.current_screen = self.menu.draw_char_select(
                self.screen, self.player_name, self.char_selection, self.mouse_pos
            )
        elif self.state == GameState.OPTIONS:
            self.current_screen = self.menu.draw_options_menu(
                self.screen, self.options_selection, self.mouse_pos
            )
        elif self.state == GameState.CONTROLS:
            self.current_screen = self.menu.draw_controls_screen(
                self.screen, self.mouse_pos
            )
        elif self.state == GameState.SETTINGS:
            self.current_screen = self.menu.draw_settings_screen(
                self.screen, self.settings, self.mouse_pos
            )
        elif self.state == GameState.CREDITS:
            self.current_screen = self.menu.draw_credits_screen(
                self.screen, self.mouse_pos
            )
        elif self.state == GameState.LEVEL_MAP:
            self.current_screen = self.menu.draw_level_map_screen(
                self.screen, self.current_profile, self.mouse_pos
            )
        elif self.state == GameState.PLAYING:
            self._draw_game()
        elif self.state == GameState.PAUSED:
            self._draw_game()
            self.current_screen = self.menu.draw_pause_menu(
                self.screen, self.pause_selection, self.mouse_pos
            )
        elif self.state == GameState.GAME_OVER:
            self.current_screen = self.menu.draw_game_over(
                self.screen, self.player.score
            )
        elif self.state == GameState.VICTORY:
            self.current_screen = self.menu.draw_victory(self.screen, self.player.score)

        # Draw popup if active
        if self.show_popup:
            self.popup.draw(self.screen, self.font_small)

        # If fullscreen, blit game surface centered on screen
        if self.settings.get_fullscreen():
            self.screen.fill((0, 0, 0))  # Black bars
            offset = self.settings.get_render_offset()
            self.screen.blit(game_surface, offset)

        pygame.display.flip()

    def _draw_popup(self):
        """Draw popup overlay"""
        if self.popup and self.popup.is_active():
            self.popup.draw(self.screen, self.font_small)

    def _draw_game(self):
        """Draw game world and HUD"""
        from utils.textures import BackgroundManager

        # Draw themed background with parallax
        theme = self.level.theme.name if self.level else "SCIFI"

        if theme == "SCIFI":
            BackgroundManager.draw_scifi_background(
                self.screen, self.camera.x, self.camera.y, SCREEN_WIDTH, SCREEN_HEIGHT
            )
        elif theme == "NATURE":
            BackgroundManager.draw_nature_background(
                self.screen, self.camera.x, self.camera.y, SCREEN_WIDTH, SCREEN_HEIGHT
            )
        elif theme == "SPACE":
            BackgroundManager.draw_space_background(
                self.screen, self.camera.x, self.camera.y, SCREEN_WIDTH, SCREEN_HEIGHT
            )
        elif theme == "UNDERGROUND":
            BackgroundManager.draw_underground_background(
                self.screen, self.camera.x, self.camera.y, SCREEN_WIDTH, SCREEN_HEIGHT
            )
        elif theme == "UNDERWATER":
            BackgroundManager.draw_underwater_background(
                self.screen, self.camera.x, self.camera.y, SCREEN_WIDTH, SCREEN_HEIGHT
            )
        else:
            # Fallback
            self.screen.fill((20, 20, 40))

        # Draw tiles
        self._draw_tiles()

        # Draw game objects
        self._draw_hazards()
        self._draw_collectibles()
        self._draw_portals()
        self._draw_enemies()
        self._draw_projectiles()
        self._draw_particles()

        # Draw boss
        if self.boss and not self.boss.defeated:
            self.boss.draw(self.screen, self.camera.x, self.camera.y)

        # Draw boss attacks
        for proj in self.boss_projectiles:
            proj.draw(self.screen, self.camera.x, self.camera.y)
        for effect in self.boss_effects:
            effect.draw(self.screen, self.camera.x, self.camera.y)

        # Draw player
        self.player.draw(self.screen, self.camera.x, self.camera.y)

        # Boss health bar
        if self.boss and not self.boss.defeated:
            self.boss.draw_health_bar(self.screen)

        # Draw HUD
        level_name, area_name = self._get_level_and_area_names()
        self.hud.draw(
            self.screen, self.player, self.current_level_index, area_name, level_name
        )

        # Draw debug info
        if self.debug_mode:
            self._draw_debug_overlay()

        # Toggleable controls
        if self.show_controls:
            self.hud.draw_controls_overlay(self.screen)

    def _draw_debug_overlay(self):
        """Draw debug information overlay"""
        # Semi-transparent background
        overlay = pygame.Surface((400, 200))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (10, 200))

        # Get level info
        level_names = [
            "Tutorial: Training Facility",
            "Level 1: The Awakening",
            "Level 2: Rising Conflict",
            "Level 3: The Ascent",
            "Level 4: Deep Dive",
            "Level 5: Convergence",
            "Level 6: Guardian's Lair (BOSS)",
        ]

        # Get area name based on position
        area_name = self._get_area_name(self.current_level_index, self.player.x)

        # Debug info
        debug_info = [
            f"DEBUG MODE (F3 to toggle)",
            f"Level: {self.current_level_index} - {level_names[self.current_level_index] if self.current_level_index < len(level_names) else 'Unknown'}",
            f"Area: {area_name}",
            f"Position: ({int(self.player.x)}, {int(self.player.y)})",
            f"Camera: ({int(self.camera.x)}, {int(self.camera.y)})",
            f"Difficulty: {self.difficulty if hasattr(self, 'difficulty') else 'N/A'}",
            f"Velocity: dx={int(self.player.dx)}, dy={int(self.player.dy)}",
        ]

        # Draw debug text
        y_offset = 210
        for i, line in enumerate(debug_info):
            color = (255, 255, 0) if i == 0 else (255, 255, 255)
            text = self.font_small.render(line, True, color)
            self.screen.blit(text, (20, y_offset + i * 25))

    def _get_area_name(self, level_index, player_x):
        """Get area name based on level and player position"""
        # Level-specific area mappings
        areas = {
            0: [  # Tutorial
                (0, 600, "Section 1: Basic Movement"),
                (600, 1200, "Section 2: Jumping"),
                (1200, 2000, "Section 3: Double Jump"),
                (2000, 2800, "Section 4: Wall Jump"),
                (2800, 3600, "Section 5: Combat - Shooting"),
                (3600, 4200, "Section 6: Melee Combat"),
                (4200, 5000, "Section 7: Hazards"),
                (5000, 5800, "Section 8: Collectibles"),
                (5800, 6400, "Section 9: Final Test"),
            ],
            1: [  # Level 1
                (0, 1500, "Area 1: Introduction"),
                (1500, 2800, "Area 2: Vertical Section"),
                (2800, 4200, "Area 3: High Platforms"),
                (4200, 5800, "Area 4: Underground Passage"),
                (5800, 7000, "Area 5: Combat Zone"),
                (7000, 8000, "Area 6: Final Ascent"),
            ],
            2: [  # Level 2
                (0, 1500, "Area 1: Gentle Start"),
                (1500, 2800, "Area 2: Tower Climb"),
                (2800, 4200, "Area 3: High Platforms"),
                (4200, 5800, "Area 4: Underground"),
                (5800, 7000, "Area 5: Combat Arena"),
                (7000, 8500, "Area 6: Final Gauntlet"),
            ],
            3: [  # Level 3
                (0, 1800, "Area 1: Courtyard"),
                (1800, 3200, "Area 2: First Tower"),
                (3200, 4500, "Area 3: Bridge Section"),
                (4500, 6000, "Area 4: Second Tower"),
                (6000, 7500, "Area 5: Spire Section (3rd Tower)"),
                (7500, 9000, "Area 6: Descent & Finale"),
            ],
            4: [  # Level 4
                (0, 1500, "Area 1: Surface"),
                (1500, 2800, "Area 2: Descent"),
                (2800, 5000, "Area 3: Cave Systems"),
                (5000, 6500, "Area 4: Underground Lake"),
                (6500, 8000, "Area 5: Crystal Caverns"),
                (8000, 9500, "Area 6: Ascent & Exit"),
            ],
            5: [  # Level 5
                (0, 2000, "Area 1: Gauntlet Start"),
                (2000, 3200, "Area 2: Wall Jump Tower"),
                (3200, 4800, "Area 3: Precision Platforming"),
                (4800, 6500, "Area 4: Combat Marathon"),
                (6500, 8000, "Area 5: Hazard Gauntlet"),
                (8000, 9500, "Area 6: Escape Sequence"),
                (9500, 10000, "Area 7: Boss Door"),
            ],
            6: [  # Boss Level
                (0, 1280, "Boss Arena: Guardian's Lair"),
            ],
        }

        # Get areas for current level
        level_areas = areas.get(level_index, [])

        # Find which area player is in
        for start_x, end_x, name in level_areas:
            if start_x <= player_x < end_x:
                return name

        return "Unknown Area"

    def _draw_tiles(self):
        """Draw level tiles with theme-based textures"""
        from utils.collision import is_rect_on_screen
        from utils.textures import TextureManager

        for tile in self.level.tiles:
            if is_rect_on_screen(
                tile["rect"], self.camera.x, self.camera.y, SCREEN_WIDTH, SCREEN_HEIGHT
            ):
                rect = self.camera.apply_rect(tile["rect"])
                theme = tile.get("theme", "SCIFI")
                color = tile["color"]

                # Different pattern per theme for easy identification
                if theme == "SCIFI":
                    # Grid pattern for sci-fi
                    TextureManager.draw_grid_rect(
                        self.screen, rect, color, (200, 200, 200), grid_size=8
                    )
                elif theme == "NATURE":
                    # Diagonal lines for nature
                    TextureManager.draw_diagonal_lines(
                        self.screen, rect, color, (150, 200, 150), spacing=6
                    )
                elif theme == "SPACE":
                    # Dots for space
                    TextureManager.draw_dotted_rect(
                        self.screen, rect, color, (150, 150, 200), dot_size=2, spacing=8
                    )
                elif theme == "UNDERGROUND":
                    # Brick pattern for underground
                    TextureManager.draw_brick_wall(
                        self.screen, rect, (80, 60, 40), color
                    )
                elif theme == "UNDERWATER":
                    # Horizontal waves for underwater
                    TextureManager.draw_striped_rect(
                        self.screen,
                        rect,
                        color,
                        (100, 150, 200),
                        stripe_width=4,
                        vertical=False,
                    )
                else:
                    # Default checkered
                    TextureManager.draw_checkered_rect(
                        self.screen, rect, color, (120, 120, 120), check_size=8
                    )

                # Border
                pygame.draw.rect(self.screen, WHITE, rect, 1)

    def _draw_hazards(self):
        """Draw hazards"""
        for hazard in self.level.hazards:
            hazard.draw(self.screen, self.camera.x, self.camera.y)

    def _draw_collectibles(self):
        """Draw coins, power-ups, keys"""
        for coin in self.level.coins:
            if not coin.collected:
                coin.draw(self.screen, self.camera.x, self.camera.y)

        for powerup in self.level.powerups:
            if not powerup.collected:
                powerup.draw(self.screen, self.camera.x, self.camera.y)

        for key in self.level.keys:
            if not key.collected:
                key.draw(self.screen, self.camera.x, self.camera.y)

    def _draw_portals(self):
        """Draw portals"""
        for portal in self.level.portals:
            portal.draw(self.screen, self.camera.x, self.camera.y)

    def _draw_enemies(self):
        """Draw enemies"""
        for enemy in self.level.enemies:
            enemy.draw(self.screen, self.camera.x, self.camera.y)

    def _draw_projectiles(self):
        """Draw projectiles"""
        for proj in self.projectiles:
            proj.draw(self.screen, self.camera.x, self.camera.y)

    def _draw_particles(self):
        """Draw particle effects"""
        for particle in self.particles:
            particle.draw(self.screen, self.camera.x, self.camera.y)

    def _draw_boss(self):
        """Draw boss and related combat objects"""
        if not self.boss or self.boss.defeated:
            return

        # Draw boss entity
        self.boss.draw(self.screen, self.camera.x, self.camera.y)

        # Draw boss health bar
        self.boss.draw_health_bar(self.screen)

        # Draw boss projectiles
        for proj in self.boss_projectiles:
            proj.draw(self.screen, self.camera.x, self.camera.y)

        # Draw boss effects
        for effect in self.boss_effects:
            effect.draw(self.screen, self.camera.x, self.camera.y)

    def _get_level_and_area_names(self):
        """Get current level and area names for HUD"""
        level_names = [
            "Tutorial: Training Facility",
            "Level 1: The Awakening",
            "Level 2: Rising Conflict",
            "Level 3: The Ascent",
            "Level 4: Deep Dive",
            "Level 5: Convergence",
            "Level 6: Guardian's Lair",
        ]

        level_name = (
            level_names[self.current_level_index]
            if 0 <= self.current_level_index < len(level_names)
            else f"Level {self.current_level_index}"
        )

        # Simplified area detection
        areas = {6: [(0, 1280, "BOSS ARENA")]}

        area_name = ""
        level_areas = areas.get(self.current_level_index, [])
        for start_x, end_x, name in level_areas:
            if start_x <= self.player.x < end_x:
                area_name = name
                break

        return level_name, area_name

    def _handle_settings_events(self, event):
        """Handle settings screen input"""
        components = self.menu.settings_components

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Save settings when leaving
                self.settings.save_settings()
                self.state = GameState.OPTIONS

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Resolution dropdown
            old_res = self.settings.settings['video']['resolution_index']
            if components['res_dropdown'].check_click(self.mouse_pos, pygame.mouse.get_pressed()):
                new_res = components['res_dropdown'].get_selected_index()
                if new_res != old_res:
                    self.settings.set_resolution(new_res)
                    self.settings_changed = True

            # Fullscreen toggle
            if components['fullscreen_toggle'].check_click(self.mouse_pos, pygame.mouse.get_pressed()):
                self.settings.toggle_fullscreen()
                # Apply immediately
                self.screen = self.settings.apply_video_settings(self.screen)
                self.settings.save_settings()

            # Music toggle
            if components['music_toggle'].check_click(self.mouse_pos, pygame.mouse.get_pressed()):
                self.settings.toggle_music()
                self.settings.save_settings()
                # TODO: Apply to audio manager when implemented

            # SFX toggle
            if components['sfx_toggle'].check_click(self.mouse_pos, pygame.mouse.get_pressed()):
                self.settings.toggle_sfx()
                self.settings.save_settings()
                # TODO: Apply to audio manager when implemented

            # Start slider drag
            components['music_slider'].start_drag(self.mouse_pos)
            components['sfx_slider'].start_drag(self.mouse_pos)

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            # Stop slider drag and save
            if components['music_slider'].dragging:
                components['music_slider'].stop_drag()
                self.settings.set_music_volume(components['music_slider'].get_value())
                self.settings.save_settings()

            if components['sfx_slider'].dragging:
                components['sfx_slider'].stop_drag()
                self.settings.set_sfx_volume(components['sfx_slider'].get_value())
                self.settings.save_settings()

        elif event.type == pygame.MOUSEMOTION:
            # Update sliders during drag
            if components['music_slider'].dragging:
                components['music_slider'].update_drag(self.mouse_pos)
                self.settings.set_music_volume(components['music_slider'].get_value())

            if components['sfx_slider'].dragging:
                components['sfx_slider'].update_drag(self.mouse_pos)
                self.settings.set_sfx_volume(components['sfx_slider'].get_value())
            """Handle settings screen input"""
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Save settings when leaving
                    self.settings.save_settings()
                    self.state = GameState.OPTIONS

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Handle clicks on settings components
                if hasattr(self, 'settings_components'):
                    components = self.settings_components

                    # Resolution dropdown
                    if 'res_dropdown' in components:
                        old_res = self.settings.settings['video']['resolution_index']
                        components['res_dropdown'].check_click(self.mouse_pos, pygame.mouse.get_pressed())
                        new_res = components['res_dropdown'].get_selected_index()
                        if new_res != old_res:
                            self.settings.set_resolution(new_res)
                            self.settings_changed = True

                    # Fullscreen toggle
                    if 'fullscreen_toggle' in components:
                        if components['fullscreen_toggle'].check_click(self.mouse_pos, pygame.mouse.get_pressed()):
                            self.settings.toggle_fullscreen()
                            # Apply immediately
                            self.screen = self.settings.apply_video_settings(self.screen)

                    # Music toggle
                    if 'music_toggle' in components:
                        if components['music_toggle'].check_click(self.mouse_pos, pygame.mouse.get_pressed()):
                            self.settings.toggle_music()
                            # Apply to audio manager (when implemented)

                    # SFX toggle
                    if 'sfx_toggle' in components:
                        if components['sfx_toggle'].check_click(self.mouse_pos, pygame.mouse.get_pressed()):
                            self.settings.toggle_sfx()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Start slider drag
                if hasattr(self, 'settings_components'):
                    components = self.settings_components
                    if 'music_slider' in components:
                        components['music_slider'].start_drag(self.mouse_pos)
                    if 'sfx_slider' in components:
                        components['sfx_slider'].start_drag(self.mouse_pos)

            elif event.type == pygame.MOUSEBUTTONUP:
                # Stop slider drag
                if hasattr(self, 'settings_components'):
                    components = self.settings_components
                    if 'music_slider' in components:
                        components['music_slider'].stop_drag()
                        self.settings.set_music_volume(components['music_slider'].get_value())
                    if 'sfx_slider' in components:
                        components['sfx_slider'].stop_drag()
                        self.settings.set_sfx_volume(components['sfx_slider'].get_value())

            elif event.type == pygame.MOUSEMOTION:
                # Update slider during drag
                if hasattr(self, 'settings_components'):
                    components = self.settings_components
                    if 'music_slider' in components:
                        components['music_slider'].update_drag(self.mouse_pos)
                        if components['music_slider'].dragging:
                            self.settings.set_music_volume(components['music_slider'].get_value())
                    if 'sfx_slider' in components:
                        components['sfx_slider'].update_drag(self.mouse_pos)
                        if components['sfx_slider'].dragging:
                            self.settings.set_sfx_volume(components['sfx_slider'].get_value())
