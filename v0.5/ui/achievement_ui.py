"""
Achievement UI Components
Notification popup and achievement display screen
"""

import pygame
from config.settings import UI_BG, UI_BORDER, UI_HIGHLIGHT, UI_TEXT, UI_TEXT_DIM, WHITE, BLACK, SCREEN_WIDTH, SCREEN_HEIGHT


class AchievementNotification:
    """Popup notification when achievement is unlocked"""
    
    def __init__(self, achievement, font_medium, font_small):
        """Initialize achievement notification"""
        self.achievement = achievement
        self.font_medium = font_medium
        self.font_small = font_small
        
        # Animation
        self.timer = 300  # Show for 5 seconds (60fps)
        self.max_timer = 300
        self.slide_in_time = 30  # 0.5 seconds
        self.slide_out_time = 30
        
        # Position (slides in from right)
        self.width = 400
        self.height = 100
        self.target_x = SCREEN_WIDTH - self.width - 20
        self.target_y = 20
        self.current_x = SCREEN_WIDTH  # Start off-screen
        self.current_y = self.target_y
    
    def update(self):
        """Update notification animation"""
        self.timer -= 1
        
        # Slide in
        if self.timer > self.max_timer - self.slide_in_time:
            progress = (self.max_timer - self.timer) / self.slide_in_time
            self.current_x = SCREEN_WIDTH - (SCREEN_WIDTH - self.target_x) * progress
        
        # Slide out
        elif self.timer < self.slide_out_time:
            progress = self.timer / self.slide_out_time
            self.current_x = self.target_x + (SCREEN_WIDTH - self.target_x) * (1 - progress)
        
        # Stay in position
        else:
            self.current_x = self.target_x
        
        return self.timer > 0
    
    def draw(self, surface):
        """Draw notification"""
        x = int(self.current_x)
        y = int(self.current_y)
        
        # Background with glow effect
        glow_rect = pygame.Rect(x - 2, y - 2, self.width + 4, self.height + 4)
        pygame.draw.rect(surface, (255, 215, 0), glow_rect, border_radius=10)
        
        bg_rect = pygame.Rect(x, y, self.width, self.height)
        pygame.draw.rect(surface, UI_BG, bg_rect, border_radius=8)
        pygame.draw.rect(surface, UI_HIGHLIGHT, bg_rect, 3, border_radius=8)
        
        # "Achievement Unlocked!" text
        header_text = self.font_small.render("Achievement Unlocked!", True, (255, 215, 0))
        surface.blit(header_text, (x + 20, y + 15))
        
        # Achievement name
        name_text = self.font_medium.render(self.achievement.name, True, WHITE)
        surface.blit(name_text, (x + 20, y + 40))
        
        # Reward info if exists
        if self.achievement.reward_type:
            reward_text = self._get_reward_text()
            reward_surface = self.font_small.render(reward_text, True, UI_TEXT_DIM)
            surface.blit(reward_surface, (x + 20, y + 70))
    
    def _get_reward_text(self):
        """Get reward description text"""
        if self.achievement.reward_type == 'life':
            return f"Reward: +{self.achievement.reward_value} Lives"
        elif self.achievement.reward_type == 'weapon':
            return f"Reward: Weapon Upgrade"
        elif self.achievement.reward_type == 'score':
            return f"Reward: +{self.achievement.reward_value} Points"
        elif self.achievement.reward_type == 'unlock':
            return f"Reward: Unlocked {self.achievement.reward_value}"
        return ""


