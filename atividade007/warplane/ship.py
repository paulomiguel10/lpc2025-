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
GAME_WIDTH, GAME_HEIGHT = 256, 192
SCALE_FACTOR = 4
WINDOW_WIDTH = GAME_WIDTH * SCALE_FACTOR
WINDOW_HEIGHT = GAME_HEIGHT * SCALE_FACTOR
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Little Plane Comabat")
clock = pygame.time.Clock()
last_shot_time_1 = 0  # ms
last_shot_time_2 = 0  # ms
shot_cooldown = 200  # ms
shot_lifetime = 350  # ms
running = True  # main loop control
shots = []  # list to store bullets
shot_size = 5   # bullet size
shot_speed = 15  # bullet speed (+ or - depending on direction)
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
# GAME FONT
font = pygame.font.Font("atividade007\\core\\PressStart2P-Regular.ttf", 70)


# PLAYER CLASS
class player:
    def __init__(self, x, y, key_left, key_right, image_path, ):
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.original_image = pygame.transform.scale_by(self.original_image, 5)
        self.hit_time = None
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))
        self.angle = 0  # 0° pointing upward
        self.rotation_speed = 3  # rotation speed
        self.moving = False
        self.key_left = key_left
        self.key_right = key_right
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        # CHANGE COLOR FOR PLAYER 1
        if key_left == pygame.K_LEFT:  # identifies player 1
            green_image = self.original_image.copy()
            arr = pygame.surfarray.pixels3d(green_image)  # access all pixels
            arr[:, :, 0] = 0  # R
            arr[:, :, 1] = 255  # G
            arr[:, :, 2] = 0  # B
            del arr
            self.original_image = green_image

        # CHANGE COLOR FOR PLAYER 2
        if key_left == pygame.K_a:  # identifies player 2
            orange_image = self.original_image.copy()
            arr = pygame.surfarray.pixels3d(orange_image)  # access all pixels
            arr[:, :, 0] = 255  # R
            arr[:, :, 1] = 75  # G
            arr[:, :, 2] = 10  # B
            del arr
            self.original_image = orange_image

    def toggle_movement(self):
        self.moving = not self.moving  # toggle on/off

    def update(self):
        keys = pygame.key.get_pressed()

        # Rotate when hit and respawn in a random position
        if self.hit_time:
            if pygame.time.get_ticks() - self.hit_time < 500:
                self.angle += 30
            else:
                self.hit_time = None
                self.rect.center = (
                    random.randint(0, WINDOW_WIDTH),
                    random.randint(0, WINDOW_HEIGHT))

        # Ship rotation
        if keys[self.key_left]:
            self.angle += self.rotation_speed
        if keys[self.key_right]:
            self.angle -= self.rotation_speed

        # Move forward; image "top" is considered the front
        if self.moving:
            rad = math.radians(self.angle - 270)  # subtract to align
            self.rect.x += math.cos(rad) * 6
            self.rect.y -= math.sin(rad) * 6  # inverted for pygame coordinates

        # Screen wrap-around
        if self.rect.centerx < 0:
            self.rect.centerx = WINDOW_WIDTH
        elif self.rect.centerx > WINDOW_WIDTH:
            self.rect.centerx = 0
        if self.rect.centery < 0:
            self.rect.centery = WINDOW_HEIGHT
        elif self.rect.centery > WINDOW_HEIGHT:
            self.rect.centery = 0


# CREATING PLAYERS
# player 1
player1 = player(
    x=WINDOW_WIDTH // 5,
    y=WINDOW_HEIGHT // 5,
    key_left=pygame.K_LEFT,
    key_right=pygame.K_RIGHT,
    image_path=("atividade007\\warplane\\aviao.png"))

# player 2
player2 = player(
    x=WINDOW_WIDTH * 4 // 5,
    y=WINDOW_HEIGHT * 4 // 5,
    key_left=pygame.K_a,
    key_right=pygame.K_d,
    image_path=("atividade007\\warplane\\aviao.png"))

# MAIN LOOP
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # PLAYERS CONTROLS
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
                            rect_x, rect_y, shot_size, shot_size),
                        "dx": shot_dx,
                        "dy": shot_dy,
                        "born_time": current_time,
                        "color": GREEN,
                        "owner": "player1"})
            if event.key == pygame.K_UP:
                player1.toggle_movement()

            # Player 2 movement and shooting
            if event.key == pygame.K_w:
                player2.toggle_movement()
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
                            rect_x, rect_y, shot_size, shot_size),
                        "dx": shot_dx,
                        "dy": shot_dy,
                        "born_time": current_time,
                        "color": ORANGE,
                        "owner": "player2"})

    screen.fill(DARK_BLUE)
    player1.update()
    player2.update()

    # BULLETS UPDATE AND DRAW
    current_time = pygame.time.get_ticks()
    for shot in shots[:]:

        # Collision with player 1
        if (shot["owner"] != "player1" and
                shot["rect"].colliderect(player1.rect)):
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
    score_text2 = font.render(f"{player2_score}", True, ORANGE)
    screen.blit(score_text2, (768, 20))
    # Player 1 WINS
    score_win1 = font.render("Player 1 Wins", True, GREEN)
    if player1_score >= 3:
        screen.fill(DARK_BLUE)
        screen.blit(score_win1, (66, 100))
    # Player 2 WINS
    score_win2 = font.render("Player 2 Wins", True, ORANGE)
    if player2_score >= 3:
        screen.fill(DARK_BLUE)
        screen.blit(score_win2, (66, 100))
    # Draw clouds on screen
    cloud_color = (100, 170, 255)

    def draw_pixel_cloud(x, y, scale=12):
        pattern = [
            "    XXXX    ",
            "  XXXXXXXX  ",
            " XXXXXXXXXX ",
            "XXXXXXXXXXXX",
            "XXXXXXXXXXXX",
            " XXXXXXXXXX ",
            "  XXXXXXXX  ",
            "    XXXX    "
        ]
        for row_idx, row in enumerate(pattern):
            for col_idx, pixel in enumerate(row):
                if pixel == "X":
                    rect = pygame.Rect(
                        x + col_idx * scale,
                        y + row_idx * scale,
                        scale,
                        scale
                    )
                    pygame.draw.rect(screen, cloud_color, rect)
    draw_pixel_cloud(150, 300, 25)
    draw_pixel_cloud(600, 300, 25)

    pygame.display.flip()
    clock.tick(60)
