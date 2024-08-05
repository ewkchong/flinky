from collections import Counter
from board import Board, Move
from die import RegularDie
from typing import List, TypedDict
import random
from agents import *

class GameResult(TypedDict):
    moves: List[Move]
    scores: tuple[int, int]

def simulateGame(a: Agent, b: Agent, verbose = False) -> GameResult:
    moves = []
    board = Board(die=RegularDie())
    while not board.isGameDone():
        moves.append(a.play(board))
        if board.isGameDone():
            break
        moves.append(b.play(board))
    if verbose:
        board.printBoardState()
        a_score, b_score = board.getPlayerScores()
        print(f"Score: A {a_score} - {b_score} B")
    return { 'moves': moves, 'scores': board.getPlayerScores() }


def main():
    n_games = 50000
    a_wins = 0
    ties = 0
    for _ in range(n_games):
        result: GameResult = simulateGame(RandomAgent(), RandomAgent())
        a_score, b_score = result['scores']
        if a_score > b_score:
            a_wins += 1
        elif a_score == b_score:
            ties += 1
    non_tied_games = n_games - ties

    print(f"Results: A {a_wins} - {non_tied_games - a_wins} B")
    print(f"A's Win Rate: {a_wins / non_tied_games * 100}%")

if __name__ == "__main__":
    main()
