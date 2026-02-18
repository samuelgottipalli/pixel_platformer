"""
Weapon System
All weapon types with power and speed upgrades
"""

import math
import pygame

from config.weapon_catalog import (get_weapon_power_upgrade,
                                   get_weapon_speed_upgrade, get_weapon_info)
from config.settings import YELLOW, ORANGE, RED, CYAN, WHITE


class Weapon:
    """Base weapon class"""
    
    def __init__(self, weapon_id, power_level=1, speed_level=1):
        """
        Initialize weapon
        
        Args:
            weapon_id: Weapon type ('standard', 'dual_back', etc.)
            power_level: Current power upgrade level (1-4)
            speed_level: Current speed upgrade level (1-3)
        """
        self.weapon_id = weapon_id
        self.power_level = power_level
        self.speed_level = speed_level
        
        # Get weapon info from catalog
        self.info = get_weapon_info(weapon_id)
        self.name = self.info["name"]
        self.type = self.info["type"]
        
        # Get current upgrade stats
        self._update_stats()
    
    def _update_stats(self):
        """Update weapon stats based on current levels"""
        power_data = get_weapon_power_upgrade(self.weapon_id, self.power_level)
        speed_data = get_weapon_speed_upgrade(self.weapon_id, self.speed_level)
        
        self.damage = power_data.get("damage", 10)
        self.speed = speed_data.get("speed", 8)
        
        # Store additional stats (weapon-specific)
        self.power_data = power_data
        self.speed_data = speed_data
    
    def upgrade_power(self):
        """Upgrade power level"""
        if self.power_level < self.info["power_max"]:
            self.power_level += 1
            self._update_stats()
            return True
        return False
    
    def upgrade_speed(self):
        """Upgrade speed level"""
        if self.speed_level < self.info["speed_max"]:
            self.speed_level += 1
            self._update_stats()
            return True
        return False
    
    def get_power_upgrade_cost(self):
        """Get cost of next power upgrade"""
        if self.power_level < self.info["power_max"]:
            next_upgrade = get_weapon_power_upgrade(self.weapon_id, self.power_level + 1)
            return next_upgrade["cost"]
        return None  # Already maxed
    
    def get_speed_upgrade_cost(self):
        """Get cost of next speed upgrade"""
        if self.speed_level < self.info["speed_max"]:
            next_upgrade = get_weapon_speed_upgrade(self.weapon_id, self.speed_level + 1)
            return next_upgrade["cost"]
        return None  # Already maxed
    
    def create_projectiles(self, player_x, player_y, player_width, player_height, direction):
        """
        Create projectiles when weapon fires
        
        Args:
            player_x, player_y: Player position
            player_width, player_height: Player dimensions
            direction: Player facing direction (1 or -1)
        
        Returns:
            List of Projectile objects
        """
        raise NotImplementedError("Subclasses must implement create_projectiles")
    
    def get_cooldown(self):
        """Get shoot cooldown for this weapon"""
        # Base cooldown, can be modified by weapon type
        base_cooldown = 15  # frames
        return base_cooldown


class StandardWeapon(Weapon):
    """Standard single shot weapon"""
    
    def create_projectiles(self, player_x, player_y, player_width, player_height, direction):
        """Create single forward projectile"""
        from entities.projectile import Projectile
        
        # Spawn position
        if direction > 0:
            spawn_x = player_x + player_width
        else:
            spawn_x = player_x
        spawn_y = player_y + player_height // 2
        
        # Create projectile
        projectile = Projectile(
            spawn_x,
            spawn_y,
            direction,
            speed=self.speed,
            damage=self.damage,
            color=YELLOW
        )
        
        return [projectile]


class DualBackWeapon(Weapon):
    """Dual shot - forward and backward"""
    
    def create_projectiles(self, player_x, player_y, player_width, player_height, direction):
        """Create forward and backward projectiles"""
        from entities.projectile import Projectile
        
        projectiles = []
        spawn_y = player_y + player_height // 2
        
        # Forward shot
        spawn_x_forward = player_x + player_width if direction > 0 else player_x
        proj_forward = Projectile(
            spawn_x_forward,
            spawn_y,
            direction,
            speed=self.speed,
            damage=self.damage,
            color=CYAN
        )
        projectiles.append(proj_forward)
        
        # Backward shot
        spawn_x_back = player_x if direction > 0 else player_x + player_width
        proj_back = Projectile(
            spawn_x_back,
            spawn_y,
            -direction,  # Opposite direction
            speed=self.speed,
            damage=self.damage,
            color=CYAN
        )
        projectiles.append(proj_back)
        
        return projectiles


