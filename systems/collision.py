import pygame

def checar_colisao(obj1, obj2):

    dx = obj2.x - obj1.x
    dy = obj2.y - obj1.y

    distancia_quadrada = dx * dx + dy * dy

    soma_raios = obj1.raio + obj2.raio

    return distancia_quadrada <= soma_raios * soma_raios