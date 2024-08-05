import random

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
        mod = self.rollCount % 3
        if mod == 0:
            num = 1
        elif mod == 1:
            num = 2
        else:
            num = 3
        self.rollCount += 1
        return num
