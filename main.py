import pygame
from systems import settings as S
from systems.game import Game

pygame.init()
tela = pygame.display.set_mode((S.LARGURA, S.ALTURA))
pygame.display.set_caption(S.TITLE)

jogo = Game(tela)
jogo.rodar()