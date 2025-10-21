import pygame
import math
import random
from pathlib import Path

pygame.init()
pygame.mixer.init()

# CONSTANTS AND GLOBAL VARIABLES
DARK_BLUE = (0, 0, 139)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
ORANGE = (255, 75, 10)
BLACK = (0, 0, 0)
YELLOW = (255, 180, 0)
BROWN = (178, 59, 25)
BLUE = (50, 50, 180)
GAME_WIDTH, GAME_HEIGHT = 256, 192
SCALE_FACTOR = 4
WINDOW_WIDTH = GAME_WIDTH * SCALE_FACTOR
WINDOW_HEIGHT = GAME_HEIGHT * SCALE_FACTOR
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Little Tank Combat")
clock = pygame.time.Clock()
last_shot_time_1 = 0  # ms
last_shot_time_2 = 0  # ms
shot_cooldown = 500  # ms
shot_lifetime = 500  # ms
running = True  # main loop control
shots = []  # list to store bullets
shot_size = 7   # bullet size
shot_speed = 20  # bullet speed (+ or - depending on direction)
player1_health = 5
player2_health = 5
player1_score = 0
player2_score = 0

# SOUNDS SETUP
BASE = Path(__file__).resolve().parent  # script folder

sound_shot = pygame.mixer.Sound(str(BASE.parent / "core" / "shotsound.mp3"))
sound_collision = pygame.mixer.Sound(
    str(BASE.parent / "core" / "colision_sound.mp3")
)

# GAME FONT
font = pygame.font.Font("atividade007\\core\\PressStart2P-Regular.ttf", 70)


class Player:

    # INIT METHOD
    def __init__(self, x, y, key_left, key_right, image_path, key_up=None):
        self.key_left = key_left
        self.key_right = key_right
        self.key_up = key_up
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.original_image = pygame.transform.scale_by(self.original_image, 5)
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))
        self.angle = 0
        self.rotation_speed = 3
        self.hit_time = None

        # Change color of player 1
        if key_left == pygame.K_LEFT:  # player 1
            green_image = self.original_image.copy()
            arr = pygame.surfarray.pixels3d(green_image)
            arr[:, :, 0] = 0
            arr[:, :, 1] = 255
            arr[:, :, 2] = 0
            del arr
            self.original_image = green_image

        # Change color of player 2
        if key_left == pygame.K_a:  # player 2
            blue_image = self.original_image.copy()
            arr = pygame.surfarray.pixels3d(blue_image)
            arr[:, :, 0] = 50
            arr[:, :, 1] = 50
            arr[:, :, 2] = 180
            del arr
            self.original_image = blue_image

    # UPDATE METHOD
    def update(self):
        keys = pygame.key.get_pressed()
        # Save old position to check collision with walls
        old_x, old_y = self.rect.x, self.rect.y
        # Rotate
        if keys[self.key_left]:
            self.angle += self.rotation_speed
        if keys[self.key_right]:
            self.angle -= self.rotation_speed
        # Update image and rect
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        # Move when up key is pressed
        if self.key_up and keys[self.key_up]:
            rad = math.radians(self.angle - 270)
            self.rect.x += math.cos(rad) * 2
            self.rect.y -= math.sin(rad) * 2
        # Rotation when hit
        if self.hit_time:
            if pygame.time.get_ticks() - self.hit_time < 500:  # rotate for 0.5s
                self.angle += 30
            else:
                self.hit_time = None
                self.rect.center = (
                    random.randint(0, WINDOW_WIDTH),
                    random.randint(0, WINDOW_HEIGHT)
                )
        # Screen wrap-around
        if self.rect.centerx < 0:
            self.rect.centerx = WINDOW_WIDTH
        elif self.rect.centerx > WINDOW_WIDTH:
            self.rect.centerx = 0
        if self.rect.centery < 0:
            self.rect.centery = WINDOW_HEIGHT
        elif self.rect.centery > WINDOW_HEIGHT:
            self.rect.centery = 0
        # Collision with walls
        for wall in walls:
            if self.rect.colliderect(wall):
                self.rect.x = old_x
                self.rect.y = old_y
                break


# CREATE PLAYERS
player1 = Player(
    x=150,
    y=430,
    key_left=pygame.K_LEFT,
    key_right=pygame.K_RIGHT,
    key_up=pygame.K_UP,
    image_path=("atividade007\\tank\\tanque.png")
)

player2 = Player(
    x=874,
    y=430,
    key_left=pygame.K_a,
    key_right=pygame.K_d,
    key_up=pygame.K_w,
    image_path=("atividade007\\tank\\tanque.png")
)


# CREATE WALLS
def create_combat_map_walls():
    walls = []
    wall1 = pygame.Rect(0, 95, 1024, 32)
    wall2 = pygame.Rect(0, 736, 1024, 32)
    wall3 = pygame.Rect(0, 95, 32, 678)
    wall4 = pygame.Rect(992, 95, 32, 678)
    wall5 = pygame.Rect(320, 406, 96, 50)
    wall6 = pygame.Rect(608, 406, 96, 50)
    wall7 = pygame.Rect(486, 525, 50, 96)
    wall8 = pygame.Rect(486, 240, 50, 96)
    wall9 = pygame.Rect(190, 300, 50, 270)
    wall10 = pygame.Rect(784, 300, 50, 270)
    walls.extend([
        wall1, wall2, wall3, wall4, wall5,
        wall6, wall7, wall8, wall9, wall10
    ])
    return walls