class SpreadWeapon(Weapon):
    """Spread shot - multiple projectiles in arc"""
    
    def create_projectiles(self, player_x, player_y, player_width, player_height, direction):
        """Create spread pattern projectiles"""
        from entities.projectile import Projectile
        
        projectiles = []
        
        # Get spread parameters from power upgrade
        count = self.power_data.get("count", 3)
        spread_degrees = self.power_data.get("spread", 30)
        
        # Spawn position
        if direction > 0:
            spawn_x = player_x + player_width
        else:
            spawn_x = player_x
        spawn_y = player_y + player_height // 2
        
        # Create spread pattern
        if count == 1:
            # Just shoot straight
            angles = [0]
        else:
            # Calculate angles
            spread_radians = math.radians(spread_degrees)
            angles = []
            for i in range(count):
                # Distribute evenly across spread
                angle_offset = (i / (count - 1) - 0.5) * spread_radians
                angles.append(angle_offset)
        
        # Create projectiles at each angle
        for angle in angles:
            projectile = Projectile(
                spawn_x,
                spawn_y,
                direction,
                speed=self.speed,
                damage=self.damage,
                color=ORANGE,
                angle=angle if direction > 0 else math.pi - angle
            )
            projectiles.append(projectile)
        
        return projectiles


class DualFrontWeapon(Weapon):
    """Dual front - two powerful forward shots"""
    
    def create_projectiles(self, player_x, player_y, player_width, player_height, direction):
        """Create two forward projectiles with vertical offset"""
        from entities.projectile import Projectile
        
        projectiles = []
        
        # Get offset from power upgrade
        offset = self.power_data.get("offset", 10)
        
        # Spawn position
        if direction > 0:
            spawn_x = player_x + player_width
        else:
            spawn_x = player_x
        center_y = player_y + player_height // 2
        
        # Top projectile
        proj_top = Projectile(
            spawn_x,
            center_y - offset,
            direction,
            speed=self.speed,
            damage=self.damage,
            color=RED
        )
        projectiles.append(proj_top)
        
        # Bottom projectile
        proj_bottom = Projectile(
            spawn_x,
            center_y + offset,
            direction,
            speed=self.speed,
            damage=self.damage,
            color=RED
        )
        projectiles.append(proj_bottom)
        
        return projectiles


class ExplosiveWeapon(Weapon):
    """Timed explosion - throwable bomb"""
    
    def create_projectiles(self, player_x, player_y, player_width, player_height, direction):
        """Create explosive projectile"""
        from entities.explosive_projectile import ExplosiveProjectile
        
        # Get explosion parameters
        explosion_damage = self.damage
        explosion_radius = self.power_data.get("radius", 50)
        fuse_time = self.speed_data.get("fuse", 2.0)
        throw_speed = self.speed_data.get("throw_speed", 6)
        
        # Spawn position
        if direction > 0:
            spawn_x = player_x + player_width
        else:
            spawn_x = player_x
        spawn_y = player_y + player_height // 2
        
        # Create explosive
        explosive = ExplosiveProjectile(
            spawn_x,
            spawn_y,
            direction,
            throw_speed=throw_speed,
            fuse_time=fuse_time,
            damage=explosion_damage,
            radius=explosion_radius
        )
        
        return [explosive]
    
    def get_cooldown(self):
        """Explosives have longer cooldown"""
        return 45  # 0.75 seconds at 60 FPS


# ============================================================
# WEAPON FACTORY
# ============================================================

def create_weapon(weapon_id, power_level=1, speed_level=1):
    """
    Factory function to create weapon instances
    
    Args:
        weapon_id: Weapon type identifier
        power_level: Power upgrade level
        speed_level: Speed upgrade level
    
    Returns:
        Weapon instance
    """
    weapon_classes = {
        "standard": StandardWeapon,
        "dual_back": DualBackWeapon,
        "spread": SpreadWeapon,
        "dual_front": DualFrontWeapon,
        "explosive": ExplosiveWeapon
    }
    
    weapon_class = weapon_classes.get(weapon_id)
    if weapon_class:
        return weapon_class(weapon_id, power_level, speed_level)
    
    # Default to standard if unknown
    return StandardWeapon("standard", power_level, speed_level)
