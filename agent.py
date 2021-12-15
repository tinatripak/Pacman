import torch
import skimage
import random
import numpy as np
from collections import deque
from ai import LinearQNet, QTrainer
from main import agent

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001
n_games = 0
epsilon = 0
gamma = 0.9
memory = deque(maxlen=MAX_MEMORY)
model = LinearQNet(840, 300, 4)
trainer = QTrainer(model, lr=LR, gamma=gamma)


def remember(state, action, reward, next_state, done):
    memory.append((state, action, reward, next_state, done))


def train_long_memory():
    if len(memory) > BATCH_SIZE:
        mini_sample = random.sample(memory, BATCH_SIZE)
    else:
        mini_sample = memory

    states, actions, rewards, next_states, dones = zip(*mini_sample)
    trainer.train_step(states, actions, rewards, next_states, dones)


def train_short_memory(state, action, reward, next_state, done):
    trainer.train_step(state, action, reward, next_state, done)


def get_action(state):
    epsilon = 150 - n_games
    final_move = [0, 0, 0, 0]
    if random.randint(0, 400) < epsilon:
        move = random.randint(0, 3)
        final_move[move] = 1
    else:
        state0 = torch.tensor(state, dtype=torch.float)
        prediction = model(state0)
        move = torch.argmax(prediction).item()
        final_move[move] = 1

    return final_move

def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    game = SnakeGameAI()
    while True:
        # get old state
        state_old = agent.get_state(game)

        # get move
        final_move = agent.get_action(state_old)

        # perform move and get new state
        reward, done, score = game.play_step(final_move)
        state_new = agent.get_state(game)

        # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # remember
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            # train long memory, plot result
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()

            print('Game', agent.n_games, 'Score', score, 'Record:', record)

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)
