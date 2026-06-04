"""
scenes/game_scene.py
Cena principal: arena, câmera, HUD, loop de jogo.
"""

import pygame
import settings as S
from systems.map          import GameMap
from entities.player      import Player
from entities.pet         import Pet
from entities.enemy_shooter import EnemyShooter
from entities.enemy_rusher  import EnemyRusher
from entities.bullet      import Bullet


def _spawn_enemies(game_map):
    """Define posições e rangers de patrol dos inimigos."""
    H = S.WORLD_H
    T = S.TILE_SIZE

    shooters = [
        EnemyShooter(700,  H - T*7 - S.SHOOTER_H,  640,  880),   # plat centro-esq
        EnemyShooter(1150, H - T*6 - S.SHOOTER_H, 1100, 1310),   # plat centro
        EnemyShooter(1750, H - T*8 - S.SHOOTER_H, 1600, 1870),   # plat direita
        EnemyShooter(2450, H - T*8 - S.SHOOTER_H, 2400, 2620),   # plat direita 2
        EnemyShooter(900,  H - T*2 - S.SHOOTER_H,  700, 1300),   # chão centro
        EnemyShooter(2100, H - T*2 - S.SHOOTER_H, 1900, 2500),   # chão direita
    ]

    rushers = [
        EnemyRusher(400,  H - T*2 - S.RUSHER_H,   200,  700),    # chão esquerda
        EnemyRusher(1500, H - T*2 - S.RUSHER_H,  1300, 1800),    # chão centro-dir
        EnemyRusher(2700, H - T*2 - S.RUSHER_H,  2600, 3000),    # chão direita
        EnemyRusher(790,  H - T*12 - S.RUSHER_H,  768, 1000),    # plat alta
        EnemyRusher(2510, H - T*13 - S.RUSHER_H, 2500, 2660),    # plat alta dir
    ]

    return shooters, rushers


