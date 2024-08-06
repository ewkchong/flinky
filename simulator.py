from typing import List, TypedDict
from agents import Agent
from board import Board, Move
from die import RegularDie
from agents import RandomAgent
import concurrent.futures
import multiprocessing


class GameResult(TypedDict):
    moves: List[Move]
    scores: tuple[int, int]


class Simulator:
    def __init__(self):
        self.average_diff = 0
        self.results = (0, 0, 0) # (A wins, ties, B wins)
        self.a_win_rate = 0


    @staticmethod
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


    @staticmethod
    def aggregateResults(resultList: List[tuple[int, int, int]]) -> tuple[int, int, int]:
        a = 0
        b = 0
        c = 0
        for x, y, z in resultList:
            a += x
            b += y
            c += z
        return (a, b, c)


    def simulateNGames(self, a: Agent, b: Agent, n_games: int):
        a_wins = 0
        ties = 0
        score_diff = 0
        for _ in range(n_games):
            result: GameResult = self.simulateGame(a, b)
            a_score, b_score = result['scores']
            if a_score > b_score:
                score_diff += a_score - b_score
                a_wins += 1
            elif a_score == b_score:
                ties += 1
            else:
                score_diff += b_score - a_score
        non_tied_games = n_games - ties

        return (a_wins, ties, non_tied_games - a_wins)


    def multiProcessSimulate(self, a: Agent, b: Agent, n_games: int) -> tuple[int, int, int]:
        n_cpu = multiprocessing.cpu_count()
        future_results = []
        with concurrent.futures.ProcessPoolExecutor(max_workers=n_cpu) as executor:
            futures = []
            for _ in range(n_cpu):
                futures.append(executor.submit(self.simulateNGames, a=RandomAgent(), b=RandomAgent(), n_games=n_games//n_cpu))
            for future in concurrent.futures.as_completed(futures):
                future_results.append(future.result())

        return self.aggregateResults(future_results)
