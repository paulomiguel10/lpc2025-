
import random
import sys
from dataclasses import dataclass
from config import WIDTH, HEIGHT
import pygame as pg
from sprites import menu
import config as C
from systems import World
from utils import text
from sounds import background_menu


@dataclass
class Scene:
    name: str


pg.mixer.init()


class Game:

    def __init__(self):
        pg.init()
        if C.RANDOM_SEED is not None:
            random.seed(C.RANDOM_SEED)
        self.screen = pg.display.set_mode((C.WIDTH, C.HEIGHT))
        pg.display.set_caption("Juci vs Zombies")
        self.clock = pg.time.Clock()
        self.font = pg.font.SysFont("consolas", 20)
        self.big = pg.font.SysFont("consolas", 48)
        self.scene = Scene("menu")
        self.world = World()

    def draw_menu(self):
        self.screen.blit(menu, (0, 0))

    def run(self):
        while True:
            dt = self.clock.tick(C.FPS) / 1000.0
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    pg.quit()
                    sys.exit(0)
                if e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit(0)
                if self.scene.name == "play":
                    if e.type == pg.MOUSEBUTTONDOWN and e.button == 1:
                        self.world.try_fire()
                    if e.type == pg.KEYDOWN and e.key == pg.K_LSHIFT:
                        self.world.hyperspace()
                elif self.scene.name == "menu":
                    if e.type == pg.KEYDOWN:
                        self.scene = Scene("play")

            keys = pg.key.get_pressed()
            self.screen.fill(C.BLACK)

            if self.scene.name == "menu":
                self.draw_menu()
            elif self.scene.name == "play":
                self.world.update(dt, keys)
                self.world.draw(self.screen, self.font)

            pg.display.flip()
