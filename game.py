import itertools
from base import GSSeries
def run_game(strats,n_games,game_size=2):
    return {tuple(c.name for c in combo): GSSeries(combo).run_series(n_games) for combo in itertools.combinations(strats, game_size)}


if __name__ == '__main__':
    from strategies import *
    strats = [RandomStrategy,CopyStrategy]
    data = run_game(strats,10)
    print(data)
