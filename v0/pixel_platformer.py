import pygame
import json
import math
import random
from enum import Enum
from dataclasses import dataclass
from typing import List, Tuple, Optional

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
TILE_SIZE = 32

# Colors (Retro Palette)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 150, 255)
YELLOW = (255, 255, 0)
PURPLE = (200, 0, 255)
CYAN = (0, 255, 255)
ORANGE = (255, 150, 0)
DARK_BLUE = (0, 50, 100)
DARK_GREEN = (0, 100, 50)
GRAY = (100, 100, 100)

# Physics
GRAVITY = 0.8
MAX_FALL_SPEED = 15
PLAYER_SPEED = 6
JUMP_POWER = -15
WALL_JUMP_POWER = -14
WALL_JUMP_PUSH = 8

class GameState(Enum):
    MENU = 1
    CHAR_SELECT = 2
    PLAYING = 3
    PAUSED = 4
    GAME_OVER = 5
    LEVEL_COMPLETE = 6

class Theme(Enum):
    SCIFI = 1
    NATURE = 2
    SPACE = 3
    UNDERGROUND = 4
    UNDERWATER = 5

@dataclass
class PlayerProfile:
    name: str
    character: int
    total_score: int
    levels_completed: int
    coins_collected: int

class Particle:
    def __init__(self, x, y, color, dx, dy, lifetime):
        self.x = x
        self.y = y
        self.color = color
        self.dx = dx
        self.dy = dy
        self.lifetime = lifetime
        self.age = 0
        
    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.dy += 0.3
        self.age += 1
        return self.age < self.lifetime
        
    def draw(self, surface, camera_x, camera_y):
        alpha = int(255 * (1 - self.age / self.lifetime))
        size = max(1, 4 - self.age // 5)
        pygame.draw.circle(surface, self.color, 
                         (int(self.x - camera_x), int(self.y - camera_y)), size)

class Animation:
    def __init__(self, frames, frame_duration):
        self.frames = frames
        self.frame_duration = frame_duration
        self.current_frame = 0
        self.timer = 0
        
    def update(self):
        self.timer += 1
        if self.timer >= self.frame_duration:
            self.timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            
    def get_frame(self):
        return self.frames[self.current_frame]
        
    def reset(self):
        self.current_frame = 0
        self.timer = 0

class Projectile:
    def __init__(self, x, y, direction, speed, damage, color):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = speed
        self.damage = damage
        self.color = color
        self.width = 12
        self.height = 6
        self.active = True
        
    def update(self, tiles):
        self.x += self.direction * self.speed
        
        # Check collision with tiles
        for tile in tiles:
            if self.get_rect().colliderect(tile['rect']):
                self.active = False
                return
                
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
        
    def draw(self, surface, camera_x, camera_y):
        rect = pygame.Rect(self.x - camera_x, self.y - camera_y, 
                          self.width, self.height)
        pygame.draw.rect(surface, self.color, rect)
        pygame.draw.rect(surface, WHITE, rect, 1)

class PowerUp:
    def __init__(self, x, y, ptype):
        self.x = x
        self.y = y
        self.type = ptype  # 'health', 'double_jump', 'speed', 'invincible'
        self.width = 24
        self.height = 24
        self.collected = False
        self.float_offset = 0
        
    def update(self):
        self.float_offset = math.sin(pygame.time.get_ticks() / 200) * 5
        
    def get_rect(self):
        return pygame.Rect(self.x, self.y + self.float_offset, 
                          self.width, self.height)
        
    def draw(self, surface, camera_x, camera_y):
        colors = {
            'health': RED,
            'double_jump': CYAN,
            'speed': YELLOW,
            'invincible': PURPLE
        }
        color = colors.get(self.type, WHITE)
        
        rect = pygame.Rect(self.x - camera_x, self.y + self.float_offset - camera_y,
                          self.width, self.height)
        pygame.draw.rect(surface, color, rect)
        pygame.draw.rect(surface, WHITE, rect, 2)
        
        # Draw icon
        cx, cy = rect.centerx, rect.centery
        if self.type == 'health':
            pygame.draw.line(surface, WHITE, (cx, cy-6), (cx, cy+6), 3)
            pygame.draw.line(surface, WHITE, (cx-6, cy), (cx+6, cy), 3)

class Coin:
    def __init__(self, x, y, value=1):
        self.x = x
        self.y = y
        self.value = value
        self.width = 20
        self.height = 20
        self.collected = False
        self.rotation = 0
        
    def update(self):
        self.rotation = (self.rotation + 5) % 360
        
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
        
    def draw(self, surface, camera_x, camera_y):
        # Animated spinning coin
        width = abs(math.cos(math.radians(self.rotation))) * self.width
        rect = pygame.Rect(self.x - camera_x + (self.width - width) / 2,
                          self.y - camera_y, width, self.height)
        pygame.draw.ellipse(surface, YELLOW, rect)
        pygame.draw.ellipse(surface, ORANGE, rect, 2)

class Key:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.width = 24
        self.height = 24
        self.collected = False
        
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
        
    def draw(self, surface, camera_x, camera_y):
        x = self.x - camera_x
        y = self.y - camera_y
        pygame.draw.circle(surface, self.color, (int(x + 8), int(y + 8)), 6)
        pygame.draw.rect(surface, self.color, (x + 8, y + 8, 12, 4))
        pygame.draw.rect(surface, self.color, (x + 16, y + 6, 2, 4))
        pygame.draw.rect(surface, self.color, (x + 16, y + 10, 2, 4))

class Portal:
    def __init__(self, x, y, destination_level, color=PURPLE):
        self.x = x
        self.y = y
        self.width = 48
        self.height = 64
        self.destination = destination_level
        self.color = color
        self.animation_offset = 0
        
    def update(self):
        self.animation_offset = (self.animation_offset + 1) % 360
        
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
        
    def draw(self, surface, camera_x, camera_y):
        x = self.x - camera_x
        y = self.y - camera_y
        
        # Animated portal effect
        for i in range(3):
            offset = math.sin(math.radians(self.animation_offset + i * 120)) * 8
            rect = pygame.Rect(x + offset, y, self.width - abs(offset) * 2, self.height)
            color = tuple(max(0, c - i * 60) for c in self.color)
            pygame.draw.ellipse(surface, color, rect)

class Enemy:
    def __init__(self, x, y, enemy_type, patrol_distance=200):
        self.x = x
        self.y = y
        self.start_x = x
        self.type = enemy_type  # 'ground', 'flying', 'turret'
        self.width = 32
        self.height = 32
        self.health = 3
        self.damage = 1
        self.direction = 1
        self.speed = 2
        self.patrol_distance = patrol_distance
        self.dy = 0
        self.dead = False
        self.shoot_timer = 0
        self.shoot_cooldown = 120
        
    def update(self, tiles):
        if self.dead:
            return
            
        if self.type == 'ground':
            self.x += self.direction * self.speed
            
            # Turn around at patrol bounds
            if abs(self.x - self.start_x) > self.patrol_distance:
                self.direction *= -1
                
            # Apply gravity
            self.dy += GRAVITY
            self.dy = min(self.dy, MAX_FALL_SPEED)
            self.y += self.dy
            
            # Check ground collision
            for tile in tiles:
                if tile['solid'] and self.get_rect().colliderect(tile['rect']):
                    if self.dy > 0:
                        self.y = tile['rect'].top - self.height
                        self.dy = 0
                        
        elif self.type == 'flying':
            # Sine wave flight pattern
            self.x += self.direction * self.speed
            self.y = self.start_x + math.sin(pygame.time.get_ticks() / 500) * 50
            
            if abs(self.x - self.start_x) > self.patrol_distance:
                self.direction *= -1
                
        elif self.type == 'turret':
            self.shoot_timer += 1
            
    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.dead = True
            
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
        
    def draw(self, surface, camera_x, camera_y):
        if self.dead:
            return
            
        rect = pygame.Rect(self.x - camera_x, self.y - camera_y, 
                          self.width, self.height)
        
        colors = {
            'ground': RED,
            'flying': CYAN,
            'turret': ORANGE
        }
        color = colors.get(self.type, RED)
        
        pygame.draw.rect(surface, color, rect)
        pygame.draw.rect(surface, WHITE, rect, 2)
        
        # Draw eyes
        eye_y = rect.y + 10
        pygame.draw.circle(surface, WHITE, (rect.x + 10, eye_y), 4)
        pygame.draw.circle(surface, WHITE, (rect.x + 22, eye_y), 4)

class Hazard:
    def __init__(self, x, y, hazard_type, width=32, height=32):
        self.x = x
        self.y = y
        self.type = hazard_type  # 'spike', 'falling_block', 'moving_platform'
        self.width = width
        self.height = height
        self.damage = 1
        self.start_x = x
        self.start_y = y
        self.dy = 0
        self.falling = False
        self.respawn_timer = 0
        
        # Moving platform
        self.direction = 1
        self.move_distance = 150
        self.speed = 2
        
    def update(self, player_rect):
        if self.type == 'falling_block':
            if not self.falling and player_rect.colliderect(self.get_trigger_rect()):
                self.falling = True
                
            if self.falling:
                self.dy += GRAVITY
                self.y += self.dy
                
            if self.y > SCREEN_HEIGHT + 100:
                self.respawn_timer += 1
                if self.respawn_timer > 300:
                    self.y = self.start_y
                    self.dy = 0
                    self.falling = False
                    self.respawn_timer = 0
                    
        elif self.type == 'moving_platform':
            self.x += self.direction * self.speed
            if abs(self.x - self.start_x) > self.move_distance:
                self.direction *= -1
                
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
        
    def get_trigger_rect(self):
        return pygame.Rect(self.x - 50, self.y - 100, self.width + 100, 100)
        
    def draw(self, surface, camera_x, camera_y):
        rect = pygame.Rect(self.x - camera_x, self.y - camera_y,
                          self.width, self.height)
        
        if self.type == 'spike':
            # Draw spikes
            points = [
                (rect.left, rect.bottom),
                (rect.centerx, rect.top),
                (rect.right, rect.bottom)
            ]
            pygame.draw.polygon(surface, RED, points)
            pygame.draw.polygon(surface, WHITE, points, 2)
            
        elif self.type == 'falling_block':
            color = GRAY if not self.falling else RED
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, WHITE, rect, 2)
            
        elif self.type == 'moving_platform':
            pygame.draw.rect(surface, BLUE, rect)
            pygame.draw.rect(surface, WHITE, rect, 2)