class GameScene:
    def __init__(self, screen: pygame.Surface):
        self.screen  = screen
        self.font_lg = pygame.font.SysFont("monospace", 64, bold=True)
        self.font_sm = pygame.font.SysFont("monospace", 22)
        self.reset()

    # ── reset / inicialização ─────────────────────────────────────────────
    def reset(self):
        H = S.WORLD_H
        T = S.TILE_SIZE
        self.game_map = GameMap()
        self.player   = Player(200, H - T*2 - S.PLAYER_H)
        self.pet      = Pet(120, H - T*2 - S.PET_H)
        self.shooters, self.rushers = _spawn_enemies(self.game_map)
        self.bullets:  list[Bullet] = []
        self.camera    = pygame.Vector2(0, 0)
        self.game_over = False
        self.kill_count = 0
        self._go_alpha  = 0    # fade do game over

    # ── câmera ────────────────────────────────────────────────────────────
    def _update_camera(self):
        target_x = self.player.rect.centerx - S.SCREEN_W // 2
        target_y = self.player.rect.centery - S.SCREEN_H // 2

        # lerp suave
        self.camera.x += (target_x - self.camera.x) * S.CAM_LERP
        self.camera.y += (target_y - self.camera.y) * S.CAM_LERP

        # clamp nos limites do mundo
        self.camera.x = max(0, min(self.camera.x, S.WORLD_W - S.SCREEN_W))
        self.camera.y = max(0, min(self.camera.y, S.WORLD_H - S.SCREEN_H))

    # ── mouse → coordenada mundo ──────────────────────────────────────────
    def _mouse_world(self) -> tuple:
        mx, my = pygame.mouse.get_pos()
        return (mx + int(self.camera.x), my + int(self.camera.y))

    # ── update principal ──────────────────────────────────────────────────
    def update(self, events: list[pygame.event.Event]):
        # restart
        for ev in events:
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_r:
                self.reset()
                return

        if self.game_over:
            self._go_alpha = min(255, self._go_alpha + 4)
            return

        keys    = pygame.key.get_pressed()
        mbuts   = pygame.mouse.get_pressed()
        mworld  = self._mouse_world()

        # ── player ────────────────────────────────────────────────────────
        self.player.update(keys, mworld, mbuts,
                            self.game_map, self.bullets, self.camera)

        # ── pet ───────────────────────────────────────────────────────────
        self.pet.update(self.player.rect, self.game_map)

        # ── balas ─────────────────────────────────────────────────────────
        # No update da GameScene (Linhas 85-90)
        alive_bullets = []
        for b in self.bullets:
            b.update(self.game_map.ground_rects, self.game_map.wall_rects)
            # Como a Bullet dá self.kill(), o método nativo b.alive() retornará False 
            # se ela sumir. Mas se preferir usar o atributo padrão do seu projeto:
            if b.lifetime > 0: 
                alive_bullets.append(b)
        self.bullets = alive_bullets

        # ── shooters ──────────────────────────────────────────────────────
        for sh in self.shooters:
            if not sh.alive:
                continue
            sh.update(self.player.rect, self.game_map, self.bullets)

            # bala do player acerta shooter
            for b in self.bullets:
                if b.friendly and sh.rect.colliderect(b.rect):
                    sh.alive = False
                    b.kill()
                    self.kill_count += 1
                    break

            # bala do shooter acerta pet → game over
            for b in self.bullets:
                if not b.friendly and self.pet.rect.colliderect(b.rect):
                    self.game_over = True

        # ── rushers ───────────────────────────────────────────────────────
        for ru in self.rushers:
            if not ru.alive:
                continue
            ru.update(self.pet.rect, self.game_map)

            # bala do player acerta rusher
            for b in self.bullets:
                if b.friendly and ru.rect.colliderect(b.rect):
                    ru.alive = False
                    b.kill()
                    self.kill_count += 1
                    break

            # rusher toca o pet → game over
            if ru.hits_pet(self.pet.rect):
                self.game_over = True

        # ── câmera ────────────────────────────────────────────────────────
        self._update_camera()

    # ── desenho ───────────────────────────────────────────────────────────
    def draw(self):
        self.screen.fill(S.C_BG)

        cam = self.camera
        self.game_map.draw(self.screen, cam)

        # entidades (ordem: pet atrás do player)
        self.pet.draw(self.screen, cam)
        self.player.draw(self.screen, cam)

        for sh in self.shooters:
            if sh.alive:
                sh.draw(self.screen, cam)
        for ru in self.rushers:
            if ru.alive:
                ru.draw(self.screen, cam)

        for b in self.bullets:
            b.draw(self.screen, cam)

        # ── HUD ───────────────────────────────────────────────────────────
        self._draw_hud()

        # ── game over overlay ─────────────────────────────────────────────
        if self.game_over:
            self._draw_gameover()

    def _draw_hud(self):
        # kills
        kills_surf = self.font_sm.render(
            f"Kills: {self.kill_count}", True, S.C_HUD)
        self.screen.blit(kills_surf, (16, 16))

        # minimap de posição do player
        map_w, map_h = 160, 40
        map_x, map_y = S.SCREEN_W - map_w - 16, 16
        pygame.draw.rect(self.screen, (30, 30, 40), (map_x, map_y, map_w, map_h))
        pygame.draw.rect(self.screen, (80, 80, 100), (map_x, map_y, map_w, map_h), 1)

        px_ratio = self.player.rect.centerx / S.WORLD_W
        py_ratio = self.player.rect.centery / S.WORLD_H
        dot_x = int(map_x + px_ratio * map_w)
        dot_y = int(map_y + py_ratio * map_h)
        pygame.draw.circle(self.screen, S.PLAYER_COLOR, (dot_x, dot_y), 4)

        pet_px = int(map_x + self.pet.rect.centerx / S.WORLD_W * map_w)
        pet_py = int(map_y + self.pet.rect.centery / S.WORLD_H * map_h)
        pygame.draw.circle(self.screen, S.PET_COLOR, (pet_px, pet_py), 3)

        # controles (canto inferior)
        hint = self.font_sm.render(
            "WASD mover  |  MOUSE mira  |  CLICK atirar  |  R reiniciar",
            True, (100, 100, 120))
        self.screen.blit(hint, (16, S.SCREEN_H - 30))

    def _draw_gameover(self):
        overlay = pygame.Surface((S.SCREEN_W, S.SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, min(180, self._go_alpha)))
        self.screen.blit(overlay, (0, 0))

        if self._go_alpha < 120:
            return

        txt1 = self.font_lg.render("GAME OVER", True, S.C_GAMEOVER)
        txt2 = self.font_sm.render("Seu pet foi atingido...", True, S.C_WHITE)
        txt3 = self.font_sm.render(f"Inimigos eliminados: {self.kill_count}", True, S.C_HUD)
        txt4 = self.font_sm.render("Pressione R para reiniciar", True, (160, 160, 180))

        cx = S.SCREEN_W // 2
        cy = S.SCREEN_H // 2
        self.screen.blit(txt1, txt1.get_rect(center=(cx, cy - 60)))
        self.screen.blit(txt2, txt2.get_rect(center=(cx, cy + 10)))
        self.screen.blit(txt3, txt3.get_rect(center=(cx, cy + 40)))
        self.screen.blit(txt4, txt4.get_rect(center=(cx, cy + 80)))
