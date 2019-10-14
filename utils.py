from card import Card

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