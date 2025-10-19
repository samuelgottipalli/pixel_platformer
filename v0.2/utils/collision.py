"""
Collision detection utilities
"""
import pygame

def check_collision(rect1, rect2):
    """Check if two rectangles collide"""
    return rect1.colliderect(rect2)

def check_collision_list(rect, rect_list):
    """
    Check collision with list of rectangles
    Returns the first colliding rectangle or None
    """
    for r in rect_list:
        if rect.colliderect(r):
            return r
    return None

def get_all_collisions(rect, rect_list):
    """Get all rectangles that collide with rect"""
    collisions = []
    for r in rect_list:
        if rect.colliderect(r):
            collisions.append(r)
    return collisions

def point_in_rect(point, rect):
    """Check if a point (x, y) is inside a rectangle"""
    x, y = point
    return rect.left <= x <= rect.right and rect.top <= y <= rect.bottom

def distance_between_rects(rect1, rect2):
    """Calculate distance between centers of two rectangles"""
    dx = rect1.centerx - rect2.centerx
    dy = rect1.centery - rect2.centery
    return (dx ** 2 + dy ** 2) ** 0.5

def is_rect_on_screen(rect, camera_x, camera_y, screen_width, screen_height, margin=32):
    """Check if rectangle is visible on screen (with margin)"""
    screen_rect = pygame.Rect(camera_x - margin, camera_y - margin, 
                             screen_width + margin * 2, screen_height + margin * 2)
    return rect.colliderect(screen_rect)