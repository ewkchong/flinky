from collections import Counter
from typing import List
import random

Move = tuple[int, int]  # (rolledNumber, columnPlayed)

# defines board state
class Board:
    def __init__(self):
        self.a_cols = [[], [], []]
        self.b_cols = [[], [], []]
        self.turnNumber = 0
        self.rolledNum = 0

    def rollDie(self) -> int:
        return random.randint(1, 6)

    @staticmethod
    def getColumnScore(col: List[int]) -> int:
        """
        Assumes col is a list of integers of length 0-3.
        Returns the score of a column: the score are added up, but
        die of the same type are multiplied.
        """
        score = 0
        ctr = Counter(col)
        for elem, cnt in ctr.items():
            if cnt == 1:
                score += elem
            elif cnt == 2:
                score += 4 * elem
            else:
                score += 9 * elem
        return score

    def makePlay(self, colNum: int) -> None:
        """
        plays the currently rolled die in given column index.
        assumes column has been validated already (i.e. not full)
        modifies board state.
        """
        num = self.rolledNum
        if self.turnNumber % 2 == 0:
            # Add your number to the column
            self.a_cols[colNum].append(num)
            # Destroy occurences on same number in opponents column
            self.b_cols[colNum] = list(filter(lambda x: x != num, self.b_cols[colNum]))
        else:
            self.b_cols[colNum].append(num)
            self.a_cols[colNum] = list(filter(lambda x: x != num, self.a_cols[colNum]))
        self.turnNumber += 1
        self.rolledNum = self.rollDie()

    def isGameDone(self) -> bool:
        if self.turnNumber % 2 == 0:
            total_len = sum([len(col) for col in self.b_cols])
            if total_len == 9:
                return True
        else:
            total_len = sum([len(col) for col in self.a_cols])
            if total_len == 9:
                return True

        return False

    def legalColumns(self) -> List[int]:
        """
        Returns a list of legal columns to play in.
        Depends on turn
        """
        legalCols = []
        if self.turnNumber % 2 == 0:
            for i in range(3):
                if len(self.a_cols[i]) < 3:
                    legalCols.append(i)
        else:
            for i in range(3):
                if len(self.b_cols[i]) < 3:
                    legalCols.append(i)
        return legalCols

class Agent:
    def play(self, b: Board) -> None:
        # TODO: implement agent play
        pass


def simulateGame(a: Agent, b: Agent) -> List[Move]:
    # TODO: implement game simulation
    return []


def main():
    board = Board()


if __name__ == "__main__":
    main()
