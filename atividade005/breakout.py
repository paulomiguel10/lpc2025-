# breakout

# Teste de primeiro comentário do código break
import math
import pygame
from pathlib import Path

pygame.init()
pygame.mixer.init()

screen_size = (800, 800)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Break Out")

ball_size = 15
ball = pygame.Rect(400, 500, ball_size, ball_size)

player_size = 100
player = pygame.Rect(400, 750, player_size, 15)

blocks_lines = 14
lines_blocks = 8


def create_blocks(blocks_line, lines_blocks):
    """Cria blocos na tela com espaçamento definido."""
    width_size, height_size = screen_size
    block_distance = int(screen_size[0] * 0.008)  # diminui espaço entre blocos
    width_block = width_size / blocks_line - block_distance
    height_block = int(screen_size[1] * 0.015)  # altura mais fina
    line_distance = height_block + int(screen_size[1] * 0.01)

    blocks = []
    offset_top = int(screen_size[1] * 0.1)
    for j in range(lines_blocks):
        for i in range(blocks_line):
            block = pygame.Rect(
                i * (width_block + block_distance),
                offset_top + j * line_distance,
                width_block,
                height_block
            )
            blocks.append(block)
    return blocks


color = {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "green": (0, 255, 0),
    "yellow": (255, 255, 0),
    "blue": (0, 0, 255),
    "orange": (249, 79, 0),
    "red": (255, 0, 0),
}

# Mapeia cada cor para um valor de pontos
pontos_por_cor = {
    color["white"]: 0,
    color["yellow"]: 1,
    color["green"]: 3,
    color["orange"]: 5,
    color["red"]: 7
}

end_game = False
vidas = 3
score = 0
velocidade_nivel_1 = 2.0
velocidade_nivel_2 = 3.5
velocidade_nivel_3 = 4.5
velocidade_nivel_4 = 5.5

# Flags para controlar se a velocidade já foi alterada
atingiu_verde = False
atingiu_laranja = False
atingiu_vermelho = False

# Direção inicial da bola diagonal normalizada
ball_move = [velocidade_nivel_1 / (2**0.5),
             velocidade_nivel_1 / (2**0.5)]


def drawn_startgame():
    """Desenha bola e jogador na tela inicial."""
    screen.fill(color["black"])
    pygame.draw.rect(screen, color["blue"], player)
    pygame.draw.rect(screen, color["white"], ball)


# cores por linha
cores_linhas = [
    color["red"], color["red"], color["orange"], color["orange"],
    color["green"], color["green"], color["yellow"], color["yellow"]
]

# Cria blocos e cores
blocks = create_blocks(blocks_lines, lines_blocks)
cores_blocos = []
for linha in range(lines_blocks):
    for _ in range(blocks_lines):
        cores_blocos.append(cores_linhas[linha])


def drawn_blocks(blocks):
    """Desenha blocos na tela com cores específicas."""
    for idx, block in enumerate(blocks):
        pygame.draw.rect(screen, cores_blocos[idx], block)


def update_player_movement():
    """Atualiza posição do jogador com base em teclas."""
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT] and (player.x + player_size) < screen_size[0]:
        player.x += 5
    if keys[pygame.K_LEFT] and player.x > 0:
        player.x -= 5


BASE = Path(__file__).resolve().parent  # pasta do script

# Sons do jogo
som_blocos = pygame.mixer.Sound(str(BASE / "assets/breaksound.wav"))
som_colisao = pygame.mixer.Sound(str(BASE / "assets/bounce.wav"))
som_perda = pygame.mixer.Sound(str(BASE / "assets/wrong-buzzer-6268.mp3"))


def moviment_ball(ball, vidas):
    """Movimenta a bola e atualiza vidas se necessário."""
    global ball_move
    moviment = ball_move
    ball.x += moviment[0]
    ball.y += moviment[1]

    # Colisões com paredes
    if ball.x <= 0 or ball.x + ball_size >= screen_size[0]:
        moviment[0] = -moviment[0]
        som_colisao.play()
    if ball.y < 0:
        moviment[1] = -moviment[1]
        som_colisao.play()

    # Sistema de vidas
    if ball.y + ball_size >= screen_size[1]:
        som_perda.play()
        vidas -= 1
        if vidas > 0:
            ball.x = screen_size[0] // 2
            ball.y = screen_size[1] // 2

            velocidade_atual_mantida = velocidade_nivel_1
            if atingiu_verde:
                velocidade_atual_mantida = velocidade_nivel_2
            if atingiu_laranja:
                velocidade_atual_mantida = velocidade_nivel_3
            if atingiu_vermelho:
                velocidade_atual_mantida = velocidade_nivel_4

            moviment[0] = velocidade_atual_mantida / math.sqrt(2)
            moviment[1] = -velocidade_atual_mantida / math.sqrt(2)

            return moviment, vidas
        else:
            return None, vidas  # acabou as vidas

    return moviment, vidas


