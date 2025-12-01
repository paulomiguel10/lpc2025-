import math
from random import uniform

import pygame as pg
import config as C
from sprites import Ship, UFO, background
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
    
    def try_fire(self):
        bullet = self.ship.fire()
        if bullet:
            self.bullets.add(bullet)
            self.all_sprites.add(bullet)

    def spawn_ufo(self):
        side = uniform(0, 4)
        if side < 1:
            pos = Vec(0, uniform(0, C.HEIGHT))
        elif side < 2:
            pos = Vec(C.WIDTH, uniform(0, C.HEIGHT))
        elif side < 3:
            pos = Vec(uniform(0, C.WIDTH), 0)
        else:
            pos = Vec(uniform(0, C.WIDTH), C.HEIGHT)

        ufo = UFO(pos, self.ship)
        self.ufos.add(ufo)
        self.all_sprites.add(ufo)

    def update(self, dt: float, keys):
        self.ship.update(dt, keys)
        self.bullets.update(dt)
        self.ufos.update(dt)

        self.safe -= dt
        self.ufo_timer -= dt

        if self.ufo_timer <= 0:
            self.spawn_ufo()
            self.ufo_timer = C.UFO_SPAWN_EVERY

        # Colisão nave x UFO
        if self.ship.invuln <= 0 and self.safe <= 0:
            for ufo in self.ufos:
                if (ufo.pos - self.ship.pos).length() < (ufo.r + self.ship.r):
                    self.ship_die()
                    break

        for ufo in list(self.ufos):
            for b in list(self.bullets):
                # Só balas da nave podem acertar o UFO
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
        # Desenha o fundo primeiro
        surf.blit(background, (0, 0))
        for spr in self.all_sprites:
            spr.draw(surf)

        pg.draw.line(surf, (60, 60, 60), (0, 50), (C.WIDTH, 50), width=1)
        txt = f"SCORE {self.score:06d}   LIVES {self.lives}"
        label = font.render(txt, True, C.WHITE)
        surf.blit(label, (10, 10))