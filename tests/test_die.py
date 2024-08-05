import pytest

from board import Board
from die import ChosenDie, DeterministicDie

class TestDie:
    def test_roll(self):
        die = DeterministicDie()
        assert die.roll() == 1
        assert die.roll() == 2
        assert die.roll() == 3
        assert die.roll() == 4
        assert die.roll() == 5
        assert die.roll() == 6

    def test_chosen_roll(self):
        die = ChosenDie([1, 1, 2, 2, 3, 3])
        assert die.roll() == 1
        assert die.roll() == 1
        assert die.roll() == 2
        assert die.roll() == 2
        assert die.roll() == 3
        assert die.roll() == 3
        assert die.roll() == 1
        assert die.roll() == 1
