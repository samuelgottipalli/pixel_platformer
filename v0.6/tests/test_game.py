"""
Headless end-to-end tests for the game.

Run from the v0.6 folder:  python -m unittest discover tests -v

Each test drives a real Game instance (dummy video/audio drivers) inside a
throwaway copy of the project, so your own data/ saves and profiles are never
touched. Audio assets are not copied; the audio manager skips missing files.
"""

import json
import os
import shutil
import sys
import tempfile
import unittest

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK_DIR = None

import pygame  # noqa: E402

# Keyboard state is faked: tests put keys in PRESSED for "held" input
PRESSED = set()


class _Keys:
    def __getitem__(self, key):
        return key in PRESSED


pygame.key.get_pressed = lambda: _Keys()


def setUpModule():
    global WORK_DIR, Game, GameState, Projectile, ExplosiveProjectile
    global ProfileManager, SaveManager, Key
    WORK_DIR = tempfile.mkdtemp(prefix="platformer_test_")
    shutil.copytree(
        PROJECT_DIR,
        WORK_DIR,
        dirs_exist_ok=True,
        ignore=shutil.ignore_patterns("assets", "data", "tests", "__pycache__", "*.ipynb"),
    )
    os.chdir(WORK_DIR)
    sys.path.insert(0, WORK_DIR)
    sys.stdout.reconfigure(errors="replace")

    from core.game import Game
    from utils.enums import GameState
    from entities.projectile import Projectile
    from entities.explosive_projectile import ExplosiveProjectile
    from save_system.profile_manager import ProfileManager
    from save_system.save_manager import SaveManager
    from objects.collectibles import Key


def tearDownModule():
    os.chdir(PROJECT_DIR)
    pygame.quit()
    shutil.rmtree(WORK_DIR, ignore_errors=True)


def reset_data(profiles=None):
    """Fresh data/ folder with fixed 1280x720 windowed settings"""
    shutil.rmtree("data", ignore_errors=True)
    os.makedirs("data")
    settings = {
        "video": {"resolution_index": 0, "fullscreen": False, "vsync": True},
        "audio": {"music_enabled": False, "music_volume": 0,
                  "sfx_enabled": False, "sfx_volume": 0},
        "accessibility": {"colorblind_mode": False},
    }
    with open("data/settings.json", "w") as f:
        json.dump(settings, f)
    if profiles is not None:
        with open("data/profiles.json", "w") as f:
            json.dump(profiles, f)


def key(k, unicode=""):
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=k, unicode=unicode, mod=0, scancode=0))


def frames(game, n=1, hold=()):
    PRESSED.clear()
    PRESSED.update(hold)
    for _ in range(n):
        game._handle_events()
        game._update()
        game._draw()
    PRESSED.clear()


class GameTestCase(unittest.TestCase):
    def new_game(self, profiles=None):
        reset_data(profiles)
        game = Game()
        pygame.event.clear()  # Drop events queued by the previous test
        return game

    def playing_game(self, level=0):
        """Game with a fresh profile, in PLAYING state on the given level"""
        g = self.new_game()
        g.player_name = "tester"
        g._create_new_profile()
        g._load_selected_profile_to_menu()
        g.difficulty_selection = 1
        g._start_new_game()
        if level:
            g._load_level(level)
        return g

    @staticmethod
    def make_invincible(g):
        g.player.invincible = True
        g.player.invincible_timer = 10**6


