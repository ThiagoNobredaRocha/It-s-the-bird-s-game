import pygame
import random
from systems import settings as S
from entities.player    import Player
from entities.obstacles import SpawnManager
from entities.enemies   import Enemy
from systems.collision  import checar_colisao
from systems.difficulty import get_difficulty

class Game:

    def __init__(self, tela):
        self.tela  = tela
        self.clock = pygame.time.Clock()
        self.fonte = pygame.font.SysFont(S.FONTE_UI, S.FONTE_TEXTO)
        self.fonte_score = pygame.font.SysFont(S.FONTE_UI, S.FONTE_SCORE)

        # objetos
        self.player = Player()
        self.spawn_manager = SpawnManager()

        # inimigos
        self.inimigos: list[Enemy] = []

        # fontes do menu
        self.fonte_titulo  = pygame.font.SysFont(S.FONTE_UI, S.FONTE_TITULO, bold=True)
        self.fonte_menu    = pygame.font.SysFont(S.FONTE_UI, S.FONTE_MENU)

        # estado
        self.estado = "menu"
        self.score = 0
        self.nivel = 1
        self.tempo_spawn = 0.0
        self.tempo_score = 0.0
        self.dificuldade = self._calcular_dificuldade()
        self.rodando = True

    def resetar(self):
        self.estado = "jogando"
        self.score = 0
        self.nivel = 1
        self.tempo_spawn = 0.0
        self.tempo_score = 0.0
        self.dificuldade = self._calcular_dificuldade()
        self.inimigos.clear()
        self.player.restart(self.tela)
        self.spawn_manager.restart()

    def _spawnar_inimigo(self):
        x = random.randint(50, S.LARGURA - 50)
        self.inimigos.append(Enemy(x))

    def _atualizar_nivel(self):
        faixa_niveis = S.NIVEL_MAX - 1
        novo = 1 + round(self.dificuldade * faixa_niveis)
        self.nivel = min(novo, S.NIVEL_MAX)

    def _calcular_dificuldade(self):
        return get_difficulty(
            self.score,
            S.DIFFICULTY_LIMIT,
            S.DIFFICULTY_SLOPE,
            S.DIFFICULTY_MIDPOINT,
        )

    def _adicionar_score(self, pontos):
        self.score += pontos

    def _pontuar_sobrevivencia(self, dt):
        self.tempo_score += dt
        while self.tempo_score >= 1.0:
            self._adicionar_score(S.SCORE_POR_SEGUNDO)
            self.tempo_score -= 1.0

    def _formatar_score(self):
        return f"{self.score:,}".replace(",", " ")

    def _remover_inimigos_mortos(self):
        inimigos_destruidos = sum(
            1 for e in self.inimigos
            if e.morto and e.destruido_pelo_jogador
        )
        if inimigos_destruidos:
            self._adicionar_score(inimigos_destruidos * S.SCORE_INIMIGO_DESTRUIDO)

        self.inimigos[:] = [e for e in self.inimigos if not e.morto]

    def _processar_eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.rodando = False

            if self.estado == "menu":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.rodando = False
                    else:
                        self.estado = "jogando"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.estado = "jogando"
                continue

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.rodando = False

                if event.key == pygame.K_SPACE:
                    if not self.player.morto:
                        self.player.mudar_direcao()

                if self.player.morto and event.key == pygame.K_r:
                    self.resetar()

    def _atualizar(self, dt):
        if self.estado != "jogando":
            return

        if self.player.morto:
            self.estado = "game_over"
            return

        self.dificuldade = self._calcular_dificuldade()
        self._atualizar_nivel()

        S.PROJECTILE_COOLDOWN += dt
        
        mouse_buttons = pygame.mouse.get_pressed()
        
        if (
            mouse_buttons[0]
            and not self.player.morto
            and S.PROJECTILE_COOLDOWN >= 0.15
        ):
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.player.disparar(mouse_x, mouse_y)
            S.PROJECTILE_COOLDOWN = 0.0

        # obstáculos (mortais e bounce, gerenciados em ondas)
        self.spawn_manager.atualizar(dt, self.dificuldade)
        for obstacle in self.spawn_manager.obstaculos:
            if checar_colisao(self.player, obstacle):
                if obstacle.tipo == "bounce":
                    if not getattr(obstacle, "pontuado", False):
                        self._adicionar_score(S.SCORE_COLETA)
                        obstacle.pontuado = True
                    self.player.aplicar_bounce()
                else:
                    self.player.morto = True

        if self.player.morto:
            self.estado = "game_over"
            return
        self.player.atualizar_rastro(dt)
        self.player.atualizar_projeteis(dt)
        self.player.zigzag(dt)
        self.player.morte_lateral(dt)

        # score e nível
        self._pontuar_sobrevivencia(dt)

        # spawn de inimigos
        self.tempo_spawn += dt
        intervalo_inimigo = S.ENEMY_SPAWN_INTERVALO / (
            1 + self.dificuldade * S.DIFFICULTY_SPAWN_FACTOR
        )
        pode_spawnar = len(self.inimigos) < S.ENEMY_MAX
        if self.tempo_spawn >= intervalo_inimigo and pode_spawnar:
            self._spawnar_inimigo()
            self.tempo_spawn = 0.0

        # inimigos — perseguem o player E são puxados pelo mapa
        for inimigo in self.inimigos:
            inimigo.atualizar(
                dt,
                self.player.x,
                self.player.y,
                self.dificuldade,
            )
            if checar_colisao(self.player, inimigo):
                self.player.morto = True

        # colisão entre projéteis e inimigos
        for proj in self.player.projeteis[:]:
            for inimigo in self.inimigos[:]:
                if not inimigo.morto and checar_colisao(proj, inimigo):
                    inimigo.destruir(pelo_jogador=True)
                    proj.morto = True
                    break

        self._remover_inimigos_mortos()

    def _desenhar(self):
        self.tela.fill(S.COR_FUNDO)
        if self.estado == "menu":
            self._desenhar_menu()
            pygame.display.flip()
            return
        self.spawn_manager.draw(self.tela)
        for inimigo in self.inimigos:
            inimigo.draw(self.tela)
        self.player.draw(self.tela)
        if self.player.morto:
            self.player.game_over(self.tela)
        self._desenhar_hud()
        pygame.display.flip()

    def _desenhar_menu(self):
        titulo = self.fonte_titulo.render(S.TITLE, True, S.COR_PINK)
        self.tela.blit(
            titulo,
            (S.LARGURA // 2 - titulo.get_width() // 2, S.ALTURA // 3 - 80)
        )

        controles = [
            ("SPACE",      "muda a direção do zigzag"),
            ("CLICK ESQ.", "dispara projétil em direção ao mouse"),
            ("R",          "reinicia depois de morrer"),
            ("ESC",        "sair do jogo"),
        ]

        coluna_tecla_x = S.LARGURA // 2 - 20
        coluna_desc_x  = S.LARGURA // 2 + 20

        y = S.ALTURA // 3 + 20
        for tecla, descricao in controles:
            texto_tecla = self.fonte_menu.render(tecla, True, S.COR_TEXTO)
            texto_desc  = self.fonte_menu.render(descricao, True, S.COR_TEXTO)

            self.tela.blit(texto_tecla, (coluna_tecla_x - texto_tecla.get_width(), y))
            self.tela.blit(texto_desc, (coluna_desc_x, y))

            y += S.FONTE_MENU + 14

        chamada = self.fonte.render(
            "Pressione qualquer tecla ou clique para começar",
            True, S.COR_RED
        )
        self.tela.blit(
            chamada,
            (S.LARGURA // 2 - chamada.get_width() // 2, y + 40)
        )

    def _desenhar_hud(self):
        score = self.fonte_score.render(f"SCORE {self._formatar_score()}", True, S.COR_TEXTO)
        msg   = self.fonte.render("R para reiniciar",         True, S.COR_TEXTO)
        self.tela.blit(score, (20, 20))

        if self.player.morto:
            self.tela.blit(msg, (S.LARGURA // 2 - 150, S.ALTURA // 2))

    def rodar(self):
        while self.rodando:
            dt = self.clock.tick(S.FPS) / 1000
            self._processar_eventos()
            self._atualizar(dt)
            self._desenhar()

        pygame.quit()