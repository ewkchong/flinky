from gym import Env
from gym import spaces
from gym.spaces import Discrete, Box
import numpy as np
import random
from agents import GreedyAgent
from board import Board

class BoardEnv(Env):
    def __init__(self):
        # Action space is choice between 3 columns
        self.action_space = Discrete(3)

        # Observation space is 6x3 grid, each possibly containing a dice value
        # Observation space also contains currently rolled dice value and whose turn it is
        self.observation_space = Box(low=0, high=6, shape=(20,))

        self.board = Board()
        self.opponent = GreedyAgent()


    def _get_column_obs(self):
        max_length = 3
        padded_a_cols = [col + [0] * (max_length - len(col)) for col in self.board.a_cols]
        padded_b_cols = [col + [0] * (max_length - len(col)) for col in self.board.b_cols]

        obs = np.concatenate([
            np.array(padded_a_cols),
            np.array(padded_b_cols)
        ])

        return obs

    def _get_obs(self):
        roll = np.array([self.board.rolledNum])
        turn = np.array([self.board.turnNumber % 2])
        board = self._get_column_obs().flatten()
        return np.concatenate((roll, turn, board))

    def _get_info(self):
        return {
            "score": self.board.getPlayerScores()
        }

    def step(self, action):
        # Get reward
        # self.board.printBoardState()
        # reward = self.board.evaluateMove(action) * 0.4
        reward = 0

        # Apply action
        rolledNum = self.board.rolledNum
        self.board.makePlay(action)

        # print(f"Turn {self.board.turnNumber}: Agent played {rolledNum} in column {action + 1}")
        terminated = self.board.isGameDone()

        if not terminated:
            rolledNum = self.board.rolledNum
            self.opponent.play(self.board)
            # print(f"Turn {self.board.turnNumber}: Opponent plays {rolledNum}")
            # self.board.printBoardState()

        # Get observation and info
        observation = self._get_obs()
        info = self._get_info()

        terminated = self.board.isGameDone()

        if terminated:
            a_score, b_score = self.board.getPlayerScores()
            if a_score > b_score:
                reward = 1
            elif a_score < b_score:
                reward = -1
            else:
                reward = 0
            # self.board.printBoardState()

            # print(f"Game over! Player A: {a_score}, Player B: {b_score}")

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
