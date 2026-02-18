import json

from act1_levels_design import get_act1_levels

levels = get_act1_levels()
names = ["tutorial", "level01", "level02", "level03", "level04", "level05", "boss01"]

for i, level in enumerate(levels):
    filename = f"levels/data/act1_{names[i]}.json"
    with open(filename, "w") as f:
        json.dump(level, f, indent=2)
    print(f"✓ Saved {filename}")
