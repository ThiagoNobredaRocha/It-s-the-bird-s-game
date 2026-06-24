#JANELA
TITLE = "ZigZag Cosmic"
LARGURA = 1550
ALTURA = 900
FPS = 60

#PLAYER
PLAYER_X_INICIAL = LARGURA / 2
PLAYER_Y_INICIAL = 800
PLAYER_RAIO = 20
PLAYER_SPEED = 800
PLAYER_SPEED_VERTICAL = 250
PLAYER_SPEED_RASTRO = 500
PLAYER_TAMANHO_RASTRO = 30

#PLAYER - BOOST (bounce)
PLAYER_BOOST_FATOR = 3       # multiplicador de velocidade durante o boost
PLAYER_BOOST_DURACAO = 0.4   # segundos

#OBSTACULOS
OBSTACLE_RAIO = 120
OBSTACLE_VELOCIDADE = 600

#ENEMY
ENEMY_SPEED = 150
ENEMY_RAIO = 14
ENEMY_SPAWN_INTERVALO = 2.0
ENEMY_MAX = 20
ENEMY_SPAWN_Y = -30

#PROJECTILES (TIRO)
PROJECTILE_SPEED = 800
PROJECTILE_RAIO = 8
PROJECTILE_COOLDOWN = 0.2  # tempo mínimo entre tiros (segundos)

#SCORE
SCORE_POR_SEGUNDO = 1
INIMIGO_MORTO_SCORE = 5  # pontos por derrotar um inimigo com tiro
NIVEL_INTERVALO = 10
NIVEL_MAX = 10

#CORES
COR_FUNDO = "#212040"
COR_TEXTO = (255, 255, 255)
COR_PINK = "pink"
COR_RED = "red"
COR_BLUE = "blue"
COR_PLAYER_BOOST = (255, 220, 0)

#OBSTACULOS - MORTAL / BOUNCE (spawn em ondas)
RAIO_MORTAL  = 180
RAIO_BOUNCE  = 90

VEL_MIN      = 420
VEL_MAX      = 620

# Intervalo entre ondas de spawn (segundos)
INTERVALO_SPAWN = 2.2

# Quantos obstáculos por onda
QTDE_POR_ONDA = 3

# Distância horizontal mínima entre os CENTROS de dois obstáculos da mesma onda.
# Evita que eles nasçam colados/sobrepostos mesmo com jitter.
DISTANCIA_MIN_X = (RAIO_MORTAL * 2) + 60

# Margem vertical fora da tela onde o obstáculo nasce
MARGEM_SPAWN_Y = -80

# Espaçamento vertical extra entre obstáculos da MESMA onda
# (cada obstáculo subsequente nasce mais "atrasado" verticalmente)
ESPACAMENTO_VERTICAL_MIN = 250
ESPACAMENTO_VERTICAL_MAX = 450