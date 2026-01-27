"""
Game Settings and Constants
"""

# Screen Settings
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
TILE_SIZE = 32

# Physics
GRAVITY = 0.8
MAX_FALL_SPEED = 15
PLAYER_SPEED = 6
JUMP_POWER = -15
WALL_JUMP_POWER = -14
WALL_JUMP_PUSH = 8

# Player Settings
PLAYER_WIDTH = 28
PLAYER_HEIGHT = 48
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
CYAN = (100, 200, 220)  # Soft cyan
ORANGE = (230, 140, 70)  # Soft orange

# UI-specific Colors
UI_BG = (25, 25, 35)  # UI background
UI_BORDER = (100, 100, 120)  # UI borders
UI_HIGHLIGHT = (120, 180, 240)  # Selection highlight
UI_TEXT = (220, 220, 230)  # Primary text
UI_TEXT_DIM = (150, 150, 160)  # Secondary text

# Theme Background Colors (slightly muted)
THEME_BACKGROUNDS = {
    "SCIFI": (15, 20, 35),
    "NATURE": (30, 45, 35),
    "SPACE": (8, 8, 18),
    "UNDERGROUND": (25, 18, 15),
    "UNDERWATER": (12, 25, 45),
}

# Theme Tile Colors (muted)
THEME_TILE_COLORS = {
    "SCIFI": (85, 90, 130),
    "NATURE": (80, 120, 85),
    "SPACE": (45, 45, 75),
    "UNDERGROUND": (100, 70, 55),
    "UNDERWATER": (45, 85, 120),
}

# Character Colors (slightly muted)
CHARACTER_COLORS = [
    (90, 150, 230),  # Blue
    (80, 200, 120),  # Green
    (180, 100, 220),  # Purple
    (230, 140, 70),  # Orange
]

# Legacy colors for compatibility
DARK_BLUE = (30, 50, 100)
DARK_GREEN = (40, 100, 60)

# Enemy Settings
ENEMY_GROUND_SPEED = 2
ENEMY_FLYING_SPEED = 2
ENEMY_BASE_HEALTH = 3
ENEMY_BASE_DAMAGE = 1
ENEMY_SHOOT_COOLDOWN = 120

# Score Values
SCORE_COIN = 10
SCORE_ENEMY_KILL = 50
SCORE_ENEMY_HIT = 10
SCORE_MELEE_HIT = 25
SCORE_POWERUP = 50
SCORE_KEY = 100

# Paths
SAVE_DIR = "data/saves"
PROFILES_FILE = "data/profiles.json"
LEVELS_DIR = "levels/data"
