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
AMARELO = (255, 180, 0)
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
sound_colision = pygame.mixer.Sound(
    str(BASE.parent / "core" / "colision_sound.mp3")
)
# game font
font = pygame.font.Font("atividade007\\core\\PressStart2P-Regular.ttf", 70)


class player:

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

        # Muda cor do player 1
        if key_left == pygame.K_LEFT:  # player 1
            green_image = self.original_image.copy()
            arr = pygame.surfarray.pixels3d(green_image)
            arr[:, :, 0] = 0
            arr[:, :, 1] = 255
            arr[:, :, 2] = 0
            del arr
            self.original_image = green_image

        # Muda cor do player 2
        if key_left == pygame.K_a:  # player 2
            orange_image = self.original_image.copy()
            arr = pygame.surfarray.pixels3d(orange_image)
            arr[:, :, 0] = 50
            arr[:, :, 1] = 50
            arr[:, :, 2] = 180
            del arr
            self.original_image = orange_image

    # UPDATE METHOD
    def update(self):
        keys = pygame.key.get_pressed()
        # Salva posição antiga para checar colisão com paredes
        old_x, old_y = self.rect.x, self.rect.y
        # Rotate
        if keys[self.key_left]:
            self.angle += self.rotation_speed
        if keys[self.key_right]:
            self.angle -= self.rotation_speed
        # Att image and rect
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        # Move when up key is pressed
        if self.key_up and keys[self.key_up]:
            rad = math.radians(self.angle - 270)
            self.rect.x += math.cos(rad) * 2
            self.rect.y -= math.sin(rad) * 2
        # Rotation when hit
        if self.hit_time:
            if pygame.time.get_ticks() - self.hit_time < 500:  # rotate 0.5s
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
        for parede in paredes:
            if self.rect.colliderect(parede):
                self.rect.x = old_x
                self.rect.y = old_y
                break


# CREATING PLAYERS
# player 1
player1 = player(
    x=150,
    y=430,
    key_left=pygame.K_LEFT,
    key_right=pygame.K_RIGHT,
    key_up=pygame.K_UP,  # tecla para andar
    image_path=("atividade007\\tank\\tanque.png"))

# player 2
player2 = player(
    x=874,
    y=430,
    key_left=pygame.K_a,
    key_right=pygame.K_d,
    key_up=pygame.K_w,  # tecla para andar
    image_path=("atividade007\\tank\\tanque.png"))


# CREATING WALLS
def criar_paredes_mapa_combat():
    paredes = []
    parede1 = pygame.Rect(0, 95, 1024, 32)
    parede2 = pygame.Rect(0, 736, 1024, 32)
    parede3 = pygame.Rect(0, 95, 32, 678)
    parede4 = pygame.Rect(992, 95, 32, 678)
    parede5 = pygame.Rect(320, 406, 96, 50)
    parede6 = pygame.Rect(608, 406, 96, 50)
    parede7 = pygame.Rect(486, 525, 50, 96)
    parede8 = pygame.Rect(486, 240, 50, 96)
    parede9 = pygame.Rect(190, 300, 50, 270)
    parede10 = pygame.Rect(784, 300, 50, 270)
    paredes.append(parede1)
    paredes.append(parede2)
    paredes.append(parede3)
    paredes.append(parede4)
    paredes.append(parede5)
    paredes.append(parede6)
    paredes.append(parede7)
    paredes.append(parede8)
    paredes.append(parede9)
    paredes.append(parede10)
    return paredes


paredes = criar_paredes_mapa_combat()


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
                    # Convert angle to match ship movement
                    rad = math.radians(player1.angle - 270)
                    # distance from center to tip
                    tip_offset = player1.original_image.get_height() / 2
                    # Calculate ship tip coordinates when shooting
                    tip_x = player1.rect.centerx + math.cos(rad) * tip_offset
                    tip_y = player1.rect.centery - math.sin(rad) * tip_offset
                    # Bullet direction: same vector used for ship movement
                    shot_dx = math.cos(rad) * shot_speed
                    shot_dy = -math.sin(rad) * shot_speed
                    # Add bullet to list
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
            if event.key == pygame.K_s:  # Player 2 shoots
                sound_shot.play()
                current_time = pygame.time.get_ticks()
                if current_time - last_shot_time_2 >= shot_cooldown:
                    last_shot_time_2 = current_time  # update last shot time
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
            sound_colision.play()
            player1_health -= 1
            player2_score += 1
            player1.hit_time = pygame.time.get_ticks()  # activate rotation
            shots.remove(shot)
            continue
        # Collision with player 2
        if (
            shot["owner"] != "player2"
            and shot["rect"].colliderect(player2.rect)
        ):
            sound_colision.play()
            player2_health -= 1
            player2.hit_time = pygame.time.get_ticks()  # activate rotation
            player1_score += 1
            shots.remove(shot)
            continue
        # Collision with walls
        for parede in paredes:
            if shot["rect"].colliderect(parede):
                shots.remove(shot)  # remove the shot
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

    # Draw players
    screen.blit(player1.image, player1.rect)
    screen.blit(player2.image, player2.rect)
    # Player 1 score
    score_text1 = font.render(f"{player1_score}", True, GREEN)
    screen.blit(score_text1, (256, 20))
    # Player 2 score
    score_text2 = font.render(f"{player2_score}", True, BLUE)
    screen.blit(score_text2, (768, 20))
    # Player 1 WINS
    score_win1 = font.render("Player 1 Wins", True, GREEN)
    if player1_score >= 3:
        screen.fill(BROWN)
        screen.blit(score_win1, (66, 140))
    # Player 2 WINS
    score_win2 = font.render("Player 2 Wins", True, BLUE)
    if player2_score >= 3:
        screen.fill(BROWN)
        screen.blit(score_win2, (66, 140))
    for parede in paredes:
        pygame.draw.rect(screen, AMARELO, parede)

    pygame.display.flip()
    clock.tick(60)
