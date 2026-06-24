import pygame
import math
from systems import settings as S

class Enemy:

    def __init__(self, x):
        self.x = x
        self.y = S.ENEMY_SPAWN_Y
        self.raio = S.ENEMY_RAIO
        self.velocidade = S.ENEMY_SPEED
        self.morto = False
        self.destruido_pelo_jogador = False

    def destruir(self, pelo_jogador=False):
        self.morto = True
        self.destruido_pelo_jogador = pelo_jogador

    def atualizar(self, dt, player_x, player_y, dificuldade=0.0):
        dx = player_x - self.x
        dy = player_y - self.y
        distancia = math.hypot(dx, dy)

        if distancia > 0:
            dx /= distancia
            dy /= distancia

        # persegue o player
        velocidade = self.velocidade * (
            1 + dificuldade * S.DIFFICULTY_ENEMY_SPEED_FACTOR
        )
        self.x += dx * velocidade * dt
        self.y += dy * velocidade * dt

        # puxado pelo mapa
        velocidade_scroll = S.OBSTACLE_VELOCIDADE * (
            1 + dificuldade * S.DIFFICULTY_SCROLL_FACTOR
        )
        self.y += velocidade_scroll * dt / 2

        if self.y - self.raio > S.ALTURA:
            self.destruir()

    def draw(self, tela):
        p1 = (self.x, self.y - self.raio)
        p2 = (self.x - self.raio, self.y + self.raio)
        p3 = (self.x + self.raio, self.y + self.raio)
        pygame.draw.polygon(tela, S.COR_BLUE, [p1, p2, p3])
