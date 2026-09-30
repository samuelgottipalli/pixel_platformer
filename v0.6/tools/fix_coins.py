"""
Move coins the player can't collect (inside or between bricks, or floating
where no jump reaches) to the nearest spot the player can actually reach.

Reachability comes from tools/level_checker.py (real player physics). A coin
that can't be collected is moved into a standing spot's body height, keeping
its x position when a reachable platform is directly above/below it so rows
and arcs keep their shape. Coins with no reachable spot nearby are removed.

CLI:  python tools/fix_coins.py              (all levels, writes the JSON files)
      python tools/fix_coins.py act1/level_03.json
"""

import os
import sys

if __package__ in (None, ""):  # run as a script: make the game importable
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame  # noqa: E402

COIN_SIZE = 16
PLAYER_WIDTH = 28
KEEP_X_RANGE = 40      # reuse a coin's x if a spot is this close horizontally
MAX_MOVE = 700         # coins further than this from any reachable spot are removed


def _solid_rects(level_data, tile_size=32):
    return [pygame.Rect(t["x"], t["y"], tile_size, tile_size)
            for t in level_data["tiles"] if t.get("solid", True)]


def fix_coins(level_data, verbose=False):
    """
    Fix coin placement in level_data (modified in place).
    Returns (moved, removed) counts.
    """
    from tools.level_checker import LevelChecker

    tiles = _solid_rects(level_data)
    coins = level_data.get("coins", [])
    moved = removed = 0

    for attempt in range(2):
        checker = LevelChecker(level_data).check()
        spots = list(checker.spot_positions.values())
        bad = [i for i, c in enumerate(coins)
               if i not in checker.coins_seen
               or pygame.Rect(c["x"], c["y"], COIN_SIZE, COIN_SIZE).collidelist(tiles) != -1]
        if not bad:
            break

        taken = [pygame.Rect(c["x"], c["y"], COIN_SIZE, COIN_SIZE).inflate(8, 8)
                 for i, c in enumerate(coins) if i not in bad]
        keep = []
        for i, coin in enumerate(coins):
            if i not in bad:
                keep.append(coin)
                continue
            best = None
            for px, py in spots:
                keep_x = attempt == 0 and abs((px + PLAYER_WIDTH / 2) - (coin["x"] + COIN_SIZE / 2)) <= KEEP_X_RANGE
                x = coin["x"] if keep_x else int(px) + (PLAYER_WIDTH - COIN_SIZE) // 2
                y = int(py) + 16  # chest height of a standing player
                rect = pygame.Rect(x, y, COIN_SIZE, COIN_SIZE)
                if rect.collidelist(tiles) != -1 or rect.collidelist(taken) != -1:
                    continue
                cost = abs(x - coin["x"]) * 2 + abs(y - coin["y"])  # prefer vertical moves
                if cost <= MAX_MOVE and (best is None or cost < best[0]):
                    best = (cost, x, y)
            if best is None:
                removed += 1
                if verbose:
                    print(f"   removed coin at ({coin['x']}, {coin['y']})")
                continue
            _, x, y = best
            if verbose:
                print(f"   moved coin ({coin['x']}, {coin['y']}) -> ({x}, {y})")
            coin = dict(coin, x=x, y=y)
            taken.append(pygame.Rect(x, y, COIN_SIZE, COIN_SIZE).inflate(8, 8))
            keep.append(coin)
            moved += 1
        coins[:] = keep
    return moved, removed


def main():
    game_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(game_dir)
    sys.stdout.reconfigure(errors="replace")
    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    pygame.init()
    pygame.display.set_mode((1280, 720))
    from config.settings import update_screen_size
    from levels.level_loader import LevelLoader

    update_screen_size(1280, 720)
    files = sys.argv[1:] or [lvl["file"] for act in LevelLoader.load_acts() for lvl in act["levels"]]
    for filename in files:
        data = LevelLoader.load_from_file(filename)
        moved, removed = fix_coins(data)
        if moved or removed:
            LevelLoader.save_to_file(data, filename)
        print(f"{filename}: moved {moved}, removed {removed}")


if __name__ == "__main__":
    main()
