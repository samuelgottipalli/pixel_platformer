"""
Complete Act 1 Levels 2-6
Ready for integration into level_loader.py
"""

from config.settings import TILE_SIZE


def get_complete_act1_levels():
    """
    Get complete Act 1 levels 2-6
    Returns list of level dictionaries ready to load
    """
    levels = []

    # ============================================================
    # LEVEL 2: "RISING CONFLICT" (18 minutes, 8500px)
    # ============================================================

    level_2 = {
        "width": 8500,
        "height": 720,
        "theme": "SCIFI",
        "spawn_x": 100,
        "spawn_y": 500,
        "time_limit": "long",
        "tiles": [
            # === AREA 1: GENTLE START (0-1500) ===
            *[{"x": i * TILE_SIZE, "y": 640, "solid": True} for i in range(50)],
            # Ascending platforms
            *[
                {"x": 300 + i * 100, "y": 600 - i * 30, "solid": True}
                for i in range(12)
            ],
            *[
                {"x": 332 + i * 100, "y": 600 - i * 30, "solid": True}
                for i in range(12)
            ],
            # === AREA 2: TOWER CLIMB (1500-2800) ===
            # Main tower structure
            *[{"x": 1500, "y": 640 - i * TILE_SIZE, "solid": True} for i in range(18)],
            *[{"x": 1532, "y": 640 - i * TILE_SIZE, "solid": True} for i in range(18)],
            # Side platforms for zigzag climb
            *[
                {"x": 1600 + (i % 2) * 150, "y": 600 - i * 40, "solid": True}
                for i in range(15)
            ],
            *[
                {"x": 1632 + (i % 2) * 150, "y": 600 - i * 40, "solid": True}
                for i in range(15)
            ],
            # Stepping stones from the tower top to the top platform
            # (the 390px gap was wider than a double jump)
            *[{"x": 1900 + i * TILE_SIZE, "y": 110, "solid": True} for i in range(2)],
            *[{"x": 2050 + i * TILE_SIZE, "y": 130, "solid": True} for i in range(2)],
            # Top platform
            *[{"x": 2200 + i * TILE_SIZE, "y": 150, "solid": True} for i in range(20)],
            # === AREA 3: HIGH PLATFORMS (2800-4200) ===
            # Floating island section
            *[
                {"x": 2800 + i * 200, "y": 200 + (i % 3) * 60, "solid": True}
                for i in range(15)
            ],
            *[
                {"x": 2832 + i * 200, "y": 200 + (i % 3) * 60, "solid": True}
                for i in range(15)
            ],
            # Drop platforms
            *[{"x": 3500, "y": 200 + i * 80, "solid": True} for i in range(6)],
            *[{"x": 3532, "y": 200 + i * 80, "solid": True} for i in range(6)],
            # Ground return
            *[{"x": 3800 + i * TILE_SIZE, "y": 640, "solid": True} for i in range(30)],
            # === AREA 4: UNDERGROUND PASSAGE (4200-5800) ===
            # Descent into underground
            *[{"x": 4200 + i * 80, "y": 640 - i * 20, "solid": True} for i in range(8)],
            *[{"x": 4232 + i * 80, "y": 640 - i * 20, "solid": True} for i in range(8)],
            # Underground floor and ceiling
            *[{"x": 4800 + i * TILE_SIZE, "y": 640, "solid": True} for i in range(35)],
            *[{"x": 4800 + i * TILE_SIZE, "y": 400, "solid": True} for i in range(35)],
            # Pillars in underground
            *[{"x": 5000, "y": 400 + i * TILE_SIZE, "solid": True} for i in range(4)],
            *[{"x": 5200, "y": 400 + i * TILE_SIZE, "solid": True} for i in range(4)],
            *[{"x": 5400, "y": 400 + i * TILE_SIZE, "solid": True} for i in range(4)],
            # === AREA 5: COMBAT ARENA (5800-7000) ===
            *[{"x": 5800 + i * TILE_SIZE, "y": 640, "solid": True} for i in range(40)],
            # Multi-level combat platforms
            *[{"x": 5900, "y": 550, "solid": True}],
            *[{"x": 5932, "y": 550, "solid": True}],
            *[{"x": 6100, "y": 500, "solid": True}],
            *[{"x": 6132, "y": 500, "solid": True}],
            *[{"x": 6300, "y": 450, "solid": True}],
            *[{"x": 6332, "y": 450, "solid": True}],
            *[{"x": 6500, "y": 500, "solid": True}],
            *[{"x": 6532, "y": 500, "solid": True}],
            *[{"x": 6700, "y": 550, "solid": True}],
            *[{"x": 6732, "y": 550, "solid": True}],
            # === AREA 6: FINAL GAUNTLET (7000-8500) ===
            *[{"x": 7000 + i * TILE_SIZE, "y": 640, "solid": True} for i in range(50)],
            # Platforming challenge
            *[
                {"x": 7100 + i * 120, "y": 550 - (i % 4) * 40, "solid": True}
                for i in range(20)
            ],
            *[
                {"x": 7132 + i * 120, "y": 550 - (i % 4) * 40, "solid": True}
                for i in range(20)
            ],
            # Final climb to exit
            *[{"x": 8200, "y": 640 - i * TILE_SIZE, "solid": True} for i in range(12)],
            *[{"x": 8232, "y": 640 - i * TILE_SIZE, "solid": True} for i in range(12)],
            *[{"x": 8200 + i * TILE_SIZE, "y": 260, "solid": True} for i in range(10)],
        ],
        "enemies": [
            # Area 1 - Easy intro
            {"x": 500, "y": 550, "type": "ground", "patrol": 150},
            {"x": 800, "y": 450, "type": "ground", "patrol": 120},
            # Area 2 - Tower climb
            {"x": 1650, "y": 550, "type": "flying", "patrol": 150},
            {"x": 1700, "y": 400, "type": "ground", "patrol": 80},
            {"x": 1850, "y": 350, "type": "ground", "patrol": 80},
            {"x": 2000, "y": 250, "type": "flying", "patrol": 200},
            # Area 3 - High platforms
            {"x": 2900, "y": 200, "type": "flying", "patrol": 250},
            {"x": 3200, "y": 250, "type": "flying", "patrol": 200},
            {"x": 3500, "y": 300, "type": "ground", "patrol": 100},
            # Area 4 - Underground
            {"x": 5000, "y": 590, "type": "ground", "patrol": 180},
            {"x": 5200, "y": 590, "type": "ground", "patrol": 180},
            {"x": 5400, "y": 590, "type": "ground", "patrol": 180},
            {"x": 5100, "y": 500, "type": "flying", "patrol": 200},
            {"x": 5300, "y": 500, "type": "flying", "patrol": 200},
            # Area 5 - Combat arena
            {"x": 5950, "y": 500, "type": "ground", "patrol": 100},
            {"x": 6150, "y": 450, "type": "ground", "patrol": 100},
            {"x": 6350, "y": 400, "type": "flying", "patrol": 150},
            {"x": 6550, "y": 450, "type": "ground", "patrol": 100},
            {"x": 6750, "y": 500, "type": "ground", "patrol": 100},
            {"x": 6400, "y": 350, "type": "turret"},
            # Area 6 - Final gauntlet
            {"x": 7200, "y": 500, "type": "flying", "patrol": 250},
            {"x": 7500, "y": 450, "type": "flying", "patrol": 250},
            {"x": 7800, "y": 400, "type": "flying", "patrol": 250},
            {"x": 8100, "y": 590, "type": "ground", "patrol": 200},
        ],
        "hazards": [
            # Spikes
            *[{"x": 1200 + i * 64, "y": 640, "type": "spike"} for i in range(5)],
            *[{"x": 4000 + i * 64, "y": 640, "type": "spike"} for i in range(6)],
            # Falling blocks
            {"x": 2300, "y": 100, "type": "falling_block"},
            {"x": 2500, "y": 100, "type": "falling_block"},
            {"x": 3600, "y": 250, "type": "falling_block"},
            # Moving platforms
            {"x": 3000, "y": 300, "type": "moving_platform", "width": 96},
            {"x": 3400, "y": 350, "type": "moving_platform", "width": 96},
            {"x": 5600, "y": 500, "type": "moving_platform", "width": 128},
            {"x": 7400, "y": 450, "type": "moving_platform", "width": 96},
        ],
        "coins": [
            # Main path coins
            *[{"x": 350 + i * 100, "y": 550 - i * 30, "value": 1} for i in range(12)],
            *[
                {"x": 1650 + (i % 2) * 150, "y": 550 - i * 40, "value": 1}
                for i in range(15)
            ],
            *[
                {"x": 2850 + i * 200, "y": 150 + (i % 3) * 60, "value": 2}
                for i in range(15)
            ],
            # High value coins
            {"x": 2250, "y": 100, "value": 20},
            {"x": 5200, "y": 350, "value": 15},
            {"x": 6400, "y": 400, "value": 15},
            # Secret coins underground
            *[{"x": 5000 + i * 150, "y": 450, "value": 3} for i in range(10)],
        ],
        "powerups": [
            {"x": 1700, "y": 350, "type": "health"},
            {"x": 3500, "y": 250, "type": "speed"},
            {"x": 5300, "y": 590, "type": "health"},
            {"x": 6800, "y": 500, "type": "invincible"},
            {"x": 8100, "y": 210, "type": "health"},
        ],
        "keys": [],
        "portals": [{"x": 8350, "y": 170, "dest": 3}],
    }
    levels.append(level_2)

    # ============================================================
    # LEVEL 3: "THE ASCENT" (20 minutes, 9000px) - see _build_level_3
    # ============================================================

    levels.append(_build_level_3())

    # ============================================================
    # LEVEL 4: "DEEP DIVE" (20 minutes, 9500px)
    # ============================================================

    level_4 = {
        "width": 9500,
        "height": 720,
        "theme": "SCIFI",
        "spawn_x": 100,
        "spawn_y": 500,
        "time_limit": "medium",
        "tiles": [
            # === AREA 1: SURFACE (0-1500) ===
            *[{"x": i * TILE_SIZE, "y": 640, "solid": True} for i in range(50)],
            *[{"x": 400 + i * TILE_SIZE, "y": 550, "solid": True} for i in range(8)],
            *[{"x": 800 + i * TILE_SIZE, "y": 480, "solid": True} for i in range(8)],
            # === AREA 2: DESCENT (1500-2800) ===
            # Spiral descent
            *[
                {"x": 1500 + i * 100, "y": 640 - i * 40, "solid": True}
                for i in range(14)
            ],
            *[
                {"x": 1532 + i * 100, "y": 640 - i * 40, "solid": True}
                for i in range(14)
            ],
            # === AREA 3: CAVE SYSTEMS (2800-5000) ===
            # Complex cave floor
            *[{"x": 2800 + i * TILE_SIZE, "y": 640, "solid": True} for i in range(70)],
            # Cave ceiling (varies height)
            *[
                {"x": 2800 + i * 64, "y": 350 - (i % 5) * 30, "solid": True}
                for i in range(35)
            ],
            # Stalactites (hang from ceiling)
            *[{"x": 3000 + i * 200, "y": 350, "solid": True} for i in range(10)],
            *[{"x": 3000 + i * 200, "y": 382, "solid": True} for i in range(10)],
            # Platforms in caves
            *[
                {"x": 3200 + (i % 6) * 150, "y": 550 - (i // 6) * 60, "solid": True}
                for i in range(24)
            ],
            *[
                {"x": 3232 + (i % 6) * 150, "y": 550 - (i // 6) * 60, "solid": True}
                for i in range(24)
            ],
            # === AREA 4: UNDERGROUND LAKE (5000-6500) ===
            # Water level simulation (lower platforms)
            *[{"x": 5000 + i * TILE_SIZE, "y": 680, "solid": True} for i in range(50)],
            # Islands in lake
            *[{"x": 5200, "y": 600, "solid": True}],
            *[{"x": 5232, "y": 600, "solid": True}],
            *[{"x": 5500, "y": 580, "solid": True}],
            *[{"x": 5532, "y": 580, "solid": True}],
            *[{"x": 5800, "y": 600, "solid": True}],
            *[{"x": 5832, "y": 600, "solid": True}],
            *[{"x": 6100, "y": 580, "solid": True}],
            *[{"x": 6132, "y": 580, "solid": True}],
            # === AREA 5: CRYSTAL CAVERNS (6500-8000) ===
            *[{"x": 6500 + i * TILE_SIZE, "y": 640, "solid": True} for i in range(50)],
            # Crystal formations (platforms at various heights)
            *[
                {"x": 6700 + i * 180, "y": 550 - i * 25, "solid": True}
                for i in range(15)
            ],
            *[
                {"x": 6732 + i * 180, "y": 550 - i * 25, "solid": True}
                for i in range(15)
            ],
            # Tall crystal pillars
            *[{"x": 7200, "y": 640 - i * TILE_SIZE, "solid": True} for i in range(8)],
            *[{"x": 7500, "y": 640 - i * TILE_SIZE, "solid": True} for i in range(10)],
            # === AREA 6: ASCENT & EXIT (8000-9500) ===
            # Climb back to surface
            *[
                {"x": 8000 + i * 80, "y": 640 - i * 35, "solid": True}
                for i in range(16)
            ],
            *[
                {"x": 8032 + i * 80, "y": 640 - i * 35, "solid": True}
                for i in range(16)
            ],
            # Surface exit
            *[{"x": 9200 + i * TILE_SIZE, "y": 100, "solid": True} for i in range(10)],
        ],
        "enemies": [
            # Area 1 - Surface
            {"x": 500, "y": 590, "type": "ground", "patrol": 150},
            {"x": 900, "y": 430, "type": "ground", "patrol": 150},
            # Area 2 - Descent
            {"x": 1700, "y": 550, "type": "flying", "patrol": 200},
            {"x": 2000, "y": 400, "type": "flying", "patrol": 200},
            # Area 3 - Cave systems
            {"x": 3000, "y": 590, "type": "ground", "patrol": 180},
            {"x": 3300, "y": 590, "type": "ground", "patrol": 180},
            {"x": 3600, "y": 590, "type": "ground", "patrol": 180},
            {"x": 3900, "y": 590, "type": "ground", "patrol": 180},
            {"x": 4200, "y": 590, "type": "ground", "patrol": 180},
            {"x": 3500, "y": 450, "type": "flying", "patrol": 250},
            {"x": 4000, "y": 450, "type": "flying", "patrol": 250},
            {"x": 4500, "y": 450, "type": "flying", "patrol": 250},
            {"x": 3800, "y": 500, "type": "turret"},
            {"x": 4300, "y": 500, "type": "turret"},
            # Area 4 - Lake
            {"x": 5300, "y": 550, "type": "flying", "patrol": 200},
            {"x": 5600, "y": 530, "type": "flying", "patrol": 200},
            {"x": 5900, "y": 550, "type": "flying", "patrol": 200},
            {"x": 6200, "y": 530, "type": "flying", "patrol": 200},
            # Area 5 - Crystal caverns
            {"x": 6800, "y": 590, "type": "ground", "patrol": 200},
            {"x": 7100, "y": 500, "type": "ground", "patrol": 150},
            {"x": 7400, "y": 400, "type": "flying", "patrol": 250},
            {"x": 7700, "y": 350, "type": "flying", "patrol": 250},
            # Area 6 - Ascent
            {"x": 8200, "y": 550, "type": "flying", "patrol": 250},
            {"x": 8500, "y": 400, "type": "flying", "patrol": 250},
            {"x": 8800, "y": 250, "type": "flying", "patrol": 250},
        ],
        "hazards": [
            # Cave spikes
            *[{"x": 2900 + i * 64, "y": 640, "type": "spike"} for i in range(8)],
            *[{"x": 4600 + i * 64, "y": 640, "type": "spike"} for i in range(6)],
            # Falling stalactites
            {"x": 3200, "y": 350, "type": "falling_block"},
            {"x": 3600, "y": 350, "type": "falling_block"},
            {"x": 4000, "y": 350, "type": "falling_block"},
            # Moving platforms over water
            {"x": 5350, "y": 620, "type": "moving_platform", "width": 96},
            {"x": 5650, "y": 620, "type": "moving_platform", "width": 96},
            {"x": 5950, "y": 620, "type": "moving_platform", "width": 96},
            # Crystal area hazards
            {"x": 7000, "y": 550, "type": "moving_platform", "width": 128},
            {"x": 7600, "y": 450, "type": "moving_platform", "width": 128},
        ],
        "coins": [
            # Path coins
            *[{"x": 400 + i * 80, "y": 510, "value": 1} for i in range(60)],
            # Cave coins
            *[
                {"x": 3250 + (i % 6) * 150, "y": 500 - (i // 6) * 60, "value": 2}
                for i in range(24)
            ],
            # Lake coins (risky)
            *[{"x": 5250 + i * 300, "y": 550, "value": 5} for i in range(4)],
            # Crystal coins
            *[{"x": 6750 + i * 180, "y": 500 - i * 25, "value": 2} for i in range(15)],
            # High value secrets
            {"x": 3500, "y": 380, "value": 20},
            {"x": 7500, "y": 150, "value": 25},
        ],
        "powerups": [
            {"x": 1800, "y": 450, "type": "health"},
            {"x": 4000, "y": 450, "type": "speed"},
            {"x": 6000, "y": 530, "type": "invincible"},
            {"x": 7500, "y": 300, "type": "health"},
            {"x": 9000, "y": 200, "type": "health"},
        ],
        "keys": [],
        "portals": [{"x": 9350, "y": 10, "dest": 5}],
    }
    levels.append(level_4)

    # ============================================================
    # LEVEL 5: "CONVERGENCE" (20 minutes, 10000px)
    # ============================================================

    level_5 = {
        "width": 10000,
        "height": 720,
        "theme": "SCIFI",
        "spawn_x": 100,
        "spawn_y": 500,
        "time_limit": "medium",
        "tiles": [
            # === AREA 1: GAUNTLET START (0-2000) ===
            *[{"x": i * TILE_SIZE, "y": 640, "solid": True} for i in range(65)],
            # Quick platforming warmup
            *[
                {"x": 300 + i * 100, "y": 550 - (i % 3) * 50, "solid": True}
                for i in range(15)
            ],
            *[
                {"x": 332 + i * 100, "y": 550 - (i % 3) * 50, "solid": True}
                for i in range(15)
            ],
            # === AREA 2: WALL JUMP TOWER (2000-3200) ===
            # Tall narrow tower requiring perfect wall jumps
            *[{"x": 2100, "y": 640 - i * TILE_SIZE, "solid": True} for i in range(20)],
            *[{"x": 2300, "y": 640 - i * TILE_SIZE, "solid": True} for i in range(20)],
            # Alternating mini platforms
            *[
                {"x": 2132 + (i % 2) * 136, "y": 610 - i * 32, "solid": True}
                for i in range(20)
            ],
            # Tower top
            *[{"x": 2500 + i * TILE_SIZE, "y": 100, "solid": True} for i in range(20)],
            # === AREA 3: PRECISION PLATFORMING (3200-4800) ===
            # Narrow platforms with big gaps
            *[
                {"x": 3300 + i * 180, "y": 150 + (i % 5) * 60, "solid": True}
                for i in range(20)
            ],
            *[
                {"x": 3332 + i * 180, "y": 150 + (i % 5) * 60, "solid": True}
                for i in range(20)
            ],
            # Midway steps where the sawtooth resets to the top
            # (a 240px climb is higher than a double jump)
            *[
                {"x": 3300 + i * 180 - 90 + dx, "y": 270, "solid": True}
                for i in (5, 10, 15)
                for dx in (0, TILE_SIZE)
            ],
            # Ground section
            *[{"x": 4500 + i * TILE_SIZE, "y": 640, "solid": True} for i in range(10)],
            # === AREA 4: COMBAT MARATHON (4800-6500) ===
            *[{"x": 4800 + i * TILE_SIZE, "y": 640, "solid": True} for i in range(55)],
            # Multi-level combat arena
            *[{"x": 5000, "y": 550, "solid": True}],
            *[{"x": 5032, "y": 550, "solid": True}],
            *[{"x": 5200, "y": 500, "solid": True}],
            *[{"x": 5232, "y": 500, "solid": True}],
            *[{"x": 5400, "y": 450, "solid": True}],
            *[{"x": 5432, "y": 450, "solid": True}],
            *[{"x": 5600, "y": 500, "solid": True}],
            *[{"x": 5632, "y": 500, "solid": True}],
            *[{"x": 5800, "y": 550, "solid": True}],
            *[{"x": 5832, "y": 550, "solid": True}],
            *[{"x": 6000, "y": 500, "solid": True}],
            *[{"x": 6032, "y": 500, "solid": True}],
            *[{"x": 6200, "y": 450, "solid": True}],
            *[{"x": 6232, "y": 450, "solid": True}],
            # === AREA 5: HAZARD GAUNTLET (6500-8000) ===
            *[{"x": 6500 + i * TILE_SIZE, "y": 640, "solid": True} for i in range(50)],
            # Platform path through hazards
            *[
                {"x": 6600 + i * 120, "y": 550 - (i % 4) * 50, "solid": True}
                for i in range(25)
            ],
            *[
                {"x": 6632 + i * 120, "y": 550 - (i % 4) * 50, "solid": True}
                for i in range(25)
            ],
            # === AREA 6: ESCAPE SEQUENCE (8000-9500) ===
            # Fast-paced platforming to boss door
            *[{"x": 8000 + i * TILE_SIZE, "y": 640, "solid": True} for i in range(50)],
            # Rising platforms
            *[
                {"x": 8100 + i * 90, "y": 600 - i * 30, "solid": True}
                for i in range(15)
            ],
            *[
                {"x": 8132 + i * 90, "y": 600 - i * 30, "solid": True}
                for i in range(15)
            ],
            # === AREA 7: BOSS DOOR (9500-10000) ===
            # Safe area before boss
            *[{"x": 9500 + i * TILE_SIZE, "y": 640, "solid": True} for i in range(16)],
            *[{"x": 9500 + i * TILE_SIZE, "y": 200, "solid": True} for i in range(16)],
            # Ascent to boss door
            *[{"x": 9600, "y": 640 - i * TILE_SIZE, "solid": True} for i in range(14)],
            *[{"x": 9700, "y": 640 - i * TILE_SIZE, "solid": True} for i in range(14)],
        ],
        "enemies": [
            # Area 1 - Warmup
            {"x": 500, "y": 500, "type": "ground", "patrol": 150},
            {"x": 800, "y": 450, "type": "ground", "patrol": 150},
            {"x": 1100, "y": 400, "type": "flying", "patrol": 200},
            {"x": 1500, "y": 590, "type": "ground", "patrol": 180},
            # Area 2 - Tower
            {"x": 2150, "y": 500, "type": "flying", "patrol": 150},
            {"x": 2200, "y": 350, "type": "flying", "patrol": 150},
            {"x": 2250, "y": 200, "type": "flying", "patrol": 150},
            # Area 3 - Precision
            {"x": 3500, "y": 200, "type": "flying", "patrol": 250},
            {"x": 3900, "y": 250, "type": "flying", "patrol": 250},
            {"x": 4300, "y": 300, "type": "flying", "patrol": 250},
            # Area 4 - Combat marathon (MANY enemies)
            {"x": 5050, "y": 500, "type": "ground", "patrol": 100},
            {"x": 5250, "y": 450, "type": "ground", "patrol": 100},
            {"x": 5450, "y": 400, "type": "ground", "patrol": 100},
            {"x": 5650, "y": 450, "type": "ground", "patrol": 100},
            {"x": 5850, "y": 500, "type": "ground", "patrol": 100},
            {"x": 6050, "y": 450, "type": "ground", "patrol": 100},
            {"x": 6250, "y": 400, "type": "ground", "patrol": 100},
            {"x": 5300, "y": 400, "type": "flying", "patrol": 250},
            {"x": 5700, "y": 400, "type": "flying", "patrol": 250},
            {"x": 6100, "y": 400, "type": "flying", "patrol": 250},
            {"x": 5100, "y": 450, "type": "turret"},
            {"x": 5900, "y": 450, "type": "turret"},
            {"x": 6300, "y": 450, "type": "turret"},
            # Area 5 - Hazard gauntlet
            {"x": 6700, "y": 500, "type": "flying", "patrol": 250},
            {"x": 7000, "y": 450, "type": "flying", "patrol": 250},
            {"x": 7300, "y": 400, "type": "flying", "patrol": 250},
            {"x": 7600, "y": 450, "type": "flying", "patrol": 250},
            # Area 6 - Escape
            {"x": 8300, "y": 550, "type": "flying", "patrol": 250},
            {"x": 8600, "y": 450, "type": "flying", "patrol": 250},
            {"x": 8900, "y": 350, "type": "flying", "patrol": 250},
        ],
        "hazards": [
            # Tower spikes
            *[{"x": 2000 + i * 32, "y": 640, "type": "spike"} for i in range(5)],
            # Precision section falling blocks
            {"x": 3400, "y": 150, "type": "falling_block"},
            {"x": 3700, "y": 200, "type": "falling_block"},
            {"x": 4000, "y": 250, "type": "falling_block"},
            {"x": 4300, "y": 300, "type": "falling_block"},
            # Combat arena moving platforms
            {"x": 5500, "y": 550, "type": "moving_platform", "width": 96},
            {"x": 6100, "y": 550, "type": "moving_platform", "width": 96},
            # MANY spikes in hazard gauntlet
            *[{"x": 6600 + i * 64, "y": 640, "type": "spike"} for i in range(22)],
            # Moving platforms through spikes
            {"x": 6800, "y": 500, "type": "moving_platform", "width": 96},
            {"x": 7200, "y": 450, "type": "moving_platform", "width": 96},
            {"x": 7600, "y": 500, "type": "moving_platform", "width": 96},
            # Escape section hazards
            {"x": 8400, "y": 500, "type": "moving_platform", "width": 128},
            {"x": 8800, "y": 400, "type": "moving_platform", "width": 128},
        ],
        "coins": [
            # Generous coins on main path
            *[
                {"x": 350 + i * 100, "y": 500 - (i % 3) * 50, "value": 1}
                for i in range(80)
            ],
            # Tower coins
            *[
                {"x": 2170 + (i % 2) * 100, "y": 580 - i * 32, "value": 2}
                for i in range(20)
            ],
            # Precision coins (high risk/reward)
            *[
                {"x": 3350 + i * 180, "y": 100 + (i % 5) * 60, "value": 3}
                for i in range(20)
            ],
            # Combat coins
            *[{"x": 5050 + i * 150, "y": 450, "value": 2} for i in range(20)],
            # Secret high value
            {"x": 2600, "y": 50, "value": 30},
            {"x": 7500, "y": 350, "value": 25},
        ],
        "powerups": [
            {"x": 1800, "y": 590, "type": "health"},
            {"x": 2700, "y": 50, "type": "double_jump"},
            {"x": 4700, "y": 590, "type": "health"},
            {"x": 6300, "y": 400, "type": "invincible"},
            {"x": 8000, "y": 590, "type": "speed"},
            {"x": 9200, "y": 150, "type": "health"},
            {"x": 9650, "y": 590, "type": "health"},
        ],
        "keys": [],
        "portals": [{"x": 9850, "y": 110, "dest": 6, "color": [255, 0, 0]}],
    }
    levels.append(level_5)

    # ============================================================
    # LEVEL 6: "GUARDIAN'S LAIR" - BOSS FIGHT
    # ============================================================

    # boss_arena = {
    #     "width": 1280,
    #     "height": 720,
    #     "theme": "SCIFI",
    #     "spawn_x": 200,
    #     "spawn_y": 580,
    #     "time_limit": "none",
    #     "tiles": [
    #         # Floor
    #         *[{"x": i * TILE_SIZE, "y": 640, "solid": True} for i in range(40)],
    #         # Side walls (prevent escape)
    #         *[{"x": 0, "y": i * TILE_SIZE, "solid": True} for i in range(22)],
    #         *[{"x": 1248, "y": i * TILE_SIZE, "solid": True} for i in range(22)],
    #         # Ceiling
    #         *[{"x": i * TILE_SIZE, "y": 0, "solid": True} for i in range(40)],
    #         # Small platforms for player mobility
    #         {"x": 200, "y": 550, "solid": True},
    #         {"x": 232, "y": 550, "solid": True},
    #         {"x": 400, "y": 500, "solid": True},
    #         {"x": 432, "y": 500, "solid": True},
    #         {"x": 600, "y": 450, "solid": True},
    #         {"x": 632, "y": 450, "solid": True},
    #         {"x": 800, "y": 500, "solid": True},
    #         {"x": 832, "y": 500, "solid": True},
    #         {"x": 1000, "y": 550, "solid": True},
    #         {"x": 1032, "y": 550, "solid": True},
    #     ],
    #     "enemies": [],
    #     "hazards": [
    #         # Corner spikes (activate in phase 3)
    #         {"x": 64, "y": 640, "type": "spike"},
    #         {"x": 1184, "y": 640, "type": "spike"},
    #     ],
    #     "coins": [],
    #     "powerups": [
    #         # Health pickups for long fight
    #         {"x": 200, "y": 510, "type": "health"},
    #         {"x": 1000, "y": 510, "type": "health"},
    #     ],
    #     "keys": [],
    #     "portals": [],
    # }
    
    boss_arena = {
        "width": 1280,  # Single screen
        "height": 720,
        "theme": "SCIFI",
        "spawn_x": 200,
        "spawn_y": 580,
        "time_limit": "none",
        "tiles": [
            # FLOOR - Main ground level
            *[{"x": i * TILE_SIZE, "y": 640, "solid": True} for i in range(40)],
            
            # SIDE WALLS (prevent escape)
            *[{"x": 0, "y": i * TILE_SIZE, "solid": True} for i in range(20)],
            *[{"x": 1248, "y": i * TILE_SIZE, "solid": True} for i in range(20)],
            
            # BOTTOM TIER PLATFORMS (Safe zones - wide and low)
            {"x": 100, "y": 600, "solid": True},
            {"x": 132, "y": 600, "solid": True},
            {"x": 164, "y": 600, "solid": True},
            {"x": 196, "y": 600, "solid": True},
            {"x": 228, "y": 600, "solid": True},  # Left safe platform (5 tiles wide)
            
            {"x": 1020, "y": 600, "solid": True},
            {"x": 1052, "y": 600, "solid": True},
            {"x": 1084, "y": 600, "solid": True},
            {"x": 1116, "y": 600, "solid": True},
            {"x": 1148, "y": 600, "solid": True},  # Right safe platform (5 tiles wide)
            
            # MID TIER PLATFORMS (Tactical positions)
            # Left-mid platform
            {"x": 300, "y": 500, "solid": True},
            {"x": 332, "y": 500, "solid": True},
            {"x": 364, "y": 500, "solid": True},
            {"x": 396, "y": 500, "solid": True},  # 4 tiles wide
            
            # Center platform (key position)
            {"x": 608, "y": 450, "solid": True},
            {"x": 640, "y": 450, "solid": True},
            {"x": 672, "y": 450, "solid": True},  # 3 tiles wide at center
            
            # Right-mid platform
            {"x": 884, "y": 500, "solid": True},
            {"x": 916, "y": 500, "solid": True},
            {"x": 948, "y": 500, "solid": True},
            {"x": 980, "y": 500, "solid": True},  # 4 tiles wide
            
            # UPPER TIER PLATFORMS (High risk, better angles)
            # Left upper
            {"x": 448, "y": 320, "solid": True},
            {"x": 480, "y": 320, "solid": True},
            {"x": 512, "y": 320, "solid": True},  # 3 tiles wide
            
            # Right upper
            {"x": 768, "y": 320, "solid": True},
            {"x": 800, "y": 320, "solid": True},
            {"x": 832, "y": 320, "solid": True},  # 3 tiles wide
            
            # TOP CENTER PLATFORM (Highest risk/reward)
            {"x": 608, "y": 200, "solid": True},
            {"x": 640, "y": 200, "solid": True},
            {"x": 672, "y": 200, "solid": True},  # 3 tiles at top center
        ],
        "enemies": [],  # Boss spawns automatically
        "hazards": [
            # Corner spikes (slight danger, not too punishing)
            {"x": 32, "y": 640, "type": "spike"},
            {"x": 1216, "y": 640, "type": "spike"},
        ],
        "coins": [],  # No coins during boss fight
        "powerups": [
            # Health pickups on safe platforms (regenerate over time in actual game)
            {"x": 164, "y": 560, "type": "health"},   # Left safe platform
            {"x": 1084, "y": 560, "type": "health"},  # Right safe platform
        ],
        "keys": [],
        "portals": [],  # Spawns on boss defeat
    }
    
    levels.append(boss_arena)

    return levels


# ============================================================
# LEVEL 3 BUILDER
# ============================================================


def _row(x, y, count):
    """Horizontal run of solid tiles starting at (x, y)"""
    return [{"x": x + i * TILE_SIZE, "y": y, "solid": True} for i in range(count)]


def _col(x, y_top, y_bottom):
    """Vertical run of solid tiles from y_top down to y_bottom (inclusive)"""
    return [{"x": x, "y": y, "solid": True} for y in range(y_top, y_bottom + 1, TILE_SIZE)]


def _build_level_3():
    """
    LEVEL 3: "THE ASCENT" - vertical emphasis.

    Rebuilt so every section connects (checked with tests/level_checker.py):
      1. Courtyard (0-1800): stepped platforms over solid ground
      2. First Tower (1800-3200): enter at the bottom, zigzag ledges up,
         exit at the top onto a high walkway
      3. Bridge (3200-4500): suspended planks and a moving platform over a pit
      4. Second Tower (4500-6000): stairs down, then a narrower zigzag climb
      5. Spire (6000-7500): wall-jump up a single column, then summit hops
      6. Descent & Finale (7500-9000): staircase down to the exit dais
    """
    ground = 640
    tiles = []
    enemies = []
    hazards = []
    coins = []
    powerups = []

    # === AREA 1: COURTYARD (0-1800) ===
    tiles += _row(0, ground, 57)
    for x, y in [(300, 544), (560, 448), (820, 352), (1100, 448), (1360, 544)]:
        tiles += _row(x, y, 4)
        coins += [{"x": x + 16 + i * 32, "y": y - 30, "value": 1} for i in range(3)]
    coins += [{"x": 150 + i * 100, "y": 600, "value": 1} for i in range(17)]
    enemies += [
        {"x": 500, "y": ground - 32, "type": "ground", "patrol": 150},
        {"x": 1200, "y": ground - 32, "type": "ground", "patrol": 150},
        {"x": 850, "y": 320, "type": "ground", "patrol": 40},
        {"x": 1000, "y": 420, "type": "flying", "patrol": 200},
    ]
    powerups.append({"x": 1500, "y": 590, "type": "health"})

    # === AREA 2: FIRST TOWER (1800-3200) ===
    tiles += _row(1824, ground, 12)           # tower floor
    tiles += _col(1888, 64, 512)               # left wall, doorway at the bottom
    tiles += _col(2208, 192, 608)              # right wall, open at the top
    ledges = [(1920, 560), (2112, 480), (1920, 400), (2112, 320), (1920, 240)]
    for x, y in ledges:
        tiles += _row(x, y, 3)
        coins.append({"x": x + 40, "y": y - 30, "value": 2})
    tiles += _row(2112, 160, 34)               # exit ledge + high walkway to 3200
    coins += [{"x": 2350 + i * 100, "y": 120, "value": 1} for i in range(8)]
    enemies += [
        {"x": 2060, "y": 420, "type": "flying", "patrol": 60},
        {"x": 2500, "y": 128, "type": "ground", "patrol": 150},
        {"x": 2700, "y": 128, "type": "turret"},
        {"x": 2950, "y": 128, "type": "ground", "patrol": 150},
    ]
    hazards += [{"x": 1760 + i * 32, "y": ground, "type": "spike"} for i in range(2)]

    # === AREA 3: BRIDGE (3200-4500) ===
    for x in (3310, 3520, 4040, 4250):
        tiles += _row(x, 160, 3)
        coins.append({"x": x + 40, "y": 120, "value": 3})
    hazards.append({"x": 3780, "y": 160, "type": "moving_platform", "width": 96})
    tiles += _row(4450, 160, 4)                # landing
    hazards += [{"x": x, "y": 40, "type": "falling_block"} for x in (3340, 3550, 4280)]
    enemies += [
        {"x": 3450, "y": 90, "type": "flying", "patrol": 150},
        {"x": 3900, "y": 70, "type": "flying", "patrol": 200},
        {"x": 4300, "y": 90, "type": "flying", "patrol": 150},
    ]
    powerups.append({"x": 4500, "y": 120, "type": "health"})

    # === AREA 4: SECOND TOWER (4500-6000) ===
    for x, y in [(4620, 260), (4720, 360), (4820, 460), (4920, 560)]:
        tiles += _row(x, y, 2)
    tiles += _row(4600, ground, 31)            # ground, also the tower floor
    tiles += _col(5200, 96, 512)               # left wall, doorway at the bottom
    tiles += _col(5520, 144, 608)              # right wall, open at the top
    ledges = [(5232, 552), (5456, 464), (5232, 376), (5456, 288), (5232, 200)]
    for x, y in ledges:
        tiles += _row(x, y, 2)
        coins.append({"x": x + 24, "y": y - 30, "value": 2})
    tiles += _row(5456, 112, 17)               # exit ledge + walkway to 6000
    coins += [{"x": 5650 + i * 80, "y": 80, "value": 1} for i in range(4)]
    enemies += [
        {"x": 4800, "y": ground - 32, "type": "ground", "patrol": 150},
        {"x": 5050, "y": ground - 32, "type": "ground", "patrol": 100},
        {"x": 5380, "y": 380, "type": "flying", "patrol": 60},
        {"x": 5700, "y": 80, "type": "ground", "patrol": 100},
        {"x": 5900, "y": 80, "type": "turret"},
    ]
    powerups.append({"x": 5600, "y": 70, "type": "double_jump"})

    # === AREA 5: SPIRE (6000-7500) ===
    tiles += _row(6000, ground, 10)            # base of the spire
    tiles += _col(6320, 96, 608)               # the spire: wall-jump up its face
    for y in (480, 352, 224):                  # small rest ledges on the spire
        tiles.append({"x": 6288, "y": y, "solid": True})
        coins.append({"x": 6292, "y": y - 30, "value": 2})
    summit = [(6450, 128, 3), (6650, 96, 3), (6860, 128, 3), (7060, 96, 3), (7260, 128, 4)]
    for x, y, n in summit:
        tiles += _row(x, y, n)
        coins.append({"x": x + 40, "y": y - 30, "value": 2})
    coins.append({"x": 6700, "y": 40, "value": 25})  # summit treasure
    enemies += [
        {"x": 6150, "y": ground - 32, "type": "ground", "patrol": 100},
        {"x": 6500, "y": 260, "type": "flying", "patrol": 150},
        {"x": 6900, "y": 220, "type": "flying", "patrol": 150},
        {"x": 7080, "y": 64, "type": "turret"},
    ]
    powerups.append({"x": 6100, "y": 590, "type": "speed"})

    # === AREA 6: DESCENT & FINALE (7500-9000) ===
    for i in range(7):
        x, y = 7460 + i * 95, 176 + i * 60
        tiles += _row(x, y, 2)
        coins.append({"x": x + 24, "y": y - 30, "value": 1})
    tiles += _row(8100, ground, 28)            # finale floor
    tiles += _row(8740, 544, 8)                # exit dais
    hazards += [{"x": 8330 + i * 32, "y": ground, "type": "spike"} for i in range(2)]
    coins += [{"x": 8150 + i * 80, "y": 600, "value": 1} for i in range(7)]
    enemies += [
        {"x": 7700, "y": 250, "type": "flying", "patrol": 200},
        {"x": 8000, "y": 380, "type": "flying", "patrol": 200},
        {"x": 8250, "y": ground - 32, "type": "ground", "patrol": 60},
        {"x": 8500, "y": ground - 32, "type": "ground", "patrol": 120},
        {"x": 8650, "y": ground - 32, "type": "turret"},
        {"x": 8850, "y": 512, "type": "ground", "patrol": 60},
    ]
    powerups.append({"x": 8150, "y": 590, "type": "health"})

    return {
        "width": 9000,
        "height": 720,
        "theme": "SCIFI",
        "spawn_x": 100,
        "spawn_y": 500,
        "time_limit": "medium",
        "tiles": tiles,
        "enemies": enemies,
        "hazards": hazards,
        "coins": coins,
        "powerups": powerups,
        "keys": [],
        "portals": [{"x": 8850, "y": 480, "dest": 4}],
    }
