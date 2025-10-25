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
            self."""
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
        self.difficulty_selection = 1  # Default to Normal (0=Easy, 1=Normal, 2=Hard)
        self.pause_selection = 0
        self.profile_selection = 0
        self.char_selection = 0
        self.player_name = ""
        
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
        self.boss = None  # Current boss
        self.boss_projectiles = []  # Boss projectiles
        self.boss_effects = []  # Boss attack effects
        self.boss_defeated = False
        
        # Input state tracking
        self.jump_pressed = False
        self.pause_pressed = False
        
    def run(self):
        """Main game loop"""
        while self.running:
            self._handle_events()
            self._update()
            self._draw()
            self.clock.tick(FPS)
            
        pygame.quit()
        
    def _handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            if self.state == GameState.MENU:
                self._handle_menu_events(event)
            elif self.state == GameState.DIFFICULTY_SELECT:
                self._handle_difficulty_select_events(event)
            elif self.state == GameState.PROFILE_SELECT:
                self._handle_profile_select_events(event)
            elif self.state == GameState.CHAR_SELECT:
                self._handle_char_select_events(event)
            elif self.state == GameState.PAUSED:
                self._handle_pause_events(event)
            elif self.state == GameState.GAME_OVER:
                self._handle_game_over_events(event)
            elif self.state == GameState.VICTORY:
                self._handle_victory_events(event)
                
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
            self.state = GameState.DIFFICULTY_SELECT
            self.difficulty_selection = 1  # Default to Normal
        elif self.menu_selection == 1:  # Load Game
            if self.profiles:
                self.state = GameState.PROFILE_SELECT
                self.profile_selection = 0
        elif self.menu_selection == 2:  # Quit
            self.running = False
            
    def _handle_difficulty_select_events(self, event):
        """Handle difficulty selection input"""
        if event.type == pygame.KEYDOWN:
            if controls.check_key_event(event, controls.MENU_UP):
                self.difficulty_selection = (self.difficulty_selection - 1) % 3
            elif controls.check_key_event(event, controls.MENU_DOWN):
                self.difficulty_selection = (self.difficulty_selection + 1) % 3
            elif controls.check_key_event(event, controls.MENU_SELECT):
                # Set difficulty and proceed to character select
                difficulties = ['EASY', 'NORMAL', 'HARD']
                self.difficulty = difficulties[self.difficulty_selection]
                self.state = GameState.CHAR_SELECT
                self.player_name = ""
            elif controls.check_key_event(event, controls.MENU_BACK):
                self.state = GameState.MENU
            
    def _handle_profile_select_events(self, event):
        """Handle profile selection input"""
        if event.type == pygame.KEYDOWN:
            if controls.check_key_event(event, controls.MENU_UP):
                self.profile_selection = (self.profile_selection - 1) % len(self.profiles)
            elif controls.check_key_event(event, controls.MENU_DOWN):
                self.profile_selection = (self.profile_selection + 1) % len(self.profiles)
            elif controls.check_key_event(event, controls.MENU_SELECT):
                self._load_selected_profile()
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
            if controls.check_key_event(event, controls.MENU_LEFT):
                self.char_selection = (self.char_selection - 1) % 4
            elif controls.check_key_event(event, controls.MENU_RIGHT):
                self.char_selection = (self.char_selection + 1) % 4
            elif event.key == pygame.K_BACKSPACE:
                self.player_name = self.player_name[:-1]
            elif event.key == pygame.K_RETURN and len(self.player_name) > 0:
                self._create_new_profile()
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
        
        # Initialize difficulty manager
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
        
    def _update_boss(self):
        """Update boss fight logic"""
        from entities.boss_attacks import BossAttackManager, BossAttackEffect
        
        # Update boss
        current_time = pygame.time.get_ticks()
        self.boss.update(self.player, self.level.tiles, current_time)
        
        # Execute boss attacks
        if self.boss.current_attack and self.boss.attack_state == 0:
            new_attacks = BossAttackManager.execute_attack(
                self.boss, 
                self.boss.current_attack,
                self.player,
                current_time
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
            if effect.type != 'minion_spawn':
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
            (255, 215, 0)  # Gold portal
        )
        self.level.portals.append(portal)
        
        # Victory particles
        for _ in range(50):
            self.particles.append(Particle(
                self.boss.x + self.boss.width // 2,
                self.boss.y + self.boss.height // 2,
                YELLOW,
                random.uniform(-8, 8),
                random.uniform(-8, 8),
                60
            ))
        
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
        boss_levels = {
            6: 'guardian',
            12: 'forest',
            18: 'void',
            24: 'ancient'
        }
        
        if self.current_level_index in boss_levels:
            boss_type = boss_levels[self.current_level_index]
            # Spawn boss at center-top of screen
            self.boss = Boss(
                SCREEN_WIDTH // 2 - 48,
                100,
                boss_type,
                self.difficulty
            )
            self.boss_defeated = False
            self.boss_projectiles = []
            self.boss_effects = []
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
                level_completed=True
            )
            ProfileManager.save_profiles(self.profiles)
            
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
        
        # Save completed game stats and delete active profile
        if self.current_profile:
            ProfileManager.save_completed_game(self.current_profile, self.player.score)
            ProfileManager.delete_profile(self.current_profile.name)
            SaveManager.delete_save(self.current_profile.name)
            
            # Reload profiles list
            self.profiles = ProfileManager.load_profiles()
            
    def _draw(self):
        """Draw current game state"""
        if self.state == GameState.MENU:
            self.menu.draw_main_menu(self.screen, self.menu_selection)
        elif self.state == GameState.DIFFICULTY_SELECT:
            self.menu.draw_difficulty_select(self.screen, self.difficulty_selection)
        elif self.state == GameState.PROFILE_SELECT:
            self.menu.draw_profile_select(self.screen, self.profiles, self.profile_selection)
        elif self.state == GameState.CHAR_SELECT:
            self.menu.draw_char_select(self.screen, self.player_name, 
                                      self.char_selection)
        elif self.state == GameState.PLAYING:
            self._draw_game()
        elif self.state == GameState.PAUSED:
            self._draw_game()
            self.menu.draw_pause_menu(self.screen, self.pause_selection)
        elif self.state == GameState.GAME_OVER:
            self.menu.draw_game_over(self.screen, self.player.score)
        elif self.state == GameState.VICTORY:
            self.menu.draw_victory(self.screen, self.player.score)
            
        pygame.display.flip()
        
    def _draw_game(self):
        """Draw game world and HUD"""
        # Background
        self.screen.fill(self.level.get_background_color())
        
        # Draw tiles
        self._draw_tiles()
        
        # Draw game objects
        self._draw_hazards()
        self._draw_collectibles()
        self._draw_portals()
        self._draw_enemies()
        
        # Draw boss (if exists)
        if self.boss and not self.boss.defeated:
            self.boss.draw(self.screen, self.camera.x, self.camera.y)
            
        # Draw boss attacks
        for proj in self.boss_projectiles:
            proj.draw(self.screen, self.camera.x, self.camera.y)
        for effect in self.boss_effects:
            effect.draw(self.screen, self.camera.x, self.camera.y)
        
        self._draw_projectiles()
        self._draw_particles()
        
        # Draw player
        self.player.draw(self.screen, self.camera.x, self.camera.y)
        
        # Draw HUD
        self.hud.draw(self.screen, self.player, self.current_level_index)
        
        # Draw boss health bar (if boss active)
        if self.boss and not self.boss.defeated:
            self.boss.draw_health_bar(self.screen)
        
    def _draw_tiles(self):
        """Draw level tiles"""
        from utils.collision import is_rect_on_screen
        
        for tile in self.level.tiles:
            if is_rect_on_screen(tile['rect'], self.camera.x, self.camera.y,
                                SCREEN_WIDTH, SCREEN_HEIGHT):
                rect = self.camera.apply_rect(tile['rect'])
                pygame.draw.rect(self.screen, tile['color'], rect)
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