"""
Weapon and Stats Catalog
Central data store for all weapons, upgrades, and stat purchases
"""

# ============================================================
# WEAPON CATALOG
# ============================================================

WEAPON_CATALOG = {
    "standard": {
        "name": "Standard Shot",
        "unlock_cost": 0,  # Free starting weapon
        "description": "Single forward projectile - reliable and accurate",
        "type": "projectile",
        "power_max": 4,
        "speed_max": 3,
        "power_upgrades": [
            {"level": 1, "cost": 0, "damage": 10},      # Starting level
            {"level": 2, "cost": 40, "damage": 15},
            {"level": 3, "cost": 80, "damage": 20},
            {"level": 4, "cost": 120, "damage": 25}
        ],
        "speed_upgrades": [
            {"level": 1, "cost": 0, "speed": 8},        # Starting level
            {"level": 2, "cost": 30, "speed": 10},
            {"level": 3, "cost": 60, "speed": 12}
        ]
    },
    
    "dual_back": {
        "name": "Dual Shot",
        "unlock_cost": 50,
        "description": "Shoots forward AND backward - defensive coverage",
        "type": "projectile",
        "power_max": 4,
        "speed_max": 3,
        "power_upgrades": [
            {"level": 1, "cost": 0, "damage": 10},      # Gets level 1 on unlock
            {"level": 2, "cost": 40, "damage": 15},
            {"level": 3, "cost": 80, "damage": 20},
            {"level": 4, "cost": 120, "damage": 25}
        ],
        "speed_upgrades": [
            {"level": 1, "cost": 0, "speed": 8},
            {"level": 2, "cost": 30, "speed": 10},
            {"level": 3, "cost": 60, "speed": 12}
        ]
    },
    
    "spread": {
        "name": "Spread Shot",
        "unlock_cost": 100,
        "description": "Multi-directional spread pattern - area coverage",
        "type": "projectile",
        "power_max": 4,
        "speed_max": 3,
        "power_upgrades": [
            {"level": 1, "cost": 0, "damage": 8, "count": 3, "spread": 30},
            {"level": 2, "cost": 60, "damage": 10, "count": 5, "spread": 35},
            {"level": 3, "cost": 100, "damage": 12, "count": 5, "spread": 40},
            {"level": 4, "cost": 140, "damage": 15, "count": 7, "spread": 45}
        ],
        "speed_upgrades": [
            {"level": 1, "cost": 0, "speed": 7},
            {"level": 2, "cost": 40, "speed": 9},
            {"level": 3, "cost": 70, "speed": 11}
        ]
    },
    
    "dual_front": {
        "name": "Dual Front",
        "unlock_cost": 150,
        "description": "Heavy dual forward shots - high damage output",
        "type": "projectile",
        "power_max": 4,
        "speed_max": 3,
        "power_upgrades": [
            {"level": 1, "cost": 0, "damage": 15, "offset": 10},    # offset = spacing between shots
            {"level": 2, "cost": 70, "damage": 20, "offset": 10},
            {"level": 3, "cost": 110, "damage": 25, "offset": 12},
            {"level": 4, "cost": 150, "damage": 30, "offset": 12}
        ],
        "speed_upgrades": [
            {"level": 1, "cost": 0, "speed": 7},
            {"level": 2, "cost": 50, "speed": 9},
            {"level": 3, "cost": 80, "speed": 11}
        ]
    },
    
    "explosive": {
        "name": "Timed Explosion",
        "unlock_cost": 200,
        "description": "Throwable timed bomb - explosive area damage",
        "type": "explosive",
        "power_max": 4,
        "speed_max": 3,
        "power_upgrades": [
            {"level": 1, "cost": 0, "damage": 30, "radius": 50},
            {"level": 2, "cost": 90, "damage": 40, "radius": 75},
            {"level": 3, "cost": 130, "damage": 50, "radius": 100},
            {"level": 4, "cost": 180, "damage": 60, "radius": 125}
        ],
        "speed_upgrades": [
            {"level": 1, "cost": 0, "fuse": 2.0, "throw_speed": 6},
            {"level": 2, "cost": 60, "fuse": 1.5, "throw_speed": 8},
            {"level": 3, "cost": 100, "fuse": 1.0, "throw_speed": 10}
        ]
    }
}


