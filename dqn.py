import gymnasium as gym
from gym.wrappers import FlattenObservation
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import random
from boardenv import BoardEnv
from collections import deque

# Define the neural network for the DQN
class DQN(nn.Module):
    def __init__(self, state_size, action_size):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(state_size, 24)
        self.fc2 = nn.Linear(24, 24)
        self.fc3 = nn.Linear(24, action_size)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)

# Hyperparameters
EPISODES = 40000
GAMMA = 0.95
LEARNING_RATE = 0.001
MEMORY_SIZE = 40000
BATCH_SIZE = 64
EPSILON = 1.0
EPSILON_DECAY = 0.9998
EPSILON_MIN = 0.001

# Initialize environment and DQN
env = BoardEnv()
state_size = env.observation_space.shape[0]
action_size = env.action_space.n
dqn = DQN(state_size, action_size)
optimizer = optim.Adam(dqn.parameters(), lr=LEARNING_RATE)
criterion = nn.MSELoss()
memory = deque(maxlen=MEMORY_SIZE)

# Function to choose an action
def choose_action(state, epsilon):
    legal_actions_mask = np.zeros(action_size)
    legal_actions = env.board.legalColumns()
    legal_actions_mask[legal_actions] = 1

    if np.random.rand() <= epsilon:
        # Choose a random legal action
        legal_actions = np.where(legal_actions_mask == 1)[0]
        return np.random.choice(legal_actions)
    
    state = torch.FloatTensor(state).unsqueeze(0)
    with torch.no_grad():
        q_values = dqn(state)
    
    # Mask illegal actions by setting their Q-values to a very low number
    q_values = q_values.numpy()
    q_values[0][legal_actions_mask == 0] = -np.inf
    
    return np.argmax(q_values)

# Function to replay memory and train the network
def replay():
    if len(memory) < BATCH_SIZE:
        return
    minibatch = random.sample(memory, BATCH_SIZE)
    for state, action, reward, next_state, done in minibatch:
        target = reward
        if not done:
            next_state = torch.FloatTensor(next_state).unsqueeze(0)
            target = reward + GAMMA * torch.max(dqn(next_state)).item()
        state = np.array(state)
        state = torch.FloatTensor(state).unsqueeze(0)
        target_f = dqn(state)
        target_f[0][action] = target
        optimizer.zero_grad()
        loss = criterion(dqn(state), target_f)
        loss.backward()
        optimizer.step()

if __name__ == "__main__":
    # Training loop
    for e in range(EPISODES):
        state, _ = env.reset()
        done = False
        total_reward = 0
        while not done:
            action = choose_action(state, EPSILON)
            next_state, reward, done, _, _ = env.step(action)
            memory.append((state, action, reward, next_state, done))
            state = next_state
            total_reward += reward
            if done:
                print(f"Episode: {e+1}/{EPISODES}, Score: {total_reward}, Epsilon: {EPSILON:.2}")
                break
        replay()
        if EPSILON > EPSILON_MIN:
            EPSILON *= EPSILON_DECAY

    torch.save(dqn.state_dict(), "flinky.model")
    print("Model saved as flinky.model")