class ProfileTests(GameTestCase):
    def test_boot_draws_profile_select(self):
        g = self.new_game()
        frames(g, 3)
        self.assertEqual(g.state, GameState.PROFILE_SELECT)

    def test_create_profile_with_keyboard(self):
        g = self.new_game()
        key(pygame.K_n)
        frames(g)
        for ch in "sam":
            key(ord(ch), ch)
        key(pygame.K_RETURN)
        frames(g, 2)
        self.assertEqual(g.state, GameState.MENU)
        self.assertEqual([p.name for p in ProfileManager.load_profiles()], ["sam"])

    def test_old_profile_format_is_migrated(self):
        old = [{"name": "old", "character": 2, "total_score": 50,
                "levels_completed": 3, "coins_collected": 40}]
        g = self.new_game(profiles=old)
        self.assertEqual(len(g.profiles), 1)
        p = g.profiles[0]
        self.assertEqual((p.name, p.character, p.total_coins_collected), ("old", 2, 40))
        ProfileManager.save_profiles(g.profiles)
        self.assertEqual(ProfileManager.load_profiles()[0].name, "old")

    def test_unreadable_profiles_are_backed_up(self):
        reset_data()
        with open("data/profiles.json", "w") as f:
            f.write("{not json")
        self.assertEqual(ProfileManager.load_profiles(), [])
        self.assertTrue(os.path.exists("data/profiles.json.bak"))


class MenuTests(GameTestCase):
    def test_all_menu_screens_draw(self):
        g = self.playing_game()
        for state in (GameState.MENU, GameState.OPTIONS, GameState.CONTROLS,
                      GameState.SETTINGS, GameState.CREDITS, GameState.LEVEL_MAP,
                      GameState.ACHIEVEMENTS, GameState.DIFFICULTY_SELECT):
            g.state = state
            frames(g, 2)

    def test_new_game_from_menu_with_keyboard(self):
        g = self.new_game()
        g.player_name = "kb"
        g._create_new_profile()
        g._load_selected_profile_to_menu()
        key(pygame.K_RETURN)  # New Game
        frames(g)
        self.assertEqual(g.state, GameState.DIFFICULTY_SELECT)
        key(pygame.K_RETURN)  # Normal
        frames(g, 2)
        self.assertEqual(g.state, GameState.PLAYING)
        self.assertGreater(g.current_profile.max_lives, 0)

    def test_resolution_change_redraws(self):
        g = self.playing_game()
        from config.settings import update_screen_size
        g.settings.set_resolution(1)
        g.screen = g.settings.apply_video_settings(g.screen)
        update_screen_size(g.settings.width, g.settings.height)
        g.menu.refresh_buttons()
        g.state = GameState.MENU
        frames(g, 2)


class LayoutTests(GameTestCase):
    def tearDown(self):
        from config.settings import update_screen_size
        update_screen_size(1280, 720)

    def test_unknown_resolution_gets_its_own_screen_size(self):
        from config.layout_manager import LayoutManager, get_screen_size
        from config.settings import update_screen_size
        update_screen_size(1024, 768)
        self.assertEqual(get_screen_size(), (1024, 768))
        self.assertAlmostEqual(LayoutManager.get_scale_factor(), 768 / 720)

    def test_physics_scale_with_resolution_in_every_layout(self):
        """Jumps must be the same height relative to level geometry at every resolution"""
        base = json.load(open("config/layouts/layout_1280x720.json"))
        for name in os.listdir("config/layouts"):
            layout = json.load(open(os.path.join("config/layouts", name)))
            scale = layout["resolution"]["scale_factor"]
            for key, value in base["physics"].items():
                with self.subTest(layout=name, physics=key):
                    self.assertAlmostEqual(layout["physics"][key], value * scale, places=2)


