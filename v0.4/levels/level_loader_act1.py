"""
Level loader - loads Act 1 levels
"""
import json
import os
from config.settings import LEVELS_DIR, TILE_SIZE

class LevelLoader:
    """Loads and manages level data"""
    
    @staticmethod
    def load_from_file(filename):
        """Load level from JSON file"""
        try:
            filepath = os.path.join(LEVELS_DIR, filename)
            with open(filepath, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading level {filename}: {e}")
            return None
            
    @staticmethod
    def save_to_file(level_data, filename):
        """Save level to JSON file"""
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
        """Create Act 1 levels (Free version)"""
        from levels.act1_levels_complete import get_act1_levels_2_to_6
        from levels.act1_levels_design import get_act1_levels
        
        levels = []
        
        # Get Level 0 (Tutorial) and Level 1 from act1_levels_design
        act1_base = get_act1_levels()
        levels.extend(act1_base)  # Levels 0-1
        
        # Get Levels 2-6 from act1_levels_complete
        act1_expanded = get_act1_levels_2_to_6()
        levels.extend(act1_expanded)  # Levels 2-6 (includes boss)
        
        print(f"✓ Loaded {len(levels)} levels for Act 1")
        for i, level in enumerate(levels):
            width = level['width']
            theme = level.get('theme', 'UNKNOWN')
            print(f"  Level {i}: {width}px, {theme}")
        
        return levels
