from game_round import Game_round
from rules import Rules

import random

class Game:
    def __init__(self,
        match,
        starting_position):
        self.match = match
        self.starting_position = starting_position
        self.game_type = None
        self.playing = True
        self.game_rounds = []
        self.winner = None
        self.deck = list(range(24))
        random.shuffle(self.deck)

    def start(self):
        print("New game. Starting position is {0}".format(self.starting_position))
        for i in range(self.match.num_players):
            current_position = (self.starting_position + i) % self.match.num_players
            player = self.match.players[current_position]
            player.cards = self.deck[i*6:i*6+6]
            game_type = player.decide_on_game(self)
            print("Player {0} is playing {1}".format(current_position, game_type))
            self.game_type = game_type

    def run(self):
        while self.playing:
            game_round = Game_round(
                self,
                self.starting_position
            )
            game_round.start()
            game_round.run()
            game_round.end()
            self.game_rounds.append(game_round)

    def end(self):
        self.winner = Rules.calc_game_winner(self)
        print("Player {0} won this game.".format(self.winner))
        self.match.current_starting_position = \
            (self.match.current_starting_position + 1) % self.match.num_players