from collections import Counter
from board import Board
from typing import List
import random
from agents import *

Move = tuple[int, int]  # (rolledNumber, columnPlayed)

def simulateGame(a: Agent, b: Agent) -> List[Move]:
    # TODO: implement game simulation
    return []


def main():
    board = Board()
    board.makePlay(0)
    board.makePlay(1)
    board.makePlay(2)
    board.makePlay(0)
    board.makePlay(1)
    board.makePlay(2)
    board.makePlay(0)
    board.makePlay(1)
    board.makePlay(2)
    board.printBoardState();

if __name__ == "__main__":
    main()
