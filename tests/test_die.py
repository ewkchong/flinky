import pytest

from board import Board
from die import DeterministicDie

class TestDie:
    def test_roll(self):
        board = Board(die=DeterministicDie())
        board.makePlay(0)
        board.makePlay(1)
        board.makePlay(2)
        assert board.a_cols == [[1], [], [3]]
        assert board.b_cols == [[], [2], []]
