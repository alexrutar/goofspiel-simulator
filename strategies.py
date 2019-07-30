from base import GSStrategy
import random


class RandomStrategy(GSStrategy):
    name = "random"
    def __init__(self, n):
        self.n = n

    def start_game(self):
        self.valid_moves = list(range(self.n))
        random.shuffle(self.valid_moves)

    def get_bid(self, step_value):
        return self.valid_moves.pop()

    def update_history(self, hist):
        return

class CopyStrategy(GSStrategy):
    name = "copy"
    def __init__(self, n):
        return

    def start_game(self):
        return

    def get_bid(self, step_value):
        return step_value

    def update_history(self, hist):
        return
