from simulator import Simulator
from agents import GreedyAgent, RandomAgent
import click

agents = {
    'greedy': GreedyAgent(),
    'random': RandomAgent()
}

@click.command()
@click.option("-n", default=50000, help="Number of games to simulate")
@click.option("-a",
                default="greedy",
                help="Agent A",
                type=click.Choice(list(agents.keys())))
@click.option("-b",
                default="greedy",
                help="Agent B",
                type=click.Choice(list(agents.keys())))
def simulate(n, a, b):
    sim = Simulator()
    agent_a = agents[a]
    agent_b = agents[b]
    a_wins, ties, b_wins = sim.simulateNGames(agent_a, agent_b, n_games=n)

    print(f"Results: A {a_wins} - {b_wins} B")
    print(f"A win rate: {'{:.2f}'.format(a_wins / (a_wins + b_wins) * 100)}%")

if __name__ == "__main__":
    simulate()
