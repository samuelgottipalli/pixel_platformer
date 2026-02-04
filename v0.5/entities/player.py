"""
Player entity
"""

import pygame

from config.settings import (BLACK, CHARACTER_COLORS, GRAVITY, JUMP_POWER,
                             MAX_FALL_SPEED, MELEE_DURATION, MELEE_RANGE,
                             PLAYER_HEIGHT, PLAYER_MAX_HEALTH,
                             PLAYER_MAX_JUMPS, PLAYER_SPEED,
                             PLAYER_SPEED_BOOST_MULTIPLIER, PLAYER_START_LIVES,
                             PLAYER_WIDTH, SHOOT_BASE_COOLDOWN,
                             WALL_JUMP_POWER, WALL_JUMP_PUSH,
                             WEAPON_UPGRADE_COSTS, WHITE, YELLOW)


class Player:
    """Main player character"""

    def __init__(self, x, y, character=0, audio=None):
        """
        Args:
            x, y: Starting position
            character: Character skin index (0-3)
        """
        # Position and physics
        self.x = x
        self.y = y
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.dx = 0
        self.dy = 0
        self.direction = 1  # 1 = right, -1 = left

        # Movement state
        self.on_ground = False
        self.on_wall = False
        self.wall_direction = 0
        self.jump_count = 0
        self.max_jumps = PLAYER_MAX_JUMPS

        # Stats
        self.health = PLAYER_MAX_HEALTH
        self.max_health = PLAYER_MAX_HEALTH
        self.lives = PLAYER_START_LIVES
        self.coins = 0
        self.keys = []
        self.score = 0
        self.character = character

        # Power-ups
        self.invincible = False
        self.invincible_timer = 0
        self.speed_boost = False
        self.speed_boost_timer = 0

        # Combat
        self.weapon_level = 1
        self.can_shoot = True
        self.shoot_cooldown = 0
        self.melee_active = False
        self.melee_timer = 0

        # SFX manager
        self.audio = audio

        # Achievement tracking
        self.total_deaths = 0
        self.enemies_killed_stomp = 0
        self.enemies_killed_projectile = 0
        self.enemies_killed_melee = 0

    def update(self, keys, tiles, hazards):
        """
        Update player state
        Args:
            keys: Pygame key state
            tiles: List of tile dictionaries
            hazards: List of hazard objects
        """
        # Handle power-up timers
        self._update_timers()

        # Movement
        self._handle_movement(keys)

        # Apply gravity
        self.dy += GRAVITY
        self.dy = min(self.dy, MAX_FALL_SPEED)

        # Wall slide
        if self.on_wall and not self.on_ground and self.dy > 0:
            self.dy = min(self.dy, 2)

        # Update position with collision
        self.x += self.dx
        self._check_collision_x(tiles)

        self.y += self.dy
        self._check_collision_y(tiles)

        # Check hazards
        if not self.invincible:
            self._check_hazard_collision(hazards)

    def _update_timers(self):
        """Update all active timers"""
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

    def _handle_movement(self, keys):
        """Handle player movement input"""
        from config.controls import MOVE_LEFT, MOVE_RIGHT, check_key_pressed

        speed = PLAYER_SPEED * (
            PLAYER_SPEED_BOOST_MULTIPLIER if self.speed_boost else 1
        )

        if check_key_pressed(keys, MOVE_LEFT):
            self.dx = -speed
            self.direction = -1
        elif check_key_pressed(keys, MOVE_RIGHT):
            self.dx = speed
            self.direction = 1
        else:
            self.dx *= 0.8
            if abs(self.dx) < 0.1:
                self.dx = 0

    def _check_collision_x(self, tiles):
        """Check and resolve horizontal collisions"""
        self.on_wall = False
        player_rect = self.get_rect()

        for tile in tiles:
            if tile.get("solid", True) and player_rect.colliderect(tile["rect"]):
                if self.dx > 0:
                    self.x = tile["rect"].left - self.width
                    self.on_wall = True
                    self.wall_direction = 1
                elif self.dx < 0:
                    self.x = tile["rect"].right
                    self.on_wall = True
                    self.wall_direction = -1
                self.dx = 0

    def _check_collision_y(self, tiles):
        """Check and resolve vertical collisions"""
        self.on_ground = False
        player_rect = self.get_rect()

        for tile in tiles:
            if tile.get("solid", True) and player_rect.colliderect(tile["rect"]):
                if self.dy > 0:
                    self.y = tile["rect"].top - self.height
                    self.dy = 0
                    self.on_ground = True
                    self.jump_count = 0
                elif self.dy < 0:
                    self.y = tile["rect"].bottom
                    self.dy = 0

    def _check_hazard_collision(self, hazards):
        """Check collision with hazards"""
        from utils.enums import HazardType

        for hazard in hazards:
            if hazard.type in [HazardType.SPIKE.value, HazardType.FALLING_BLOCK.value]:
                if self.get_rect().colliderect(hazard.get_rect()):
                    self.take_damage(hazard.damage)

    def jump(self):
        """Attempt to jump. Returns True if successful"""
        if self.on_ground:
            self.dy = JUMP_POWER
            self.jump_count = 1
            if self.audio:
                self.audio.player_jump()
            return True
        elif self.on_wall:
            # Wall jump
            self.dy = WALL_JUMP_POWER
            self.dx = -self.wall_direction * WALL_JUMP_PUSH
            self.jump_count = 1
            if self.audio:
                self.audio.player_jump()
            return True
        elif self.jump_count < self.max_jumps:
            # Double jump
            self.dy = JUMP_POWER * 0.85
            self.jump_count += 1
            if self.audio:
                self.audio.player_double_jump()
            return True
        return False

    def shoot(self):
        """Attempt to shoot. Returns True if successful"""
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = SHOOT_BASE_COOLDOWN - (self.weapon_level * 5)
            if self.audio:
                self.audio.player_shoot()
            return True
        return False

    def melee_attack(self):
        """Attempt melee attack. Returns True if successful"""
        if self.melee_timer == 0:
            self.melee_active = True
            self.melee_timer = MELEE_DURATION
            if self.audio:
                self.audio.player_melee()
            return True
        return False

    def get_melee_rect(self):
        """Get melee attack hit box"""
        if self.melee_active:
            return pygame.Rect(
                self.x + (self.width if self.direction > 0 else -MELEE_RANGE),
                self.y + 10,
                MELEE_RANGE,
                28,
            )
        return pygame.Rect(0, 0, 0, 0)

    def take_damage(self, damage):
        """Take damage. Handle death if health depletes"""
        if not self.invincible:
            self.health -= damage
            if self.audio:
                self.audio.player_hurt()
            if self.health <= 0:
                self.die()

    def die(self):
        """Handle player death"""
        self.lives -= 1
        if self.audio:
            self.audio.player_die()
        self.health = self.max_health
        if self.lives >= 0:
            self.respawn()
        self.total_deaths += 1

    def respawn(self, spawn_x=100, spawn_y=100):
        """Respawn player at checkpoint"""
        self.x = spawn_x
        self.y = spawn_y
        self.dx = 0
        self.dy = 0
        self.invincible = True
        self.invincible_timer = 120

    def add_powerup(self, ptype):
        """Apply power-up effect"""
        from config.settings import (PLAYER_INVINCIBILITY_DURATION,
                                     PLAYER_SPEED_BOOST_DURATION)
        from utils.enums import PowerUpType

        if ptype == PowerUpType.HEALTH.value:
            self.health = min(self.health + 50, self.max_health)
        elif ptype == PowerUpType.DOUBLE_JUMP.value:
            self.max_jumps = 3
        elif ptype == PowerUpType.SPEED.value:
            self.speed_boost = True
            self.speed_boost_timer = PLAYER_SPEED_BOOST_DURATION
        elif ptype == PowerUpType.INVINCIBLE.value:
            self.invincible = True
            self.invincible_timer = PLAYER_INVINCIBILITY_DURATION

    def upgrade_weapon(self):
        """Upgrade weapon if player has enough coins. Returns True if successful"""
        if self.weapon_level < 4:
            cost = WEAPON_UPGRADE_COSTS.get(self.weapon_level, 999)
            if self.coins >= cost:
                self.coins -= cost
                self.weapon_level += 1
                return True
        return False

    def get_rect(self):
        """Get collision rectangle"""
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, surface, camera_x, camera_y, colorblind_mode=False):
        """Render player to screen with texture"""
        from utils.textures import TextureManager

        # Invincibility flicker
        if self.invincible and (pygame.time.get_ticks() // 100) % 2:
            return

        rect = pygame.Rect(
            self.x - camera_x, self.y - camera_y, self.width, self.height
        )

        # Body color based on character
        color = CHARACTER_COLORS[self.character % len(CHARACTER_COLORS)]

        # PATTERN: Vertical stripes for player
        TextureManager.draw_striped_rect(
            surface, rect, color, WHITE, stripe_width=3, vertical=True, colorblind_mode=colorblind_mode
        )

        # Thick border
        pygame.draw.rect(surface, WHITE, rect, 3)

        # Eyes
        eye_y = rect.y + 12
        eye_x = rect.centerx + (5 if self.direction > 0 else -10)
        pygame.draw.circle(surface, WHITE, (eye_x, eye_y), 6)
        pygame.draw.circle(surface, BLACK, (eye_x + self.direction * 2, eye_y), 3)

        # Melee effect
        if self.melee_active:
            melee_rect = self.get_melee_rect()
            melee_rect.x -= camera_x
            melee_rect.y -= camera_y
            pygame.draw.arc(surface, YELLOW, melee_rect, 0, 3.14, 3)
