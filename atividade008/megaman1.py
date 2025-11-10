import pygame
import sys

# Inicialização
pygame.init()

# Configurações da tela
screen_size = (850, 720)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Sprites")

#Fundo de tela
background = pygame.image.load('atividade008/sprites/fundo.png')
background = pygame.transform.scale(background, screen_size)

class Megaman(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = []

        #Sprites de andar
        self.sprites_andar = [
            pygame.image.load('atividade008/sprites/andar_1.png'),
            pygame.image.load('atividade008/sprites/andar_2.png'),
            pygame.image.load('atividade008/sprites/andar_3.png')
        ]
        #Sprite ficar parado
        self.sprites_parado = [
            pygame.image.load('atividade008/sprites/parado_1.png')
        ]

        #Sprite de pular
        self.sprites_pular = [
            (pygame.image.load('atividade008/sprites/pulo.png'))
                             ]
        #Sprite de atirar parado
        self.sprites_atirarparado = [
          (pygame.image.load('atividade008/sprites/parado_atira.png'))
        ]
        #Sprite de atirar correndo 
        self.sprites_atirarcorrendo = [
            pygame.image.load('atividade008/sprites/atira_1.png'),
            pygame.image.load('atividade008/sprites/atira_2.png'),
            pygame.image.load('atividade008/sprites/atira_3.png')
        ]
        #Define a animação inicial
        self.sprites = self.sprites_andar

        self.atual = 0
        self.velocidade = 8 #velocidade de movimento|
        self.direcao = 1 #direita: 1 esquerda: -1
        self.image = self.sprites[self.atual]
        self.image = pygame.transform.scale(self.image, (499/5, 500/5))

        self.rect = self.image.get_rect()
        self.rect.topleft = 200,530
        self.animar = False
    
    def pular(self):
        if self.rect.y == 530 and (not hasattr(self, "velocidade_y") or self.velocidade_y == 0):

            self.animar = True
            self.sprites = self.sprites_pular
            self.image = self.sprites[0]
            self.image = pygame.transform.scale(self.image, (499/5, 500/5))
            self.velocidade_y = -17

    def atirarparado(self):
        self.animar = True
        self.atual = 0
        self.sprites = self.sprites_atirarparado
        self.image = self.sprites[0] 
        self.image = pygame.transform.scale(self.image, (499/4.6, 500/4.6))

        if self.direcao == 1:
            self.image = pygame.transform.flip(self.image, True, False)
    
    def atirarcorrendo(self):
        self.animar = True
        self.atual = 0
        self.sprites = self.sprites_atirarcorrendo

    def andar(self, direcao):
      self.animar = True
      self.direcao = direcao
      self.sprites = self.sprites_andar
  
    def parar(self):
        self.animar = False
        self.atual = 0
        self.sprites = self.sprites_parado
        self.image = self.sprites[0]
        self.image = pygame.transform.scale(self.image, (499/5, 500/5))

        if self.direcao == 1:
            self.image = pygame.transform.flip(self.image, True, False)
    def update(self):
        if self. animar == True:
            self.atual = self.atual + 0.2
            if self.atual >= len(self.sprites):
                self.atual = 0
            self.image = self.sprites[int(self.atual)]
            self.image = pygame.transform.scale(self.image, (499/5, 500/5))
            #Inverte imagem se estiver indo para esquerda
            if self.direcao == 1:
                self.image = pygame.transform.flip(self.image, True, False)
  
        if hasattr(self, "velocidade_y"):
            self.rect.y += self.velocidade_y
            self.velocidade_y += 1

            if self.rect.y >= 530:
                self.rect.y = 530
                self.velocidade_y = 0
            else:
                self.sprites = self.sprites_pular
                self.image = self.sprites[0]
                self.image = pygame.transform.scale(self.image, (499/5, 500/5))
                if self.direcao == 1:
                  self.image = pygame.transform.flip(self.image, True, False)

class Tiro(pygame.sprite.Sprite):
    def __init__(self, x, y, direcao):
        pygame.sprite.Sprite.__init__(self)
        self.sprites_tiro = [pygame.image.load('atividade008/sprites/tiro.png')]
        self.image = self.sprites_tiro[0]
        self.image = pygame.transform.scale(self.image, (30, 15))
        # tamanho do tiro

        # Inverter caso esteja virado para a direita (1)
        if direcao == 1:
            self.image = pygame.transform.flip(self.image, True, False)

        # Posição e direção
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direcao = direcao
        self.velocidade = 15 * direcao

    def update(self):
        self.rect.x += self.velocidade
        if self.rect.x < 0 or self.rect.x > 850:
            self.kill()

#Criação do sprite
todas_as_sprites = pygame.sprite.Group()
megaman = Megaman()
tiros = pygame.sprite.Group()
todas_as_sprites.add(megaman)

relogio = pygame.time.Clock()

import pygame
import sys

# Inicialização
pygame.init()

# Configurações da tela
screen_size = (850, 720)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Sprites")

#Fundo de tela
background = pygame.image.load('atividade008/sprites/fundo.png')
background = pygame.transform.scale(background, screen_size)

class Megaman(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = []

        #Sprites de andar
        self.sprites_andar = [
            pygame.image.load('atividade008/sprites/andar_1.png'),
            pygame.image.load('atividade008/sprites/andar_2.png'),
            pygame.image.load('atividade008/sprites/andar_3.png')
        ]
        #Sprite ficar parado
        self.sprites_parado = [
            pygame.image.load('atividade008/sprites/parado_1.png')
        ]

        #Sprite de pular
        self.sprites_pular = [
            (pygame.image.load('atividade008/sprites/pulo.png'))
                             ]
        #Sprite de atirar parado
        self.sprites_atirarparado = [
          (pygame.image.load('atividade008/sprites/parado_atira.png'))
        ]
        #Sprite de atirar correndo 
        self.sprites_atirarcorrendo = [
            pygame.image.load('atividade008/sprites/atira_1.png'),
            pygame.image.load('atividade008/sprites/atira_2.png'),
            pygame.image.load('atividade008/sprites/atira_3.png')
        ]
        #Define a animação inicial
        self.sprites = self.sprites_andar

        self.atual = 0
        self.velocidade = 8 #velocidade de movimento|
        self.direcao = 1 #direita: 1 esquerda: -1
        self.image = self.sprites[self.atual]
        self.image = pygame.transform.scale(self.image, (499/5, 500/5))

        self.rect = self.image.get_rect()
        self.rect.topleft = 200,530
        self.animar = False
    
    def pular(self):
        if self.rect.y == 530 and (not hasattr(self, "velocidade_y") or self.velocidade_y == 0):

            self.animar = True
            self.sprites = self.sprites_pular
            self.image = self.sprites[0]
            self.image = pygame.transform.scale(self.image, (499/5, 500/5))
            self.velocidade_y = -17

    def atirarparado(self):
        self.animar = True
        self.atual = 0
        self.sprites = self.sprites_atirarparado
        self.image = self.sprites[0] 
        self.image = pygame.transform.scale(self.image, (499/4.6, 500/4.6))

        if self.direcao == 1:
            self.image = pygame.transform.flip(self.image, True, False)
    
    def atirarcorrendo(self):
        self.animar = True
        self.sprites = self.sprites_atirarcorrendo
        self.atual += 0.3
        
        if self.atual >= len(self.sprites):
            self.atual = 0

        #Atualiza a imagem atual
        self.image = self.sprites[int(self.atual)]
        self.image = pygame.transform.scale(self.image, (499/5, 500/5))

        #Se estiver indo para direita
        if self.direcao == 1:
            self.image = pygame.transform.flip(self.image, True, False)  

    def andar(self, direcao):
      self.animar = True
      self.direcao = direcao
      self.sprites = self.sprites_andar
  
    def parar(self):
        self.animar = False
        self.atual = 0
        self.sprites = self.sprites_parado
        self.image = self.sprites[0]
        self.image = pygame.transform.scale(self.image, (499/5, 500/5))

        if self.direcao == 1:
            self.image = pygame.transform.flip(self.image, True, False)

    def update(self):
        if self. animar == True:
            self.atual = self.atual + 0.2
            if self.atual >= len(self.sprites):
                self.atual = 0
            self.image = self.sprites[int(self.atual)]
            self.image = pygame.transform.scale(self.image, (499/5, 500/5))
            #Inverte imagem se estiver indo para esquerda
            if self.direcao == 1:
                self.image = pygame.transform.flip(self.image, True, False)
  
        if hasattr(self, "velocidade_y"):
            self.rect.y += self.velocidade_y
            self.velocidade_y += 1

            if self.rect.y >= 530:
                self.rect.y = 530
                self.velocidade_y = 0
            else:
                self.sprites = self.sprites_pular
                self.image = self.sprites[0]
                self.image = pygame.transform.scale(self.image, (499/5, 500/5))
                if self.direcao == 1:
                  self.image = pygame.transform.flip(self.image, True, False)

class Tiro(pygame.sprite.Sprite):
    def __init__(self, x, y, direcao):
        pygame.sprite.Sprite.__init__(self)
        self.sprites_tiro = [pygame.image.load('atividade008/sprites/tiro.png')]
        self.image = self.sprites_tiro[0]
        self.image = pygame.transform.scale(self.image, (30, 15))
        # tamanho do tiro

        # Inverter caso esteja virado para a direita (1)
        if direcao == 1:
            self.image = pygame.transform.flip(self.image, True, False)

        # Posição e direção
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direcao = direcao
        self.velocidade = 15 * direcao

    def update(self):
        self.rect.x += self.velocidade
        if self.rect.x < 0 or self.rect.x > 850:
            self.kill()
         
#Criação do sprite
todas_as_sprites = pygame.sprite.Group()
megaman = Megaman()
tiros = pygame.sprite.Group()
todas_as_sprites.add(megaman)

relogio = pygame.time.Clock()

# LOOP PRINCIPAL
running = True
while running:
    relogio.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
        
        # Cria tiro ao apertar S
        if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            if megaman.direcao == 1:
                x_tiro = megaman.rect.right - 10
            else:
                x_tiro = megaman.rect.left + 10

            y_tiro = megaman.rect.centery - 5
            tiro = Tiro(x_tiro, y_tiro, megaman.direcao)
            todas_as_sprites.add(tiro)
            tiros.add(tiro)

    keys = pygame.key.get_pressed()
    movendo = False

    # Movimento para a direita
    if keys[pygame.K_RIGHT]:
        megaman.rect.x += megaman.velocidade
        megaman.direcao = 1
        if keys[pygame.K_s]:
            megaman.atirarcorrendo()
        else:
            megaman.andar(1)
            movendo = True

    # Movimento para a esquerda
    elif keys[pygame.K_LEFT]:
        megaman.rect.x -= megaman.velocidade
        megaman.direcao = -1
        if keys[pygame.K_s]:
            megaman.atirarcorrendo()
            movendo = True
        else:
            megaman.andar(-1)    
        movendo = True

    # Atirar parado (animação)
    if keys[pygame.K_s] and megaman.rect.y == 530 and not (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]):
        megaman.atirarparado()
        movendo = True

    # Pular
    elif keys[pygame.K_SPACE]:
        megaman.pular()
        movendo = True
        
    # Parado
    if not movendo:
        megaman.parar()

    # Atualização de tela
    screen.blit(background, (0,0))
    todas_as_sprites.update()
    todas_as_sprites.draw(screen)
    pygame.display.flip()
