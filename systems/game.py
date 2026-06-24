import pygame
import random
from systems import settings as S
from entities.player    import Player
from entities.obstacles import SpawnManager
from entities.enemies   import Enemy
from systems.collision  import checar_colisao
from systems.difficulty import get_difficulty

class Game:

    def __init__(self, tela):
        self.tela  = tela
        self.clock = pygame.time.Clock()
        self.fonte = pygame.font.SysFont(S.FONTE_UI, S.FONTE_TEXTO)
        self.fonte_score = pygame.font.SysFont(S.FONTE_UI, S.FONTE_SCORE)

        # objetos
        self.player = Player()
        self.spawn_manager = SpawnManager()

        # inimigos
        self.inimigos: list[Enemy] = []

        # estado
        self.score       = 0
        self.nivel       = 1
        self.tempo_spawn = 0.0
        self.tempo_score = 0.0
        self.dificuldade = self._calcular_dificuldade()
        self.rodando     = True

    def resetar(self):
        self.score       = 0
        self.nivel       = 1
        self.tempo_spawn = 0.0
        self.tempo_score = 0.0
        self.dificuldade = self._calcular_dificuldade()
        self.inimigos.clear()
        self.player.restart(self.tela)
        self.spawn_manager.restart()

    def _spawnar_inimigo(self):
        x = random.randint(50, S.LARGURA - 50)
        self.inimigos.append(Enemy(x))

    def _atualizar_nivel(self):
        faixa_niveis = S.NIVEL_MAX - 1
        novo = 1 + round(self.dificuldade * faixa_niveis)
        self.nivel = min(novo, S.NIVEL_MAX)

    def _calcular_dificuldade(self):
        return get_difficulty(
            self.score,
            S.DIFFICULTY_LIMIT,
            S.DIFFICULTY_SLOPE,
            S.DIFFICULTY_MIDPOINT,
        )

    def _adicionar_score(self, pontos):
        self.score += pontos

    def _pontuar_sobrevivencia(self, dt):
        self.tempo_score += dt
        while self.tempo_score >= 1.0:
            self._adicionar_score(S.SCORE_POR_SEGUNDO)
            self.tempo_score -= 1.0

    def _formatar_score(self):
        return f"{self.score:,}".replace(",", " ")

    def _remover_inimigos_mortos(self):
        inimigos_destruidos = sum(
            1 for e in self.inimigos
            if e.morto and e.destruido_pelo_jogador
        )
        if inimigos_destruidos:
            self._adicionar_score(inimigos_destruidos * S.SCORE_INIMIGO_DESTRUIDO)

        self.inimigos[:] = [e for e in self.inimigos if not e.morto]

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
        if self.player.morto:
            return

        self.dificuldade = self._calcular_dificuldade()
        self._atualizar_nivel()

        # obstáculos (mortais e bounce, gerenciados em ondas)
        self.spawn_manager.atualizar(dt, self.dificuldade)
        for obstacle in self.spawn_manager.obstaculos:
            if checar_colisao(self.player, obstacle):
                if obstacle.tipo == "bounce":
                    if not getattr(obstacle, "pontuado", False):
                        self._adicionar_score(S.SCORE_COLETA)
                        obstacle.pontuado = True
                    self.player.aplicar_bounce()
                else:
                    self.player.morto = True

        if self.player.morto:
            return

        # player
        self.player.atualizar_rastro(dt)
        self.player.zigzag(dt)
        self.player.morte_lateral(dt)

        # score e nível
        self._pontuar_sobrevivencia(dt)

        # spawn de inimigos
        self.tempo_spawn += dt
        intervalo_inimigo = S.ENEMY_SPAWN_INTERVALO / (
            1 + self.dificuldade * S.DIFFICULTY_SPAWN_FACTOR
        )
        pode_spawnar = len(self.inimigos) < S.ENEMY_MAX
        if self.tempo_spawn >= intervalo_inimigo and pode_spawnar:
            self._spawnar_inimigo()
            self.tempo_spawn = 0.0

        # inimigos — perseguem o player E são puxados pelo mapa
        for inimigo in self.inimigos:
            inimigo.atualizar(
                dt,
                self.player.x,
                self.player.y,
                self.dificuldade,
            )
            if checar_colisao(self.player, inimigo):
                self.player.morto = True

        self._remover_inimigos_mortos()

    def _desenhar(self):
        self.tela.fill(S.COR_FUNDO)

        self.spawn_manager.draw(self.tela)

        for inimigo in self.inimigos:
            inimigo.draw(self.tela)

        self.player.draw(self.tela)

        if self.player.morto:
            self.player.game_over(self.tela)

        self._desenhar_hud()
        pygame.display.flip()

    def _desenhar_hud(self):
        score = self.fonte_score.render(f"SCORE {self._formatar_score()}", True, S.COR_TEXTO)
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
