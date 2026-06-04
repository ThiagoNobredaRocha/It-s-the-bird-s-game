# ── Janela ──────────────────────────────────────────────────────────────
TITLE        = "Pet Guardian"
SCREEN_W     = 1280
SCREEN_H     = 720
FPS          = 60

# ── Física ───────────────────────────────────────────────────────────────
GRAVITY      = 0.6
MAX_FALL     = 18        # velocidade máxima de queda

# ── Player ───────────────────────────────────────────────────────────────
PLAYER_W         = 28
PLAYER_H         = 48
PLAYER_SPEED     = 4
PLAYER_JUMP      = -13
PLAYER_COLOR     = (80, 160, 255)

BULLET_SPEED     = 12
BULLET_W         = 8
BULLET_H         = 4
BULLET_COLOR     = (255, 230, 60)
BULLET_LIFETIME  = 90    # frames

# ── Pet ──────────────────────────────────────────────────────────────────
PET_W        = 22
PET_H        = 22
PET_SPEED    = 5
PET_COLOR    = (255, 160, 60)
PET_FOLLOW_DIST = 60     # distância ideal do player (px)

# ── Inimigo Atirador (Shooter) ────────────────────────────────────────────
SHOOTER_W        = 28
SHOOTER_H        = 44
SHOOTER_SPEED    = 1.8
SHOOTER_COLOR    = (200, 60, 60)
SHOOTER_DETECT   = 380   # raio de detecção (px)
SHOOTER_SHOOT_CD = 90    # frames entre tiros
ENEMY_BULLET_SPEED  = 7
ENEMY_BULLET_COLOR  = (255, 80, 80)

# ── Inimigo Rusher ────────────────────────────────────────────────────────
RUSHER_W        = 32
RUSHER_H        = 44
RUSHER_SPEED    = 1.8
RUSHER_RUSH_SPD = 5.5
RUSHER_COLOR    = (180, 40, 200)
RUSHER_DETECT   = 320

# ── Câmera ───────────────────────────────────────────────────────────────
CAM_LERP     = 0.1       # suavização (0 = sem mover, 1 = instantâneo)

# ── Mapa / Arena ─────────────────────────────────────────────────────────
WORLD_W      = 3200
WORLD_H      = 900
TILE_SIZE    = 32

# ── Cores ────────────────────────────────────────────────────────────────
C_BG         = (18, 18, 28)
C_GROUND     = (60, 65, 80)
C_PLATFORM   = (80, 90, 110)
C_WALL       = (45, 50, 65)
C_LADDER     = (140, 100, 50)
C_LADDER_RNG = (160, 120, 70)
C_HUD        = (220, 220, 230)
C_GAMEOVER   = (220, 60, 60)
C_WHITE      = (255, 255, 255)
