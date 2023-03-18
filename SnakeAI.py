from SnakeEnvironment import Environement
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import time


class Linear_QNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.linear1 = nn.Linear(input_size,hidden_size)
        self.linear2 = nn.Linear(hidden_size,output_size)

    def forward(self, x):
        x = F.relu(self.linear1(x))
        x = self.linear2(x)
        return x

model = Linear_QNet(11,256,3)
model.load_state_dict(torch.load("model/model_11_256_3v2.pth"))
game = Environement()

def get_state(game):
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

def get_action(state,model):
    final_move = [0,0,0]
    state0 = torch.tensor(state, dtype=torch.float)
    prediction = model(state0)
    move = torch.argmax(prediction).item()
    final_move[move] = 1
    return final_move

def play():
    high_score = 0
    total_score = 0
    game_number = 0
    game = Environement()
    while True:
        state = get_state(game)
        final_move = get_action(state, model)
        r, done, score = game.play_step(final_move.index(1))
        time.sleep(0.1) #comment or remove that line for fastplay
        if done:
            game_number += 1
            total_score += score
            game.reset(score)
            if score > high_score:
                high_score = score
            print("High Score: ", high_score, "Mean Score: ", "%.2f" %(total_score/game_number), "Game Number: ", game_number)

if __name__ == "__main__":
    play()