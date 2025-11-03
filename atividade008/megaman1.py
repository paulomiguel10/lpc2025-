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
        #oi
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
            self.velocidade_y = -20
           

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
        if self.direcao == -1:
            self.image = pygame.transform.flip(self.image, True, False)

    def update(self):
        if self. animar == True:
            self.atual = self.atual + 0.5
            if self.atual >= len(self.sprites):
                self.atual = 0
            self.image = self.sprites[int(self.atual)]
            self.image = pygame.transform.scale(self.image, (499/5, 500/5))
            #Inverte imagem se estiver indo para esquerda
            if self.direcao == -1:
                self.image = pygame.transform.flip(self.image, True, False)
        if hasattr(self, "velocidade_y"):
            self.rect.y += self.velocidade_y
            self.velocidade_y += 1

            if self.rect.y >= 530:
                self.rect.y = 530
                self.velocidade_y = 0
                self.sprites = self.sprites_andar
            else:
                self.sprites = self.sprites_pular
                
#Criação do sprite
todas_as_sprites = pygame.sprite.Group()
megaman = Megaman()
todas_as_sprites.add(megaman)

relogio = pygame.time.Clock()

#LOOP PRINCIPAL
running = True
while running:
    relogio.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
        
    keys = pygame.key.get_pressed()
    movendo = False
    
   

    if keys[pygame.K_RIGHT]:
        megaman.rect.x += megaman.velocidade
        megaman.direcao = 1
        megaman.andar(-1)
        movendo = True

    elif keys[pygame.K_LEFT]:
        megaman.rect.x -= megaman.velocidade
        megaman.andar(1)    
        movendo = True
    
    elif keys[pygame.K_SPACE]:
        megaman.pular()
        movendo = True
        
    if not movendo:
        megaman.parar()

    screen.blit(background, (0,0)) #Desenha o fundo 
    todas_as_sprites.draw(screen) 
    pygame.display.flip() #Atualiza a tela
    todas_as_sprites.update()

pygame.quit()