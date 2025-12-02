
from random import uniform
import pygame as pg
import config as C
from sprites import JUCI, ZOMBIE, background
from utils import Vec
from sounds import sound_shot, zombie_sound, zombie_death, player_death


class World:

    def __init__(self):
        self.JUCI = JUCI(Vec(C.WIDTH / 2, C.HEIGHT / 2))
        self.bullets = pg.sprite.Group()
        self.ZOMBIEs = pg.sprite.Group()
        self.all_sprites = pg.sprite.Group(self.JUCI)

        self.ZOMBIE_timer = C.ZOMBIE_SPAWN_EVERY
        self.spawn_multiplier = 1  # Quantos zumbis nascem por vez
        self.difficulty_timer = 0  # Contador de tempo para aumentar dificul

        self.score = 0
        self.lives = C.START_LIVES
        self.game_over = False
        self.safe = C.SAFE_SPAWN_TIME
        self.ZOMBIE_timer = C.ZOMBIE_SPAWN_EVERY

        self.buildings = [
            pg.Rect(45, 75, 190, 220),  # Prédio esquerdo
            pg.Rect(735, 330, 140, 250)  # Prédio direito
        ]

    def try_fire(self):
        bullet = self.JUCI.fire()
        if bullet:
            self.bullets.add(bullet)
            self.all_sprites.add(bullet)
        sound_shot.play()

    # Spawnar ZOMBIEs
    def spawn_ZOMBIE(self):
        zombie_sound.play()
        side = uniform(0, 4)
        if side < 1:
            pos = Vec(0, uniform(0, C.HEIGHT))
        elif side < 2:
            pos = Vec(C.WIDTH, uniform(0, C.HEIGHT))
        elif side < 3:
            pos = Vec(uniform(0, C.WIDTH), 0)
        else:
            pos = Vec(uniform(0, C.WIDTH), C.HEIGHT)

        zombie_instance = ZOMBIE(pos, self.JUCI)
        self.ZOMBIEs.add(zombie_instance)
        self.all_sprites.add(zombie_instance)

    def update(self, dt: float, keys):
        self.JUCI.update(dt, keys)
        self.bullets.update(dt)
        self.ZOMBIEs.update(dt)

        self.safe -= dt
        self.ZOMBIE_timer -= dt

        # Aumenta dificul
        self.difficulty_timer += dt

        if self.difficulty_timer >= 25:  # A cada 25 segundos
            self.difficulty_timer = 0

        # Aumenta quantos zumbis nascem por vez (máx 8)
            if self.spawn_multiplier < 8:
                self.spawn_multiplier += 1

        # Diminui o tempo entre spawns (mínimo 0.4s)
            C.ZOMBIE_SPAWN_EVERY = max(0.4, C.ZOMBIE_SPAWN_EVERY * 0.85)

    # SPAWN DE ZUMBIS
        if self.ZOMBIE_timer <= 0:
            for _ in range(self.spawn_multiplier):   # spawn múltiplo
                self.spawn_ZOMBIE()

            self.ZOMBIE_timer = C.ZOMBIE_SPAWN_EVERY

        # Colisão Player x ZOMBIE
        if self.JUCI.invuln <= 0 and self.safe <= 0:
            for zombie in self.ZOMBIEs:
                if (
                    (zombie.pos - self.JUCI.pos).length()
                    < (zombie.r + self.JUCI.r)
                ):
                    player_death.play()
                    self.JUCI_die()
                    break

        # Colisão dos zumbis com as paredes
        for zombie in self.ZOMBIEs:
            rect = zombie.rect
            for b in self.buildings:
                if rect.colliderect(b):
                    # Recuar movimento
                    zombie.pos -= zombie.dir * zombie.speed * dt
                    zombie.rect.center = zombie.pos
                    # Faz o zumbi andar pro outro lado
                    zombie.dir.rotate_ip(90)

        # Colisão JUCI com as paredes
        JUCI_rect = self.JUCI.rect
        for b in self.buildings:
            if JUCI_rect.colliderect(b):
                # Recuar o movimento do player
                self.JUCI.pos -= self.JUCI.vel * dt
                # Atualizar rect depois de mover a posição
                self.JUCI.rect.center = self.JUCI.pos
                # Para garantir que ele realmente pare
                self.JUCI.vel.xy = (0, 0)

        for zombie in list(self.ZOMBIEs):
            for b in list(self.bullets):
                # Só balas da nave podem acertar o ZOMBIE
                if getattr(b, "owner", "JUCI") != "JUCI":
                    continue
                if (zombie.pos - b.pos).length() < (zombie.r + b.r):
                    self.score += C.ZOMBIE_SMALL["score"]
                    zombie.kill()
                    b.kill()
                    zombie_death.play()

    def JUCI_die(self):
        self.lives -= 1
        self.JUCI.pos.xy = (C.WIDTH / 2, C.HEIGHT / 2)
        self.JUCI.vel.xy = (0, 0)
        self.JUCI.angle = -90
        self.JUCI.invuln = C.SAFE_SPAWN_TIME
        self.safe = C.SAFE_SPAWN_TIME
        if self.lives < 0:
            # Marca fim de jogo; Game cuidará do restante
            self.game_over = True

    def draw(self, surf: pg.Surface, font: pg.font.Font):
        # Desenha o fundo primeiro
        surf.blit(background, (0, 0))
        for spr in self.all_sprites:
            spr.draw(surf)

        pg.draw.line(surf, (60, 60, 60), (0, 50), (C.WIDTH, 50), width=1)
        txt = f"SCORE {self.score:06d}   LIVES {self.lives}"
        label = font.render(txt, True, C.WHITE)
        surf.blit(label, (10, 10))
