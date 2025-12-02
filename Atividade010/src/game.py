import random
import sys
from dataclasses import dataclass
import pygame as pg
from sprites import menu
import config as C
from systems import World


@dataclass
class Scene:
    name: str


pg.mixer.init()
...


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

        # Leaderboard simples em memória
        self.leaderboard = []  # lista de (score, nome)
        self.name_input = ""
        self.max_name_length = 3
        self.last_score = 0

    def draw_menu(self):
        self.screen.blit(menu, (0, 0))

    def draw_enter_score(self):
        # Tela para o jogador digitar um nome de 3 letras
        title = self.big.render("GAME OVER", True, C.WHITE)
        prompt = self.font.render("Digite seu nome (3 letras):", True, C.WHITE)
        name_txt = self.big.render(
            self.name_input.ljust(self.max_name_length, "_"),
            True,
            C.WHITE,
        )

        rect = title.get_rect(center=(C.WIDTH // 2, C.HEIGHT // 2 - 80))
        self.screen.blit(title, rect)
        rect = prompt.get_rect(center=(C.WIDTH // 2, C.HEIGHT // 2))
        self.screen.blit(prompt, rect)
        rect = name_txt.get_rect(center=(C.WIDTH // 2, C.HEIGHT // 2 + 60))
        self.screen.blit(name_txt, rect)

    def draw_leaderboard(self):
        # Tela simples de leaderboard em memória
        title = self.big.render("LEADERBOARD", True, C.WHITE)
        rect = title.get_rect(center=(C.WIDTH // 2, 80))
        self.screen.blit(title, rect)

        y = 140
        for idx, (score, name) in enumerate(self.leaderboard, start=1):
            line = f"{idx}. {name} - {score:06d}"
            txt = self.font.render(line, True, C.WHITE)
            self.screen.blit(
                txt,
                (C.WIDTH // 2 - txt.get_width() // 2, y),
            )
            y += 30

        msg = self.font.render(
            "clique qualquer tecla para jogar novamente",
            True,
            C.WHITE,
        )
        rect = msg.get_rect(center=(C.WIDTH // 2, C.HEIGHT - 80))
        self.screen.blit(msg, rect)

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

                elif self.scene.name == "enter_score":
                    if e.type == pg.KEYDOWN:
                        if e.key in (pg.K_RETURN, pg.K_KP_ENTER):
                            if len(self.name_input) == self.max_name_length:
                                name = self.name_input.upper()
                                self.leaderboard.append(
                                    (self.last_score, name))
                                # Ordena do maior para o menor, mantém top 5
                                self.leaderboard = sorted(
                                    self.leaderboard,
                                    key=lambda x: x[0],
                                    reverse=True,
                                )[:5]
                                self.scene = Scene("leaderboard")
                        elif e.key == pg.K_BACKSPACE:
                            self.name_input = self.name_input[:-1]
                        else:
                            ch = e.unicode
                            if (
                                ch
                                and ch.isalpha()
                                and len(self.name_input) < self.max_name_length
                            ):
                                self.name_input += ch.upper()

                elif self.scene.name == "leaderboard":
                    if e.type == pg.KEYDOWN:
                        # Reinicia o jogo mantendo o leaderboard em memória
                        self.world = World()
                        self.scene = Scene("play")

            keys = pg.key.get_pressed()
            self.screen.fill(C.BLACK)

            if self.scene.name == "menu":
                self.draw_menu()
            elif self.scene.name == "play":
                self.world.update(dt, keys)
                # Se o mundo marcar game_over, troca para tela de nome
                if getattr(self.world, "game_over", False):
                    self.last_score = self.world.score
                    self.name_input = ""
                    self.scene = Scene("enter_score")
                self.world.draw(self.screen, self.font)
            elif self.scene.name == "enter_score":
                self.draw_enter_score()
            elif self.scene.name == "leaderboard":
                self.draw_leaderboard()

            pg.display.flip()
