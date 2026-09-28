"""
Player profile management
"""

import json
import os
import shutil
from dataclasses import asdict, dataclass, field, fields

from config.settings import PROFILES_FILE


@dataclass
class PlayerProfile:
    """Player profile data"""

    name: str
    character: int = 0
    total_score: int = 0
    levels_completed: int = 0
    total_coins_collected: int = 0
    current_coins: int = 0
    max_health: int = 100
    current_health: int = 100
    max_lives: int = 0
    current_lives: int = 0
    keys_collected: int = 0
    current_weapon: str = "standard"
    enemies_defeated: int = 0
    time_played_seconds: int = 0
    deaths: int = 0
    total_damage_taken: int = 0
    powerups_collected: int = 0
    secrets_found: int = 0
    speedrun_time: float = 0.0
    weapons: dict = field(default_factory=dict)
    upgrades: dict = field(default_factory=dict)


@dataclass
class CompletedGame:
    """Completed game record for leaderboard/stats"""

    name: str
    character: int = 0
    final_score: int = 0
    levels_completed: int = 0
    coins_collected: int = 0
    coins_used: int = 0
    keys_collected: int = 0
    enemies_defeated: int = 0
    time_played_seconds: int = 0
    deaths: int = 0
    total_damage_taken: int = 0
    powerups_collected: int = 0
    secrets_found: int = 0
    speedrun_time: float = 0.0
    completion_date: str = ""


# Field renames between save-format versions: old name -> new name
_PROFILE_RENAMES = {"coins_collected": "total_coins_collected"}
_COMPLETED_RENAMES = {"player_name": "name"}


def _from_dict(cls, data, renames):
    """Build a dataclass from saved data, migrating old field names and
    ignoring unknown keys so older/newer files still load"""
    data = {renames.get(k, k): v for k, v in data.items()}
    known = {f.name for f in fields(cls)}
    return cls(**{k: v for k, v in data.items() if k in known})


class ProfileManager:
    """Manages player profiles"""

    @staticmethod
    def load_profiles():
        """
        Load all player profiles from file
        Returns:
            List of PlayerProfile objects
        """
        try:
            # Create data directory if it doesn't exist
            os.makedirs(os.path.dirname(PROFILES_FILE), exist_ok=True)

            with open(PROFILES_FILE, "r") as f:
                data = json.load(f)
                return [_from_dict(PlayerProfile, p, _PROFILE_RENAMES) for p in data]
        except FileNotFoundError:
            return []
        except Exception as e:
            # Keep a copy so the next save can't silently wipe unreadable profiles
            backup = PROFILES_FILE + ".bak"
            shutil.copyfile(PROFILES_FILE, backup)
            print(f"Error loading profiles: {e} (backed up to {backup})")
            return []

    @staticmethod
    def save_profiles(profiles):
        """
        Save all player profiles to file
        Args:
            profiles: List of PlayerProfile objects
        Returns:
            True if successful
        """
        try:
            os.makedirs(os.path.dirname(PROFILES_FILE), exist_ok=True)

            with open(PROFILES_FILE, "w") as f:
                data = [asdict(p) for p in profiles]
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving profiles: {e}")
            return False

    @staticmethod
    def load_completed_games():
        """
        Load completed game records
        Returns:
            List of CompletedGame objects
        """
        try:
            completed_file = PROFILES_FILE.replace(
                "profiles.json", "completed_games.json"
            )
            with open(completed_file, "r") as f:
                data = json.load(f)
                return [_from_dict(CompletedGame, g, _COMPLETED_RENAMES) for g in data]
        except FileNotFoundError:
            return []
        except Exception as e:
            print(f"Error loading completed games: {e}")
            return []

    @staticmethod
    def save_completed_game(profile, final_score):
        """
        Save a completed game record and delete the active profile
        Args:
            profile: PlayerProfile object
            final_score: Final score achieved
        Returns:
            True if successful
        """
        try:
            from datetime import datetime

            # Load existing completed games
            completed_games = ProfileManager.load_completed_games()

            # Create new completed game record
            new_record = CompletedGame(
                name=profile.name,
                character=profile.character,
                final_score=final_score,
                levels_completed=profile.levels_completed,
                coins_collected=profile.total_coins_collected,
                completion_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            )
            completed_games.append(new_record)

            # Save completed games
            completed_file = PROFILES_FILE.replace(
                "profiles.json", "completed_games.json"
            )
            os.makedirs(os.path.dirname(completed_file), exist_ok=True)
            with open(completed_file, "w") as f:
                data = [asdict(g) for g in completed_games]
                json.dump(data, f, indent=2)

            return True
        except Exception as e:
            print(f"Error saving completed game: {e}")
            return False

    @staticmethod
    def delete_profile(profile_name):
        """
        Delete a profile by name
        Args:
            profile_name: Name of profile to delete
        Returns:
            True if successful
        """
        try:
            profiles = ProfileManager.load_profiles()
            profiles = [p for p in profiles if p.name != profile_name]
            ProfileManager.save_profiles(profiles)
            return True
        except Exception as e:
            print(f"Error deleting profile: {e}")
            return False

    @staticmethod
    def get_profile_by_name(profiles, name):
        """
        Get profile by player name
        Args:
            profiles: List of PlayerProfile objects
            name: Player name to search for
        Returns:
            PlayerProfile or None
        """
        for profile in profiles:
            if profile.name == name:
                return profile
        return None

    @staticmethod
    def update_profile_stats(
        profile, score_gained, coins_gained, level_completed=False
    ):
        """
        Update profile statistics
        Args:
            profile: PlayerProfile object
            score_gained: Score to add
            coins_gained: Coins to add
            level_completed: Whether a level was completed
        """
        profile.total_score += score_gained
        profile.total_coins_collected += coins_gained
        if level_completed:
            profile.levels_completed += 1

    @staticmethod
    def get_top_profiles(profiles, limit=10):
        """
        Get top profiles by score
        Args:
            profiles: List of PlayerProfile objects
            limit: Maximum number to return
        Returns:
            List of top PlayerProfile objects
        """
        return sorted(profiles, key=lambda p: p.total_score, reverse=True)[:limit]
