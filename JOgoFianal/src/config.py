# Screen
WIDTH = 960
HEIGHT = 720
FPS = 60

# Game
START_LIVES = 3
SAFE_SPAWN_TIME = 2.0
WAVE_DELAY = 2.0

# Ship
SHIP_RADIUS = 15
SHIP_TURN_SPEED = 220.0
SHIP_THRUST = 220.0
SHIP_FRICTION = 0.995
SHIP_FIRE_RATE = 0.2
SHIP_BULLET_SPEED = 420.0
HYPERSPACE_COST = 250

# Asteroids
AST_VEL_MIN = 30.0
AST_VEL_MAX = 90.0
AST_SIZES = {
    "L": {"r": 46, "score": 20, "split": ["M", "M"]},
    "M": {"r": 24, "score": 50, "split": ["S", "S"]},
    "S": {"r": 12, "score": 100, "split": []},
}

# Shot
BULLET_RADIUS = 2
BULLET_TTL = 1.0
MAX_BULLETS = 4

# UFO
UFO_SPAWN_EVERY = 3.0  # seconds
UFO_SPEED = 80.0
UFO_BIG = {"r": 18, "score": 200}
UFO_SMALL = {"r": 12, "score": 1000}

# Colors
WHITE = (240, 240, 240)
GRAY = (120, 120, 120)
BLACK = (0, 0, 0)

# Random
RANDOM_SEED = None
