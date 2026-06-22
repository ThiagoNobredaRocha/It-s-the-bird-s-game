import pygame
import random
from systems import settings as S
from entities.player    import Player
from entities.obstacles import Obstacle
from entities.enemies   import Enemy
from systems.collision  import checar_colisao

class Game:

    def __init__(self, tela):
        self.tela  = tela
        self.clock = pygame.time.Clock()
        self.fonte = pygame.font.SysFont("Arial", 36)

        # objetos
        self.player    = Player()
        self.obstacles = [
            Obstacle(100, 100),
            Obstacle(400, 0),
        ]

        # inimigos
        self.inimigos: list[Enemy] = []

        # estado
        self.score       = 0.0
        self.nivel       = 1
        self.tempo_spawn = 0.0
        self.rodando     = True

    def resetar(self):
        self.score       = 0.0
        self.nivel       = 1
        self.tempo_spawn = 0.0
        self.inimigos.clear()
        self.player.restart(self.tela)
        for obstacle in self.obstacles:
            obstacle.restart()

    def _spawnar_inimigo(self):
        x = random.randint(50, S.LARGURA - 50)
        self.inimigos.append(Enemy(x))

    def _atualizar_nivel(self):
        novo = int(self.score // S.NIVEL_INTERVALO) + 1
        self.nivel = min(novo, S.NIVEL_MAX)

    def _processar_eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.rodando = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.rodando = False

                if event.key == pygame.K_SPACE:
                    if not self.player.morto:
                        self.player.mudar_direcao()

                if event.key == pygame.K_w:
                    self.player.morto = True

                if self.player.morto and event.key == pygame.K_r:
                    self.resetar()

    def _atualizar(self, dt):

        # obstáculos
        for obstacle in self.obstacles:
            obstacle.atualizar(dt)
            if checar_colisao(self.player, obstacle):
                self.player.morto = True

        if self.player.morto:
            return

        # player
        self.player.atualizar_rastro(dt)
        self.player.zigzag(dt)
        self.player.morte_lateral(dt)

        # score e nível
        self.score += S.SCORE_POR_SEGUNDO * dt
        self._atualizar_nivel()

        # spawn de inimigos
        self.tempo_spawn += dt
        if self.tempo_spawn >= S.ENEMY_SPAWN_INTERVALO and len(self.inimigos) < S.ENEMY_MAX:
            self._spawnar_inimigo()
            self.tempo_spawn = 0.0

        # inimigos — perseguem o player E são puxados pelo mapa
        for inimigo in self.inimigos:
            inimigo.atualizar(dt, self.player.x, self.player.y)
            if checar_colisao(self.player, inimigo):
                self.player.morto = True

        self.inimigos[:] = [e for e in self.inimigos if not e.morto]

    def _desenhar(self):
        self.tela.fill(S.COR_FUNDO)

        for obstacle in self.obstacles:
            obstacle.draw(self.tela)

        for inimigo in self.inimigos:
            inimigo.draw(self.tela)

        self.player.draw(self.tela)

        if self.player.morto:
            self.player.game_over(self.tela)

        self._desenhar_hud()
        pygame.display.flip()

    def _desenhar_hud(self):
        score = self.fonte.render(f"Score: {int(self.score)}", True, S.COR_TEXTO)
        msg   = self.fonte.render("R para reiniciar",         True, S.COR_TEXTO)
        self.tela.blit(score, (20, 20))

        if self.player.morto:
            self.tela.blit(msg, (S.LARGURA // 2 - 150, S.ALTURA // 2))

    def rodar(self):
        while self.rodando:
            dt = self.clock.tick(S.FPS) / 1000
            self._processar_eventos()
            self._atualizar(dt)
            self._desenhar()

        pygame.quit()