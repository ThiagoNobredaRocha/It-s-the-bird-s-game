"""
systems/map.py
Gera a arena: chão, paredes, plataformas e escadas.
Retorna listas de pygame.Rect usadas nas colisões.
"""

import pygame
import settings as S


class GameMap:
    def __init__(self):
        self.ground_rects: list[pygame.Rect] = []   # superfícies sólidas (chão + plataformas)
        self.wall_rects:   list[pygame.Rect] = []   # paredes laterais e blocos
        self.ladder_rects: list[pygame.Rect] = []   # escadas (só colisão vertical)
        self._build()

    # ── construção ────────────────────────────────────────────────────────
    def _add_ground(self, x, y, w, h=S.TILE_SIZE):
        self.ground_rects.append(pygame.Rect(x, y, w, h))

    def _add_wall(self, x, y, w, h):
        self.wall_rects.append(pygame.Rect(x, y, w, h))

    def _add_ladder(self, x, y, h):
        self.ladder_rects.append(pygame.Rect(x, y, S.TILE_SIZE, h))

    def _build(self):
        W, H = S.WORLD_W, S.WORLD_H
        T = S.TILE_SIZE

        # ── Chão principal ──────────────────────────────────────────────
        self._add_ground(0, H - T, W, T)           # chão completo

        # ── Paredes laterais ────────────────────────────────────────────
        self._add_wall(0,     0, T, H)             # parede esquerda
        self._add_wall(W - T, 0, T, H)             # parede direita

        # ── Teto ────────────────────────────────────────────────────────
        self._add_wall(0, 0, W, T)

        # ── Bloco central baixo ─────────────────────────────────────────
        self._add_ground(480,  H - T*4, T*6, T*3)  # bloco sólido esquerda

        # ── Plataformas flutuantes ───────────────────────────────────────
        # seção esquerda
        self._add_ground(160,  H - T*7,  T*5, T)
        self._add_ground(96,   H - T*12, T*4, T)
        # seção centro-esquerda
        self._add_ground(640,  H - T*6,  T*4, T)
        self._add_ground(768,  H - T*11, T*5, T)
        # seção centro
        self._add_ground(1100, H - T*5,  T*6, T)
        self._add_ground(1050, H - T*10, T*4, T)
        # seção direita
        self._add_ground(1600, H - T*7,  T*5, T)
        self._add_ground(1700, H - T*12, T*4, T)
        self._add_ground(2000, H - T*5,  T*6, T)
        self._add_ground(2100, H - T*10, T*3, T)
        self._add_ground(2400, H - T*7,  T*5, T)
        self._add_ground(2500, H - T*12, T*4, T)
        self._add_ground(2700, H - T*5,  T*6, T)

        # ── Blocos-obstáculo no chão ─────────────────────────────────────
        self._add_ground(320,  H - T*3, T*2, T*2)
        self._add_ground(1400, H - T*3, T*2, T*2)
        self._add_ground(1900, H - T*3, T*3, T*2)
        self._add_ground(2600, H - T*3, T*2, T*2)
        self._add_ground(2900, H - T*3, T*2, T*2)

        # ── Escadas ──────────────────────────────────────────────────────
        # cada escada: x alinhado com borda de plataforma, y do topo até o chão/plat inferior
        self._add_ladder(224,  H - T*7,   T*6)   # sobe para plat 160
        self._add_ladder(128,  H - T*12,  T*5)   # sobe para plat 96
        self._add_ladder(736,  H - T*6,   T*5)   # sobe para plat 640
        self._add_ladder(800,  H - T*11,  T*5)   # sobe para plat 768
        self._add_ladder(1152, H - T*5,   T*4)   # sobe para plat 1100
        self._add_ladder(1088, H - T*10,  T*5)   # sobe para plat 1050
        self._add_ladder(1664, H - T*7,   T*6)   # sobe para plat 1600
        self._add_ladder(1728, H - T*12,  T*5)   # sobe para plat 1700
        self._add_ladder(2048, H - T*5,   T*4)
        self._add_ladder(2432, H - T*7,   T*6)
        self._add_ladder(2528, H - T*12,  T*5)
        self._add_ladder(2720, H - T*5,   T*4)

    # ── desenho ───────────────────────────────────────────────────────────
    def draw(self, surface: pygame.Surface, cam_offset: pygame.Vector2):
        ox, oy = int(cam_offset.x), int(cam_offset.y)

        for r in self.ground_rects:
            shifted = r.move(-ox, -oy)
            if -r.width < shifted.x < S.SCREEN_W and -r.height < shifted.y < S.SCREEN_H:
                pygame.draw.rect(surface, S.C_GROUND, shifted)
                pygame.draw.rect(surface, S.C_PLATFORM, shifted, 2)

        for r in self.wall_rects:
            shifted = r.move(-ox, -oy)
            if -r.width < shifted.x < S.SCREEN_W and -r.height < shifted.y < S.SCREEN_H:
                pygame.draw.rect(surface, S.C_WALL, shifted)

        for r in self.ladder_rects:
            shifted = r.move(-ox, -oy)
            if -r.width < shifted.x < S.SCREEN_W and -r.height < shifted.y < S.SCREEN_H:
                # desenha degraus
                pygame.draw.rect(surface, S.C_LADDER, shifted)
                step = S.TILE_SIZE // 2
                for i in range(0, r.height, step):
                    y = shifted.y + i
                    pygame.draw.line(surface, S.C_LADDER_RNG,
                                    (shifted.x, y), (shifted.right, y), 2)
