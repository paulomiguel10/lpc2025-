import pygame
import math

# Inicialização
pygame.init()
pygame.mixer.init()

# Configurações da tela
screen_size = (800, 800)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Jogo da Nave")

# Cores
blue = (0, 0, 255)
black = (0, 0, 0)

# Posição inicial e ângulo da nave
pos_x, pos_y = 400, 500
angulo = 270  # 270 graus = apontando pra cima

# Velocidades
vel = 0
aceleracao = 0.2
atrito = 0.98

clock = pygame.time.Clock()
running = True

# Função para desenhar o triângulo (nave)
def desenhar_nave(x, y, ang):
    tamanho = 25
    pontos_base = [
        (0, 0),   # vértice da frente
        (-tamanho / 2, tamanho ),  # canto inferior esquerdo
        (tamanho / 2, tamanho )    # canto inferior direito
    ]

    # Rotaciona os pontos com base no ângulo
    pontos_rotacionados = []
    for px, py in pontos_base:
        rx = px * math.cos(math.radians(ang)) - py * math.sin(math.radians(ang))
        ry = px * math.sin(math.radians(ang)) + py * math.cos(math.radians(ang))
        pontos_rotacionados.append((x + rx, y + ry))

    # Desenha o triângulo
    pygame.draw.polygon(screen, blue, pontos_rotacionados)

    ponta = pontos_rotacionados[0]
    pygame.draw.circle(screen,(255,0,0), (int(ponta[0]), int(ponta[1])), 5)

# LOOP PRINCIPAL
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Teclas pressionadas
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        angulo -= 5  # gira para a esquerda
    if keys[pygame.K_RIGHT]:
        angulo += 5  # gira para a direita
    if keys[pygame.K_UP]:
        vel += aceleracao  # acelera para frente

    vel *= atrito
    # Calcula o movimento com base no ângulo
    pos_x += vel * math.cos(math.radians(angulo))
    pos_y += vel * math.sin(math.radians(angulo))

    # Mantém a nave dentro da tela (teletransporte nas bordas)
    if pos_x < 0:
        pos_x = screen_size[0]
    elif pos_x > screen_size[0]:
        pos_x = 0
    if pos_y < 0:
        pos_y = screen_size[1]
    elif pos_y > screen_size[1]:
        pos_y = 0

    # Limpa a tela
    screen.fill(black)

    # Desenha a nave
    desenhar_nave(pos_x, pos_y, angulo)

    # Atualiza a tela
    pygame.display.flip()

    # Controla FPS
    clock.tick(60)

pygame.quit()
