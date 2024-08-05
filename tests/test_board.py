import pytest
from board import Board
from die import DeterministicDie

class TestColumnScore:
    def test_empty(self):
        assert Board.getColumnScore([]) == 0

    def test_single(self):
        assert Board.getColumnScore([2]) == 2

    def test_mixed(self):
        assert Board.getColumnScore([2, 3, 4]) == 9

    def test_double_one(self):
        assert Board.getColumnScore([1, 1]) == 4

    def test_double_two(self):
        assert Board.getColumnScore([2, 2, 1]) == 9

    def test_double_five(self):
        assert Board.getColumnScore([5, 5, 3]) == 23

    def test_triple_one(self):
        assert Board.getColumnScore([1, 1, 1]) == 9

    def test_triple_three(self):
        assert Board.getColumnScore([3, 3, 3]) == 27

class TestLegalColumns:
    def test_empty(self):
        board = Board()
        assert board.legalColumns() == [0, 1, 2]

    def test_secondTurn(self):
        board = Board()
        board.makePlay(0)
        assert board.legalColumns() == [0, 1, 2]

    def test_fullColumn(self):
        board = Board()
        for _ in range(3):
            board.makePlay(0)  # player A plays column 0
            board.makePlay(1)  # player B plays column 1

        # Ensure player A's column 0 is full
        assert board.legalColumns() == [1, 2]
        board.makePlay(2)  # player B plays column 2

        # Ensure player B's column 1 is full
        assert board.legalColumns() == [0, 2]

class TestIsGameDone:
    def test_empty(self):
        board = Board()
        assert not board.isGameDone()

    def test_columnFull(self):
        board = Board()
        for _ in range(3):
            board.makePlay(0)
            board.makePlay(1)

        assert not board.isGameDone()

    def test_game_done(self):
        board = Board(die=DeterministicDie())
        for _ in range(6):
            board.makePlay(0)
            assert not board.isGameDone()
        for _ in range(6):
            board.makePlay(1)
            assert not board.isGameDone()
        for _ in range(4):
            board.makePlay(2)
            assert not board.isGameDone()

        board.makePlay(2)
        assert board.isGameDone()
