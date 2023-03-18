import pygame
import sys
import numpy as np
import random
import time
import math

pygame.init()
clock = pygame.time.Clock()
clock.tick(60)
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
SPEED = 1
game_over = False
time_to_display = 0
time_to_subtract = 0
score = 0
high_score = 0

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

    def check_wall_collision(self,grid):
        if 2 in list(grid[:,ROWS]) or 2 in list(grid[COLS,:]):
            return True

    def move(self, turn):
        base_x = math.floor(self.body[0][0])
        base_y = math.floor(self.body[0][1])
        # directions 1=UP,2=RIGHT,3=DOWN,4=LEFT
        # straight = 0, turn left = 1 turn right = 2
        left_turns = [4,1,2,3]
        right_turns = [2,3,4,1]
        if turn == 1:
            self.direction = left_turns[self.direction-1]
        elif turn == 2:
            self.direction = right_turns[self.direction-1]
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


class Environement():
    def __init__(self):
        self.high_score = 0
        self.game_over = False
        self.prev_body = 0
        self.last_4_actions = [0,0,0,0]
        self.time_to_subtract = 0
        self.create_board()
        self.snake = Snake(10, 10, 1)
        self.fruit = Fruit(self.randomizing_fruit_cords())
        self.window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF)
        pygame.display.set_caption("SnakeGame")
        self.fill_board()
        self.play_surface = pygame.Surface((500, 500))
        self.info_surface = pygame.Surface((500, 100))
        self.info_surface.fill(GRAY)
        self.play_surface.fill(BLACK)
        self.fruit.draw_fruit(self.play_surface)
        self.draw_board()
        timer = my_font.render("0",1,WHITE)
        length = my_font.render(str(self.snake.length),1,WHITE)
        self.info_surface.blit(timer,(140,30))
        self.info_surface.blit(length,(320,30))
        self.window.blit(self.play_surface, (0, 100))
        self.window.blit(self.info_surface, (0, 0))
        pygame.display.update()


    def create_board(self):
        self.grid = np.zeros((ROWS+1, COLS+1)).astype(int)


    def reset_board(self):
        self.grid.fill(0)

    def get_board(self):
        return self.grid

    def get_direction_down(self): #1=UP,2=RIGHT,3=DOWN,4=LEFT
        return self.snake.direction == 3

    def get_direction_up(self):
        return self.snake.direction == 1

    def get_direction_left(self):
        return self.snake.direction == 4

    def get_direction_right(self):
        return self.snake.direction == 2

    def get_food_above(self): #absolutes x,y
        return self.snake.body[0][1] > self.fruit.y

    def get_food_below(self):
        return self.snake.body[0][1] < self.fruit.y

    def get_food_right(self):
        return self.snake.body[0][0] < self.fruit.x

    def get_food_left(self):
        return self.snake.body[0][0] > self.fruit.x

    def get_obstacle_left(self):
        return (self.snake.body[0][1] == 0 and self.snake.direction == 2) or (self.snake.body[0][1] == 19 and self.snake.direction == 4) or (self.snake.body[0][0] == 0 and self.snake.direction == 1) or (self.snake.body[0][0] == 19 and self.snake.direction == 3) \
        or (self.grid[self.snake.body[0][1]][self.snake.body[0][0]-1] == 1 and self.snake.direction == 1) or (self.grid[self.snake.body[0][1]][self.snake.body[0][0]+1] == 1 and self.snake.direction == 3) or (self.grid[self.snake.body[0][1]+1][self.snake.body[0][0]] == 1 and self.snake.direction == 4) \
        or (self.grid[self.snake.body[0][1]-1][self.snake.body[0][0]] == 1 and self.snake.direction == 2)

    def get_obstacle_right(self):
        return (self.snake.body[0][1] == 0 and self.snake.direction == 4) or (self.snake.body[0][1] == 19 and self.snake.direction == 2) or (self.snake.body[0][0] == 0 and self.snake.direction == 3) or (self.snake.body[0][0] == 19 and self.snake.direction == 1) \
        or (self.grid[self.snake.body[0][1]][self.snake.body[0][0]+1] == 1 and self.snake.direction == 1) or (self.grid[self.snake.body[0][1]][self.snake.body[0][0]-1] == 1 and self.snake.direction == 3) or (self.grid[self.snake.body[0][1]-1][self.snake.body[0][0]] == 1 and self.snake.direction == 4) \
        or (self.grid[self.snake.body[0][1]+1][self.snake.body[0][0]] == 1 and self.snake.direction == 2)

    def get_obstacle_straight(self):
        return (self.snake.body[0][1] == 0 and self.snake.direction == 1) or (self.snake.body[0][1] == 19 and self.snake.direction == 3) or (self.snake.body[0][0] == 0 and self.snake.direction == 4) or(self.snake.body[0][0] == 19 and self.snake.direction == 2) \
        or (self.grid[self.snake.body[0][1]-1][self.snake.body[0][0]] == 1 and self.snake.direction == 1) or (self.grid[self.snake.body[0][1]+1][self.snake.body[0][0]] == 1 and self.snake.direction == 3) or (self.grid[self.snake.body[0][1]][self.snake.body[0][0]-1] == 1 and self.snake.direction == 4) \
        or (self.grid[self.snake.body[0][1]][self.snake.body[0][0]+1] == 1 and self.snake.direction == 2)

    def fill_board(self):
        fruit_x, fruit_y = self.fruit.x, self.fruit.y
        self.grid[fruit_y][fruit_x] = 3
        for cell in self.snake.body:
            x = math.floor(cell[0])
            y = math.floor(cell[1])
            self.grid[y][x] = 1
        head_x = math.floor(self.snake.body[0][0])
        head_y = math.floor(self.snake.body[0][1])
        self.grid[head_y][head_x] = 2

    def draw_board(self):
        for x,y in np.ndindex(self.grid.shape):
            if self.grid[y][x] == 0:
                pygame.draw.rect(self.play_surface, BLACK, (x*25, y*25, 25, 25))
            elif self.grid[y][x] == 2:
                pygame.draw.rect(self.play_surface, MAGENTA, (x*25, y*25, 25, 25))
            elif self.grid[y][x] == 1:
                pygame.draw.rect(self.play_surface, RED, (x*25, y*25, 25, 25))

    def randomizing_fruit_cords(self):
        available_xy = []
        for x, y in np.ndindex(self.grid.shape):
            if x != 0 and x != ROWS and y != 0 and y != COLS:
                if self.grid[y,x] == 0:
                    available_xy.append([x,y])
        if len(available_xy) == 0:
            return False
        cords = random.choice(available_xy)
        return cords[0],cords[1]

    def compute_time(self, nanoseconds):
        seconds = int(int(nanoseconds)/1000000000)
        minutes = int(seconds/60)
        return minutes,seconds-(60*minutes)

    def reset(self, score):
        self.reset_board()
        if score > self.high_score:
            self.high_score = score
        del self.snake
        del self.fruit
        self.game_over = False
        self.last_4_actions = [0,0,0,0]
        self.play_surface.fill(BLACK)
        self.info_surface.fill(GRAY)
        self.snake = Snake(10, 10, 1)
        self.fruit = Fruit(self.randomizing_fruit_cords())
        self.fill_board()
        self.draw_board()
        self.fruit.draw_fruit(self.play_surface)
        timer = my_font.render("0",1,WHITE)
        length = my_font.render(str(self.snake.length),1,WHITE)
        self.info_surface.blit(timer,(140,30))
        self.info_surface.blit(length,(320,30))
        self.window.blit(self.play_surface, (0, 100))
        self.window.blit(self.info_surface, (0, 0))
        self.time_to_subtract = time.perf_counter_ns()
        pygame.display.update()

    def calculate_fruit_distance_reward(self):
        reward = 9
        fruit_x, fruit_y = self.fruit.x, self.fruit.y
        snake_x, snake_y = self.snake.body[0][0], self.snake.body[0][1]
        distance_x = abs(fruit_x-snake_x)
        distance_y = abs(fruit_y-snake_y)
        distance = math.sqrt(pow(distance_x,2) + pow(distance_y,2))
        return int((reward - distance)/3)

    def play_step(self,turn):
        self.reset_board()
        self.last_4_actions.pop()
        self.last_4_actions.insert(0,turn)
        for event in pygame.event.get(): #keep the env running
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        self.prev_body = self.snake.body.copy()
        self.snake.move(turn)
        self.fill_board()
        self.info_surface.fill(GRAY)
        self.play_surface.fill(BLACK)
        self.fruit.draw_fruit(self.play_surface)
        self.draw_board()
        time_to_display = time.perf_counter_ns() - self.time_to_subtract
        time_to_display = "%s:%s" % self.compute_time(time_to_display)
        timer = my_font.render(time_to_display,1,WHITE)
        length = my_font.render(str(self.snake.length),1,WHITE)
        self.info_surface.blit(timer,(140,30)) #board y,x instead of x,y
        self.info_surface.blit(length,(320,30))
        self.window.blit(self.play_surface, (0, 100))
        self.window.blit(self.info_surface, (0, 0))
        pygame.display.update()

        if self.snake.check_collision_fruit(self.fruit):
            del self.fruit
            self.snake.grow(self.prev_body[-1])
            new_fruit_cords = self.randomizing_fruit_cords()
            if new_fruit_cords == False:
                self.game_over = True
                self.fruit = Fruit((20,20))
            else:
                self.fruit = Fruit(new_fruit_cords)
                return 15, False, int(self.snake.length)
        else:
            if self.snake.check_wall_collision(self.grid):
                self.game_over = True
            if self.snake.check_collision_body():
                self.game_over = True
            if self.game_over == True:
                score = self.snake.length
                self.reset(score)
                return -20, True, int(score)
        reward = self.calculate_fruit_distance_reward()
        if self.last_4_actions == [1,1,1,1] or self.last_4_actions == [2,2,2,2]:
            reward = -120
            self.game_over = True
            return reward, True, int(self.snake.length)
        return reward, False, int(self.snake.length)

if __name__ == "__main__":
    env = Environement()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    env.play_step(2)
                if event.key == pygame.K_s:
                    env.play_step(0)
                if event.key == pygame.K_a:
                    env.play_step(1)
            if event.type == pygame.QUIT:
                sys.exit()