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
        """Create Act 1 levels (Free version)"""
        from levels.act1_levels_design import get_act1_levels
        
        levels = []
        
        # Get Level 0 (Tutorial) and Level 1
        act1_base = get_act1_levels()
        levels.extend(act1_base)  # Levels 0-1
        # Add levels 2-6 from act1_levels_complete
        try:
            from levels.act1_levels_complete import get_act1_levels_2_to_6
            act1_expanded = get_act1_levels_2_to_6()
            levels.extend(act1_expanded)
        except ImportError:
            print("⚠️  act1_levels_complete not found, using demo levels")
        
        levels = [LevelLoader.fix_spike_positions(level) for level in levels]
        
        print(f"✓ Loaded {len(levels)} levels")
        return levels
    
    @staticmethod
    def create_spike(x, ground_y=640):
        """Create spike on top of ground"""
        return {'x': x, 'y': ground_y - 32, 'type': 'spike', 'height': 32, 'width': 32}

    @staticmethod
    def fix_spike_positions(level_data):
        """Fix spike positions to be on top of ground"""
        for hazard in level_data.get('hazards', []):
            if hazard['type'] == 'spike' and hazard.get('y', 0) >= 640:
                hazard['y'] = 608  # Place on top of ground
        return level_data