# breakout

#teste de primeiro comentário do código break- DESKTOP-1RLNS3S.py
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
    width_size, height_size = screen_size
    block_distance = int(screen_size[0]*0.008)  # diminuir o espaço entre blocos
    width_block = width_size / blocks_line - block_distance
    height_block = int(screen_size[1]*0.015)    # altura mais fina
    line_distance = height_block + int(screen_size[1]*0.01)

    blocks = []
    offset_top = int(screen_size[1]*0.1)
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
    color["white"]:0,
    color["yellow"]: 1,  # Amarelo vale menos
    color["green"]: 3,
    color["orange"]: 5,
    color["red"]: 7      # Vermelho vale mais
}

end_game = False
vidas = 3 
score = 0
velocidade_nivel_1 = 2.0  # Velocidade inicial
velocidade_nivel_2 = 3.5  # Velocidade ao atingir o primeiro verde
velocidade_nivel_3 = 4.5  # Velocidade ao atingir o primeiro laranja
velocidade_nivel_4 = 5.5  # Velocidade ao atingir o primeiro vermelho

# Flags para controlar se a velocidade já foi alterada
atingiu_verde = False
atingiu_laranja = False
atingiu_vermelho = False

# A direção inicial será diagonal. Normalizamos o vetor [1, 1] e multiplicamos pela velocidade.
ball_move = [velocidade_nivel_1 / (2**0.5), velocidade_nivel_1 / (2**0.5)]

def drawn_startgame():
    screen.fill(color["black"])
    pygame.draw.rect(screen, color["blue"], player)
    pygame.draw.rect(screen, color["white"], ball)

# cores por linha
cores_linhas = [ color["red"], color["red"], color["orange"], color["orange"],
                color["green"], color["green"], color["yellow"], color["yellow"]]

blocks = create_blocks(blocks_lines, lines_blocks) #cria os nvos blocos superiores e adiciona as cores sobrepondo uma as outras

# Criar lista que mantém a cor de cada bloco individualmente
cores_blocos = []
for linha in range(lines_blocks):
    for _ in range(blocks_lines):
        cores_blocos.append(cores_linhas[linha])


def drawn_blocks(blocks):
    for idx, block in enumerate(blocks):
        pygame.draw.rect(screen, cores_blocos[idx], block)  # usa cor específica de cada bloco
        
def update_player_movement():
    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT]:
        if (player.x + player_size) < screen_size[0]:
            player.x = player.x + 5

    if keys[pygame.K_LEFT]:
        if player.x > 0:
            player.x = player.x - 5


BASE = Path(__file__).resolve().parent  # pasta do script

som_blocos = pygame.mixer.Sound(str(BASE / "assets/breaksound.wav"))
som_colisao = pygame.mixer.Sound(str(BASE / "assets/bounce.wav"))
som_perda = pygame.mixer.Sound(str(BASE / "assets/wrong-buzzer-6268.mp3"))


def moviment_ball(ball, vidas):
    global ball_move
    moviment = ball_move
    ball.x = ball.x + moviment[0]
    ball.y = ball.y + moviment[1]

    if ball.x <= 0:
        moviment[0] = -moviment[0]
        som_colisao.play()
    if ball.y < 0:
        moviment[1] = -moviment[1]
        som_colisao.play()
    if ball.x + ball_size >= screen_size[0]:
        moviment[0] = -moviment[0]
        som_colisao.play()

    # Sistema de contagem de vidas      
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
            return None, vidas #acabou as vidas

    return moviment, vidas
    
blocks = create_blocks(blocks_lines, lines_blocks)

def ball_collision_player(ball, player):
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



            # --- INÍCIO DA CORREÇÃO DO BUG ---
            # Garante uma velocidade vertical mínima para evitar que a bola fique presa.
            min_vertical_speed = 1.5  # Define uma velocidade vertical mínima
            
            if abs(ball_move[1]) < min_vertical_speed:
                # Mantém o sinal original (sempre será para cima após o rebote)
                ball_move[1] = -min_vertical_speed

                # RE-NORMALIZAÇÃO: Como alteramos um componente, a velocidade total está errada.
                # Precisamos ajustar o componente X para manter a velocidade_alvo_atual.
                # Usando Pitágoras: X_novo^2 + Y_novo^2 = V_total^2
                # X_novo = sqrt(V_total^2 - Y_novo^2)
                new_speed_x_squared = velocidade_alvo_atual**2 - ball_move[1]**2
                if new_speed_x_squared > 0:
                    new_speed_x = math.sqrt(new_speed_x_squared)
                    # Mantém a direção horizontal original (esquerda ou direita)
                    if ball_move[0] < 0:
                        ball_move[0] = -new_speed_x
                    else:
                        ball_move[0] = new_speed_x
            # --- FIM DA CORREÇÃO DO BUG ---


