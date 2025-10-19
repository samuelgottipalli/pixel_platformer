"""
Level loader - loads levels from JSON files or creates default levels
"""
import json
import os
from config.settings import LEVELS_DIR, TILE_SIZE

class LevelLoader:
    """Loads and manages level data"""
    
    @staticmethod
    def load_from_file(filename):
        """
        Load level from JSON file
        Args:
            filename: JSON file path
        Returns:
            Level data dictionary
        """
        try:
            filepath = os.path.join(LEVELS_DIR, filename)
            with open(filepath, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading level {filename}: {e}")
            return None
            
    @staticmethod
    def save_to_file(level_data, filename):
        """
        Save level to JSON file
        Args:
            level_data: Level data dictionary
            filename: Output JSON file path
        """
        try:
            os.makedirs(LEVELS_DIR, exist_ok=True)
            filepath = os.path.join(LEVELS_DIR, filename)
            with open(filepath, 'w') as f:
                json.dump(level_data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving level {filename}: {e}")
            return False
            
    @staticmethod
    def create_default_levels():
        """
        Create default level set
        Returns:
            List of level data dictionaries
        """
        levels = []
        
        # Level 1: Tutorial/Easy Sci-Fi Level
        level1 = {
            'width': 3200,
            'height': 720,
            'theme': 'SCIFI',
            'spawn_x': 100,
            'spawn_y': 500,
            'tiles': [
                # Ground
                *[{'x': i * TILE_SIZE, 'y': 640, 'solid': True} for i in range(100)],
                # Platforms
                *[{'x': 400 + i * TILE_SIZE, 'y': 500, 'solid': True} for i in range(5)],
                *[{'x': 700 + i * TILE_SIZE, 'y': 400, 'solid': True} for i in range(4)],
                *[{'x': 1000 + i * TILE_SIZE, 'y': 300, 'solid': True} for i in range(6)],
                # Walls
                *[{'x': 1500, 'y': 640 - i * TILE_SIZE, 'solid': True} for i in range(8)],
            ],
            'enemies': [
                {'x': 600, 'y': 450, 'type': 'ground', 'patrol': 150},
                {'x': 1200, 'y': 250, 'type': 'ground', 'patrol': 100},
                {'x': 800, 'y': 300, 'type': 'flying', 'patrol': 200},
            ],
            'hazards': [
                {'x': 900, 'y': 640, 'type': 'spike'},
                {'x': 1100, 'y': 200, 'type': 'falling_block'},
                {'x': 1600, 'y': 400, 'type': 'moving_platform', 'width': 96},
            ],
            'coins': [
                *[{'x': 400 + i * 50, 'y': 450, 'value': 1} for i in range(10)],
                {'x': 1000, 'y': 250, 'value': 5},
            ],
            'powerups': [
                {'x': 750, 'y': 350, 'type': 'health'},
            ],
            'keys': [],
            'portals': [
                {'x': 2900, 'y': 550, 'dest': 1}
            ]
        }
        
        # Level 2: Nature Theme with more challenges
        level2 = {
            'width': 4000,
            'height': 720,
            'theme': 'NATURE',
            'spawn_x': 100,
            'spawn_y': 500,
            'tiles': [
                *[{'x': i * TILE_SIZE, 'y': 640, 'solid': True} for i in range(125)],
                *[{'x': 300 + i * TILE_SIZE, 'y': 520, 'solid': True} for i in range(8)],
                *[{'x': 800 + i * TILE_SIZE, 'y': 420, 'solid': True} for i in range(6)],
                *[{'x': 1300 + i * TILE_SIZE, 'y': 320, 'solid': True} for i in range(5)],
                *[{'x': 1800, 'y': 640 - i * TILE_SIZE, 'solid': True} for i in range(10)],
                *[{'x': 2000 + i * TILE_SIZE, 'y': 450, 'solid': True} for i in range(10)],
            ],
            'enemies': [
                {'x': 500, 'y': 470, 'type': 'ground', 'patrol': 200},
                {'x': 900, 'y': 370, 'type': 'ground', 'patrol': 150},
                {'x': 1100, 'y': 250, 'type': 'flying', 'patrol': 250},
                {'x': 1500, 'y': 270, 'type': 'ground', 'patrol': 100},
                {'x': 2200, 'y': 400, 'type': 'flying', 'patrol': 300},
            ],
            'hazards': [
                {'x': 700, 'y': 640, 'type': 'spike'},
                {'x': 732, 'y': 640, 'type': 'spike'},
                {'x': 1200, 'y': 220, 'type': 'falling_block'},
                {'x': 1700, 'y': 350, 'type': 'moving_platform', 'width': 96},
                {'x': 2500, 'y': 500, 'type': 'moving_platform', 'width': 128},
            ],
            'coins': [
                *[{'x': 300 + i * 60, 'y': 470, 'value': 1} for i in range(12)],
                *[{'x': 1300 + i * 60, 'y': 270, 'value': 1} for i in range(8)],
                {'x': 1100, 'y': 200, 'value': 10},
            ],
            'powerups': [
                {'x': 850, 'y': 370, 'type': 'speed'},
                {'x': 2100, 'y': 400, 'type': 'invincible'},
            ],
            'keys': [
                {'x': 3500, 'y': 590, 'color': [255, 0, 0]}
            ],
            'portals': [
                {'x': 3700, 'y': 550, 'dest': 2}
            ]
        }
        
        # Level 3: Space Theme - Sublevel example
        level3 = {
            'width': 3500,
            'height': 720,
            'theme': 'SPACE',
            'spawn_x': 100,
            'spawn_y': 500,
            'tiles': [
                *[{'x': i * TILE_SIZE, 'y': 640, 'solid': True} for i in range(110)],
                *[{'x': 400 + i * 64, 'y': 500 - i * 40, 'solid': True} for i in range(10)],
                *[{'x': 1500 + i * TILE_SIZE, 'y': 350, 'solid': True} for i in range(8)],
                *[{'x': 2200 + i * TILE_SIZE, 'y': 450, 'solid': True} for i in range(12)],
            ],
            'enemies': [
                {'x': 700, 'y': 300, 'type': 'flying', 'patrol': 300},
                {'x': 1000, 'y': 200, 'type': 'flying', 'patrol': 250},
                {'x': 1600, 'y': 300, 'type': 'turret'},
                {'x': 2000, 'y': 300, 'type': 'turret'},
                {'x': 2500, 'y': 400, 'type': 'ground', 'patrol': 200},
            ],
            'hazards': [
                *[{'x': 1100 + i * 64, 'y': 640, 'type': 'spike'} for i in range(5)],
                {'x': 1800, 'y': 250, 'type': 'falling_block'},
                {'x': 2100, 'y': 550, 'type': 'moving_platform', 'width': 96},
            ],
            'coins': [
                *[{'x': 500 + i * 80, 'y': 400 - i * 40, 'value': 2} for i in range(10)],
                {'x': 1600, 'y': 300, 'value': 15},
            ],
            'powerups': [
                {'x': 900, 'y': 150, 'type': 'double_jump'},
                {'x': 2300, 'y': 400, 'type': 'health'},
            ],
            'keys': [],
            'portals': [
                {'x': 3200, 'y': 550, 'dest': 0}  # Back to level 1 for demo
            ]
        }
        
        levels.extend([level1, level2, level3])
        return levels