# Retro Pixel Platformer

A nostalgic 2D side-scrolling platformer inspired by NES classics.

**Version:** 0.4 Alpha  
**Status:** Act 1 Complete (7 levels + boss fight)

---

## Quick Start

```bash
# Install dependencies
pip install pygame

# Run setup
python setup.py

# Play the game
python main.py
```

---

## Features

✅ **Classic Platforming** - Run, jump, wall jump  
✅ **Combat System** - Stomp, shoot, melee attacks  
✅ **Boss Battles** - Multi-phase epic encounters  
✅ **3 Difficulty Modes** - Easy, Normal, Hard  
✅ **Save System** - Continue your adventure  
✅ **Act 1 Complete** - 7 levels, 2-3 hours of gameplay

---

## Controls

**Movement:** Arrow Keys or WASD  
**Jump:** Spacebar  
**Shoot:** Z  
**Melee:** X  
**Switch Weapon:** 1-5 (buy weapons and upgrades in the Shop, from the Pause menu)  
**Pause:** P or ESC  
**Save:** F5  

Press **F1** during gameplay for full controls reference.

---

## Documentation

📖 **[PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)** - Complete documentation including:
- Game structure and flow
- File organization
- Installation guide
- Development roadmap
- Technical architecture
- Game design philosophy

---

## Project Structure

```
v0.4/
├── main.py              # Entry point
├── setup.py             # Setup script
├── config/              # Game settings
├── core/                # Game loop & camera
├── entities/            # Player, enemies, bosses
├── objects/             # Collectibles & hazards
├── levels/              # Level data
├── ui/                  # Menus & HUD
├── utils/               # Helpers & utilities
└── save_system/         # Profiles & saves
```

---

## Current Content

**Act 1 (Free):** 7 levels  
- Tutorial level  
- 5 progressive challenge levels  
- Epic boss fight  
- 2-3 hours of gameplay  

**Planned:** Acts 2-4 (18 additional levels)

---

## Requirements

- Python 3.7+
- Pygame 2.0+
- 50MB disk space

---

## Running Tests

Headless end-to-end tests (no window or sound; your saves are not touched):

```bash
cd v0.6
python -m unittest discover -s tests -v
```

Run them before tagging a release. They include a check that every level's
exit is reachable. When editing levels, the checker also works on its own and
lists any unreachable coins:

```bash
python tests/level_checker.py        # all levels
python tests/level_checker.py 3      # just Level 3
```

---

## Development Status

- ✅ Phase 1: Foundation Complete
- 🚧 Phase 2: Content Expansion (In Progress)
- ⏳ Phase 3: Advanced Mechanics
- ⏳ Phase 4: Additional Acts
- ⏳ Phase 5: Polish & Audio
- ⏳ Phase 6: Release & Distribution

---

## License

TBD (Will be determined before public release)

---

## Contact

For questions, feedback, or bug reports, please refer to PROJECT_OVERVIEW.md for more information.

---

**Enjoy the game!** 🎮