class GameplayTests(GameTestCase):
    def test_move_jump_shoot_melee(self):
        g = self.playing_game()
        start_x = g.player.x
        frames(g, 60, hold={pygame.K_RIGHT})
        self.assertGreater(g.player.x, start_x)
        frames(g, 5, hold={pygame.K_SPACE})
        frames(g, 30, hold={pygame.K_z})
        frames(g, 10, hold={pygame.K_x})

    def test_every_weapon_fires(self):
        g = self.playing_game(level=1)
        self.make_invincible(g)
        weapons = [("standard", pygame.K_1), ("dual_back", pygame.K_2), ("spread", pygame.K_3),
                   ("dual_front", pygame.K_4), ("explosive", pygame.K_5)]
        for wid, _ in weapons[1:]:
            g.player.unlock_weapon(wid)
        for wid, k in weapons:
            frames(g, 1, hold={k})
            self.assertEqual(g.player.current_weapon_id, wid)
            frames(g, 150, hold={pygame.K_z})

    def test_spread_shots_hit_enemies_not_player(self):
        g = self.playing_game(level=1)
        g.player.unlock_weapon("spread")
        g.player.switch_weapon("spread")
        enemy = g.level.enemies[0]
        # Face left: leftward shots spawn overlapping the player
        g.player.x, g.player.y = enemy.x + enemy.width + 2, enemy.y
        g.player.direction = -1
        health = g.player.health
        g.projectiles = g.player.shoot()
        self.assertTrue(g.projectiles)
        g._update_projectiles()
        self.assertEqual(g.player.health, health)
        self.assertTrue(enemy.dead or enemy.health < enemy.max_health)

    def test_explosion_damages_enemies_in_radius(self):
        g = self.playing_game(level=1)
        enemy = g.level.enemies[0]
        bomb = ExplosiveProjectile(enemy.x + 10, enemy.y, 1, damage=1, radius=60)
        bomb.explode()
        g.projectiles = [bomb]
        health = enemy.health
        for _ in range(5):
            g._update_projectiles()
        self.assertEqual(enemy.health, health - 1, "blast should hit exactly once")

    def test_turret_shots_hurt_player(self):
        g = self.playing_game(level=1)
        shot = Projectile(g.player.x, g.player.y, 1, 0, 7, (255, 165, 0), angle=0, hostile=True)
        g.projectiles = [shot]
        health = g.player.health
        g._update_projectiles()
        self.assertEqual(g.player.health, health - 7)

    def test_touching_enemy_is_one_hit_then_brief_invulnerability(self):
        g = self.playing_game(level=1)
        enemy = next(e for e in g.level.enemies if e.type == "ground")
        g.player.dy = 0  # not stomping
        health = g.player.health
        for _ in range(30):  # stay in contact for half a second
            g.player.x, g.player.y = enemy.x, enemy.y
            g._handle_enemy_player_collision(enemy)
            g.player._update_timers()
        self.assertEqual(g.player.health, health - enemy.damage)
        self.assertEqual(g.total_damage_taken, enemy.damage)
        for _ in range(40):  # invulnerability wears off after 60 frames
            g.player._update_timers()
        g._handle_enemy_player_collision(enemy)
        self.assertEqual(g.player.health, health - 2 * enemy.damage)

    def test_spikes_hit_once_per_contact(self):
        g = self.playing_game()
        from objects.hazards import Hazard
        spike = Hazard(g.player.x, g.player.y, "spike")
        health = g.player.health
        for _ in range(20):
            g.player._check_hazard_collision([spike])
        self.assertEqual(g.player.health, health - 15)

    def test_collect_key(self):
        g = self.playing_game(level=1)
        g.level.keys.append(Key(g.player.x, g.player.y, (255, 0, 0)))
        g._update_collectibles()
        self.assertEqual(g.player.keys, [(255, 0, 0)])

    def test_respawn_at_level_spawn(self):
        g = self.playing_game(level=2)
        g.player.x, g.player.y = 5000, 100
        g.player.die()
        self.assertEqual((g.player.x, g.player.y), (g.level.spawn_x, g.level.spawn_y))

    def test_reloading_level_does_not_move_objects(self):
        g = self.playing_game()
        from config.layout_manager import LayoutManager
        original = LayoutManager.__dict__["scale_position"]
        LayoutManager.scale_position = classmethod(lambda cls, x, y: (int(x * 1.5), int(y * 1.5)))
        try:
            g._load_level(1)
            first = [(c.x, c.y) for c in g.level.coins]
            g._load_level(1)
            second = [(c.x, c.y) for c in g.level.coins]
        finally:
            LayoutManager.scale_position = original
        self.assertEqual(first, second)

    def test_every_level_loads_and_runs(self):
        g = self.playing_game()
        for i in range(len(g.levels)):
            g._load_level(i)
            g.state = GameState.PLAYING
            self.make_invincible(g)
            frames(g, 90, hold={pygame.K_RIGHT, pygame.K_z})


