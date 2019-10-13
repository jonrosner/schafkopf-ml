import random

from rules import Rules

class Player:
    def __init__(self, position, is_human):
        self.position = position
        self.is_human = is_human
        self.cards = []

    def decide_on_game(self, game):
        game = ''
        possible_games = Rules.get_possible_games(game)
        if self.is_human:
            while game == '':
                console_input = input("What game do you want to play?")
                try:
                    if console_input not in possible_games:
                        raise Exception()
                    game = console_input
                except:
                    print("Please pick a valid game.")
        else:
            game = random.randint(0, len(possible_games) - 1)
        return game

    def decide_on_card(self, round):
        card_index = -1
        if self.is_human:
            while card_index == -1:
                console_input = input("What card index do you want to pick?")
                try:
                    console_int_input = int(console_input)
                    if console_int_input >= len(self.cards):
                        raise Exception()
                    card_index = console_int_input
                except:
                    print("Please pick a valid card.")
        else:
            card_index = random.randint(0, len(self.cards) - 1)
        picked_card = self.cards[card_index]
        self.cards.pop(card_index)
        return picked_card