import unittest
from main import Board

class TestColumnScore(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(Board.getColumnScore([]), 0)

    def test_single(self):
        self.assertEqual(Board.getColumnScore([2]), 2)

    def test_mixed(self):
        self.assertEqual(Board.getColumnScore([2, 3, 4]), 9)

    def test_double_one(self):
        self.assertEqual(Board.getColumnScore([1, 1]), 4)

    def test_double_two(self):
        self.assertEqual(Board.getColumnScore([2, 2, 1]), 9)

    def test_double_five(self):
        self.assertEqual(Board.getColumnScore([5, 5, 3]), 23)

    def test_triple_one(self):
        self.assertEqual(Board.getColumnScore([1, 1, 1]), 9)

    def test_triple_three(self):
        self.assertEqual(Board.getColumnScore([3, 3, 3]), 27)

class TestLegalColumns(unittest.TestCase):
    def test_empty(self):
        board = Board()
        self.assertEqual(board.legalColumns(), [0, 1, 2])

    def test_secondTurn(self):
        board = Board()
        board.makePlay(0)  # player A goes
        # player B still has all columns available
        self.assertEqual(board.legalColumns(), [0, 1, 2])

    def test_fullColumn(self):
        board = Board()
        for _ in range(3):
            board.makePlay(0)  # player A plays column 0
            board.makePlay(1)  # player B plays column 1

        # turn 0: player A plays column 0
        # turn 1: player B plays column 0
        # turn 2: player A plays column 0
        # turn 3: player B plays column 0
        # turn 4: player A plays column 0
        # turn 5: player B plays column 0
        # After 6 turns, column 0 of player A is full
        self.assertEqual(board.legalColumns(), [1, 2])
        board.makePlay(1);

        # Ensure player B's column 1 is full
        self.assertEqual(board.legalColumns(), [0, 2])

class TestIsGameDone(unittest.TestCase):
    def test_empty(self):
        board = Board()
        self.assertFalse(board.isGameDone())

    def test_columnFull(self):
        board = Board()
        for _ in range(3):
            board.makePlay(0)
            board.makePlay(1)
        self.assertFalse(board.isGameDone())

    # TODO: mock die roll to test true

if __name__ == '__main__':
    unittest.main()