class PauseAndShopTests(GameTestCase):
    def pause(self, g):
        frames(g, 1, hold={pygame.K_p})
        self.assertEqual(g.state, GameState.PAUSED)
        frames(g)

    def test_pause_menu_keyboard_reaches_all_options_and_esc_resumes(self):
        g = self.playing_game()
        self.pause(g)
        for _ in range(3):
            key(pygame.K_DOWN)
        frames(g)
        self.assertEqual(g.pause_selection, 3)
        key(pygame.K_ESCAPE)
        frames(g)
        self.assertEqual(g.state, GameState.PLAYING)

    def test_shop_purchase_spends_player_coins(self):
        g = self.playing_game()
        self.pause(g)
        g.pause_selection = 0
        g._handle_pause_selection()
        self.assertEqual(g.state, GameState.SHOP)
        g.player.coins = 500
        g._refresh_shop_data()
        g.shop.selected_weapon = 1  # dual_back, costs 50
        g.shop.selected_upgrade = "unlock"
        key(pygame.K_RETURN)
        frames(g, 3)
        self.assertEqual(g.player.coins, 450)
        self.assertIsNotNone(g.player.weapons["dual_back"])
        self.assertEqual(g.shop_player_data["coins"], 450)

    def test_shop_rejects_unaffordable_purchase(self):
        g = self.playing_game()
        g.state = GameState.PAUSED
        g._enter_shop()
        g.player.coins = 10
        g.shop.selected_weapon = 4  # explosive, costs 200
        g.shop.selected_upgrade = "unlock"
        key(pygame.K_RETURN)
        frames(g)
        self.assertEqual(g.player.coins, 10)
        self.assertIsNone(g.player.weapons["explosive"])

    def stats_shop(self, coins=1000):
        g = self.playing_game()
        g.state = GameState.PAUSED
        g._enter_shop()
        g.player.coins = coins
        g._refresh_shop_data()
        key(pygame.K_TAB)
        frames(g)
        self.assertEqual(g.shop.current_tab, 1)
        return g

    def buy(self, g, category):
        g.shop.selected_stat_category = category
        key(pygame.K_RETURN)
        frames(g)

    def test_buy_health_tiers_in_order(self):
        g = self.stats_shop()
        self.buy(g, 0)
        self.assertEqual((g.player.max_health, g.player.coins), (125, 950))
        self.buy(g, 0)  # second tier costs 100
        self.assertEqual((g.player.max_health, g.player.coins), (150, 850))
        self.assertEqual(g.player.upgrades["health"], 2)
        self.assertEqual(g.shop_player_data["max_hp"], 150)

    def test_health_upgrades_max_out(self):
        g = self.stats_shop(coins=5000)
        for _ in range(6):
            self.buy(g, 0)
        self.assertEqual(g.player.max_health, 100 + 25 + 25 + 25 + 50)
        self.assertIsNone(g.shop.get_selected_purchase(g.shop_player_data))

    def test_buy_extra_life(self):
        g = self.stats_shop()
        lives = g.player.lives
        self.buy(g, 1)
        self.assertEqual((g.player.lives, g.player.coins), (lives + 1, 925))

    def test_health_potion(self):
        g = self.stats_shop()
        self.buy(g, 2)  # full health: refused, no charge
        self.assertEqual(g.player.coins, 1000)
        g.player.health = 30
        g._refresh_shop_data()
        self.buy(g, 2)
        self.assertEqual((g.player.health, g.player.coins), (80, 990))

    def test_stat_upgrades_survive_save_and_continue(self):
        g = self.stats_shop()
        self.buy(g, 0)
        g._save_game()
        g.player = None
        g.menu_selection = 1
        g._handle_menu_selection()
        self.assertEqual(g.player.max_health, 125)
        self.assertEqual(g.player.upgrades["health"], 1)

    def test_all_five_weapons_can_be_shown(self):
        g = self.stats_shop()
        key(pygame.K_TAB)
        for _ in range(4):
            key(pygame.K_DOWN)
        frames(g)
        self.assertEqual(g.shop.weapon_ids[g.shop.selected_weapon], "explosive")

    def test_esc_from_shop_returns_to_pause(self):
        g = self.playing_game()
        g.state = GameState.PAUSED
        g._enter_shop()
        key(pygame.K_ESCAPE)
        frames(g)
        self.assertEqual(g.state, GameState.PAUSED)


