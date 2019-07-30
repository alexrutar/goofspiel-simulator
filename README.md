# Goofspiel Simulator
This program is a simulator for the game Goofspiel.
The rules of this implementation are as follows.
A horizon `n` is fixed at the beginning of the game.
At each step of the game, a random integer from the list `[0,1,...,n-1]` is removed from the list and revealed to the players.
Then each player simultaneously makes a closed bid from the `[0,1,...,n-1]`, which must be distinct from all previous bids that they have made.
The players who have made the highest bid share the integer value of the game equally.
This proceeds until there the list is empty.

One can find a description of the card game on the [Wikipedia page for Goofspiel](https://en.wikipedia.org/wiki/Goofspiel#Game_play).

## Goofspiel Strategies
In this implementation, strategies are rules which are implemented as below.
For each pair of strategies, a series of `n` games are played, where `n` is an unknown horizon (but usually set to 100).
Strategies are allowed to maintain state between games of a series, but a new instance will be created for every series.

Any strategy class should be a subclass of the model below:
~~~python
class GSStrategy:
    name = ""
    def __init__(self, game_length):
        raise NotImplementedError

    def start_game(self):
        raise NotImplementedError

    def get_bid(self, step_value):
        raise NotImplementedError

    def update_history(self, hist):
        raise NotImplementedError
~~~
- `name` is a string which works as an identifier for the strategy.
- `__init__` is called at the beginning of the series, and the parameter `game_length` describes how many moves there are in a given game (usually 13).
- `start_game` is called at the beginning of each game, to initialize parameters etc.
- At the beginning of each step of the game, `get_bid` is called, where `step_value` is the integer revealed for that step (i.e. the number of points that turn is worth).
  This function must return a valid integer bid (distinct from all other bids made earlier during the game).
  If the bid is not valid, the game will automatically return the smallest possible bid.
- After every step of the game, `update_history` is called with `hist=(card,other_bids,your_bid)` and `card` is the integer value of the card just played, `other_plays` is a list of the bids that the other players made last turn, and `your_bid` is the bid that you made last turn.
  Note that if the bid made by `get_bid` is invalid, `your_bid` may be different than the return value of `get_bid`.

Other helper methods may be implemented, but the class is not allowed to maintain global state other than `name`.
See the `strategies.py` file for example strategies.