walls = create_combat_map_walls()


# MAIN LOOP
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # PLAYER CONTROLS
        if event.type == pygame.KEYDOWN:

            # Player 1 movement and shooting
            if event.key == pygame.K_DOWN:
                sound_shot.play()
                current_time = pygame.time.get_ticks()
                if current_time - last_shot_time_1 >= shot_cooldown:
                    last_shot_time_1 = current_time  # update last shot time
                    rad = math.radians(player1.angle - 270)
                    tip_offset = player1.original_image.get_height() / 2
                    tip_x = player1.rect.centerx + math.cos(rad) * tip_offset
                    tip_y = player1.rect.centery - math.sin(rad) * tip_offset
                    shot_dx = math.cos(rad) * shot_speed
                    shot_dy = -math.sin(rad) * shot_speed
                    rect_x = int(tip_x - shot_size // 2)
                    rect_y = int(tip_y - shot_size // 2)
                    shots.append({
                        "rect": pygame.Rect(
                            rect_x, rect_y, shot_size, shot_size
                        ),
                        "dx": shot_dx,
                        "dy": shot_dy,
                        "born_time": current_time,
                        "color": GREEN,
                        "owner": "player1"
                    })

            # Player 2 movement and shooting
            if event.key == pygame.K_s:
                sound_shot.play()
                current_time = pygame.time.get_ticks()
                if current_time - last_shot_time_2 >= shot_cooldown:
                    last_shot_time_2 = current_time
                    rad = math.radians(player2.angle - 270)
                    tip_offset = player2.original_image.get_height() / 2
                    tip_x = player2.rect.centerx + math.cos(rad) * tip_offset
                    tip_y = player2.rect.centery - math.sin(rad) * tip_offset
                    shot_dx = math.cos(rad) * shot_speed
                    shot_dy = -math.sin(rad) * shot_speed
                    rect_x = int(tip_x - shot_size // 2)
                    rect_y = int(tip_y - shot_size // 2)
                    shots.append({
                        "rect": pygame.Rect(
                            rect_x, rect_y, shot_size, shot_size
                        ),
                        "dx": shot_dx,
                        "dy": shot_dy,
                        "born_time": current_time,
                        "color": BLUE,
                        "owner": "player2"
                    })

    screen.fill(BROWN)
    player1.update()
    player2.update()

    # BULLETS UPDATE AND DRAW
    current_time = pygame.time.get_ticks()
    for shot in shots[:]:
        # Collision with player 1
        if (
            shot["owner"] != "player1"
            and shot["rect"].colliderect(player1.rect)
        ):
            sound_collision.play()
            player1_health -= 1
            player2_score += 1
            player1.hit_time = pygame.time.get_ticks()
            shots.remove(shot)
            continue
        # Collision with player 2
        if (
            shot["owner"] != "player2"
            and shot["rect"].colliderect(player2.rect)
        ):
            sound_collision.play()
            player2_health -= 1
            player2.hit_time = pygame.time.get_ticks()
            player1_score += 1
            shots.remove(shot)
            continue
        # Collision with walls
        for wall in walls:
            if shot["rect"].colliderect(wall):
                shots.remove(shot)
                break
        shot["rect"].x += shot["dx"]
        shot["rect"].y += shot["dy"]
        pygame.draw.rect(screen, (shot["color"]), shot["rect"])
        # Screen wrap-around for bullets
        if shot["rect"].top < 0:
            shot["rect"].bottom = WINDOW_HEIGHT
        elif shot["rect"].bottom > WINDOW_HEIGHT:
            shot["rect"].top = 0
        if shot["rect"].left < 0:
            shot["rect"].right = WINDOW_WIDTH
        elif shot["rect"].right > WINDOW_WIDTH:
            shot["rect"].left = 0
        if current_time - shot["born_time"] >= shot_lifetime:
            shots.remove(shot)

    # DRAW PLAYERS
    screen.blit(player1.image, player1.rect)
    screen.blit(player2.image, player2.rect)

    # PLAYER 1 SCORE
    score_text1 = font.render(f"{player1_score}", True, GREEN)
    screen.blit(score_text1, (256, 20))

    # PLAYER 2 SCORE
    score_text2 = font.render(f"{player2_score}", True, BLUE)
    screen.blit(score_text2, (768, 20))

    # PLAYER 1 WINS
    score_win1 = font.render("Player 1 Wins", True, GREEN)
    if player1_score >= 3:
        screen.fill(BROWN)
        screen.blit(score_win1, (66, 140))

    # PLAYER 2 WINS
    score_win2 = font.render("Player 2 Wins", True, BLUE)
    if player2_score >= 3:
        screen.fill(BROWN)
        screen.blit(score_win2, (66, 140))

    for wall in walls:
        pygame.draw.rect(screen, YELLOW, wall)

    pygame.display.flip()
    clock.tick(60)
