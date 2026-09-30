import math

import pygame

from config.settings import SCIFI_BG, SCIFI_GRID, SCIFI_NODE, WHITE


class TextureManager:
    """Creates patterns and textures for game objects"""

    @staticmethod
    def draw_striped_rect(
        surface,
        rect,
        base_color,
        stripe_color,
        stripe_width=4,
        vertical=True,
        colorblind_mode=True,
    ):
        """Draw rectangle with stripes"""
        pygame.draw.rect(surface, base_color, rect)

        # Only draw patterns if colorblind mode is enabled
        if colorblind_mode:
            if vertical:
                for x in range(rect.left, rect.right, stripe_width * 2):
                    stripe_rect = pygame.Rect(x, rect.top, stripe_width, rect.height)
                    pygame.draw.rect(surface, stripe_color, stripe_rect)
            else:
                for y in range(rect.top, rect.bottom, stripe_width * 2):
                    stripe_rect = pygame.Rect(rect.left, y, rect.width, stripe_width)
                    pygame.draw.rect(surface, stripe_color, stripe_rect)

    @staticmethod
    def draw_checkered_rect(
        surface, rect, color1, color2, check_size=8, colorblind_mode=False
    ):
        if not colorblind_mode:
            # Just draw solid color
            pygame.draw.rect(surface, color1, rect)
            return

        """Draw rectangle with checkerboard pattern"""
        for y in range(rect.top, rect.bottom, check_size):
            for x in range(rect.left, rect.right, check_size):
                # Alternate colors in checkerboard pattern
                row = (y - rect.top) // check_size
                col = (x - rect.left) // check_size
                color = color1 if (row + col) % 2 == 0 else color2

                check_rect = pygame.Rect(
                    x,
                    y,
                    min(check_size, rect.right - x),
                    min(check_size, rect.bottom - y),
                )
                pygame.draw.rect(surface, color, check_rect)

    @staticmethod
    def draw_dotted_rect(surface, rect, base_color, dot_color, dot_size=2, spacing=6, colorblind_mode=False):
        """Draw rectangle with dot pattern"""
        pygame.draw.rect(surface, base_color, rect)

        if not colorblind_mode:
            return

        for y in range(rect.top + spacing // 2, rect.bottom, spacing):
            for x in range(rect.left + spacing // 2, rect.right, spacing):
                pygame.draw.circle(surface, dot_color, (x, y), dot_size)

    @staticmethod
    def draw_brick_wall(surface, rect, mortar_color, brick_color, colorblind_mode=False):
        """Draw brick wall pattern (already a distinct pattern, so colorblind_mode changes nothing)"""
        brick_height = 16
        brick_width = 32
        mortar_width = 2

        y = rect.top
        row = 0
        while y < rect.bottom:
            x = rect.left
            # Offset every other row for brick pattern
            if row % 2 == 1:
                x -= brick_width // 2

            while x < rect.right:
                brick_rect = pygame.Rect(x, y, brick_width, brick_height)
                # Clip to boundaries
                brick_rect = brick_rect.clip(rect)
                if brick_rect.width > 0 and brick_rect.height > 0:
                    pygame.draw.rect(surface, brick_color, brick_rect)
                    pygame.draw.rect(surface, mortar_color, brick_rect, mortar_width)

                x += brick_width + mortar_width

            y += brick_height + mortar_width
            row += 1

    @staticmethod
    def draw_diagonal_lines(
        surface,
        rect,
        base_color,
        line_color,
        spacing=8,
        line_width=2,
        colorblind_mode=True,
    ):
        """Draw diagonal line pattern"""
        pygame.draw.rect(surface, base_color, rect)

        if not colorblind_mode:
            return

        # Draw diagonal lines from top-left to bottom-right
        for offset in range(-rect.height, rect.width, spacing):
            start_x = rect.left + offset
            start_y = rect.top
            end_x = rect.left + offset + rect.height
            end_y = rect.bottom

            pygame.draw.line(
                surface, line_color, (start_x, start_y), (end_x, end_y), line_width
            )

    @staticmethod
    def draw_grid_rect(
        surface, rect, base_color, grid_color, grid_size=16, colorblind_mode=False
    ):
        """Draw rectangle with grid pattern"""
        pygame.draw.rect(surface, base_color, rect)

        if not colorblind_mode:
            return

        # Vertical lines
        for x in range(rect.left, rect.right, grid_size):
            pygame.draw.line(surface, grid_color, (x, rect.top), (x, rect.bottom), 1)

        # Horizontal lines
        for y in range(rect.top, rect.bottom, grid_size):
            pygame.draw.line(surface, grid_color, (rect.left, y), (rect.right, y), 1)


class BackgroundManager:
    """
    Themed parallax backgrounds.

    Each theme is a flat base color plus a few pre-rendered, tileable layers
    that are blitted at camera-dependent offsets (cheap: a few blits per
    frame). Layers are built once per screen size with a local RNG, so they
    never touch the global random module.
    """

    _cache = {}

    # --- helpers ---------------------------------------------------------

    @staticmethod
    def _layer(key, size, period, painter):
        """Cached transparent layer: `size` plus one `period`, for scrolling"""
        cache = BackgroundManager._cache
        if key not in cache:
            pw, ph = period
            surf = pygame.Surface((size[0] + pw, size[1] + ph))
            surf.fill((0, 0, 0))
            surf.set_colorkey((0, 0, 0))
            tile = pygame.Surface((pw, ph))
            tile.fill((0, 0, 0))
            painter(tile)
            for x in range(0, surf.get_width(), pw):
                for y in range(0, surf.get_height(), ph):
                    surf.blit(tile, (x, y))
            cache[key] = surf
        return cache[key]

    @staticmethod
    def _scroll(surface, layer, period, offset_x, offset_y):
        """Blit a tiled layer scrolled by the given offsets"""
        pw, ph = period
        surface.blit(layer, (-(int(offset_x) % pw), -(int(offset_y) % ph)))

    @staticmethod
    def _dots(seed, count, colors, sizes, outline=False):
        """Painter: random dots within the tile (wrapping at the edges)"""
        import random

        def paint(tile):
            rng = random.Random(seed)
            w, h = tile.get_size()
            for _ in range(count):
                x, y = rng.randrange(w), rng.randrange(h)
                size = rng.choice(sizes)
                color = rng.choice(colors)
                for dx in (-w, 0, w):
                    for dy in (-h, 0, h):
                        pygame.draw.circle(tile, color, (x + dx, y + dy), size, 1 if outline else 0)
        return paint

    # --- themes ----------------------------------------------------------

    @staticmethod
    def draw_scifi_background(surface, camera_x, camera_y, screen_width, screen_height):
        """Sci-fi tech background: grid and circuit nodes"""
        size = (screen_width, screen_height)

        def grid(tile):
            pygame.draw.line(tile, SCIFI_GRID, (0, 0), (0, 63))
            pygame.draw.line(tile, SCIFI_GRID, (0, 0), (63, 0))

        def nodes(tile):
            for cx, cy in ((0, 0), (128, 0), (0, 128), (128, 128)):
                pygame.draw.circle(tile, SCIFI_NODE, (cx, cy), 4, 1)
                pygame.draw.circle(tile, SCIFI_GRID, (cx, cy), 8, 1)

        surface.fill(SCIFI_BG)
        B = BackgroundManager
        B._scroll(surface, B._layer(("scifi_grid", size), size, (64, 64), grid), (64, 64),
                  camera_x // 4, camera_y // 4)
        B._scroll(surface, B._layer(("scifi_nodes", size), size, (128, 128), nodes), (128, 128),
                  camera_x // 2, camera_y // 2)

    @staticmethod
    def draw_nature_background(surface, camera_x, camera_y, screen_width, screen_height):
        """Forest: distant hills, tree trunks, drifting leaves"""
        size = (screen_width, screen_height)

        def hills(tile):
            w, h = tile.get_size()
            points = [(0, h)]
            for x in range(0, w + 1, 16):
                y = h - 150 - 60 * math.sin(x / w * 2 * math.pi) - 25 * math.sin(x / w * 6 * math.pi)
                points.append((x, int(y)))
            points.append((w, h))
            pygame.draw.polygon(tile, (30, 48, 34), points)

        def trunks(tile):
            h = tile.get_height()
            for x, width in ((40, 18), (190, 26), (330, 14)):
                pygame.draw.rect(tile, (38, 50, 36), (x, 0, width, h))
                pygame.draw.circle(tile, (40, 60, 42), (x + width // 2, 60), 70)

        surface.fill((26, 40, 30))
        B = BackgroundManager
        B._scroll(surface, B._layer(("nature_hills", size), size, size, hills), size, camera_x // 8, 0)
        B._scroll(surface, B._layer(("nature_trunks", size), size, (420, screen_height), trunks),
                  (420, screen_height), camera_x // 4, 0)
        leaves = B._dots(42, 40, [(58, 82, 58), (70, 92, 60)], [2, 3])
        B._scroll(surface, B._layer(("nature_leaves", size), size, (240, 240), leaves), (240, 240),
                  camera_x // 2, camera_y // 2 - pygame.time.get_ticks() // 60)

    @staticmethod
    def draw_space_background(surface, camera_x, camera_y, screen_width, screen_height):
        """Space: nebula clouds and two star fields"""
        size = (screen_width, screen_height)

        def nebula(tile):
            # A couple of faint, large clouds on a wide tile (so it rarely repeats)
            for x, y, r in ((260, 220, 150), (940, 520, 190)):
                pygame.draw.circle(tile, (17, 14, 30), (x, y), r)
                pygame.draw.circle(tile, (21, 16, 36), (x + 30, y - 20), int(r * 0.6))

        surface.fill((10, 10, 20))
        B = BackgroundManager
        B._scroll(surface, B._layer(("space_nebula", size), size, (1200, 800), nebula), (1200, 800),
                  camera_x // 10, camera_y // 10)
        far = B._dots(123, 60, [(120, 120, 150), (100, 100, 135)], [1, 1, 2])
        B._scroll(surface, B._layer(("space_far", size), size, (256, 256), far), (256, 256),
                  camera_x // 4, camera_y // 4)
        near = B._dots(456, 18, [(170, 170, 195)], [2])
        B._scroll(surface, B._layer(("space_near", size), size, (256, 256), near), (256, 256),
                  camera_x // 2, camera_y // 2)

    @staticmethod
    def draw_underground_background(surface, camera_x, camera_y, screen_width, screen_height):
        """Caves: rock strata, rock specks, stalactites"""
        size = (screen_width, screen_height)

        def strata(tile):
            w = tile.get_width()
            points = [(x, int(20 + 8 * math.sin(x / w * 4 * math.pi))) for x in range(0, w + 1, 20)]
            pygame.draw.lines(tile, (46, 34, 26), False, points, 2)

        def stalactites(tile):
            for x, length in ((20, 60), (80, 35), (120, 80)):
                pygame.draw.polygon(tile, (24, 18, 14), [(x - 18, 0), (x + 18, 0), (x, length)])

        surface.fill((30, 22, 18))
        B = BackgroundManager
        B._scroll(surface, B._layer(("cave_strata", size), size, (400, 40), strata), (400, 40),
                  camera_x // 5, camera_y // 5)
        rocks = B._dots(789, 30, [(52, 40, 32), (58, 44, 34)], [2, 3, 4])
        B._scroll(surface, B._layer(("cave_rocks", size), size, (240, 240), rocks), (240, 240),
                  camera_x // 3, camera_y // 3)
        B._scroll(surface, B._layer(("cave_stalactites", size), size, (150, screen_height), stalactites),
                  (150, screen_height), camera_x // 2, 0)

    @staticmethod
    def draw_underwater_background(surface, camera_x, camera_y, screen_width, screen_height):
        """Underwater: light rays, caustics, rising bubbles"""
        size = (screen_width, screen_height)

        def rays(tile):
            h = tile.get_height()
            pygame.draw.polygon(tile, (22, 42, 64), [(40, 0), (70, h), (95, h), (62, 0)])

        def caustics(tile):
            pygame.draw.circle(tile, (26, 46, 72), (50, 50), 25, 1)

        surface.fill((14, 28, 46))
        B = BackgroundManager
        ticks = pygame.time.get_ticks()
        B._scroll(surface, B._layer(("water_rays", size), size, (250, screen_height), rays),
                  (250, screen_height), camera_x // 8, 0)
        B._scroll(surface, B._layer(("water_caustics", size), size, (100, 100), caustics), (100, 100),
                  camera_x // 3 + int(12 * math.sin(ticks / 700)), camera_y // 3 + ticks // 60)
        bubbles = B._dots(101112, 12, [(46, 74, 110)], [3, 4, 5], outline=True)
        B._scroll(surface, B._layer(("water_bubbles", size), size, (256, 256), bubbles), (256, 256),
                  camera_x // 2, camera_y // 2 + ticks // 20)
