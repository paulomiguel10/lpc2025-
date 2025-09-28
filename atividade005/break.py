# breakout

#teste de primeiro comentário do código break- DESKTOP-1RLNS3S.py

import pygame

pygame.init()

screen_size = (800, 800)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Break Out")

ball_size = 15
ball = pygame.Rect(400, 500, ball_size, ball_size)

player_size = 100
player = pygame.Rect(400, 750, player_size, 15)

blocks_lines = 14
lines_blocks = 8
total_blocks = blocks_lines * lines_blocks


def create_blocks(blocks_line, lines_blocks):
    width_size = screen_size[0]
    block_distance = 8
    width_block = width_size / 14 - block_distance
    height_block = 15
    line_distance = height_block + 10

    blocks = []

    for j in range(lines_blocks):
        for i in range(blocks_line):
            block = pygame.Rect(i * (width_block + block_distance),
                                j * line_distance, width_block, height_block)
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
    color["yellow"]: 1,  # Amarelo vale menos
    color["green"]: 3,
    color["orange"]: 5,
    color["red"]: 7      # Vermelho vale mais
}

end_game = False
score = 0
ball_move = [1, 1]


def drawn_startgame():
    screen.fill(color["black"])
    pygame.draw.rect(screen, color["blue"], player)
    pygame.draw.rect(screen, color["white"], ball)


# cores por linha
cores_linhas = [color["red"], color["red"], color["orange"], color["orange"],
                color["green"], color["green"], color["yellow"], color["yellow"]]

blocks = create_blocks (blocks_lines, lines_blocks) #cria os nvos blocos superiores e adiciona as cores sobrepondo uma as outras

def drawn_blocks(blocks):
    for idx, block in enumerate(blocks):
        linha = idx // blocks_lines
        pygame.draw.rect(screen, cores_linhas[linha], block) #função para enumerar os blocos sobrepondo-os
        


def update_player_movement():
    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT]:
        if (player.x + player_size) < screen_size[0]:
            player.x = player.x + 5

    if keys[pygame.K_LEFT]:
        if player.x > 0:
            player.x = player.x - 5


def moviment_ball(ball):
    moviment = ball_move
    ball.x = ball.x + moviment[0]
    ball.y = ball.y + moviment[1]

    if ball.x <= 0:
        moviment[0] = -moviment[0]
    if ball.y < 0:
        moviment[1] = -moviment[1]
    if ball.x + ball_size >= screen_size[0]:
        moviment[0] = -moviment[0]
    if ball.y + ball_size >= screen_size[1]:
        moviment[1] = -moviment[1]

    return moviment


blocks = create_blocks(blocks_lines, lines_blocks)


def ball_collision_player(ball, player):
    if ball.colliderect(player):
        if ball_move[1] > 0:
            ball.bottom = player.top
            ball_move[1] = -ball_move[1]
            offset = ball.centerx - player.centerx
            new_speed_x = offset / 10
            max_speed_x = 4
            if new_speed_x > max_speed_x:
                new_speed_x = max_speed_x
            elif new_speed_x < -max_speed_x:
                new_speed_x = -max_speed_x
            ball_move[0] = new_speed_x


while not end_game:
    drawn_startgame()
    drawn_blocks(blocks)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end_game = True

    update_player_movement()

    ball_collision_player(ball, player)
   # Colisão com blocos
    for idx, block in enumerate(blocks[:]):
        if ball.colliderect(block):
            # 1. Descobrir a cor do bloco que foi atingido
            linha_do_bloco = idx // blocks_lines
            cor_do_bloco = cores_linhas[linha_do_bloco]

            # 2. Obter os pontos para essa cor
            pontos_ganhos = pontos_por_cor.get(cor_do_bloco, 1) # Pega os pontos, ou 1 como padrão

            # 3. Atualizar a lógica do jogo
            ball_move[1] = -ball_move[1]
            blocks.remove(block)
            score += pontos_ganhos
            break  # Evita múltiplas colisões na mesma atualização

    # Desenhar score proporcional
    font = pygame.font.SysFont(None, int(screen_size[1]*0.04))
    score_text = font.render(f"Score: {score}", True, color["white"])
    screen.blit(score_text, (10, 10))

    ball_move = moviment_ball(ball)
    pygame.time.wait(5)
    pygame.display.flip()

pygame.quit()
