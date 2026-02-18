"""
Shop UI System
Browse and purchase weapons, upgrades, and stat improvements
"""

import pygame

from config.layout_manager import get_screen_size, get_font_size
from config.settings import (BLACK, UI_BG, UI_BORDER, UI_HIGHLIGHT, UI_TEXT,
                             UI_TEXT_DIM, WHITE, YELLOW, GREEN, RED, ORANGE, CYAN)
from config.weapon_catalog import (WEAPON_CATALOG, STATS_CATALOG, 
                                   get_all_weapon_ids, get_weapon_info,
                                   get_weapon_power_upgrade, get_weapon_speed_upgrade)
from ui.components import Screen


class Shop:
    """Shop interface for purchasing weapons and upgrades"""
    
    def __init__(self):
        """Initialize shop"""
        # Get scaled fonts
        large_size = get_font_size('large') or 52
        medium_size = get_font_size('medium') or 32
        small_size = get_font_size('small') or 22
        tiny_size = get_font_size('tiny') or 18
        
        self.font_large = pygame.font.Font(None, large_size)
        self.font_medium = pygame.font.Font(None, medium_size)
        self.font_small = pygame.font.Font(None, small_size)
        self.font_tiny = pygame.font.Font(None, tiny_size)
        
        # Tabs
        self.tabs = ['WEAPONS', 'STATS']
        self.current_tab = 0  # 0 = WEAPONS, 1 = STATS
        
        # Selection
        self.selected_weapon = 0
        self.selected_upgrade = 'power'  # 'power' or 'speed' or 'unlock'
        self.selected_stat_category = 0  # 0 = health, 1 = lives, 2 = consumables
        self.selected_stat_item = 0
        
        # Weapon list
        self.weapon_ids = get_all_weapon_ids()
    
    def draw(self, surface, player_data, mouse_pos=None):
        """
        Draw shop interface
        
        Args:
            surface: Pygame surface
            player_data: Dict with 'coins', 'weapons', 'max_hp', 'max_lives'
            mouse_pos: Mouse position for hover effects
        """
        screen_width, screen_height = get_screen_size()
        
        # Background
        surface.fill(BLACK)
        
        # Title
        title = self.font_large.render("UPGRADE SHOP", True, UI_HIGHLIGHT)
        surface.blit(title, (screen_width // 2 - title.get_width() // 2, 40))
        
        # Coin display
        coin_text = self.font_medium.render(
            f"Coins: {player_data.get('coins', 0)}", 
            True, 
            YELLOW
        )
        surface.blit(coin_text, (screen_width - coin_text.get_width() - 40, 40))
        
        # Tabs
        self._draw_tabs(surface, screen_width)
        
        # Content based on current tab
        if self.current_tab == 0:
            self._draw_weapons_tab(surface, player_data, mouse_pos)
        else:
            self._draw_stats_tab(surface, player_data, mouse_pos)
        
        # Controls hint
        hint_text = "TAB: Switch Tab  |  UP/DOWN: Navigate  |  LEFT/RIGHT: Select Upgrade  |  ENTER: Buy  |  ESC: Exit"
        hint = self.font_tiny.render(hint_text, True, UI_TEXT_DIM)
        surface.blit(hint, (screen_width // 2 - hint.get_width() // 2, screen_height - 40))
    
    def _draw_tabs(self, surface, screen_width):
        """Draw tab buttons"""
        tab_width = 200
        tab_height = 50
        tab_y = 120
        spacing = 20
        
        total_width = len(self.tabs) * tab_width + (len(self.tabs) - 1) * spacing
        start_x = screen_width // 2 - total_width // 2
        
        for i, tab_name in enumerate(self.tabs):
            tab_x = start_x + i * (tab_width + spacing)
            is_active = i == self.current_tab
            
            # Tab background
            color = UI_HIGHLIGHT if is_active else UI_BG
            border = WHITE if is_active else UI_BORDER
            
            tab_rect = pygame.Rect(tab_x, tab_y, tab_width, tab_height)
            pygame.draw.rect(surface, color, tab_rect, border_radius=5)
            pygame.draw.rect(surface, border, tab_rect, 2, border_radius=5)
            
            # Tab text
            text_color = BLACK if is_active else UI_TEXT
            text = self.font_medium.render(tab_name, True, text_color)
            surface.blit(
                text,
                (tab_x + tab_width // 2 - text.get_width() // 2, tab_y + 12)
            )
    
    def _draw_weapons_tab(self, surface, player_data, mouse_pos):
        """Draw weapons list with upgrades"""
        screen_width, screen_height = get_screen_size()
        
        # Starting position for weapon list
        start_y = 200
        item_height = 110
        max_visible = 4
        
        # Get player weapons data
        weapons_data = player_data.get('weapons', {})
        
        # Draw visible weapons
        for i, weapon_id in enumerate(self.weapon_ids):
            if i >= max_visible:
                break
            
            y = start_y + i * item_height
            is_selected = i == self.selected_weapon
            
            # Get weapon state
            weapon_state = weapons_data.get(weapon_id, {
                'unlocked': weapon_id == 'standard',
                'power_level': 1 if weapon_id == 'standard' else 0,
                'speed_level': 1 if weapon_id == 'standard' else 0
            })
            
            self._draw_weapon_item(
                surface,
                weapon_id,
                weapon_state,
                player_data.get('coins', 0),
                y,
                is_selected
            )
    
    def _draw_weapon_item(self, surface, weapon_id, weapon_state, player_coins, y, is_selected):
        """Draw individual weapon item"""
        screen_width, _ = get_screen_size()
        x = 80
        width = screen_width - 160
        height = 100
        
        # Get weapon info
        weapon_info = get_weapon_info(weapon_id)
        unlocked = weapon_state.get('unlocked', False)
        power_level = weapon_state.get('power_level', 0)
        speed_level = weapon_state.get('speed_level', 0)
        
        # Background
        bg_color = UI_HIGHLIGHT if is_selected else UI_BG
        border_color = WHITE if is_selected else UI_BORDER
        
        item_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(surface, bg_color, item_rect, border_radius=8)
        pygame.draw.rect(surface, border_color, item_rect, 2, border_radius=8)
        
        # Weapon name
        name_text = self.font_medium.render(weapon_info['name'], True, UI_TEXT)
        surface.blit(name_text, (x + 20, y + 10))
        
        # Description
        desc_text = self.font_tiny.render(weapon_info['description'], True, UI_TEXT_DIM)
        surface.blit(desc_text, (x + 20, y + 40))
        
        if not unlocked:
            # Show unlock cost
            cost = weapon_info['unlock_cost']
            can_afford = player_coins >= cost
            color = GREEN if can_afford else RED
            
            unlock_text = self.font_small.render(
                f"UNLOCK: {cost} coins",
                True,
                color
            )
            surface.blit(unlock_text, (x + 20, y + 65))
            
            if is_selected and self.selected_upgrade == 'unlock':
                # Highlight unlock option
                pygame.draw.rect(
                    surface,
                    YELLOW,
                    (x + 15, y + 62, unlock_text.get_width() + 10, 25),
                    2
                )
        else:
            # Show upgrade options
            upgrade_y = y + 65
            
            # Power upgrade
            power_cost = self._get_upgrade_cost(weapon_id, 'power', power_level)
            if power_cost is not None:
                can_afford = player_coins >= power_cost
                color = GREEN if can_afford else UI_TEXT_DIM
                power_text = f"Power Lvl {power_level + 1}: {power_cost} coins"
            else:
                color = CYAN
                power_text = f"Power: MAX (Lvl {power_level})"
            
            power_render = self.font_small.render(power_text, True, color)
            surface.blit(power_render, (x + 30, upgrade_y))
            
            if is_selected and self.selected_upgrade == 'power' and power_cost is not None:
                pygame.draw.rect(
                    surface,
                    YELLOW,
                    (x + 25, upgrade_y - 2, power_render.get_width() + 10, 22),
                    2
                )
            
            # Speed upgrade
            speed_y = upgrade_y + 25
            speed_cost = self._get_upgrade_cost(weapon_id, 'speed', speed_level)
            if speed_cost is not None:
                can_afford = player_coins >= speed_cost
                color = GREEN if can_afford else UI_TEXT_DIM
                speed_text = f"Speed Lvl {speed_level + 1}: {speed_cost} coins"
            else:
                color = CYAN
                speed_text = f"Speed: MAX (Lvl {speed_level})"
            
            speed_render = self.font_small.render(speed_text, True, color)
            surface.blit(speed_render, (x + 30, speed_y))
            
            if is_selected and self.selected_upgrade == 'speed' and speed_cost is not None:
                pygame.draw.rect(
                    surface,
                    YELLOW,
                    (x + 25, speed_y - 2, speed_render.get_width() + 10, 22),
                    2
                )
    
    def _get_upgrade_cost(self, weapon_id, upgrade_type, current_level):
        """Get cost of next upgrade"""
        weapon_info = get_weapon_info(weapon_id)
        
        if upgrade_type == 'power':
            if current_level < weapon_info['power_max']:
                next_upgrade = get_weapon_power_upgrade(weapon_id, current_level + 1)
                return next_upgrade['cost']
        elif upgrade_type == 'speed':
            if current_level < weapon_info['speed_max']:
                next_upgrade = get_weapon_speed_upgrade(weapon_id, current_level + 1)
                return next_upgrade['cost']
        
        return None  # Already maxed
    
    def _draw_stats_tab(self, surface, player_data, mouse_pos):
        """Draw stats upgrades tab"""
        screen_width, screen_height = get_screen_size()
        
        start_y = 200
        section_spacing = 200
        
        # Current stats
        current_max_hp = player_data.get('max_hp', 100)
        current_max_lives = player_data.get('max_lives', 3)
        player_coins = player_data.get('coins', 0)
        
        # HEALTH SECTION
        self._draw_stat_section(
            surface,
            "HEALTH UPGRADES",
            f"Current Max HP: {current_max_hp}",
            STATS_CATALOG['health'],
            start_y,
            player_coins,
            self.selected_stat_category == 0
        )
        
        # LIVES SECTION
        self._draw_stat_section(
            surface,
            "EXTRA LIVES",
            f"Current Max Lives: {current_max_lives}",
            STATS_CATALOG['lives'],
            start_y + section_spacing,
            player_coins,
            self.selected_stat_category == 1
        )
        
        # CONSUMABLES SECTION
        cons_y = start_y + section_spacing * 2
        cons_title = self.font_medium.render("CONSUMABLES", True, UI_HIGHLIGHT)
        surface.blit(cons_title, (150, cons_y))
        
        # Health potion
        for i, item in enumerate(STATS_CATALOG['consumables']):
            item_y = cons_y + 50 + i * 40
            can_afford = player_coins >= item['cost']
            color = GREEN if can_afford else UI_TEXT_DIM
            
            text = f"{item['name']} (+{item['hp_restore']} HP) - {item['cost']} coins"
            render = self.font_small.render(text, True, color)
            surface.blit(render, (170, item_y))
            
            if self.selected_stat_category == 2 and i == self.selected_stat_item:
                pygame.draw.rect(
                    surface,
                    YELLOW,
                    (165, item_y - 2, render.get_width() + 10, 25),
                    2
                )
    
    def _draw_stat_section(self, surface, title, current_text, items, y, player_coins, is_selected):
        """Draw a stat section (health or lives)"""
        # Title
        title_render = self.font_medium.render(title, True, UI_HIGHLIGHT)
        surface.blit(title_render, (150, y))
        
        # Current value
        current_render = self.font_small.render(current_text, True, UI_TEXT)
        surface.blit(current_render, (150, y + 40))
        
        # Items
        for i, item in enumerate(items):
            item_y = y + 80 + i * 40
            can_afford = player_coins >= item['cost']
            color = GREEN if can_afford else UI_TEXT_DIM
            
            text = f"{item['name']} - {item['cost']} coins"
            render = self.font_small.render(text, True, color)
            surface.blit(render, (170, item_y))
            
            # Highlight if selected
            if is_selected and i == self.selected_stat_item:
                pygame.draw.rect(
                    surface,
                    YELLOW,
                    (165, item_y - 2, render.get_width() + 10, 25),
                    2
                )
    
    # Navigation methods
    def switch_tab(self):
        """Switch between WEAPONS and STATS tabs"""
        self.current_tab = (self.current_tab + 1) % len(self.tabs)
        self.selected_stat_category = 0
        self.selected_stat_item = 0
    
    def navigate_up(self):
        """Navigate selection up"""
        if self.current_tab == 0:  # WEAPONS tab
            self.selected_weapon = max(0, self.selected_weapon - 1)
        else:  # STATS tab
            self.selected_stat_category = max(0, self.selected_stat_category - 1)
    
    def navigate_down(self):
        """Navigate selection down"""
        if self.current_tab == 0:  # WEAPONS tab
            self.selected_weapon = min(len(self.weapon_ids) - 1, self.selected_weapon + 1)
        else:  # STATS tab
            self.selected_stat_category = min(2, self.selected_stat_category + 1)
    
    def navigate_left(self):
        """Navigate upgrade type left (weapons only)"""
        if self.current_tab == 0:
            options = ['unlock', 'power', 'speed']
            current_idx = options.index(self.selected_upgrade)
            self.selected_upgrade = options[max(0, current_idx - 1)]
    
    def navigate_right(self):
        """Navigate upgrade type right (weapons only)"""
        if self.current_tab == 0:
            options = ['unlock', 'power', 'speed']
            current_idx = options.index(self.selected_upgrade)
            self.selected_upgrade = options[min(len(options) - 1, current_idx + 1)]
    
    def get_selected_purchase(self, player_data):
        """
        Get currently selected purchase option
        
        Returns:
            Dict with 'type', 'item', 'cost', or None if nothing selected
        """
        if self.current_tab == 0:  # WEAPONS tab
            weapon_id = self.weapon_ids[self.selected_weapon]
            weapons_data = player_data.get('weapons', {})
            weapon_state = weapons_data.get(weapon_id, {'unlocked': weapon_id == 'standard'})
            
            if not weapon_state.get('unlocked', False) and self.selected_upgrade == 'unlock':
                return {
                    'type': 'weapon_unlock',
                    'weapon_id': weapon_id,
                    'cost': get_weapon_info(weapon_id)['unlock_cost']
                }
            elif weapon_state.get('unlocked', False):
                if self.selected_upgrade == 'power':
                    power_level = weapon_state.get('power_level', 0)
                    cost = self._get_upgrade_cost(weapon_id, 'power', power_level)
                    if cost is not None:
                        return {
                            'type': 'weapon_power',
                            'weapon_id': weapon_id,
                            'cost': cost
                        }
                elif self.selected_upgrade == 'speed':
                    speed_level = weapon_state.get('speed_level', 0)
                    cost = self._get_upgrade_cost(weapon_id, 'speed', speed_level)
                    if cost is not None:
                        return {
                            'type': 'weapon_speed',
                            'weapon_id': weapon_id,
                            'cost': cost
                        }
        
        return None
