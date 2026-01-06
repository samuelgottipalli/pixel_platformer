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

# Debug Controls
DEBUG_TOGGLE = [pygame.K_F3]

def check_key_pressed(keys, key_list):
    """Check if any key in key_list is pressed"""
    return any(keys[key] for key in key_list)

def check_key_event(event, key_list):
    """Check if event key is in key_list"""
    return event.key in key_list
