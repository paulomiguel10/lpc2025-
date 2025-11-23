
import math
from random import uniform
import pygame as pg
from sounds import sound_shot
import config as C
from utils import Vec, angle_to_vec, draw_circle, draw_poly, wrap_pos


class Bullet(pg.sprite.Sprite):
    def __init__(self, pos: Vec, vel: Vec, owner: str = "ship"):
        super().__init__()
        self.pos = Vec(pos)
        self.vel = Vec(vel)
        self.ttl = C.BULLET_TTL
        self.r = C.BULLET_RADIUS
        self.rect = pg.Rect(0, 0, self.r * 2, self.r * 2)
        self.owner = owner


    def update(self, dt: float):
        self.pos += self.vel * dt
        self.pos = wrap_pos(self.pos)
        self.ttl -= dt
        if self.ttl <= 0:
            self.kill()
        self.rect.center = self.pos


    def draw(self, surf: pg.Surface):
        draw_circle(surf, self.pos, self.r)


class Asteroid(pg.sprite.Sprite):
    def __init__(self, pos: Vec, vel: Vec, size: str):
        super().__init__()
        self.pos = Vec(pos)
        self.vel = Vec(vel)
        self.size = size  
        self.r = C.AST_SIZES[size]["r"]
        self.poly = self._make_poly()
        self.rect = pg.Rect(0, 0, self.r * 2, self.r * 2)


    def _make_poly(self):
        steps = 12 if self.size == "L" else 10 if self.size == "M" else 8
        pts = []
        for i in range(steps):
            ang = i * (360 / steps)
            jitter = uniform(0.75, 1.2)
            r = self.r * jitter
            v = Vec(math.cos(math.radians(ang)),
                    math.sin(math.radians(ang)))
            pts.append(v * r)
        return pts


    def update(self, dt: float):
        self.pos += self.vel * dt
        self.pos = wrap_pos(self.pos)
        self.rect.center = self.pos


    def draw(self, surf: pg.Surface):
        pts = [(self.pos + p) for p in self.poly]
        pg.draw.polygon(surf, C.WHITE, pts, width=1)


class Ship(pg.sprite.Sprite):
    instance = None
    def __init__(self, pos: Vec):
        super().__init__()
        self.pos = Vec(pos)
        self.vel = Vec(0, 0)
        self.angle = -90.0
        self.cool = 0.0
        self.invuln = 0.0
        self.alive = True
        self.r = C.SHIP_RADIUS
        self.rect = pg.Rect(0, 0, self.r * 2, self.r * 2)
        Ship.instance = self


    def control(self, keys: pg.key.ScancodeWrapper, dt: float):
        if keys[pg.K_LEFT]:
            self.angle -= C.SHIP_TURN_SPEED * dt
        if keys[pg.K_RIGHT]:
            self.angle += C.SHIP_TURN_SPEED * dt
        if keys[pg.K_UP]:
            self.vel += angle_to_vec(self.angle) * C.SHIP_THRUST * dt
        self.vel *= C.SHIP_FRICTION


    def fire(self) -> Bullet | None:
        if self.cool > 0:
            return None
        sound_shot.play()
        dirv = angle_to_vec(self.angle)
        pos = self.pos + dirv * (self.r + 6)
        vel = self.vel + dirv * C.SHIP_BULLET_SPEED
        self.cool = C.SHIP_FIRE_RATE
        return Bullet(pos, vel)


    def hyperspace(self):
        self.pos = Vec(uniform(0, C.WIDTH), uniform(0, C.HEIGHT))
        self.vel.xy = (0, 0)
        self.invuln = 1.0


    def update(self, dt: float):
        if self.cool > 0:
            self.cool -= dt
        if self.invuln > 0:
            self.invuln -= dt
        self.pos += self.vel * dt
        self.pos = wrap_pos(self.pos)
        self.rect.center = self.pos


    def draw(self, surf: pg.Surface):
        dirv = angle_to_vec(self.angle)
        left = angle_to_vec(self.angle + 140)
        right = angle_to_vec(self.angle - 140)
        p1 = self.pos + dirv * self.r
        p2 = self.pos + left * self.r * 0.9
        p3 = self.pos + right * self.r * 0.9
        draw_poly(surf, [p1, p2, p3])
        if self.invuln > 0 and int(self.invuln * 10) % 2 == 0:
            draw_circle(surf, self.pos, self.r + 6)


