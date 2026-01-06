"""
Enumerations used throughout the game
"""
from enum import Enum

class GameState(Enum):
    """Game state machine states"""
    MENU = 1
    DIFFICULTY_SELECT = 2  # NEW - Added in fixes
    PROFILE_SELECT = 3
    CHAR_SELECT = 4
    LEVEL_SELECT = 5  # NEW - Add this line
    PLAYING = 6
    PAUSED = 7
    GAME_OVER = 8
    LEVEL_COMPLETE = 9
    VICTORY = 10

class Theme(Enum):
    """Level themes"""
    SCIFI = 1
    NATURE = 2
    SPACE = 3
    UNDERGROUND = 4
    UNDERWATER = 5

class EnemyType(Enum):
    """Types of enemies"""
    GROUND = "ground"
    FLYING = "flying"
    TURRET = "turret"

class HazardType(Enum):
    """Types of hazards"""
    SPIKE = "spike"
    FALLING_BLOCK = "falling_block"
    MOVING_PLATFORM = "moving_platform"

class PowerUpType(Enum):
    """Types of power-ups"""
    HEALTH = "health"
    DOUBLE_JUMP = "double_jump"
    SPEED = "speed"
    INVINCIBLE = "invincible"

class Difficulty(Enum):
    """Game difficulty levels"""
    EASY = "EASY"
    NORMAL = "NORMAL"
    HARD = "HARD"
