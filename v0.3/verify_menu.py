"""
Quick verification that menu.py has been updated correctly
Run this from your project root: python verify_menu.py
"""

def verify_menu_updated():
    """Check if menu.py has the correct signature"""
    try:
        with open('ui/menu.py', 'r') as f:
            content = f.read()
        
        # Check for the new signature
        if 'def draw_main_menu(self, surface, selection, mouse_pos=None):' in content:
            print("✓ menu.py is UPDATED correctly!")
            print("✓ draw_main_menu signature supports mouse_pos")
            return True
        elif 'def draw_main_menu(self, surface, selection):' in content:
            print("✗ menu.py is OLD version!")
            print("✗ You need to replace ui/menu.py with the new version")
            print("\nFix:")
            print("1. Copy the menu.py from outputs folder")
            print("2. Replace your ui/menu.py file")
            return False
        else:
            print("? Could not find draw_main_menu method")
            return False
            
    except FileNotFoundError:
        print("✗ ui/menu.py not found!")
        print("Make sure you're running this from your project root")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Menu.py Verification")
    print("=" * 60)
    print()
    
    if verify_menu_updated():
        print("\n" + "=" * 60)
        print("All good! Your menu.py is updated.")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("ACTION REQUIRED: Update your menu.py file")
        print("=" * 60)
