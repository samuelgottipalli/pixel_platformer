# Level Editor & Difficulty System - Complete Guide

## 🎮 What's New

### ✅ Difficulty System
- **Three difficulty modes:** Easy, Normal, Hard
- **Progressive difficulty:** Levels get harder as you progress
- **Smart scaling:** Last level of Easy = First level of Normal difficulty
- **Automatic adjustments:** Lives, enemy count/damage, coins, powerups, costs, time limits

### ✅ Level Editor
- **Visual editor:** Click-to-place level design tool
- **Real-time preview:** See your level as you build it
- **JSON export:** Save levels for use in the game
- **All object types:** Tiles, enemies, coins, hazards, portals, keys, powerups

---

## 🎯 Difficulty System Details

### How It Works

**Player Chooses Difficulty:**
- **Easy:** 5 lives, more resources, easier enemies, 2x time
- **Normal:** 3 lives, balanced, standard time
- **Hard:** 1 life, fewer resources, tougher enemies, 0.5x time

**Progressive Scaling:**
- As you complete levels, difficulty increases within your chosen mode
- Level 1 Easy → Level 20 Easy (gets progressively harder)
- Level 20 Easy ≈ Level 1 Normal (difficulty matches)
- Level 20 Normal ≈ Level 1 Hard (difficulty matches)

### Difficulty Parameters

| Parameter | Easy | Normal | Hard |
|-----------|------|--------|------|
| **Lives** | 5 → 3 | 3 → 1 | 1 |
| **Enemy Count** | 70% | 100% | 150% |
| **Enemy Damage** | 70% | 100% | 150% |
| **Coins** | 150% | 100% | 70% |
| **Powerups** | 150% | 100% | 60% |
| **Upgrade Costs** | 70% | 100% | 150% |
| **Time Limit** | 2x | 1x | 0.5x |
| **Score Multiplier** | 1x | 1.5x | 2x |

**Plus progressive scaling** - all these values adjust as player progresses through levels!

---

## 🛠️ Level Editor Usage

### Starting the Editor

```bash
python level_editor.py
```

### Controls

**Mode Selection (Number Keys):**
- `1` - Tile mode (ground/platforms)
- `2` - Enemy mode
- `3` - Coin mode
- `4` - Powerup mode
- `5` - Hazard mode
- `6` - Portal mode
- `7` - Key mode
- `8` - Spawn point mode

**Mouse Controls:**
- `Left Click` - Place object at cursor
- `Right Click` - Remove object at cursor

**Camera:**
- `Arrow Keys` - Pan camera around level

**Sub-Options:**
- `E` - Cycle enemy type (ground/flying/turret)
- `H` - Cycle hazard type (spike/falling_block/moving_platform)
- `P` - Cycle powerup type (health/speed/invincible/double_jump)
- `T` - Change theme (SCIFI/NATURE/SPACE/UNDERGROUND/UNDERWATER)
- `L` - Change time limit (short/medium/long/none)

**File Operations:**
- `Ctrl+S` - Save level (prompts for filename)
- `Ctrl+O` - Load level (prompts for filename)
- `Ctrl+C` - Clear all objects

**Help:**
- `F1` - Toggle help overlay

---

## 📝 Level Design Workflow

### Step 1: Plan Your Level

**Ask yourself:**
- What's the difficulty target? (Early game, mid game, end game?)
- What's the main challenge? (Platforming, combat, puzzle, mixed?)
- What theme fits? (Sci-fi, nature, space, underground, underwater?)
- How long should it take? (1-3 minutes?)

### Step 2: Create Base Geometry

1. Run `python level_editor.py`
2. Press `1` for Tile mode
3. Press `T` to select theme
4. Left-click to place ground and platforms
5. Create your level layout

**Tips:**
- Start with main path first
- Add platforms for vertical movement
- Create safe zones and challenge zones
- Leave room for enemies

### Step 3: Set Spawn Point

1. Press `8` for Spawn mode
2. Click where player should start
3. Green crosshair marks spawn location

### Step 4: Add Enemies

1. Press `2` for Enemy mode
2. Press `E` to cycle enemy types:
   - **Ground** - Patrols horizontally
   - **Flying** - Sine wave movement
   - **Turret** - Stationary shooter
3. Click to place enemies

**Placement Tips:**
- Ground enemies on platforms
- Flying enemies in open spaces
- Turrets at choke points
- Don't overcrowd (difficulty system will add more on Hard)

### Step 5: Add Collectibles

**Coins** (Press `3`):
- Place along main path
- Add in risky areas for risk/reward
- Remember: Easy mode gets 1.5x coins!

**Powerups** (Press `4`):
- Press `P` to cycle types
- Place before difficult sections
- Use health before boss areas
- Speed/invincible for challenge rooms

