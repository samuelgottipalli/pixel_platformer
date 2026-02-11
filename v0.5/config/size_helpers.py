"""
Config helpers for backward compatibility
Provides constants that now come from LayoutManager
"""

from config.layout_manager import LayoutManager


def get_player_width():
    """Get player width from layout"""
    size = LayoutManager.get_object_size('player')
    return size['width'] if size else 28


def get_player_height():
    """Get player height from layout"""
    size = LayoutManager.get_object_size('player')
    return size['height'] if size else 48


def get_enemy_size():
    """Get enemy dimensions from layout"""
    size = LayoutManager.get_object_size('enemy')
    return (size['width'], size['height']) if size else (32, 32)


def get_projectile_size():
    """Get projectile dimensions from layout"""
    size = LayoutManager.get_object_size('projectile')
    return (size['width'], size['height']) if size else (12, 6)


def get_tile_size():
    """Get tile size from layout"""
    size = LayoutManager.get_object_size('tile')
    return size['size'] if size else 32


def get_coin_size():
    """Get coin dimensions from layout"""
    size = LayoutManager.get_object_size('coin')
    return (size['width'], size['height']) if size else (16, 16)


def get_powerup_size():
    """Get powerup dimensions from layout"""
    size = LayoutManager.get_object_size('powerup')
    return (size['width'], size['height']) if size else (24, 24)


def get_portal_size():
    """Get portal dimensions from layout"""
    size = LayoutManager.get_object_size('portal')
    return (size['width'], size['height']) if size else (48, 64)


def get_key_size():
    """Get key dimensions from layout"""
    size = LayoutManager.get_object_size('key')
    return (size['width'], size['height']) if size else (24, 24)


def get_boss_size():
    """Get boss dimensions from layout"""
    size = LayoutManager.get_object_size('boss')
    return (size['width'], size['height']) if size else (120, 120)


# For easier importing - create module-level constants
# These get initialized when layout loads
PLAYER_WIDTH = 28  # Will be updated
PLAYER_HEIGHT = 48  # Will be updated
ENEMY_WIDTH = 32  # Will be updated
ENEMY_HEIGHT = 32  # Will be updated


def update_size_constants():
    """Update module constants from layout (called after layout loads)"""
    global PLAYER_WIDTH, PLAYER_HEIGHT, ENEMY_WIDTH, ENEMY_HEIGHT
    
    player = LayoutManager.get_object_size('player')
    if player:
        PLAYER_WIDTH = player['width']
        PLAYER_HEIGHT = player['height']
    
    enemy = LayoutManager.get_object_size('enemy')
    if enemy:
        ENEMY_WIDTH = enemy['width']
        ENEMY_HEIGHT = enemy['height']
