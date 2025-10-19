"""
Setup script to create necessary directories and __init__.py files
Run this before running the game for the first time
"""
import os

def create_directory_structure():
    """Create all necessary directories"""
    directories = [
        'config',
        'core',
        'entities',
        'objects',
        'levels',
        'levels/data',
        'ui',
        'utils',
        'save_system',
        'data',
        'data/saves'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created directory: {directory}")
        
        # Create __init__.py if it's a Python package directory
        if directory not in ['data', 'data/saves', 'levels/data']:
            init_file = os.path.join(directory, '__init__.py')
            if not os.path.exists(init_file):
                with open(init_file, 'w') as f:
                    f.write(f'"""{directory.replace("/", ".")} package"""\n')
                print(f"  ✓ Created {init_file}")

def verify_structure():
    """Verify all files exist"""
    required_files = [
        'main.py',
        'config/settings.py',
        'config/controls.py',
        'core/game.py',
        'core/camera.py',
        'entities/player.py',
        'entities/enemy.py',
        'entities/projectile.py',
        'entities/particle.py',
        'objects/collectibles.py',
        'objects/hazards.py',
        'objects/portal.py',
        'levels/level.py',
        'levels/level_loader.py',
        'ui/menu.py',
        'ui/hud.py',
        'utils/enums.py',
        'utils/animation.py',
        'utils/collision.py',
        'save_system/profile_manager.py',
        'save_system/save_manager.py'
    ]
    
    missing = []
    for file in required_files:
        if not os.path.exists(file):
            missing.append(file)
    
    if missing:
        print("\n⚠️  Missing files:")
        for file in missing:
            print(f"  ✗ {file}")
        return False
    else:
        print("\n✓ All required files present")
        return True

def main():
    """Run setup"""
    print("=" * 60)
    print("Retro Pixel Platformer - Setup")
    print("=" * 60)
    print()
    
    print("Creating directory structure...")
    create_directory_structure()
    
    print("\nVerifying file structure...")
    if verify_structure():
        print("\n" + "=" * 60)
        print("Setup complete! You can now run: python main.py")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("Setup incomplete. Please create missing files.")
        print("=" * 60)

if __name__ == "__main__":
    main()