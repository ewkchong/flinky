from board import Board, Move
import random

class Agent:
    def play(self, b: Board) -> Move:
        rolledNum = b.rolledNum
        decision = self.decide(b)
        b.makePlay(decision)
        return (rolledNum, decision)

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
        max_idx = 0
        max_val = -1
        for col in b.legalColumns():
            val = b.evaluateMove(col)
            if val > max_val:
                max_val = val
                max_idx = col
        return max_idx
