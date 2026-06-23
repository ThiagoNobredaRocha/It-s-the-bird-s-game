import unittest

from entities.enemies import Enemy
from entities.obstacles import ObstaculoMortal, SpawnManager
from systems import settings as S
from systems.difficulty import get_difficulty
from systems.game import Game


class DifficultyTests(unittest.TestCase):

    def test_logistic_curve(self):
        self.assertAlmostEqual(get_difficulty(2000), 0.5)
        self.assertLess(get_difficulty(0), get_difficulty(500))
        self.assertLess(get_difficulty(500), get_difficulty(2000))
        self.assertLess(get_difficulty(2000), get_difficulty(4500))
        self.assertLess(get_difficulty(4500), get_difficulty(8000))

    def test_obstacle_scroll_reaches_sixty_percent_increase(self):
        obstacle = ObstaculoMortal(0, 0, 100)

        obstacle.atualizar(1, 1 + S.DIFFICULTY_SCROLL_FACTOR)

        self.assertAlmostEqual(obstacle.y, 160)

    def test_obstacle_waves_spawn_sooner_with_difficulty(self):
        manager = SpawnManager.__new__(SpawnManager)
        manager.obstaculos = []
        manager.timer = 0.0
        manager.ondas_spawnadas = 0
        manager._spawnar_onda = lambda: setattr(
            manager,
            "ondas_spawnadas",
            manager.ondas_spawnadas + 1,
        )

        manager.atualizar(1.3, dificuldade=1)

        self.assertEqual(manager.ondas_spawnadas, 1)

    def test_enemy_speed_doubles_at_maximum_difficulty(self):
        enemy = Enemy(0)
        enemy.y = 0

        enemy.atualizar(1, 1000, 0, dificuldade=1)

        self.assertAlmostEqual(enemy.x, S.ENEMY_SPEED * 2)
        self.assertAlmostEqual(
            enemy.y,
            S.OBSTACLE_VELOCIDADE * (1 + S.DIFFICULTY_SCROLL_FACTOR),
        )


class EnemyScoreTests(unittest.TestCase):

    def setUp(self):
        self.game = Game.__new__(Game)
        self.game.score = 0
        self.game.inimigos = []

    def test_enemy_leaving_screen_does_not_score(self):
        enemy = Enemy(100)
        enemy.destruir()
        self.game.inimigos = [enemy]

        self.game._remover_inimigos_mortos()

        self.assertEqual(self.game.score, 0)
        self.assertEqual(self.game.inimigos, [])

    def test_enemy_destroyed_by_player_scores_ten(self):
        enemy = Enemy(100)
        enemy.destruir(pelo_jogador=True)
        self.game.inimigos = [enemy]

        self.game._remover_inimigos_mortos()

        self.assertEqual(self.game.score, S.SCORE_INIMIGO_DESTRUIDO)
        self.assertEqual(self.game.inimigos, [])


if __name__ == "__main__":
    unittest.main()
