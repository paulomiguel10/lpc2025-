import pygame
import math
import random
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

pygame.init()
pygame.mixer.init()

#CONSTANTS
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
pygame.display.set_caption("Core")

clock = pygame.time.Clock()
shots = []

#SOUNDS
BASE = Path(__file__).resolve().parent
sound_shot = pygame.mixer.Sound(str(BASE / "shotsound.mp3"))
sound_collision = pygame.mixer.Sound(str(BASE / "colision_sound.mp3"))

#FONT
font = pygame.font.Font(str(BASE / "PressStart2P-Regular.ttf"), 70)


#PLAYER CLASS 
class Player:
    def __init__(self, x, y, key_left, key_right, image_path, key_up=None, toggle=False, color_mode=None):
        self.key_left = key_left
        self.key_right = key_right
        self.key_up = key_up
        self.toggle = toggle
        self.moving = False
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.original_image = pygame.transform.scale_by(self.original_image, 5)
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))
        self.angle = 0
        self.rotation_speed = 3
        self.hit_time = None
        self.score = 0

        # Color adjustment
        if key_left == pygame.K_LEFT:
            img = self.original_image.copy()
            arr = pygame.surfarray.pixels3d(img)
            if color_mode == "tank":
                arr[:, :, :] = [0, 255, 0]
            else:
                arr[:, :, :] = [0, 255, 0]
            del arr
            self.original_image = img
        elif key_left == pygame.K_a:
            img = self.original_image.copy()
            arr = pygame.surfarray.pixels3d(img)
            if color_mode == "tank":
                arr[:, :, :] = [50, 50, 180]
            else:
                arr[:, :, :] = [255, 75, 10]
            del arr
            self.original_image = img

    def toggle_movement(self):
        self.moving = not self.moving

    def update(self, walls=None):
        keys = pygame.key.get_pressed()

        # Save old position to restore after wall collision
        old_x, old_y = self.rect.x, self.rect.y

        # Rotation
        if keys[self.key_left]:
            self.angle += self.rotation_speed
        if keys[self.key_right]:
            self.angle -= self.rotation_speed

        # Apply rotation
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        # Movement
        if self.toggle:
            if self.moving:
                rad = math.radians(self.angle - 270)
                self.rect.x += math.cos(rad) * 6
                self.rect.y -= math.sin(rad) * 6
        elif self.key_up and keys[self.key_up]:
            rad = math.radians(self.angle - 270)
            self.rect.x += math.cos(rad) * 2
            self.rect.y -= math.sin(rad) * 2

        # Wall collision 
        if walls:
            for wall in walls:
                if self.rect.colliderect(wall):
                    self.rect.x, self.rect.y = old_x, old_y
                    break

        # Respawn inside play area
        if self.hit_time:
            if pygame.time.get_ticks() - self.hit_time < 500:
                self.angle += 30
            else:
                self.hit_time = None
                if walls:
                   spawned = False
                while not spawned:
                    new_x = random.randint(walls[2].right + 40, walls[3].left - 40)
                    new_y = random.randint(walls[0].bottom + 40, walls[1].top - 40)
                    self.rect.center = (new_x, new_y)

                    # Check collides with walls
                    if not any(self.rect.colliderect(w) for w in walls):
                        spawned = True

#MAIN LOOP 
def main_loop(
    player1, player2, walls,
    shot_cooldown, shot_lifetime,
    shot_size, shot_speed,
    background_color, color_player2,
    draw_extra=None
):
    last_shot_time_1 = 0
    last_shot_time_2 = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                #PLAYER 1 TOGGLE MOVEMENT
                if player1.toggle and event.key == pygame.K_w:
                    player1.toggle_movement()

                #PLAYER 2 TOGGLE MOVEMENT
                if player2.toggle and event.key == pygame.K_UP:
                    player2.toggle_movement()

                #PLAYER 1 SHOOT
                if event.key == pygame.K_DOWN:
                    sound_shot.play()
                    now = pygame.time.get_ticks()
                    if now - last_shot_time_1 >= shot_cooldown:
                        last_shot_time_1 = now
                        rad = math.radians(player1.angle - 270)
                        tip_x = player1.rect.centerx + math.cos(rad) * 25
                        tip_y = player1.rect.centery - math.sin(rad) * 25
                        shots.append({
                            "rect": pygame.Rect(tip_x, tip_y, shot_size, shot_size),
                            "dx": math.cos(rad) * shot_speed,
                            "dy": -math.sin(rad) * shot_speed,
                            "born": now,
                            "color": GREEN,
                            "owner": "p1"
                        })

                #PLAYER 2 SHOOT 
                if event.key == pygame.K_s:
                    sound_shot.play()
                    now = pygame.time.get_ticks()
                    if now - last_shot_time_2 >= shot_cooldown:
                        last_shot_time_2 = now
                        rad = math.radians(player2.angle - 270)
                        tip_x = player2.rect.centerx + math.cos(rad) * 25
                        tip_y = player2.rect.centery - math.sin(rad) * 25
                        shots.append({
                            "rect": pygame.Rect(tip_x, tip_y, shot_size, shot_size),
                            "dx": math.cos(rad) * shot_speed,
                            "dy": -math.sin(rad) * shot_speed,
                            "born": now,
                            "color": color_player2,
                            "owner": "p2"
                        })

        #UPDATE
        player1.update(walls)
        player2.update(walls)

        #BULLETS
        for shot in shots[:]:
            shot["rect"].x += shot["dx"]
            shot["rect"].y += shot["dy"]

            if shot["owner"] == "p1" and shot["rect"].colliderect(player2.rect):
                sound_collision.play()
                player1.score += 1
                player2.hit_time = pygame.time.get_ticks()
                shots.remove(shot)
                continue
            elif shot["owner"] == "p2" and shot["rect"].colliderect(player1.rect):
                sound_collision.play()
                player2.score += 1
                player1.hit_time = pygame.time.get_ticks()
                shots.remove(shot)
                continue

            if walls:
                for wall in walls:
                    if shot["rect"].colliderect(wall):
                        shots.remove(shot)
                        break

            if pygame.time.get_ticks() - shot["born"] > shot_lifetime:
                shots.remove(shot)

        #DRAW 
        screen.fill(background_color)
        if walls:
            for wall in walls:
                pygame.draw.rect(screen, YELLOW, wall)
        for shot in shots:
            pygame.draw.rect(screen, shot["color"], shot["rect"])
        screen.blit(player1.image, player1.rect)
        screen.blit(player2.image, player2.rect)

        # Extra drawing 
        if draw_extra:
            draw_extra()

        # Scores
        s1 = font.render(str(player1.score), True, GREEN)
        s2 = font.render(str(player2.score), True, color_player2)
        screen.blit(s1, (250, 20))
        screen.blit(s2, (750, 20))

        # Win check
        if player1.score >= 3:
            screen.fill(background_color)
            win = font.render("Player 1 Wins", True, GREEN)
            win_rect = win.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            screen.blit(win, win_rect)
        elif player2.score >= 3:
            screen.fill(background_color)
            win = font.render("Player 2 Wins", True, color_player2)
            win_rect = win.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            screen.blit(win, win_rect)

        pygame.display.flip()
        clock.tick(60)
