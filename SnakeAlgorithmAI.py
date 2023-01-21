import pygame
import sys
import numpy as np
import random
import time
import math

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
ready_to_move = True
move_one_block_counter = 0
SPEED = 1 # max speed = 0.5 (other smaller speeds have to be SPPED * X = 1 X is integer)

class Fruit:
    def __init__(self, pos):
        self.x = pos[0]
        self.y = pos[1]
    def draw_fruit(self, surface):
        pygame.draw.rect(surface, GREEN, (self.x*25, self.y*25, 25, 25))


class Snake:
    def __init__(self, x, y, direction):
        self.direction = direction
        self.length = 1
        self.body = [[x, y]]


    def grow(self,last_cell):
        self.length += 1
        self.body.append(last_cell)

    def check_collision_fruit(self, target):
        if math.floor(self.body[0][0]) == target.x and math.floor(self.body[0][1]) ==  target.y:
            return True

    def check_collision_body(self):
        for cell in self.body[1:]:
            if math.floor(cell[0]) == math.floor(self.body[0][0]) and math.floor(cell[1]) == math.floor(self.body[0][1]):
                return True
        #if len(snake.body) != len(set(snake.body)):

    def check_wall_collision(self,grid):
        if 2 in list(grid[:,ROWS]) or 2 in list(grid[COLS,:]):
            return True

    def move(self):
        base_x = math.floor(self.body[0][0])
        base_y = math.floor(self.body[0][1])
        # 1=UP,2=RIGHT,3=DOWN,4=LEFT
        if self.direction == 1:
            if(math.floor(self.body[0][1] - SPEED) != base_y):
                for body in reversed(self.body):
                    if self.body.index(body) != 0:
                        index = self.body.index(body)
                        self.body[index] = self.body[index - 1]
                    else:
                        self.body[0] = body[0], body[1] - SPEED
            else:
                self.body[0] = self.body[0][0], self.body[0][1] - SPEED
        if self.direction == 2:
            if(math.floor(self.body[0][0] + SPEED) != base_x):
                for body in reversed(self.body):
                    if self.body.index(body) != 0:
                        index = self.body.index(body)
                        self.body[index] = self.body[index - 1]
                    else:
                        self.body[0] = body[0] + SPEED, body[1]
            else:
                self.body[0] = self.body[0][0] + SPEED, self.body[0][1]
        if self.direction == 3:
            if(math.floor(self.body[0][1] + SPEED) != base_y):
                for body in reversed(self.body):
                    if self.body.index(body) != 0:
                        index = self.body.index(body)
                        self.body[index] = self.body[index - 1]
                    else:
                        self.body[0] = body[0], body[1] + SPEED
            else:
                self.body[0] = self.body[0][0], self.body[0][1] + SPEED
        if self.direction == 4:
            if(math.floor(self.body[0][0] - SPEED) != base_x):
                for body in reversed(self.body):
                    if self.body.index(body) != 0:
                        index = self.body.index(body)
                        self.body[index] = self.body[index - 1]
                    else:
                        self.body[0] = body[0] - SPEED, body[1]
            else:
                self.body[0] = self.body[0][0] - SPEED, self.body[0][1]


window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF)
pygame.display.set_caption("SnakeAlgorithmicAI")
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
    fruit_x, fruit_y = target[0], target[1]
    grid[fruit_y][fruit_x] = 3
    for cell in body:
        x = math.floor(cell[0])
        y = math.floor(cell[1])
        grid[y][x] = 1
    head_x = math.floor(body[0][0])
    head_y = math.floor(body[0][1])
    grid[head_y][head_x] = 2
    return grid

def draw_board(grid,surface):
    for x,y in np.ndindex(grid.shape):
        if grid[y][x] == 0:
            pygame.draw.rect(surface, BLACK, (x*25, y*25, 25, 25))
        elif grid[y][x] == 2:
            pygame.draw.rect(surface, MAGENTA, (x*25, y*25, 25, 25))
        elif grid[y][x] == 1:
            pygame.draw.rect(surface, RED, (x*25, y*25, 25, 25))


def randomizing_fruit_cords(grid):
    available_xy = []
    for x, y in np.ndindex(grid.shape):
        if x != ROWS and y != COLS:
            if grid[y,x] == 0:
                available_xy.append([x,y])
    if len(available_xy) == 0:
        return False
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

def make_move(board,snake,ready_to_move):
    head_position = np.where(board == 2)
    future_direction = None
    if head_position[0] == 19:
        snake.direction = 4
        future_direction = 1
        ready_to_move = False
    elif head_position[0] == 1 and head_position[1] != 0 and head_position[1] != 19:
        snake.direction = 4
        future_direction = 3
        ready_to_move = False
    elif head_position[0] == 0 and head_position[1] == 0:
        snake.direction = 2
    elif head_position[0] == 0 and head_position[1] == 19:
        snake.direction = 3
    return future_direction,ready_to_move

board = create_board(ROWS,COLS)
snake = Snake(10, 10, 1)
fruit = Fruit(randomizing_fruit_cords(board))
snake.move()
while not game_over:
    if ready_to_move:
        future_direction,ready_to_move = make_move(board,snake,ready_to_move)
    else:
        move_one_block_counter += 1
        if move_one_block_counter == 1/SPEED:
            ready_to_move = True
            move_one_block_counter = 0
            if future_direction != None:
                snake.direction = future_direction
    if snake.check_collision_fruit(fruit):
        del fruit
        snake.grow(prev_body[-1])
        new_fruit_cords = randomizing_fruit_cords(board)
        if new_fruit_cords == False:
            game_over = True
            fruit = Fruit((20,20))
        else:
            fruit = Fruit(new_fruit_cords)

    if snake.check_wall_collision(board):
        game_over = True
    reset_board(board)
    if snake.check_collision_body():
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
        snake = Snake(10, 10, 1)
        future_direction = None
        move_one_block_counter = 0
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
    clock.tick(60)
    time_to_display = time.perf_counter_ns() - time_to_subtract
    time_to_display = "%s:%s" % compute_time(time_to_display)
    timer = my_font.render(time_to_display,1,WHITE)
    length = my_font.render(str(score),1,WHITE)
    info_surface.blit(timer,(140,30))
    info_surface.blit(length,(320,30))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()