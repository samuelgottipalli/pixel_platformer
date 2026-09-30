# Retro Pixel Platformer

A nostalgic 2D side-scrolling platformer inspired by NES classics.

**Version:** 0.7 Alpha  
**Status:** Acts 1-4 playable (25 levels, 4 boss fights)

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
✅ **4 Acts** - 25 levels across sci-fi, forest, space and cave/underwater themes  
✅ **Level Builder** - Edit and create levels, check them, playtest them

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
v0.6/
├── main.py              # Entry point
├── level_builder.py     # Level builder (python level_builder.py)
├── setup.py             # Setup script
├── config/              # Game settings
├── core/                # Game loop & camera
├── entities/            # Player, enemies, bosses
├── objects/             # Collectibles & hazards
├── levels/              # Level loading; levels/data/actN/*.json = the levels
├── tools/               # Level checker, coin fixer, Act 2-4 generator
├── ui/                  # Menus & HUD
├── utils/               # Helpers & utilities
└── save_system/         # Profiles & saves
```

---

## Current Content

| Act | Name | Levels | Theme | Boss |
|-----|------|--------|-------|------|
| 1 (Free) | The Awakening | 0-6 (tutorial + 5 + boss) | Sci-fi | Guardian |
| 2 | Nature's Fury | 7-12 | Forest | Forest Guardian |
| 3 | Cosmic Voyage | 13-18 | Space | Void Sentinel |
| 4 | Depths Unknown | 19-24 | Caves / underwater | Ancient Evil |

Enemies (and their turret weapons) get tougher every level; tune the rates in
`ENEMY_LEVEL_SCALING` in `config/settings.py`.

---

## Level Builder

```bash
python level_builder.py        # open the first level
python level_builder.py 12     # open level 12
```

Place tiles, coins, enemies, hazards, power-ups, the exit portal and the start
point; press **H** in the builder for all keys. **C** checks the level (is the
exit reachable? which coins can't be collected?), **F** fixes coins
automatically, **P** saves and playtests the level in the game.

Levels are JSON files in `levels/data/actN/`, listed in `levels/data/acts.json`.
Acts 2-4 were made with `tools/level_generator.py` (section-based, every level
verified completable); it never overwrites existing level files unless you pass
`--force`, so builder edits are safe.

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
python tools/level_checker.py        # all levels (in parallel)
python tools/level_checker.py 3      # just Level 3
python tools/fix_coins.py            # move uncollectible coins to reachable spots
```

---

## Development Status

- ✅ Phase 1: Foundation Complete
- 🚧 Phase 2: Content Expansion (In Progress)
- ⏳ Phase 3: Advanced Mechanics
- ✅ Phase 4: Additional Acts (first pass: generated levels, no new enemy types or swimming yet)
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
