from collections import Counter
import random
from typing import List
from die import Die, RegularDie

Move = tuple[int, int]  # (rolledNumber, columnPlayed)

class Board:
    def __init__(self, die=Die()):
        self.a_cols = [[], [], []]
        self.b_cols = [[], [], []]
        self.die = die
        self.turnNumber = 0
        self.rolledNum = self.die.roll()
        self.winner = None

    def printBoardState(self) -> None:
        def constructRow(idx: int, colSet: List[List[int]]) -> str:
            row = [-1, -1, -1]
            for i, col in enumerate(colSet):
                if len(col) > idx:
                    row[i] = col[idx]
            row_str = list(map(lambda x: str(x) if x != -1 else " ", row))
            return f"| {row_str[0]} | {row_str[1]} | {row_str[2]} |"

        for i in range(3):
            print(constructRow(i, self.a_cols))
        print('-------------')
        for i in range(3):
            print(constructRow(i, self.b_cols))

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


    def getPlayerScores(self) -> tuple[int, int]:
        """
        Returns the current scores of the players in a tuple:
        (Player A's score, Player B's score)
        """
        a_score = 0
        b_score = 0
        for col in self.a_cols:
            a_score += self.getColumnScore(col)
        for col in self.b_cols:
            b_score += self.getColumnScore(col)
        return (a_score, b_score)

    def evaluateMove(self, colNum: int) -> int:
        """
        Returns the change in score difference that would result from playing in column col.
        Will only be called with legal columns
        """
        num = self.rolledNum
        a_col = self.a_cols[colNum].copy()
        b_col = self.b_cols[colNum].copy()
        a_score = self.getColumnScore(a_col)
        b_score = self.getColumnScore(b_col)
        if self.turnNumber % 2 == 0:
            # Add your number to the column
            a_col.append(num)
            # Destroy occurences on same number in opponents column
            b_col = list(filter(lambda x: x != num, b_col))

            new_a_score = self.getColumnScore(a_col)
            new_b_score = self.getColumnScore(b_col)
            return new_a_score - a_score - (new_b_score - b_score)
        else:
            # Player B
            b_col.append(num)
            a_col = list(filter(lambda x: x != num, a_col))

            new_a_score = self.getColumnScore(a_col)
            new_b_score = self.getColumnScore(b_col)
            return new_b_score - b_score - (new_a_score - a_score)
        return 0

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
        self.rolledNum = self.die.roll();


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
