"""
entities/enemy_shooter.py
Inimigo 1: patrol → detecta player → atira nele.
Estados: PATROL | AIM | SHOOT
"""

import pygame
import settings as S
from systems.collision import resolve_platform
from systems.ai        import patrol_update, can_see_target
from entities.bullet   import Bullet
from utils.helpers     import angle_to


class EnemyShooter(pygame.sprite.Sprite):
    PATROL = "patrol"
    AIM    = "aim"

    def __init__(self, x: int, y: int,
                patrol_left: int, patrol_right: int):
        super().__init__()
        self.image = pygame.Surface((S.SHOOTER_W, S.SHOOTER_H), pygame.SRCALPHA)
        self._draw_shape()
        self.rect  = self.image.get_rect(topleft=(x, y))

        self.vx: float = 0.0
        self.vy: float = 0.0
        self.on_ground  = False

        self.patrol_left  = patrol_left
        self.patrol_right = patrol_right
        self.direction    = 1

        self.state    = self.PATROL
        self.shoot_cd = 0
        self.alive    = True

    # ── visual ────────────────────────────────────────────────────────────
    def _draw_shape(self):
        self.image.fill((0, 0, 0, 0))
        r = self.image.get_rect()
        # corpo
        pygame.draw.rect(self.image, S.SHOOTER_COLOR,
                         (2, r.height // 3, r.width - 4, r.height * 2 // 3))
        # cabeça quadrada (robótico)
        head_h = r.height // 3
        pygame.draw.rect(self.image, S.SHOOTER_COLOR, (3, 0, r.width - 6, head_h))
        # viseira (olho vermelho)
        pygame.draw.rect(self.image, (255, 60, 60),
                         (r.width // 4, head_h // 4, r.width // 2, head_h // 3))
        # cano de arma (lado direito)
        pygame.draw.rect(self.image, (40, 40, 40),
                         (r.width - 4, r.height // 2, 8, 4))

    # ── update ────────────────────────────────────────────────────────────
    def update(self, player_rect: pygame.Rect, game_map, bullets: list):
        if not self.alive:
            return

        ground = game_map.ground_rects
        walls  = game_map.wall_rects

        sees = can_see_target(self.rect, player_rect,
                                S.SHOOTER_DETECT, walls)

        # ── máquina de estado ─────────────────────────────────────────────
        if sees:
            self.state = self.AIM
        else:
            self.state = self.PATROL

        if self.state == self.PATROL:
            self.vx, self.direction = patrol_update(
                self.rect, S.SHOOTER_SPEED,
                self.direction, self.patrol_left, self.patrol_right)
        else:
            # fica parado e atira
            self.vx = 0
            self.shoot_cd -= 1
            if self.shoot_cd <= 0:
                angle = angle_to(self.rect, player_rect.center)
                b = Bullet(self.rect.centerx, self.rect.centery,
                            angle, S.ENEMY_BULLET_SPEED,
                            S.ENEMY_BULLET_COLOR, friendly=False,
                            lifetime=120)
                bullets.append(b)
                self.shoot_cd = S.SHOOTER_SHOOT_CD

        # ── física ───────────────────────────────────────────────────────
        self.vy += S.GRAVITY
        self.vy  = min(self.vy, S.MAX_FALL)

        self.rect, self.vx, self.vy, self.on_ground = resolve_platform(
            self.rect, self.vx, self.vy, ground, walls)

        self.rect.x = max(S.TILE_SIZE,
                            min(self.rect.x, S.WORLD_W - S.TILE_SIZE - S.SHOOTER_W))

    # ── desenho ───────────────────────────────────────────────────────────
    def draw(self, surface: pygame.Surface, cam_offset: pygame.Vector2):
        ox, oy = int(cam_offset.x), int(cam_offset.y)
        surface.blit(self.image, (self.rect.x - ox, self.rect.y - oy))

        # indicador de estado acima da cabeça
        color = (255, 60, 60) if self.state == self.AIM else (80, 80, 80)
        cx = self.rect.centerx - ox
        cy = self.rect.top - oy - 8
        pygame.draw.circle(surface, color, (cx, cy), 5)
