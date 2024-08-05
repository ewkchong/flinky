import random
from typing import List

class Die:
    def roll(self) -> int:
        return 1

class RegularDie(Die):
    def roll(self) -> int:
        return random.randint(1, 6)

class DeterministicDie(Die):
    def __init__(self):
        self.rollCount = 0

    def roll(self) -> int:
        mod = self.rollCount % 6
        self.rollCount += 1
        return mod + 1

class ChosenDie(Die):
    def __init__(self, rollSequence: List[int]):
        self.rollCount = 0
        if len(rollSequence) == 0:
            raise Exception("rollSequence cannot be empty")
        self.rollSequence = rollSequence

    def roll(self) -> int:
        """
        Rolls in sequence this die was initialized with
        """
        n = len(self.rollSequence)
        num = self.rollSequence[self.rollCount % n]
        self.rollCount += 1
        return num
