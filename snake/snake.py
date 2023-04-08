import pygame
import time
import random


pygame.init()

## DISPLAY
WIDTH = 800                                               # Window size
WIN = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption("Snake")

## COLORS
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
L_BLUE = (0, 128, 255)
CYAN = (0, 255, 255)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
BLACK = (0, 0, 0)

font_style = pygame.font.SysFont(None, 200)

# Game over message
def message(msg,color):
    mesg = font_style.render(msg, True, color)
    WIN.blit(mesg, [0+70, WIDTH/2-100])

def main(win, width):

    # Variable declaration
    ## Snake variables
    snake_chunk = 20    # snake base square size
    snake_len = 1       # base snake length

    # Snake pos vars
    x1 = width/2 - 20   # snake x axis position
    y1 = width/2 - 20   # snake y axis pos

    # Snake movement vars
    x1_move = 0         # snake start x axis movement speed
    y1_move = 0         # snake start y axis movement speed

    # Food vars
    food_x = round(random.uniform(0 + 2*snake_chunk, width - 2*snake_chunk ) / 20.0) * 20.0     # random food x asix pos
    food_y = round(random.uniform(0 + 2*snake_chunk, width - 2*snake_chunk ) / 20.0) * 20.0     # random food y asix pos

    # Snake pos (logs) lists
    snake_pos_x = [x1]  
    snake_pos_y = [y1]  

    # game vars
    run = True
    game_over = False

    #clock vars
    clock = pygame.time.Clock()

    # Game loop
    while run and not game_over:
        # Game events
        for event in pygame.event.get():
            # Game quit
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                # Escape press -> quit
                if event.key == pygame.K_ESCAPE: 
                    pygame.quit()                    

            # Snake controls
            if event.type == pygame.KEYDOWN:
                # A or left arrow press -> move left if not moving right
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    if x1_move != snake_chunk:
                        x1_move = -snake_chunk
                        y1_move = 0
                # D or right arrow press -> move right if not moving left
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    if x1_move != -snake_chunk:
                        x1_move = snake_chunk
                        y1_move = 0
                # W or up arrow press -> move up if not moving down
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    if y1_move != snake_chunk:
                        x1_move = 0
                        y1_move = -snake_chunk
                # S or down arrow press -> move down if not moving up
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if y1_move != -snake_chunk:
                        x1_move = 0
                        y1_move = snake_chunk

        # Equivalent to x1 += x1_move
        snake_pos_x_cur = snake_pos_x[len(snake_pos_x)-1]
        # Equivalent to y1 += y1_move
        snake_pos_y_cur = snake_pos_y[len(snake_pos_y)-1] 
        snake_pos_x.append(snake_pos_x_cur + x1_move)
        snake_pos_y.append(snake_pos_y_cur + y1_move)
        #print("[X,Y] =","[",snake_pos_x_cur,",",snake_pos_y_cur,"]")
        
        # Map border collision -> Game over
        if snake_pos_x_cur+snake_chunk >= width or snake_pos_x_cur <= 0 or snake_pos_y_cur+snake_chunk >= width or snake_pos_y_cur <= 0:
            game_over = True

        # Background       
        win.fill(WHITE) 

        # Snake body frame reset
        snake_body = []
        snake_body_pos_x = []
        snake_body_pos_y = []

        # Snake body loop
        for i in range(1,snake_len):
            
            # Snake body pos (log) list
            snake_body_pos_x.append(snake_pos_x[len(snake_pos_x)-i-2])
            snake_body_pos_y.append(snake_pos_y[len(snake_pos_y)-i-2])
            # Snake body (light blue) draw
            snake_body.append(pygame.draw.rect(WIN, L_BLUE, [snake_pos_x[len(snake_pos_x)-i-2], snake_pos_y[len(snake_pos_y)-i-2] , snake_chunk ,snake_chunk]))

            # Snake body collision -> Game over
            if  snake_pos_x_cur == snake_body_pos_x[i-1] \
            and snake_pos_y_cur == snake_body_pos_y[i-1]:
                game_over = True
            
            # Food body collision -> new food position
            if  food_x == snake_body_pos_x[i-1] \
            and food_y == snake_body_pos_y[i-1]:
                food_x = round(random.uniform(0 + 2*snake_chunk, width - 2*snake_chunk ) / 20.0) * 20.0
                food_y = round(random.uniform(0 + 2*snake_chunk, width - 2*snake_chunk ) / 20.0) * 20.0

        # Food (red) draw 
        food = pygame.draw.rect(WIN, RED, [food_x,food_y, snake_chunk ,snake_chunk])
        # Snake head (blue) draw
        snake_head = pygame.draw.rect(WIN, BLUE, [snake_pos_x_cur, snake_pos_y_cur, snake_chunk ,snake_chunk])
        # Game frame update
        pygame.display.update()

        # Food collision - +1 snake body chunk
        if snake_pos_x_cur == food_x and snake_pos_y_cur == food_y:
            food_x = round(random.uniform(0 + 2*snake_chunk, width - 2*snake_chunk ) / 20.0) * 20.0
            food_y = round(random.uniform(0 + 2*snake_chunk, width - 2*snake_chunk ) / 20.0) * 20.0
            snake_len += 1
        
        # Game speed
        clock.tick(15)

    # Game end
    if game_over == True:
        time.sleep(2)
        win.fill(BLACK) 
        message("YOU DIED",RED)
        pygame.display.update()
        time.sleep(2)
    
main(WIN,WIDTH)