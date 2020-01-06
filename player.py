import random
import numpy as np
from rules import Rules
from utils import Utils

class Player:
    def __init__(self, position, is_human, rl_agent):
        self.position = position
        self.is_human = is_human
        self.cards = []
        self.game_points = 0
        self.coins = 10000
        self.rl_agent = rl_agent
        # is used to remember transition
        self.old_state = None

    def decide_on_game(self, game_obj):
        game = ''
        possible_games = Rules.get_possible_games()
        if self.is_human:
            while game == '':
                game_obj.log_msgs.append(str(self))
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
            features = Utils.features_from_game(game_obj, self)
            game_index = self.rl_agent.predict_game(features)
            self.rl_agent.update_game_memory(self.position, features, game_index)
        else:
            if self.rl_agent:
                features = Utils.features_from_game(game_obj, self)
                game_index = self.rl_agent.predict_game(features)
                if game_index == 0:
                    game_type = 'no_game'
                    color = None
                elif game_index == 1:
                    game_type = 'wenz'
                    color = None
                else:
                    # means its a solo, now determine color
                    color = Rules.get_color_ordering()[game_index - 2]
                    game_type = 'solo'
                self.rl_agent.update_game_memory(self.position, features, game_index)
            else:
                game_type = random.choice(Rules.get_possible_games())
                color = random.choice(Rules.get_color_ordering())
            game = {
                "game": game_type,
                "color": color,
                "player_id": self.position
            }
        return game

    def decide_on_card(self, game_round):
        card_index = -1
        playable_cards_indices = [i for i in range(len(self.cards)) if self.cards[i].playable]
        #print("Playable cards:", playable_cards_indices)
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
            features = Utils.features_from_round(game_round, self)
            if self.old_state:
                self.rl_agent.update_card_memory_with_next_state(self.position, features, False)
            self.old_state = features
            self.rl_agent.update_card_memory(self.position, features, card_index)
        else:
            if self.rl_agent:
                features = Utils.features_from_round(game_round, self)
                if self.old_state:
                    self.rl_agent.update_card_memory_with_next_state(self.position, features, False)
                self.old_state = features
                # every 10 rounds do not explore on cards but do on game
                explore = game_round.game.game_no % 10 != 0
                card_index = self.rl_agent.predict_action(features, playable_cards_indices, game_round.game.game_type["game"], explore)
                self.rl_agent.update_card_memory(self.position, features, card_index)
            else:
                # pick highest card and play it
                highest_index = playable_cards_indices[0]
                game = game_round.game.game_type
                for i in playable_cards_indices[1:]:
                    if Rules.get_card_ordering(game).index(self.cards[i].value) > Rules.get_card_ordering(game).index(self.cards[highest_index].value):
                        highest_index = i
                    elif (Rules.get_card_ordering(game).index(self.cards[i].value) == Rules.get_card_ordering(game).index(self.cards[highest_index].value) and Rules.get_color_ordering().index(self.cards[i].color) > Rules.get_color_ordering().index(self.cards[highest_index].color)):
                        highest_index = i
                card_index = highest_index
        picked_card = self.cards[card_index]
        self.cards.pop(card_index)
        return picked_card

    def __str__(self):
        cards_str = " ".join(list(map(str, self.cards)))
        return "[Player: {0}. Cards: {1}. Coins: {2}]".format(self.position, cards_str, self.coins)