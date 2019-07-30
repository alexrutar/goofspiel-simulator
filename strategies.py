from base import GSStrategy
import random


class RandomStrategy(GSStrategy):
    name = "random"
    def __init__(self, n):
        self.n = n

    def update_history(self, hist):
        return

    def get_move(self, new_card):
        return self.valid_moves.pop()

    def reset(self):
        self.valid_moves = list(range(self.n))
        random.shuffle(self.valid_moves)

class CopyStrategy(GSStrategy):
    name = "copy"
    def __init__(self, n):
        return

    def update_history(self, hist):
        return

    def get_move(self, new_card):
        return new_card

    def reset(self):
        return