**Keys** (Press `7`):
- For locked portals
- Different colors for visual variety

### Step 6: Add Hazards

1. Press `5` for Hazard mode
2. Press `H` to cycle types:
   - **Spike** - Instant damage obstacle
   - **Falling Block** - Triggered by proximity
   - **Moving Platform** - Transportation + challenge
3. Click to place

**Placement Tips:**
- Spikes below jumps
- Falling blocks over pits
- Moving platforms for progression

### Step 7: Add Portal

1. Press `6` for Portal mode
2. Click at level end
3. Purple ellipse marks portal
4. Edit JSON to set destination level

### Step 8: Set Time Limit

- Press `L` to cycle: short (1min) / medium (2min) / long (3min) / none
- Consider level length and difficulty
- Remember: Easy gets 2x time, Hard gets 0.5x time

### Step 9: Save Level

1. Press `Ctrl+S`
2. Enter filename (e.g., "level_04")
3. File saved to `levels/data/level_04.json`

### Step 10: Test & Refine

1. Add level to game's level list
2. Playtest on all difficulties
3. Adjust based on feedback
4. Reload in editor and refine

---

## 📦 Adding Your Level to the Game

### Method 1: Edit level_loader.py

Open `levels/level_loader.py` and add your level:

```python
# Load your custom level
level4 = LevelLoader.load_from_file('level_04.json')
if level4:
    levels.append(level4)
```

### Method 2: Direct JSON

Your saved level JSON looks like this:

```json
{
  "width": 3200,
  "height": 720,
  "theme": "NATURE",
  "spawn_x": 100,
  "spawn_y": 500,
  "time_limit": "medium",
  "tiles": [...],
  "enemies": [...],
  "coins": [...],
  "powerups": [...],
  "keys": [...],
  "hazards": [...],
  "portals": [...]
}
```

---

## 🎨 Level Design Tips

### Difficulty Curve

**Easy Levels (1-7):**
- Wide platforms
- Few enemies
- Generous coin placement
- Clear paths
- Forgiving jumps

**Medium Levels (8-14):**
- Narrower platforms
- More enemies
- Tighter timing
- Some secret paths
- Precision required

**Hard Levels (15-20):**
- Pixel-perfect jumps
- Many enemies
- Complex hazards
- Hidden paths
- Master-level challenge

### Theme Usage

- **SCIFI (Levels 1-5):** Introduction, tutorials
- **NATURE (Levels 6-10):** Exploration, organic challenges
- **SPACE (Levels 11-15):** Precision, zero-gravity feel
- **UNDERGROUND (Levels 16-18):** Tight spaces, dark palette
- **UNDERWATER (Levels 19-20):** Final challenges (when implemented)

### Pacing

**Good level flow:**
1. Safe start area
2. Easy warm-up challenge
3. Introduce mechanic
4. Main challenge using mechanic
5. Difficult section (optional path)
6. Cool-down area
7. Portal to next level

---

## 🐛 Troubleshooting

### Editor Issues

**"Can't save file":**
- Make sure `levels/data/` directory exists
- Check file permissions
- Don't use special characters in filename

**"Objects not appearing":**
- Check camera position (use arrow keys)
- Make sure you're in correct mode
- Check object is within level bounds

**"Game won't load my level":**
- Verify JSON is valid
- Check file path is correct
- Make sure all required fields exist

### Difficulty System

**"Enemy count seems wrong":**
- Remember difficulty multiplier applies
- Progressive scaling adds more over time
- Check difficulty manager settings

**"Time limit not working":**
- Make sure time_limit field is in JSON
- Check it's not set to "none"
- Verify difficulty multiplier is applying

---

## 📊 Level Statistics

**Track these while designing:**
- Enemy count
- Coin count
- Hazard count
- Estimated completion time
- Required skill level

**Use editor's bottom-left display:**
- Shows real-time object counts
- Helps balance resources
- Ensures variety

---

## 🚀 Next Steps

1. **Create levels 4-10** using the editor
2. **Playtest each difficulty** mode
3. **Balance resources** based on testing
4. **Add story elements** between levels
5. **Create boss levels** (coming next phase)

---

## 📝 Level Design Checklist

Before finalizing a level:

- [ ] Has clear start (spawn point)
- [ ] Has clear end (portal)
- [ ] Difficulty appropriate for position in game
- [ ] Multiple paths (optional)
- [ ] Risk/reward collectibles
- [ ] Fair challenge (beatable but fun)
- [ ] Theme is consistent
- [ ] Time limit is reasonable
- [ ] Tested on all 3 difficulties
- [ ] No soft-locks or dead ends
- [ ] Fun to replay

---

**Happy Level Designing! 🎮**