class SaveTests(GameTestCase):
    def test_save_return_to_menu_and_continue(self):
        g = self.playing_game(level=2)
        g.player.coins = 33
        g.state = GameState.PAUSED
        g.pause_selection = 2  # Save & Return to Menu
        g._handle_pause_selection()
        self.assertEqual(g.state, GameState.MENU)
        g.player = None
        g.menu_selection = 1  # Continue
        g._handle_menu_selection()
        self.assertEqual(g.state, GameState.PLAYING)
        self.assertEqual(g.current_level_index, 2)
        self.assertEqual(g.player.coins, 33)

    def test_continue_from_pre_weapon_system_save(self):
        g = self.playing_game()
        os.makedirs("data/saves", exist_ok=True)
        with open("data/saves/save_tester.json", "w") as f:
            json.dump({"profile_name": "tester", "current_level": 1, "player": {
                "x": 100, "y": 100, "health": 100, "lives": 3, "coins": 5, "score": 10,
                "weapon_level": 1, "keys": [], "max_jumps": 2}}, f)
        g.menu_selection = 1
        g._handle_menu_selection()
        self.assertEqual(g.state, GameState.PLAYING)
        self.assertEqual(g.player.current_weapon_id, "standard")


class LevelMapTests(GameTestCase):
    def profile_game(self, levels_completed=0):
        g = self.new_game()
        g.player_name = "mapper"
        g._create_new_profile()
        g.current_profile.levels_completed = levels_completed
        g._load_selected_profile_to_menu()
        g.menu_selection = 2
        g._handle_menu_selection()
        self.assertEqual(g.state, GameState.LEVEL_MAP)
        return g

    def test_level_names_match_design(self):
        from levels.level_names import LEVEL_NAMES, level_title
        self.assertEqual(len(LEVEL_NAMES), 7)
        self.assertEqual(level_title(0), "Tutorial: Training Facility")
        self.assertEqual(level_title(3), "Level 3: The Ascent")
        self.assertEqual(level_title(6, mark_boss=True), "Level 6: Guardian's Lair (BOSS)")

    def test_new_profile_can_only_play_tutorial(self):
        g = self.profile_game(levels_completed=0)
        frames(g)
        key(pygame.K_DOWN)
        frames(g)
        self.assertEqual(g.level_selection, 0)
        g._select_level_from_map(1)  # locked
        self.assertEqual(g.state, GameState.LEVEL_MAP)

    def test_start_unlocked_level_from_map(self):
        g = self.profile_game(levels_completed=3)
        self.assertEqual(g.level_selection, 3)  # opens on furthest unlocked level
        frames(g, 2)
        key(pygame.K_RETURN)
        frames(g)
        self.assertEqual(g.state, GameState.DIFFICULTY_SELECT)
        key(pygame.K_RETURN)
        frames(g, 2)
        self.assertEqual(g.state, GameState.PLAYING)
        self.assertEqual(g.current_level_index, 3)
        self.assertEqual(g.current_profile.levels_completed, 3, "starting a run keeps unlocks")

    def test_locked_level_cannot_be_started(self):
        g = self.profile_game(levels_completed=2)
        g._select_level_from_map(4)
        self.assertEqual(g.state, GameState.LEVEL_MAP)

    def test_click_level_row(self):
        g = self.profile_game(levels_completed=2)
        frames(g)
        row = g.menu.get_level_map_row_rects(len(g.levels))[1]
        g.mouse_pos = row.center
        pygame.mouse.get_pressed = lambda num_buttons=3: (True, False, False)
        try:
            g._handle_mouse_click()
        finally:
            del pygame.mouse.get_pressed
        self.assertEqual(g.state, GameState.DIFFICULTY_SELECT)
        self.assertEqual(g.start_level_index, 1)

    def test_completing_a_level_unlocks_the_next_once(self):
        g = self.playing_game(level=2)
        g._transition_to_level(3)
        self.assertEqual(g.current_profile.levels_completed, 3)
        g._load_level(0)
        g._transition_to_level(1)  # replaying the tutorial doesn't reset progress
        self.assertEqual(g.current_profile.levels_completed, 3)
        self.assertEqual(ProfileManager.load_profiles()[0].levels_completed, 3)


