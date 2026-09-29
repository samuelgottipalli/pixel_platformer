"""
Shop UI System
Browse and purchase weapons, upgrades, and stat improvements
"""

import pygame

from config.layout_manager import get_screen_size, get_font_size
from config.settings import (UI_SELECTED_BG, BLACK, UI_BG, UI_BORDER, UI_HIGHLIGHT, UI_TEXT,
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

        # Clickable areas recorded while drawing: (rect, action). Clicks are
        # tested against exactly what was drawn last frame.
        self._targets = []

    def draw(self, surface, player_data, mouse_pos=None):
        """
        Draw shop interface

        Args:
            surface: Pygame surface
            player_data: Dict with 'coins', 'weapons', 'max_hp', 'max_lives'
            mouse_pos: Mouse position for hover effects
        """
        screen_width, screen_height = get_screen_size()
        self._targets = []

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
        if self.current_tab == 0:
            hint_text = "Click a price to buy  |  TAB: Tab  |  UP/DOWN: Weapon  |  LEFT/RIGHT: Power/Speed  |  ENTER: Buy  |  ESC: Exit"
        else:
            hint_text = "Click a price to buy  |  TAB: Tab  |  UP/DOWN: Section  |  ENTER: Buy next upgrade  |  ESC: Exit"
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
            color = UI_SELECTED_BG if is_active else UI_BG
            border = UI_HIGHLIGHT if is_active else UI_BORDER

            tab_rect = pygame.Rect(tab_x, tab_y, tab_width, tab_height)
            self._targets.append((tab_rect, {'tab': i}))
            pygame.draw.rect(surface, color, tab_rect, border_radius=5)
            pygame.draw.rect(surface, border, tab_rect, 2, border_radius=5)

            # Tab text
            text_color = UI_HIGHLIGHT if is_active else UI_TEXT_DIM
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

        # Draw a window of weapons that scrolls to keep the selection visible
        first = max(0, min(self.selected_weapon - max_visible + 1, len(self.weapon_ids) - max_visible))
        for i, weapon_id in enumerate(self.weapon_ids):
            if not first <= i < first + max_visible:
                continue

            y = start_y + (i - first) * item_height
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
                is_selected,
                index=i,
            )

    def _draw_weapon_item(self, surface, weapon_id, weapon_state, player_coins, y, is_selected, index=0):
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
        # Selected card: thick highlight border on the dark card (keeps text readable)
        border_color = UI_HIGHLIGHT if is_selected else UI_BORDER
        border_width = 4 if is_selected else 2

        item_rect = pygame.Rect(x, y, width, height)
        self._targets.append((item_rect, {'weapon': index}))
        pygame.draw.rect(surface, UI_BG, item_rect, border_radius=8)
        pygame.draw.rect(surface, border_color, item_rect, border_width, border_radius=8)

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
            self._targets.append((
                pygame.Rect(x + 15, y + 60, unlock_text.get_width() + 10, 28),
                {'weapon': index, 'upgrade': 'unlock', 'buy': True},
            ))

            if is_selected:  # Enter unlocks a locked weapon
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
            self._targets.append((
                pygame.Rect(x + 25, upgrade_y - 4, power_render.get_width() + 10, 28),
                {'weapon': index, 'upgrade': 'power', 'buy': power_cost is not None},
            ))

            if is_selected and self.selected_upgrade == 'power' and power_cost is not None:
                pygame.draw.rect(
                    surface,
                    YELLOW,
                    (x + 25, upgrade_y - 2, power_render.get_width() + 10, 22),
                    2
                )

            # Speed upgrade (same line as Power, to its right)
            speed_y = upgrade_y
            speed_x = x + 30 + 340
            speed_cost = self._get_upgrade_cost(weapon_id, 'speed', speed_level)
            if speed_cost is not None:
                can_afford = player_coins >= speed_cost
                color = GREEN if can_afford else UI_TEXT_DIM
                speed_text = f"Speed Lvl {speed_level + 1}: {speed_cost} coins"
            else:
                color = CYAN
                speed_text = f"Speed: MAX (Lvl {speed_level})"

            speed_render = self.font_small.render(speed_text, True, color)
            surface.blit(speed_render, (speed_x, speed_y))
            self._targets.append((
                pygame.Rect(speed_x - 5, speed_y - 4, speed_render.get_width() + 10, 28),
                {'weapon': index, 'upgrade': 'speed', 'buy': speed_cost is not None},
            ))

            if is_selected and self.selected_upgrade == 'speed' and speed_cost is not None:
                pygame.draw.rect(
                    surface,
                    YELLOW,
                    (speed_x - 5, speed_y - 2, speed_render.get_width() + 10, 22),
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
        """Draw stats upgrades tab: health tiers, extra lives, consumables"""
        start_y = 200
        section_spacing = 190
        player_coins = player_data.get('coins', 0)
        upgrades = player_data.get('upgrades', {})

        self._drawing_category = 0
        self._draw_stat_section(
            surface,
            "HEALTH UPGRADES",
            f"Max HP: {player_data.get('max_hp', 100)}",
            STATS_CATALOG['health'],
            upgrades.get('health', 0),
            start_y,
            player_coins,
            self.selected_stat_category == 0,
        )
        self._drawing_category = 1
        self._draw_stat_section(
            surface,
            "EXTRA LIVES",
            f"Lives: {player_data.get('max_lives', 3)}",
            STATS_CATALOG['lives'],
            upgrades.get('lives', 0),
            start_y + section_spacing,
            player_coins,
            self.selected_stat_category == 1,
        )

        # CONSUMABLES SECTION
        cons_y = start_y + section_spacing * 2
        cons_title = self.font_medium.render("CONSUMABLES", True, UI_HIGHLIGHT)
        surface.blit(cons_title, (150, cons_y))
        hp_text = self.font_small.render(
            f"HP: {player_data.get('health', 100)}/{player_data.get('max_hp', 100)}", True, UI_TEXT
        )
        surface.blit(hp_text, (150, cons_y + 36))
        for i, item in enumerate(STATS_CATALOG['consumables']):
            item_y = cons_y + 66 + i * 34
            color = GREEN if player_coins >= item['cost'] else RED
            text = f"{item['name']} (+{item['hp_restore']} HP) - {item['cost']} coins"
            render = self.font_small.render(text, True, color)
            surface.blit(render, (170, item_y))
            self._targets.append((
                pygame.Rect(165, item_y - 4, render.get_width() + 10, 30),
                {'category': 2, 'item': i, 'buy': True},
            ))
            if self.selected_stat_category == 2 and i == self.selected_stat_item:
                pygame.draw.rect(surface, YELLOW, (165, item_y - 2, render.get_width() + 10, 25), 2)

    def _draw_stat_section(self, surface, title, current_text, items, owned, y, player_coins,
                           is_selected):
        """
        Draw a tiered stat section. Tiers are bought in order: the first
        `owned` tiers are OWNED, the next one is for sale, the rest are locked.
        """
        title_render = self.font_medium.render(title, True, UI_HIGHLIGHT)
        surface.blit(title_render, (150, y))
        current_render = self.font_small.render(current_text, True, UI_TEXT)
        surface.blit(current_render, (150 + title_render.get_width() + 30, y + 6))

        for i, item in enumerate(items):
            item_y = y + 40 + i * 34
            if i < owned:
                text, color = f"{item['name']} - OWNED", CYAN
            elif i == owned:
                text = f"{item['name']} - {item['cost']} coins"
                color = GREEN if player_coins >= item['cost'] else RED
            else:
                text, color = f"{item['name']} - {item['cost']} coins (buy previous first)", UI_TEXT_DIM
            render = self.font_small.render(text, True, color)
            surface.blit(render, (170, item_y))
            if i == owned:  # only the next tier is for sale
                self._targets.append((
                    pygame.Rect(165, item_y - 4, render.get_width() + 10, 30),
                    {'category': self._drawing_category, 'buy': True},
                ))

            if is_selected and i == owned:
                pygame.draw.rect(surface, YELLOW, (165, item_y - 2, render.get_width() + 10, 25), 2)

        if owned >= len(items):
            maxed = self.font_small.render("MAXED", True, CYAN)
            surface.blit(maxed, (170 + 330, y + 40))

    def click(self, pos):
        """
        Handle a mouse click. Selects whatever was clicked and returns True
        if it was a price (the caller then attempts the purchase).
        """
        hit = None
        for rect, action in self._targets:
            if rect.collidepoint(pos):
                hit = action  # later targets are drawn on top (more specific)
        if hit is None:
            return False
        if 'tab' in hit:
            if hit['tab'] != self.current_tab:
                self.switch_tab()
            return False
        if 'weapon' in hit:
            self.selected_weapon = hit['weapon']
            if hit.get('upgrade') in ('power', 'speed'):
                self.selected_upgrade = hit['upgrade']
        if 'category' in hit:
            self.selected_stat_category = hit['category']
            self.selected_stat_item = hit.get('item', 0)
        return hit.get('buy', False)

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
            self.selected_upgrade = 'power'

    def navigate_right(self):
        """Navigate upgrade type right (weapons only)"""
        if self.current_tab == 0:
            self.selected_upgrade = 'speed'

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

            if not weapon_state.get('unlocked', False):
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

        # STATS tab: health/lives sell their next tier; consumables sell the potion
        upgrades = player_data.get('upgrades', {})
        if self.selected_stat_category in (0, 1):
            stat = 'health' if self.selected_stat_category == 0 else 'lives'
            tier = upgrades.get(stat, 0)
            tiers = STATS_CATALOG[stat]
            if tier >= len(tiers):
                return None  # Maxed
            return {'type': f'stat_{stat}', 'tier': tier, 'item': tiers[tier],
                    'cost': tiers[tier]['cost'], 'name': tiers[tier]['name']}

        item = STATS_CATALOG['consumables'][self.selected_stat_item]
        return {'type': 'consumable', 'item': item, 'cost': item['cost'], 'name': item['name']}
