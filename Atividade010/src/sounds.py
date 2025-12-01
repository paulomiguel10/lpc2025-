import pygame
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

pygame.mixer.init()

# SOUNDS
BASE = Path(__file__).resolve().parent

player_death = pygame.mixer.Sound("atividade010/sounds/player_death.mp3")

sound_shot = pygame.mixer.Sound("atividade010/sounds/shot.mp3")
sound_shot.set_volume(0.3)

zombie_sound = pygame.mixer.Sound("atividade010/sounds/zombie_sound.mp3")
zombie_death = pygame.mixer.Sound("atividade010/sounds/zombie_death.mp3")

background_menu = pygame.mixer_music.load(
    "atividade010/sounds/background_menu.mp3")
background_menu = pygame.mixer.music.set_volume(0.8)
background_menu = pygame.mixer.music.play(-1)
