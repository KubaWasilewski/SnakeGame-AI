import torch
import random
from collections import deque
import numpy as np
from SnakeEnvironment import Environement
from model import Linear_QNet, QTrainer

MAX_MEMORY = 100000
BATCH_SIZE = 1000
LR = 0.005

# direction [straight,right,left]

class Agent:

    def __init__(self):
        self.number_of_games = 0
        self.epsilon = 0 # random evolution rate
        self.gamma = 0.8  # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # if sized exceeded pop left
        self.model = Linear_QNet(11,256,3) #left right straight
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self, game):
        #state = list((game.get_board()).flatten()/3)
        state = []
        state.append(int(game.get_direction_up()))
        state.append(int(game.get_direction_down()))
        state.append(int(game.get_direction_left()))
        state.append(int(game.get_direction_right()))
        state.append(int(game.get_food_below()))
        state.append(int(game.get_food_above()))
        state.append(int(game.get_food_left()))
        state.append(int(game.get_food_right()))
        state.append(int(game.get_obstacle_left()))
        state.append(int(game.get_obstacle_right()))
        state.append(int(game.get_obstacle_straight()))
        return np.array(state,dtype=float)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        self.epsilon = 220 - self.number_of_games
        final_move = [0,0,0]
        if random.randint(0, 500) < self.epsilon: #random moves
            move = random.randint(0,2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
        return final_move

def train():
    total_score = 0
    high_score = 0
    agent = Agent()
    game = Environement()
    while True:
        # get old state
        state_old = agent.get_state(game)

        # get next move
        final_move = agent.get_action(state_old)

        # perform move and get new state
        reward, done, score = game.play_step(final_move.index(1))
        state_new = agent.get_state(game)

        # train short memory 1 step
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # remember
        agent.remember(state_old, final_move, reward, state_new, done)
        if agent.number_of_games == 20:
            print(np.array_equal(state_new,state_old))
        if done:
            # train long memory (replay), plot result
            game.reset(score)
            agent.number_of_games += 1
            agent.train_long_memory()

            if score > high_score:
                high_score = score

            if agent.number_of_games == 1000: #save after 1k games
                agent.model.save()

            total_score += score
            print("Game", agent.number_of_games, "score", score, "high_score", high_score, "mean score", total_score/agent.number_of_games)

            # plot_scores.append(score)
            # total_score += score
            # mean_score = total_score / agent.number_of_games
            # plot_mean_scores.append(mean_score)
            # plot_save(plot_scores,plot_mean_scores)

if __name__ == "__main__":
    train()