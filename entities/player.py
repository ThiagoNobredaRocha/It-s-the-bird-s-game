import pygame
from systems import settings as S

#player_sprite = pygame.image.load("assets/Maguinho.png")

class Player:

    def __init__(self):
        self.largura = 30
        self.altura = 25

        self.x = S.PLAYER_X_INICIAL
        self.y = S.PLAYER_Y_INICIAL
        self.raio = S.PLAYER_RAIO
        self.velocidade = S.PLAYER_SPEED
        self.vertical = S.PLAYER_SPEED_VERTICAL
        self.velocidade_rastro = S.PLAYER_SPEED_RASTRO

        self.morto = False
        self.direcao_x = -1
        self.rastro = []

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

    def draw(self, tela):
        # desenha o rastro
        if len(self.rastro) >= 2:
            for i in range(1, len(self.rastro)):
                progresso = i / len(self.rastro)
                intensidade = int(255 * progresso)
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
        pygame.draw.circle(
            tela,
            S.COR_PINK,
            (self.x, self.y),
            self.raio
        )
    # def desenhar_player(self, tela):
    #     tela.blit(player_sprite, (self.x, self.y))
    def subir(self, dt):
        pass

    def zigzag(self, dt):
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
        self.rastro.clear()


#print(player_sprite.get_size())