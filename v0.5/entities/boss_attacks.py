"""
Boss attack patterns and abilities
"""

import math

import pygame
from config.settings import RED
from entities.boss import BossProjectile


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
            "projectile": BossAttackManager.projectile_single,
            "projectile_spread": BossAttackManager.projectile_spread,
            "slam": BossAttackManager.ground_slam,
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
            spawn_x, spawn_y, angle, speed=5, damage=10, color=boss.colors["accent"]
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
                spawn_x, spawn_y, angle, speed=4, damage=8, color=boss.colors["accent"]
            )
            projectiles.append(projectile)

        return projectiles

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
            "type": "shockwave",
            "x": boss.x + boss.width // 2,
            "y": boss.y + boss.height,
            "radius": 0,
            "max_radius": 200,
            "expansion_speed": 5,
            "damage": 15,
            "color": boss.colors["secondary"],
            "age": 0,
            "lifetime": 60,
        }

        return [shockwave]


class BossAttackEffect:
    """Visual and damaging effects from boss attacks"""

    def __init__(self, effect_data):
        """
        Args:
            effect_data: Dictionary of effect properties
        """
        self.type = effect_data["type"]
        self.x = effect_data["x"]
        self.y = effect_data["y"]
        self.damage = effect_data.get("damage", 10)
        self.color = effect_data.get("color", RED)
        self.age = 0
        self.active = True

        # Type-specific properties
        if self.type == "shockwave":
            self.radius = effect_data["radius"]
            self.max_radius = effect_data["max_radius"]
            self.expansion_speed = effect_data["expansion_speed"]
            self.lifetime = effect_data["lifetime"]

    def update(self, boss=None):
        """Update effect"""
        self.age += 1

        if self.type == "shockwave":
            self.radius += self.expansion_speed
            if self.radius >= self.max_radius or self.age >= self.lifetime:
                self.active = False

    def get_damage_rect(self):
        """Get rectangle that deals damage"""
        if self.type == "shockwave":
            return pygame.Rect(
                self.x - self.radius,
                self.y - self.radius,
                self.radius * 2,
                self.radius * 2,
            )

        return pygame.Rect(0, 0, 0, 0)

    def draw(self, surface, camera_x, camera_y):
        """Render effect"""
        if self.type == "shockwave":
            self._draw_shockwave(surface, camera_x, camera_y)

    def _draw_shockwave(self, surface, camera_x, camera_y):
        """Draw expanding shockwave"""
        screen_x = int(self.x - camera_x)
        screen_y = int(self.y - camera_y)

        # Outer ring
        pygame.draw.circle(
            surface, self.color, (screen_x, screen_y), int(self.radius), 3
        )
        # Inner glow
        pygame.draw.circle(
            surface,
            (255, 255, 255, 128),
            (screen_x, screen_y),
            int(self.radius * 0.7),
            1,
        )
