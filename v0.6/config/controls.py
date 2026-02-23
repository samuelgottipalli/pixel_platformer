"""
Control Bindings Configuration
"""

import pygame

# Movement Controls
MOVE_LEFT = [pygame.K_LEFT, pygame.K_a]
MOVE_RIGHT = [pygame.K_RIGHT, pygame.K_d]
MOVE_UP = [pygame.K_UP, pygame.K_w]
MOVE_DOWN = [pygame.K_DOWN, pygame.K_s]

# Action Controls
JUMP = [pygame.K_SPACE, pygame.K_w, pygame.K_UP]
SHOOT = [pygame.K_z, pygame.K_j]
MELEE = [pygame.K_x, pygame.K_k]
UPGRADE_WEAPON = [pygame.K_u]

# Menu Controls
MENU_UP = [pygame.K_UP, pygame.K_w]
MENU_DOWN = [pygame.K_DOWN, pygame.K_s]
MENU_LEFT = [pygame.K_LEFT, pygame.K_a]
MENU_RIGHT = [pygame.K_RIGHT, pygame.K_d]
MENU_SELECT = [pygame.K_RETURN, pygame.K_SPACE]
MENU_BACK = [pygame.K_ESCAPE]

# System Controls
PAUSE = [pygame.K_ESCAPE, pygame.K_p]
SAVE_GAME = [pygame.K_F5]
QUIT = [pygame.K_ESCAPE]
TOGGLE_CONTROLS = [pygame.K_F1]

# Debug Controls
DEBUG_TOGGLE = [pygame.K_F3]

# Weapon Switching
STANDARD = [pygame.K_1]
DUAL_BACK = [pygame.K_2]
SPREAD = [pygame.K_3]
DUAL_FRONT = [pygame.K_4]
EXPLOSIVE = [pygame.K_5]
# WEAPON_6 = [pygame.K_6]
# WEAPON_7 = [pygame.K_7]
# TOGGLE_WEAPON = [pygame.K_t, pygame.K_TAB]



def check_key_pressed(keys, key_list):
    """Check if any key in key_list is pressed"""
    return any(keys[key] for key in key_list)


def check_key_event(event, key_list):
    """Check if event key is in key_list"""
    return event.key in key_list