# ============================================================
# STATS CATALOG
# ============================================================

STATS_CATALOG = {
    "health": [
        {
            "name": "Max HP +25",
            "cost": 50,
            "hp_increase": 25,
            "description": "Increase maximum health"
        },
        {
            "name": "Max HP +25",
            "cost": 100,
            "hp_increase": 25,
            "description": "Increase maximum health",
            "requires_hp": 125  # Must have at least 125 HP to buy this
        },
        {
            "name": "Max HP +25",
            "cost": 150,
            "hp_increase": 25,
            "description": "Increase maximum health",
            "requires_hp": 150
        },
        {
            "name": "Max HP +50",
            "cost": 250,
            "hp_increase": 50,
            "description": "Major health increase",
            "requires_hp": 175
        }
    ],
    
    "lives": [
        {
            "name": "Extra Life +1",
            "cost": 75,
            "description": "Start with an additional life"
        },
        {
            "name": "Extra Life +1",
            "cost": 150,
            "description": "Start with an additional life",
            "requires_lives": 4
        },
        {
            "name": "Extra Life +1",
            "cost": 250,
            "description": "Start with an additional life",
            "requires_lives": 5
        },
        {
            "name": "Extra Life +1",
            "cost": 400,
            "description": "Start with an additional life",
            "requires_lives": 6
        }
    ],
    
    "consumables": [
        {
            "name": "Health Potion",
            "cost": 10,
            "hp_restore": 50,
            "description": "Restore 50 HP instantly",
            "consumable": True,
            "max_stack": 5  # Can buy up to 5 at a time
        }
    ]
}


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_weapon_info(weapon_id):
    """Get weapon catalog entry"""
    return WEAPON_CATALOG.get(weapon_id)


def get_weapon_power_upgrade(weapon_id, level):
    """Get power upgrade data for weapon at level"""
    weapon = WEAPON_CATALOG.get(weapon_id)
    if weapon and 0 < level <= weapon["power_max"]:
        return weapon["power_upgrades"][level - 1]
    return None


def get_weapon_speed_upgrade(weapon_id, level):
    """Get speed upgrade data for weapon at level"""
    weapon = WEAPON_CATALOG.get(weapon_id)
    if weapon and 0 < level <= weapon["speed_max"]:
        return weapon["speed_upgrades"][level - 1]
    return None


def get_all_weapon_ids():
    """Get list of all weapon IDs in order"""
    return ["standard", "dual_back", "spread", "dual_front", "explosive"]


def get_total_weapon_cost(weapon_id, power_level, speed_level):
    """Calculate total coins spent on a weapon"""
    total = 0
    weapon = WEAPON_CATALOG.get(weapon_id)
    
    if not weapon:
        return 0
    
    # Add unlock cost if not standard
    if weapon_id != "standard":
        total += weapon["unlock_cost"]
    
    # Add power upgrade costs
    for lvl in range(1, power_level):
        upgrade = weapon["power_upgrades"][lvl]
        total += upgrade["cost"]
    
    # Add speed upgrade costs
    for lvl in range(1, speed_level):
        upgrade = weapon["speed_upgrades"][lvl]
        total += upgrade["cost"]
    
    return total


def can_afford_upgrade(player_coins, cost):
    """Check if player can afford an upgrade"""
    return player_coins >= cost


def get_stat_upgrade_index(stat_type, current_value):
    """
    Get next available stat upgrade index
    
    Args:
        stat_type: 'health' or 'lives'
        current_value: Current max HP or max lives
    
    Returns:
        Index of next available upgrade, or -1 if maxed
    """
    if stat_type == "health":
        # Starting HP is 100
        hp_purchased = (current_value - 100) // 25
        if hp_purchased < len(STATS_CATALOG["health"]):
            return hp_purchased
    elif stat_type == "lives":
        # Starting lives is 3
        lives_purchased = current_value - 3
        if lives_purchased < len(STATS_CATALOG["lives"]):
            return lives_purchased
    
    return -1  # Maxed out
