import torch
import numpy as np
from boardenv import BoardEnv
from dqn import DQN

# Load the trained model
def load_model(model_path, state_size, action_size):
    model = DQN(state_size, action_size)
    model.load_state_dict(torch.load(model_path, weights_only=True))
    model.eval()
    return model

# Function to play a game using the DQN model
def play_game(model, env):
    state, _ = env.reset()
    done = False
    total_reward = 0

    while not done:
        state = torch.FloatTensor(state).unsqueeze(0)
        with torch.no_grad():
            q_values = model(state)

        legal_actions_mask = np.zeros(action_size)
        legal_actions = env.board.legalColumns()
        legal_actions_mask[legal_actions] = 1

        q_values = q_values.numpy()
        q_values[0][legal_actions_mask == 0] = -np.inf
        print(q_values)

        action = np.argmax(q_values)
        next_state, reward, done, _, _ = env.step(action)
        state = next_state
        total_reward += reward

    a_score, b_score = env.board.getPlayerScores()
    return total_reward, a_score, b_score

if __name__ == "__main__":
    # Initialize environment
    env = BoardEnv()
    state_size = env.observation_space.shape[0]
    action_size = env.action_space.n

    # Load the trained DQN model
    model_path = "flinky.model"
    model = load_model(model_path, state_size, action_size)

    a_wins = 0
    b_wins = 0
    ties = 0

    # Play 10000 games
    for i in range(1):
        total_reward, a_score, b_score = play_game(model, env)

        if (a_score == b_score):
            ties += 1
        elif (a_score > b_score):
            a_wins += 1
        else:
            b_wins += 1

    print(f"A wins: {a_wins}, B wins: {b_wins}, Ties: {ties}")
    print(f"A win rate: {'{:.2f}'.format(a_wins / (a_wins + b_wins) * 100)}%")