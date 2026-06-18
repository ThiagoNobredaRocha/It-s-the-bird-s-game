import pygame
from systems import settings as S

class Obstacle:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.x_inicial = x
        self.y_inicial = y
        self.raio = S.OBSTACLE_RAIO
        self.velocidade = S.OBSTACLE_VELOCIDADE
        self.morto = False 
        
    def draw(self, tela):
        pygame.draw.circle(
            tela,
            "blue",
            (self.x, self.y),
            self.raio
        )
        
    def atualizar(self, dt):
        self.y += self.velocidade * dt
        if self.y - self.raio > S.ALTURA:
            self.morto = True

    def restart(self):
        self.x = self.x_inicial
        self.y = self.y_inicial