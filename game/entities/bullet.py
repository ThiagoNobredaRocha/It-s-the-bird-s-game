"""
entities/bullet.py
Projétil genérico — usado pelo player e pelos inimigos.
"""

import math
import pygame
import settings as S


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x: float, y: float,
                 angle_deg: float,
                 speed: float,
                 color: tuple,
                 friendly: bool,          # True = do player, False = do inimigo
                 lifetime: int = S.BULLET_LIFETIME):
        super().__init__()
        self.friendly  = friendly
        self.lifetime  = lifetime
        self.color     = color
        self.speed     = speed

        rad = math.radians(angle_deg)
        self.vx = math.cos(rad) * speed
        self.vy = math.sin(rad) * speed

        self.image = pygame.Surface((S.BULLET_W, S.BULLET_H), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, color, self.image.get_rect())

        # rotaciona visualmente
        self.image = pygame.transform.rotate(self.image, -angle_deg)
        self.rect  = self.image.get_rect(center=(x, y))

        # posição float para precisão sub-pixel
        self.fx = float(x)
        self.fy = float(y)

    def update(self, ground_rects: list[pygame.Rect], wall_rects: list[pygame.Rect]):
        self.fx += self.vx
        self.fy += self.vy
        self.rect.centerx = int(self.fx)
        self.rect.centery  = int(self.fy)
        self.lifetime -= 1

        if self.lifetime <= 0:
            self.kill()
            return

        # some ao bater em chão ou parede
        all_solid = ground_rects + wall_rects
        for r in all_solid:
            if self.rect.colliderect(r):
                self.kill()
                return

    def draw(self, surface: pygame.Surface, cam_offset: pygame.Vector2):
        ox, oy = int(cam_offset.x), int(cam_offset.y)
        surface.blit(self.image,
                     (self.rect.x - ox, self.rect.y - oy))
