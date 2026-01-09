# Retro Pixel Platformer - Complete Project Overview

**Version:** 0.4  
**Status:** Alpha - Act 1 Complete  
**Last Updated:** January 2026

---

## 📋 Table of Contents

1. [Project Vision](#project-vision)
2. [Game Structure & Flow](#game-structure--flow)
3. [File Organization](#file-organization)
4. [Installation & Setup](#installation--setup)
5. [Current Features](#current-features)
6. [Development Roadmap](#development-roadmap)
7. [Technical Architecture](#technical-architecture)
8. [Game Design](#game-design)

---

## 🎯 Project Vision

### Core Concept
A nostalgic 2D side-scrolling platformer inspired by NES classics (Super Mario Bros, Dave) with modern game design. Players rescue a captured character and collect an artifact to defeat a universe-threatening final boss.

### Design Pillars
1. **Retro Aesthetic** - Pixel art, limited colors, classic feel
2. **Skill-Based Gameplay** - Wall jumps, precise platforming, combat mastery
3. **Fair Monetization** - Free Act 1 (2+ hours), affordable Acts 2-4 ($1.99)
4. **Progressive Challenge** - Multiple difficulty modes, clear progression
5. **Replayability** - Score tracking, speedrun potential, collectibles

### Target Audience
- Indie game enthusiasts
- Retro gaming fans (25-40 years old)
- Casual to hardcore platformer players
- Players seeking fair pricing and quality content

---

## 🎮 Game Structure & Flow

### Main Game Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                         MAIN MENU                               │
│  ┌──────────┐  ┌──────────┐  ┌─────────┐  ┌──────────┐        │
│  │New Game  │  │Load Game │  │Controls │  │Level Map │  [Quit]│
│  └────┬─────┘  └────┬─────┘  └─────────┘  └──────────┘        │
└───────┼─────────────┼──────────────────────────────────────────┘
        │             │
        ▼             ▼
  ┌───────────┐  ┌────────────┐
  │ Difficulty│  │Profile     │
  │  Select   │  │Select      │
  │ Easy/Norm │  │(Load Game) │
  │ /Hard     │  └─────┬──────┘
  └─────┬─────┘        │
        │              │
        ▼              │
  ┌───────────┐        │
  │Character  │        │
  │  Select   │        │
  │(4 colors) │        │
  └─────┬─────┘        │
        │              │
        └──────┬───────┘
               ▼
        ┌─────────────┐
        │   PLAYING   │
        │   (Levels)  │
        └──────┬──────┘
               │
     ┌─────────┼─────────┐
     ▼         ▼         ▼
┌─────────┐ ┌──────┐ ┌─────────┐
│Complete │ │Pause │ │Game Over│
│Victory! │ │Menu  │ │ Screen  │
└─────────┘ └──────┘ └─────────┘
```

### Level Progression (Act 1)

```
Level 0: Tutorial → Training Facility
   ↓
Level 1: The Awakening → First Real Challenge
   ↓
Level 2: Rising Conflict → Combat Focus
   ↓
Level 3: The Ascent → Vertical Platforming
   ↓
Level 4: Deep Dive → Underground Lake
   ↓
Level 5: Convergence → Pre-Boss Gauntlet
   ↓
Level 6: Guardian's Lair → BOSS FIGHT
   ↓
Victory Screen → Game Complete (Act 1)
```

### Difficulty System

| Mode   | Lives | Enemy Count | Coins | Time Limit | Boss HP |
|--------|-------|-------------|-------|------------|---------|
| Easy   | 5→3   | 70%         | 150%  | 2x         | 70%     |
| Normal | 3→1   | 100%        | 100%  | 1x         | 100%    |
| Hard   | 1     | 150%        | 70%   | 0.5x       | 150%    |

---

## 📁 File Organization

### Project Structure

```
v0.4/
│
├── main.py                          # Entry point - runs the game
├── setup.py                         # Creates directories and __init__ files
├── PROJECT_OVERVIEW.md             # This file - complete documentation
├── .gitignore                       # Git ignore patterns
│
├── config/                          # Game configuration
│   ├── __init__.py
│   ├── settings.py                  # Constants, colors, physics values
│   └── controls.py                  # Key bindings
│
├── core/                            # Core game systems
│   ├── __init__.py
│   ├── game.py                      # Main game loop, state management
│   └── camera.py                    # Camera follow system
│
├── entities/                        # Game entities (player, enemies, etc.)
│   ├── __init__.py
│   ├── player.py                    # Player movement, combat, stats
│   ├── enemy.py                     # Enemy AI and behavior
│   ├── boss.py                      # Boss entity (multi-phase combat)
│   ├── boss_attacks.py              # Boss attack patterns
│   ├── projectile.py                # Projectile physics
│   └── particle.py                  # Particle effects
│
├── objects/                         # Interactive objects
│   ├── __init__.py
│   ├── collectibles.py              # Coins, keys, powerups
│   ├── hazards.py                   # Spikes, falling blocks, platforms
│   └── portal.py                    # Level transitions
│
├── levels/                          # Level data and loading
│   ├── __init__.py
│   ├── level.py                     # Level class
│   ├── level_loader.py              # Loads levels from Python modules
│   ├── act1_levels_design.py        # Tutorial and Level 1
│   └── act1_complete_levels.py      # Levels 2-6 (full content)
│
├── ui/                              # User interface
│   ├── __init__.py
│   ├── menu.py                      # All menu screens
│   └── hud.py                       # In-game HUD
│
├── utils/                           # Utility modules
│   ├── __init__.py
│   ├── enums.py                     # Game state enums, themes, types
│   ├── textures.py                  # Visual patterns and backgrounds
│   └── difficulty_manager.py        # Difficulty scaling system
│
├── save_system/                     # Save/load functionality
│   ├── __init__.py
│   ├── profile_manager.py           # Player profiles
│   ├── save_manager.py              # Save game state
│   └── difficulty_completion_tracker.py  # Track completed difficulties
│
└── data/                            # Runtime data (created automatically)
    ├── profiles.json                # Active player profiles
    ├── completed_games.json         # Completed game records
    └── saves/                       # Individual save files
        └── save_*.json
```

### Key File Descriptions

**main.py**
- Entry point
- Initializes game and starts main loop
- Error handling

**core/game.py** (1000+ lines)
- Main game loop
- State management (menu, playing, paused, etc.)
- Event handling
- Update logic for all game objects
- Drawing/rendering
- Boss integration

**entities/player.py**
- Player movement (run, jump, double jump, wall jump)
- Combat (stomp, shoot, melee)
- Stats (health, lives, score, coins)
- Power-up management
- Collision detection

**entities/boss.py**
- Multi-phase boss fights (3 phases)
- Phase-based attack patterns
- Health management
- Visual feedback (damage flash, invulnerability)
- Boss-specific colors per type

**levels/act1_complete_levels.py**
- Complete Act 1 level designs (Levels 2-6)
- Each level 8000-10000px wide
- 15-20 minutes per level
- Progressive difficulty scaling
- Boss arena for Level 6

**ui/menu.py**
- Main menu
- Difficulty selection
- Profile selection
- Character selection
- Pause menu
- Game over screen
- Victory screen
- Controls display
- Level map

**save_system/profile_manager.py**
- Create/load/save profiles
- Track stats (score, coins, levels completed)
- Completed games tracking
- Profile deletion on game completion

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.7+ 
- pip (Python package installer)

### Quick Start

```bash
# 1. Install Pygame
pip install pygame

# 2. Navigate to project directory
cd v0.4

# 3. Run setup (creates directories and __init__ files)
python setup.py

# 4. Run the game
python main.py
```

### Verify Installation

```bash
python setup.py
```

Expected output:
```
============================================================
Retro Pixel Platformer - Setup
============================================================

Creating directory structure...
✓ Created directory: config
✓ Created directory: core
...
✓ All required files present

============================================================
Setup complete! You can now run: python main.py
============================================================
```

### Troubleshooting

**"ModuleNotFoundError: No module named 'pygame'"**
```bash
pip install pygame
# or
pip3 install pygame
```

**"ModuleNotFoundError: No module named 'config'"**
- Ensure you're running from v0.4/ directory
- Run `python setup.py` to create `__init__.py` files

**"FileNotFoundError" for save files**
- Normal on first run
- data/ directory created automatically
- Profiles saved after creating first character

---

## ✅ Current Features (v0.4)

### Completed Systems

**Player Mechanics**
- ✅ Run, jump, double jump
- ✅ Wall jump with precise timing
- ✅ Stomp enemies from above
- ✅ Projectile shooting
- ✅ Melee attack with weapon levels
- ✅ Health and lives system
- ✅ Invincibility frames after damage
- ✅ Power-up collection (health, double jump, speed, invincible)

**Enemy System**
- ✅ Ground patrol enemies
- ✅ Flying enemies with patrol patterns
- ✅ Turret enemies (stationary shooting)
- ✅ Enemy health and damage
- ✅ Death particles and score rewards

**Boss System**
- ✅ Multi-phase combat (3 phases)
- ✅ Guardian boss (Act 1)
- ✅ Phase transitions with invulnerability
- ✅ Multiple attack patterns:
  - Single projectile
  - Projectile spread
  - Ground slam with shockwave
  - Laser beam (phase 3)
  - Orbital projectiles (phase 3)
- ✅ Boss health bar display
- ✅ Victory portal spawns on defeat

**Level Design**
- ✅ 7 complete Act 1 levels
- ✅ Tutorial level (training facility)
- ✅ 5 main levels (8000-10000px each)
- ✅ Boss arena (Level 6)
- ✅ Multiple themes (Sci-Fi, Nature, Space, Underground, Underwater)
- ✅ Parallax scrolling backgrounds
- ✅ Theme-specific visual effects

**Collectibles & Objects**
- ✅ Coins (1, 2, 5, 10, 15 value)
- ✅ Keys (colored, required for certain portals)
- ✅ Power-ups (4 types with timed effects)
- ✅ Portals (level transitions)
- ✅ Hazards (spikes, falling blocks, moving platforms)

**UI/UX**
- ✅ Main menu with mouse support
- ✅ Difficulty selection (Easy/Normal/Hard)
- ✅ Character selection (4 color variants)
- ✅ Profile creation and management
- ✅ Profile selection screen
- ✅ Pause menu (Resume/Save/Quit)
- ✅ Game over screen
- ✅ Victory screen
- ✅ Controls reference screen
- ✅ Level map display
- ✅ In-game HUD (health, lives, score, coins, weapon level)
- ✅ F1 toggleable controls overlay

**Save System**
- ✅ Profile creation/deletion
- ✅ Save game state (F5 or auto-save on quit)
- ✅ Load game (continues from last checkpoint)
- ✅ Completed games tracking
- ✅ Profile stats persistence
- ✅ Difficulty completion tracking

**Difficulty Modes**
- ✅ Easy mode (more lives, fewer enemies, more coins)
- ✅ Normal mode (balanced experience)
- ✅ Hard mode (one life, more enemies, less resources)
- ✅ Progressive difficulty scaling within levels
- ✅ Difficulty-adjusted boss health

**Visual Features**
- ✅ Colorblind-friendly patterns (vertical/horizontal stripes)
- ✅ Parallax backgrounds per theme
- ✅ Particle effects (enemy death, collections, boss defeat)
- ✅ Damage flash effects
- ✅ Power-up visual indicators
- ✅ Boss phase visual changes

**Camera System**
- ✅ Smooth player follow
- ✅ Level boundary constraints
- ✅ Lookahead in movement direction

---

## 🗺️ Development Roadmap

### Phase 1: Foundation ✅ COMPLETE
- Core game engine
- All basic mechanics
- Modular architecture
- Save/load system
- Act 1 (7 levels) complete

### Phase 2: Content Expansion 🚧 IN PROGRESS
**Next Immediate Steps:**
1. ⏳ Playtest Act 1 thoroughly
2. ⏳ Fix any discovered bugs
3. ⏳ Balance difficulty across all levels
4. ⏳ Add story text/cutscenes
5. ⏳ Begin Act 2 design (Nature theme)

**Act 2 Goals:**
- Levels 7-12 (Nature/Forest theme)
- Forest Guardian boss (Level 12)
- New enemy types
- New hazards
- Story progression

### Phase 3: Advanced Mechanics ⏳ PLANNED
- ⏳ Underwater level mechanics
  - Swimming physics
  - Oxygen meter
  - Water currents
  - Underwater enemies
- ⏳ Checkpoint system
- ⏳ More power-up types
- ⏳ Secret areas and collectibles
- ⏳ Achievement tracking

### Phase 4: Acts 3-4 ⏳ PLANNED
**Act 3 (Levels 13-18):**
- Space theme
- Void Sentinel boss
- Zero-gravity sections (optional)
- Advanced platforming

**Act 4 (Levels 19-24):**
- Underground/Underwater finale
- Ancient Evil final boss
- Multi-phase epic battle
- Story conclusion

### Phase 5: Polish & Audio ⏳ PLANNED
**Sound Effects:**
- Player actions (jump, shoot, melee, damage)
- Enemy sounds
- Collectibles
- Menu navigation

**Music:**
- Main menu theme
- Per-theme background music
- Boss battle music
- Victory/game over themes

**Visual Polish:**
- Better animations
- Screen transitions
- Enhanced particles
- HUD animations

### Phase 6: Packaging & Release ⏳ PLANNED
- Full playthrough testing
- Bug fixing
- Performance optimization
- Cross-platform testing
- Documentation
- Standalone executable creation
- Distribution (itch.io, GitHub)

---

## 🏗️ Technical Architecture

### Core Design Patterns

**Game State Machine**
```python
class GameState(Enum):
    MENU = 1
    DIFFICULTY_SELECT = 2
    PROFILE_SELECT = 3
    CHAR_SELECT = 4
    PLAYING = 5
    PAUSED = 6
    GAME_OVER = 7
    LEVEL_COMPLETE = 8
    VICTORY = 9
    CONTROLS = 10
    LEVEL_MAP = 11
```

**Main Game Loop**
```python
def run(self):
    while self.running:
        self._handle_events()    # Process input
        self._update()           # Update game state
        self._draw()             # Render to screen
        self.clock.tick(FPS)     # 60 FPS
```

**Entity System**
- All entities inherit from base classes
- Update/Draw pattern
- Collision detection via pygame.Rect
- State management per entity

**Level Loading**
- Levels defined as Python dictionaries
- Dynamic loading via imports
- Fallback demo levels if Act files missing
- JSON export capability (future level editor)

### Performance Considerations

**Collision Optimization**
- Only check nearby tiles
- Projectile pooling
- Particle cleanup

**Memory Management**
- Remove inactive projectiles immediately
- Limit particle count
- Clear level data on transition

**Rendering**
- Camera culling (only draw visible objects)
- Minimal overdraw
- Efficient particle drawing

---

## 🎨 Game Design

### Level Design Philosophy

**Pacing**
Each level follows this structure:
1. Safe introduction area
2. Introduce/reinforce mechanic
3. Light challenge
4. Main challenge section
5. Combat arena or platforming gauntlet
6. Cool-down area
7. Portal to next level

**Duration**
- Tutorial: 5-8 minutes
- Main levels: 15-20 minutes each
- Boss fight: 10-15 minutes

**Progressive Difficulty**
- Easy start within each level
- Gradual escalation
- Peak difficulty 75% through
- Slight cool-down before exit

### Combat Design

**Player Options**
1. **Stomp** - Jump on enemies (instant kill, safe)
2. **Shoot** - Ranged attack (uses ammo/cooldown)
3. **Melee** - Close combat (risky but high reward)

**Enemy Types**
1. **Ground Patrol** - Basic enemies, predictable
2. **Flying** - Vertical threat, requires timing
3. **Turret** - Stationary ranged threat

**Boss Phases**
- **Phase 1 (100-66% HP)**: Learning phase, basic attacks
- **Phase 2 (66-33% HP)**: Increased speed, new attacks
- **Phase 3 (33-0% HP)**: All attacks unlocked, maximum challenge

### Collectible Economy

**Coins**
- Value 1: Common (80% of coins)
- Value 2: Uncommon (15% of coins)
- Value 5: Rare (4% of coins)
- Value 10: Very rare (0.9% of coins)
- Value 15: Secret/hard to reach (0.1% of coins)

**Power-ups**
- Health: Restore 1 heart
- Double Jump: 30 seconds
- Speed: 20 seconds
- Invincible: 10 seconds

### Accessibility Features

**Colorblind Support**
- Distinct visual patterns (vertical/horizontal/diagonal stripes)
- Not relying solely on color for differentiation
- High contrast UI elements

**Difficulty Options**
- Easy mode for casual players
- Hard mode for challenge seekers
- Clear difficulty descriptions

**Controls**
- Rebindable keys (future)
- Gamepad support (future)
- F1 in-game controls reference

---

## 📊 Current Content Summary

### Act 1 Complete (Free Version)

**7 Levels:**
- Level 0: Tutorial
- Levels 1-5: Progressive challenge
- Level 6: Boss fight

**Gameplay Time:** 2-3 hours (first playthrough)

**Content Stats:**
- ~70,000 pixels of level design
- 100+ enemies
- 50+ hazards
- 400+ coins
- 25+ power-ups
- 1 epic boss fight

**Replayability:**
- 3 difficulty modes
- Score chasing
- Speedrun potential
- Multiple playstyles

---

## 🎯 Success Metrics

### Minimum Viable Product ✅
- ✅ Core mechanics working
- ✅ 7 playable levels
- ✅ 1 boss fight
- ✅ Save/load functionality
- ✅ Stable, bug-free experience

### Full Release Goals
- ⏳ 25 total levels
- ⏳ 4 boss fights
- ⏳ All 5 themes implemented
- ⏳ Sound effects and music
- ⏳ Polished UI/UX
- ⏳ Packaged for distribution

### Stretch Goals
- ⏳ Level editor
- ⏳ Achievement system
- ⏳ Speedrun timer/leaderboards
- ⏳ New Game+ mode
- ⏳ Additional characters

---

## 📝 Development Notes

### Known Technical Debt
- Add JSON validation for level data
- Improve error handling throughout
- Add comprehensive logging system
- Optimize collision detection for large levels

### Future Enhancements
- Asset manager for sprites
- Configuration file for settings
- Procedurally generated challenge levels
- Daily challenges
- Steam Workshop integration (far future)

### Community Features (Future)
- Level sharing system
- Online leaderboards
- Replay system
- Community challenges

---

## 🤝 Contributing

This is currently a solo project, but contributions may be accepted in the future.

### Code Style
- Follow PEP 8
- Descriptive variable names
- Comprehensive docstrings
- Type hints where appropriate

### Testing
- Test all difficulty modes
- Verify save/load functionality
- Check collision edge cases
- Platform compatibility testing

---

## 📄 License

TBD - Will be decided before public release

---

## 🙏 Acknowledgments

**Inspiration:**
- Super Mario Bros (NES)
- Dave (DOS)
- Celeste
- Shovel Knight

**Tools:**
- Python 3.11
- Pygame 2.5.0
- VS Code
- Git

---

## 📞 Contact & Support

**Development Status:** Active  
**Current Version:** 0.4 Alpha  
**Next Milestone:** Act 1 Polish & Act 2 Design  

---

**Last Updated:** January 2026  
**Document Version:** 1.0  
**Game Version:** 0.4 Alpha
