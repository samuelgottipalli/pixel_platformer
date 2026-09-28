"""
Act 1 level names (from the original ACT1_LEVEL_MAP design doc).
Single source of truth for the HUD, debug overlay and level map.
"""

LEVEL_NAMES = [
    "Training Facility",
    "The Awakening",
    "Rising Conflict",
    "The Ascent",
    "Deep Dive",
    "Convergence",
    "Guardian's Lair",
]

BOSS_LEVELS = {6}


def level_title(index, mark_boss=False):
    """Display title, e.g. 'Tutorial: Training Facility' or 'Level 3: The Ascent'"""
    if not 0 <= index < len(LEVEL_NAMES):
        return f"Level {index}"
    prefix = "Tutorial" if index == 0 else f"Level {index}"
    suffix = " (BOSS)" if mark_boss and index in BOSS_LEVELS else ""
    return f"{prefix}: {LEVEL_NAMES[index]}{suffix}"
