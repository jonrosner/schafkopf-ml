from card import Card
from rules import Rules

import json
import random

cards = None
with open('cards.json') as f:
    cards = json.load(f)

class Utils:
    @staticmethod
    def create_new_deck():
        deck = []
        for card in cards:
            c = Card(card['id'], card['value'], card['color'])
            deck.append(c)
        random.shuffle(deck)
        return deck

    @staticmethod
    def print_players_information(players):
        for player in players:
            cards_str = " ".join(list(map(str, player.cards)))
            print("Player {0}:\n\tCards: {1}".format(player.position, cards_str))

    @staticmethod
    def features_from_game(game, player):
        # 1-8 cards
        # 9 position
        features = [0] * 9
        cards = Rules.get_cards()
        for i in range(8):
            features[i] = [j for j,card in enumerate(cards) if card["id"] == player.cards[i].id][0]
        features[8] = (player.position - game.starting_position) % game.match.num_players
        return features


    @staticmethod
    def features_from_round(game_round, player):
        # 1-8 cards (-1 for None)
        # 9-10 played cards (-1 for None)
        # 11 position
        features = [0] * 11
        cards = Rules.get_cards()
        for i in range(8):
            try:
                features[i] = [j for j,card in enumerate(cards) if card["id"] == player.cards[i].id][0]
            except:
                features[i] = -1
        for i in range(8, 10):
            try:
                features[i] = [j for j,card in enumerate(cards) if card["id"] == game_round.played_cards[i-8].id][0]
            except:
                features[i] = -1
        # relative position in round
        features[10] = (player.position - game_round.starting_position) % game_round.game.match.num_players
        return features

    @staticmethod
    def get_game_from_index(game_index):
        return ("solo", "heart")