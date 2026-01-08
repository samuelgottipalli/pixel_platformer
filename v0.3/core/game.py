"""
Main game class - handles game loop and state management
"""
import pygame
import random
from utils.enums import GameState
from config.settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, CYAN, SCORE_COIN, SCORE_ENEMY_KILL,
    SCORE_ENEMY_HIT, SCORE_MELEE_HIT, SCORE_POWERUP, SCORE_KEY, YELLOW, WHITE
)
from config import controls
from core.camera import Camera
from entities.player import Player
from entities.projectile import Projectile
from entities.particle import Particle
from levels.level import Level
from levels.level_loader import LevelLoader
from save_system.profile_manager import ProfileManager, PlayerProfile
from save_system.save_manager import SaveManager
from save_system.difficulty_completion_tracker import DifficultyCompletionTracker
from ui.menu import Menu
from ui.hud import HUD

class Game:
    """Main game class"""

    def __init__(self):
        """Initialize game"""
        pygame.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Retro Pixel Platformer")
        self.clock = pygame.time.Clock()
        self.running = True

        # Fonts
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)

        # UI
        self.menu = Menu(self.font_large, self.font_medium, self.font_small)
        self.hud = HUD(self.font_small)

        # Game state
        self.state = GameState.MENU
        self.menu_selection = 0
        self.pause_selection = 0
        self.profile_selection = 0
        self.char_selection = 0
        self.player_name = ""
        self.level_selection = 0  # For level select screen

        # Player and level
        self.profiles = ProfileManager.load_profiles()
        self.current_profile = None
        self.player = None
        self.current_level_index = 0
        self.level = None
        self.camera = Camera()
        self.difficulty = 'NORMAL'  # EASY, NORMAL, HARD
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

    def run(self):
        """Main game loop"""
        while self.running:
            self._handle_events()
            self._update()
            self._draw()
            self.clock.tick(FPS)

        pygame.quit()

    def _handle_mouse_click(self):
        """Handle mouse clicks on buttons"""
        mouse_pressed = pygame.mouse.get_pressed()
        if not mouse_pressed[0]:  # Left click
            return

        if self.state == GameState.MENU:
            idx = self.menu.check_button_click(
                self.menu.main_buttons, self.mouse_pos, mouse_pressed
            )
            if idx >= 0:
                self.menu_selection = idx
                self._handle_menu_selection()

        elif self.state == GameState.CHAR_SELECT:
            idx = self.menu.check_button_click(
                self.menu.char_buttons, self.mouse_pos, mouse_pressed
            )
            if idx >= 0:
                self.char_selection = idx
                # Auto-start if name entered
                if len(self.player_name) > 0:
                    self._create_new_profile()

        elif self.state == GameState.PROFILE_SELECT:
            # Manual check for profile boxes
            mouse_x, mouse_y = self.mouse_pos
            y_start = 180
            box_width = 500
            box_height = 60
            box_x = SCREEN_WIDTH // 2 - box_width // 2
            for i in range(len(self.profiles)):
                y = y_start + i * 70
                box_rect = pygame.Rect(box_x, y, box_width, box_height)
                if box_rect.collidepoint(mouse_x, mouse_y):
                    self.profile_selection = i
                    self._load_selected_profile()
                    break

        elif self.state == GameState.PAUSED:
            idx = self.menu.check_button_click(
                self.menu.pause_buttons, self.mouse_pos, mouse_pressed
            )
            if idx >= 0:
                self.pause_selection = idx
                self._handle_pause_selection()

    def _handle_events(self):
        """Handle pygame events"""
        self.mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # Mouse clicks
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._handle_mouse_click()

            # Keyboard events
            if self.state == GameState.MENU:
                self._handle_menu_events(event)
            elif self.state == GameState.CHAR_SELECT:
                self._handle_char_select_events(event)
            elif self.state == GameState.PROFILE_SELECT:
                self._handle_profile_select_events(event)
            elif self.state == GameState.CONTROLS:
                self._handle_controls_events(event)
            elif self.state == GameState.LEVEL_MAP:
                self._handle_level_map_events(event)
            elif self.state == GameState.PAUSED:
                self._handle_pause_events(event)
            elif self.state == GameState.GAME_OVER:
                self._handle_game_over_events(event)
            elif self.state == GameState.VICTORY:
                self._handle_victory_events(event)
            elif self.state == GameState.DIFFICULTY_SELECT:
                self._handle_difficulty_select_events(event)
            elif self.state == GameState.LEVEL_SELECT:
                self._handle_level_select_events(event)

    def _handle_difficulty_select_events(self, event):
        """Handle difficulty selection input"""
        if event.type == pygame.KEYDOWN:
            if controls.check_key_event(event, controls.MENU_UP):
                self.difficulty_selection = (self.difficulty_selection - 1) % 5
            elif controls.check_key_event(event, controls.MENU_DOWN):
                self.difficulty_selection = (self.difficulty_selection + 1) % 5
            elif controls.check_key_event(event, controls.MENU_SELECT):
                # Set difficulty
                difficulties = ['EASY', 'NORMAL', 'HARD']
                self.difficulty = difficulties[self.difficulty_selection]

                # Check if this difficulty is completed for current profile
                if self.current_profile:
                    completed = DifficultyCompletionTracker.has_completed_difficulty(
                        self.current_profile.name, 
                        self.difficulty
                    )
                    if completed:
                        # Show level selection
                        self.state = GameState.LEVEL_SELECT
                        self.level_selection = 0
                        return

                # Otherwise go to character select
                self.state = GameState.CHAR_SELECT
                self.player_name = ""
            elif controls.check_key_event(event, controls.MENU_BACK):
                self.state = GameState.MENU

    def _apply_difficulty_selection(self):
        """Apply selected difficulty and proceed to character select"""
        difficulties = ['EASY', 'NORMAL', 'HARD']
        self.difficulty = difficulties[self.difficulty_selection]
        self.state = GameState.CHAR_SELECT
        self.player_name = ""

    def _handle_controls_events(self, event):
        """Handle controls screen input"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.state = GameState.MENU

    def _handle_level_map_events(self, event):
        """Handle level map screen input"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.state = GameState.MENU

    def _handle_menu_events(self, event):
        """Handle main menu input"""
        if event.type == pygame.KEYDOWN:
            if controls.check_key_event(event, controls.MENU_UP):
                self.menu_selection = (self.menu_selection - 1) % 3
            elif controls.check_key_event(event, controls.MENU_DOWN):
                self.menu_selection = (self.menu_selection + 1) % 3
            elif controls.check_key_event(event, controls.MENU_SELECT):
                self._handle_menu_selection()

    def _handle_menu_selection(self):
        """Handle menu option selection"""
        if self.menu_selection == 0:  # New Game
            self.state = GameState.CHAR_SELECT
            self.player_name = ""
        elif self.menu_selection == 1:  # Load Game
            if self.profiles:
                self.state = GameState.PROFILE_SELECT
                self.profile_selection = 0
        elif self.menu_selection == 2:  # Controls
            self.state = GameState.CONTROLS
        elif self.menu_selection == 3:  # Level Map
            self.state = GameState.LEVEL_MAP
        elif self.menu_selection == 4:  # Quit
            self.running = False

    def _handle_profile_select_events(self, event):
        """Handle profile selection input"""
        if event.type == pygame.KEYDOWN:
            if controls.check_key_event(event, controls.MENU_UP):
                self.profile_selection = (self.profile_selection - 1) % len(self.profiles)
            elif controls.check_key_event(event, controls.MENU_DOWN):
                self.profile_selection = (self.profile_selection + 1) % len(self.profiles)
            elif event.key == pygame.K_l:  # L key to load
                self._load_selected_profile()
            elif event.key == pygame.K_d:  # D key to delete
                self._delete_selected_profile()
            elif controls.check_key_event(event, controls.MENU_BACK):
                self.state = GameState.MENU

    def _load_selected_profile(self):
        """Load the selected profile"""
        self.current_profile = self.profiles[self.profile_selection]
        self.player = Player(100, 100, self.current_profile.character)

        save_data = SaveManager.load_game(self.current_profile.name)
        if save_data:
            self.current_level_index = save_data['current_level']
            SaveManager.apply_save_to_player(self.player, save_data)
        else:
            self.current_level_index = 0

        self._load_level(self.current_level_index)
        self.state = GameState.PLAYING

    def _handle_char_select_events(self, event):
        """Handle character selection input"""
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
                self.state = GameState.MENU
            # Allow all alphanumeric including 'a' and 'd'
            elif event.unicode.isalnum() and len(self.player_name) < 15:
                self.player_name += event.unicode

    def _create_new_profile(self):
        """Create new player profile and start game"""
        from utils.difficulty_manager import DifficultyManager

        self.current_profile = PlayerProfile(
            name=self.player_name,
            character=self.char_selection,
            total_score=0,
            levels_completed=0,
            coins_collected=0
        )
        self.profiles.append(self.current_profile)
        ProfileManager.save_profiles(self.profiles)

        # Initialize difficulty manager with selected difficulty
        self.difficulty_manager = DifficultyManager(self.difficulty, len(self.levels))

        # Start game with difficulty-adjusted lives
        lives = self.difficulty_manager.get_lives(0)
        self.player = Player(100, 100, self.char_selection)
        self.player.lives = lives

        self._load_level(0)
        self.state = GameState.PLAYING

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
        elif self.pause_selection == 2:  # Quit Game
            self._save_game()  # Auto-save before quitting
            self.running = False

    def _handle_game_over_events(self, event):
        """Handle game over screen input"""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            # Delete the save file when returning to menu after game over
            if self.current_profile:
                SaveManager.delete_save(self.current_profile.name)
            self.state = GameState.MENU

    def _handle_victory_events(self, event):
        """Handle victory screen input"""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.state = GameState.MENU

    def _update(self):
        """Update game state"""
        if self.state == GameState.PLAYING:
            self._update_game()

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
            self.level.height
        )

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

    def _create_jump_particles(self):
        """Create particles for jump effect"""
        for _ in range(5):
            self.particles.append(Particle(
                self.player.x + self.player.width // 2,
                self.player.y + self.player.height,
                WHITE,
                random.uniform(-2, 2),
                random.uniform(-1, 1),
                20
            ))

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
            CYAN
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
            self.particles.append(Particle(
                coin.x + coin.width // 2,
                coin.y + coin.height // 2,
                YELLOW,
                random.uniform(-3, 3),
                random.uniform(-3, 3),
                30
            ))

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
        if (self.player.dy > 0 and 
            self.player.y + self.player.height - 10 < enemy.y + enemy.height // 2):
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
            self.particles.append(Particle(
                enemy.x + enemy.width // 2,
                enemy.y + enemy.height // 2,
                RED,
                random.uniform(-4, 4),
                random.uniform(-4, 4),
                40
            ))

    def _update_hazards(self):
        """Update hazards and check platform collisions"""
        for hazard in self.level.hazards:
            hazard.update(self.player.get_rect())

            # Moving platform collision
            if hazard.type == 'moving_platform':
                if self.player.dy > 0:
                    platform_top = pygame.Rect(
                        hazard.x, 
                        hazard.y - 5, 
                        hazard.width, 
                        10
                    )
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

    def _transition_to_level(self, level_index):
        """Transition to new level"""
        # Update profile stats
        if self.current_profile:
            ProfileManager.update_profile_stats(
                self.current_profile,
                self.player.score,
                self.player.coins,
                level_completed=True
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
                self.current_profile.name,
                self.player,
                self.current_level_index
            )

    def _game_over(self):
        """Handle game over"""
        self.state = GameState.GAME_OVER

        # Update final profile stats
        if self.current_profile:
            ProfileManager.update_profile_stats(
                self.current_profile,
                self.player.score,
                self.player.coins
            )
            ProfileManager.save_profiles(self.profiles)

    def _game_complete(self):
        """Handle game completion (victory)"""
        self.state = GameState.VICTORY

        # Mark difficulty as completed
        if self.current_profile:
            DifficultyCompletionTracker.mark_difficulty_complete(
                self.current_profile.name,
                self.difficulty
            )

            # Save completed game stats and delete active profile
            ProfileManager.save_completed_game(self.current_profile, self.player.score)
            ProfileManager.delete_profile(self.current_profile.name)
            SaveManager.delete_save(self.current_profile.name)

            # Reload profiles list
            self.profiles = ProfileManager.load_profiles()

    def _draw(self):
        """Draw current game state"""
        if self.state == GameState.MENU:
            self.menu.draw_main_menu(self.screen, self.menu_selection, self.mouse_pos)
        elif self.state == GameState.DIFFICULTY_SELECT:
            self.menu.draw_difficulty_select(self.screen, self.difficulty_selection)
        elif self.state == GameState.LEVEL_SELECT:
            self.menu.draw_level_select(self.screen, self.levels, 
                                        self.level_selection, self.difficulty)
        elif self.state == GameState.PROFILE_SELECT:
            self.menu.draw_profile_select(self.screen, self.profiles, 
                                        self.profile_selection, self.mouse_pos)
        elif self.state == GameState.CHAR_SELECT:
            self.menu.draw_char_select(self.screen, self.player_name, 
                                    self.char_selection, self.mouse_pos)
        elif self.state == GameState.CONTROLS:
            self.menu.draw_controls_screen(self.screen, self.mouse_pos)
        elif self.state == GameState.LEVEL_MAP:
            self.menu.draw_level_map_screen(self.screen, self.mouse_pos)
        elif self.state == GameState.PLAYING:
            self._draw_game()
        elif self.state == GameState.PAUSED:
            self._draw_game()
            self.menu.draw_pause_menu(self.screen, self.pause_selection, self.mouse_pos)
        elif self.state == GameState.GAME_OVER:
            self.menu.draw_game_over(self.screen, self.player.score)
        elif self.state == GameState.VICTORY:
            self.menu.draw_victory(self.screen, self.player.score)

        pygame.display.flip()

    def _draw_game(self):
        """Draw game world and HUD"""
        from utils.textures import BackgroundManager

        # Draw themed background with parallax
        theme = self.level.theme.name if self.level else 'SCIFI'

        if theme == 'SCIFI':
            BackgroundManager.draw_scifi_background(
                self.screen, self.camera.x, self.camera.y, SCREEN_WIDTH, SCREEN_HEIGHT)
        elif theme == 'NATURE':
            BackgroundManager.draw_nature_background(
                self.screen, self.camera.x, self.camera.y, SCREEN_WIDTH, SCREEN_HEIGHT)
        elif theme == 'SPACE':
            BackgroundManager.draw_space_background(
                self.screen, self.camera.x, self.camera.y, SCREEN_WIDTH, SCREEN_HEIGHT)
        elif theme == 'UNDERGROUND':
            BackgroundManager.draw_underground_background(
                self.screen, self.camera.x, self.camera.y, SCREEN_WIDTH, SCREEN_HEIGHT)
        elif theme == 'UNDERWATER':
            BackgroundManager.draw_underwater_background(
                self.screen, self.camera.x, self.camera.y, SCREEN_WIDTH, SCREEN_HEIGHT)
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

        # Draw player
        self.player.draw(self.screen, self.camera.x, self.camera.y)

        # Draw HUD
        self.hud.draw(self.screen, self.player, self.current_level_index)

        # Draw debug info
        if self.debug_mode:
            self._draw_debug_overlay()

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
            if is_rect_on_screen(tile['rect'], self.camera.x, self.camera.y,
                                SCREEN_WIDTH, SCREEN_HEIGHT):
                rect = self.camera.apply_rect(tile['rect'])
                theme = tile.get('theme', 'SCIFI')
                color = tile['color']

                # Different pattern per theme for easy identification
                if theme == 'SCIFI':
                    # Grid pattern for sci-fi
                    TextureManager.draw_grid_rect(self.screen , rect, color, (200, 200, 200), grid_size=8)
                elif theme == 'NATURE':
                    # Diagonal lines for nature
                    TextureManager.draw_diagonal_lines(self.screen, rect, color, (150, 200, 150), spacing=6)
                elif theme == 'SPACE':
                    # Dots for space
                    TextureManager.draw_dotted_rect(self.screen, rect, color, (150, 150, 200), dot_size=2, spacing=8)
                elif theme == 'UNDERGROUND':
                    # Brick pattern for underground
                    TextureManager.draw_brick_wall(self.screen, rect, (80, 60, 40), color)
                elif theme == 'UNDERWATER':
                    # Horizontal waves for underwater
                    TextureManager.draw_striped_rect(self.screen, rect, color, (100, 150, 200), stripe_width=4, vertical=False)
                else:
                    # Default checkered
                    TextureManager.draw_checkered_rect(self.screen, rect, color, (120, 120, 120), check_size=8)

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

    def _delete_selected_profile(self):
        """Delete the selected profile"""
        if not self.profiles:
            return

        profile = self.profiles[self.profile_selection]

        # Delete save file
        SaveManager.delete_save(profile.name)

        # Delete profile
        ProfileManager.delete_profile(profile.name)

        # Reload profiles
        self.profiles = ProfileManager.load_profiles()

        # Adjust selection
        if self.profile_selection >= len(self.profiles):
            self.profile_selection = max(0, len(self.profiles) - 1)

        # If no profiles left, return to menu
        if not self.profiles:
            self.state = GameState.MENU

    def _handle_level_select_events(self, event):
        """Handle level selection input"""
        if event.type == pygame.KEYDOWN:
            if controls.check_key_event(event, controls.MENU_UP):
                self.level_selection = (self.level_selection - 1) % len(self.levels)
            elif controls.check_key_event(event, controls.MENU_DOWN):
                self.level_selection = (self.level_selection + 1) % len(self.levels)
            elif controls.check_key_event(event, controls.MENU_SELECT):
                # Start from selected level
                self._start_from_level_select()
            elif controls.check_key_event(event, controls.MENU_BACK):
                self.state = GameState.DIFFICULTY_SELECT

    def _start_from_level_select(self):
        """Start game from level selection"""
        from utils.difficulty_manager import DifficultyManager

        # Create or use existing profile
        if not self.current_profile:
            # Create temp profile
            self.current_profile = PlayerProfile(
                name=f"LevelSelect_{self.difficulty}",
                character=0,
                total_score=0,
                levels_completed=0,
                coins_collected=0,
            )

        # Initialize difficulty manager
        self.difficulty_manager = DifficultyManager(self.difficulty, len(self.levels))

        # Start game with difficulty-adjusted lives
        lives = self.difficulty_manager.get_lives(self.level_selection)
        self.player = Player(100, 100, self.current_profile.character)
        self.player.lives = lives

        # Load selected level
        self._load_level(self.level_selection)
        self.state = GameState.PLAYING
