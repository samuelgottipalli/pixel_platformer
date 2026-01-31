"""
Achievement System - Sprint 3
Tracks player achievements with rewards
Persistent storage and unlock notifications
"""

import json
import os
from datetime import datetime


class Achievement:
    """Individual achievement definition"""
    
    def __init__(self, achievement_id, name, description, category, 
                 goal, reward_type=None, reward_value=None, hidden=False):
        """
        Initialize achievement
        Args:
            achievement_id: Unique identifier
            name: Display name
            description: Description text
            category: Category (collection, combat, speed, difficulty, exploration)
            goal: Target value to unlock
            reward_type: Type of reward (life, weapon, score, unlock)
            reward_value: Value of reward
            hidden: Whether achievement is hidden until unlocked
        """
        self.id = achievement_id
        self.name = name
        self.description = description
        self.category = category
        self.goal = goal
        self.reward_type = reward_type
        self.reward_value = reward_value
        self.hidden = hidden
        
        # Progress tracking
        self.unlocked = False
        self.progress = 0
        self.unlock_date = None
    
    def update_progress(self, value):
        """Update progress toward achievement"""
        if self.unlocked:
            return False
        
        self.progress = min(value, self.goal)
        
        if self.progress >= self.goal:
            self.unlock()
            return True
        
        return False
    
    def unlock(self):
        """Unlock the achievement"""
        if not self.unlocked:
            self.unlocked = True
            self.progress = self.goal
            self.unlock_date = datetime.now().isoformat()
            return True
        return False
    
    def get_progress_percent(self):
        """Get progress as percentage"""
        if self.goal == 0:
            return 100 if self.unlocked else 0
        return min(100, int((self.progress / self.goal) * 100))
    
    def to_dict(self):
        """Convert to dictionary for saving"""
        return {
            'id': self.id,
            'unlocked': self.unlocked,
            'progress': self.progress,
            'unlock_date': self.unlock_date
        }
    
    def from_dict(self, data):
        """Load from dictionary"""
        self.unlocked = data.get('unlocked', False)
        self.progress = data.get('progress', 0)
        self.unlock_date = data.get('unlock_date', None)


