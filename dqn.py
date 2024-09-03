import numpy as np
from boardenv import BoardEnv
from keras import models, layers, optimizers

from rl.agents import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory

def build_model(states, actions):
    model = models.Sequential()
    model.add(layers.Dense(24, activation='relu', input_shape=states))
    model.add(layers.Dense(24, activation='relu'))
    model.add(layers.Dense(actions, activation='linear'))
    return model


def build_agent(model, actions):
    policy = BoltzmannQPolicy()
    memory = SequentialMemory(limit=50000, window_length=1)
    dqn = DQNAgent(model=model, memory=memory, policy=policy,
                  nb_actions=actions, nb_steps_warmup=10, target_model_update=1e-2)
    return dqn


env = BoardEnv()

states = env.observation_space.shape
actions = env.action_space.shape

my_model = build_model(states, actions)

dqn = build_agent(my_model, actions)
dqn.compile(optimizers.Adam(lr=1e-3), metrics=['mae'])
dqn.fit(env, nb_steps=50000, visualize=False, verbose=1)

scores = dqn.test(env, nb_episodes=100, visualize=False)
print(np.mean(scores.history['episode_reward']))

_ = dqn.test(env, nb_episodes=15, visualize=True)
