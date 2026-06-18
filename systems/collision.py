import pygame
from systems.utils import dist

def checar_colisao(obj1, obj2) -> bool:
    distancia = dist(obj1.x, obj1.y, obj2.x, obj2.y)
    return distancia <= obj1.raio + obj2.raio