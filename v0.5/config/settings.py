"""
Game Settings and Constants
NOW USING LAYOUT MANAGER FOR RESOLUTION-BASED SCALING
"""

from config.layout_manager import LayoutManager, get_layout, get_screen_size

# Screen Settings - Now Dynamic!
# These will be updated when LayoutManager loads
SCREEN_WIDTH = 1280  # Default, will be updated
SCREEN_HEIGHT = 720  # Default, will be updated
FPS = 60
TILE_SIZE = 32  # Default, will be updated

# # Player/Enemy dimensions - backward compatibility
# # These will be updated when layout loads
# PLAYER_WIDTH = 28  # Default
# PLAYER_HEIGHT = 48  # Default
# ENEMY_WIDTH = 32  # Default
# ENEMY_HEIGHT = 32  # Default


def update_screen_size(width, height):
    """
    Update screen dimensions and load appropriate layout
    Called when resolution changes
    """
    # global SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE
    # global PLAYER_WIDTH, PLAYER_HEIGHT, ENEMY_WIDTH, ENEMY_HEIGHT

    # Load layout for this resolution
    LayoutManager.load_layout(width, height)

    # Update globals
    # SCREEN_WIDTH = width
    # SCREEN_HEIGHT = height

    # Update tile size from layout
    tile_config = LayoutManager.get_object_size("tile")
    if tile_config:
        TILE_SIZE = tile_config.get("size", 32)

    # Update player dimensions
    player_config = LayoutManager.get_object_size("player")
    if player_config:
        PLAYER_WIDTH = player_config["width"]
        PLAYER_HEIGHT = player_config["height"]

    # Update enemy dimensions
    enemy_config = LayoutManager.get_object_size("enemy")
    if enemy_config:
        ENEMY_WIDTH = enemy_config["width"]
        ENEMY_HEIGHT = enemy_config["height"]


def get_screen_width():
    """Get current screen width from layout"""
    return LayoutManager.get("screen", "width") or SCREEN_WIDTH


def get_screen_height():
    """Get current screen height from layout"""
    return LayoutManager.get("screen", "height") or SCREEN_HEIGHT


# Physics - These don't scale with resolution
GRAVITY = 0.8
MAX_FALL_SPEED = 15
PLAYER_SPEED = 6
JUMP_POWER = -15
WALL_JUMP_POWER = -14
WALL_JUMP_PUSH = 8

# Player Settings - Now using layout for dimensions
PLAYER_MAX_HEALTH = 100
PLAYER_START_LIVES = 3
PLAYER_MAX_JUMPS = 2
PLAYER_INVINCIBILITY_DURATION = 120  # frames
PLAYER_SPEED_BOOST_DURATION = 600  # frames
PLAYER_SPEED_BOOST_MULTIPLIER = 1.5

# Combat
SHOOT_BASE_COOLDOWN = 30  # frames
MELEE_DURATION = 20  # frames
MELEE_RANGE = 32

# Weapon Upgrade Costs
WEAPON_UPGRADE_COSTS = {
    1: 20,  # Level 1 -> 2: 20 coins
    2: 50,  # Level 2 -> 3: 50 coins
    3: 100,  # Level 3 -> 4: 100 coins
    4: 999,  # Level 4 is max
}

# Difficulty Settings
DIFFICULTY_MODIFIERS = {
    "EASY": {
        "lives": 5,
        "enemy_count_multiplier": 0.7,  # 70% of normal enemy count
        "enemy_damage_multiplier": 0.7,
        "coin_multiplier": 1.5,
        "powerup_multiplier": 1.5,
        "weapon_upgrade_cost_multiplier": 0.7,
        "time_limit_multiplier": 2.0,  # 2x more time
        "score_multiplier": 1.0,
    },
    "NORMAL": {
        "lives": 3,
        "enemy_count_multiplier": 1.0,
        "enemy_damage_multiplier": 1.0,
        "coin_multiplier": 1.0,
        "powerup_multiplier": 1.0,
        "weapon_upgrade_cost_multiplier": 1.0,
        "time_limit_multiplier": 1.0,
        "score_multiplier": 1.5,
    },
    "HARD": {
        "lives": 1,
        "enemy_count_multiplier": 1.5,
        "enemy_damage_multiplier": 1.5,
        "coin_multiplier": 0.7,
        "powerup_multiplier": 0.6,
        "weapon_upgrade_cost_multiplier": 1.5,
        "time_limit_multiplier": 0.5,
        "score_multiplier": 2.0,
    },
}

# Progressive difficulty scaling
# As player progresses through levels, difficulty increases
# Last level of EASY = First level of NORMAL difficulty
# Last level of NORMAL = First level of HARD difficulty
PROGRESSIVE_DIFFICULTY_ENABLED = True
PROGRESSIVE_DIFFICULTY_CURVE = 0.5  # How much harder each level gets (0-1)

# Modern Color Palette - Muted and Professional
BLACK = (15, 15, 20)  # Soft black
WHITE = (240, 240, 245)  # Soft white
GRAY = (120, 120, 130)  # Medium gray
LIGHT_GRAY = (180, 180, 190)  # Light gray
DARK_GRAY = (60, 60, 70)  # Dark gray

# Accent Colors - Softer, less saturated
RED = (220, 80, 80)  # Soft red
GREEN = (80, 200, 120)  # Soft green
BLUE = (90, 150, 230)  # Soft blue
YELLOW = (240, 200, 80)  # Soft yellow
PURPLE = (180, 100, 220)  # Soft purple
CYAN = (80, 200, 230)  # Soft cyan
ORANGE = (240, 140, 80)  # Soft orange

# UI Colors
UI_BG = (25, 25, 35)  # Dark background
UI_BORDER = (100, 100, 120)  # Border color
UI_HIGHLIGHT = (140, 180, 240)  # Highlight color
UI_TEXT = WHITE  # Main text
UI_TEXT_DIM = LIGHT_GRAY  # Dimmed text

# Theme Tile Colors (muted)
THEME_TILE_COLORS = {
    "SCIFI": (85, 90, 130),
    "NATURE": (80, 120, 85),
    "SPACE": (45, 45, 75),
    "UNDERGROUND": (100, 70, 55),
    "UNDERWATER": (45, 85, 120),
}

# Enemy Colors
ENEMY_GROUND_COLOR = RED
ENEMY_FLYING_COLOR = PURPLE
ENEMY_TURRET_COLOR = ORANGE

# Scoring
SCORE_COIN = 10
SCORE_POWERUP = 50
SCORE_KEY = 100
SCORE_ENEMY_HIT = 5
SCORE_ENEMY_KILL = 25
SCORE_MELEE_HIT = 10
SCORE_BOSS_HIT = 50

# Enemy Settings
ENEMY_GROUND_SPEED = 2
ENEMY_FLYING_SPEED = 2
ENEMY_BASE_HEALTH = 3
ENEMY_BASE_DAMAGE = 1
ENEMY_SHOOT_COOLDOWN = 120  # frames (~2 seconds)

# Character Colors
CHARACTER_COLORS = [
    (100, 150, 250),  # Blue
    (250, 100, 100),  # Red
    (100, 250, 150),  # Green
    (250, 200, 100),  # Yellow
]

# Paths
SAVE_DIR = "data/saves"
PROFILES_FILE = "data/profiles.json"
LEVELS_DIR = "levels/data"
