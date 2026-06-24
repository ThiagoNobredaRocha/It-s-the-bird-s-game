import pygame
from systems import settings as S
import math
from entities.projectiles import Projectile

# player_sprite = pygame.image.load("assets/Maguinho.png")

class Player:

    def __init__(self):
        self.largura = 30
        self.altura  = 25
        self.x = S.PLAYER_X_INICIAL
        self.y = S.PLAYER_Y_INICIAL
        self.raio = S.PLAYER_RAIO

        self.velocidade_base = S.PLAYER_SPEED
        self.velocidade = self.velocidade_base

        self.vertical = S.PLAYER_SPEED_VERTICAL
        self.velocidade_rastro = S.PLAYER_SPEED_RASTRO

        self.morto     = False
        self.direcao_x = -1
        self.rastro = []

        # boost
        self._boost_timer    = 0.0
        self._boost_ativo    = False
        self._bounce_recente = False   # evita múltiplas colisões no mesmo frame

        # tiro
        self.projeteis = []
        self._tiro_cooldown = 0.0

    # ── boost ──────────────────────────────────────────────────────────────────

    def aplicar_bounce(self):
        """Chamado pelo game quando há colisão com ObstaculoBounce."""
        if self._bounce_recente:
            return
        self.direcao_x      *= -1
        self._boost_ativo    = True
        self._boost_timer    = S.PLAYER_BOOST_DURACAO
        self.velocidade      = self.velocidade_base * S.PLAYER_BOOST_FATOR
        self._bounce_recente = True   # trava até o próximo frame

    def disparar(self, mouse_x, mouse_y):
        """Cria um novo projétil na posição do player em direção ao mouse."""
        if self._tiro_cooldown <= 0:
            self.projeteis.append(Projectile(self.x, self.y, mouse_x, mouse_y))
            self._tiro_cooldown = S.PROJECTILE_COOLDOWN

    def atualizar_projeteis(self, dt):
        """Atualiza todos os projéteis e remove os que saíram da tela."""
        for proj in self.projeteis:
            proj.atualizar(dt)
        self.projeteis = [p for p in self.projeteis if not p.fora_da_tela()]

    def _atualizar_boost(self, dt):
        # libera a trava de colisão a cada frame
        self._bounce_recente = False

        if self._boost_ativo:
            self._boost_timer -= dt
            if self._boost_timer <= 0:
                self._boost_ativo = False
                self._boost_timer = 0.0
                self.velocidade   = self.velocidade_base

        # atualiza cooldown de tiro
        if self._tiro_cooldown > 0:
            self._tiro_cooldown -= dt

    def atualizar_rastro(self,dt):
        # faz os pontos antigos descerem
        for i in range(len(self.rastro)):
            x, y = self.rastro[i]
            self.rastro[i] = (x, y + self.velocidade_rastro * dt)
    # adiciona a posição atual do player
        self.rastro.append((self.x, self.y))
    # limita o tamanho do rastro
        if len(self.rastro) > S.PLAYER_TAMANHO_RASTRO:
            self.rastro.pop(0)

    # ── draw ───────────────────────────────────────────────────────────────────

    def draw(self, tela):
        # desenha os projéteis
        for proj in self.projeteis:
            proj.draw(tela)

        # desenha o rastro
        if len(self.rastro) >= 2:
            for i in range(1, len(self.rastro)):
                progresso = i / len(self.rastro)
                intensidade = int(255 * progresso)

                if self._boost_ativo:
                    cor = (255, int(180 * progresso), 0)
                else:
                    cor = (
                        intensidade,
                        intensidade,
                        intensidade
                    )

                pygame.draw.line(
                    tela,
                    cor,
                    self.rastro[i - 1],
                    self.rastro[i],
                    3
                )

        cor_player = S.COR_PLAYER_BOOST if self._boost_ativo else S.COR_PINK
        pygame.draw.circle(
            tela,
            cor_player,
            (self.x, self.y),
            self.raio
        )
    # def desenhar_player(self, tela):
    #     tela.blit(player_sprite, (self.x, self.y))

    def subir(self, dt):
        pass

    def zigzag(self, dt):
        self._atualizar_boost(dt)
        self.x += self.direcao_x * self.velocidade * dt

    def mudar_direcao(self):
        self.direcao_x *= -1

    def morte_lateral(self, dt):
        if self.x - self.raio <= 0:
            self.morto = True
        if self.x + self.raio >= S.LARGURA:
            self.morto = True

    def game_over(self, tela):
        pygame.draw.circle(
            tela,
            S.COR_RED,
            (self.x, self.y),
            40
        )

    def restart(self, tela):
        self.morto = False
        self.x = S.PLAYER_X_INICIAL
        self.y = S.PLAYER_Y_INICIAL
        self.direcao_x      = -1
        self.velocidade     = self.velocidade_base
        self._boost_ativo   = False
        self._boost_timer   = 0.0
        self._bounce_recente = False
        self.rastro.clear()
        self.projeteis.clear()
        self._tiro_cooldown = 0.0