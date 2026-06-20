import pygame
from entities.player import Player
from entities.obstacles import SpawnManager
from systems.collision import checar_colisao
from systems.settings import LARGURA, ALTURA, FPS

# ── setup ─────────────────────────────────────────────────────────────────────
pygame.init()
tela  = pygame.display.set_mode((LARGURA, ALTURA))
clock = pygame.time.Clock()

player       = Player()
spawn_manager = SpawnManager()


def main():
    running      = True
    player.morto = False

    while running:
        dt = clock.tick(FPS) / 1000

        tela.fill("#212040")

        # ── desenho ───────────────────────────────────────────────────────────
        player.draw(tela)
        spawn_manager.draw(tela)

        # ── lógica ────────────────────────────────────────────────────────────
        if not player.morto:
            spawn_manager.atualizar(dt)

            for obs in spawn_manager.obstaculos:
                if checar_colisao(player, obs):
                    if obs.tipo == "mortal":
                        player.morto = True
                    elif obs.tipo == "bounce":
                        player.aplicar_bounce()

            player.atualizar_rastro(dt)
            player.zigzag(dt)
            player.morte_lateral(dt)
        else:
            player.game_over(tela)

        # ── eventos ───────────────────────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return

                if event.key == pygame.K_SPACE:
                    player.mudar_direcao()

                if event.key == pygame.K_w:
                    player.morto = True

                if player.morto and event.key == pygame.K_r:
                    player.restart(tela)
                    spawn_manager.restart()

        pygame.display.flip()

    pygame.quit()


main()