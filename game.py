import itertools
from base import GSSeries


def run_game(strats,n_games,game_size=2):
    return [GSSeries(combo).run_series(n_games) for combo in itertools.combinations(strats, game_size)]


if __name__ == '__main__':
    from strategies import *
    strats = [RandomStrategy,CopyStrategy,CopyP1Strategy,AntiDetStrategy]
    data = run_game(strats,1000)
    for v in data:
        print(v.report())
