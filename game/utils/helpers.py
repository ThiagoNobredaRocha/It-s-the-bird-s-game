import math
import pygame


def normalize(vx: float, vy: float) -> tuple[float, float]:
    """Retorna vetor unitário (vx, vy). Se zero, retorna (0,0)."""
    mag = math.hypot(vx, vy)
    if mag == 0:
        return 0.0, 0.0
    return vx / mag, vy / mag


def distance(a: pygame.Rect, b: pygame.Rect) -> float:
    """Distância entre centros de dois Rects."""
    dx = a.centerx - b.centerx
    dy = a.centery - b.centery
    return math.hypot(dx, dy)


def angle_to(src: pygame.Rect, dst_pos: tuple) -> float:
    """Ângulo em graus de src.center até dst_pos."""
    dx = dst_pos[0] - src.centerx
    dy = dst_pos[1] - src.centery
    return math.degrees(math.atan2(dy, dx))


def vec_toward(src: pygame.Rect, dst: pygame.Rect, speed: float) -> tuple[float, float]:
    """Vetor de movimento de src em direção ao centro de dst, com comprimento=speed."""
    dx = dst.centerx - src.centerx
    dy = dst.centery - src.centery
    nx, ny = normalize(dx, dy)
    return nx * speed, ny * speed
