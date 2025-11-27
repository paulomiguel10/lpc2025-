import pygame
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

pygame.mixer.init()

# SOUNDS
BASE = Path(__file__).resolve().parent
sound_shot = pygame.mixer.Sound("JogoFinal/sounds/fire.wav")
break_asteroid = pygame.mixer.Sound("JogoFinal/sounds/bangMedium.wav")
ufo_sound = pygame.mixer.Sound("JogoFinal/sounds/ufo_sound.mp3")
ufo_death = pygame.mixer.Sound("JogoFinal/sounds/bangSmall.wav")
