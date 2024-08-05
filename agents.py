from board import Board
import random

class Agent:
    def play(self, b: Board) -> None:
        # TODO: implement agent play
        pass

    def decide(self, b: Board) -> int:
        """
        Assumes it is the agent's turn.
        """
        return 0;


class RandomAgent(Agent):
    def decide(self, b: Board) -> int:
        return random.choice(b.legalColumns())


class GreedyAgent(Agent):
    def decide(self, b: Board) -> int:
        # TODO: implement greedy strategy
        return random.choice(b.legalColumns())
