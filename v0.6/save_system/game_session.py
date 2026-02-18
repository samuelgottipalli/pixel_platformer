"""
Game Session Tracking System
Tracks all game sessions (completed and failed) with detailed stats
Provides leaderboards and player comparison features
"""

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List
import json
import os

GAME_HISTORY_FILE = "data/game_history.json"


@dataclass
class GameSession:
    """Represents a single game session with all stats"""
    
    # Player info
    player_name: str
    character: int
    
    # Game details
    difficulty: str  # EASY, NORMAL, HARD
    result: str  # COMPLETED, GAME_OVER, QUIT
    
    # Core stats
    final_score: int
    coins_collected: int
    levels_completed: int
    enemies_defeated: int
    time_played_seconds: int
    
    # Detailed stats
    deaths: int
    damage_taken: int
    powerups_collected: int
    secrets_found: int
    
    # Metadata
    session_date: str  # ISO format timestamp
    session_id: str  # Unique identifier
    
    # Speedrun (only for completed runs)
    speedrun_time: float = 0.0


class GameHistoryManager:
    """Manages game session history and statistics"""
    
    @staticmethod
    def save_session(session: GameSession) -> bool:
        """
        Save a game session to history
        Args:
            session: GameSession object
        Returns:
            True if successful
        """
        try:
            # Load existing history
            history = GameHistoryManager.load_history()
            
            # Add new session
            history.append(session)
            
            # Save to file
            os.makedirs('data', exist_ok=True)
            with open(GAME_HISTORY_FILE, 'w') as f:
                data = [asdict(s) for s in history]
                json.dump(data, f, indent=2)
            
            print(f"Game session saved: {session.player_name} - {session.result}")
            return True
            
        except Exception as e:
            print(f"Error saving game session: {e}")
            return False
    
    @staticmethod
    def load_history() -> List[GameSession]:
        """
        Load all game sessions from history
        Returns:
            List of GameSession objects
        """
        try:
            if os.path.exists(GAME_HISTORY_FILE):
                with open(GAME_HISTORY_FILE, 'r') as f:
                    data = json.load(f)
                    return [GameSession(**s) for s in data]
            return []
            
        except Exception as e:
            print(f"Error loading game history: {e}")
            return []
    
    # ========================================================================
    # PLAYER-SPECIFIC QUERIES
    # ========================================================================
    
    @staticmethod
    def get_player_sessions(player_name: str) -> List[GameSession]:
        """Get all sessions for a specific player"""
        history = GameHistoryManager.load_history()
        return [s for s in history if s.player_name == player_name]
    
    @staticmethod
    def get_player_stats(player_name: str) -> dict:
        """
        Get aggregate statistics for a player
        Returns:
            Dictionary with comprehensive player stats
        """
        sessions = GameHistoryManager.get_player_sessions(player_name)
        
        if not sessions:
            return {
                'total_sessions': 0,
                'completions': 0,
                'game_overs': 0,
                'quits': 0,
                'total_score': 0,
                'highest_score': 0,
                'lowest_score': 0,
                'avg_score': 0,
                'total_coins': 0,
                'total_enemies': 0,
                'total_deaths': 0,
                'total_damage': 0,
                'total_powerups': 0,
                'total_secrets': 0,
                'total_time_hours': 0.0,
                'completion_rate': 0,
                'best_speedrun': 0.0
            }
        
        # Categorize sessions
        completions = [s for s in sessions if s.result == "COMPLETED"]
        game_overs = [s for s in sessions if s.result == "GAME_OVER"]
        quits = [s for s in sessions if s.result == "QUIT"]
        
        # Calculate stats
        scores = [s.final_score for s in sessions]
        total_score = sum(scores)
        highest_score = max(scores)
        lowest_score = min(scores)
        avg_score = int(total_score / len(sessions))
        
        total_time = sum(s.time_played_seconds for s in sessions)
        
        # Best speedrun time
        speedruns = [s.speedrun_time for s in completions if s.speedrun_time > 0]
        best_speedrun = min(speedruns) if speedruns else 0.0
        
        return {
            'total_sessions': len(sessions),
            'completions': len(completions),
            'game_overs': len(game_overs),
            'quits': len(quits),
            'total_score': total_score,
            'highest_score': highest_score,
            'lowest_score': lowest_score,
            'avg_score': avg_score,
            'total_coins': sum(s.coins_collected for s in sessions),
            'total_enemies': sum(s.enemies_defeated for s in sessions),
            'total_deaths': sum(s.deaths for s in sessions),
            'total_damage': sum(s.damage_taken for s in sessions),
            'total_powerups': sum(s.powerups_collected for s in sessions),
            'total_secrets': sum(s.secrets_found for s in sessions),
            'total_time_hours': round(total_time / 3600, 2),
            'completion_rate': int((len(completions) / len(sessions)) * 100) if sessions else 0,
            'best_speedrun': best_speedrun
        }
    
    # ========================================================================
    # LEADERBOARDS
    # ========================================================================
    
    @staticmethod
    def get_top_scores(limit: int = 10, difficulty: str = None) -> List[GameSession]:
        """
        Get top scores (leaderboard)
        Args:
            limit: Number of entries to return
            difficulty: Filter by difficulty (None = all)
        Returns:
            List of top GameSession objects sorted by score
        """
        history = GameHistoryManager.load_history()
        
        # Filter by difficulty if specified
        if difficulty:
            history = [s for s in history if s.difficulty == difficulty]
        
        # Sort by score descending
        sorted_history = sorted(history, key=lambda s: s.final_score, reverse=True)
        
        return sorted_history[:limit]
    
    @staticmethod
    def get_completed_runs(difficulty: str = None) -> List[GameSession]:
        """
        Get only completed runs
        Args:
            difficulty: Filter by difficulty (None = all)
        Returns:
            List of completed GameSession objects
        """
        history = GameHistoryManager.load_history()
        completed = [s for s in history if s.result == "COMPLETED"]
        
        if difficulty:
            completed = [s for s in completed if s.difficulty == difficulty]
        
        return sorted(completed, key=lambda s: s.final_score, reverse=True)
    
    @staticmethod
    def get_speedrun_leaderboard(difficulty: str = None, limit: int = 10) -> List[GameSession]:
        """
        Get speedrun leaderboard (fastest completions)
        Args:
            difficulty: Filter by difficulty (None = all)
            limit: Number of entries to return
        Returns:
            List of GameSession objects sorted by speedrun time
        """
        completed = GameHistoryManager.get_completed_runs(difficulty)
        
        # Filter only runs with recorded speedrun time
        speedruns = [s for s in completed if s.speedrun_time > 0]
        
        # Sort by time ascending (fastest first)
        sorted_speedruns = sorted(speedruns, key=lambda s: s.speedrun_time)
        
        return sorted_speedruns[:limit]
    
    @staticmethod
    def get_difficulty_leaderboards() -> dict:
        """
        Get leaderboards for each difficulty
        Returns:
            Dictionary with leaderboards per difficulty
        """
        return {
            'EASY': GameHistoryManager.get_top_scores(10, 'EASY'),
            'NORMAL': GameHistoryManager.get_top_scores(10, 'NORMAL'),
            'HARD': GameHistoryManager.get_top_scores(10, 'HARD')
        }
    
    # ========================================================================
    # COMPARISONS
    # ========================================================================
    
    @staticmethod
    def get_all_players() -> List[str]:
        """Get list of all unique player names"""
        history = GameHistoryManager.load_history()
        return sorted(list(set(s.player_name for s in history)))
    
    @staticmethod
    def compare_players(player1: str, player2: str) -> dict:
        """
        Compare stats between two players
        Returns:
            Dictionary with comparison data
        """
        stats1 = GameHistoryManager.get_player_stats(player1)
        stats2 = GameHistoryManager.get_player_stats(player2)
        
        return {
            'player1': player1,
            'player2': player2,
            'stats1': stats1,
            'stats2': stats2,
            'winner_highest_score': player1 if stats1['highest_score'] > stats2['highest_score'] else player2,
            'winner_completions': player1 if stats1['completions'] > stats2['completions'] else player2,
            'winner_completion_rate': player1 if stats1['completion_rate'] > stats2['completion_rate'] else player2
        }
    
    @staticmethod
    def get_global_stats() -> dict:
        """
        Get global statistics across all players
        Returns:
            Dictionary with global stats
        """
        history = GameHistoryManager.load_history()
        
        if not history:
            return {
                'total_sessions': 0,
                'total_players': 0,
                'total_completions': 0,
                'total_score': 0,
                'highest_score': 0,
                'total_playtime_hours': 0.0
            }
        
        all_players = GameHistoryManager.get_all_players()
        completions = [s for s in history if s.result == "COMPLETED"]
        scores = [s.final_score for s in history]
        total_time = sum(s.time_played_seconds for s in history)
        
        return {
            'total_sessions': len(history),
            'total_players': len(all_players),
            'total_completions': len(completions),
            'total_score': sum(scores),
            'highest_score': max(scores) if scores else 0,
            'total_playtime_hours': round(total_time / 3600, 2)
        }
    
    # ========================================================================
    # FILTERS AND SEARCHES
    # ========================================================================
    
    @staticmethod
    def get_recent_sessions(limit: int = 10) -> List[GameSession]:
        """Get most recent game sessions"""
        history = GameHistoryManager.load_history()
        # Sort by date descending (most recent first)
        sorted_history = sorted(history, key=lambda s: s.session_date, reverse=True)
        return sorted_history[:limit]
    
    @staticmethod
    def get_sessions_by_difficulty(difficulty: str) -> List[GameSession]:
        """Get all sessions for a specific difficulty"""
        history = GameHistoryManager.load_history()
        return [s for s in history if s.difficulty == difficulty]
    
    @staticmethod
    def get_sessions_by_result(result: str) -> List[GameSession]:
        """Get all sessions with a specific result"""
        history = GameHistoryManager.load_history()
        return [s for s in history if s.result == result]
    
    # ========================================================================
    # UTILITY
    # ========================================================================
    
    @staticmethod
    def clear_history() -> bool:
        """Clear all game history (use with caution!)"""
        try:
            if os.path.exists(GAME_HISTORY_FILE):
                os.remove(GAME_HISTORY_FILE)
                print("Game history cleared")
            return True
        except Exception as e:
            print(f"Error clearing history: {e}")
            return False
    
    @staticmethod
    def delete_player_sessions(player_name: str) -> bool:
        """Delete all sessions for a specific player"""
        try:
            history = GameHistoryManager.load_history()
            filtered = [s for s in history if s.player_name != player_name]
            
            os.makedirs('data', exist_ok=True)
            with open(GAME_HISTORY_FILE, 'w') as f:
                data = [asdict(s) for s in filtered]
                json.dump(data, f, indent=2)
            
            print(f"Deleted all sessions for {player_name}")
            return True
            
        except Exception as e:
            print(f"Error deleting player sessions: {e}")
            return False
    
    @staticmethod
    def export_stats_to_text(filename: str = "data/game_stats.txt") -> bool:
        """Export statistics to a readable text file"""
        try:
            global_stats = GameHistoryManager.get_global_stats()
            all_players = GameHistoryManager.get_all_players()
            
            with open(filename, 'w') as f:
                f.write("=" * 60 + "\n")
                f.write("RETRO PLATFORMER - GAME STATISTICS\n")
                f.write("=" * 60 + "\n\n")
                
                # Global stats
                f.write("GLOBAL STATISTICS\n")
                f.write("-" * 60 + "\n")
                f.write(f"Total Sessions: {global_stats['total_sessions']}\n")
                f.write(f"Total Players: {global_stats['total_players']}\n")
                f.write(f"Total Completions: {global_stats['total_completions']}\n")
                f.write(f"Highest Score Ever: {global_stats['highest_score']}\n")
                f.write(f"Total Playtime: {global_stats['total_playtime_hours']} hours\n\n")
                
                # Per-player stats
                f.write("PLAYER STATISTICS\n")
                f.write("-" * 60 + "\n")
                for player in all_players:
                    stats = GameHistoryManager.get_player_stats(player)
                    f.write(f"\n{player}:\n")
                    f.write(f"  Games Played: {stats['total_sessions']}\n")
                    f.write(f"  Completions: {stats['completions']}\n")
                    f.write(f"  Completion Rate: {stats['completion_rate']}%\n")
                    f.write(f"  Highest Score: {stats['highest_score']}\n")
                    f.write(f"  Average Score: {stats['avg_score']}\n")
                
                # Leaderboards
                f.write("\n\nLEADERBOARDS\n")
                f.write("-" * 60 + "\n")
                top_scores = GameHistoryManager.get_top_scores(10)
                f.write("\nTop 10 Scores:\n")
                for i, session in enumerate(top_scores, 1):
                    f.write(f"  {i}. {session.player_name} - {session.final_score} ({session.difficulty})\n")
            
            print(f"Stats exported to {filename}")
            return True
            
        except Exception as e:
            print(f"Error exporting stats: {e}")
            return False
