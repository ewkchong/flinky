from simulator import Simulator
from agents import RandomAgent

def main():
    sim = Simulator()
    a_wins, ties, b_wins = sim.multiProcessSimulate(RandomAgent(), RandomAgent(), 90000)

    print(f"Games simulated: {a_wins + ties + b_wins}")
    print(f"Results: A {a_wins} - {b_wins} B")
    print(f"A win rate: {"{:.2f}".format(a_wins / (a_wins + b_wins) * 100)}%")


if __name__ == "__main__":
    main()
