"""
Level display titles. Names live in each level's JSON file ("name");
levels are numbered by their global index across all acts.
"""


def level_title(level, mark_boss=False):
    """
    Display title for a level data dict, e.g. 'Tutorial: Training Facility',
    'Level 7: Forest Entrance' or 'Level 12: Forest Guardian (BOSS)'.
    """
    index = level.get("index", 0)
    name = level.get("name") or f"Level {index}"
    prefix = "Tutorial" if index == 0 else f"Level {index}"
    suffix = " (BOSS)" if mark_boss and level.get("boss") else ""
    return f"{prefix}: {name}{suffix}"
