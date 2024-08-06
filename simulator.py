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
    def simulateGame(a: Agent, b: Agent, a_first = True, verbose = False) -> GameResult:
        moves = []
        board = Board(die=RegularDie())
        if a_first:
            while not board.isGameDone():
                moves.append(a.play(board))
                if board.isGameDone():
                    break
                moves.append(b.play(board))
        else:
            while not board.isGameDone():
                moves.append(b.play(board))
                if board.isGameDone():
                    break
                moves.append(a.play(board))

        if verbose:
            board.printBoardState()
            a_score, b_score = board.getPlayerScores()
            print(f"Score: A {a_score} - {b_score} B")

        a_score, b_score = board.getPlayerScores()

        return { 'moves': moves, 'scores': (a_score, b_score) if a_first else (b_score, a_score) }

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


    def simpleSimulateNGames(self, a: Agent, b: Agent, n_games: int):
        a_wins = 0
        ties = 0
        score_diff = 0
        for i in range(n_games):
            # A should go first only half of the time
            if i % 2 == 0:
                a_first = True
            else:
                a_first = False
            result: GameResult = self.simulateGame(a, b, a_first)
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


    def simulateNGames(self, agent_a: Agent, agent_b: Agent, n_games: int) -> tuple[int, int, int]:
        n_cpu = multiprocessing.cpu_count()
        future_results = []
        divisions = [ n_games//n_cpu for _ in range(n_cpu) ]
        remainder = n_games - (divisions[0] * n_cpu)
        if remainder > 0:
            divisions[-1] += remainder

        with concurrent.futures.ProcessPoolExecutor(max_workers=n_cpu) as executor:
            futures = []
            for i in range(len(divisions)):
                futures.append(executor.submit(self.simpleSimulateNGames, a=agent_a, b=agent_b, n_games=divisions[i]))
            for future in concurrent.futures.as_completed(futures):
                future_results.append(future.result())

        return self.aggregateResults(future_results)
