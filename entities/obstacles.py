import pygame
from systems import settings as S
import random


# ── classes de obstáculo ──────────────────────────────────────────────────────

class ObstaculoMortal:
    """Mata o player ao colidir."""

    def __init__(self, x, y, velocidade):
        self.x = x
        self.y = y
        self.raio = S.RAIO_MORTAL
        self.velocidade = velocidade
        self.tipo = "mortal"

    def draw(self, tela):
        pygame.draw.circle(tela, (124, 53, 50), (int(self.x), int(self.y)), self.raio)
        # anel para destacar
        pygame.draw.circle(tela, (255, 120, 120), (int(self.x), int(self.y)), self.raio, 3)

    def atualizar(self, dt):
        self.y += self.velocidade * dt

    def fora_da_tela(self):
        return self.y - self.raio > S.ALTURA


class ObstaculoBounce:
    """Inverte a direção horizontal do player e aplica boost de velocidade."""

    def __init__(self, x, y, velocidade):
        self.x = x
        self.y = y
        self.raio = S.RAIO_BOUNCE
        self.velocidade = velocidade
        self.tipo = "bounce"
        self.pontuado = False

    def draw(self, tela):
        pygame.draw.circle(tela, (80, 200, 255), (int(self.x), int(self.y)), self.raio)
        pygame.draw.circle(tela, (180, 240, 255), (int(self.x), int(self.y)), self.raio, 3)

    def atualizar(self, dt):
        self.y += self.velocidade * dt

    def fora_da_tela(self):
        return self.y - self.raio > S.ALTURA


# ── spawn manager ─────────────────────────────────────────────────────────────

class SpawnManager:
    """
    Gerencia o spawn de obstáculos com fair-randomness:
    - Gera posições X garantindo DISTANCIA_MIN_X entre todos os obstáculos
      da mesma onda, evitando que nasçam colados ou sobrepostos.
    - Escalonamento vertical entre os obstáculos da mesma onda, para criar
      gaps verticais que sinergizam com o zigzag do player.
    - Pelo menos 1 obstáculo bounce por onda.
    """

    def __init__(self):
        self.obstaculos: list = []
        self.timer = 0.0
        # dispara a primeira onda imediatamente
        self._spawnar_onda()

    def _gerar_posicoes_x(self):
        """
        Gera QTDE_POR_ONDA posições X garantindo DISTANCIA_MIN_X entre
        quaisquer dois centros, para que obstáculos nunca nasçam colados
        ou sobrepostos, mesmo entre tipos diferentes (mortal/bounce).
        """
        x_min = S.RAIO_MORTAL + 10
        x_max = S.LARGURA - S.RAIO_MORTAL - 10

        posicoes = []
        tentativas_max = 200

        for _ in range(S.QTDE_POR_ONDA):
            for _ in range(tentativas_max):
                candidato = random.randint(x_min, x_max)
                if all(abs(candidato - p) >= S.DISTANCIA_MIN_X for p in posicoes):
                    posicoes.append(candidato)
                    break
            else:
                # não achou posição livre o suficiente; usa o que sobrar de espaço
                # (caso extremo — espalha uniformemente como fallback)
                if posicoes:
                    posicoes.append(max(x_min, min(x_max, posicoes[-1] + S.DISTANCIA_MIN_X)))
                else:
                    posicoes.append(random.randint(x_min, x_max))

        return posicoes

    def _spawnar_onda(self):
        # posições x com distância mínima garantida entre todos os obstáculos
        posicoes_x = self._gerar_posicoes_x()

        # garante pelo menos 1 bounce na onda
        idx_bounce_forcado = random.randrange(S.QTDE_POR_ONDA)

        # ordem aleatória de "atraso vertical" — não correlaciona com a posição x,
        # então o gap vertical aparece em posições x diferentes a cada onda
        ordem_atraso = list(range(S.QTDE_POR_ONDA))
        random.shuffle(ordem_atraso)

        for i, x in enumerate(posicoes_x):
            posicao_na_ordem = ordem_atraso[i]
            if posicao_na_ordem == 0:
                atraso = 0
            else:
                atraso = posicao_na_ordem * random.randint(
                    S.ESPACAMENTO_VERTICAL_MIN, S.ESPACAMENTO_VERTICAL_MAX
                )

            y = S.MARGEM_SPAWN_Y - atraso

            vel = random.uniform(S.VEL_MIN, S.VEL_MAX)

            if i == idx_bounce_forcado:
                tipo = "bounce"
            else:
                tipo = "mortal"  # slots extras sempre mortais

            if tipo == "mortal":
                self.obstaculos.append(ObstaculoMortal(x, y, vel))
            else:
                self.obstaculos.append(ObstaculoBounce(x, y, vel))

    def atualizar(self, dt):
        for obs in self.obstaculos:
            obs.atualizar(dt)

        # remove os que saíram da tela
        self.obstaculos = [o for o in self.obstaculos if not o.fora_da_tela()]

        # conta o tempo para a próxima onda
        self.timer += dt
        if self.timer >= S.INTERVALO_SPAWN:
            self.timer = 0.0
            self._spawnar_onda()

    def draw(self, tela):
        for obs in self.obstaculos:
            obs.draw(tela)

    def restart(self):
        self.obstaculos.clear()
        self.timer = 0.0
        self._spawnar_onda()
