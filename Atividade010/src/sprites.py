import math
import os
from random import uniform
import pygame as pg
import config as C
from utils import Vec, angle_to_vec, draw_circle, draw_poly, wrap_pos
from config import WIDTH, HEIGHT, FPS
from PIL import Image

# Caminho base do projeto
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Caminho da imagem de fundo
BACKGROUND_PATH = os.path.join(BASE_DIR, "sprites", "cenario.png")

background = pg.image.load(BACKGROUND_PATH)
background = pg.transform.scale(background, (WIDTH, HEIGHT))

# Caminho base do projeto
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Caminho da imagem de fundo
MENU_PATH = os.path.join(BASE_DIR, "sprites", "menu_game.png")

menu = pg.image.load(MENU_PATH)
menu = pg.transform.scale(menu, (WIDTH, HEIGHT))

class Bullet(pg.sprite.Sprite):
    def __init__(self, pos: Vec, vel: Vec, owner: str = "ship"):
        super().__init__()
        self.pos = Vec(pos)
        self.vel = Vec(vel)
        self.ttl = 0.6
        self.r = 2
        self.owner = owner

        self.image = pg.Surface((self.r * 2, self.r * 2), pg.SRCALPHA)
        self.rect = self.image.get_rect(center=self.pos)

    def update(self, dt: float):
        self.pos += self.vel * dt
        self.pos = wrap_pos(self.pos)
        self.ttl -= dt
        if self.ttl <= 0:
            self.kill()
        self.rect.center = self.pos

    def draw(self, surf: pg.Surface):
        draw_circle(surf, self.pos, self.r)


class Ship(pg.sprite.Sprite):
    instance = None

    def __init__(self, pos: Vec):
        super().__init__()
        self.pos = Vec(pos)
        self.vel = Vec(0, 0)
        self.angle = -90
        self.r = C.SHIP_RADIUS
        self.cool = 0.0
        self.invuln = C.SAFE_SPAWN_TIME

        self.image = pg.Surface((self.r * 2, self.r * 2), pg.SRCALPHA)
        self.rect = self.image.get_rect(center=self.pos)

        Ship.instance = self

    def rotate(self, dir: float, dt: float):
        self.angle += dir * C.SHIP_TURN_SPEED * dt

    def accelerate(self, dt: float):
        dirv = angle_to_vec(self.angle)
        self.vel += dirv * C.SHIP_THRUST * dt

    def update(self, dt: float, keys):
        if keys[pg.K_LEFT]:
            self.rotate(-1, dt)
        if keys[pg.K_RIGHT]:
            self.rotate(1, dt)

        # Aceleração
        if keys[pg.K_UP]:
            self.accelerate(dt)
        else:
            # Sem tecla de acelerar: para completamente
            self.vel.xy = (0, 0)

        # Fogo
        if keys[pg.K_SPACE]:
            self.fire()

        # Hiperespaço
        if keys[pg.K_LSHIFT] or keys[pg.K_RSHIFT]:
            self.hyperspace()

        if self.cool > 0:
            self.cool -= dt
        if self.invuln > 0:
            self.invuln -= dt

        self.pos += self.vel * dt
        self.pos = wrap_pos(self.pos)
        self.rect.center = self.pos

    def fire(self) -> "Bullet | None":
        if self.cool > 0:
            return None
        dirv = angle_to_vec(self.angle)
        pos = self.pos + dirv * (self.r + 6)
        vel = self.vel + dirv * C.SHIP_BULLET_SPEED
        self.cool = C.SHIP_FIRE_RATE
        return Bullet(pos, vel)

    def hyperspace(self):
        self.pos = Vec(uniform(0, C.WIDTH), uniform(0, C.HEIGHT))
        self.vel.xy = (0, 0)
        self.invuln = 1.0

    def draw(self, surf: pg.Surface):
        dirv = angle_to_vec(self.angle)
        left = angle_to_vec(self.angle + 140)
        right = angle_to_vec(self.angle - 140)

        tip = self.pos + dirv * self.r
        left_pt = self.pos + left * self.r * 0.8
        right_pt = self.pos + right * self.r * 0.8

        draw_poly(surf, [tip, left_pt, right_pt])

        if self.invuln > 0:
            # contorno de invulnerabilidade
            draw_circle(surf, self.pos, self.r + 3)

zombiemov_gif = os.path.join(BASE_DIR,"sprites","zombie_anda.gif")

class UFO(pg.sprite.Sprite):
    def __init__(self, pos: Vec, target: pg.sprite.Sprite):
        super().__init__()
        self.speed = 60
        self.turn_rate = math.radians(120)
        self.atual = 0  
        self.anim_timer = 0
        self.anim_speed = 0.12 #segundos por frame
        self.r = 16

        # Carregar sprites
        gif = Image.open(zombiemov_gif)
        self.sprites = []

        try:
            while True:
                gif.seek(len(self.sprites))
                frame = gif.copy().convert("RGBA")
                zombiewalk_img = pg.image.fromstring(frame.tobytes(), frame.size, frame.mode)

                # ESCALA
                zombiewalk_img = pg.transform.scale(zombiewalk_img, (32, 48))

                self.sprites.append(zombiewalk_img)
        except EOFError:
            pass
        
        self.image = self.sprites[0]
        self.rect = self.image.get_rect(center = pos)

        self.pos = Vec(pos)
        self.target = target
        self.dir = Vec(1, 0)

    def update(self, dt: float):
        # Aim at target (ship)
        if self.target and hasattr(self.target, "pos"):
            to_ship = self.target.pos - self.pos
            if to_ship.length_squared() > 0:
                desired_dir = to_ship.normalize()

                # Current angle and desired angle
                current_angle = math.atan2(self.dir.y, self.dir.x)
                desired_angle = math.atan2(desired_dir.y, desired_dir.x)

                # Shortest angle difference
                angle_diff = (desired_angle - current_angle + math.pi) % (
                    2 * math.pi
                ) - math.pi

                max_step = self.turn_rate * dt
                if angle_diff > max_step:
                    angle_diff = max_step
                elif angle_diff < -max_step:
                    angle_diff = -max_step

                new_angle = current_angle + angle_diff
                self.dir = Vec(math.cos(new_angle), math.sin(new_angle))
        # Movement
        self.pos += self.dir * self.speed * dt
        self.pos = wrap_pos(self.pos)
        self.rect.center = self.pos
        #Animation
        self.anim_timer += dt
        if self.anim_timer >= self.anim_speed:
            self.anim_timer = 0
            self.atual = (self.atual + 1) % len(self.sprites)
            
            self.image = self.sprites[self.atual]
            self.rect = self.image.get_rect(center =self.rect.center)

    def draw(self, surf: pg.Surface):
        surf.blit(self.image, self.rect)