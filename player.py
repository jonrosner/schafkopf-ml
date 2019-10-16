import random
import numpy as np
from rules import Rules

class Player:
    def __init__(self, position, is_human):
        self.position = position
        self.is_human = is_human
        self.cards = []
        self.game_points = 0
        self.coins = 10000

    def decide_on_game(self, game):
        game = ''
        possible_games = Rules.get_possible_games()
        if self.is_human:
            while game == '':
                console_input = input("What game do you want to play?")
                color = None
                if console_input == 'solo':
                    color = input("What color do you want to play?")
                try:
                    if console_input not in possible_games:
                        raise Exception()
                    game = {
                        "game": console_input,
                        "color": color,
                        "player_id": self.position
                    }
                except:
                    print("Please pick a valid game.")
        else:
            game = {
                "game": random.choice(Rules.get_possible_games()),
                "color": random.choice(Rules.get_color_ordering()),
                "player_id": self.position
            }
        return game

    def decide_on_card(self, round):
        card_index = -1
        playable_cards_indices = [i for i in range(len(self.cards)) if self.cards[i].playable]
        print("Playable cards:", playable_cards_indices)
        if self.is_human:
            while card_index == -1:
                console_input = input("What card index do you want to pick?")
                try:
                    console_int_input = int(console_input)
                    if console_int_input not in playable_cards_indices:
                        raise Exception()
                    card_index = console_int_input
                except:
                    print("Please pick a valid card.")
        else:
            card_index = random.choice(playable_cards_indices)
        picked_card = self.cards[card_index]
        self.cards.pop(card_index)
        return picked_card
