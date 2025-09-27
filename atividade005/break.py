import pygame

#inicializar 
pygame.init()

screen_size = (800,800) #tamanho da tela
screen = pygame.display.set_mode(screen_size) #atribui a criação da tela a variável screen
pygame.display.set_caption("Break Out") #titulo do jogo

ball_size = 15 #tamanho da bola
ball = pygame.Rect(400,500,ball_size,ball_size) #cria um retangulo que representa a bola

player_size = 100 # tamanho da raquete controlada
player = pygame.Rect(400,750,player_size,15)

blocks_lines = 14 # blocos por linha
lines_blocks = 8 # linhas por blocos
total_blocks = blocks_lines * lines_blocks

def create_blocks(blocks_line,lines_blocks):
    height_size = screen_size[1] #altura da tela
    width_size = screen_size[0] #largura da tela
    block_distance = 8
    width_block = width_size / 14 - block_distance
    height_block = 15 #altura do bloco
    line_distance = height_block + 10

    blocks = []

    #criar os blocos
    for j in range(lines_blocks):
        for i in range(blocks_line):
            #criar o bloco
            block = pygame.Rect(i * (width_block+ block_distance), j * line_distance, width_block,height_block)

            #adicionar o bloco na lista de blocos
            blocks.append(block)

    return blocks

color = {
    "white": (255,255,255),
    "black": (0,0,0),
    "green": (0,255,0),
    "yellow": (255,255,0),
    "blue": (0,0,255),
    "orange":(249,79,0),
    "red": (255,0,0),
}

end_game = False #se torna true quando o jogo acaba
score = 0 
ball_move = [1, 1] #quantos px a bola se movimenta a cada seg

#desenhar na tela
def drawn_startgame():
    screen.fill(color["black"])
    pygame.draw.rect(screen, color["blue"], player)
    pygame.draw.rect(screen, color["white"], ball)

def drawn_blocks(blocks):
    for block in blocks:
        pygame.draw.rect(screen, color["green"], block)

# Criar as funções do jogo
def moviment_player(event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RIGHT:
            if (player.x + player_size) < screen_size[0]:
                player.x =  player.x + 10
        if event.key == pygame.K_LEFT:
            if player.x > 0:
                player.x = player.x - 10  
    
def moviment_ball(ball):
    moviment = ball_move
    ball.x = ball.x + moviment[0]
    ball.y = ball.y + moviment[1]
   
    if ball.x <= 0:
        moviment[0] = -moviment[0]
    if ball.y <- 0:
        moviment[1] = -moviment[1]
    if ball.x + ball_size >= screen_size[0]:
        moviment[0] = -moviment[0] 
    if ball.y + ball_size >= screen_size[1]:
        moviment[1] = -moviment[1]
    
    return moviment
blocks = create_blocks(blocks_lines,lines_blocks)

#criar um loop infinito
while not end_game:
    drawn_startgame()
    drawn_blocks(blocks)
    for event in pygame.event.get(): #todos os eventos que ocorrem durante o game

       if event.type == pygame.QUIT:  
         end_game = True
       moviment_player(event)

    ball_move = moviment_ball(ball)
    pygame.time.wait(1)
    pygame.display.flip() #atualiza a tela do jogo

pygame.quit()


