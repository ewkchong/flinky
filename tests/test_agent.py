import pytest
from agents import RandomAgent, GreedyAgent
from board import Board
from die import ChosenDie

class TestGreedyAgent:
    def test_basic(self):
        agent = GreedyAgent()
        board = Board(die=ChosenDie([1, 1, 2, 2]))

        # Turn 1
        board.makePlay(0)

        assert agent.decide(board) == 0
        board.makePlay(1)

        # Turn 2
        board.makePlay(2)

        assert agent.decide(board) == 2
