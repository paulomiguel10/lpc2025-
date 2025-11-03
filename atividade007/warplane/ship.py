import sys
from pathlib import Path
import pygame
import math
import random
sys.path.append(str(Path(__file__).resolve().parents[1]))
from core.core import (
    Player, DARK_BLUE, WINDOW_WIDTH, WINDOW_HEIGHT,
    ORANGE, screen, main_loop
)


# SHIP SPECIFIC SETTINGS
shot_cooldown = 200      # time between shots
shot_lifetime = 350      # bullet lifespan
shot_size = 5            # bullet size
shot_speed = 15          # bullet speed
background_color = DARK_BLUE
color_mode = "ship"
walls = None  # no barriers


# SHIP PLAYER CLASS
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


# PLAYER INSTANCES
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


# CLOUD DRAWING FUNCTION
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


# MAIN LOOP
def ship_loop():
    main_loop(
        player1, player2, walls,
        shot_cooldown, shot_lifetime, shot_size,
        shot_speed, background_color, ORANGE,
    )


# START GAME
ship_loop()