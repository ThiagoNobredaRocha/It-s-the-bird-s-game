"""
systems/ai.py
Lógica de IA reutilizável: patrol, detecção, etc.
"""

import pygame
from utils.helpers import distance, normalize


def patrol_update(rect: pygame.Rect,
                    speed: float,
                    direction: int,
                    patrol_left: int,
                    patrol_right: int) -> tuple[float, int]:
    """
    Move horizontalmente entre patrol_left e patrol_right.
    Retorna (vx, nova_direction).
    direction: +1 = direita, -1 = esquerda
    """
    vx = speed * direction
    if rect.right >= patrol_right:
        direction = -1
    elif rect.left <= patrol_left:
        direction = 1
    return vx, direction


def can_see_target(src: pygame.Rect,
                    target: pygame.Rect,
                    detect_range: float,
                    walls: list[pygame.Rect] | None = None) -> bool:
    """
    Verifica se src enxerga target dentro de detect_range.
    Se walls for fornecido, faz raycast simples por sampling.
    """
    if distance(src, target) > detect_range:
        return False
    if not walls:
        return True

    # raycast simples por amostragem (32 passos)
    sx, sy = float(src.centerx), float(src.centery)
    tx, ty = float(target.centerx), float(target.centery)
    dx, dy = tx - sx, ty - sy
    nx, ny = normalize(dx, dy)
    steps = 32
    step_len = ((dx**2 + dy**2) ** 0.5) / steps
    for i in range(1, steps):
        px = int(sx + nx * step_len * i)
        py = int(sy + ny * step_len * i)
        probe = pygame.Rect(px - 2, py - 2, 4, 4)
        for w in walls:
            if probe.colliderect(w):
                return False
    return True
