"""
Boss attack patterns and abilities
"""
import math
import pygame
from entities.boss import BossProjectile
from config.settings import RED, ORANGE, CYAN, PURPLE, YELLOW

class BossAttackManager:
    """Manages boss attack patterns"""
    
    @staticmethod
    def execute_attack(boss, attack_type, player, current_time):
        """
        Execute a boss attack
        Args:
            boss: Boss entity
            attack_type: Type of attack to execute
            player: Player object
            current_time: Current game time
        Returns:
            List of projectiles/effects created
        """
        attacks = {
            'projectile': BossAttackManager.projectile_single,
            'projectile_spread': BossAttackManager.projectile_spread,
            'laser': BossAttackManager.laser_beam,
            'slam': BossAttackManager.ground_slam,
            'summon': BossAttackManager.summon_minions,
            'orbital': BossAttackManager.orbital_projectiles,
        }
        
        attack_func = attacks.get(attack_type)
        if attack_func:
            return attack_func(boss, player, current_time)
        return []
        
    @staticmethod
    def projectile_single(boss, player, current_time):
        """Fire single projectile at player"""
        spawn_x, spawn_y = boss.get_projectile_spawn_point()
        
        # Calculate angle to player
        dx = player.x - spawn_x
        dy = player.y - spawn_y
        angle = math.atan2(dy, dx)
        
        projectile = BossProjectile(
            spawn_x, spawn_y,
            angle,
            speed=5,
            damage=10,
            color=boss.colors['accent']
        )
        
        return [projectile]
        
    @staticmethod
    def projectile_spread(boss, player, current_time):
        """Fire spread of projectiles"""
        spawn_x, spawn_y = boss.get_projectile_spawn_point()
        projectiles = []
        
        # Calculate base angle to player
        dx = player.x - spawn_x
        dy = player.y - spawn_y
        base_angle = math.atan2(dy, dx)
        
        # Create spread (3 or 5 projectiles based on phase)
        count = 3 if boss.phase < 3 else 5
        spread = math.pi / 6  # 30 degrees spread
        
        for i in range(count):
            offset = (i - count // 2) * (spread / count)
            angle = base_angle + offset
            
            projectile = BossProjectile(
                spawn_x, spawn_y,
                angle,
                speed=4,
                damage=8,
                color=boss.colors['accent']
            )
            projectiles.append(projectile)
            
        return projectiles
        
    @staticmethod
    def laser_beam(boss, player, current_time):
        """
        Laser beam attack (creates warning line, then laser)
        Returns laser object that game will handle
        """
        spawn_x, spawn_y = boss.get_projectile_spawn_point()
        
        # Calculate angle to player
        dx = player.x - spawn_x
        dy = player.y - spawn_y
        angle = math.atan2(dy, dx)
        
        # Create laser object (special type)
        laser = {
            'type': 'laser',
            'x': spawn_x,
            'y': spawn_y,
            'angle': angle,
            'warning_time': 60,  # 1 second warning
            'duration': 120,  # 2 second laser
            'damage': 20,
            'width': 1000,  # Long range
            'height': 10,
            'color': boss.colors['accent'],
            'age': 0
        }
        
        return [laser]
        
    @staticmethod
    def ground_slam(boss, player, current_time):
        """
        Ground slam attack - boss slams down creating shockwave
        Returns shockwave effect
        """
        # Only if boss is above player
        if boss.y > player.y:
            return []
            
        shockwave = {
            'type': 'shockwave',
            'x': boss.x + boss.width // 2,
            'y': boss.y + boss.height,
            'radius': 0,
            'max_radius': 200,
            'expansion_speed': 5,
            'damage': 15,
            'color': boss.colors['secondary'],
            'age': 0,
            'lifetime': 60
        }
        
        return [shockwave]
        
    @staticmethod
    def summon_minions(boss, player, current_time):
        """
        Summon minion enemies
        Returns minion spawn data
        """
        minions = []
        
        # Spawn 2-3 minions based on phase
        count = boss.phase + 1
        
        for i in range(count):
            # Spawn around boss
            offset_x = (i - count // 2) * 150
            minion = {
                'type': 'minion_spawn',
                'x': boss.x + offset_x,
                'y': boss.y,
                'enemy_type': 'flying',
                'age': 0,
                'spawn_delay': i * 20  # Stagger spawns
            }
            minions.append(minion)
            
        return minions
        
    @staticmethod
    def orbital_projectiles(boss, player, current_time):
        """
        Create orbiting projectiles around boss
        Phase 3 only
        """
        if boss.phase < 3:
            return []
            
        spawn_x, spawn_y = boss.get_projectile_spawn_point()
        projectiles = []
        
        # Create 6 orbiting projectiles
        for i in range(6):
            angle = (i / 6) * math.pi * 2
            radius = 80
            
            projectile = {
                'type': 'orbital',
                'center_x': spawn_x,
                'center_y': spawn_y,
                'angle': angle,
                'radius': radius,
                'speed': 0.05,  # Rotation speed
                'damage': 10,
                'color': boss.colors['accent'],
                'age': 0,
                'lifetime': 300  # 5 seconds
            }
            projectiles.append(projectile)
            
        return projectiles


class BossAttackEffect:
    """Visual and damaging effects from boss attacks"""
    
    def __init__(self, effect_data):
        """
        Args:
            effect_data: Dictionary of effect properties
        """
        self.type = effect_data['type']
        self.x = effect_data['x']
        self.y = effect_data['y']
        self.damage = effect_data.get('damage', 10)
        self.color = effect_data.get('color', RED)
        self.age = 0
        self.active = True
        
        # Type-specific properties
        if self.type == 'laser':
            self.angle = effect_data['angle']
            self.warning_time = effect_data['warning_time']
            self.duration = effect_data['duration']
            self.width = effect_data['width']
            self.height = effect_data['height']
            self.is_warning = True
            
        elif self.type == 'shockwave':
            self.radius = effect_data['radius']
            self.max_radius = effect_data['max_radius']
            self.expansion_speed = effect_data['expansion_speed']
            self.lifetime = effect_data['lifetime']
            
        elif self.type == 'orbital':
            self.center_x = effect_data['center_x']
            self.center_y = effect_data['center_y']
            self.angle = effect_data['angle']
            self.radius = effect_data['radius']
            self.speed = effect_data['speed']
            self.lifetime = effect_data['lifetime']
            
    def update(self, boss=None):
        """Update effect"""
        self.age += 1
        
        if self.type == 'laser':
            if self.is_warning and self.age >= self.warning_time:
                self.is_warning = False
                self.age = 0
            elif not self.is_warning and self.age >= self.duration:
                self.active = False
                
        elif self.type == 'shockwave':
            self.radius += self.expansion_speed
            if self.radius >= self.max_radius or self.age >= self.lifetime:
                self.active = False
                
        elif self.type == 'orbital':
            if boss:
                # Update center to boss position
                self.center_x, self.center_y = boss.get_projectile_spawn_point()
            self.angle += self.speed
            # Update position
            self.x = self.center_x + math.cos(self.angle) * self.radius
            self.y = self.center_y + math.sin(self.angle) * self.radius
            
            if self.age >= self.lifetime:
                self.active = False
                
    def get_damage_rect(self):
        """Get rectangle that deals damage"""
        if self.type == 'laser' and not self.is_warning:
            # Laser damage rectangle
            end_x = self.x + math.cos(self.angle) * self.width
            end_y = self.y + math.sin(self.angle) * self.width
            # Simplified rect (actual laser would need line collision)
            return pygame.Rect(
                min(self.x, end_x), 
                min(self.y, end_y) - self.height // 2,
                abs(end_x - self.x),
                self.height
            )
            
        elif self.type == 'shockwave':
            return pygame.Rect(
                self.x - self.radius,
                self.y - self.radius,
                self.radius * 2,
                self.radius * 2
            )
            
        elif self.type == 'orbital':
            return pygame.Rect(self.x - 8, self.y - 8, 16, 16)
            
        return pygame.Rect(0, 0, 0, 0)
        
    def draw(self, surface, camera_x, camera_y):
        """Render effect"""
        if self.type == 'laser':
            self._draw_laser(surface, camera_x, camera_y)
        elif self.type == 'shockwave':
            self._draw_shockwave(surface, camera_x, camera_y)
        elif self.type == 'orbital':
            self._draw_orbital(surface, camera_x, camera_y)
            
    def _draw_laser(self, surface, camera_x, camera_y):
        """Draw laser beam"""
        start_x = self.x - camera_x
        start_y = self.y - camera_y
        end_x = start_x + math.cos(self.angle) * self.width
        end_y = start_y + math.sin(self.angle) * self.width
        
        if self.is_warning:
            # Warning line (thin, red, blinking)
            if self.age % 10 < 5:
                pygame.draw.line(surface, (255, 0, 0, 128), 
                               (start_x, start_y), (end_x, end_y), 2)
        else:
            # Actual laser (thick, bright)
            pygame.draw.line(surface, self.color, 
                           (start_x, start_y), (end_x, end_y), self.height)
            pygame.draw.line(surface, (255, 255, 255), 
                           (start_x, start_y), (end_x, end_y), 4)
                           
    def _draw_shockwave(self, surface, camera_x, camera_y):
        """Draw expanding shockwave"""
        screen_x = int(self.x - camera_x)
        screen_y = int(self.y - camera_y)
        
        # Outer ring
        pygame.draw.circle(surface, self.color, 
                          (screen_x, screen_y), int(self.radius), 3)
        # Inner glow
        pygame.draw.circle(surface, (255, 255, 255, 128), 
                          (screen_x, screen_y), int(self.radius * 0.7), 1)
                          
    def _draw_orbital(self, surface, camera_x, camera_y):
        """Draw orbiting projectile"""
        screen_x = int(self.x - camera_x)
        screen_y = int(self.y - camera_y)
        
        pygame.draw.circle(surface, self.color, (screen_x, screen_y), 8)
        pygame.draw.circle(surface, (255, 255, 255), (screen_x, screen_y), 8, 2)