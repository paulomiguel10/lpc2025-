import pygame
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

pygame.mixer.init()

# SOUNDS
BASE = Path(__file__).resolve().parent
sound_shot = pygame.mixer.Sound("atividade009/sounds/fire.wav")
break_asteroid = pygame.mixer.Sound("atividade009/sounds/bangMedium.wav")
ufo_sound = pygame.mixer.Sound("atividade009/sounds/ufo_sound.mp3")
ufo_death = pygame.mixer.Sound("atividade009/sounds/bangSmall.wav")
