# breakout

# First code test comment break- DESKTOP-1RLNS3S.py
import math
import pygame

pygame.init()
pygame.mixer.init()

screen_size = (800, 800)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Breakout")

ball_size = 15
ball = pygame.Rect(400, 500, ball_size, ball_size)

player_size = 100
player = pygame.Rect(400, 750, player_size, 15)

blocks_lines = 14 
lines_blocks = 8

def create_blocks(blocks_line, lines_blocks):
    width_size, height_size = screen_size
    block_distance = int(screen_size[0]*0.008)  # decrease block spacing
    width_block = width_size / blocks_line - block_distance
    height_block = int(screen_size[1]*0.015)    # thinner height
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

# Map each color to a score value
points_per_color = {
    color["yellow"]: 1,  # Yellow worth less
    color["green"]: 3,
    color["orange"]: 5,
    color["red"]: 7      # Red worth more
}

end_game = False
lives = 3 
score = 0
speed_level_1 = 2.5 # Initial speed
speed_level_2 = 4.0 # Speed when hitting first green
speed_level_3 = 12.0 # Speed when hitting first red

# Flags to control if speed has already changed
hit_green = False
hit_red = False
# The initial direction will be diagonal. Normalize vector [1, 1] and multiply by speed.
ball_move = [speed_level_1 / (2**0.5), speed_level_1 / (2**0.5)]

def draw_startgame():
    screen.fill(color["black"])
    pygame.draw.rect(screen, color["blue"], player)
    pygame.draw.rect(screen, color["white"], ball)

# Colors by line
line_colors = [color["red"], color["red"], color["orange"], color["orange"],
                color["green"], color["green"], color["yellow"], color["yellow"]]

blocks = create_blocks(blocks_lines, lines_blocks) # creates new top blocks and overlays the colors

def draw_blocks(blocks):
    for idx, block in enumerate(blocks):
        line = idx // blocks_lines
        pygame.draw.rect(screen, line_colors[line], block) # function to enumerate and overlay blocks
        
def update_player_movement():
    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT]:
        if (player.x + player_size) < screen_size[0]:
            player.x = player.x + 5

    if keys[pygame.K_LEFT]:
        if player.x > 0:
            player.x = player.x - 5

sound_blocks = pygame.mixer.Sound("./assets/breaksound.wav")
sound_collision = pygame.mixer.Sound("./assets/bounce.wav")
sound_loss = pygame.mixer.Sound("./assets/wrong-buzzer-6268.mp3")

def move_ball(ball, lives):
    global ball_move
    movement = ball_move
    ball.x = ball.x + movement[0]
    ball.y = ball.y + movement[1]

    if ball.x <= 0:
        movement[0] = -movement[0]
        sound_collision.play()
    if ball.y < 0:
        movement[1] = -movement[1]
        sound_collision.play()
    if ball.x + ball_size >= screen_size[0]:
        movement[0] = -movement[0]
        sound_collision.play()

    # Lives system       
    if ball.y + ball_size >= screen_size[1]:
         sound_loss.play()
         lives -= 1
         if lives > 0:
             ball.x = screen_size[0] // 2
             ball.y = screen_size[1] // 2
             movement[0] = speed_level_1/math.sqrt(2)
             movement[1] = -speed_level_1/math.sqrt(2)
             return movement, lives
         else:
             return None, lives # no lives left

    return movement, lives
    
blocks = create_blocks(blocks_lines, lines_blocks)

def ball_collision_player(ball, player):
    global hit_green, hit_red
    if ball.colliderect(player):
        sound_collision.play()
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
            # Start with base speed.
            target_speed = speed_level_1

            # If level 2 was activated, use speed 2.
            if hit_green:
                target_speed = speed_level_2
            
            # If level 3 was activated, it OVERWRITES speed 2.
            # Use separate if instead of elif to ensure priority.
            if hit_red:
                target_speed = speed_level_3
            current_speed = (ball_move[0]**2 + ball_move[1]**2)**0.5
            if current_speed > 0:
                factor = target_speed / current_speed
                ball_move[0] *= factor
                ball_move[1] *= factor

while not end_game:
    result = move_ball(ball,lives)
    draw_startgame()
    draw_blocks(blocks)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end_game = True

    update_player_movement()

    if result is None:  # if lives are over, game ends
         pygame.display.flip()
         break
    else:
         ball_move, lives = result

    ball_collision_player(ball, player)
   # Collision with blocks
    for idx, block in enumerate(blocks[:]):
        if ball.colliderect(block):
            sound_blocks.play()
            # 1. Get the color of the block that was hit
            block_line = idx // blocks_lines
            block_color = line_colors[block_line]

            target_speed = 0 # Variable to store new desired speed

            # If hitting a RED block for the FIRST TIME
            if block_color == color["red"] and not hit_red:
                hit_red = True # Mark that we reached level 3
                hit_green = True    # Level 3 also counts as having reached level 2
                target_speed = speed_level_3
                print("SPEED LEVEL 3 activated!") # Feedback message (optional)

            # If hitting a GREEN block for the FIRST TIME (and not level 3 yet)
            elif block_color == color["green"] and not hit_green:
                hit_green = True # Mark that we reached level 2
                target_speed = speed_level_2
                print("SPEED LEVEL 2 activated!") # Feedback message (optional)

            # If target_speed was set, adjust ball_move
            if target_speed > 0:
                # Calculate current speed to find scale factor
                current_speed = (ball_move[0]**2 + ball_move[1]**2)**0.5
                
                # Avoid division by zero if ball stopped
                if current_speed > 0:
                    factor = target_speed / current_speed
                    ball_move[0] *= factor
                    ball_move[1] *= factor

            # 2. Get points for that color
            points_gained = points_per_color.get(block_color, 1) # default 1

            # 3. Update game logic
            ball_move[1] = -ball_move[1]
            blocks.remove(block)
            score += points_gained
            break  # Avoid multiple collisions in same update

    # Draw proportional score
    font = pygame.font.SysFont(None, int(screen_size[1]*0.04))
    score_text = font.render(f"Score: {score}", True, color["white"])
    screen.blit(score_text, (10, 10))

    # Draw lives system
    lives_text = font.render(f"Lives: {lives}",True ,color["white"] )
    screen.blit(lives_text,(10,40))
    

    pygame.time.wait(5)
    pygame.display.flip()

pygame.quit()