while not end_game:
    resultado = moviment_ball(ball,vidas)
    drawn_startgame()
    drawn_blocks(blocks)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end_game = True

    update_player_movement()

    if resultado is None:  #se acabar as vidas o jogo acaba
        pygame.display.flip()
        break
    else:
        ball_move, vidas = resultado


    ball_collision_player(ball, player)
   # Colisão com blocos
    for idx, block in enumerate(blocks[:] ) :
        if ball.colliderect(block):
            som_blocos.play()
            # 1. Descobrir a cor do bloco que foi atingido
            cor_do_bloco = cores_blocos[idx]  # usa cor específica do bloco

            velocidade_alvo = 0 # Variável para guardar a nova velocidade desejada

            # Se atingir um bloco VERMELHO e for a PRIMEIRA VEZ
            if cor_do_bloco == color["red"] and not atingiu_vermelho:
                atingiu_vermelho = True # Marca que já passamos para o nível 4
                atingiu_laranja = True  # Nível 4 também conta como tendo passado pelos níveis anteriores
                atingiu_verde = True
                velocidade_alvo = velocidade_nivel_4
                print("NÍVEL 4 de velocidade ativado!") # Mensagem de feedback

            # Se atingir um bloco LARANJA e for a PRIMEIRA VEZ (e não tivermos ativado o nível 4 ainda)
            elif cor_do_bloco == color["orange"] and not atingiu_laranja:
                atingiu_laranja = True # Marca que já passamos para o nível 3
                atingiu_verde = True
                velocidade_alvo = velocidade_nivel_3
                print("NÍVEL 3 de velocidade ativado!") # Mensagem de feedback

            # Se atingir um bloco VERDE e for a PRIMEIRA VEZ (e não tivermos ativado níveis superiores ainda)
            elif cor_do_bloco == color["green"] and not atingiu_verde:
                atingiu_verde = True # Marca que já passamos para o nível 2
                velocidade_alvo = velocidade_nivel_2
                print("NÍVEL 2 de velocidade ativado!") # Mensagem de feedback

            # Se a velocidade_alvo foi definida, precisamos ajustar o vetor ball_move
            if velocidade_alvo > 0:
                # Calcula a velocidade atual para encontrar o fator de escala
                velocidade_atual = (ball_move[0]**2 + ball_move[1]**2)**0.5
                
                # Evita divisão por zero se a bola estiver parada
                if velocidade_atual > 0:
                    fator = velocidade_alvo / velocidade_atual
                    ball_move[0] *= fator
                    ball_move[1] *= fator

            # 2. Obter os pontos para essa cor
            pontos_ganhos = pontos_por_cor.get(cor_do_bloco, 1) # Pega os pontos, ou 1 como padrão

            # 3. Atualizar a lógica do jogo
            ball_move[1] = -ball_move[1]
            blocks.remove(block)
            cores_blocos.pop(idx)  # remove a cor correspondente
            score += pontos_ganhos
            break  
    # Desenhar score proporcional
    # Configuração da fonte para o estilo arcade (topo da tela)
    font_size = int(screen_size[1] * 0.05)
    font = pygame.font.SysFont(None, font_size)
    y_pos_top = 10 # Posição Y no topo

    # --- 1. PLACAR (SCORE) ---
    # A chave é o f-string: {score:03d} força 3 dígitos com zero à esquerda.
    score_formatado = f"{score:03d}" 
    score_texto = font.render(score_formatado, True, color["white"])

    # Posição: Center-Right (para imitar o local do '000' na imagem)
    # Exemplo de posição X: metade da tela + 100 pixels
    x_pos_score = screen_size[0] // 2 + 100 
    screen.blit(score_texto, (x_pos_score, y_pos_top))

    # --- 2. VIDAS 
    # Exibe apenas o número de vidas restantes
    vidas_texto = font.render(f"{vidas}", True, color["white"])
    # Posição: Superior Esquerdo (onde o '1' está na imagem)
    screen.blit(vidas_texto, (30, y_pos_top))

    # --- 3. Divisão
    player_label = font.render("||", True, color["white"])
    # Posição: Center-Left (onde o '2' está na imagem)
    screen.blit(player_label, (screen_size[0] // 2 - 100, y_pos_top))
    

    pygame.time.wait(5)
    pygame.display.flip()

pygame.quit()
