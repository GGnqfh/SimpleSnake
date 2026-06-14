import pygame
import random
import sys
import math

pygame.init()

BLACK = (10, 10, 20)
DARK_GRID = (20, 25, 40)
SNAKE_HEAD = (100, 255, 100)
SNAKE_BODY = (50, 200, 50)
FOOD_COLOR = (255, 60, 60)
FOOD_GLOW = (255, 120, 80)
SCORE_BG = (30, 35, 55, 200)
SCORE_TEXT = (220, 220, 255)
WHITE = (255, 255, 255)
OVERLAY = (0, 0, 0, 180)

DIS_WIDTH = 800
DIS_HEIGHT = 600
BLOCK = 20
SPEED = 10

dis = pygame.display.set_mode((DIS_WIDTH, DIS_HEIGHT))
pygame.display.set_caption('Simple Snake')

clock = pygame.time.Clock()

font_large = pygame.font.Font(None, 72)
font_medium = pygame.font.Font(None, 36)
font_small = pygame.font.Font(None, 24)


def draw_grid():
    for x in range(0, DIS_WIDTH, BLOCK):
        pygame.draw.line(dis, DARK_GRID, (x, 0), (x, DIS_HEIGHT))
    for y in range(0, DIS_HEIGHT, BLOCK):
        pygame.draw.line(dis, DARK_GRID, (0, y), (DIS_WIDTH, y))


def show_score(score):
    text = font_medium.render(f"Score: {score}", True, SCORE_TEXT)
    pad = 10
    bg = pygame.Surface((text.get_width() + pad * 2, text.get_height() + pad * 2), pygame.SRCALPHA)
    pygame.draw.rect(bg, SCORE_BG, bg.get_rect(), border_radius=8)
    dis.blit(bg, (10, 10))
    dis.blit(text, (10 + pad, 10 + pad))


def draw_snake(snake_list):
    n = len(snake_list)
    for i, (x, y) in enumerate(snake_list):
        t = i / max(n, 1)
        if i == n - 1:
            color = SNAKE_HEAD
            pygame.draw.rect(dis, color, (x + 1, y + 1, BLOCK - 2, BLOCK - 2), border_radius=4)
            eye_size = 3
            off = 5
            pygame.draw.circle(dis, BLACK, (x + off, y + off), eye_size)
            pygame.draw.circle(dis, BLACK, (x + BLOCK - off, y + off), eye_size)
        else:
            r = int(SNAKE_HEAD[0] * (1 - t) + SNAKE_BODY[0] * t)
            g = int(SNAKE_HEAD[1] * (1 - t) + SNAKE_BODY[1] * t)
            b = int(SNAKE_HEAD[2] * (1 - t) + SNAKE_BODY[2] * t)
            pygame.draw.rect(dis, (r, g, b), (x + 1, y + 1, BLOCK - 2, BLOCK - 2), border_radius=4)


def draw_food(x, y, time):
    cx, cy = x + BLOCK // 2, y + BLOCK // 2
    pulse = math.sin(time * 0.005) * 3
    glow_r = int(BLOCK * 0.75 + pulse)
    surf = pygame.Surface((glow_r * 2, glow_r * 2), pygame.SRCALPHA)
    for i in range(3):
        r = glow_r - i * 3
        alpha = 80 // (i + 1)
        pygame.draw.circle(surf, (*FOOD_GLOW, alpha), (glow_r, glow_r), r)
    dis.blit(surf, (cx - glow_r, cy - glow_r))
    pygame.draw.circle(dis, FOOD_COLOR, (cx, cy), BLOCK // 2 - 2)


def show_game_over(score):
    overlay = pygame.Surface((DIS_WIDTH, DIS_HEIGHT), pygame.SRCALPHA)
    overlay.fill(OVERLAY)
    dis.blit(overlay, (0, 0))

    t1 = font_large.render("Game Over", True, FOOD_COLOR)
    t2 = font_medium.render(f"Score: {score}", True, SCORE_TEXT)
    t3 = font_small.render("Press R to Restart  |  Q to Quit", True, (150, 150, 180))

    dis.blit(t1, t1.get_rect(center=(DIS_WIDTH // 2, DIS_HEIGHT // 2 - 60)))
    dis.blit(t2, t2.get_rect(center=(DIS_WIDTH // 2, DIS_HEIGHT // 2)))
    dis.blit(t3, t3.get_rect(center=(DIS_WIDTH // 2, DIS_HEIGHT // 2 + 50)))


def random_food(snake_list):
    cells = [(x, y) for x in range(0, DIS_WIDTH, BLOCK) for y in range(0, DIS_HEIGHT, BLOCK)
             if [x, y] not in snake_list]
    return random.choice(cells) if cells else (0, 0)


def gameLoop():
    while True:
        game_over = False
        game_close = False

        x1 = DIS_WIDTH // 2
        y1 = DIS_HEIGHT // 2
        x1_change = 0
        y1_change = 0

        snake_list = []
        length = 1
        foodx, foody = random_food(snake_list)

        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if game_close:
                        if event.key == pygame.K_q:
                            pygame.quit()
                            sys.exit()
                        if event.key == pygame.K_r:
                            game_over = True
                            break
                    else:
                        k = event.key
                        if k in (pygame.K_LEFT, pygame.K_a) and x1_change == 0:
                            x1_change = -BLOCK; y1_change = 0
                        elif k in (pygame.K_RIGHT, pygame.K_d) and x1_change == 0:
                            x1_change = BLOCK; y1_change = 0
                        elif k in (pygame.K_UP, pygame.K_w) and y1_change == 0:
                            y1_change = -BLOCK; x1_change = 0
                        elif k in (pygame.K_DOWN, pygame.K_s) and y1_change == 0:
                            y1_change = BLOCK; x1_change = 0

            if game_over:
                break

            if game_close:
                dis.fill(BLACK)
                show_game_over(length - 1)
                pygame.display.update()
                clock.tick(SPEED)
                continue

            x1 += x1_change
            y1 += y1_change

            if x1 < 0 or x1 + BLOCK > DIS_WIDTH or y1 < 0 or y1 + BLOCK > DIS_HEIGHT:
                game_close = True
                continue

            dis.fill(BLACK)
            draw_grid()
            draw_food(foodx, foody, pygame.time.get_ticks())

            head = [x1, y1]
            snake_list.append(head)
            if len(snake_list) > length:
                del snake_list[0]

            if head in snake_list[:-1]:
                game_close = True

            draw_snake(snake_list)
            show_score(length - 1)
            pygame.display.update()

            if x1 == foodx and y1 == foody:
                foodx, foody = random_food(snake_list)
                length += 1

            clock.tick(SPEED)

    pygame.quit()
    sys.exit()


gameLoop()
