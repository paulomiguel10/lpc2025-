import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from core.core import *
import pygame
import math
import random

#SHIP SPECIFIC SETTINGS
shot_cooldown = 200      # time between shots 
shot_lifetime = 350      # bullet lifespan 
shot_size = 5            # bullet size
shot_speed = 15          # bullet speed
background_color = DARK_BLUE
color_mode = "ship"
walls = None  # no barriers 

# LAYER CLASS
class ShipPlayer(Player):
    def update(self, walls=None):
        keys = pygame.key.get_pressed()

        # Rotation and hit-time 
        if self.hit_time:
            if pygame.time.get_ticks() - self.hit_time < 500:
                self.angle += 30
            else:
                self.hit_time = None
                self.rect.center = (
                    random.randint(0, WINDOW_WIDTH),
                    random.randint(0, WINDOW_HEIGHT)
                )

        # Rotation
        if keys[self.key_left]:
            self.angle += self.rotation_speed
        if keys[self.key_right]:
            self.angle -= self.rotation_speed

        # Update rotated image and hitbox
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        # Continuous movement
        if self.moving:
            rad = math.radians(self.angle - 270)
            self.rect.x += math.cos(rad) * 6
            self.rect.y -= math.sin(rad) * 6

        # Screen wrap-around
        if self.rect.centerx < 0:
            self.rect.centerx = WINDOW_WIDTH
        elif self.rect.centerx > WINDOW_WIDTH:
            self.rect.centerx = 0
        if self.rect.centery < 0:
            self.rect.centery = WINDOW_HEIGHT
        elif self.rect.centery > WINDOW_HEIGHT:
            self.rect.centery = 0


#PLAYER INSTANCES
player1 = ShipPlayer(
    x=WINDOW_WIDTH // 5,
    y=WINDOW_HEIGHT // 5,
    key_left=pygame.K_LEFT,
    key_right=pygame.K_RIGHT,
    image_path="atividade007/warplane/aviao.png",
    toggle=True,
    color_mode=color_mode
)

player2 = ShipPlayer(
    x=WINDOW_WIDTH * 4 // 5,
    y=WINDOW_HEIGHT * 4 // 5,
    key_left=pygame.K_a,
    key_right=pygame.K_d,
    image_path="atividade007/warplane/aviao.png",
    toggle=True,
    color_mode=color_mode
)


#CLOUD DRAWING FUNCTION 
def draw_pixel_clouds():
    cloud_color = (100, 170, 255)

    def draw_pixel_cloud(x, y, scale=25):
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


#MAIN LOOP 
def ship_loop():
    last_shot_time_1 = 0
    last_shot_time_2 = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            #PLAYER 1 CONTROLS
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:  # toggle movement
                    player1.toggle_movement()
                if event.key == pygame.K_DOWN:  # shoot
                    now = pygame.time.get_ticks()
                    if now - last_shot_time_1 >= shot_cooldown:
                        sound_shot.play()
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

                #PLAYER 2 CONTROLS 
                if event.key == pygame.K_w:  # toggle movement
                    player2.toggle_movement()
                if event.key == pygame.K_s:  # shoot
                    now = pygame.time.get_ticks()
                    if now - last_shot_time_2 >= shot_cooldown:
                        sound_shot.play()
                        last_shot_time_2 = now
                        rad = math.radians(player2.angle - 270)
                        tip_x = player2.rect.centerx + math.cos(rad) * 25
                        tip_y = player2.rect.centery - math.sin(rad) * 25
                        shots.append({
                            "rect": pygame.Rect(tip_x, tip_y, shot_size, shot_size),
                            "dx": math.cos(rad) * shot_speed,
                            "dy": -math.sin(rad) * shot_speed,
                            "born": now,
                            "color": ORANGE,
                            "owner": "p2"
                        })

        #UPDATE 
        player1.update()
        player2.update()

        #BULLETS
        current_time = pygame.time.get_ticks()
        for shot in shots[:]:
            shot["rect"].x += shot["dx"]
            shot["rect"].y += shot["dy"]

            # Bullet wrap-around
            if shot["rect"].top < 0:
                shot["rect"].bottom = WINDOW_HEIGHT
            elif shot["rect"].bottom > WINDOW_HEIGHT:
                shot["rect"].top = 0
            if shot["rect"].left < 0:
                shot["rect"].right = WINDOW_WIDTH
            elif shot["rect"].right > WINDOW_WIDTH:
                shot["rect"].left = 0

            # Collisions
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

            # Remove expired bullets
            if current_time - shot["born"] > shot_lifetime:
                shots.remove(shot)

        #DRAW 
        screen.fill(background_color)
        for shot in shots:
            pygame.draw.rect(screen, shot["color"], shot["rect"])
        screen.blit(player1.image, player1.rect)
        screen.blit(player2.image, player2.rect)
        draw_pixel_clouds()

        # Scoreboard
        s1 = font.render(str(player1.score), True, GREEN)
        s2 = font.render(str(player2.score), True, ORANGE)
        screen.blit(s1, (256, 20))
        screen.blit(s2, (768, 20))

        # Check victory
        if player1.score >= 3:
            screen.fill(background_color)
            win = font.render("Player 1 Wins", True, GREEN)
            win_rect = win.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            screen.blit(win, win_rect)
            pygame.display.flip()
            pygame.time.wait(3000)
            running = False
            continue
        elif player2.score >= 3:
            screen.fill(background_color)
            win = font.render("Player 2 Wins", True, ORANGE)
            win_rect = win.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            screen.blit(win, win_rect)
            pygame.display.flip()
            pygame.time.wait(3000)
            running = False
            continue

        pygame.display.flip()
        clock.tick(60)


# START GAME
ship_loop()