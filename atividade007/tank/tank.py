import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1])) 

from core.core import *
import pygame

#Configs
shot_cooldown = 500
shot_lifetime = 500
shot_size = 7
shot_speed = 20
background_color = BROWN
color_mode = "tank"

#Walls 
def create_combat_map_walls():
    walls = []
    walls.append(pygame.Rect(0, 95, 1024, 32))
    walls.append(pygame.Rect(0, 736, 1024, 32))
    walls.append(pygame.Rect(0, 95, 32, 678))
    walls.append(pygame.Rect(992, 95, 32, 678))
    walls.append(pygame.Rect(320, 406, 96, 50))
    walls.append(pygame.Rect(608, 406, 96, 50))
    walls.append(pygame.Rect(486, 525, 50, 96))
    walls.append(pygame.Rect(486, 240, 50, 96))
    walls.append(pygame.Rect(190, 300, 50, 270))
    walls.append(pygame.Rect(784, 300, 50, 270))
    return walls

walls = create_combat_map_walls()

#Players
player1 = Player(150, 430, pygame.K_LEFT, pygame.K_RIGHT, "atividade007/tank/tanque.png", key_up=pygame.K_UP, toggle=False, color_mode=color_mode)
player2 = Player(874, 430, pygame.K_a, pygame.K_d, "atividade007/tank/tanque.png", key_up=pygame.K_w, toggle=False, color_mode=color_mode)

# Start game 
main_loop(player1, player2, walls, shot_cooldown, shot_lifetime, shot_size, shot_speed, background_color, BLUE)
