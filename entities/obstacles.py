import pygame
from systems.settings import LARGURA, ALTURA

class Obstacle:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
        self.x_inicial = x
        self.y_inicial = y
        
        self.raio = 120
        
        self.velocidade = 600
        
    def draw(self, tela):
        pygame.draw.circle(
            tela,
            "blue",
            (self.x, self.y),
            self.raio
        )
        
    def atualizar(self, dt):
        self.y += self.velocidade * dt
        
    def restart(self):
        self.x = self.x_inicial
        self.y = self.y_inicial