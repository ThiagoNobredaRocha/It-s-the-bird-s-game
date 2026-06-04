"""
entities/pet.py
Bichinho que segue o player pelas plataformas com física normal.
"""

import pygame
import settings as S
from systems.collision import resolve_platform, on_ladder
from utils.helpers     import normalize


class Pet(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int):
        super().__init__()
        self.image = pygame.Surface((S.PET_W, S.PET_H), pygame.SRCALPHA)
        self._draw_shape()
        self.rect  = self.image.get_rect(topleft=(x, y))

        self.vx: float = 0.0
        self.vy: float = 0.0
        self.on_ground  = False
        self.alive      = True

        # animação de flutuar (bobbing)
        self._bob_timer = 0.0

    # ── visual ────────────────────────────────────────────────────────────
    def _draw_shape(self):
        self.image.fill((0, 0, 0, 0))
        w, h = S.PET_W, S.PET_H
        # corpo arredondado (elipse)
        pygame.draw.ellipse(self.image, S.PET_COLOR, (0, h // 4, w, h * 3 // 4))
        # cabeça redonda
        pygame.draw.circle(self.image, S.PET_COLOR, (w // 2, h // 4), h // 4)
        # olhinhos
        pygame.draw.circle(self.image, (255, 255, 255), (w // 2 - 3, h // 4 - 1), 3)
        pygame.draw.circle(self.image, (255, 255, 255), (w // 2 + 3, h // 4 - 1), 3)
        pygame.draw.circle(self.image, (30, 30, 30),    (w // 2 - 3, h // 4 - 1), 1)
        pygame.draw.circle(self.image, (30, 30, 30),    (w // 2 + 3, h // 4 - 1), 1)
        # aurinhas
        pygame.draw.polygon(self.image, S.PET_COLOR,
                            [(w // 2 - 6, h // 4 - 4),
                             (w // 2 - 10, 0),
                             (w // 2 - 2, h // 4 - 6)])
        pygame.draw.polygon(self.image, S.PET_COLOR,
                            [(w // 2 + 6, h // 4 - 4),
                             (w // 2 + 10, 0),
                             (w // 2 + 2, h // 4 - 6)])

    # ── update ────────────────────────────────────────────────────────────
    def update(self, player_rect: pygame.Rect, game_map):
        if not self.alive:
            return

        ground  = game_map.ground_rects
        walls   = game_map.wall_rects
        ladders = game_map.ladder_rects

        # ── lógica de seguir ──────────────────────────────────────────────
        dx = player_rect.centerx - self.rect.centerx
        dy = player_rect.centery - self.rect.centery
        dist = (dx**2 + dy**2) ** 0.5

        # posição alvo: ao lado do player (oposto ao centro da tela)
        target_x = player_rect.left - S.PET_W - 8   # fica à esquerda do player
        dead_zone = 12   # não move se já está perto o suficiente

        h_diff = abs(self.rect.centerx - target_x)

        if h_diff > dead_zone:
            nx, _ = normalize(target_x - self.rect.centerx, 0)
            self.vx = nx * S.PET_SPEED
        else:
            self.vx = 0.0

        # ── escada ────────────────────────────────────────────────────────
        lad = on_ladder(self.rect, ladders)
        if lad and abs(dy) > 20:
            # sobe ou desce na escada em direção ao player
            ny = -1 if player_rect.centery < self.rect.centery else 1
            self.vy = ny * S.PET_SPEED
        else:
            # gravidade normal
            self.vy += S.GRAVITY
            self.vy  = min(self.vy, S.MAX_FALL)

            # se player está muito acima e pet está no chão → pula
            if (player_rect.bottom < self.rect.top - 40 and
                    self.on_ground and dist < 250):
                self.vy = S.PLAYER_JUMP * 0.9

        # ── resolver colisão ─────────────────────────────────────────────
        self.rect, self.vx, self.vy, self.on_ground = resolve_platform(
            self.rect, self.vx, self.vy, ground, walls)

        self.rect.x = max(S.TILE_SIZE,
                            min(self.rect.x, S.WORLD_W - S.TILE_SIZE - S.PET_W))
        self.rect.y = max(S.TILE_SIZE,
                            min(self.rect.y, S.WORLD_H - S.TILE_SIZE - S.PET_H))

        # bobbing visual suave
        self._bob_timer += 0.08

    # ── desenho ───────────────────────────────────────────────────────────
    def draw(self, surface: pygame.Surface, cam_offset: pygame.Vector2):
        import math
        ox, oy = int(cam_offset.x), int(cam_offset.y)
        bob = int(math.sin(self._bob_timer) * 2)   # oscila 2px
        surface.blit(self.image,
                    (self.rect.x - ox, self.rect.y - oy + bob))