class ProfileStatsTests(GameTestCase):
    def test_score_counted_once_across_level_exits(self):
        g = self.playing_game()
        g.player.score = 100
        g._transition_to_level(1)
        g.player.score = 250  # run score keeps growing
        g._transition_to_level(2)
        self.assertEqual(g.current_profile.total_score, 250)

    def test_coins_collected_ignores_shop_spending(self):
        g = self.playing_game(level=1)
        coin = g.level.coins[0]
        g.player.x, g.player.y = coin.x, coin.y
        g._update_collectibles()
        earned = g.player.coins_earned
        self.assertGreater(earned, 0)
        g.player.coins = 0  # spent everything in the shop
        g._transition_to_level(2)
        self.assertEqual(g.current_profile.total_coins_collected, earned)

    def test_quit_and_continue_does_not_double_count(self):
        g = self.playing_game()
        g.player.score = 300
        g.state = GameState.PAUSED
        g.pause_selection = 2  # Save & Return to Menu (banks 300)
        g._handle_pause_selection()
        g.player = None
        g.menu_selection = 1  # Continue
        g._handle_menu_selection()
        g.player.score += 50
        g._transition_to_level(1)
        self.assertEqual(g.current_profile.total_score, 350)

    def test_game_over_adds_only_new_score(self):
        g = self.playing_game()
        g.player.score = 100
        g._transition_to_level(1)
        g.player.score = 180
        g.player.lives = 0
        g.player.die()
        g._update()
        self.assertEqual(g.state, GameState.GAME_OVER)
        self.assertEqual(g.current_profile.total_score, 180)


class WeaponAndSoundTests(GameTestCase):
    def test_u_key_upgrade_removed(self):
        g = self.playing_game()
        g.player.coins = 500
        frames(g, 3, hold={pygame.K_u})
        self.assertEqual(g.player.coins, 500)
        self.assertFalse(hasattr(g.player, "upgrade_weapon"))
        self.assertFalse(hasattr(g.player, "weapon_level"))

    def test_hud_shows_equipped_weapon(self):
        g = self.playing_game()
        self.assertEqual(g.player.get_weapon_name(), "Standard Shot P1")

    def test_melee_sound_file_exists(self):
        path = os.path.join(PROJECT_DIR, "assets", "audio", "sfx", "melee.wav")
        self.assertTrue(os.path.exists(path), "audio manager loads sfx/melee.wav")


