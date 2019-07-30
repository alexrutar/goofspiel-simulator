import random
import itertools
import logging

class GSStrategy:
    name = ""
    def __init__(self, game_params):
        raise NotImplementedError

    def start_game(self):
        raise NotImplementedError

    def get_bid(self, step_value):
        raise NotImplementedError

    def update_history(self, hist):
        raise NotImplementedError

class GSPlayer:
    def __init__(self, game, strategy):
        self.strat = strategy
        self.name = strategy.name
        self.game = game
        self.legal_moves = list(range(self.game.n))
        self.score = 0

    def reset(self):
        self.score = 0
        self.legal_moves = list(range(self.game.n))
        self.strat.start_game()

    def update_score(self, v):
        self.score += v

    def update_history(self, data):
        self.strat.update_history(data)

    def make_move(self, new_card):
        move = self.strat.get_bid(new_card)
        try:
            self.legal_moves.remove(move)
        except ValueError:
            print(f"Warning: strategy {self.name} made invalid move.")
            move = min(self.legal_moves)
            self.legal_moves.remove(move)
        return move

class GSSeries:
    def __init__(self, strat_cls_list, n=13,horizon=1000):
        self.n = n
        self.player_names = tuple(strat.name for strat in strat_cls_list)
        self.players = {strat.name:GSPlayer(self, strat({'length':n,'players':self.player_names,'horizon':horizon})) for strat in strat_cls_list}
        self.series_data = SeriesData(tuple(self.players.keys()))
        self.horizon=horizon

    def game_step(self,card):
        bids = {pl.name:pl.make_move(card) for pl in self.players.values()} # bids is a dict of the moves
        winning = max(bids.values())
        winners = tuple(k for k,v in bids.items() if v == winning)
        pts = card/len(winners)
        for w in winners:
            self.players[w].update_score(pts)
        for pl in self.players.values():
            pl.update_history({'turn_value':card,'bids':bids})
        return bids

    def run_game(self):
        for pl in self.players.values():
            pl.reset()
        cards = list(range(self.n))
        random.shuffle(cards)
        plays = [self.game_step(card) for card in cards]
        self.series_data.add_game_data({'scores':{pl.name:pl.score for pl in self.players.values()},'cards':cards,'moves':{pl.name:[play[pl.name] for play in plays] for pl in self.players.values()}})

    def run_series(self):
        for _ in range(self.horizon):
            self.run_game()
        return self.series_data
        
class SeriesData:
    def __init__(self, name_tuple):
        self.names = name_tuple
        self.scores = {name:0 for name in self.names}
        self.points = {name:0 for name in self.names}
        self.series = []

    def __str__(self):
        return "\n".join(str(dat) for dat in self.series)

    def add_game_data(self, data):
        self.series.append(data)
        top_score = max(data['scores'].values())
        winners = [name for name in self.names if data['scores'][name] == top_score]
        for name in winners:
            self.points[name] += 1/len(winners)

        for name in self.names:
            self.scores[name] += data['scores'][name]

    def score(self, name):
        return self.scores[name]

    def report(self):
        return "\nGame with players: " + ", ".join(name for name in self.names) + "\n" \
                + "  Average scores: " + str({k:s/len(self.series) for k,s in self.scores.items()}) + "\n" \
                + "  Points: " + str(self.points)

