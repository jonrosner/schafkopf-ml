import random
import numpy as np

class Rules:
    @staticmethod
    def get_all_games():
        return {
            'solo': 1,
            'wenz': 0
        }

    @staticmethod
    def calc_round_winner(game_round):
        winner = (np.argmax(game_round.played_cards) + game_round.starting_position) % \
            game_round.game.match.num_players
        return winner

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