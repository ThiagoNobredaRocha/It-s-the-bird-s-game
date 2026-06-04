"""
entities/player.py
Controles: A/D mover, W/S em escada, W pular no chão, mouse mira e atira.
"""

import pygame
import settings as S
from systems.collision import resolve_platform, on_ladder
from entities.bullet   import Bullet
from utils.helpers     import angle_to


class Player(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int):
        super().__init__()
        self.image = pygame.Surface((S.PLAYER_W, S.PLAYER_H), pygame.SRCALPHA)
        self._draw_shape()
        self.rect  = self.image.get_rect(topleft=(x, y))

        self.vx: float = 0.0
        self.vy: float = 0.0
        self.on_ground  = False
        self.on_ladder_obj: pygame.Rect | None = None
        self.facing     = 1            # +1 direita, -1 esquerda
        self.shoot_cd   = 0
        self.alive      = True

    # ── visual ────────────────────────────────────────────────────────────
    def _draw_shape(self):
        self.image.fill((0, 0, 0, 0))
        r = self.image.get_rect()
        # corpo
        pygame.draw.rect(self.image, S.PLAYER_COLOR,
                         (2, r.height // 3, r.width - 4, r.height * 2 // 3))
        # cabeça
        head_r = r.width // 2 - 2
        pygame.draw.circle(self.image, S.PLAYER_COLOR,
                           (r.width // 2, head_r + 2), head_r)
        # olho (indica direção)
        eye_x = r.width // 2 + 4
        pygame.draw.circle(self.image, (255, 255, 255), (eye_x, head_r), 3)
        pygame.draw.circle(self.image, (0, 0, 0),       (eye_x, head_r), 1)

    # ── update ────────────────────────────────────────────────────────────
    def update(self,
                keys: pygame.key.ScancodeWrapper,
                mouse_world_pos: tuple,
                mouse_buttons: tuple,
                game_map,
                bullets: list,
                cam_offset: pygame.Vector2):

        if not self.alive:
            return

        ground = game_map.ground_rects
        walls  = game_map.wall_rects
        ladders= game_map.ladder_rects

        # ── escada ────────────────────────────────────────────────────────
        lad = on_ladder(self.rect, ladders)
        self.on_ladder_obj = lad

        # ── horizontal ────────────────────────────────────────────────────
        self.vx = 0
        if keys[pygame.K_a]:
            self.vx = -S.PLAYER_SPEED
            self.facing = -1
        if keys[pygame.K_d]:
            self.vx =  S.PLAYER_SPEED
            self.facing = 1

        # ── vertical ──────────────────────────────────────────────────────
        if lad:
            # no modo escada cancela gravidade
            self.vy = 0
            if keys[pygame.K_w]:
                self.vy = -S.PLAYER_SPEED
            elif keys[pygame.K_s]:
                self.vy =  S.PLAYER_SPEED
            # saída da escada pelo topo: pulo normal
        else:
            # gravidade
            self.vy += S.GRAVITY
            self.vy  = min(self.vy, S.MAX_FALL)

            # pulo
            if keys[pygame.K_w] and self.on_ground:
                self.vy = S.PLAYER_JUMP

        # ── resolver colisão ─────────────────────────────────────────────
        self.rect, self.vx, self.vy, self.on_ground = resolve_platform(
            self.rect, self.vx, self.vy, ground, walls)

        # clamp dentro do mundo
        self.rect.x = max(S.TILE_SIZE,
                            min(self.rect.x, S.WORLD_W - S.TILE_SIZE - S.PLAYER_W))
        self.rect.y = max(S.TILE_SIZE,
                            min(self.rect.y, S.WORLD_H - S.TILE_SIZE - S.PLAYER_H))

        # ── tiro ──────────────────────────────────────────────────────────
        if self.shoot_cd > 0:
            self.shoot_cd -= 1

        if mouse_buttons[0] and self.shoot_cd == 0:
            angle = angle_to(self.rect, mouse_world_pos)
            b = Bullet(self.rect.centerx, self.rect.centery,
                        angle, S.BULLET_SPEED, S.BULLET_COLOR, friendly=True)
            bullets.append(b)
            self.shoot_cd = 15

    # ── desenho ───────────────────────────────────────────────────────────
    def draw(self, surface: pygame.Surface, cam_offset: pygame.Vector2):
        ox, oy = int(cam_offset.x), int(cam_offset.y)
        surface.blit(self.image, (self.rect.x - ox, self.rect.y - oy))

        # barra de "escada" indicator
        if self.on_ladder_obj:
            pygame.draw.rect(surface, S.C_LADDER,
                                (self.rect.x - ox - 2, self.rect.y - oy - 4,
                                self.rect.width + 4, 3))
