"""
Difficulty Completion Tracker
Tracks which difficulties have been completed and enables level selection
"""
import json
import os
from config.settings import SAVE_DIR

class DifficultyCompletionTracker:
    """Tracks completion of difficulties to unlock level selection"""
    
    @staticmethod
    def get_completion_file():
        """Get completion tracking file path"""
        return os.path.join(SAVE_DIR, 'difficulty_completions.json')
    
    @staticmethod
    def load_completions():
        """
        Load difficulty completion data
        Returns:
            Dictionary with difficulty completions:
            {
                'profile_name': {
                    'EASY': True/False,
                    'NORMAL': True/False,
                    'HARD': True/False
                }
            }
        """
        try:
            filepath = DifficultyCompletionTracker.get_completion_file()
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            print(f"Error loading difficulty completions: {e}")
            return {}
    
    @staticmethod
    def save_completions(completions):
        """
        Save difficulty completion data
        Args:
            completions: Dictionary of completions
        """
        try:
            os.makedirs(SAVE_DIR, exist_ok=True)
            filepath = DifficultyCompletionTracker.get_completion_file()
            with open(filepath, 'w') as f:
                json.dump(completions, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving difficulty completions: {e}")
            return False
    
    @staticmethod
    def mark_difficulty_complete(profile_name, difficulty):
        """
        Mark a difficulty as completed for a profile
        Args:
            profile_name: Player profile name
            difficulty: 'EASY', 'NORMAL', or 'HARD'
        """
        completions = DifficultyCompletionTracker.load_completions()
        
        if profile_name not in completions:
            completions[profile_name] = {
                'EASY': False,
                'NORMAL': False,
                'HARD': False
            }
        
        completions[profile_name][difficulty] = True
        DifficultyCompletionTracker.save_completions(completions)
        print(f"✓ {profile_name} completed {difficulty} difficulty!")
    
    @staticmethod
    def has_completed_difficulty(profile_name, difficulty):
        """
        Check if profile has completed a difficulty
        Args:
            profile_name: Player profile name
            difficulty: 'EASY', 'NORMAL', or 'HARD'
        Returns:
            True if completed, False otherwise
        """
        completions = DifficultyCompletionTracker.load_completions()
        
        if profile_name in completions:
            return completions[profile_name].get(difficulty, False)
        
        return False
    
    @staticmethod
    def get_completed_difficulties(profile_name):
        """
        Get list of completed difficulties for a profile
        Args:
            profile_name: Player profile name
        Returns:
            List of completed difficulties ['EASY', 'NORMAL', 'HARD']
        """
        completions = DifficultyCompletionTracker.load_completions()
        
        if profile_name not in completions:
            return []
        
        completed = []
        for diff in ['EASY', 'NORMAL', 'HARD']:
            if completions[profile_name].get(diff, False):
                completed.append(diff)
        
        return completed
