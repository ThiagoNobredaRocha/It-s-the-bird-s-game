import pygame
import math
from systems import settings as S


class Projectile:
    """Projétil disparado pelo player que se move em direção ao mouse."""

    def __init__(self, x, y, mouse_x, mouse_y):
        self.x = x
        self.y = y
        self.raio = S.PROJECTILE_RAIO
        self.morto = False  # sai da tela ou atinge um enemy

        # calcula a direção do player até o mouse
        dx = mouse_x - self.x
        dy = mouse_y - self.y
        distancia = math.hypot(dx, dy)

        # normaliza a direção
        if distancia > 0:
            self.vx = (dx / distancia) * S.PROJECTILE_SPEED
            self.vy = (dy / distancia) * S.PROJECTILE_SPEED
        else:
            self.vx = 0
            self.vy = -S.PROJECTILE_SPEED

    def atualizar(self, dt):
        # move na direção calculada
        self.x += self.vx * dt
        self.y += self.vy * dt

        # marca como morto se saiu da tela
        if self.fora_da_tela():
            self.morto = True

    def draw(self, tela):
        pygame.draw.circle(tela, S.COR_TEXTO, (int(self.x), int(self.y)), self.raio)
        # anel para destacar
        pygame.draw.circle(tela, (255, 255, 0), (int(self.x), int(self.y)), self.raio, 2)

    def fora_da_tela(self):
        return (self.x + self.raio < 0 or self.x - self.raio > S.LARGURA or
                self.y + self.raio < 0 or self.y - self.raio > S.ALTURA)
