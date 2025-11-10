import pygame
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

# Initialization
pygame.init()
pygame.mixer.init()

# === SOUNDS ===
BASE = Path(__file__).resolve().parent
sound_shot = pygame.mixer.Sound("atividade008/megaman1/sounds/tiro.wav")
sound_jump = pygame.mixer.Sound("atividade008/megaman1/sounds/jump.wav")

# Background music
pygame.mixer.music.load("atividade008/megaman1/sounds/soundtrack.mp3")  # music file path
pygame.mixer.music.set_volume(0.4)  # volume from 0.0 to 1.0
pygame.mixer.music.play(-1)  # -1 means infinite loop

#SCREEN SETTINGS 
screen_size = (850, 720)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Sprites")

#BACKGROUND 
background = pygame.image.load('atividade008/megaman1/sprites/fundo.png')
background = pygame.transform.scale(background, screen_size)

class Megaman(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = []

        # Walking sprites
        self.sprites_walk = [
            pygame.image.load('atividade008/megaman1/sprites/andar1.png'),
            pygame.image.load('atividade008/megaman1/sprites/andar2.png'),
            pygame.image.load('atividade008/megaman1/sprites/andar3.png')
        ]

        # Idle sprite
        self.sprites_idle = [
            pygame.image.load('atividade008/megaman1/sprites/parado_1.png')
        ]

        # Jumping sprite
        self.sprites_jump = [
            pygame.image.load('atividade008/megaman1/sprites/pulo.png')
        ]

        # Shooting while standing
        self.sprites_shoot_idle = [
            pygame.image.load('atividade008/megaman1/sprites/parado_atira.png')
        ]

        # Shooting while running
        self.sprites_shoot_running = [
            pygame.image.load('atividade008/megaman1/sprites/atira_1.png'),
            pygame.image.load('atividade008/megaman1/sprites/atira_2.png'),
            pygame.image.load('atividade008/megaman1/sprites/atira_3.png')
        ]

        # Shooting while jumping
        self.sprites_shoot_jumping = [
            pygame.image.load('atividade008/megaman1/sprites/pularatirando.png')
        ]

        # Initial animation
        self.sprites = self.sprites_walk

        self.current_frame = 0
        self.speed = 8  # movement speed
        self.direction = 1  # right: 1  left: -1
        self.image = self.sprites[self.current_frame]
        self.image = pygame.transform.scale(self.image, (499/5, 500/5))

        self.rect = self.image.get_rect()
        self.rect.topleft = 200, 530
        self.animate = False
    
    def jump(self):
        if self.rect.y == 530 and (not hasattr(self, "velocity_y") or self.velocity_y == 0):
            sound_jump.play()
            self.animate = True
            self.sprites = self.sprites_jump
            self.image = self.sprites[0]
            self.image = pygame.transform.scale(self.image, (499/5, 500/5))
            self.velocity_y = -17

    def shoot_idle(self):
        self.animate = True
        self.current_frame = 0
        self.sprites = self.sprites_shoot_idle
        self.image = self.sprites[0] 
        self.image = pygame.transform.scale(self.image, (499/4.6, 500/4.6))
        
        if self.direction == 1:
            self.image = pygame.transform.flip(self.image, True, False)
    
    def shoot_running(self):
        self.animate = True
        self.current_frame = 0
        self.sprites = self.sprites_shoot_running

    def walk(self, direction):
        self.animate = True
        self.direction = direction
        self.sprites = self.sprites_walk

    def stop(self):
        self.animate = False
        self.current_frame = 0
        self.sprites = self.sprites_idle
        self.image = self.sprites[0]
        self.image = pygame.transform.scale(self.image, (499/5, 500/5))

        if self.direction == 1:
            self.image = pygame.transform.flip(self.image, True, False)

    def update(self):
        if self.animate:
            self.current_frame += 0.2
            if self.current_frame >= len(self.sprites):
                self.current_frame = 0
            self.image = self.sprites[int(self.current_frame)]
            self.image = pygame.transform.scale(self.image, (499/5, 500/5))

            # Flip image if facing right
            if self.direction == 1:
                self.image = pygame.transform.flip(self.image, True, False)
  
        if hasattr(self, "velocity_y"):
            self.rect.y += self.velocity_y
            self.velocity_y += 1

            if self.rect.y >= 530:
                self.rect.y = 530
                self.velocity_y = 0
            else:
                self.sprites = self.sprites_jump
                self.image = self.sprites[0]
                self.image = pygame.transform.scale(self.image, (499/5, 500/5))
                if self.direction == 1:
                    self.image = pygame.transform.flip(self.image, True, False)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.sprites_bullet = [pygame.image.load('atividade008/megaman1/sprites/tiro.png')]
        self.image = self.sprites_bullet[0]
        self.image = pygame.transform.scale(self.image, (30, 15))
        # bullet size

        # Flip if facing right (1)
        if direction == 1:
            self.image = pygame.transform.flip(self.image, True, False)

        # Position and direction
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        self.speed = 15 * direction

    def update(self):
        self.rect.x += self.speed
        if self.rect.x < 0 or self.rect.x > 850:
            self.kill()

#SPRITE CREATION
all_sprites = pygame.sprite.Group()
megaman = Megaman()
bullets = pygame.sprite.Group()
all_sprites.add(megaman)

clock = pygame.time.Clock()

#MAIN LOOP 
running = True
while running:
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
        
        # Create bullet when pressing S
        if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            sound_shot.play()
            if megaman.direction == 1:
                bullet_x = megaman.rect.right - 10
            else:
                bullet_x = megaman.rect.left + 10

            bullet_y = megaman.rect.centery - 0.5
            bullet = Bullet(bullet_x, bullet_y, megaman.direction)
            all_sprites.add(bullet)
            bullets.add(bullet)

    keys = pygame.key.get_pressed()
    moving = False

    # Move right
    if keys[pygame.K_RIGHT]:
        megaman.rect.x += megaman.speed
        megaman.direction = 1
        if keys[pygame.K_s]:
            megaman.shoot_running()
        else:
            megaman.walk(1)
        moving = True

    # Move left
    elif keys[pygame.K_LEFT]:
        megaman.rect.x -= megaman.speed
        megaman.direction = -1
        if keys[pygame.K_s]:
            megaman.shoot_running()
            moving = True
        else:
            megaman.walk(-1)    
        moving = True

    # Shoot idle animation
    if keys[pygame.K_s] and megaman.rect.y == 530 and not (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]):
        megaman.shoot_idle()
        moving = True

    # Jump
    elif keys[pygame.K_SPACE]:
        megaman.jump()
        moving = True
        
    # Idle
    if not moving:
        megaman.stop()

    # === SCREEN UPDATE ===
    screen.blit(background, (0,0))
    all_sprites.update()
    all_sprites.draw(screen)
    pygame.display.flip()
