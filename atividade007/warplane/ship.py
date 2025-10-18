import pygame
import math

pygame.init()
pygame.mixer.init()

DARK_BLUE = (0, 0, 139)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
BLACK = (0, 0, 0)

GAME_WIDTH, GAME_HEIGHT = 256, 192
SCALE_FACTOR = 4
WINDOW_WIDTH = GAME_WIDTH * SCALE_FACTOR
WINDOW_HEIGHT = GAME_HEIGHT * SCALE_FACTOR
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Navezinha")
clock = pygame.time.Clock()


class player:
    

    def __init__(self, x, y, key_left, key_right, image_path, ):
        self.x = x
        self.y = y

        self.original_image = pygame.image.load("C:\\Users\\Paulo\\lpc2025-\\atividade007\\aviao.png").convert_alpha()
        self.original_image = pygame.transform.scale_by(self.original_image, 5)

#--------------Mudando cor do Player 1-------------------------
        if key_left == pygame.K_LEFT: #serve pra identificar o player 2
            green_image = self.original_image.copy() #cria uma copia independente
            arr = pygame.surfarray.pixels3d(green_image) #acessar todos os pixels
            arr[:, :, 0] = 0 #R
            arr[:, :, 1] = 180 #G
            arr[:, :, 2] = 0 #B # pinta todos os pixels de laranja
            del arr
            self.original_image = green_image


#--------------Mudando cor do Player 2-------------------------
        if key_left == pygame.K_a: #serve pra identificar o player 2
            orange_image = self.original_image.copy() #cria uma copia independente
            arr = pygame.surfarray.pixels3d(orange_image) #acessar todos os pixels
            arr[:, :, 0] = 255 #R
            arr[:, :, 1] = 213 #G
            arr[:, :, 2] = 128 #B # pinta todos os pixels de laranja
            del arr
            self.original_image = orange_image

        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))

        self.angle = 0  # 0° pointing upward
        self.rotation_speed = 3  # rotation speed
        self.moving = False

        self.key_left = key_left
        self.key_right = key_right

    def toggle_movement(self):
        self.moving = not self.moving  # altern on and off

    def update(self):
        keys = pygame.key.get_pressed()

        # Ship rotation
        if keys[self.key_left]:
            self.angle += self.rotation_speed
        if keys[self.key_right]:
            self.angle -= self.rotation_speed

        # Update rotated image without distortion
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        # Move forward; image "top" is considered the front
        if self.moving:
            rad = math.radians(self.angle - 270)  # subtract oto align
            self.rect.x += math.cos(rad) * 6
            self.rect.y -= math.sin(rad) * 6  # inverted for pygame coordinates

        if self.rect.centerx < 0:
            self.rect.centerx = WINDOW_WIDTH
        elif self.rect.centerx > WINDOW_WIDTH:
            self.rect.centerx = 0

        if self.rect.centery < 0:
            self.rect.centery = WINDOW_HEIGHT
        elif self.rect.centery > WINDOW_HEIGHT:
            self.rect.centery = 0

colors = {
    "white": (255, 255, 255),
}


# SHOT SETUP
shot_size = 10



# SHOT MOVEMENT
def move_shot(shot):
    global shot_move
    movement = shot_move
    shot.x += movement[0]
    shot.y += movement[1]


# Criação dos jogadores
# PLAYER 1
player1 = player(
    x = WINDOW_WIDTH // 2,
    y = WINDOW_HEIGHT // 2,
    key_left=pygame.K_LEFT,
    key_right=pygame.K_RIGHT,
    image_path="C:\\Users\\Paulo\\lpc2025-\\atividade007\\aviao.png")

#Player 2
player2 = player(
    x = WINDOW_WIDTH // 2 * 3,
    y = WINDOW_HEIGHT // 2,
    key_left=pygame.K_a,
    key_right=pygame.K_d,
    image_path="C:\\Users\\Paulo\\lpc2025-\\atividade007\\aviao.png")

# Main loop
running = True
shots = []
shot_size = 10
shot_speed = 5  # velocidade do tiro (positivo ou negativo dependendo da direção)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
          
        # Movimentos e disparo do player 1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:

                # Calcular ponta da nave no momento do tiro
                angle = player1.angle
                rad = math.radians(angle)

                tip_x = player1.rect.centerx + math.cos(rad - math.pi/2) * (player1.original_image.get_height() / 2)
                tip_y = player1.rect.centery + math.sin(rad - math.pi/2) * (player1.original_image.get_height() / 2)

                # Direção do tiro
                shot_dx = math.cos(rad - math.pi/2) * shot_speed
                shot_dy = math.sin(rad - math.pi/2) * shot_speed

                # Adicionar tiro à lista
                current_time = pygame.time.get_ticks() 
                shots.append({
                    "rect": pygame.Rect(tip_x - shot_size//2, tip_y - shot_size//2, shot_size, shot_size),
                    "dx": shot_dx,
                    "dy": shot_dy,
                    "born_time": current_time #armazena quando o tiro foi criado
                })

            if event.key == pygame.K_UP:
                player1.toggle_movement()

            # Movimento do player 2
            if event.key == pygame.K_w:
                player2.toggle_movement()

    screen.fill(DARK_BLUE)
    player1.update()
    player2.update()

    # Atualizar e desenhar tiros
    current_time = pygame.time.get_ticks() 
    for shot in shots[:]:
        shot["rect"].x += shot["dx"]
        shot["rect"].y += shot["dy"]

        pygame.draw.rect(screen, (255,255,255), shot["rect"])

        # Wrap-around horizontal e vertical
        if shot["rect"].top < 0:
            shot["rect"].bottom = WINDOW_HEIGHT
        elif shot["rect"].bottom > WINDOW_HEIGHT:
            shot["rect"].top = 0

        if shot["rect"].left < 0:
            shot["rect"].right = WINDOW_WIDTH
        elif shot["rect"].right > WINDOW_WIDTH:
            shot["rect"].left = 0

        if current_time - shot["born_time"] >= 400:
            shots.remove(shot)


    # Desenha jogadores
    screen.blit(player1.image, player1.rect)
    screen.blit(player2.image, player2.rect)
    
    pygame.display.flip()
    clock.tick(60)