def ball_collision_player(ball, player):
    """Verifica colisão da bola com o jogador e ajusta velocidade."""
    global atingiu_verde, atingiu_laranja, atingiu_vermelho
    if ball.colliderect(player):
        som_colisao.play()
        if ball_move[1] > 0:
            ball.bottom = player.top
            ball_move[1] = -ball_move[1]
            offset = ball.centerx - player.centerx
            new_speed_x = offset / 10
            max_speed_x = 6
            if new_speed_x > max_speed_x:
                new_speed_x = max_speed_x
            elif new_speed_x < -max_speed_x:
                new_speed_x = -max_speed_x
            ball_move[0] = new_speed_x

            # Ajusta a velocidade alvo de acordo com os níveis
            velocidade_alvo_atual = velocidade_nivel_1
            if atingiu_verde:
                velocidade_alvo_atual = velocidade_nivel_2
            if atingiu_laranja:
                velocidade_alvo_atual = velocidade_nivel_3
            if atingiu_vermelho:
                velocidade_alvo_atual = velocidade_nivel_4

            velocidade_atual = (ball_move[0]**2 + ball_move[1]**2)**0.5
            if velocidade_atual > 0:
                fator = velocidade_alvo_atual / velocidade_atual
                ball_move[0] *= fator
                ball_move[1] *= fator

            # --- Correção do bug ---
            min_vertical_speed = 1.5  # velocidade vertical mínima
            if abs(ball_move[1]) < min_vertical_speed:
                ball_move[1] = -min_vertical_speed
                new_speed_x_squared = (velocidade_alvo_atual**2 -
                                       ball_move[1]**2)
                if new_speed_x_squared > 0:
                    new_speed_x = math.sqrt(new_speed_x_squared)
                    if ball_move[0] < 0:
                        ball_move[0] = -new_speed_x
                    else:
                        ball_move[0] = new_speed_x
            # --- Fim da correção ---


while not end_game:
    resultado = moviment_ball(ball, vidas)
    drawn_startgame()
    drawn_blocks(blocks)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end_game = True

    update_player_movement()

    if resultado is None:  # Se acabar as vidas, o jogo termina
        pygame.display.flip()
        break
    else:
        ball_move, vidas = resultado

    ball_collision_player(ball, player)

    # Colisão com blocos
    for idx, block in enumerate(blocks[:]):
        if ball.colliderect(block):
            som_blocos.play()

            cor_do_bloco = cores_blocos[idx]
            velocidade_alvo = 0

            # Ajusta níveis de velocidade
            if cor_do_bloco == color["red"] and not atingiu_vermelho:
                atingiu_vermelho = True
                atingiu_laranja = True
                atingiu_verde = True
                velocidade_alvo = velocidade_nivel_4
                print("Nível 4 de velocidade ativado!")
            elif cor_do_bloco == color["orange"] and not atingiu_laranja:
                atingiu_laranja = True
                atingiu_verde = True
                velocidade_alvo = velocidade_nivel_3
                print("Nível 3 de velocidade ativado!")
            elif cor_do_bloco == color["green"] and not atingiu_verde:
                atingiu_verde = True
                velocidade_alvo = velocidade_nivel_2
                print("Nível 2 de velocidade ativado!")

            # Ajusta vetor ball_move se velocidade_alvo for definida
            if velocidade_alvo > 0:
                velocidade_atual = (ball_move[0]**2 + ball_move[1]**2)**0.5
                if velocidade_atual > 0:
                    fator = velocidade_alvo / velocidade_atual
                    ball_move[0] *= fator
                    ball_move[1] *= fator

            # Pontos ganhos e atualização do score
            pontos_ganhos = pontos_por_cor.get(cor_do_bloco, 1)
            ball_move[1] = -ball_move[1]
            blocks.remove(block)
            cores_blocos.pop(idx)
            score += pontos_ganhos
            break

    # Desenhar score e vidas
    font_size = int(screen_size[1] * 0.05)
    font = pygame.font.SysFont(None, font_size)
    y_pos_top = 10

    # Score formatado
    score_formatado = f"{score:03d}"
    score_texto = font.render(score_formatado, True, color["white"])
    x_pos_score = screen_size[0] // 2 + 100
    screen.blit(score_texto, (x_pos_score, y_pos_top))

    # Vidas restantes
    vidas_texto = font.render(f"{vidas}", True, color["white"])
    screen.blit(vidas_texto, (30, y_pos_top))

    # Divisão central
    player_label = font.render("||", True, color["white"])
    screen.blit(player_label, (screen_size[0] // 2 - 100, y_pos_top))

    pygame.time.wait(5)
    pygame.display.flip()

pygame.quit()
