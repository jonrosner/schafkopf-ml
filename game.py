from game_round import Game_round
from rules import Rules
from utils import Utils

import random

class Game:
    def __init__(self,
        match,
        starting_position):
        self.match = match
        self.starting_position = starting_position
        self.games_called = []
        self.game_type = None
        self.playing = True
        self.game_rounds = []
        self.winner = None
        self.deck = Utils.create_new_deck()

    def start(self):
        print("New game. Starting position is {0}".format(self.starting_position))
        for i in range(self.match.num_players):
            current_position = (self.starting_position + i) % self.match.num_players
            player = self.match.players[current_position]
            cards_per_player = len(self.deck) // self.match.num_players
            player.cards = self.deck[i*cards_per_player:i*cards_per_player+cards_per_player]
            game_type = player.decide_on_game(self)
            print("Player {0} wants to play {1}".format(current_position, game_type))
            self.games_called.append(game_type)
        self.game_type = Rules.calc_highest_game(self.games_called)
        print("We play:", self.game_type)
        self.starting_position = self.game_type["player_id"]
        for player in self.match.players:
            for card in player.cards:
                card.is_trump = Rules.is_card_trump(card, self.game_type)

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
        self.payout = Rules.calc_game_payout(self)
        self.match.players[self.winner].coins += self.payout
        print("Player {0} won this game.".format(self.winner))
        self.match.current_starting_position = \
            (self.match.current_starting_position + 1) % self.match.num_players