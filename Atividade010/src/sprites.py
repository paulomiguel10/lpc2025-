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
        angle = math.degrees(math.atan2(-self.vel.y, self.vel.x)) - 90

        self.image = pg.transform.rotate(pg.transform.scale(pg.image.load(
            os.path.join(BASE_DIR, "sprites", "imagem.png")
        ).convert_alpha(), (self.r * 8, self.r * 8)), angle)

        self.rect = self.image.get_rect(center=self.pos)

    def update(self, dt: float):
        self.pos += self.vel * dt
        self.pos = wrap_pos(self.pos)
        self.ttl -= dt
        if self.ttl <= 0:
            self.kill()
        self.rect.center = self.pos

    def draw(self, surf: pg.Surface):
        surf.blit(self.image, self.rect)


class Ship(pg.sprite.Sprite):
    instance = None

    def __init__(self, pos: Vec):
        super().__init__()
        self.pos = Vec(pos)
        self.vel = Vec(0, 0)
        # Direção "olhando" inicial (apenas usada como fallback)
        self.facing = Vec(0, -1)
        self.angle = -90
        self.r = C.SHIP_RADIUS
        self.cool = 0.0
        self.invuln = C.SAFE_SPAWN_TIME
        self.mouse_was_down = False

        # Sprites de animação do player (até 11 quadros) usando juci.gif
        self.sprites = []
        try:
            gif = Image.open(juci_gif)
            while len(self.sprites) < 11:
                gif.seek(len(self.sprites))
                frame = gif.copy().convert("RGBA")
                frame_surf = pg.image.fromstring(
                    frame.tobytes(), frame.size, frame.mode
                )
                frame_surf = pg.transform.scale(
                    frame_surf, (int(self.r * 5), int(self.r * 5))
                )
                self.sprites.append(frame_surf)
        except EOFError:
            # Se o GIF tiver menos de 11 quadros, usamos só os disponíveis
            pass

        self.current_frame = 0
        self.anim_timer = 0.0
        self.anim_speed = 0.12  # segundos por frame

        if self.sprites:
            self.image = self.sprites[0]
        else:
            # Fallback: superfície vazia, caso não carregue sprites
            self.image = pg.Surface((self.r * 2, self.r * 2), pg.SRCALPHA)

        self.rect = self.image.get_rect(center=self.pos)

        Ship.instance = self

    def update(self, dt: float, keys):
        """Atualiza posição, animação e ações do player.

        Movimento em quatro direções usando as setas.
        A animação só roda quando o player está se movendo.
        """
        moving = False
        move_dir = Vec(0, 0)

        # Movimento horizontal
        if keys[pg.K_a]:
            move_dir.x -= 1
            moving = True
        if keys[pg.K_d]:
            move_dir.x += 1
            moving = True

        # Movimento vertical
        if keys[pg.K_w]:
            move_dir.y -= 1
            moving = True
        if keys[pg.K_s]:
            move_dir.y += 1
            moving = True

        # Normaliza direção e aplica velocidade
        if move_dir.length_squared() > 0:
            move_dir = move_dir.normalize()
            self.vel = move_dir * C.SHIP_THRUST
        else:
            # Parado: sem velocidade
            self.vel.xy = (0, 0)

        # Tiro (mirando com o mouse) no clique esquerdo (apenas na transição solto->pressionado)
        mouse_down = pg.mouse.get_pressed()[0]
        if mouse_down and not self.mouse_was_down:
            self.fire()
        self.mouse_was_down = mouse_down

        if self.cool > 0:
            self.cool -= dt
        if self.invuln > 0:
            self.invuln -= dt

        # Movimento físico
        self.pos += self.vel * dt
        self.pos = wrap_pos(self.pos)

        # Animação do juci.gif
        if moving and self.sprites:
            self.anim_timer += dt
            if self.anim_timer >= self.anim_speed:
                self.anim_timer = 0.0
                self.current_frame = (
                    self.current_frame + 1) % len(self.sprites)
        else:
            self.current_frame = 0
            self.anim_timer = 0.0

        if self.sprites:
            self.image = self.sprites[self.current_frame]
            self.rect = self.image.get_rect(center=self.pos)
        else:
            self.rect.center = self.pos

    def fire(self) -> "Bullet | None":
        """Dispara em direção ao mouse."""
        if self.cool > 0:
            return None

        mouse_pos = Vec(pg.mouse.get_pos())
        dirv = mouse_pos - self.pos

        if dirv.length_squared() == 0:
            dirv = Vec(0, -1)
        else:
            dirv = dirv.normalize()

        # Atualiza facing apenas para consistência se for usado em outro lugar
        self.facing = Vec(dirv)

        pos = self.pos + dirv * (self.r + 6)
        vel = dirv * C.SHIP_BULLET_SPEED
        self.cool = C.SHIP_FIRE_RATE
        return Bullet(pos, vel)

    def hyperspace(self):
        self.pos = Vec(uniform(0, C.WIDTH), uniform(0, C.HEIGHT))
        self.vel.xy = (0, 0)
        self.invuln = 1.0

    def draw(self, surf: pg.Surface):
        # Desenha o sprite atual do player olhando para a mira (esquerda/direita)
        if hasattr(self, "image") and self.image:
            mouse_x, _ = pg.mouse.get_pos()
            img = self.image
            # Se o mouse estiver à esquerda do player, espelha o sprite na horizontal
            if mouse_x > self.pos.x:
                img = pg.transform.flip(self.image, True, False)
            rect = img.get_rect(center=self.pos)
            surf.blit(img, rect)

        # Contorno de invulnerabilidade permanece em volta do personagem
        if self.invuln > 0:
            raio = max(self.rect.width, self.rect.height) // 2
            draw_circle(surf, self.pos, raio + 3)


zombiemov_gif = os.path.join(BASE_DIR, "sprites", "zombie_anda.gif")
juci_gif = os.path.join(BASE_DIR, "sprites", "juci.gif")


class UFO(pg.sprite.Sprite):
    def __init__(self, pos: Vec, target: pg.sprite.Sprite):
        super().__init__()
        self.speed = 60
        self.turn_rate = math.radians(120)
        self.atual = 0
        self.anim_timer = 0
        self.anim_speed = 0.12  # segundos por frame
        self.r = 16

        # Carregar sprites
        gif = Image.open(zombiemov_gif)
        self.sprites = []

        try:
            while True:
                gif.seek(len(self.sprites))
                frame = gif.copy().convert("RGBA")
                zombiewalk_img = pg.image.fromstring(
                    frame.tobytes(), frame.size, frame.mode)

                # ESCALA
                zombiewalk_img = pg.transform.scale(zombiewalk_img, (32, 48))

                self.sprites.append(zombiewalk_img)
        except EOFError:
            pass

        self.image = self.sprites[0]
        self.rect = self.image.get_rect(center=pos)

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
        # Animation
        self.anim_timer += dt
        if self.anim_timer >= self.anim_speed:
            self.anim_timer = 0
            self.atual = (self.atual + 1) % len(self.sprites)

            self.image = self.sprites[self.atual]
            self.rect = self.image.get_rect(center=self.rect.center)

    def draw(self, surf: pg.Surface):
        surf.blit(self.image, self.rect)
