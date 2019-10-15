import random
import numpy as np
import json

cards = None
with open('cards.json') as f:
    cards = json.load(f)

class Rules:
    @staticmethod
    def get_all_games():
        return {
            'solo': 1,
            'wenz': 0
        }

    @staticmethod
    def calc_round_winner(game_round):
        first_card = game_round.played_cards[0]
        highest_card = first_card
        winner = 0
        card_ordering = Rules.get_card_ordering(game_round.game.game_type)
        color_ordering = Rules.get_color_ordering()
        for i in range(1, len(game_round.played_cards)):
            # trump vs no trump, wenz Jd vs Ad
            if not highest_card.is_trump and game_round.played_cards[i].is_trump:
                highest_card = game_round.played_cards[i]
                winner = i
                continue
            # same color and higher, eg Ac vs 10c
            if first_card.color == game_round.played_cards[i].color and \
                card_ordering.index(game_round.played_cards[i].value) > card_ordering.index(highest_card.value):
                highest_card = game_round.played_cards[i]
                winner = i
                continue
            # if cards are both trump but one is higher, eg. solo Q vs J
            if highest_card.is_trump and game_round.played_cards[i].is_trump and \
                card_ordering.index(game_round.played_cards[i].value) > card_ordering.index(highest_card.value):
                highest_card = game_round.played_cards[i]
                winner = i
                continue
            # if cards are the same value and trump, check color ordering, eg wenz Jc vs Jd
            if highest_card.is_trump and game_round.played_cards[i].is_trump and \
                game_round.played_cards[i].value == highest_card.value and \
                color_ordering.index(game_round.played_cards[i].color) > color_ordering.index(highest_card.color):
                highest_card = game_round.played_cards[i]
                winner = i
                continue
        # move from nth card played to correct played based on relative position
        return (winner + game_round.starting_position) % game_round.game.match.num_players

    @staticmethod
    def calc_game_winner(game):
        win_counts = {}
        for player in game.match.players:
            win_counts[player.position] = 0
        for game_round in game.game_rounds:
            win_counts[game_round.winner] += 1
        print(win_counts)
        winner = list(win_counts.keys())[np.argmax(list(win_counts.values()))]
        return winner

    @staticmethod
    def get_possible_games(game):
        return {
            'solo', 'wenz'
        }

    @staticmethod
    def get_color_ordering():
        return ['d', 'h', 's', 'c']

    @staticmethod
    def get_card_ordering(game_type):
        if game_type['game'] == 'wenz':
            return ['9', 'Q', 'K', '10', 'A', 'J']
        if game_type['game'] == 'solo':
            return ['9', 'K', '10', 'A', 'J', 'Q']

    @staticmethod
    def is_card_trump(card, game_type):
        if game_type['game'] == 'wenz':
            # only J are trump
            return card.value == 'J'
        if game_type['game'] == 'solo':
            # all Q, J and color are trump
            return card.value == 'Q' or card.value == 'J' or card.color == game_type['color']

    @staticmethod
    def _is_card_playable(card, game_type, played_cards, player_cards):
        # played_cards should never be empty here, if it is just fail!
        first_card = played_cards[0]
        if first_card.is_trump:
            if card.is_trump:
                return True
            else:
                # playable if he does not have any other trump card
                return len(list(filter(lambda c: c.is_trump, player_cards))) == 0
        else:
            # playable if card is no trump and has same color
            if not card.is_trump and card.color == first_card.color:
                return True
            else:
                # playable if he does not have any other card of same color that is not trump
                # acceptable would be if first_card = 'As' and player has 'Qs' in a solo.
                return len(list(filter(lambda c: c.color == first_card.color and not c.is_trump, player_cards))) == 0

    @staticmethod
    def set_playable_cards(game_round, end_of_round):
        for player in game_round.game.match.players:
            for card in player.cards:
                if end_of_round:
                    card.playable = True
                else:
                    card.playable = Rules._is_card_playable(card,
                        game_round.game.game_type,
                        game_round.played_cards,
                        player.cards)
