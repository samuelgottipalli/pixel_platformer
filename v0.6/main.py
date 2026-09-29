"""
Retro Pixel Platformer - Main Entry Point
"""

import os
import sys

# Add project root to path, and run from it: config, data and assets are
# loaded by relative path, so launching from another folder would break them
GAME_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, GAME_DIR)
os.chdir(GAME_DIR)

# Status prints use symbols like ✓; don't crash when stdout can't encode them
# (e.g. output redirected to a file on Windows)
for stream in (sys.stdout, sys.stderr):
    if stream and hasattr(stream, "reconfigure"):
        stream.reconfigure(errors="replace")

from core.game import Game


def main():
    """Main entry point"""
    try:
        game = Game()
        game.run()
    except Exception as e:
        # Keep a crash log so a crash is never mistaken for the game "just
        # closing" (there is no console when the game is double-clicked)
        import traceback
        from datetime import datetime

        print(f"Fatal error: {e}")
        traceback.print_exc()
        os.makedirs("data", exist_ok=True)
        with open(os.path.join("data", "crash.log"), "a", encoding="utf-8") as log:
            log.write(f"\n=== {datetime.now():%Y-%m-%d %H:%M:%S} ===\n")
            traceback.print_exc(file=log)
        sys.exit(1)


if __name__ == "__main__":
    main()
