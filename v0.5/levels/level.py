"""
Level class for managing level data
"""

import pygame

from config.settings import THEME_TILE_COLORS, TILE_SIZE
from entities.enemy import Enemy
from objects.collectibles import Coin, Key, PowerUp
from objects.hazards import Hazard
from objects.portal import Portal
from utils.enums import Theme


class Level:
    """Level containing all game objects"""

    def __init__(self, level_data):
        """
        Args:
            level_data: Dictionary containing level configuration
        """
        self.width = level_data["width"]
        self.height = level_data["height"]
        self.theme = Theme[level_data.get("theme", "SCIFI")]
        self.spawn_x = level_data.get("spawn_x", 100)
        self.spawn_y = level_data.get("spawn_y", 500)

        # Create all level objects from data
        self.tiles = self._create_tiles(level_data["tiles"])
        self.enemies = self._create_enemies(level_data.get("enemies", []))
        self.hazards = self._create_hazards(level_data.get("hazards", []))
        self.coins = self._create_coins(level_data.get("coins", []))
        self.powerups = self._create_powerups(level_data.get("powerups", []))
        self.keys = self._create_keys(level_data.get("keys", []))
        self.portals = self._create_portals(level_data.get("portals", []))

    def _create_tiles(self, tile_data):
        """Create tile list from data with textures"""
        from utils.textures import TextureManager

        tiles = []
        default_color = THEME_TILE_COLORS.get(self.theme.name, (100, 100, 100))

        for tile in tile_data:
            tile_dict = {
                "rect": pygame.Rect(tile["x"], tile["y"], TILE_SIZE, TILE_SIZE),
                "type": tile.get("type", "ground"),
                "solid": tile.get("solid", True),
                "color": tuple(tile.get("color", default_color)),
                "theme": self.theme.name,  # Add theme for drawing
            }
            tiles.append(tile_dict)

        return tiles

    def _create_enemies(self, enemy_data):
        """Create enemy list from data"""
        return [
            Enemy(e["x"], e["y"], e["type"], e.get("patrol", 200)) for e in enemy_data
        ]

    def _create_hazards(self, hazard_data):
        """Create hazard list from data"""
        return [
            Hazard(h["x"], h["y"], h["type"], h.get("width", 32), h.get("height", 32))
            for h in hazard_data
        ]

    def _create_coins(self, coin_data):
        """Create coin list from data"""
        return [Coin(c["x"], c["y"], c.get("value", 1)) for c in coin_data]

    def _create_powerups(self, powerup_data):
        """Create power-up list from data"""
        return [PowerUp(p["x"], p["y"], p["type"]) for p in powerup_data]

    def _create_keys(self, key_data):
        """Create key list from data"""
        return [Key(k["x"], k["y"], tuple(k["color"])) for k in key_data]

    def _create_portals(self, portal_data):
        """Create portal list from data"""
        portals = []
        for p in portal_data:
            color = tuple(p["color"]) if "color" in p else None
            keys = p.get("required_keys", [])
            portals.append(Portal(p["x"], p["y"], p["dest"], color, keys))
        return portals

    def get_background_color(self):
        """Get background color for this theme"""
        from config.settings import THEME_BACKGROUNDS

        return THEME_BACKGROUNDS.get(self.theme.name, (0, 0, 0))

    def reset(self):
        """Reset level state (respawn collectibles, etc.)"""
        from config.settings import ENEMY_BASE_HEALTH

        for coin in self.coins:
            coin.collected = False
        for powerup in self.powerups:
            powerup.collected = False
        for key in self.keys:
            key.collected = False
        for enemy in self.enemies:
            enemy.dead = False
            enemy.health = ENEMY_BASE_HEALTH
            enemy.x = enemy.start_x
            enemy.y = enemy.start_y
