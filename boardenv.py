from gym import Env
from gym import spaces
from gym.spaces import Discrete, Box
import numpy as np
import random
from agents import GreedyAgent
from board import Board

class BoardEnv(Env):
    def __init(self):
        # Action space is choice between 3 columns
        self.action_space = Discrete(3)

        # Observation space is 6x3 grid, each possibly containing a dice value
        # Observation space also contains currently rolled dice value and whose turn it is
        self.observation_space = spaces.Dict(
            {
                "roll": Discrete(6, start=1),
                "turn": Discrete(2),
                "board": Box(low=0, high=6, shape=(3,6))
            }
        )

        self.board = Board()
        self.opponent = GreedyAgent()


    def _get_column_obs(self):
        return np.concatenate(
            np.array(self.board.a_cols),
            np.array(self.board.b_cols)
        )

    def _get_obs(self):
        return {
            "roll": self.board.rolledNum,
            "turn": self.board.turnNumber % 2,
            "board": self._get_column_obs()
        }


    def _get_info(self):
        return {
            "score": self.board.getPlayerScores()
        }

    def step(self, action):
        # Get reward
        reward = self.board.evaluateMove(action)

        # Apply action
        self.board.makePlay(action)
        terminated = self.board.isGameDone()

        if not terminated:
            self.opponent.play(self.board)

        # Get observation and info
        observation = self._get_obs()
        info = self._get_info()

        terminated = self.board.isGameDone()

        # return step information (observation, reward, done, info)
        return observation, reward, terminated, False, info

    def render(self):
        # get a visual representation of the current board state
        pass

    def reset(self, seed=None, options=None):
        # seeding self.np_random
        super().reset(seed=seed)

        # start with a fresh board
        self.board = Board()

        observation = self._get_obs()
        info = self._get_info()

        return observation, info
