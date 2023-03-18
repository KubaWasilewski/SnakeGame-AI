# SnakeGame + AI
Classic snake game with score, high score, time tracking. Exe file does not require python to be installed on the machine.
Algorithmic artificial inteligence, snake follows hamiltonian cycle, which prevents it from dying but does not collect food/apples
in an optimal manner.
Snake AI, is an implementation of reinforcment learning, using a deep Q neural network. Deep Q alghorithm assings a Q score to each action
at a given state. The neural network takes an input (state of the game) and choses the best action based on the Q scores. The current neural networks
consists of 11 input neurons as the game state: direction_up, direction_down, direction_left, direction_right - these are boolean values that determine
the direction of the sanke, food_below, food_above, food_left, food_right - these are boolean values that determine the absolute (x,y) position of the 
fruit on the board compared to the snake position (x,y), obstacle_turn_left, obstacle_turn_right, obstacle_straight - these are boolean values that
determine if the snake will hit an obstacle (wall or body) if he turns left, right or goes straight. Then there is a hidden layer of 256 neurons, and
an output layer of 3 neurons, which represent 3 actions: go straight, turn left, turn right.
The neural network achieves a high score of 58, mean score of 30 over 250 games.
<br />
files:
Snake.exe - executable file for the snake game (does not require python installed), run to play the game w,a,s,d <br />
Snake.py - python file for the snake game, run to play the game w,a,s,d <br />
SnakeAlgorithmAI - snake algorithm following hamiltonian cycle (guaranteed win), run to see the AI play <br />
SnakeAI - snake game played by a neural network mentioned in the description, run to see the AI play <br />
SnakeEnviroment.py - snake game enviorment for the neural network (Environment class), run to interact with environment <br />
agent.py - snake agent learns and trains neural network (Agent class), run to train model <br />
model.py - neural network model (Linear_QNet class) <br />
