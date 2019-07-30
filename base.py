import random
import itertools
import logging

class GSStrategy:
    name = ""
    # n is the number of moves in the game, usually 13
    def __init__(self, n):
        raise NotImplementedError

    def update_history(self, hist):
        raise NotImplementedError

    def get_move(self, new_card):
        raise NotImplementedError

    def reset(self):
        raise NotImplementedError

class GSPlayer:
    def __init__(self, game, strategy):
        self.strat = strategy
        self.name = strategy.name
        self.game = game
        self.legal_moves = list(range(self.game.n))
        self.score = 0

    def start_game(self):
        self.score = 0
        self.legal_moves = list(range(self.game.n))
        self.strat.reset()

    def update_score(self, v):
        self.score += v

    def update_history(self, data):
        self.strat.update_history(data)

    def get_bid(self, new_card):
        move = self.strat.get_move(new_card)
        try:
            self.legal_moves.remove(move)
        except ValueError:
            move = min(self.legal_moves)
            self.legal_moves.remove(move)
        return move

class GSSeries:
    def __init__(self, strat_cls_list, n=13):
        self.n = n
        self.players = [GSPlayer(self, strat(n)) for strat in strat_cls_list]
        self.game_data = []

    def game_step(self,card):
        plays = [pl.get_bid(card) for pl in self.players] # plays is a list of the moves
        winning = max(plays)
        winners = [i for i,pl in enumerate(plays) if pl == winning]
        pts = card/len(winners)
        for w in winners:
            self.players[w].update_score(pts)
        for idx,pl in enumerate(self.players):
            pl.update_history((card,plays[:idx]+plays[idx+1:],plays[idx]))
        return plays

    def run_game(self):
        for pl in self.players:
            pl.start_game()
        cards = list(range(self.n))
        random.shuffle(cards)
        plays = [self.game_step(card) for card in cards]
        self.game_data.append({'scores':{pl.name:pl.score for pl in self.players},'moves':{pl.name:[play[i] for play in plays] for i,pl in enumerate(self.players)}})

    def run_series(self,n_games):
        for _ in range(n_games):
            self.run_game()
        return self.game_data
        



