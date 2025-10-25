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
PLAYER_SPEED_BOOST_DURATION = 600    # frames
PLAYER_SPEED_BOOST_MULTIPLIER = 1.5

# Combat
SHOOT_BASE_COOLDOWN = 30  # frames
MELEE_DURATION = 20       # frames
MELEE_RANGE = 32

# Weapon Upgrade Costs
WEAPON_UPGRADE_COSTS = {
    1: 20,   # Level 1 -> 2: 20 coins
    2: 50,   # Level 2 -> 3: 50 coins
    3: 100,  # Level 3 -> 4: 100 coins
    4: 999   # Level 4 is max
}

# Difficulty Settings
DIFFICULTY_MODIFIERS = {
    'EASY': {
        'lives': 5,
        'enemy_count_multiplier': 0.7,  # 70% of normal enemy count
        'enemy_damage_multiplier': 0.7,
        'coin_multiplier': 1.5,
        'powerup_multiplier': 1.5,
        'weapon_upgrade_cost_multiplier': 0.7,
        'time_limit_multiplier': 2.0,  # 2x more time
        'score_multiplier': 1.0
    },
    'NORMAL': {
        'lives': 3,
        'enemy_count_multiplier': 1.0,
        'enemy_damage_multiplier': 1.0,
        'coin_multiplier': 1.0,
        'powerup_multiplier': 1.0,
        'weapon_upgrade_cost_multiplier': 1.0,
        'time_limit_multiplier': 1.0,
        'score_multiplier': 1.5
    },
    'HARD': {
        'lives': 1,
        'enemy_count_multiplier': 1.5,  # 50% more enemies
        'enemy_damage_multiplier': 1.5,
        'coin_multiplier': 0.7,
        'powerup_multiplier': 0.6,
        'weapon_upgrade_cost_multiplier': 1.5,
        'time_limit_multiplier': 0.5,  # Half the time
        'score_multiplier': 2.0
    }
}

# Progressive difficulty scaling
# As player progresses through levels, difficulty increases
# Last level of EASY = First level of NORMAL difficulty
# Last level of NORMAL = First level of HARD difficulty
PROGRESSIVE_DIFFICULTY_ENABLED = True
PROGRESSIVE_DIFFICULTY_CURVE = 0.5  # How much harder each level gets (0-1)

# Colors - Retro Palette
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 150, 255)
YELLOW = (255, 255, 0)
PURPLE = (200, 0, 255)
CYAN = (0, 255, 255)
ORANGE = (255, 150, 0)
DARK_BLUE = (0, 50, 100)
DARK_GREEN = (0, 100, 50)
GRAY = (100, 100, 100)

# Theme Background Colors
THEME_BACKGROUNDS = {
    'SCIFI': (20, 20, 40),
    'NATURE': (40, 60, 40),
    'SPACE': (10, 10, 20),
    'UNDERGROUND': (30, 20, 15),
    'UNDERWATER': (15, 30, 50)
}

# Theme Tile Colors
THEME_TILE_COLORS = {
    'SCIFI': (100, 100, 150),
    'NATURE': (100, 150, 100),
    'SPACE': (50, 50, 80),
    'UNDERGROUND': (120, 80, 60),
    'UNDERWATER': (50, 100, 150)
}

# Character Colors
CHARACTER_COLORS = [BLUE, GREEN, PURPLE, ORANGE]

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