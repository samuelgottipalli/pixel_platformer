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
        'width': 8500,
        'height': 720,
        'theme': 'SCIFI',
        'spawn_x': 100,
        'spawn_y': 500,
        'time_limit': 'long',
        'tiles': [
            # === AREA 1: GENTLE START (0-1500) ===
            *[{'x': i * TILE_SIZE, 'y': 640, 'solid': True} for i in range(50)],
            # Ascending platforms
            *[{'x': 300 + i * 100, 'y': 600 - i * 30, 'solid': True} for i in range(12)],
            *[{'x': 332 + i * 100, 'y': 600 - i * 30, 'solid': True} for i in range(12)],
            
            # === AREA 2: TOWER CLIMB (1500-2800) ===
            # Main tower structure
            *[{'x': 1500, 'y': 640 - i * TILE_SIZE, 'solid': True} for i in range(18)],
            *[{'x': 1532, 'y': 640 - i * TILE_SIZE, 'solid': True} for i in range(18)],
            # Side platforms for zigzag climb
            *[{'x': 1600 + (i % 2) * 150, 'y': 600 - i * 40, 'solid': True} for i in range(15)],
            *[{'x': 1632 + (i % 2) * 150, 'y': 600 - i * 40, 'solid': True} for i in range(15)],
            # Top platform
            *[{'x': 2200 + i * TILE_SIZE, 'y': 150, 'solid': True} for i in range(20)],
            
            # === AREA 3: HIGH PLATFORMS (2800-4200) ===
            # Floating island section
            *[{'x': 2800 + i * 200, 'y': 200 + (i % 3) * 60, 'solid': True} for i in range(15)],
            *[{'x': 2832 + i * 200, 'y': 200 + (i % 3) * 60, 'solid': True} for i in range(15)],
            # Drop platforms
            *[{'x': 3500, 'y': 200 + i * 80, 'solid': True} for i in range(6)],
            *[{'x': 3532, 'y': 200 + i * 80, 'solid': True} for i in range(6)],
            # Ground return
            *[{'x': 3800 + i * TILE_SIZE, 'y': 640, 'solid': True} for i in range(30)],
            
            # === AREA 4: UNDERGROUND PASSAGE (4200-5800) ===
            # Descent into underground
            *[{'x': 4200 + i * 80, 'y': 640 - i * 20, 'solid': True} for i in range(8)],
            *[{'x': 4232 + i * 80, 'y': 640 - i * 20, 'solid': True} for i in range(8)],
            # Underground floor and ceiling
            *[{'x': 4800 + i * TILE_SIZE, 'y': 640, 'solid': True} for i in range(35)],
            *[{'x': 4800 + i * TILE_SIZE, 'y': 400, 'solid': True} for i in range(35)],
            # Pillars in underground
            *[{'x': 5000, 'y': 400 + i * TILE_SIZE, 'solid': True} for i in range(4)],
            *[{'x': 5200, 'y': 400 + i * TILE_SIZE, 'solid': True} for i in range(4)],
            *[{'x': 5400, 'y': 400 + i * TILE_SIZE, 'solid': True} for i in range(4)],
            
            # === AREA 5: COMBAT ARENA (5800-7000) ===
            *[{'x': 5800 + i * TILE_SIZE, 'y': 640, 'solid': True} for i in range(40)],
            # Multi-level combat platforms
            *[{'x': 5900, 'y': 550, 'solid': True}],
            *[{'x': 5932, 'y': 550, 'solid': True}],
            *[{'x': 6100, 'y': 500, 'solid': True}],
            *[{'x': 6132, 'y': 500, 'solid': True}],
            *[{'x': 6300, 'y': 450, 'solid': True}],
            *[{'x': 6332, 'y': 450, 'solid': True}],
            *[{'x': 6500, 'y': 500, 'solid': True}],
            *[{'x': 6532, 'y': 500, 'solid': True}],
            *[{'x': 6700, 'y': 550, 'solid': True}],
            *[{'x': 6732, 'y': 550, 'solid': True}],
            
            # === AREA 6: FINAL GAUNTLET (7000-8500) ===
            *[{'x': 7000 + i * TILE_SIZE, 'y': 640, 'solid': True} for i in range(50)],
            # Platforming challenge
            *[{'x': 7100 + i * 120, 'y': 550 - (i % 4) * 40, 'solid': True} for i in range(20)],
            *[{'x': 7132 + i * 120, 'y': 550 - (i % 4) * 40, 'solid': True} for i in range(20)],
            # Final climb to exit
            *[{'x': 8200, 'y': 640 - i * TILE_SIZE, 'solid': True} for i in range(12)],
            *[{'x': 8232, 'y': 640 - i * TILE_SIZE, 'solid': True} for i in range(12)],
            *[{'x': 8200 + i * TILE_SIZE, 'y': 260, 'solid': True} for i in range(10)],
        ],
        'enemies': [
            # Area 1 - Easy intro
            {'x': 500, 'y': 550, 'type': 'ground', 'patrol': 150},
            {'x': 800, 'y': 450, 'type': 'ground', 'patrol': 120},
            # Area 2 - Tower climb
            {'x': 1650, 'y': 550, 'type': 'flying', 'patrol': 150},
            {'x': 1700, 'y': 400, 'type': 'ground', 'patrol': 80},
            {'x': 1850, 'y': 350, 'type': 'ground', 'patrol': 80},
            {'x': 2000, 'y': 250, 'type': 'flying', 'patrol': 200},
            # Area 3 - High platforms
            {'x': 2900, 'y': 200, 'type': 'flying', 'patrol': 250},
            {'x': 3200, 'y': 250, 'type': 'flying', 'patrol': 200},
            {'x': 3500, 'y': 300, 'type': 'ground', 'patrol': 100},
            # Area 4 - Underground
            {'x': 5000, 'y': 590, 'type': 'ground', 'patrol': 180},
            {'x': 5200, 'y': 590, 'type': 'ground', 'patrol': 180},
            {'x': 5400, 'y': 590, 'type': 'ground', 'patrol': 180},
            {'x': 5100, 'y': 500, 'type': 'flying', 'patrol': 200},
            {'x': 5300, 'y': 500, 'type': 'flying', 'patrol': 200},
            # Area 5 - Combat arena
            {'x': 5950, 'y': 500, 'type': 'ground', 'patrol': 100},
            {'x': 6150, 'y': 450, 'type': 'ground', 'patrol': 100},
            {'x': 6350, 'y': 400, 'type': 'flying', 'patrol': 150},
            {'x': 6550, 'y': 450, 'type': 'ground', 'patrol': 100},
            {'x': 6750, 'y': 500, 'type': 'ground', 'patrol': 100},
            {'x': 6400, 'y': 350, 'type': 'turret'},
            # Area 6 - Final gauntlet
            {'x': 7200, 'y': 500, 'type': 'flying', 'patrol': 250},
            {'x': 7500, 'y': 450, 'type': 'flying', 'patrol': 250},
            {'x': 7800, 'y': 400, 'type': 'flying', 'patrol': 250},
            {'x': 8100, 'y': 590, 'type': 'ground', 'patrol': 200},
        ],
        'hazards': [
            # Spikes
            *[{'x': 1200 + i * 64, 'y': 640, 'type': 'spike'} for i in range(5)],
            *[{'x': 4000 + i * 64, 'y': 640, 'type': 'spike'} for i in range(6)],
            # Falling blocks
            {'x': 2300, 'y': 100, 'type': 'falling_block'},
            {'x': 2500, 'y': 100, 'type': 'falling_block'},
            {'x': 3600, 'y': 250, 'type': 'falling_block'},
            # Moving platforms
            {'x': 3000, 'y': 300, 'type': 'moving_platform', 'width': 96},
            {'x': 3400, 'y': 350, 'type': 'moving_platform', 'width': 96},
            {'x': 5600, 'y': 500, 'type': 'moving_platform', 'width': 128},
            {'x': 7400, 'y': 450, 'type': 'moving_platform', 'width': 96},
        ],
        'coins': [
            # Main path coins
            *[{'x': 350 + i * 100, 'y': 550 - i * 30, 'value': 1} for i in range(12)],
            *[{'x': 1650 + (i % 2) * 150, 'y': 550 - i * 40, 'value': 1} for i in range(15)],
            *[{'x': 2850 + i * 200, 'y': 150 + (i % 3) * 60, 'value': 2} for i in range(15)],
            # High value coins
            {'x': 2250, 'y': 100, 'value': 20},
            {'x': 5200, 'y': 350, 'value': 15},
            {'x': 6400, 'y': 400, 'value': 15},
            # Secret coins underground
            *[{'x': 5000 + i * 150, 'y': 450, 'value': 3} for i in range(10)],
        ],
        'powerups': [
            {'x': 1700, 'y': 350, 'type': 'health'},
            {'x': 3500, 'y': 250, 'type': 'speed'},
            {'x': 5300, 'y': 590, 'type': 'health'},
            {'x': 6800, 'y': 500, 'type': 'invincible'},
            {'x': 8100, 'y': 210, 'type': 'health'},
        ],
        'keys': [],
        'portals': [
            {'x': 8350, 'y': 170, 'dest': 3}
        ]
    }
    levels.append(level_2)
    
    # ============================================================
    # LEVEL 3: "THE ASCENT" (20 minutes, 9000px)
    # ============================================================
    
    level_3 = {
        'width': 9000,
        'height': 720,
        'theme': 'SCIFI',
        'spawn_x': 100,
        'spawn_y': 500,
        'time_limit': 'medium',
        'tiles': [
            # === AREA 1: COURTYARD (0-1800) ===
            *[{'x': i * TILE_SIZE, 'y': 640, 'solid': True} for i in range(60)],
            # Multiple paths intro
            *[{'x': 300 + i * TILE_SIZE, 'y': 550, 'solid': True} for i in range(6)],
            *[{'x': 600 + i * TILE_SIZE, 'y': 450, 'solid': True} for i in range(6)],
            *[{'x': 900 + i * TILE_SIZE, 'y': 350, 'solid': True} for i in range(6)],
            # Converge
            *[{'x': 1500 + i * TILE_SIZE, 'y': 640, 'solid': True} for i in range(10)],
            
            # === AREA 2: FIRST TOWER (1800-3200) ===
            # Narrow tower with alternating platforms
            *[{'x': 1900, 'y': 640 - i * TILE_SIZE, 'solid': True} for i in range(20)],
            *[{'x': 2100, 'y': 640 - i * TILE_SIZE, 'solid': True} for i in range(20)],
            # Platforms inside tower (alternating sides)
            *[{'x': 1932 + (i % 2) * 136, 'y': 600 - i * 35, 'solid': True} for i in range(18)],
            # Top of tower
            *[{'x': 2400 + i * TILE_SIZE, 'y': 100, 'solid': True} for i in range(25)],
            
            # === AREA 3: BRIDGE SECTION (3200-4500) ===
            # Narrow suspended bridges
            *[{'x': 3200 + i * 150, 'y': 150, 'solid': True} for i in range(10)],
            *[{'x': 3232 + i * 150, 'y': 150, 'solid': True} for i in range(10)],
            
            # === AREA 4: SECOND TOWER (4500-6000) ===
            # Wider tower with more complex platforming
            *[{'x': 4600, 'y': 640 - i * TILE_SIZE, 'solid': True} for i in range(20)],
            *[{'x': 4900, 'y': 640 - i * TILE_SIZE, 'solid': True} for i in range(20)],
            # Spiral staircase effect
            *[{'x': 4632 + (i % 4) * 70, 'y': 600 - i * 30, 'solid': True} for i in range(20)],
            *[{'x': 4664 + (i % 4) * 70, 'y': 600 - i * 30, 'solid': True} for i in range(20)],
            # Tower top platform
            *[{'x': 5200 + i * TILE_SIZE, 'y': 100, 'solid': True} for i in range(25)],
            
            # === AREA 5: SPIRE SECTION (6000-7500) ===
            # Very narrow, very tall section
            *[{'x': 6100, 'y': 640 - i * TILE_SIZE, 'solid': True} for i in range(22)],
            # Tiny platforms jutting out
            *[{'x': 6132, 'y': 600 - i * 45, 'solid': True} for i in range(14)],
            *[{'x': 6100 - (i % 2) * 64, 'y': 575 - i * 45, 'solid': True} for i in range(14)],
            # Spire top
            *[{'x': 6500 + i * TILE_SIZE, 'y': 50, 'solid': True} for i in range(20)],
            
            # FIXED: Static floating platform after spire (3rd tower)
            {'x': 7300, 'y': 120, 'solid': True},
            {'x': 7332, 'y': 120, 'solid': True},
            {'x': 7364, 'y': 120, 'solid': True},  # 3 tiles wide for safety
            
            # === AREA 6: DESCENT & FINALE (7500-9000) ===
            # Controlled descent with combat
            *[{'x': 7500 + i * 100, 'y': 100 + i * 50, 'solid': True} for i in range(12)],
            *[{'x': 7532 + i * 100, 'y': 100 + i * 50, 'solid': True} for i in range(12)],
            # Ground finale
            *[{'x': 8200 + i * TILE_SIZE, 'y': 640, 'solid': True} for i in range(26)],
            # Exit platforms
            *[{'x': 8700, 'y': 640 - i * TILE_SIZE, 'solid': True} for i in range(10)],
            *[{'x': 8700 + i * TILE_SIZE, 'y': 320, 'solid': True} for i in range(10)],
        ],
        'enemies': [
            # Area 1 - Courtyard
            {'x': 400, 'y': 500, 'type': 'ground', 'patrol': 150},
            {'x': 700, 'y': 400, 'type': 'ground', 'patrol': 150},
            {'x': 1000, 'y': 300, 'type': 'ground', 'patrol': 150},
            {'x': 800, 'y': 500, 'type': 'flying', 'patrol': 200},
            # Area 2 - First tower
            {'x': 1950, 'y': 550, 'type': 'flying', 'patrol': 100},
            {'x': 2000, 'y': 400, 'type': 'ground', 'patrol': 60},
            {'x': 2050, 'y': 250, 'type': 'flying', 'patrol': 100},
            {'x': 2000, 'y': 150, 'type': 'turret'},
            # Area 3 - Bridge
            {'x': 3300, 'y': 100, 'type': 'flying', 'patrol': 250},
            {'x': 3700, 'y': 100, 'type': 'flying', 'patrol': 250},
            {'x': 4100, 'y': 100, 'type': 'flying', 'patrol': 250},
            # Area 4 - Second tower
            {'x': 4700, 'y': 550, 'type': 'ground', 'patrol': 80},
            {'x': 4750, 'y': 400, 'type': 'flying', 'patrol': 150},
            {'x': 4700, 'y': 250, 'type': 'ground', 'patrol': 80},
            {'x': 4800, 'y': 150, 'type': 'turret'},
            # Area 5 - Spire
            {'x': 6150, 'y': 500, 'type': 'flying', 'patrol': 150},
            {'x': 6150, 'y': 350, 'type': 'flying', 'patrol': 150},
            {'x': 6150, 'y': 200, 'type': 'flying', 'patrol': 150},
            # Area 6 - Descent
            {'x': 7600, 'y': 200, 'type': 'flying', 'patrol': 250},
            {'x': 7900, 'y': 350, 'type': 'flying', 'patrol': 250},
            {'x': 8300, 'y': 590, 'type': 'ground', 'patrol': 200},
            {'x': 8500, 'y': 590, 'type': 'ground', 'patrol': 200},
            {'x': 8700, 'y': 590, 'type': 'ground', 'patrol': 200},
        ],
        'hazards': [
            # Spikes at tower bases
            *[{'x': 1800 + i * 32, 'y': 640, 'type': 'spike'} for i in range(5)],
            *[{'x': 4500 + i * 32, 'y': 640, 'type': 'spike'} for i in range(5)],
            # Falling blocks on bridges
            {'x': 3300, 'y': 100, 'type': 'falling_block'},
            {'x': 3600, 'y': 100, 'type': 'falling_block'},
            {'x': 3900, 'y': 100, 'type': 'falling_block'},
            {'x': 4200, 'y': 100, 'type': 'falling_block'},
            # Moving platforms
            {'x': 2600, 'y': 200, 'type': 'moving_platform', 'width': 96},
            {'x': 5400, 'y': 200, 'type': 'moving_platform', 'width': 96},  # Reverted to original
            {'x': 7200, 'y': 180, 'type': 'moving_platform', 'width': 96},  # FIXED: Starts at x=7200 (closer to static platform), y=180 (below static platform at y=120)
        ],
        'coins': [
            # Path coins
            *[{'x': 350 + i * 80, 'y': 510, 'value': 1} for i in range(50)],
            # Tower climb rewards
            *[{'x': 1970 + (i % 2) * 100, 'y': 570 - i * 35, 'value': 2} for i in range(18)],
            # Bridge coins (risky)
            *[{'x': 3250 + i * 150, 'y': 110, 'value': 3} for i in range(10)],
            # Tower 2 coins
            *[{'x': 4650 + (i % 4) * 70, 'y': 570 - i * 30, 'value': 2} for i in range(20)],
            # High value at top
            {'x': 7000, 'y': 0, 'value': 25},
        ],
        'powerups': [
            {'x': 1200, 'y': 590, 'type': 'health'},
            {'x': 2500, 'y': 50, 'type': 'double_jump'},
            {'x': 4000, 'y': 100, 'type': 'speed'},
            {'x': 5500, 'y': 50, 'type': 'invincible'},
            {'x': 8400, 'y': 590, 'type': 'health'},
        ],
        'keys': [],
        'portals': [
            {'x': 8850, 'y': 230, 'dest': 4}
        ]
    }
    levels.append(level_3)
    
    # ============================================================
    # LEVEL 4: "DEEP DIVE" (20 minutes, 9500px)
    # ============================================================
    
    level_4 = {
        'width': 9500,
        'height': 720,
        'theme': 'SCIFI',
        'spawn_x': 100,
        'spawn_y': 500,
        'time_limit': 'medium',
        'tiles': [
            # === AREA 1: SURFACE (0-1500) ===
            *[{'x': i * TILE_SIZE, 'y': 640, 'solid': True} for i in range(50)],
            *[{'x': 400 + i * TILE_SIZE, 'y': 550, 'solid': True} for i in range(8)],
            *[{'x': 800 + i * TILE_SIZE, 'y': 480, 'solid': True} for i in range(8)],
            
            # === AREA 2: DESCENT (1500-2800) ===
            # Spiral descent
            *[{'x': 1500 + i * 100, 'y': 640 - i * 40, 'solid': True} for i in range(14)],
            *[{'x': 1532 + i * 100, 'y': 640 - i * 40, 'solid': True} for i in range(14)],
            
            # === AREA 3: CAVE SYSTEMS (2800-5000) ===
            # Complex cave floor
            *[{'x': 2800 + i * TILE_SIZE, 'y': 640, 'solid': True} for i in range(70)],
            # Cave ceiling (varies height)
            *[{'x': 2800 + i * 64, 'y': 350 - (i % 5) * 30, 'solid': True} for i in range(35)],
            # Stalactites (hang from ceiling)
            *[{'x': 3000 + i * 200, 'y': 350, 'solid': True} for i in range(10)],
            *[{'x': 3000 + i * 200, 'y': 382, 'solid': True} for i in range(10)],
            # Platforms in caves
            *[{'x': 3200 + (i % 6) * 150, 'y': 550 - (i // 6) * 60, 'solid': True} for i in range(24)],
            *[{'x': 3232 + (i % 6) * 150, 'y': 550 - (i // 6) * 60, 'solid': True} for i in range(24)],
            
            # === AREA 4: UNDERGROUND LAKE (5000-6500) ===
            # Water level simulation (lower platforms)
            *[{'x': 5000 + i * TILE_SIZE, 'y': 680, 'solid': True} for i in range(50)],
            # Islands in lake
            *[{'x': 5200, 'y': 600, 'solid': True}],
            *[{'x': 5232, 'y': 600, 'solid': True}],
            *[{'x': 5500, 'y': 580, 'solid': True}],
            *[{'x': 5532, 'y': 580, 'solid': True}],
            *[{'x': 5800, 'y': 600, 'solid': True}],
            *[{'x': 5832, 'y': 600, 'solid': True}],
            *[{'x': 6100, 'y': 580, 'solid': True}],
            *[{'x': 6132, 'y': 580, 'solid': True}],
            
            # === AREA 5: CRYSTAL CAVERNS (6500-8000) ===
            *[{'x': 6500 + i * TILE_SIZE, 'y': 640, 'solid': True} for i in range(50)],
            # Crystal formations (platforms at various heights)
            *[{'x': 6700 + i * 180, 'y': 550 - i * 25, 'solid': True} for i in range(15)],
            *[{'x': 6732 + i * 180, 'y': 550 - i * 25, 'solid': True} for i in range(15)],
            # Tall crystal pillars
            *[{'x': 7200, 'y': 640 - i * TILE_SIZE, 'solid': True} for i in range(8)],
            *[{'x': 7500, 'y': 640 - i * TILE_SIZE, 'solid': True} for i in range(10)],
            
            # === AREA 6: ASCENT & EXIT (8000-9500) ===
            # Climb back to surface
            *[{'x': 8000 + i * 80, 'y': 640 - i * 35, 'solid': True} for i in range(16)],
            *[{'x': 8032 + i * 80, 'y': 640 - i * 35, 'solid': True} for i in range(16)],
            # Surface exit
            *[{'x': 9200 + i * TILE_SIZE, 'y': 100, 'solid': True} for i in range(10)],
        ],
        'enemies': [
            # Area 1 - Surface
            {'x': 500, 'y': 590, 'type': 'ground', 'patrol': 150},
            {'x': 900, 'y': 430, 'type': 'ground', 'patrol': 150},
            # Area 2 - Descent
            {'x': 1700, 'y': 550, 'type': 'flying', 'patrol': 200},
            {'x': 2000, 'y': 400, 'type': 'flying', 'patrol': 200},
            # Area 3 - Cave systems
            {'x': 3000, 'y': 590, 'type': 'ground', 'patrol': 180},
            {'x': 3300, 'y': 590, 'type': 'ground', 'patrol': 180},
            {'x': 3600, 'y': 590, 'type': 'ground', 'patrol': 180},
            {'x': 3900, 'y': 590, 'type': 'ground', 'patrol': 180},
            {'x': 4200, 'y': 590, 'type': 'ground', 'patrol': 180},
            {'x': 3500, 'y': 450, 'type': 'flying', 'patrol': 250},
            {'x': 4000, 'y': 450, 'type': 'flying', 'patrol': 250},
            {'x': 4500, 'y': 450, 'type': 'flying', 'patrol': 250},
            {'x': 3800, 'y': 500, 'type': 'turret'},
            {'x': 4300, 'y': 500, 'type': 'turret'},
            # Area 4 - Lake
            {'x': 5300, 'y': 550, 'type': 'flying', 'patrol': 200},
            {'x': 5600, 'y': 530, 'type': 'flying', 'patrol': 200},
            {'x': 5900, 'y': 550, 'type': 'flying', 'patrol': 200},
            {'x': 6200, 'y': 530, 'type': 'flying', 'patrol': 200},
            # Area 5 - Crystal caverns
            {'x': 6800, 'y': 590, 'type': 'ground', 'patrol': 200},
            {'x': 7100, 'y': 500, 'type': 'ground', 'patrol': 150},
            {'x': 7400, 'y': 400, 'type': 'flying', 'patrol': 250},
            {'x': 7700, 'y': 350, 'type': 'flying', 'patrol': 250},
            # Area 6 - Ascent
            {'x': 8200, 'y': 550, 'type': 'flying', 'patrol': 250},
            {'x': 8500, 'y': 400, 'type': 'flying', 'patrol': 250},
            {'x': 8800, 'y': 250, 'type': 'flying', 'patrol': 250},
        ],
        'hazards': [
            # Cave spikes
            *[{'x': 2900 + i * 64, 'y': 640, 'type': 'spike'} for i in range(8)],
            *[{'x': 4600 + i * 64, 'y': 640, 'type': 'spike'} for i in range(6)],
            # Falling stalactites
            {'x': 3200, 'y': 350, 'type': 'falling_block'},
            {'x': 3600, 'y': 350, 'type': 'falling_block'},
            {'x': 4000, 'y': 350, 'type': 'falling_block'},
            # Moving platforms over water
            {'x': 5350, 'y': 620, 'type': 'moving_platform', 'width': 96},
            {'x': 5650, 'y': 620, 'type': 'moving_platform', 'width': 96},
            {'x': 5950, 'y': 620, 'type': 'moving_platform', 'width': 96},
            # Crystal area hazards
            {'x': 7000, 'y': 550, 'type': 'moving_platform', 'width': 128},
            {'x': 7600, 'y': 450, 'type': 'moving_platform', 'width': 128},
        ],
        'coins': [
            # Path coins
            *[{'x': 400 + i * 80, 'y': 510, 'value': 1} for i in range(60)],
            # Cave coins
            *[{'x': 3250 + (i % 6) * 150, 'y': 500 - (i // 6) * 60, 'value': 2} for i in range(24)],
            # Lake coins (risky)
            *[{'x': 5250 + i * 300, 'y': 550, 'value': 5} for i in range(4)],
            # Crystal coins
            *[{'x': 6750 + i * 180, 'y': 500 - i * 25, 'value': 2} for i in range(15)],
            # High value secrets
            {'x': 3500, 'y': 380, 'value': 20},
            {'x': 7500, 'y': 150, 'value': 25},
        ],
        'powerups': [
            {'x': 1800, 'y': 450, 'type': 'health'},
            {'x': 4000, 'y': 450, 'type': 'speed'},
            {'x': 6000, 'y': 530, 'type': 'invincible'},
            {'x': 7500, 'y': 300, 'type': 'health'},
            {'x': 9000, 'y': 200, 'type': 'health'},
        ],
        'keys': [],
        'portals': [
            {'x': 9350, 'y': 10, 'dest': 5}
        ]
    }
    levels.append(level_4)
    
    # ============================================================
    # LEVEL 5: "CONVERGENCE" (20 minutes, 10000px)
    # ============================================================
    
    level_5 = {
        'width': 10000,
        'height': 720,
        'theme': 'SCIFI',
        'spawn_x': 100,
        'spawn_y': 500,
        'time_limit': 'medium',
        'tiles': [
            # === AREA 1: GAUNTLET START (0-2000) ===
            *[{'x': i * TILE_SIZE, 'y': 640, 'solid': True} for i in range(65)],
            # Quick platforming warmup
            *[{'x': 300 + i * 100, 'y': 550 - (i % 3) * 50, 'solid': True} for i in range(15)],
            *[{'x': 332 + i * 100, 'y': 550 - (i % 3) * 50, 'solid': True} for i in range(15)],
            
            # === AREA 2: WALL JUMP TOWER (2000-3200) ===
            # Tall narrow tower requiring perfect wall jumps
            *[{'x': 2100, 'y': 640 - i * TILE_SIZE, 'solid': True} for i in range(20)],
            *[{'x': 2300, 'y': 640 - i * TILE_SIZE, 'solid': True} for i in range(20)],
            # Alternating mini platforms
            *[{'x': 2132 + (i % 2) * 136, 'y': 610 - i * 32, 'solid': True} for i in range(20)],
            # Tower top
            *[{'x': 2500 + i * TILE_SIZE, 'y': 100, 'solid': True} for i in range(20)],
            
            # === AREA 3: PRECISION PLATFORMING (3200-4800) ===
            # Narrow platforms with big gaps
            *[{'x': 3300 + i * 180, 'y': 150 + (i % 5) * 60, 'solid': True} for i in range(20)],
            *[{'x': 3332 + i * 180, 'y': 150 + (i % 5) * 60, 'solid': True} for i in range(20)],
            # Ground section
            *[{'x': 4500 + i * TILE_SIZE, 'y': 640, 'solid': True} for i in range(10)],
            
            # === AREA 4: COMBAT MARATHON (4800-6500) ===
            *[{'x': 4800 + i * TILE_SIZE, 'y': 640, 'solid': True} for i in range(55)],
            # Multi-level combat arena
            *[{'x': 5000, 'y': 550, 'solid': True}],
            *[{'x': 5032, 'y': 550, 'solid': True}],
            *[{'x': 5200, 'y': 500, 'solid': True}],
            *[{'x': 5232, 'y': 500, 'solid': True}],
            *[{'x': 5400, 'y': 450, 'solid': True}],
            *[{'x': 5432, 'y': 450, 'solid': True}],
            *[{'x': 5600, 'y': 500, 'solid': True}],
            *[{'x': 5632, 'y': 500, 'solid': True}],
            *[{'x': 5800, 'y': 550, 'solid': True}],
            *[{'x': 5832, 'y': 550, 'solid': True}],
            *[{'x': 6000, 'y': 500, 'solid': True}],
            *[{'x': 6032, 'y': 500, 'solid': True}],
            *[{'x': 6200, 'y': 450, 'solid': True}],
            *[{'x': 6232, 'y': 450, 'solid': True}],
            
            # === AREA 5: HAZARD GAUNTLET (6500-8000) ===
            *[{'x': 6500 + i * TILE_SIZE, 'y': 640, 'solid': True} for i in range(50)],
            # Platform path through hazards
            *[{'x': 6600 + i * 120, 'y': 550 - (i % 4) * 50, 'solid': True} for i in range(25)],
            *[{'x': 6632 + i * 120, 'y': 550 - (i % 4) * 50, 'solid': True} for i in range(25)],
            
            # === AREA 6: ESCAPE SEQUENCE (8000-9500) ===
            # Fast-paced platforming to boss door
            *[{'x': 8000 + i * TILE_SIZE, 'y': 640, 'solid': True} for i in range(50)],
            # Rising platforms
            *[{'x': 8100 + i * 90, 'y': 600 - i * 30, 'solid': True} for i in range(15)],
            *[{'x': 8132 + i * 90, 'y': 600 - i * 30, 'solid': True} for i in range(15)],
            
            # === AREA 7: BOSS DOOR (9500-10000) ===
            # Safe area before boss
            *[{'x': 9500 + i * TILE_SIZE, 'y': 640, 'solid': True} for i in range(16)],
            *[{'x': 9500 + i * TILE_SIZE, 'y': 200, 'solid': True} for i in range(16)],
            # Ascent to boss door
            *[{'x': 9600, 'y': 640 - i * TILE_SIZE, 'solid': True} for i in range(14)],
            *[{'x': 9700, 'y': 640 - i * TILE_SIZE, 'solid': True} for i in range(14)],
        ],
        'enemies': [
            # Area 1 - Warmup
            {'x': 500, 'y': 500, 'type': 'ground', 'patrol': 150},
            {'x': 800, 'y': 450, 'type': 'ground', 'patrol': 150},
            {'x': 1100, 'y': 400, 'type': 'flying', 'patrol': 200},
            {'x': 1500, 'y': 590, 'type': 'ground', 'patrol': 180},
            # Area 2 - Tower
            {'x': 2150, 'y': 500, 'type': 'flying', 'patrol': 150},
            {'x': 2200, 'y': 350, 'type': 'flying', 'patrol': 150},
            {'x': 2250, 'y': 200, 'type': 'flying', 'patrol': 150},
            # Area 3 - Precision
            {'x': 3500, 'y': 200, 'type': 'flying', 'patrol': 250},
            {'x': 3900, 'y': 250, 'type': 'flying', 'patrol': 250},
            {'x': 4300, 'y': 300, 'type': 'flying', 'patrol': 250},
            # Area 4 - Combat marathon (MANY enemies)
            {'x': 5050, 'y': 500, 'type': 'ground', 'patrol': 100},
            {'x': 5250, 'y': 450, 'type': 'ground', 'patrol': 100},
            {'x': 5450, 'y': 400, 'type': 'ground', 'patrol': 100},
            {'x': 5650, 'y': 450, 'type': 'ground', 'patrol': 100},
            {'x': 5850, 'y': 500, 'type': 'ground', 'patrol': 100},
            {'x': 6050, 'y': 450, 'type': 'ground', 'patrol': 100},
            {'x': 6250, 'y': 400, 'type': 'ground', 'patrol': 100},
            {'x': 5300, 'y': 400, 'type': 'flying', 'patrol': 250},
            {'x': 5700, 'y': 400, 'type': 'flying', 'patrol': 250},
            {'x': 6100, 'y': 400, 'type': 'flying', 'patrol': 250},
            {'x': 5100, 'y': 450, 'type': 'turret'},
            {'x': 5900, 'y': 450, 'type': 'turret'},
            {'x': 6300, 'y': 450, 'type': 'turret'},
            # Area 5 - Hazard gauntlet
            {'x': 6700, 'y': 500, 'type': 'flying', 'patrol': 250},
            {'x': 7000, 'y': 450, 'type': 'flying', 'patrol': 250},
            {'x': 7300, 'y': 400, 'type': 'flying', 'patrol': 250},
            {'x': 7600, 'y': 450, 'type': 'flying', 'patrol': 250},
            # Area 6 - Escape
            {'x': 8300, 'y': 550, 'type': 'flying', 'patrol': 250},
            {'x': 8600, 'y': 450, 'type': 'flying', 'patrol': 250},
            {'x': 8900, 'y': 350, 'type': 'flying', 'patrol': 250},
        ],
        'hazards': [
            # Tower spikes
            *[{'x': 2000 + i * 32, 'y': 640, 'type': 'spike'} for i in range(5)],
            # Precision section falling blocks
            {'x': 3400, 'y': 150, 'type': 'falling_block'},
            {'x': 3700, 'y': 200, 'type': 'falling_block'},
            {'x': 4000, 'y': 250, 'type': 'falling_block'},
            {'x': 4300, 'y': 300, 'type': 'falling_block'},
            # Combat arena moving platforms
            {'x': 5500, 'y': 550, 'type': 'moving_platform', 'width': 96},
            {'x': 6100, 'y': 550, 'type': 'moving_platform', 'width': 96},
            # MANY spikes in hazard gauntlet
            *[{'x': 6600 + i * 64, 'y': 640, 'type': 'spike'} for i in range(22)],
            # Moving platforms through spikes
            {'x': 6800, 'y': 500, 'type': 'moving_platform', 'width': 96},
            {'x': 7200, 'y': 450, 'type': 'moving_platform', 'width': 96},
            {'x': 7600, 'y': 500, 'type': 'moving_platform', 'width': 96},
            # Escape section hazards
            {'x': 8400, 'y': 500, 'type': 'moving_platform', 'width': 128},
            {'x': 8800, 'y': 400, 'type': 'moving_platform', 'width': 128},
        ],
        'coins': [
            # Generous coins on main path
            *[{'x': 350 + i * 100, 'y': 500 - (i % 3) * 50, 'value': 1} for i in range(80)],
            # Tower coins
            *[{'x': 2170 + (i % 2) * 100, 'y': 580 - i * 32, 'value': 2} for i in range(20)],
            # Precision coins (high risk/reward)
            *[{'x': 3350 + i * 180, 'y': 100 + (i % 5) * 60, 'value': 3} for i in range(20)],
            # Combat coins
            *[{'x': 5050 + i * 150, 'y': 450, 'value': 2} for i in range(20)],
            # Secret high value
            {'x': 2600, 'y': 50, 'value': 30},
            {'x': 7500, 'y': 350, 'value': 25},
        ],
        'powerups': [
            {'x': 1800, 'y': 590, 'type': 'health'},
            {'x': 2700, 'y': 50, 'type': 'double_jump'},
            {'x': 4700, 'y': 590, 'type': 'health'},
            {'x': 6300, 'y': 400, 'type': 'invincible'},
            {'x': 8000, 'y': 590, 'type': 'speed'},
            {'x': 9200, 'y': 150, 'type': 'health'},
            {'x': 9650, 'y': 590, 'type': 'health'},
        ],
        'keys': [],
        'portals': [
            {'x': 9850, 'y': 110, 'dest': 6, 'color': [255, 0, 0]}
        ]
    }
    levels.append(level_5)
    
    # ============================================================
    # LEVEL 6: "GUARDIAN'S LAIR" - BOSS FIGHT
    # ============================================================
    
    boss_arena = {
        'width': 1280,
        'height': 720,
        'theme': 'SCIFI',
        'spawn_x': 200,
        'spawn_y': 580,
        'time_limit': 'none',
        'tiles': [
            # Floor
            *[{'x': i * TILE_SIZE, 'y': 640, 'solid': True} for i in range(40)],
            # Side walls (prevent escape)
            *[{'x': 0, 'y': i * TILE_SIZE, 'solid': True} for i in range(22)],
            *[{'x': 1248, 'y': i * TILE_SIZE, 'solid': True} for i in range(22)],
            # Ceiling
            *[{'x': i * TILE_SIZE, 'y': 0, 'solid': True} for i in range(40)],
            # Small platforms for player mobility
            {'x': 200, 'y': 550, 'solid': True},
            {'x': 232, 'y': 550, 'solid': True},
            {'x': 400, 'y': 500, 'solid': True},
            {'x': 432, 'y': 500, 'solid': True},
            {'x': 600, 'y': 450, 'solid': True},
            {'x': 632, 'y': 450, 'solid': True},
            {'x': 800, 'y': 500, 'solid': True},
            {'x': 832, 'y': 500, 'solid': True},
            {'x': 1000, 'y': 550, 'solid': True},
            {'x': 1032, 'y': 550, 'solid': True},
        ],
        'enemies': [],
        'hazards': [
            # Corner spikes (activate in phase 3)
            {'x': 64, 'y': 640, 'type': 'spike'},
            {'x': 1184, 'y': 640, 'type': 'spike'},
        ],
        'coins': [],
        'powerups': [
            # Health pickups for long fight
            {'x': 200, 'y': 510, 'type': 'health'},
            {'x': 1000, 'y': 510, 'type': 'health'},
        ],
        'keys': [],
        'portals': []
    }
    levels.append(boss_arena)
    
    return levels