class DifficultyScalingTests(GameTestCase):
    def enemies_on(self, level, difficulty=1):
        g = self.new_game()
        g.player_name = "scale"
        g._create_new_profile()
        g.difficulty_selection = difficulty
        g._start_new_game()
        g._load_level(level)
        return g, g.level.enemies

    def test_enemies_get_tougher_each_level(self):
        _, first = self.enemies_on(0)
        _, later = self.enemies_on(5)
        self.assertGreater(later[0].max_health, first[0].max_health)
        self.assertGreater(later[0].damage, first[0].damage)
        turrets0 = [e for e in first if e.type == "turret"]
        turrets5 = [e for e in later if e.type == "turret"]
        self.assertTrue(turrets5)
        if turrets0:
            self.assertLess(turrets5[0].shoot_cooldown, turrets0[0].shoot_cooldown)
        self.assertGreater(turrets5[0].projectile_damage, 8)

    def test_difficulty_changes_enemy_stats(self):
        _, easy = self.enemies_on(2, difficulty=0)
        _, normal = self.enemies_on(2, difficulty=1)
        _, hard = self.enemies_on(2, difficulty=2)
        self.assertLess(easy[0].max_health, normal[0].max_health)
        self.assertLess(normal[0].max_health, hard[0].max_health)

    def test_turret_fires_scaled_shot(self):
        g, enemies = self.enemies_on(5)
        turret = next(e for e in enemies if e.type == "turret")
        g.player.x, g.player.y = turret.x + 100, turret.y
        turret.shoot_timer = turret.shoot_cooldown
        g.projectiles = []
        g._update_enemies()
        shots = [p for p in g.projectiles if p.hostile]
        self.assertEqual(len(shots), 1)
        self.assertEqual(shots[0].damage, turret.projectile_damage)

    def test_standard_shot_kills_tutorial_enemy_in_two_hits(self):
        _, enemies = self.enemies_on(0)
        enemy = next(e for e in enemies if e.type == "ground")
        enemy.take_damage(10)
        self.assertFalse(enemy.dead)
        enemy.take_damage(10)
        self.assertTrue(enemy.dead)


class LevelDesignTests(GameTestCase):
    """Every level must be completable with the real player physics"""

    def test_every_level_can_reach_its_exit(self):
        g = self.new_game()  # Loads the 1280x720 layout + level data
        shutil.copy(os.path.join(PROJECT_DIR, "tests", "level_checker.py"), WORK_DIR)
        from level_checker import check_level
        for i, data in enumerate(g.levels):
            if not data.get("portals"):
                self.assertEqual(i, 6, "only the boss arena may have no portal")
                continue
            with self.subTest(level=i):
                result = check_level(data)
                self.assertTrue(result.portal_reached, f"level {i} exit is unreachable")
                self.assertGreaterEqual(result.coin_coverage(), 0.75,
                                        f"level {i}: too many unreachable coins "
                                        f"{result.unreachable_coins()[:10]}")


class BossAndEndingTests(GameTestCase):
    def test_boss_updates_once_per_frame(self):
        g = self.playing_game(level=6)
        self.assertIsNotNone(g.boss)
        calls = []
        original = g._update_boss
        g._update_boss = lambda: (calls.append(1), original())
        g._update()
        self.assertEqual(len(calls), 1)

    def test_boss_defeat_spawns_portal(self):
        g = self.playing_game(level=6)
        self.make_invincible(g)
        g.boss.health = 1
        g.boss.phase = 3  # skip the phase-change invulnerability
        g.boss.invuln_timer = 0
        portals = len(g.level.portals)
        for _ in range(300):
            g.projectiles = [Projectile(g.boss.x + 5, g.boss.y + 5, 1, 0, 5, (255, 255, 0))]
            g._update()
            if g.boss_defeated:
                break
        self.assertTrue(g.boss_defeated)
        self.assertEqual(len(g.level.portals), portals + 1)

    def test_act_complete_victory(self):
        g = self.playing_game(level=6)
        g._transition_to_level(7)
        frames(g, 2)
        self.assertEqual(g.state, GameState.VICTORY)
        completed = ProfileManager.load_completed_games()
        self.assertEqual([c.name for c in completed], ["tester"])
        key(pygame.K_RETURN)
        frames(g)
        self.assertEqual(g.state, GameState.PROFILE_SELECT)

    def test_game_over(self):
        g = self.playing_game()
        awarded = []
        g.achievement_manager.check_difficulty_complete = awarded.append
        g.player.lives = 0
        g.player.die()
        frames(g, 2)
        self.assertEqual(g.state, GameState.GAME_OVER)
        self.assertEqual(awarded, [], "game over must not award difficulty completion")
        key(pygame.K_RETURN)
        frames(g)
        self.assertEqual(g.state, GameState.MENU)
        self.assertIsNone(SaveManager.load_game("tester"))


if __name__ == "__main__":
    unittest.main()
