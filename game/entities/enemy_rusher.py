"""
entities/enemy_rusher.py
Inimigo 2: patrol → detecta pet → corre em direção ao pet.
Dano ao tocar o pet → game over.
"""

import pygame
import settings as S
from systems.collision import resolve_platform
from systems.ai        import patrol_update, can_see_target
from utils.helpers     import normalize


class EnemyRusher(pygame.sprite.Sprite):
    PATROL = "patrol"
    RUSH   = "rush"

    def __init__(self, x: int, y: int,
                    patrol_left: int, patrol_right: int):
        super().__init__()
        self.image = pygame.Surface((S.RUSHER_W, S.RUSHER_H), pygame.SRCALPHA)
        self._draw_shape()
        self.rect  = self.image.get_rect(topleft=(x, y))

        self.vx: float = 0.0
        self.vy: float = 0.0
        self.on_ground  = False

        self.patrol_left  = patrol_left
        self.patrol_right = patrol_right
        self.direction    = 1

        self.state = self.PATROL
        self.alive = True

    # ── visual ────────────────────────────────────────────────────────────
    def _draw_shape(self):
        self.image.fill((0, 0, 0, 0))
        r = self.image.get_rect()
        # corpo mais largo (agressivo)
        pygame.draw.rect(self.image, S.RUSHER_COLOR,
                         (0, r.height // 4, r.width, r.height * 3 // 4))
        # cabeça com chifre
        head_cx, head_cy = r.width // 2, r.height // 5
        head_r = r.width // 2 - 1
        pygame.draw.circle(self.image, S.RUSHER_COLOR, (head_cx, head_cy), head_r)
        # chifres
        pygame.draw.polygon(self.image, (220, 180, 50),
                            [(head_cx - 6, head_cy - head_r),
                            (head_cx - 12, head_cy - head_r - 10),
                            (head_cx - 1, head_cy - head_r + 2)])
        pygame.draw.polygon(self.image, (220, 180, 50),
                            [(head_cx + 6, head_cy - head_r),
                            (head_cx + 12, head_cy - head_r - 10),
                            (head_cx + 1, head_cy - head_r + 2)])
        # olhos furiosos
        pygame.draw.circle(self.image, (255, 220, 50), (head_cx - 5, head_cy), 4)
        pygame.draw.circle(self.image, (255, 220, 50), (head_cx + 5, head_cy), 4)
        pygame.draw.circle(self.image, (0, 0, 0),      (head_cx - 5, head_cy), 2)
        pygame.draw.circle(self.image, (0, 0, 0),      (head_cx + 5, head_cy), 2)

    # ── update ────────────────────────────────────────────────────────────
    def update(self, pet_rect: pygame.Rect, game_map):
        if not self.alive:
            return

        ground = game_map.ground_rects
        walls  = game_map.wall_rects

        sees = can_see_target(self.rect, pet_rect, S.RUSHER_DETECT, walls)

        if sees:
            self.state = self.RUSH
        else:
            self.state = self.PATROL

        if self.state == self.PATROL:
            self.vx, self.direction = patrol_update(
                self.rect, S.RUSHER_SPEED,
                self.direction, self.patrol_left, self.patrol_right)
        else:
            # rush: só horizontal (plataformer — não voa)
            dx = pet_rect.centerx - self.rect.centerx
            nx, _ = normalize(dx, 0)
            self.vx = nx * S.RUSHER_RUSH_SPD

        # ── física ───────────────────────────────────────────────────────
        self.vy += S.GRAVITY
        self.vy  = min(self.vy, S.MAX_FALL)

        self.rect, self.vx, self.vy, self.on_ground = resolve_platform(
            self.rect, self.vx, self.vy, ground, walls)

        self.rect.x = max(S.TILE_SIZE,
                        min(self.rect.x, S.WORLD_W - S.TILE_SIZE - S.RUSHER_W))

    def hits_pet(self, pet_rect: pygame.Rect) -> bool:
        return self.rect.colliderect(pet_rect)

    # ── desenho ───────────────────────────────────────────────────────────
    def draw(self, surface: pygame.Surface, cam_offset: pygame.Vector2):
        ox, oy = int(cam_offset.x), int(cam_offset.y)
        surface.blit(self.image, (self.rect.x - ox, self.rect.y - oy))

        # indicador de rush
        if self.state == self.RUSH:
            cx = self.rect.centerx - ox
            cy = self.rect.top - oy - 8
            pygame.draw.line(surface, (255, 200, 0),
                            (cx - 6, cy), (cx + 6, cy), 3)
