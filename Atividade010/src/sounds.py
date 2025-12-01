import pygame
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

pygame.mixer.init()

# SOUNDS
BASE = Path(__file__).resolve().parent
sound_shot = pygame.mixer.Sound("atividade010/sounds/shot.mp3")
zombie_sound = pygame.mixer.Sound("atividade010/sounds/zombie_sound.mp3")
background_menu = pygame.mixer.Sound("atividade010/sounds/background_menu.mp3")
zombie_death = pygame.mixer.Sound("atividade010/sounds/zombie_death.mp3")
