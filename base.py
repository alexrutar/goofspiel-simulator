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
    def __init__(self, strat_cls_list, n=13):
        self.n = n
        self.players = [GSPlayer(self, strat({'length':n,'n_players':len(strat_cls_list)})) for strat in strat_cls_list]
        self.series_data = SeriesData(tuple(pl.name for pl in self.players))

    def game_step(self,card):
        plays = [pl.make_move(card) for pl in self.players] # plays is a list of the moves
        winning = max(plays)
        winners = [i for i,pl in enumerate(plays) if pl == winning]
        pts = card/len(winners)
        for w in winners:
            self.players[w].update_score(pts)
        for idx,pl in enumerate(self.players):
            pl.update_history({'step_value':card,'other_bids':plays[:idx]+plays[idx+1:],'your_bid':plays[idx]})
        return plays

    def run_game(self):
        for pl in self.players:
            pl.reset()
        cards = list(range(self.n))
        random.shuffle(cards)
        plays = [self.game_step(card) for card in cards]
        self.series_data.add_game_data({'scores':{pl.name:pl.score for pl in self.players},'moves':{pl.name:[play[i] for play in plays] for i,pl in enumerate(self.players)}})

    def run_series(self,n_games):
        for _ in range(n_games):
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
                + "Average scores: " + str({k:s/len(self.series) for k,s in self.scores.items()}) + "\n" \
                + "Points: " + str(self.points)

