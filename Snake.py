import pygame
import sys
import numpy as np
import random
import time

pygame.init()
clock = pygame.time.Clock()
pygame.font.init()
my_font = pygame.font.SysFont('calibri',58)
small_font = pygame.font.SysFont('calibri',32)
WIDTH = 500
HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (64, 64, 64)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
MAGENTA = (255, 0, 255)
ROWS = int((HEIGHT - 100) / 25)
COLS = int(WIDTH / 25)
game_over = False
time_to_display = 0
time_to_subtract = 0
score = 0
high_score = 0

class Fruit:
    def __init__(self, pos):
        x, y = int(pos[0] * 25), int((pos[1] * 25))
        self.x = x
        self.y = y
    def draw_fruit(self, surface):
        pygame.draw.rect(surface, GREEN, (self.x, self.y, 25, 25))


class Snake:
    def __init__(self, x, y, direction):
        x, y = int(x * 25), int((y * 25))
        self.direction = direction
        self.length = 1
        self.body = [[x, y]]

    def draw_head(self, surface):
        pygame.draw.rect(surface, MAGENTA, (self.body[0][0], self.body[0][1], 25, 25))

    def draw_body(self, surface):
        for body in self.body[1:]:
            pygame.draw.rect(surface, RED, (body[0], body[1], 25, 25))

    def grow(self,last_cell):
        self.length += 1
        self.body.append(last_cell)

    def check_collision_fruit(self, target):
        if self.body[0] == (target.x, target.y):
            return True

    def check_collision_body(self,grid):
        head = snake.body[0]
        if len(snake.body) != len(set(snake.body)):
            return True

    def check_wall_collision(self,grid):
        if 2 in list(grid[:,20]) or 2 in list(grid[20,:]):
            return True

    def move(self):
        # 1=UP,2=RIGHT,3=DOWN,4=LEFT
        if self.direction == 1:
            for body in reversed(self.body):
                if self.body.index(body) != 0:
                    index = self.body.index(body)
                    self.body[index] = self.body[index - 1]
                else:
                    self.body[0] = body[0], body[1] - 25
        if self.direction == 2:
            for body in reversed(self.body):
                if self.body.index(body) != 0:
                    index = self.body.index(body)
                    self.body[index] = self.body[index - 1]
                else:
                    self.body[0] = body[0] + 25, body[1]
        if self.direction == 3:
            for body in reversed(self.body):
                if self.body.index(body) != 0:
                    index = self.body.index(body)
                    self.body[index] = self.body[index - 1]
                else:
                    self.body[0] = body[0], body[1] + 25
        if self.direction == 4:
            for body in reversed(self.body):
                if self.body.index(body) != 0:
                    index = self.body.index(body)
                    self.body[index] = self.body[index - 1]
                else:
                    self.body[0] = body[0] - 25, body[1]


window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF)
pygame.display.set_caption("SnakeGame")
play_surface = pygame.Surface((500, 500))
info_surface = pygame.Surface((500, 100))
info_surface.fill(GRAY)
play_surface.fill(BLACK)
window.blit(play_surface,(0, 100))
window.blit(info_surface,(0, 0))
pygame.display.update()


def create_board(rows, cols):
    return np.zeros((rows+1, cols+1)).astype(int)


def reset_board(grid):
    grid.fill(0)


def fill_board(grid, body, target):
    for cell in body:
        x = int(cell[0] / 25)
        y = int((cell[1] / 25))
        grid[x][y] = 1
    head_x = body[0][0] // 25
    head_y = body[0][1] // 25
    grid[head_x][head_y] = 2
    fruit_x, fruit_y = int(target[0] / 25), int((target[1] / 25))
    grid[fruit_y][fruit_x] = 3
    return grid

def draw_board(grid,surface):
    for x,y in np.ndindex(grid.shape):
        if grid[x][y] == 0:
            pygame.draw.rect(surface, BLACK, (x*25, y*25, 25, 25))


def randomizing_fruit_cords(grid):
    available_xy = []
    for x, y in np.ndindex(grid.shape):
        if x != 0 and x != 20 and y != 0 and y != 20:
            if grid[x,y] == 0:
                available_xy.append([x,y])
    cords = random.choice(available_xy)
    return cords[0],cords[1]

def compute_time(nanoseconds):
    seconds = int(int(nanoseconds)/1000000000)
    minutes = int(seconds/60)
    return minutes,seconds-(60*minutes)

def draw_start_screen(time_to_display,score,high_score):
    game_over_text = my_font.render("Game Over",1,WHITE)
    timer = my_font.render(f"Current time: {time_to_display}", 1, WHITE)
    score = my_font.render(f"Current Score: {score}", 1, WHITE)
    high_score = my_font.render(f"High Score: {high_score}", 1, WHITE)
    restart_info = small_font.render("press space to restart", 1, WHITE)
    window.fill(BLACK)
    window.blit(game_over_text,(30,10))
    window.blit(timer, (30, 100))
    window.blit(score, (30, 300))
    window.blit(high_score, (30, 500))
    window.blit(restart_info, (130, 550))
    pygame.display.update()



board = create_board(ROWS,COLS)
snake = Snake(10, 10, 3)
fruit = Fruit(randomizing_fruit_cords(board))
snake.move()
while not game_over:
    if snake.check_collision_fruit(fruit):
        del fruit
        snake.grow(prev_body[-1])
        fruit = Fruit(randomizing_fruit_cords(board))
    else:
        if snake.check_wall_collision(board):
            game_over = True
        reset_board(board)
        if snake.check_collision_body(board):
            game_over = True
        score = snake.length
        if game_over == True:
            if high_score < score:
                high_score = score
            del snake
            del fruit
            draw_start_screen(time_to_display,score,high_score)
            while game_over:
                for event in pygame.event.get():
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_SPACE:
                            game_over = False
                    if event.type == pygame.QUIT:
                        sys.exit()
            play_surface.fill(BLACK)
            info_surface.fill(GRAY)
            snake = Snake(10, 10, 3)
            fruit = Fruit(randomizing_fruit_cords(board))
            time_to_subtract = time.perf_counter_ns()
            pygame.display.update()
        prev_body = snake.body.copy()
        snake.move()
        fill_board(board, snake.body, (fruit.x, fruit.y))
        window.blit(play_surface, (0, 100))
        window.blit(info_surface, (0, 0))
        info_surface.fill(GRAY)
        draw_board(board, play_surface)
        fruit.draw_fruit(play_surface)
        snake.draw_head(play_surface)
        snake.draw_body(play_surface)
        clock.tick(10)
        time_to_display = time.perf_counter_ns() - time_to_subtract
        time_to_display = "%s:%s" % compute_time(time_to_display)
        timer = my_font.render(time_to_display,1,WHITE)
        length = my_font.render(str(score),1,WHITE)
        info_surface.blit(timer,(140,30))
        info_surface.blit(length,(320,30))
        pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and snake.direction != 3:
                snake.direction = 1
            if event.key == pygame.K_d and snake.direction != 4:
                snake.direction = 2
            if event.key == pygame.K_s and snake.direction != 1:
                snake.direction = 3
            if event.key == pygame.K_a and snake.direction != 2:
                snake.direction = 4
        if event.type == pygame.QUIT:
            sys.exit()