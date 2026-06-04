"""
main.py
Ponto de entrada — inicializa pygame e roda o loop principal.
"""

import pygame
import settings as S
from scenes.game_scene import GameScene


def main():
    pygame.init()
    pygame.display.set_caption(S.TITLE)
    screen = pygame.display.set_mode((S.SCREEN_W, S.SCREEN_H))
    clock  = pygame.time.Clock()

    scene = GameScene(screen)

    running = True
    while running:
        events = pygame.event.get()
        for ev in events:
            if ev.type == pygame.QUIT:
                running = False
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                running = False

        scene.update(events)
        scene.draw()
        pygame.display.flip()
        clock.tick(S.FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
