import pygame
from systems.settings import LARGURA, ALTURA

# player_sprite = pygame.image.load("assets/Maguinho.png")

TAMANHO_RASTRO  = 30
BOOST_FATOR     = 3  # multiplicador de velocidade durante o boost
BOOST_DURACAO   = 0.4  # segundos


class Player:

    def __init__(self):
        self.largura = 30
        self.altura  = 25

        self.x = LARGURA / 2
        self.y = 800

        self.raio = 20

        self.velocidade_base = 800
        self.velocidade      = self.velocidade_base
        self.vertical        = 250

        self.morto     = False
        self.direcao_x = -1

        self.rastro           = []
        self.velocidade_rastro = 500

        # boost
        self._boost_timer    = 0.0
        self._boost_ativo    = False
        self._bounce_recente = False   # evita múltiplas colisões no mesmo frame

    # ── boost ──────────────────────────────────────────────────────────────────

    def aplicar_bounce(self):
        """Chamado pelo main quando há colisão com ObstaculoBounce."""
        if self._bounce_recente:
            return
        self.direcao_x      *= -1
        self._boost_ativo    = True
        self._boost_timer    = BOOST_DURACAO
        self.velocidade      = self.velocidade_base * BOOST_FATOR
        self._bounce_recente = True   # trava até o próximo frame

    def _atualizar_boost(self, dt):
        # libera a trava de colisão a cada frame
        self._bounce_recente = False

        if self._boost_ativo:
            self._boost_timer -= dt
            if self._boost_timer <= 0:
                self._boost_ativo = False
                self._boost_timer = 0.0
                self.velocidade   = self.velocidade_base

    # ── rastro ─────────────────────────────────────────────────────────────────

    def atualizar_rastro(self, dt):
        for i in range(len(self.rastro)):
            x, y = self.rastro[i]
            self.rastro[i] = (x, y + self.velocidade_rastro * dt)

        self.rastro.append((self.x, self.y))

        if len(self.rastro) > TAMANHO_RASTRO:
            self.rastro.pop(0)

    # ── draw ───────────────────────────────────────────────────────────────────

    def draw(self, tela):
        if len(self.rastro) >= 2:
            for i in range(1, len(self.rastro)):
                progresso  = i / len(self.rastro)
                intensidade = int(255 * progresso)

                # rastro fica amarelo/laranja durante o boost
                if self._boost_ativo:
                    cor = (255, int(180 * progresso), 0)
                else:
                    cor = (intensidade, intensidade, intensidade)

                pygame.draw.line(tela, cor, self.rastro[i - 1], self.rastro[i], 3)

        cor_player = (255, 220, 0) if self._boost_ativo else (255, 182, 193)  # amarelo ou pink
        pygame.draw.circle(tela, cor_player, (int(self.x), int(self.y)), self.raio)

    def desenhar_player(self, tela):
        pass  # tela.blit(player_sprite, (self.x, self.y))

    # ── movimento ──────────────────────────────────────────────────────────────

    def subir(self, dt):
        pass

    def zigzag(self, dt):
        self._atualizar_boost(dt)
        self.x += self.direcao_x * self.velocidade * dt

    def mudar_direcao(self):
        self.direcao_x *= -1

    def morte_lateral(self, dt):
        self.lado_esquerdo = self.x - self.raio
        self.lado_direito  = self.x + self.raio

        if self.lado_esquerdo <= 0:
            self.morto = True

        if self.lado_direito >= LARGURA:
            self.morto = True

    # ── estados ────────────────────────────────────────────────────────────────

    def game_over(self, tela):
        pygame.draw.circle(tela, "red", (int(self.x), int(self.y)), 40)

    def restart(self, tela):
        self.morto          = False
        self.x              = LARGURA / 2
        self.y              = 800
        self.direcao_x      = -1
        self.velocidade     = self.velocidade_base
        self._boost_ativo   = False
        self._boost_timer   = 0.0
        self._bounce_recente = False
        self.rastro.clear()
