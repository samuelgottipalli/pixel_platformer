"""
Retro Pixel Platformer - Main Entry Point
"""

import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.game import Game


def main():
    """Main entry point"""
    try:
        game = Game()
        game.run()
    except Exception as e:
        print(f"Fatal error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
