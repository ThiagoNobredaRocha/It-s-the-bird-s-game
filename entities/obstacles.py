import pygame
import random
from systems.settings import LARGURA, ALTURA

# ── constantes de spawn ───────────────────────────────────────────────────────
RAIO_MORTAL  = 180
RAIO_BOUNCE  = 90

VEL_MIN      = 420
VEL_MAX      = 620

# Quantas colunas dividem a tela para o fair-spawn
NUM_COLUNAS  = 6

# Intervalo entre ondas de spawn (segundos)
INTERVALO_SPAWN = 2.2

# Quantos obstáculos por onda
QTDE_POR_ONDA = 3

# Margem vertical fora da tela onde o obstáculo nasce
MARGEM_SPAWN_Y = -80

# Espaçamento vertical extra entre obstáculos da MESMA onda
# (cada obstáculo subsequente nasce mais "atrasado" verticalmente)
ESPACAMENTO_VERTICAL_MIN = 250
ESPACAMENTO_VERTICAL_MAX = 450


# ── classes de obstáculo ──────────────────────────────────────────────────────

class ObstaculoMortal:
    """Mata o player ao colidir."""

    def __init__(self, x, y, velocidade):
        self.x = x
        self.y = y
        self.raio = RAIO_MORTAL
        self.velocidade = velocidade
        self.tipo = "mortal"

    def draw(self, tela):
        pygame.draw.circle(tela, (124, 53, 50), (int(self.x), int(self.y)), self.raio)
        # anel para destacar
        pygame.draw.circle(tela, (255, 120, 120), (int(self.x), int(self.y)), self.raio, 3)

    def atualizar(self, dt):
        self.y += self.velocidade * dt

    def fora_da_tela(self):
        return self.y - self.raio > ALTURA


class ObstaculoBounce:
    """Inverte a direção horizontal do player e aplica boost de velocidade."""

    def __init__(self, x, y, velocidade):
        self.x = x
        self.y = y
        self.raio = RAIO_BOUNCE
        self.velocidade = velocidade
        self.tipo = "bounce"

    def draw(self, tela):
        pygame.draw.circle(tela, (80, 200, 255), (int(self.x), int(self.y)), self.raio)
        pygame.draw.circle(tela, (180, 240, 255), (int(self.x), int(self.y)), self.raio, 3)

    def atualizar(self, dt):
        self.y += self.velocidade * dt

    def fora_da_tela(self):
        return self.y - self.raio > ALTURA


# ── spawn manager ─────────────────────────────────────────────────────────────

class SpawnManager:
    """
    Gerencia o spawn de obstáculos com fair-randomness:
    - Divide a tela em NUM_COLUNAS colunas.
    - A cada onda, sorteia QTDE_POR_ONDA colunas *distintas* para garantir
      espaço sempre disponível para o player escapar.
    - Alterna aleatoriamente entre mortal e bounce (mínimo 1 bounce por onda).
    """

    def __init__(self):
        self.obstaculos: list = []
        self.timer = 0.0
        # dispara a primeira onda imediatamente
        self._spawnar_onda()

    # largura de cada coluna
    @property
    def _largura_coluna(self):
        return LARGURA // NUM_COLUNAS

    def _spawnar_onda(self):
        # escolhe colunas distintas (garante espaçamento mínimo entre obstáculos)
        colunas = random.sample(range(NUM_COLUNAS), QTDE_POR_ONDA)

        # garante pelo menos 1 bounce na onda
        idx_bounce_forcado = random.randrange(QTDE_POR_ONDA)

        # ordem aleatória de "atraso vertical" — não correlaciona com a coluna,
        # então o gap vertical aparece em posições x diferentes a cada onda
        ordem_atraso = list(range(QTDE_POR_ONDA))
        random.shuffle(ordem_atraso)

        # cada obstáculo nasce mais "alto" (y mais negativo) que o anterior,
        # criando espaçamento vertical real entre eles
        atraso_acumulado = 0

        for i, col in enumerate(colunas):
            # posição x centrada na coluna + pequeno jitter
            centro_coluna = col * self._largura_coluna + self._largura_coluna // 2
            jitter = random.randint(-self._largura_coluna // 4, self._largura_coluna // 4)
            x = centro_coluna + jitter
            x = max(RAIO_MORTAL + 10, min(LARGURA - RAIO_MORTAL - 10, x))  # clamp

            # posição na ordem de atraso (0 = primeiro a entrar, sem atraso)
            posicao_na_ordem = ordem_atraso[i]
            if posicao_na_ordem == 0:
                atraso = 0
            else:
                atraso = posicao_na_ordem * random.randint(
                    ESPACAMENTO_VERTICAL_MIN, ESPACAMENTO_VERTICAL_MAX
                )

            y = MARGEM_SPAWN_Y - atraso

            vel = random.uniform(VEL_MIN, VEL_MAX)

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
        if self.timer >= INTERVALO_SPAWN:
            self.timer = 0.0
            self._spawnar_onda()

    def draw(self, tela):
        for obs in self.obstaculos:
            obs.draw(tela)

    def restart(self):
        self.obstaculos.clear()
        self.timer = 0.0
        self._spawnar_onda()