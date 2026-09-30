"""
Level loader - levels are JSON data files, grouped into acts.

    levels/data/acts.json              act list: number, name, level files
    levels/data/act1/level_00.json     one file per level

Levels are addressed by a global index (0 = Act 1 tutorial, 6 = Act 1 boss,
7 = first level of Act 2, ...). Portals' "dest" and save files use it.

Edit levels with the level builder (python level_builder.py) or generate
them with the scripts in tools/.
"""

import json
import os

from config.settings import LEVELS_DIR

ACTS_FILE = os.path.join(LEVELS_DIR, "acts.json")


class LevelLoader:
    """Loads and saves level data"""

    @staticmethod
    def fix_spike_positions(level_data):
        """Fix spike positions to be on top of ground"""
        for hazard in level_data.get("hazards", []):
            if hazard["type"] == "spike" and hazard.get("y", 0) >= 640:
                hazard["y"] = 608  # 640 - 32 = 608 (on top of ground)
        return level_data

    @staticmethod
    def load_acts():
        """
        Load every act and its levels.
        Returns:
            List of acts: {"number", "name", "theme", "levels": [level data...]}.
            Each level dict also gets "act" and "index" (global index).
        """
        with open(ACTS_FILE, "r", encoding="utf-8") as f:
            acts = json.load(f)

        index = 0
        for act in acts:
            loaded = []
            for filename in act["levels"]:
                data = LevelLoader.load_from_file(filename)
                if data is None:
                    raise FileNotFoundError(f"Level file missing: {filename}")
                data = LevelLoader.fix_spike_positions(data)
                data["act"] = act["number"]
                data["index"] = index
                data["file"] = filename
                loaded.append(data)
                index += 1
            act["levels"] = loaded
        return acts

    @staticmethod
    def create_default_levels():
        """All levels of all acts, in play order (global index order)"""
        levels = [level for act in LevelLoader.load_acts() for level in act["levels"]]
        print(f"✓ Loaded {len(levels)} levels")
        return levels

    @staticmethod
    def load_from_file(filename):
        """
        Load one level from JSON
        Args:
            filename: Path relative to levels/data (e.g. "act1/level_00.json")
        Returns:
            Level data dictionary, or None if it can't be read
        """
        try:
            with open(os.path.join(LEVELS_DIR, filename), "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading level {filename}: {e}")
            return None

    @staticmethod
    def save_to_file(level_data, filename):
        """
        Save one level as JSON: top-level keys indented, one tile/enemy/coin
        per line, so files stay readable and git diffs stay small.
        Runtime-only keys ("act", "index", "file") are not written.
        """
        try:
            path = os.path.join(LEVELS_DIR, filename)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            data = {k: v for k, v in level_data.items() if k not in ("act", "index", "file")}
            lines = ["{"]
            items = list(data.items())
            for i, (key, value) in enumerate(items):
                comma = "," if i < len(items) - 1 else ""
                if isinstance(value, list) and value:
                    lines.append(f"  {json.dumps(key)}: [")
                    for j, item in enumerate(value):
                        item_comma = "," if j < len(value) - 1 else ""
                        lines.append(f"    {json.dumps(item)}{item_comma}")
                    lines.append(f"  ]{comma}")
                else:
                    lines.append(f"  {json.dumps(key)}: {json.dumps(value)}{comma}")
            lines.append("}")
            with open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write("\n".join(lines) + "\n")
            return True
        except Exception as e:
            print(f"Error saving level {filename}: {e}")
            return False

    @staticmethod
    def save_acts(acts):
        """Write acts.json (act metadata + level file names)"""
        data = [
            {
                "number": act["number"],
                "name": act["name"],
                "theme": act.get("theme", "SCIFI"),
                "levels": [lvl if isinstance(lvl, str) else lvl["file"] for lvl in act["levels"]],
            }
            for act in acts
        ]
        os.makedirs(LEVELS_DIR, exist_ok=True)
        with open(ACTS_FILE, "w", encoding="utf-8", newline="\n") as f:
            json.dump(data, f, indent=2)
            f.write("\n")
