"""
Game Settings and Constants
NOW USING LAYOUT MANAGER FOR RESOLUTION-BASED SCALING
"""

from config.layout_manager import LayoutManager

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


# Physics Settings
def get_gravity():
    return LayoutManager.get_physics("gravity") or 0.8


def get_max_fall_speed():
    return LayoutManager.get_physics("max_fall_speed") or 15


def get_player_speed():
    return LayoutManager.get_physics("player_speed") or 5


def get_jump_power():
    return LayoutManager.get_physics("jump_power") or -12


def get_wall_jump_power():
    return LayoutManager.get_physics("wall_jump_power") or -14


def get_wall_jump_push():
    return LayoutManager.get_physics("wall_jump_push") or 8


# Player Settings - Now using layout for dimensions
PLAYER_MAX_HEALTH = 100
PLAYER_START_LIVES = 3
PLAYER_MAX_JUMPS = 2
PLAYER_INVINCIBILITY_DURATION = 120  # frames
PLAYER_HURT_INVULNERABILITY = 60  # frames of invulnerability after taking a hit
PLAYER_SPEED_BOOST_DURATION = 600  # frames
PLAYER_SPEED_BOOST_MULTIPLIER = 1.5


# Combat
SHOOT_BASE_COOLDOWN = 30  # frames
MELEE_DURATION = 20  # frames
def get_melee_range():
    return LayoutManager.get_physics("melee_range") or 40

def get_projectile_speed():
    return LayoutManager.get_physics("projectile_speed") or 8

# Melee / stomp damage (guns are upgraded in the shop, see weapon_catalog.py)
MELEE_DAMAGE = 15
STOMP_DAMAGE = 20

# Difficulty Settings
DIFFICULTY_MODIFIERS = {
    "EASY": {
        "lives": 5,
        "enemy_count_multiplier": 0.7,  # 70% of normal enemy count
        "enemy_damage_multiplier": 0.7,
        "enemy_health_multiplier": 0.75,
        "enemy_speed_multiplier": 0.9,
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
        "enemy_health_multiplier": 1.0,
        "enemy_speed_multiplier": 1.0,
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
        "enemy_health_multiplier": 1.4,
        "enemy_speed_multiplier": 1.15,
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

# Soft color palette - low glare on dark backgrounds.
# Hues stay clearly distinct (and every entity also has its own pattern for
# colorblind players); only brightness/saturation are toned down.
BLACK = (15, 15, 20)
WHITE = (214, 214, 222)  # soft white for text and highlights
GRAY = (115, 115, 125)
LIGHT_GRAY = (160, 160, 172)
DARK_GRAY = (58, 58, 68)

# Accent colors
RED = (196, 92, 92)
GREEN = (92, 176, 120)
BLUE = (96, 140, 200)
YELLOW = (212, 182, 92)
PURPLE = (160, 112, 196)
CYAN = (92, 172, 198)
ORANGE = (208, 138, 92)

# Lighter tints used for texture patterns on top of the accent colors
PATTERN_RED = (222, 132, 132)
PATTERN_YELLOW = (224, 208, 140)
PATTERN_CYAN = (150, 202, 218)
PATTERN_ORANGE = (224, 174, 126)
PATTERN_MAGENTA = (206, 150, 206)
PATTERN_LIGHT_BLUE = (140, 170, 212)
WARNING_YELLOW = (220, 194, 90)  # hazard stripes / spike outlines

# Outlines drawn around entities and tiles (instead of bright white)
OUTLINE = (150, 150, 165)
TILE_OUTLINE = (104, 108, 140)

# UI Colors
UI_BG = (28, 28, 38)
UI_BORDER = (78, 80, 98)
UI_HIGHLIGHT = (118, 152, 204)
UI_SELECTED_BG = (40, 46, 66)  # fill for the selected button (text stays readable)
UI_TEXT = WHITE
UI_TEXT_DIM = LIGHT_GRAY

# Theme Tile Colors (muted) and their pattern accents
THEME_TILE_COLORS = {
    "SCIFI": (78, 82, 118),
    "NATURE": (76, 110, 80),
    "SPACE": (45, 45, 75),
    "UNDERGROUND": (96, 70, 56),
    "UNDERWATER": (45, 80, 112),
}
THEME_TILE_PATTERNS = {
    "SCIFI": (112, 116, 152),
    "NATURE": (110, 140, 112),
    "SPACE": (100, 100, 140),
    "UNDERGROUND": (80, 60, 40),
    "UNDERWATER": (86, 120, 156),
}

# Sci-fi background layers
SCIFI_BG = (18, 18, 32)
SCIFI_GRID = (32, 34, 58)
SCIFI_NODE = (50, 54, 90)

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
def get_enemy_ground_speed():
    return LayoutManager.get_physics("enemy_ground_speed") or 2

def get_enemy_flying_speed():
    return LayoutManager.get_physics("enemy_flying_speed") or 2

# Base enemy stats on the tutorial level (Normal difficulty).
# Health is in weapon-damage units: the Standard Shot does 10 per hit.
ENEMY_BASE_HEALTH = 20
ENEMY_BASE_DAMAGE = 10  # contact damage per hit
SPIKE_DAMAGE = 15
FALLING_BLOCK_DAMAGE = 20
ENEMY_SHOOT_COOLDOWN = 120  # frames (~2 seconds) between turret shots
ENEMY_PROJECTILE_BASE_DAMAGE = 8  # turret shot damage
ENEMY_MIN_SHOOT_COOLDOWN = 50  # fastest turret fire rate

# Enemies and their weapons get tougher every level.
# Each value is the increase per level index (0.25 = +25% per level),
# applied on top of the difficulty multipliers in DIFFICULTY_MODIFIERS.
# Example, Normal: enemy health 20 on the tutorial -> 45 on Level 5.
ENEMY_LEVEL_SCALING = {
    "health": 0.25,
    "damage": 0.15,             # contact damage
    "speed": 0.08,              # patrol speed
    "projectile_damage": 0.15,  # turret shots
    "projectile_speed": 0.06,
    "fire_rate": 0.08,          # turret cooldown shrinks by this much per level
}

# Character Colors
CHARACTER_COLORS = [
    (96, 136, 212),  # Blue
    (212, 104, 104),  # Red
    (100, 196, 138),  # Green
    (212, 178, 100),  # Yellow
]

# Paths
SAVE_DIR = "data/saves"
PROFILES_FILE = "data/profiles.json"
LEVELS_DIR = "levels/data"
