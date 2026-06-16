import pygame
from systems.settings import LARGURA, ALTURA

#player_sprite = pygame.image.load("assets/Maguinho.png")

TAMANHO_RASTRO = 30

class Player:

    def __init__(self):
        self.largura = 30
        self.altura = 25

        self.x = LARGURA / 2
        self.y = 800

        self.raio = 20

        self.velocidade = 800
        self.vertical = 250

        self.morto = False
        self.direcao_x = -1

        self.rastro = []
        self.velocidade_rastro = 500

    def atualizar_rastro(self,dt):

        # faz os pontos antigos descerem
        for i in range(len(self.rastro)):
            x, y = self.rastro[i]
            self.rastro[i] = (x, y + self.velocidade_rastro * dt)

    # adiciona a posição atual do player
        self.rastro.append((self.x, self.y))

    # limita o tamanho do rastro
        if len(self.rastro) > TAMANHO_RASTRO:
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
            "pink",
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

        self.lado_esquerdo = self.x - self.raio
        self.lado_direito = self.x + self.raio

        if self.lado_esquerdo <= 0:
            self.morto = True

        if self.lado_direito >= LARGURA:
            self.morto = True

    def game_over(self, tela):

        pygame.draw.circle(
            tela,
            "red",
            (self.x, self.y),
            40
        )

    def restart(self, tela):

        self.morto = False

        self.x = LARGURA / 2
        self.y = 800

        self.rastro.clear()


#print(player_sprite.get_size())