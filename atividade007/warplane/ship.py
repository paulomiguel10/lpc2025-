import pygame
import math

pygame.init()
pygame.mixer.init()

# CONSTANTES E VARIÁVEIS GLOBAIS
DARK_BLUE = (0, 0, 139)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
ORANGE = (255, 75, 10)
BLACK = (0, 0, 0)
GAME_WIDTH, GAME_HEIGHT = 256, 192
SCALE_FACTOR = 4
WINDOW_WIDTH = GAME_WIDTH * SCALE_FACTOR
WINDOW_HEIGHT = GAME_HEIGHT * SCALE_FACTOR
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Navezinha")
clock = pygame.time.Clock()
last_shot_time_1 = 0  # ms
last_shot_time_2 = 0  # ms
shot_cooldown = 200  # ms
shot_lifetime = 350  # ms
running = True  # controle do loop principal
shots = []  # lista para armazenar os tiros
shot_size = 5   # tamanho do tiro
shot_speed = 15  # velocidade do tiro (+ ou - dependendo da direção)


# CLASSE DO PLAYER
class player:
    def __init__(self, x, y, key_left, key_right, image_path, ):
        self.x = x
        self.y = y
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.original_image = pygame.transform.scale_by(self.original_image, 5)

# MUDANDO COR DO PLAYER 1
        if key_left == pygame.K_LEFT:  # serve pra identificar o player 1
            green_image = self.original_image.copy()  # cria uma copia indepen
            arr = pygame.surfarray.pixels3d(green_image)  # acess all pixels
            arr[:, :, 0] = 0  # R
            arr[:, :, 1] = 255  # G
            arr[:, :, 2] = 0  # B
            del arr
            self.original_image = green_image


# MUDANDO COR DO PLAYER 2
        if key_left == pygame.K_a:  # serve pra identificar o player 2
            orange_image = self.original_image.copy()  # cria copia independent
            arr = pygame.surfarray.pixels3d(orange_image)  # acess all pixels
            arr[:, :, 0] = 255  # R
            arr[:, :, 1] = 75  # G
            arr[:, :, 2] = 10  # B
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


# MOVIMENTO DO TIRO
def move_shot(shot):
    global shot_move
    movement = shot_move
    shot.x += movement[0]
    shot.y += movement[1]


# CRIANDO OS JOGADORES
# jogador 1
player1 = player(
    x=WINDOW_WIDTH // 5,
    y=WINDOW_HEIGHT // 5,
    key_left=pygame.K_LEFT,
    key_right=pygame.K_RIGHT,
    image_path=("atividade007\\aviao.png"))

# jogador 2
player2 = player(
    x=WINDOW_WIDTH * 4 // 5,
    y=WINDOW_HEIGHT * 4 // 5,
    key_left=pygame.K_a,
    key_right=pygame.K_d,
    image_path=("atividade007\\aviao.png"))

# LOOP PRINCIPAL
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Movimentos e disparo dos players
        # Movimento e tiro do player 1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                current_time = pygame.time.get_ticks()
                if current_time - last_shot_time_1 >= shot_cooldown:
                    last_shot_time_1 = current_time  # atualiza o tempo do último tiro

                    # Use a mesma conversão de ângulo que o movimento da nave usa
                    rad = math.radians(player1.angle - 270)

                    # distância do centro até a ponta (metade da altura da imagem original)
                    tip_offset = player1.original_image.get_height() / 2

                    # Calcular ponta da nave no momento do tiro (mesma lógica do movimento)
                    tip_x = player1.rect.centerx + math.cos(rad) * tip_offset
                    tip_y = player1.rect.centery - math.sin(rad) * tip_offset  # note o '-'

                    # Direção do tiro: mesmo vetor usado para mover a nave (multiplicado pela velocidade)
                    shot_dx = math.cos(rad) * shot_speed
                    shot_dy = -math.sin(rad) * shot_speed

                    # Adicionar tiro à lista (convertendo posições para int)
                    rect_x = int(tip_x - shot_size // 2)
                    rect_y = int(tip_y - shot_size // 2)
                    shots.append({
                        "rect": pygame.Rect(rect_x, rect_y, shot_size, shot_size),
                        "dx": shot_dx,
                        "dy": shot_dy,
                        "born_time": current_time,
                        "color": GREEN
                    })
            if event.key == pygame.K_UP:
                player1.toggle_movement()

            # Movimento e tiro do player 2
            if event.key == pygame.K_w:
                player2.toggle_movement()
            if event.key == pygame.K_s:  # Player 2 atira
                current_time = pygame.time.get_ticks()
                if current_time - last_shot_time_2 >= shot_cooldown:
                    last_shot_time_2 = current_time  # atualiza o tempo do último tiro

                    # Use a mesma conversão de ângulo que o movimento da nave usa
                    rad = math.radians(player2.angle - 270)

                    # distância do centro até a ponta (metade da altura da imagem original)
                    tip_offset = player2.original_image.get_height() / 2

                    # Calcular ponta da nave no momento do tiro (mesma lógica do movimento)
                    tip_x = player2.rect.centerx + math.cos(rad) * tip_offset
                    tip_y = player2.rect.centery - math.sin(rad) * tip_offset  # note o '-'

                    # Direção do tiro: mesmo vetor usado para mover a nave (multiplicado pela velocidade)
                    shot_dx = math.cos(rad) * shot_speed
                    shot_dy = -math.sin(rad) * shot_speed

                    # Adicionar tiro à lista (convertendo posições para int)
                    rect_x = int(tip_x - shot_size // 2)
                    rect_y = int(tip_y - shot_size // 2)
                    shots.append({
                        "rect": pygame.Rect(rect_x, rect_y, shot_size, shot_size),
                        "dx": shot_dx,
                        "dy": shot_dy,
                        "born_time": current_time,
                        "color": ORANGE
                    })

    screen.fill(DARK_BLUE)
    player1.update()
    player2.update()

    # Atualizar e desenhar tiros
    current_time = pygame.time.get_ticks()
    for shot in shots[:]:
        shot["rect"].x += shot["dx"]
        shot["rect"].y += shot["dy"]

        pygame.draw.rect(screen, (shot["color"]), shot["rect"])

        # Wrap-around horizontal e vertical
        if shot["rect"].top < 0:
            shot["rect"].bottom = WINDOW_HEIGHT
        elif shot["rect"].bottom > WINDOW_HEIGHT:
            shot["rect"].top = 0

        if shot["rect"].left < 0:
            shot["rect"].right = WINDOW_WIDTH
        elif shot["rect"].right > WINDOW_WIDTH:
            shot["rect"].left = 0

        if current_time - shot["born_time"] >= shot_lifetime:
            shots.remove(shot)

    # Desenha jogadores
    screen.blit(player1.image, player1.rect)
    screen.blit(player2.image, player2.rect)
    pygame.display.flip()
    clock.tick(60)
