"""
Level loader - loads levels from JSON files or creates default levels
UPDATED: Now loads complete Act 1 (Levels 0-6)
"""

import json
import os

from config.settings import LEVELS_DIR, TILE_SIZE


class LevelLoader:
    """Loads and manages level data"""

    @staticmethod
    def fix_spike_positions(level_data):
        """Fix spike positions to be on top of ground"""
        for hazard in level_data.get("hazards", []):
            if hazard["type"] == "spike" and hazard.get("y", 0) >= 640:
                hazard["y"] = 608  # 640 - 32 = 608 (on top of ground)
        return level_data

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
            with open(filepath, "r") as f:
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
            with open(filepath, "w") as f:
                json.dump(level_data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving level {filename}: {e}")
            return False

    @staticmethod
    def create_default_levels():
        """
        Create complete Act 1 level set
        Returns:
            List of 7 level data dictionaries (Levels 0-6)
        """
        try:
            # Try importing from act1_levels_design for tutorial and level 1
            # Try importing complete levels 2-6
            from levels.act1_complete_levels import get_complete_act1_levels
            from levels.act1_levels_design import get_act1_levels

            levels = []

            # Get Level 0 (Tutorial) and Level 1 from act1_levels_design
            act1_base = get_act1_levels()
            if len(act1_base) >= 2:
                levels.extend(act1_base[:2])  # Add Level 0 and 1

            # Get Levels 2-6 from act1_complete_levels
            act1_complete = get_complete_act1_levels()
            levels.extend(act1_complete)  # Add Levels 2-6

            # FIX SPIKE POSITIONS
            levels = [LevelLoader.fix_spike_positions(level) for level in levels]

            print(f"✓ Loaded {len(levels)} Act 1 levels")
            return levels

        except ImportError as e:
            print(f"⚠️  Could not import Act 1 levels: {e}")
            print("⚠️  Falling back to demo levels")
            