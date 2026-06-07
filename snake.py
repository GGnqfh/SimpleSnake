import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Colors
white = (255, 255, 255)
green = (0, 255, 0)
indigo = (75, 0, 130)

# Window size and title
dis_width = 800
dis_height = 600
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake')

# Game parameters
clock = pygame.time.Clock()
snake_block = 10
snake_speed = 15

# Fonts (using default font to avoid cross-platform issues)
font_style = pygame.font.Font(None, 30)
score_font = pygame.font.Font(None, 35)


def show_score(score):
    value = score_font.render("Score: " + str(score), True, white)
    dis.blit(value, [0, 0])


def draw_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, white, [x[0], x[1], snake_block, snake_block])


def display_message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])


def random_food(snake_list):
    """Generate food that does not overlap with the snake."""
    while True:
        fx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
        fy = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
        if [fx, fy] not in snake_list:
            return fx, fy


def gameLoop():
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx, foody = random_food(snake_List)

    while not game_over:

        # ----- Unified event handling -----
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if game_close:
                    # Keys in game-over screen
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_r:
                        gameLoop()   # Restart
                        return       # Exit current loop
                else:
                    # Direction controls (prevent immediate reverse)
                    if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and x1_change == 0:
                        x1_change = -snake_block
                        y1_change = 0
                    elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and x1_change == 0:
                        x1_change = snake_block
                        y1_change = 0
                    elif (event.key == pygame.K_UP or event.key == pygame.K_w) and y1_change == 0:
                        y1_change = -snake_block
                        x1_change = 0
                    elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and y1_change == 0:
                        y1_change = snake_block
                        x1_change = 0

        # Game over screen
        if game_close:
            dis.fill(indigo)
            display_message("Game Over! Press Q to quit or R to restart", white)
            show_score(Length_of_snake - 1)
            pygame.display.update()
            clock.tick(snake_speed)
            continue

        # Move the snake head
        x1 += x1_change
        y1 += y1_change

        # Border collision (using block boundary)
        if x1 < 0 or x1 + snake_block > dis_width or y1 < 0 or y1 + snake_block > dis_height:
            game_close = True
            continue

        # Draw background and food
        dis.fill(indigo)
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])

        # Update snake body
        snake_Head = [x1, y1]
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # Self collision check
        if snake_Head in snake_List[:-1]:
            game_close = True

        draw_snake(snake_block, snake_List)
        show_score(Length_of_snake - 1)
        pygame.display.update()

        # Eat food
        if x1 == foodx and y1 == foody:
            foodx, foody = random_food(snake_List)
            Length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    sys.exit()


gameLoop()