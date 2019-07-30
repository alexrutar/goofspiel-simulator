from base import GSStrategy
import random


class RandomStrategy(GSStrategy):
    """Chooses a random valid bid each turn."""
    name = "random"
    def __init__(self, game_params):
        self.n = game_params['length']

    def start_game(self):
        self.valid_moves = list(range(self.n))
        random.shuffle(self.valid_moves)

    def get_bid(self, step_value):
        return self.valid_moves.pop()

    def update_history(self, hist):
        return

class CopyStrategy(GSStrategy):
    """Makes a bid equal to the value of the card."""
    name = "copy"
    def __init__(self, game_params):
        return

    def start_game(self):
        return

    def get_bid(self, step_value):
        return step_value

    def update_history(self, hist):
        return

class CopyP1Strategy(GSStrategy):
    """Makes a bid equal to one more than the value of the card."""
    name = "copy_plus_1"
    def __init__(self, game_params):
        self.n = game_params['length']
        return

    def start_game(self):
        return

    def get_bid(self, step_value):
        return (step_value + 1) % self.n

    def update_history(self, hist):
        return


class AntiPureStrategy(GSStrategy):
    """Creates an internal distribution map for the opponent's gameplay on the last round.
    This strategy assumes there is only 1 other player.
    Initial distribution assumes the opposing player will play exactly what the card is.

    Gameplay is optimal against any pure strategy.
    """
    name = "anti_pure"
    def __init__(self, game_params):
        self.n = game_params['length']
        self.n_players = game_params['n_players']
        assert self.n_players == 2
        self.opponent_map = {n:n for n in range(self.n)}

    def start_game(self):
        return

    def update_history(self, hist):
        # update the bids made by the opponent
        self.opponent_map[hist['step_value']] = hist['other_bids'][0]

    def get_bid(self, step_value):
        return (self.opponent_map[step_value] + 1) % self.n



