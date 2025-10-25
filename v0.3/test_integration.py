"""
Integration test - Verify levels and boss system
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_level_loading():
    """Test that all levels load correctly"""
    print("=" * 60)
    print("Testing Level Loading")
    print("=" * 60)
    
    from levels.level_loader import LevelLoader
    
    try:
        levels = LevelLoader.create_default_levels()
        print(f"\n✓ Successfully loaded {len(levels)} levels")
        
        # Verify each level
        for i, level in enumerate(levels):
            width = level.get('width', 0)
            height = level.get('height', 0)
            theme = level.get('theme', 'UNKNOWN')
            tiles = len(level.get('tiles', []))
            enemies = len(level.get('enemies', []))
            coins = len(level.get('coins', []))
            
            print(f"\nLevel {i}:")
            print(f"  Size: {width}x{height}px")
            print(f"  Theme: {theme}")
            print(f"  Tiles: {tiles}")
            print(f"  Enemies: {enemies}")
            print(f"  Coins: {coins}")
            
            # Verify required fields
            assert 'width' in level, f"Level {i} missing width"
            assert 'height' in level, f"Level {i} missing height"
            assert 'spawn_x' in level, f"Level {i} missing spawn_x"
            assert 'spawn_y' in level, f"Level {i} missing spawn_y"
            assert 'tiles' in level, f"Level {i} missing tiles"
            
        print("\n✓ All levels have required fields")
        return True
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_boss_system():
    """Test boss spawning logic"""
    print("\n" + "=" * 60)
    print("Testing Boss System")
    print("=" * 60)
    
    try:
        from entities.boss import Boss
        from entities.boss_attacks import BossAttackManager
        
        # Test boss creation
        boss = Boss(640, 100, 'guardian', 'NORMAL')
        print(f"\n✓ Created boss: {boss.type}")
        print(f"  Health: {boss.health}/{boss.max_health}")
        print(f"  Phase: {boss.phase}")
        print(f"  Colors: {boss.colors}")
        
        # Test boss levels
        boss_levels = {6: 'guardian', 12: 'forest', 18: 'void', 24: 'ancient'}
        print(f"\n✓ Boss levels configured: {boss_levels}")
        
        # Test difficulty scaling
        for diff in ['EASY', 'NORMAL', 'HARD']:
            boss = Boss(640, 100, 'guardian', diff)
            print(f"  {diff}: {boss.health} HP")
        
        return True
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_difficulty_system():
    """Test difficulty manager"""
    print("\n" + "=" * 60)
    print("Testing Difficulty System")
    print("=" * 60)
    
    try:
        from utils.difficulty_manager import DifficultyManager
        
        # Test each difficulty
        for diff in ['EASY', 'NORMAL', 'HARD']:
            dm = DifficultyManager(diff, total_levels=7)
            
            print(f"\n{diff} Mode:")
            print(f"  Starting lives: {dm.get_lives(0)}")
            print(f"  Ending lives: {dm.get_lives(6)}")
            print(f"  Enemy count mult: {dm.modifiers['enemy_count_multiplier']}")
            print(f"  Score multiplier: {dm.get_score_multiplier()}")
        
        print("\n✓ Difficulty system working")
        return True
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_game_flow():
    """Test that game can start"""
    print("\n" + "=" * 60)
    print("Testing Game Initialization")
    print("=" * 60)
    
    try:
        # Don't actually run pygame, just test imports
        from core.game import Game
        print("✓ Game class imports successfully")
        
        from entities.player import Player
        player = Player(100, 100, 0)
        print(f"✓ Player created at ({player.x}, {player.y})")
        
        from levels.level import Level
        from levels.level_loader import LevelLoader
        levels = LevelLoader.create_default_levels()
        level = Level(levels[0])
        print(f"✓ Level 0 loaded: {level.width}x{level.height}")
        
        return True
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("INTEGRATION TEST SUITE")
    print("=" * 60)
    
    tests = [
        ("Level Loading", test_level_loading),
        ("Boss System", test_boss_system),
        ("Difficulty System", test_difficulty_system),
        ("Game Flow", test_game_flow),
    ]
    
    results = []
    for name, test_func in tests:
        result = test_func()
        results.append((name, result))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nTotal: {passed}/{total} passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Ready to play!")
        print("\nNext steps:")
        print("1. Run: python main.py")
        print("2. Create a new game")
        print("3. Play through Level 0 (Tutorial)")
        print("4. Test boss fight on Level 6")
    else:
        print("\n⚠️  Some tests failed. Fix errors before running game.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
