"""
Difficulty management system
"""
import math
from config.settings import (
    DIFFICULTY_MODIFIERS, WEAPON_UPGRADE_COSTS, 
    PROGRESSIVE_DIFFICULTY_ENABLED, PROGRESSIVE_DIFFICULTY_CURVE
)

class DifficultyManager:
    """Manages difficulty scaling and modifiers"""
    
    def __init__(self, difficulty='NORMAL', total_levels=20):
        """
        Args:
            difficulty: 'EASY', 'NORMAL', or 'HARD'
            total_levels: Total number of levels in the game
        """
        self.difficulty = difficulty
        self.total_levels = total_levels
        self.modifiers = DIFFICULTY_MODIFIERS[difficulty]
        
    def get_progressive_multiplier(self, current_level):
        """
        Calculate progressive difficulty multiplier for current level
        Args:
            current_level: Current level index (0-based)
        Returns:
            Multiplier value (0.0 to 1.0)
        """
        if not PROGRESSIVE_DIFFICULTY_ENABLED:
            return 0.0
            
        # Linear progression from 0 to 1 across all levels
        progress = current_level / max(self.total_levels - 1, 1)
        return progress * PROGRESSIVE_DIFFICULTY_CURVE
        
    def get_lives(self, current_level=0):
        """Get starting lives for current difficulty and level"""
        base_lives = self.modifiers['lives']
        
        # Progressive: Easy starts at 5, ends at 3 (Normal start)
        # Normal starts at 3, ends at 1 (Hard start)
        if PROGRESSIVE_DIFFICULTY_ENABLED:
            progress = self.get_progressive_multiplier(current_level)
            
            if self.difficulty == 'EASY':
                # 5 -> 3 over course of game
                return max(3, int(base_lives - (2 * progress)))
            elif self.difficulty == 'NORMAL':
                # 3 -> 1 over course of game
                return max(1, int(base_lives - (2 * progress)))
            # HARD stays at 1
            
        return base_lives
        
    def apply_enemy_scaling(self, enemies, current_level):
        """
        Apply difficulty scaling to enemy list
        Args:
            enemies: List of enemy dictionaries
            current_level: Current level index
        Returns:
            Modified enemy list
        """
        progress = self.get_progressive_multiplier(current_level)
        
        # Enemy count multiplier
        count_mult = self.modifiers['enemy_count_multiplier']
        # Progressive scaling: increases as player progresses
        count_mult += progress * 0.3
        
        # Determine how many enemies to keep/add
        target_count = int(len(enemies) * count_mult)
        
        if target_count < len(enemies):
            # Remove random enemies for easier difficulty
            import random
            enemies = random.sample(enemies, target_count)
        elif target_count > len(enemies):
            # Duplicate some enemies for harder difficulty
            import random
            to_add = target_count - len(enemies)
            for _ in range(to_add):
                enemies.append(random.choice(enemies).copy())
                
        return enemies
        
    def get_enemy_damage_multiplier(self, current_level):
        """Get enemy damage multiplier with progressive scaling"""
        progress = self.get_progressive_multiplier(current_level)
        base_mult = self.modifiers['enemy_damage_multiplier']
        
        # Increase damage as player progresses
        return base_mult + (progress * 0.5)
        
    def apply_collectible_scaling(self, collectibles, current_level, collectible_type='coin'):
        """
        Apply difficulty scaling to collectibles (coins/powerups)
        Args:
            collectibles: List of collectible dictionaries
            current_level: Current level index
            collectible_type: 'coin' or 'powerup'
        Returns:
            Modified collectible list
        """
        progress = self.get_progressive_multiplier(current_level)
        
        # Get appropriate multiplier
        if collectible_type == 'coin':
            mult = self.modifiers['coin_multiplier']
        else:
            mult = self.modifiers['powerup_multiplier']
            
        # Progressive: fewer collectibles as you progress
        mult -= progress * 0.3
        mult = max(0.3, mult)  # Always have some collectibles
        
        target_count = int(len(collectibles) * mult)
        
        if target_count < len(collectibles):
            import random
            collectibles = random.sample(collectibles, target_count)
            
        return collectibles
        
    def get_weapon_upgrade_cost(self, weapon_level, current_level):
        """
        Get weapon upgrade cost with difficulty scaling
        Args:
            weapon_level: Current weapon level
            current_level: Current game level
        Returns:
            Cost in coins
        """
        base_cost = WEAPON_UPGRADE_COSTS.get(weapon_level, 100)
        mult = self.modifiers['weapon_upgrade_cost_multiplier']
        
        # Progressive: costs increase as you progress
        progress = self.get_progressive_multiplier(current_level)
        mult += progress * 0.3
        
        return int(base_cost * mult)
        
    def get_time_limit(self, base_time, current_level):
        """
        Get time limit with difficulty scaling
        Args:
            base_time: Base time limit in seconds (or None)
            current_level: Current level index
        Returns:
            Time limit in seconds (or None if no limit)
        """
        if base_time is None:
            return None
            
        mult = self.modifiers['time_limit_multiplier']
        
        # Progressive: less time as you progress
        progress = self.get_progressive_multiplier(current_level)
        mult -= progress * 0.3
        mult = max(0.3, mult)  # Always have some time
        
        return int(base_time * mult)
        
    def get_score_multiplier(self):
        """Get score multiplier for current difficulty"""
        return self.modifiers['score_multiplier']
        
    def get_difficulty_info(self, current_level):
        """
        Get all difficulty info for display/debugging
        Args:
            current_level: Current level index
        Returns:
            Dictionary of difficulty values
        """
        return {
            'difficulty': self.difficulty,
            'level': current_level,
            'lives': self.get_lives(current_level),
            'enemy_damage_mult': self.get_enemy_damage_multiplier(current_level),
            'score_mult': self.get_score_multiplier(),
            'progressive_mult': self.get_progressive_multiplier(current_level)
        }