class AchievementManager:
    """Manages all achievements and tracking"""
    
    def __init__(self, profile_name):
        """Initialize achievement manager for a profile"""
        self.profile_name = profile_name
        self.achievements = {}
        
        # Define all achievements
        self._define_achievements()
        
        # Load progress
        self._load_achievements()
        
        # Recently unlocked (for notifications)
        self.recent_unlocks = []
    
    def _define_achievements(self):
        """Define all game achievements"""
        
        # ====================================================================
        # COLLECTION ACHIEVEMENTS
        # ====================================================================
        
        self.achievements['coin_collector_1'] = Achievement(
            'coin_collector_1',
            'Coin Collector I',
            'Collect 60% of coins in Act 1',
            'collection',
            goal=60,  # Percentage
            reward_type='score',
            reward_value=1000
        )
        
        self.achievements['coin_collector_2'] = Achievement(
            'coin_collector_2',
            'Coin Collector II',
            'Collect 80% of coins in Act 1',
            'collection',
            goal=80,
            reward_type='score',
            reward_value=2500
        )
        
        self.achievements['coin_hoarder'] = Achievement(
            'coin_hoarder',
            'Coin Hoarder',
            'Collect 100% of coins in Act 1',
            'collection',
            goal=100,
            reward_type='life',
            reward_value=1
        )
        
        self.achievements['powerup_collector'] = Achievement(
            'powerup_collector',
            'Power Hungry',
            'Collect 20 power-ups',
            'collection',
            goal=20,
            reward_type='score',
            reward_value=500
        )
        
        # ====================================================================
        # COMBAT ACHIEVEMENTS
        # ====================================================================
        
        self.achievements['exterminator'] = Achievement(
            'exterminator',
            'Exterminator',
            'Defeat 100 enemies',
            'combat',
            goal=100,
            reward_type='score',
            reward_value=1500
        )
        
        self.achievements['stomp_master'] = Achievement(
            'stomp_master',
            'Stomp Master',
            'Defeat 50 enemies by stomping',
            'combat',
            goal=50,
            reward_type='weapon',
            reward_value=1  # Start with level 2 weapon
        )
        
        self.achievements['sharpshooter'] = Achievement(
            'sharpshooter',
            'Sharpshooter',
            'Defeat 50 enemies with projectiles',
            'combat',
            goal=50,
            reward_type='score',
            reward_value=1000
        )
        
        self.achievements['melee_master'] = Achievement(
            'melee_master',
            'Melee Master',
            'Defeat 25 enemies with melee attacks',
            'combat',
            goal=25,
            reward_type='weapon',
            reward_value=1
        )
        
        # ====================================================================
        # DIFFICULTY ACHIEVEMENTS
        # ====================================================================
        
        self.achievements['easy_complete'] = Achievement(
            'easy_complete',
            'Training Complete',
            'Complete Act 1 on Easy difficulty',
            'difficulty',
            goal=1,
            reward_type='unlock',
            reward_value='easy_skin'
        )
        
        self.achievements['normal_complete'] = Achievement(
            'normal_complete',
            'Hero',
            'Complete Act 1 on Normal difficulty',
            'difficulty',
            goal=1,
            reward_type='unlock',
            reward_value='normal_skin'
        )
        
        self.achievements['hard_complete'] = Achievement(
            'hard_complete',
            'Legend',
            'Complete Act 1 on Hard difficulty',
            'difficulty',
            goal=1,
            reward_type='life',
            reward_value=2
        )
        
        # ====================================================================
        # SPEED ACHIEVEMENTS
        # ====================================================================
        
        self.achievements['speedrunner_1'] = Achievement(
            'speedrunner_1',
            'Speedrunner I',
            'Complete Act 1 in under 90 minutes',
            'speed',
            goal=90 * 60,  # 90 minutes in seconds
            reward_type='unlock',
            reward_value='timer_display'
        )
        
        self.achievements['speedrunner_2'] = Achievement(
            'speedrunner_2',
            'Speedrunner II',
            'Complete Act 1 in under 60 minutes',
            'speed',
            goal=60 * 60,  # 60 minutes in seconds
            reward_type='score',
            reward_value=5000
        )
        
        # ====================================================================
        # BOSS ACHIEVEMENTS
        # ====================================================================
        
        self.achievements['guardian_slayer'] = Achievement(
            'guardian_slayer',
            'Guardian Slayer',
            'Defeat the Guardian without taking damage',
            'boss',
            goal=1,
            reward_type='score',
            reward_value=3000,
            hidden=True
        )
        
        self.achievements['boss_master'] = Achievement(
            'boss_master',
            'Boss Master',
            'Defeat the Guardian in under 3 minutes',
            'boss',
            goal=180,  # 3 minutes in seconds
            reward_type='unlock',
            reward_value='boss_rush_mode',
            hidden=True
        )
        
        # ====================================================================
        # EXPLORATION ACHIEVEMENTS
        # ====================================================================
        
        self.achievements['explorer'] = Achievement(
            'explorer',
            'Explorer',
            'Find all 5 secret areas in Act 1',
            'exploration',
            goal=5,
            reward_type='unlock',
            reward_value='secret_level'
        )
        
        self.achievements['no_death'] = Achievement(
            'no_death',
            'Untouchable',
            'Complete Act 1 without dying',
            'challenge',
            goal=1,
            reward_type='life',
            reward_value=3,
            hidden=True
        )
    
    def _load_achievements(self):
        """Load achievement progress from file"""
        filepath = f'data/achievements_{self.profile_name}.json'
        
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                
                for achievement_id, achievement_data in data.items():
                    if achievement_id in self.achievements:
                        self.achievements[achievement_id].from_dict(achievement_data)
            except Exception as e:
                print(f"Error loading achievements: {e}")
    
    def save_achievements(self):
        """Save achievement progress to file"""
        os.makedirs('data', exist_ok=True)
        filepath = f'data/achievements_{self.profile_name}.json'
        
        try:
            data = {}
            for achievement_id, achievement in self.achievements.items():
                data[achievement_id] = achievement.to_dict()
            
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error saving achievements: {e}")
            return False
    
    # ========================================================================
    # PROGRESS TRACKING
    # ========================================================================
    
    def update_progress(self, achievement_id, value):
        """Update progress for an achievement"""
        if achievement_id not in self.achievements:
            return False
        
        achievement = self.achievements[achievement_id]
        unlocked = achievement.update_progress(value)
        
        if unlocked:
            self.recent_unlocks.append(achievement)
            self.save_achievements()
        
        return unlocked
    
    def unlock_achievement(self, achievement_id):
        """Directly unlock an achievement"""
        if achievement_id not in self.achievements:
            return False
        
        achievement = self.achievements[achievement_id]
        if achievement.unlock():
            self.recent_unlocks.append(achievement)
            self.save_achievements()
            return True
        
        return False
    
    def check_coin_percentage(self, collected, total):
        """Check coin collection achievements"""
        if total == 0:
            return
        
        percentage = int((collected / total) * 100)
        
        self.update_progress('coin_collector_1', percentage)
        self.update_progress('coin_collector_2', percentage)
        self.update_progress('coin_hoarder', percentage)
    
    def add_enemy_kill(self, kill_type='any'):
        """Track enemy kills"""
        # Total kills
        current = self.achievements['exterminator'].progress
        self.update_progress('exterminator', current + 1)
        
        # Kill type specific
        if kill_type == 'stomp':
            current = self.achievements['stomp_master'].progress
            self.update_progress('stomp_master', current + 1)
        elif kill_type == 'projectile':
            current = self.achievements['sharpshooter'].progress
            self.update_progress('sharpshooter', current + 1)
        elif kill_type == 'melee':
            current = self.achievements['melee_master'].progress
            self.update_progress('melee_master', current + 1)
    
    def add_powerup_collected(self):
        """Track powerup collection"""
        current = self.achievements['powerup_collector'].progress
        self.update_progress('powerup_collector', current + 1)
    
    def check_difficulty_complete(self, difficulty):
        """Check difficulty completion achievements"""
        if difficulty == "EASY":
            self.unlock_achievement('easy_complete')
        elif difficulty == "NORMAL":
            self.unlock_achievement('normal_complete')
        elif difficulty == "HARD":
            self.unlock_achievement('hard_complete')
    
    def check_speedrun_time(self, time_seconds):
        """Check speedrun achievements"""
        # Note: These check if time is UNDER the goal
        if time_seconds <= 90 * 60:  # 90 minutes
            self.unlock_achievement('speedrunner_1')
        
        if time_seconds <= 60 * 60:  # 60 minutes
            self.unlock_achievement('speedrunner_2')
    
    def add_secret_found(self):
        """Track secret areas found"""
        current = self.achievements['explorer'].progress
        self.update_progress('explorer', current + 1)
    
    def check_boss_no_damage(self):
        """Check if boss defeated without damage"""
        self.unlock_achievement('guardian_slayer')
    
    def check_boss_speed(self, time_seconds):
        """Check boss speed achievement"""
        if time_seconds <= 180:  # 3 minutes
            self.unlock_achievement('boss_master')
    
    def check_no_death_run(self):
        """Check no death achievement"""
        self.unlock_achievement('no_death')
    
    # ========================================================================
    # REWARDS
    # ========================================================================
    
    def get_pending_rewards(self):
        """Get rewards from recently unlocked achievements"""
        rewards = []
        
        for achievement in self.recent_unlocks:
            if achievement.reward_type:
                rewards.append({
                    'type': achievement.reward_type,
                    'value': achievement.reward_value,
                    'achievement': achievement.name
                })
        
        return rewards
    
    def clear_recent_unlocks(self):
        """Clear recent unlock notifications"""
        self.recent_unlocks = []
    
    def apply_rewards_to_player(self, player):
        """Apply achievement rewards to player"""
        rewards = self.get_pending_rewards()
        
        for reward in rewards:
            if reward['type'] == 'life':
                player.lives += reward['value']
            elif reward['type'] == 'weapon':
                player.weapon_level = min(3, player.weapon_level + reward['value'])
            elif reward['type'] == 'score':
                player.score += reward['value']
        
        return rewards
    
    # ========================================================================
    # QUERIES
    # ========================================================================
    
    def get_achievement(self, achievement_id):
        """Get specific achievement"""
        return self.achievements.get(achievement_id)
    
    def get_all_achievements(self):
        """Get all achievements"""
        return list(self.achievements.values())
    
    def get_unlocked_achievements(self):
        """Get only unlocked achievements"""
        return [a for a in self.achievements.values() if a.unlocked]
    
    def get_achievements_by_category(self, category):
        """Get achievements in a category"""
        return [a for a in self.achievements.values() if a.category == category]
    
    def get_completion_percentage(self):
        """Get overall achievement completion percentage"""
        total = len(self.achievements)
        unlocked = len(self.get_unlocked_achievements())
        
        if total == 0:
            return 0
        
        return int((unlocked / total) * 100)
    
    def get_stats(self):
        """Get achievement statistics"""
        total = len(self.achievements)
        unlocked = len(self.get_unlocked_achievements())
        
        categories = {}
        for achievement in self.achievements.values():
            if achievement.category not in categories:
                categories[achievement.category] = {'total': 0, 'unlocked': 0}
            
            categories[achievement.category]['total'] += 1
            if achievement.unlocked:
                categories[achievement.category]['unlocked'] += 1
        
        return {
            'total': total,
            'unlocked': unlocked,
            'completion': self.get_completion_percentage(),
            'categories': categories
        }
