# Installation & Setup Guide

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Step-by-Step Installation

### 1. Install Python
Download and install Python from [python.org](https://www.python.org/downloads/)

Verify installation:
```bash
python --version
# or
python3 --version
```

### 2. Install Pygame
```bash
pip install pygame
# or
pip3 install pygame
```

### 3. Set Up Project Structure

**Option A: Manual Setup**
1. Create the directory structure as shown in the project
2. Copy all `.py` files to their respective directories
3. Run the setup script:
```bash
python setup.py
```

**Option B: Clone Repository (if using Git)**
```bash
git clone <repository-url>
cd retro_platformer
python setup.py
```

### 4. Verify Installation
The setup script will check for all required files and create necessary directories.

Expected output:
```
============================================================
Retro Pixel Platformer - Setup
============================================================

Creating directory structure...
✓ Created directory: config
  ✓ Created config/__init__.py
...

Verifying file structure...
✓ All required files present

============================================================
Setup complete! You can now run: python main.py
============================================================
```

### 5. Run the Game
```bash
python main.py
```

## Directory Structure

After setup, your project should look like this:

```
retro_platformer/
├── main.py                 # Entry point
├── setup.py               # Setup script
├── config/
│   ├── __init__.py
│   ├── settings.py
│   └── controls.py
├── core/
│   ├── __init__.py
│   ├── game.py
│   └── camera.py
├── entities/
│   ├── __init__.py
│   ├── player.py
│   ├── enemy.py
│   ├── projectile.py
│   └── particle.py
├── objects/
│   ├── __init__.py
│   ├── collectibles.py
│   ├── hazards.py
│   └── portal.py
├── levels/
│   ├── __init__.py
│   ├── level.py
│   ├── level_loader.py
│   └── data/              # Level JSON files (auto-created)
├── ui/
│   ├── __init__.py
│   ├── menu.py
│   └── hud.py
├── utils/
│   ├── __init__.py
│   ├── enums.py
│   ├── animation.py
│   └── collision.py
├── save_system/
│   ├── __init__.py
│   ├── profile_manager.py
│   └── save_manager.py
└── data/                  # Runtime data (auto-created)
    ├── profiles.json
    └── saves/
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'pygame'"
**Solution:** Install pygame:
```bash
pip install pygame
```

### "ModuleNotFoundError: No module named 'config'"
**Solution:** 
1. Make sure you're running from the project root directory
2. Run `python setup.py` to create `__init__.py` files
3. Check that all `__init__.py` files exist

### "FileNotFoundError" for data directories
**Solution:** Run `python setup.py` to create all directories

### Game crashes on startup
**Solution:**
1. Check Python version (3.7+)
2. Reinstall pygame: `pip uninstall pygame && pip install pygame`
3. Check the error traceback in console
4. Verify all `.py` files are in correct directories

### Controls not working
**Solution:** Check `config/controls.py` for key bindings. Default controls:
- Movement: WASD or Arrow Keys
- Jump: Space
- Shoot: Z
- Melee: X
- Pause: P or ESC

### Save files not working
**Solution:**
1. Check that `data/saves/` directory exists
2. Verify write permissions
3. Check console for error messages

## Testing Checklist

After installation, test the following:

- [ ] Game starts without errors
- [ ] Main menu displays correctly
- [ ] Can create new profile
- [ ] Can select character
- [ ] Game loads Level 1
- [ ] Player can move (WASD/Arrows)
- [ ] Player can jump (Space)
- [ ] Player can shoot (Z)
- [ ] Player can melee attack (X)
- [ ] Coins can be collected
- [ ] Enemies can be defeated
- [ ] Can pause game (P/ESC)
- [ ] Can save game (F5)
- [ ] Portal works (leads to Level 2)
- [ ] Game over screen appears when out of lives
- [ ] Can return to main menu

## Performance Tips

### If game runs slowly:
1. Close other applications
2. Reduce particle effects (edit `config/settings.py`)
3. Lower FPS if needed (change `FPS = 60` to `FPS = 30` in settings)

### If game uses too much memory:
1. Limit number of particles
2. Reduce level size
3. Clear projectiles more frequently

## Uninstallation

To remove the game:
1. Delete the project directory
2. (Optional) Uninstall pygame: `pip uninstall pygame`

## Getting Help

If you encounter issues:
1. Check console output for error messages
2. Verify all files are in correct locations
3. Ensure all dependencies are installed
4. Check Python version compatibility

## Next Steps

After successful installation:
1. Play through the demo levels
2. Test all game mechanics
3. Check the Project Charter for development roadmap
4. Start adding new levels or features!

---

**Minimum System Requirements:**
- OS: Windows 7+, macOS 10.12+, Linux (any recent distro)
- RAM: 512MB
- Processor: 1GHz
- Storage: 50MB
- Python: 3.7+
- Pygame: 2.0+