class AchievementScreen:
    """Full achievements display screen"""
    
    def __init__(self, font_large, font_medium, font_small, font_tiny):
        """Initialize achievement screen"""
        self.font_large = font_large
        self.font_medium = font_medium
        self.font_small = font_small
        self.font_tiny = font_tiny
        
        # Categories
        self.categories = [
            ('collection', 'Collection'),
            ('combat', 'Combat'),
            ('difficulty', 'Difficulty'),
            ('speed', 'Speed'),
            ('boss', 'Boss'),
            ('exploration', 'Exploration'),
            ('challenge', 'Challenge')
        ]
        
        self.selected_category = 0
        self.scroll_offset = 0
    
    def draw(self, surface, achievement_manager, mouse_pos=None):
        """Draw achievements screen"""
        surface.fill(BLACK)
        
        # Title
        title = self.font_large.render("ACHIEVEMENTS", True, UI_HIGHLIGHT)
        surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 40))
        
        # Stats
        stats = achievement_manager.get_stats()
        stats_text = self.font_small.render(
            f"Unlocked: {stats['unlocked']}/{stats['total']} ({stats['completion']}%)",
            True, UI_TEXT
        )
        surface.blit(stats_text, (SCREEN_WIDTH // 2 - stats_text.get_width() // 2, 90))
        
        # Category tabs
        tab_y = 140
        tab_width = 140
        tab_height = 40
        tab_spacing = 10
        start_x = (SCREEN_WIDTH - (len(self.categories) * (tab_width + tab_spacing))) // 2
        
        for i, (cat_id, cat_name) in enumerate(self.categories):
            x = start_x + i * (tab_width + tab_spacing)
            tab_rect = pygame.Rect(x, tab_y, tab_width, tab_height)
            
            is_selected = i == self.selected_category
            
            # Check mouse hover
            if mouse_pos and tab_rect.collidepoint(mouse_pos):
                is_selected = True
            
            # Draw tab
            if is_selected:
                pygame.draw.rect(surface, UI_HIGHLIGHT, tab_rect, border_radius=5)
                text_color = BLACK
            else:
                pygame.draw.rect(surface, UI_BG, tab_rect, border_radius=5)
                pygame.draw.rect(surface, UI_BORDER, tab_rect, 1, border_radius=5)
                text_color = UI_TEXT
            
            # Category name
            text = self.font_tiny.render(cat_name, True, text_color)
            text_x = x + tab_width // 2 - text.get_width() // 2
            text_y = tab_y + tab_height // 2 - text.get_height() // 2
            surface.blit(text, (text_x, text_y))
        
        # Achievement list for selected category
        category_id = self.categories[self.selected_category][0]
        achievements = achievement_manager.get_achievements_by_category(category_id)
        
        list_y = 220
        item_height = 80
        visible_items = 5
        
        for i, achievement in enumerate(achievements):
            y = list_y + i * item_height - self.scroll_offset
            
            # Skip if not visible
            if y < list_y - item_height or y > list_y + visible_items * item_height:
                continue
            
            self._draw_achievement_item(surface, achievement, 100, y, SCREEN_WIDTH - 200)
        
        # Scroll indicators
        if len(achievements) > visible_items:
            if self.scroll_offset > 0:
                arrow_up = self.font_medium.render("▲", True, UI_HIGHLIGHT)
                surface.blit(arrow_up, (SCREEN_WIDTH // 2 - arrow_up.get_width() // 2, list_y - 30))
            
            max_scroll = max(0, len(achievements) * item_height - visible_items * item_height)
            if self.scroll_offset < max_scroll:
                arrow_down = self.font_medium.render("▼", True, UI_HIGHLIGHT)
                surface.blit(arrow_down, (SCREEN_WIDTH // 2 - arrow_down.get_width() // 2, list_y + visible_items * item_height + 10))
        
        # Instructions
        hint = self.font_tiny.render("ESC Back   LEFT/RIGHT Change Category   UP/DOWN Scroll", True, UI_TEXT_DIM)
        surface.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, SCREEN_HEIGHT - 50))
    
    def _draw_achievement_item(self, surface, achievement, x, y, width):
        """Draw individual achievement item"""
        height = 70
        
        # Background
        bg_rect = pygame.Rect(x, y, width, height)
        
        if achievement.unlocked:
            # Unlocked - golden glow
            pygame.draw.rect(surface, (80, 60, 0), bg_rect, border_radius=5)
            bg_color = (40, 40, 30)
        else:
            # Locked - dark
            bg_color = UI_BG
        
        pygame.draw.rect(surface, bg_color, bg_rect, border_radius=5)
        
        if achievement.unlocked:
            border_color = (255, 215, 0)  # Gold
        else:
            border_color = UI_BORDER
        
        pygame.draw.rect(surface, border_color, bg_rect, 2, border_radius=5)
        
        # Icon area
        icon_size = 50
        icon_rect = pygame.Rect(x + 10, y + 10, icon_size, icon_size)
        
        if achievement.unlocked:
            # Draw checkmark
            pygame.draw.circle(surface, (255, 215, 0), icon_rect.center, icon_size // 2)
            pygame.draw.circle(surface, BLACK, icon_rect.center, icon_size // 2 - 2)
            
            # Checkmark
            check_points = [
                (icon_rect.centerx - 10, icon_rect.centery),
                (icon_rect.centerx - 3, icon_rect.centery + 8),
                (icon_rect.centerx + 10, icon_rect.centery - 10)
            ]
            pygame.draw.lines(surface, (255, 215, 0), False, check_points, 4)
        else:
            # Draw lock
            pygame.draw.circle(surface, UI_BORDER, icon_rect.center, icon_size // 2, 2)
            lock_rect = pygame.Rect(icon_rect.centerx - 8, icon_rect.centery, 16, 12)
            pygame.draw.rect(surface, UI_BORDER, lock_rect, 2)
        
        # Text area
        text_x = x + 70
        
        # Name
        if achievement.hidden and not achievement.unlocked:
            name = "???"
        else:
            name = achievement.name
        
        name_text = self.font_small.render(name, True, WHITE if achievement.unlocked else UI_TEXT_DIM)
        surface.blit(name_text, (text_x, y + 10))
        
        # Description
        if achievement.hidden and not achievement.unlocked:
            desc = "Hidden achievement"
        else:
            desc = achievement.description
        
        desc_text = self.font_tiny.render(desc, True, UI_TEXT_DIM)
        surface.blit(desc_text, (text_x, y + 35))
        
        # Progress bar (if not unlocked)
        if not achievement.unlocked and not achievement.hidden:
            bar_width = 200
            bar_height = 8
            bar_x = text_x
            bar_y = y + 55
            
            # Background
            bar_bg = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
            pygame.draw.rect(surface, UI_BORDER, bar_bg, border_radius=4)
            
            # Fill
            progress_percent = achievement.get_progress_percent()
            fill_width = int((progress_percent / 100) * bar_width)
            if fill_width > 0:
                bar_fill = pygame.Rect(bar_x, bar_y, fill_width, bar_height)
                pygame.draw.rect(surface, UI_HIGHLIGHT, bar_fill, border_radius=4)
            
            # Text
            progress_text = self.font_tiny.render(
                f"{achievement.progress}/{achievement.goal} ({progress_percent}%)",
                True, UI_TEXT_DIM
            )
            surface.blit(progress_text, (bar_x + bar_width + 10, bar_y - 2))
    
    def change_category(self, direction):
        """Change selected category"""
        self.selected_category = (self.selected_category + direction) % len(self.categories)
        self.scroll_offset = 0
    
    def scroll(self, direction):
        """Scroll achievement list"""
        self.scroll_offset = max(0, self.scroll_offset + direction * 80)
