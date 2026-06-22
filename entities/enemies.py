import pygame
import math
from systems import settings as S

class Enemy:

    def __init__(self, x):
        self.x          = x
        self.y          = S.ENEMY_SPAWN_Y
        self.raio       = S.ENEMY_RAIO
        self.velocidade = S.ENEMY_SPEED
        self.morto      = False

    def atualizar(self, dt, player_x, player_y):
        dx = player_x - self.x
        dy = player_y - self.y
        distancia = math.hypot(dx, dy)

        if distancia > 0:
            dx /= distancia
            dy /= distancia

        # persegue o player
        self.x += dx * self.velocidade * dt
        self.y += dy * self.velocidade * dt

        # puxado pelo mapa
        self.y += S.OBSTACLE_VELOCIDADE * dt / 3

        if self.y - self.raio > S.ALTURA:
            self.morto = True

    def draw(self, tela):
        p1 = (self.x,             self.y - self.raio)
        p2 = (self.x - self.raio, self.y + self.raio)
        p3 = (self.x + self.raio, self.y + self.raio)
        pygame.draw.polygon(tela, S.COR_BLUE, [p1, p2, p3])