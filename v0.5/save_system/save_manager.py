"""
Game save/load system
"""

import json
import os

from config.settings import SAVE_DIR


class SaveManager:
    """Manages game save states"""

    @staticmethod
    def save_game(profile_name, player, current_level):
        """
        Save current game state
        Args:
            profile_name: Player profile name
            player: Player object
            current_level: Current level index
        Returns:
            True if successful
        """
        try:
            os.makedirs(SAVE_DIR, exist_ok=True)

            save_data = {
                "profile_name": profile_name,
                "current_level": current_level,
                "player": {
                    "x": player.x,
                    "y": player.y,
                    "health": player.health,
                    "lives": player.lives,
                    "coins": player.coins,
                    "score": player.score,
                    "weapon_level": player.weapon_level,
                    "keys": player.keys,
                    "max_jumps": player.max_jumps,
                },
            }

            filename = f"save_{profile_name}.json"
            filepath = os.path.join(SAVE_DIR, filename)

            with open(filepath, "w") as f:
                json.dump(save_data, f, indent=2)

            print(f"Game saved successfully for {profile_name}")
            return True

        except Exception as e:
            print(f"Error saving game: {e}")
            return False

    @staticmethod
    def load_game(profile_name):
        """
        Load saved game state
        Args:
            profile_name: Player profile name
        Returns:
            Save data dictionary or None if not found
        """
        try:
            filename = f"save_{profile_name}.json"
            filepath = os.path.join(SAVE_DIR, filename)

            with open(filepath, "r") as f:
                save_data = json.load(f)

            print(f"Game loaded successfully for {profile_name}")
            return save_data

        except FileNotFoundError:
            print(f"No save file found for {profile_name}")
            return None
        except Exception as e:
            print(f"Error loading game: {e}")
            return None

    @staticmethod
    def apply_save_to_player(player, save_data):
        """
        Apply saved data to player object
        Args:
            player: Player object to update
            save_data: Save data dictionary
        """
        p = save_data["player"]
        player.x = p["x"]
        player.y = p["y"]
        player.health = p["health"]
        player.lives = p["lives"]
        player.coins = p["coins"]
        player.score = p["score"]
        player.weapon_level = p["weapon_level"]
        player.keys = p["keys"]
        player.max_jumps = p.get("max_jumps", 2)

    @staticmethod
    def delete_save(profile_name):
        """
        Delete save file for profile
        Args:
            profile_name: Player profile name
        Returns:
            True if successful
        """
        try:
            filename = f"save_{profile_name}.json"
            filepath = os.path.join(SAVE_DIR, filename)

            if os.path.exists(filepath):
                os.remove(filepath)
                print(f"Save deleted for {profile_name}")
                return True
            return False

        except Exception as e:
            print(f"Error deleting save: {e}")
            return False

    @staticmethod
    def save_exists(profile_name):
        """
        Check if save file exists for profile
        Args:
            profile_name: Player profile name
        Returns:
            True if save exists
        """
        filename = f"save_{profile_name}.json"
        filepath = os.path.join(SAVE_DIR, filename)
        if os.path.exists(filepath):
            print(f"Profile already exists for {profile_name}")
            return True
        return False

