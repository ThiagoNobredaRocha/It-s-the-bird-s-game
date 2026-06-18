import pygame
from entities.player import Player
from entities.obstacles import Obstacle
from systems.collision import checar_colisao
from systems.settings import LARGURA, ALTURA, FPS
# pygame setup
pygame.init()
tela = pygame.display.set_mode((LARGURA, ALTURA))
clock = pygame.time.Clock()
player = Player()
obstacles = [
    Obstacle(100, 100),
    Obstacle(400, 0)
    ]
def main ():
    running = True
    player.morto = False
            
    while running:
        dt = clock.tick(FPS) / 1000
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        tela.fill("#212040")
        #player.desenhar_player(tela)
        player.draw(tela)
        
        for obstacle in obstacles:

            obstacle.draw(tela)

            if not player.morto:
                obstacle.atualizar(dt)

            if checar_colisao(player, obstacle):
                player.morto = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit() 
                
                if event.key == pygame.K_SPACE:
                    player.mudar_direcao()
                    
                if event.key == pygame.K_w:
                    player.morto = True
                    
                if player.morto == True and event.key == pygame.K_r:
                    player.restart(tela)
                    for obstacle in obstacles:
                        obstacle.restart()

        if not player.morto:
            player.atualizar_rastro(dt)
            player.zigzag(dt)
            player.morte_lateral(dt)
        else:
            player.game_over(tela)
        
        

        
        # if not player.paused:
        #     player.subir(dt)
        #     player.zigzag(dt)
        #     player.morte_lateral(dt)
        # else:
        #     player.pause(dt)
        
        
        # flip() the display to put your work on screen
        pygame.display.flip()

    clock.tick(60)  # limits FPS to 60
    pygame.quit()


main()
