import random
import numpy as np
import json

cards = None
with open('cards.json') as f:
    cards = json.load(f)

class Rules:
    @staticmethod
    def get_cards():
        return cards

    @staticmethod
    def calc_highest_game(games_called):
        ordering = Rules.get_possible_games()
        highest_game = games_called[0]
        for game in games_called:
            if ordering.index(game["game"]) > ordering.index(highest_game["game"]):
                highest_game = game
        return highest_game

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
    def calc_round_points(game_round):
        points = 0
        points_map = Rules.get_points_map()
        for card in game_round.played_cards:
            points += points_map[card.value]
        return points

    @staticmethod
    def calc_game_winner(game):
        if game.game_type['game'] != 'no_game':
            player_index = game.game_type['player_id']
            playing_points = game.match.players[player_index].game_points
            if playing_points > 60:
                return [game.match.players[player_index]]
            else:
                return [game.match.players[i] for i in range(game.match.num_players) if i != player_index]
        else:
            loser = game.match.players[0]
            for player in game.match.players:
                # schwarz spielen gewinnt ramsch
                #if player.game_points == 120:
                #    return [player]
                if player.game_points > loser.game_points:
                    loser = player
            return [game.match.players[i] for i in range(game.match.num_players) if i != loser.position]

    @staticmethod # the amount all losing players have to pay to winning players
    def calc_game_payout(game):
        payout_map = {
            "solo": 20,
            "wenz": 10,
            "no_game": 10,
            "black_factor": 2,
            "schneider": 10,
            "per_running": 10,
            "per_virgin_factor": 2
        }
        payout = 0
        payout += payout_map[game.game_type['game']]
        running_cards = Rules.get_running_cards(game.game_type['game'])
        winning_cards = [item for sublist in list(map(lambda player: player.cards, game.winners)) for item in sublist]
        winning_cards_ids = list(map(lambda card: card.id, winning_cards))
        runnings = 0
        for card_id in running_cards:
            if card_id in winning_cards_ids:
                runnings += 1
        payout += runnings * payout_map["per_running"]
        winning_game_points = sum(list(map(lambda player: player.game_points, game.winners)))
        if winning_game_points == 120:
            payout *= payout_map["black_factor"]
        elif winning_game_points  > 90 \
            or winning_game_points < 30:
            payout += payout_map["schneider"]
        if game.game_type["game"] == "no_game":
            virgins = 0
            for player in game.match.players:
                if player.game_points == 0:
                    virgins += 1
            if virgins == game.match.num_players - 1:
                payout = 100
            else:
                payout *= (virgins + 1)
        return payout

    @staticmethod
    def get_running_cards(game_type):
        if game_type == 'wenz':
            return ['Jc', 'Js', 'Jh', 'Jd']
        if game_type == 'solo' or game_type == 'no_game':
            return ['Qc', 'Qs', 'Qh', 'Qd', 'Jc', 'Js', 'Jh', 'Jd']
    @staticmethod
    def get_points_map():
        return {
            '9': 0,
            'J': 2,
            'Q': 3,
            'K': 4,
            '10': 10,
            'A': 11
        }

    @staticmethod
    def get_possible_games():
        return ['no_game', 'wenz', 'solo']

    @staticmethod
    def get_color_ordering():
        return ['d', 'h', 's', 'c']

    @staticmethod
    def get_card_ordering(game_type):
        if game_type['game'] == 'wenz':
            return ['9', 'Q', 'K', '10', 'A', 'J']
        if game_type['game'] == 'solo' or game_type['game'] == 'no_game':
            return ['9', 'K', '10', 'A', 'J', 'Q']

    @staticmethod
    def is_card_trump(card, game_type):
        if game_type['game'] == 'wenz':
            # only J are trump
            return card.value == 'J'
        if game_type['game'] == 'solo':
            # all Q, J and color are trump
            return card.value == 'Q' or card.value == 'J' or card.color == game_type['color']
        if game_type['game'] == 'no_game':
            # all Q, J and heart are trump
            return card.value == 'Q' or card.value == 'J' or card.color == 'h'

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