class UFO(pg.sprite.Sprite):
    def __init__(self, pos: Vec, small: bool):
        super().__init__()
        self.pos = Vec(pos)
        self.small = small
        self.r = C.UFO_SMALL["r"] if small else C.UFO_BIG["r"]
        self.speed = C.UFO_SPEED
        self.rect = pg.Rect(0, 0, self.r * 2, self.r * 2)
        self.dir = Vec(1, 0) if uniform(0, 1) < 0.5 else Vec(-1, 0)
        self.turn_rate = 2.5
        self.fire_cool = uniform(1.0, 2.5)
        self.world = None


    def update(self, dt: float):
        # Follow the player if it's a small UFO
        if self.small and Ship.instance is not None:
            desired = Vec(Ship.instance.pos) - self.pos
            if desired.length_squared() > 0:
                desired = desired.normalize()

                current_angle = math.atan2(self.dir.y, self.dir.x)
                desired_angle = math.atan2(desired.y, desired.x)
                angle_diff = (desired_angle - current_angle +
                              math.pi) % (2 * math.pi) - math.pi

                max_step = self.turn_rate * dt
                if angle_diff > max_step:
                    angle_diff = max_step
                elif angle_diff < -max_step:
                    angle_diff = -max_step

                new_angle = current_angle + angle_diff
                self.dir = Vec(math.cos(new_angle), math.sin(new_angle))

        # Small UFO shooting logic
        self.fire_cool -= dt
        if (Ship.instance is not None
                and self.world is not None
                and self.fire_cool <= 0):
            if self.small:
                to_ship = Vec(Ship.instance.pos) - self.pos
                if to_ship.length_squared() > 0:
                    dirv = to_ship.normalize()

                    # uses "aim" config to determine inaccuracy
                    aim = C.UFO_SMALL["aim"]
                    max_spread = math.radians(30)
                    spread = (1.0 - aim) * max_spread
                    jitter = uniform(-spread, spread)
                    base_angle = math.atan2(dirv.y, dirv.x)
                    shot_angle = base_angle + jitter
                    shot_dir = Vec(math.cos(shot_angle), math.sin(shot_angle))
            else:
                # Big UFO shoots randomly in all directions
                angle = uniform(0, math.tau)
                shot_dir = Vec(math.cos(angle), math.sin(angle))

            # Spawn bullet
            bullet_pos = self.pos + shot_dir * (self.r + 4)
            bullet_vel = shot_dir * C.SHIP_BULLET_SPEED
            b = Bullet(bullet_pos, bullet_vel, owner="ufo")
            self.world.bullets.add(b)
            self.world.all_sprites.add(b)

            # Reset cooldown (big UFO slower, small UFO faster)
            self.fire_cool = uniform(0.8, 1.3) if not self.small else uniform(0.3, 0.6)

        # Movement
        self.pos += self.dir * self.speed * dt
        self.pos = wrap_pos(self.pos)
        self.rect.center = self.pos


    def draw(self, surf: pg.Surface):
        w, h = self.r * 2, self.r
        rect = pg.Rect(0, 0, w, h)
        rect.center = self.pos
        pg.draw.ellipse(surf, C.WHITE, rect, width=1)
        cup = pg.Rect(0, 0, w * 0.5, h * 0.7)
        cup.center = (self.pos.x, self.pos.y - h * 0.3)
        pg.draw.ellipse(surf, C.WHITE, cup, width=1)