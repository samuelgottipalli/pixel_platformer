"""
RETRO PIXEL PLATFORMER - PROJECT STRUCTURE
==========================================

retro_platformer/
│
├── main.py                      # Entry point - runs the game
│
├── config/
│   ├── __init__.py
│   ├── settings.py              # Game constants, colors, physics
│   └── controls.py              # Key bindings configuration
│
├── core/
│   ├── __init__.py
│   ├── game.py                  # Main game loop and state management
│   └── camera.py                # Camera system
│
├── entities/
│   ├── __init__.py
│   ├── player.py                # Player class
│   ├── enemy.py                 # Enemy class
│   ├── projectile.py            # Projectile class
│   └── particle.py              # Particle effects
│
├── objects/
│   ├── __init__.py
│   ├── collectibles.py          # Coin, Key, PowerUp classes
│   ├── hazards.py               # Hazard class (spikes, falling blocks, etc.)
│   └── portal.py                # Portal class
│
├── levels/
│   ├── __init__.py
│   ├── level.py                 # Level class
│   ├── level_loader.py          # Level loading from JSON
│   └── data/                    # Level JSON files
│       ├── level_01.json
│       ├── level_02.json
│       └── level_03.json
│
├── ui/
│   ├── __init__.py
│   ├── menu.py                  # Menu screens
│   ├── hud.py                   # In-game HUD
│   └── fonts.py                 # Font management
│
├── utils/
│   ├── __init__.py
│   ├── enums.py                 # Enumerations (GameState, Theme, etc.)
│   ├── animation.py             # Animation class
│   └── collision.py             # Collision detection helpers
│
├── save_system/
│   ├── __init__.py
│   ├── profile_manager.py       # Player profile management
│   └── save_manager.py          # Save/Load game state
│
└── data/                        # Runtime data (created by game)
    ├── profiles.json
    └── saves/
        ├── save_Player1.json
        └── save_Player2.json

==========================================
INSTALLATION & RUNNING:

1. Create the directory structure above
2. Copy the code files I'll provide into their respective locations
3. Install pygame: pip install pygame
4. Run: python main.py

==========================================
"""