class Player:
    def __init__(self, x, y, character=0):
        self.x = x
        self.y = y
        self.width = 28
        self.height = 48
        self.dx = 0
        self.dy = 0
        self.direction = 1
        self.on_ground = False
        self.on_wall = False
        self.wall_direction = 0
        self.jump_count = 0
        self.max_jumps = 2
        self.health = 100
        self.max_health = 100
        self.lives = 3
        self.coins = 0
        self.keys = []
        self.score = 0
        self.character = character
        self.invincible = False
        self.invincible_timer = 0
        self.speed_boost = False
        self.speed_boost_timer = 0
        self.weapon_level = 1
        self.can_shoot = True
        self.shoot_cooldown = 0
        self.melee_active = False
        self.melee_timer = 0
        
    def update(self, keys, tiles, hazards):
        # Handle power-up timers
        if self.invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.invincible = False
                
        if self.speed_boost:
            self.speed_boost_timer -= 1
            if self.speed_boost_timer <= 0:
                self.speed_boost = False
                
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
            
        if self.melee_timer > 0:
            self.melee_timer -= 1
            if self.melee_timer == 0:
                self.melee_active = False
        
        # Movement
        speed = PLAYER_SPEED * (1.5 if self.speed_boost else 1)
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.dx = -speed
            self.direction = -1
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.dx = speed
            self.direction = 1
        else:
            self.dx *= 0.8
            if abs(self.dx) < 0.1:
                self.dx = 0
        
        # Apply gravity
        self.dy += GRAVITY
        self.dy = min(self.dy, MAX_FALL_SPEED)
        
        # Wall slide
        if self.on_wall and not self.on_ground and self.dy > 0:
            self.dy = min(self.dy, 2)
        
        # Update position
        self.x += self.dx
        self.check_collision_x(tiles)
        
        self.y += self.dy
        self.check_collision_y(tiles)
        
        # Check hazards
        if not self.invincible:
            for hazard in hazards:
                if hazard.type in ['spike', 'falling_block']:
                    if self.get_rect().colliderect(hazard.get_rect()):
                        self.take_damage(hazard.damage)
        
        # Death check
        if self.y > SCREEN_HEIGHT + 100:
            self.die()
            
    def check_collision_x(self, tiles):
        self.on_wall = False
        player_rect = self.get_rect()
        
        for tile in tiles:
            if tile['solid'] and player_rect.colliderect(tile['rect']):
                if self.dx > 0:
                    self.x = tile['rect'].left - self.width
                    self.on_wall = True
                    self.wall_direction = 1
                elif self.dx < 0:
                    self.x = tile['rect'].right
                    self.on_wall = True
                    self.wall_direction = -1
                self.dx = 0
                
    def check_collision_y(self, tiles):
        self.on_ground = False
        player_rect = self.get_rect()
        
        for tile in tiles:
            if tile['solid'] and player_rect.colliderect(tile['rect']):
                if self.dy > 0:
                    self.y = tile['rect'].top - self.height
                    self.dy = 0
                    self.on_ground = True
                    self.jump_count = 0
                elif self.dy < 0:
                    self.y = tile['rect'].bottom
                    self.dy = 0
                    
    def jump(self):
        if self.on_ground:
            self.dy = JUMP_POWER
            self.jump_count = 1
            return True
        elif self.on_wall:
            # Wall jump
            self.dy = WALL_JUMP_POWER
            self.dx = -self.wall_direction * WALL_JUMP_PUSH
            self.jump_count = 1
            return True
        elif self.jump_count < self.max_jumps:
            # Double jump
            self.dy = JUMP_POWER * 0.85
            self.jump_count += 1
            return True
        return False
        
    def shoot(self):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = 30 - (self.weapon_level * 5)
            return True
        return False
        
    def melee_attack(self):
        if self.melee_timer == 0:
            self.melee_active = True
            self.melee_timer = 20
            return True
        return False
        
    def get_melee_rect(self):
        if self.melee_active:
            return pygame.Rect(
                self.x + (self.width if self.direction > 0 else -32),
                self.y + 10,
                32, 28
            )
        return pygame.Rect(0, 0, 0, 0)
        
    def take_damage(self, damage):
        if not self.invincible:
            self.health -= damage
            if self.health <= 0:
                self.die()
                
    def die(self):
        self.lives -= 1
        self.health = self.max_health
        if self.lives >= 0:
            self.respawn()
            
    def respawn(self):
        self.x = 100
        self.y = 100
        self.dx = 0
        self.dy = 0
        self.invincible = True
        self.invincible_timer = 120
        
    def add_powerup(self, ptype):
        if ptype == 'health':
            self.health = min(self.health + 50, self.max_health)
        elif ptype == 'double_jump':
            self.max_jumps = 3
        elif ptype == 'speed':
            self.speed_boost = True
            self.speed_boost_timer = 600
        elif ptype == 'invincible':
            self.invincible = True
            self.invincible_timer = 300
            
    def upgrade_weapon(self):
        costs = {1: 10, 2: 25, 3: 50}
        if self.weapon_level < 4 and self.coins >= costs.get(self.weapon_level, 999):
            self.coins -= costs[self.weapon_level]
            self.weapon_level += 1
            return True
        return False
        
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
        
    def draw(self, surface, camera_x, camera_y):
        # Invincibility flicker
        if self.invincible and (pygame.time.get_ticks() // 100) % 2:
            return
            
        rect = pygame.Rect(self.x - camera_x, self.y - camera_y,
                          self.width, self.height)
        
        # Character colors
        colors = [BLUE, GREEN, PURPLE, ORANGE]
        color = colors[self.character % len(colors)]
        
        # Body
        pygame.draw.rect(surface, color, rect)
        pygame.draw.rect(surface, WHITE, rect, 2)
        
        # Eyes
        eye_y = rect.y + 12
        eye_x = rect.centerx + (5 if self.direction > 0 else -10)
        pygame.draw.circle(surface, WHITE, (eye_x, eye_y), 4)
        pygame.draw.circle(surface, BLACK, (eye_x + self.direction * 2, eye_y), 2)
        
        # Melee effect
        if self.melee_active:
            melee_rect = self.get_melee_rect()
            melee_rect.x -= camera_x
            melee_rect.y -= camera_y
            pygame.draw.arc(surface, YELLOW, melee_rect, 0, 3.14, 3)

class Level:
    def __init__(self, level_data):
        self.width = level_data['width']
        self.height = level_data['height']
        self.theme = Theme[level_data.get('theme', 'SCIFI')]
        self.tiles = self.create_tiles(level_data['tiles'])
        self.enemies = [Enemy(e['x'], e['y'], e['type'], e.get('patrol', 200)) 
                       for e in level_data.get('enemies', [])]
        self.hazards = [Hazard(h['x'], h['y'], h['type'], h.get('width', 32), h.get('height', 32))
                       for h in level_data.get('hazards', [])]
        self.coins = [Coin(c['x'], c['y'], c.get('value', 1)) 
                     for c in level_data.get('coins', [])]
        self.powerups = [PowerUp(p['x'], p['y'], p['type']) 
                        for p in level_data.get('powerups', [])]
        self.keys = [Key(k['x'], k['y'], tuple(k['color'])) 
                    for k in level_data.get('keys', [])]
        self.portals = [Portal(p['x'], p['y'], p['dest'], tuple(p.get('color', [200, 0, 255])))
                       for p in level_data.get('portals', [])]
        self.spawn_x = level_data.get('spawn_x', 100)
        self.spawn_y = level_data.get('spawn_y', 100)
        
    def create_tiles(self, tile_data):
        tiles = []
        for tile in tile_data:
            tiles.append({
                'rect': pygame.Rect(tile['x'], tile['y'], TILE_SIZE, TILE_SIZE),
                'type': tile.get('type', 'ground'),
                'solid': tile.get('solid', True),
                'color': tuple(tile.get('color', self.get_theme_color()))
            })
        return tiles
        
    def get_theme_color(self):
        theme_colors = {
            Theme.SCIFI: (100, 100, 150),
            Theme.NATURE: (100, 150, 100),
            Theme.SPACE: (50, 50, 80),
            Theme.UNDERGROUND: (120, 80, 60),
            Theme.UNDERWATER: (50, 100, 150)
        }
        return theme_colors.get(self.theme, (100, 100, 100))

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Retro Pixel Platformer")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = GameState.MENU
        
        self.profiles = self.load_profiles()
        self.current_profile = None
        self.player = None
        self.current_level = 0
        self.levels = self.create_levels()
        self.level = None
        
        self.camera_x = 0
        self.camera_y = 0
        self.projectiles = []
        self.particles = []
        
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)
        
        self.menu_selection = 0
        self.char_selection = 0
        self.player_name = ""
        
    def create_levels(self):
        # Level 1: Tutorial/Easy Sci-Fi Level
        level1 = {
            'width': 3200,
            'height': 720,
            'theme': 'SCIFI',
            'spawn_x': 100,
            'spawn_y': 500,
            'tiles': [
                # Ground
                *[{'x': i * TILE_SIZE, 'y': 640, 'solid': True} for i in range(100)],
                # Platforms
                *[{'x': 400 + i * TILE_SIZE, 'y': 500, 'solid': True} for i in range(5)],
                *[{'x': 700 + i * TILE_SIZE, 'y': 400, 'solid': True} for i in range(4)],
                *[{'x': 1000 + i * TILE_SIZE, 'y': 300, 'solid': True} for i in range(6)],
                # Walls
                *[{'x': 1500, 'y': 640 - i * TILE_SIZE, 'solid': True} for i in range(8)],
            ],
            'enemies': [
                {'x': 600, 'y': 450, 'type': 'ground', 'patrol': 150},
                {'x': 1200, 'y': 250, 'type': 'ground', 'patrol': 100},
                {'x': 800, 'y': 300, 'type': 'flying', 'patrol': 200},
            ],
            'hazards': [
                {'x': 900, 'y': 640, 'type': 'spike'},
                {'x': 1100, 'y': 200, 'type': 'falling_block'},
                {'x': 1600, 'y': 400, 'type': 'moving_platform', 'width': 96},
            ],
            'coins': [
                *[{'x': 400 + i * 50, 'y': 450, 'value': 1} for i in range(10)],
                {'x': 1000, 'y': 250, 'value': 5},
            ],
            'powerups': [
                {'x': 750, 'y': 350, 'type': 'health'},
            ],
            'keys': [],
            'portals': [
                {'x': 2900, 'y': 550, 'dest': 1}
            ]
        }
        
        # Level 2: Nature Theme with more challenges
        level2 = {
            'width': 4000,
            'height': 720,
            'theme': 'NATURE',
            'spawn_x': 100,
            'spawn_y': 500,
            'tiles': [
                *[{'x': i * TILE_SIZE, 'y': 640, 'solid': True, 'color': (100, 150, 100)} for i in range(125)],
                *[{'x': 300 + i * TILE_SIZE, 'y': 520, 'solid': True, 'color': (80, 130, 80)} for i in range(8)],
                *[{'x': 800 + i * TILE_SIZE, 'y': 420, 'solid': True, 'color': (80, 130, 80)} for i in range(6)],
                *[{'x': 1300 + i * TILE_SIZE, 'y': 320, 'solid': True, 'color': (80, 130, 80)} for i in range(5)],
                *[{'x': 1800, 'y': 640 - i * TILE_SIZE, 'solid': True, 'color': (80, 130, 80)} for i in range(10)],
                *[{'x': 2000 + i * TILE_SIZE, 'y': 450, 'solid': True, 'color': (80, 130, 80)} for i in range(10)],
            ],
            'enemies': [
                {'x': 500, 'y': 470, 'type': 'ground', 'patrol': 200},
                {'x': 900, 'y': 370, 'type': 'ground', 'patrol': 150},
                {'x': 1100, 'y': 250, 'type': 'flying', 'patrol': 250},
                {'x': 1500, 'y': 270, 'type': 'ground', 'patrol': 100},
                {'x': 2200, 'y': 400, 'type': 'flying', 'patrol': 300},
            ],
            'hazards': [
                {'x': 700, 'y': 640, 'type': 'spike'},
                {'x': 732, 'y': 640, 'type': 'spike'},
                {'x': 1200, 'y': 220, 'type': 'falling_block'},
                {'x': 1700, 'y': 350, 'type': 'moving_platform', 'width': 96},
                {'x': 2500, 'y': 500, 'type': 'moving_platform', 'width': 128},
            ],
            'coins': [
                *[{'x': 300 + i * 60, 'y': 470, 'value': 1} for i in range(12)],
                *[{'x': 1300 + i * 60, 'y': 270, 'value': 1} for i in range(8)],
                {'x': 1100, 'y': 200, 'value': 10},
            ],
            'powerups': [
                {'x': 850, 'y': 370, 'type': 'speed'},
                {'x': 2100, 'y': 400, 'type': 'invincible'},
            ],
            'keys': [
                {'x': 3500, 'y': 590, 'color': [255, 0, 0]}
            ],
            'portals': [
                {'x': 3700, 'y': 550, 'dest': 2, 'color': [0, 255, 0]}
            ]
        }
        
        # Level 3: Space Theme - Sublevel example
        level3 = {
            'width': 3500,
            'height': 720,
            'theme': 'SPACE',
            'spawn_x': 100,
            'spawn_y': 500,
            'tiles': [
                *[{'x': i * TILE_SIZE, 'y': 640, 'solid': True, 'color': (50, 50, 80)} for i in range(110)],
                *[{'x': 400 + i * 64, 'y': 500 - i * 40, 'solid': True, 'color': (70, 70, 100)} for i in range(10)],
                *[{'x': 1500 + i * TILE_SIZE, 'y': 350, 'solid': True, 'color': (70, 70, 100)} for i in range(8)],
                *[{'x': 2200 + i * TILE_SIZE, 'y': 450, 'solid': True, 'color': (70, 70, 100)} for i in range(12)],
            ],
            'enemies': [
                {'x': 700, 'y': 300, 'type': 'flying', 'patrol': 300},
                {'x': 1000, 'y': 200, 'type': 'flying', 'patrol': 250},
                {'x': 1600, 'y': 300, 'type': 'turret'},
                {'x': 2000, 'y': 300, 'type': 'turret'},
                {'x': 2500, 'y': 400, 'type': 'ground', 'patrol': 200},
            ],
            'hazards': [
                *[{'x': 1100 + i * 64, 'y': 640, 'type': 'spike'} for i in range(5)],
                {'x': 1800, 'y': 250, 'type': 'falling_block'},
                {'x': 2100, 'y': 550, 'type': 'moving_platform', 'width': 96},
            ],
            'coins': [
                *[{'x': 500 + i * 80, 'y': 400 - i * 40, 'value': 2} for i in range(10)],
                {'x': 1600, 'y': 300, 'value': 15},
            ],
            'powerups': [
                {'x': 900, 'y': 150, 'type': 'double_jump'},
                {'x': 2300, 'y': 400, 'type': 'health'},
            ],
            'keys': [],
            'portals': [
                {'x': 3200, 'y': 550, 'dest': 0, 'color': [255, 255, 0]}  # Back to level 1 for demo
            ]
        }
        
        return [level1, level2, level3]
    
    def load_profiles(self):
        try:
            with open('profiles.json', 'r') as f:
                data = json.load(f)
                return [PlayerProfile(**p) for p in data]
        except:
            return []
    
    def save_profiles(self):
        try:
            with open('profiles.json', 'w') as f:
                data = [{'name': p.name, 'character': p.character, 
                        'total_score': p.total_score, 'levels_completed': p.levels_completed,
                        'coins_collected': p.coins_collected} for p in self.profiles]
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving profiles: {e}")
    
    def save_game(self):
        if not self.current_profile or not self.player:
            return
            
        try:
            save_data = {
                'profile_name': self.current_profile.name,
                'current_level': self.current_level,
                'player': {
                    'x': self.player.x,
                    'y': self.player.y,
                    'health': self.player.health,
                    'lives': self.player.lives,
                    'coins': self.player.coins,
                    'score': self.player.score,
                    'weapon_level': self.player.weapon_level,
                    'keys': self.player.keys
                }
            }
            with open(f'save_{self.current_profile.name}.json', 'w') as f:
                json.dump(save_data, f, indent=2)
        except Exception as e:
            print(f"Error saving game: {e}")
    
    def load_game(self):
        if not self.current_profile:
            return False
            
        try:
            with open(f'save_{self.current_profile.name}.json', 'r') as f:
                save_data = json.load(f)
                self.current_level = save_data['current_level']
                self.load_level(self.current_level)
                
                p = save_data['player']
                self.player.x = p['x']
                self.player.y = p['y']
                self.player.health = p['health']
                self.player.lives = p['lives']
                self.player.coins = p['coins']
                self.player.score = p['score']
                self.player.weapon_level = p['weapon_level']
                self.player.keys = p['keys']
                return True
        except:
            return False
    
    def load_level(self, level_index):
        if 0 <= level_index < len(self.levels):
            self.current_level = level_index
            self.level = Level(self.levels[level_index])
            if self.player:
                self.player.x = self.level.spawn_x
                self.player.y = self.level.spawn_y
            self.projectiles = []
            self.particles = []
    
    def update_camera(self):
        # Smooth camera follow
        target_x = self.player.x - SCREEN_WIDTH // 2
        target_y = self.player.y - SCREEN_HEIGHT // 2
        
        self.camera_x += (target_x - self.camera_x) * 0.1
        self.camera_y += (target_y - self.camera_y) * 0.1
        
        # Clamp camera
        self.camera_x = max(0, min(self.camera_x, self.level.width - SCREEN_WIDTH))
        self.camera_y = max(0, min(self.camera_y, self.level.height - SCREEN_HEIGHT))
    
    def handle_menu_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.menu_selection = (self.menu_selection - 1) % 3
            elif event.key == pygame.K_DOWN:
                self.menu_selection = (self.menu_selection + 1) % 3
            elif event.key == pygame.K_RETURN:
                if self.menu_selection == 0:  # New Game
                    self.state = GameState.CHAR_SELECT
                    self.player_name = ""
                elif self.menu_selection == 1:  # Load Game
                    if self.profiles:
                        self.current_profile = self.profiles[0]
                        self.player = Player(100, 100, self.current_profile.character)
                        if self.load_game():
                            self.state = GameState.PLAYING
                        else:
                            self.load_level(0)
                            self.state = GameState.PLAYING
                elif self.menu_selection == 2:  # Quit
                    self.running = False
    
    def handle_char_select_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.char_selection = (self.char_selection - 1) % 4
            elif event.key == pygame.K_RIGHT:
                self.char_selection = (self.char_selection + 1) % 4
            elif event.key == pygame.K_BACKSPACE:
                self.player_name = self.player_name[:-1]
            elif event.key == pygame.K_RETURN and len(self.player_name) > 0:
                # Create new profile
                self.current_profile = PlayerProfile(
                    name=self.player_name,
                    character=self.char_selection,
                    total_score=0,
                    levels_completed=0,
                    coins_collected=0
                )
                self.profiles.append(self.current_profile)
                self.save_profiles()
                
                # Start game
                self.player = Player(100, 100, self.char_selection)
                self.load_level(0)
                self.state = GameState.PLAYING
            elif event.unicode.isalnum() and len(self.player_name) < 15:
                self.player_name += event.unicode
    
    def handle_game_input(self, keys):
        # Jump
        if keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]:
            if not hasattr(self, 'jump_pressed') or not self.jump_pressed:
                if self.player.jump():
                    # Add jump particles
                    for _ in range(5):
                        self.particles.append(Particle(
                            self.player.x + self.player.width // 2,
                            self.player.y + self.player.height,
                            WHITE,
                            random.uniform(-2, 2),
                            random.uniform(-1, 1),
                            20
                        ))
                self.jump_pressed = True
        else:
            self.jump_pressed = False
        
        # Shoot
        if keys[pygame.K_z] or keys[pygame.K_j]:
            if self.player.shoot():
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
        
        # Melee
        if keys[pygame.K_x] or keys[pygame.K_k]:
            self.player.melee_attack()
        
        # Weapon upgrade
        if keys[pygame.K_u]:
            self.player.upgrade_weapon()
        
        # Save game
        if keys[pygame.K_F5]:
            self.save_game()
        
        # Pause
        if keys[pygame.K_ESCAPE] or keys[pygame.K_p]:
            if not hasattr(self, 'pause_pressed') or not self.pause_pressed:
                self.state = GameState.PAUSED
                self.pause_pressed = True
        else:
            self.pause_pressed = False
    
    def update_game(self, keys):
        # Update player
        self.player.update(keys, self.level.tiles, self.level.hazards)
        
        # Update level objects
        for coin in self.level.coins:
            if not coin.collected:
                coin.update()
                if self.player.get_rect().colliderect(coin.get_rect()):
                    coin.collected = True
                    self.player.coins += coin.value
                    self.player.score += coin.value * 10
                    # Coin particles
                    for _ in range(8):
                        self.particles.append(Particle(
                            coin.x + coin.width // 2,
                            coin.y + coin.height // 2,
                            YELLOW,
                            random.uniform(-3, 3),
                            random.uniform(-3, 3),
                            30
                        ))
        
        for powerup in self.level.powerups:
            if not powerup.collected:
                powerup.update()
                if self.player.get_rect().colliderect(powerup.get_rect()):
                    powerup.collected = True
                    self.player.add_powerup(powerup.type)
                    self.player.score += 50
        
        for key in self.level.keys:
            if not key.collected:
                if self.player.get_rect().colliderect(key.get_rect()):
                    key.collected = True
                    self.player.keys.append(key.color)
                    self.player.score += 100
        
        for portal in self.level.portals:
            portal.update()
            if self.player.get_rect().colliderect(portal.get_rect()):
                # Check if player has required keys (if any)
                self.load_level(portal.destination)
        
        for enemy in self.level.enemies:
            if not enemy.dead:
                enemy.update(self.level.tiles)
                
                # Check collision with player
                if self.player.get_rect().colliderect(enemy.get_rect()):
                    # Check if player is stomping
                    if self.player.dy > 0 and self.player.y + self.player.height - 10 < enemy.y + enemy.height // 2:
                        enemy.take_damage(2)
                        self.player.dy = -10
                        self.player.score += 50
                        # Enemy death particles
                        if enemy.dead:
                            for _ in range(15):
                                self.particles.append(Particle(
                                    enemy.x + enemy.width // 2,
                                    enemy.y + enemy.height // 2,
                                    RED,
                                    random.uniform(-4, 4),
                                    random.uniform(-4, 4),
                                    40
                                ))
                    else:
                        self.player.take_damage(enemy.damage)
                
                # Check melee attack
                if self.player.melee_active:
                    if self.player.get_melee_rect().colliderect(enemy.get_rect()):
                        enemy.take_damage(self.player.weapon_level + 1)
                        self.player.score += 25
        
        for hazard in self.level.hazards:
            hazard.update(self.player.get_rect())
            
            # Moving platform collision
            if hazard.type == 'moving_platform':
                if self.player.dy > 0:
                    platform_top = pygame.Rect(hazard.x, hazard.y - 5, hazard.width, 10)
                    if self.player.get_rect().colliderect(platform_top):
                        self.player.y = hazard.y - self.player.height
                        self.player.dy = 0
                        self.player.on_ground = True
                        self.player.x += hazard.direction * hazard.speed
        
        # Update projectiles
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
                    self.player.score += 10
                    break
        
        # Update particles
        self.particles = [p for p in self.particles if p.update()]
        
        # Update camera
        self.update_camera()
        
        # Check game over
        if self.player.lives < 0:
            self.state = GameState.GAME_OVER
    
    def draw_menu(self):
        self.screen.fill(BLACK)
        
        # Title
        title = self.font_large.render("RETRO PLATFORMER", True, CYAN)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 150))
        
        # Menu options
        options = ["New Game", "Load Game", "Quit"]
        for i, option in enumerate(options):
            color = YELLOW if i == self.menu_selection else WHITE
            text = self.font_medium.render(option, True, color)
            self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 350 + i * 80))
        
        # Instructions
        inst = self.font_small.render("Use Arrow Keys and ENTER", True, GRAY)
        self.screen.blit(inst, (SCREEN_WIDTH // 2 - inst.get_width() // 2, 600))
    
    def draw_char_select(self):
        self.screen.fill(BLACK)
        
        # Title
        title = self.font_large.render("CHARACTER SELECT", True, CYAN)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))
        
        # Name input
        name_text = self.font_medium.render(f"Name: {self.player_name}_", True, WHITE)
        self.screen.blit(name_text, (SCREEN_WIDTH // 2 - name_text.get_width() // 2, 200))
        
        # Characters
        colors = [BLUE, GREEN, PURPLE, ORANGE]
        for i in range(4):
            x = SCREEN_WIDTH // 2 - 250 + i * 120
            y = 350
            
            # Draw character preview
            rect = pygame.Rect(x, y, 56, 96)
            pygame.draw.rect(self.screen, colors[i], rect)
            pygame.draw.rect(self.screen, YELLOW if i == self.char_selection else WHITE, rect, 3)
            
            # Eyes
            pygame.draw.circle(self.screen, WHITE, (x + 20, y + 24), 8)
            pygame.draw.circle(self.screen, BLACK, (x + 24, y + 24), 4)
        
        # Instructions
        inst1 = self.font_small.render("Type your name, use Arrow Keys to select character", True, GRAY)
        inst2 = self.font_small.render("Press ENTER to start", True, GRAY)
        self.screen.blit(inst1, (SCREEN_WIDTH // 2 - inst1.get_width() // 2, 520))
        self.screen.blit(inst2, (SCREEN_WIDTH // 2 - inst2.get_width() // 2, 560))
    
    def draw_game(self):
        # Background
        bg_colors = {
            Theme.SCIFI: (20, 20, 40),
            Theme.NATURE: (40, 60, 40),
            Theme.SPACE: (10, 10, 20),
            Theme.UNDERGROUND: (30, 20, 15),
            Theme.UNDERWATER: (15, 30, 50)
        }
        self.screen.fill(bg_colors.get(self.level.theme, BLACK))
        
        # Draw tiles
        for tile in self.level.tiles:
            rect = pygame.Rect(
                tile['rect'].x - self.camera_x,
                tile['rect'].y - self.camera_y,
                TILE_SIZE, TILE_SIZE
            )
            if -TILE_SIZE < rect.x < SCREEN_WIDTH and -TILE_SIZE < rect.y < SCREEN_HEIGHT:
                pygame.draw.rect(self.screen, tile['color'], rect)
                pygame.draw.rect(self.screen, WHITE, rect, 1)
        
        # Draw hazards
        for hazard in self.level.hazards:
            hazard.draw(self.screen, self.camera_x, self.camera_y)
        
        # Draw coins
        for coin in self.level.coins:
            if not coin.collected:
                coin.draw(self.screen, self.camera_x, self.camera_y)
        
        # Draw powerups
        for powerup in self.level.powerups:
            if not powerup.collected:
                powerup.draw(self.screen, self.camera_x, self.camera_y)
        
        # Draw keys
        for key in self.level.keys:
            if not key.collected:
                key.draw(self.screen, self.camera_x, self.camera_y)
        
        # Draw portals
        for portal in self.level.portals:
            portal.draw(self.screen, self.camera_x, self.camera_y)
        
        # Draw enemies
        for enemy in self.level.enemies:
            enemy.draw(self.screen, self.camera_x, self.camera_y)
        
        # Draw projectiles
        for proj in self.projectiles:
            proj.draw(self.screen, self.camera_x, self.camera_y)
        
        # Draw particles
        for particle in self.particles:
            particle.draw(self.screen, self.camera_x, self.camera_y)
        
        # Draw player
        self.player.draw(self.screen, self.camera_x, self.camera_y)
        
        # HUD
        self.draw_hud()
    
    def draw_hud(self):
        # Health bar
        health_width = 200
        health_height = 20
        health_percent = self.player.health / self.player.max_health
        pygame.draw.rect(self.screen, RED, (20, 20, health_width, health_height))
        pygame.draw.rect(self.screen, GREEN, (20, 20, health_width * health_percent, health_height))
        pygame.draw.rect(self.screen, WHITE, (20, 20, health_width, health_height), 2)
        
        health_text = self.font_small.render(f"HP: {self.player.health}/{self.player.max_health}", True, WHITE)
        self.screen.blit(health_text, (230, 20))
        
        # Lives
        lives_text = self.font_small.render(f"Lives: {self.player.lives}", True, WHITE)
        self.screen.blit(lives_text, (20, 50))
        
        # Coins
        coins_text = self.font_small.render(f"Coins: {self.player.coins}", True, YELLOW)
        self.screen.blit(coins_text, (20, 80))
        
        # Score
        score_text = self.font_small.render(f"Score: {self.player.score}", True, WHITE)
        self.screen.blit(score_text, (20, 110))
        
        # Weapon level
        weapon_text = self.font_small.render(f"Weapon Lv: {self.player.weapon_level}", True, CYAN)
        self.screen.blit(weapon_text, (20, 140))
        
        # Level
        level_text = self.font_small.render(f"Level: {self.current_level + 1}", True, WHITE)
        self.screen.blit(level_text, (SCREEN_WIDTH - 150, 20))
        
        # Controls reminder
        controls = [
            "WASD/Arrows: Move",
            "Space: Jump",
            "Z: Shoot",
            "X: Melee",
            "U: Upgrade",
            "P/ESC: Pause"
        ]
        for i, ctrl in enumerate(controls):
            text = self.font_small.render(ctrl, True, GRAY)
            text.set_alpha(128)
            self.screen.blit(text, (SCREEN_WIDTH - 220, SCREEN_HEIGHT - 200 + i * 30))
    
    def draw_paused(self):
        # Draw game underneath
        self.draw_game()
        
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Paused text
        text = self.font_large.render("PAUSED", True, YELLOW)
        self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        
        inst = self.font_medium.render("Press P or ESC to resume", True, WHITE)
        self.screen.blit(inst, (SCREEN_WIDTH // 2 - inst.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
    
    def draw_game_over(self):
        self.screen.fill(BLACK)
        
        text = self.font_large.render("GAME OVER", True, RED)
        self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
        
        score_text = self.font_medium.render(f"Final Score: {self.player.score}", True, WHITE)
        self.screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
        
        inst = self.font_small.render("Press ENTER to return to menu", True, GRAY)
        self.screen.blit(inst, (SCREEN_WIDTH // 2 - inst.get_width() // 2, SCREEN_HEIGHT // 2 + 100))
    
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                if self.state == GameState.MENU:
                    self.handle_menu_input(event)
                elif self.state == GameState.CHAR_SELECT:
                    self.handle_char_select_input(event)
                elif self.state == GameState.PAUSED:
                    if event.type == pygame.KEYDOWN:
                        if event.key in [pygame.K_ESCAPE, pygame.K_p]:
                            self.state = GameState.PLAYING
                elif self.state == GameState.GAME_OVER:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        self.state = GameState.MENU
            
            # Get keys
            keys = pygame.key.get_pressed()
            
            # Update
            if self.state == GameState.PLAYING:
                self.handle_game_input(keys)
                self.update_game(keys)
            
            # Draw
            if self.state == GameState.MENU:
                self.draw_menu()
            elif self.state == GameState.CHAR_SELECT:
                self.draw_char_select()
            elif self.state == GameState.PLAYING:
                self.draw_game()
            elif self.state == GameState.PAUSED:
                self.draw_paused()
            elif self.state == GameState.GAME_OVER:
                self.draw_game_over()
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()