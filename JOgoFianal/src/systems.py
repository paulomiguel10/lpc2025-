
import math
from random import uniform

import pygame as pg
import config as C
from sprites import Ship, UFO
from utils import Vec, rand_edge_pos


class World:

    def __init__(self):
        self.ship = Ship(Vec(C.WIDTH / 2, C.HEIGHT / 2))
        self.bullets = pg.sprite.Group()
        self.ufos = pg.sprite.Group()
        self.all_sprites = pg.sprite.Group(self.ship)
        self.score = 0
        self.lives = C.START_LIVES
        self.safe = C.SAFE_SPAWN_TIME
        self.ufo_timer = C.UFO_SPAWN_EVERY

    def spawn_ufo(self):
        small = True  # apenas naves pequenas
        y = uniform(0, C.HEIGHT)
        x = 0 if uniform(0, 1) < 0.5 else C.WIDTH
        ufo = UFO(Vec(x, y), small)
        ufo.world = self    # ADIÇÂO: referência ao mundo
        self.ufos.add(ufo)
        self.all_sprites.add(ufo)

    def try_fire(self):
        if len(self.bullets) >= C.MAX_BULLETS:
            return
        b = self.ship.fire()
        if b:
            self.bullets.add(b)
            self.all_sprites.add(b)

    def hyperspace(self):
        self.ship.hyperspace()
        self.score = max(0, self.score - C.HYPERSPACE_COST)

    def update(self, dt: float, keys):
        self.all_sprites.update(dt)
        self.ship.control(keys, dt)

        # Timers
        if self.safe > 0:
            self.safe -= dt
            self.ship.invuln = 0.5
        self.ufo_timer -= dt
        if self.ufo_timer <= 0:
            self.spawn_ufo()
            self.ufo_timer = C.UFO_SPAWN_EVERY

        self.handle_collisions()


    def handle_collisions(self):
        if self.ship.invuln <= 0 and self.safe <= 0:
            for ufo in self.ufos:
                if (ufo.pos - self.ship.pos).length() < (ufo.r + self.ship.r):
                    self.ship_die()
                    break

            # ADIÇÂO:
            # Balas dos UFOs acertando a nave
            for b in list(self.bullets):
                if getattr(b, "owner", "ship") == "ufo":
                    if (b.pos - self.ship.pos).length() < (b.r + self.ship.r):
                        self.ship_die()
                        b.kill()
                        break
            # FIM DA ADIÇÂO

        for ufo in list(self.ufos):
            for b in list(self.bullets):
                # ADIÇÂO: só balas da nave podem acertar o UFO
                if getattr(b, "owner", "ship") != "ship":
                    continue
                if (ufo.pos - b.pos).length() < (ufo.r + b.r):
                    self.score += C.UFO_SMALL["score"]
                    ufo.kill()
                    b.kill()

    def ship_die(self):
        self.lives -= 1
        self.ship.pos.xy = (C.WIDTH / 2, C.HEIGHT / 2)
        self.ship.vel.xy = (0, 0)
        self.ship.angle = -90
        self.ship.invuln = C.SAFE_SPAWN_TIME
        self.safe = C.SAFE_SPAWN_TIME
        if self.lives < 0:
            # Reset total
            self.__init__()

    def draw(self, surf: pg.Surface, font: pg.font.Font):
        for spr in self.all_sprites:
            spr.draw(surf)

        pg.draw.line(surf, (60, 60, 60), (0, 50), (C.WIDTH, 50), width=1)
        txt = f"SCORE {self.score:06d}   LIVES {self.lives}"
        label = font.render(txt, True, C.WHITE)
        surf.blit(label, (10, 10))
