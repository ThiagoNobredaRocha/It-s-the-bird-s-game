"""
systems/collision.py
Funções centralizadas de colisão.
"""

import pygame
import settings as S


def resolve_platform(entity_rect: pygame.Rect,
                        vx: float, vy: float,
                        ground_rects: list[pygame.Rect],
                        wall_rects:   list[pygame.Rect]) -> tuple[pygame.Rect, float, float, bool]:
    """
    Move entity_rect com (vx, vy) e resolve colisões com chão e paredes.
    Retorna (rect_final, vx_final, vy_final, on_ground).
    """
    on_ground = False

    # ── horizontal ────────────────────────────────────────────────────────
    entity_rect.x += int(vx)
    all_solid = ground_rects + wall_rects
    for wall in all_solid:
        if entity_rect.colliderect(wall):
            if vx > 0:
                entity_rect.right = wall.left
            elif vx < 0:
                entity_rect.left = wall.right

    # ── vertical ──────────────────────────────────────────────────────────
    entity_rect.y += int(vy)
    for surface in ground_rects:
        if entity_rect.colliderect(surface):
            if vy > 0:                          # caindo
                entity_rect.bottom = surface.top
                vy = 0
                on_ground = True
            elif vy < 0:                        # subindo (cabeça bate)
                entity_rect.top = surface.bottom
                vy = 0

    for wall in wall_rects:
        if entity_rect.colliderect(wall):
            if vy > 0:
                entity_rect.bottom = wall.top
                vy = 0
                on_ground = True
            elif vy < 0:
                entity_rect.top = wall.bottom
                vy = 0

    return entity_rect, vx, vy, on_ground


def on_ladder(entity_rect: pygame.Rect,
                ladder_rects: list[pygame.Rect]) -> pygame.Rect | None:
    """Retorna a escada que colide com o entity, ou None."""
    for lad in ladder_rects:
        if entity_rect.colliderect(lad):
            return lad
    return None


def bullet_hits(bullet_rect: pygame.Rect,
                targets: list[pygame.Rect]) -> int:
    """Retorna índice do primeiro alvo atingido, ou -1."""
    for i, t in enumerate(targets):
        if bullet_rect.colliderect(t):
            return i
    return -1
