from game_round import Game_round
from rules import Rules
from utils import Utils

import random

class Game:
    def __init__(self,
        match,
        starting_position,
        game_no):
        self.match = match
        self.starting_position = starting_position
        self.games_called = []
        self.game_type = None
        self.playing = True
        self.game_rounds = []
        self.winners = []
        self.deck = Utils.create_new_deck()
        self.game_no = game_no

    def start(self):
        print("New game {0}. Starting position is {1}".format(self.game_no, self.starting_position))
        playable_games_idxs = [0,1,2]
        for i in range(self.match.num_players):
            if self.game_no % 100 == 0:
                self.match.rl_agent.explore = False
            else:
                self.match.rl_agent.explore = True
            self.match.players[i].game_points = 0
            current_position = (self.starting_position + i) % self.match.num_players
            player = self.match.players[current_position]
            cards_per_player = len(self.deck) // self.match.num_players
            player.cards = self.deck[i*cards_per_player:i*cards_per_player+cards_per_player]
            print("Player: {0}".format(str(player)))
            game_type = player.decide_on_game(self, playable_games_idxs)
            if game_type['game'] == 'wenz':
                playable_games_idxs = [0,2]
            if game_type['game'] == 'solo':
                playable_games_idxs = [0]
            print("Player {0} wants to play {1}".format(current_position, game_type))
            self.games_called.append(game_type)
        self.game_type = Rules.calc_highest_game(self.games_called)
        print("We play:", self.game_type)
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
        self.winners = Rules.calc_game_winner(self)
        self.payout = Rules.calc_game_payout(self)
        #print("Points: ", list(map(lambda player: player.game_points, self.match.players)))
        print("Player(s) {0} won this game.".format(list(map(lambda player: player.position, self.winners))))
        old_coins = list(map(lambda player: player.coins, self.match.players))
        for player in self.match.players:
            if player in self.winners:
                continue
            for winning_player in self.winners:
                #TODO: this will not work with callgame!!
                player.coins -= self.payout
                winning_player.coins += self.payout
        new_coins = list(map(lambda player: player.coins, self.match.players))
        rewards = [x[0] - x[1] for x in zip(new_coins, old_coins)]
        for i, reward in enumerate(rewards):
            # TODO: position is probably wrong here
            self.match.rl_agent.update_game_memory_with_reward(self.match.players[i].position, reward)
        for player in self.match.players:
            self.match.rl_agent.update_card_memory_with_next_state(player.position, None, True)
            game_number = Rules.get_possible_games().index(self.game_type['game'])
            self.match.rl_agent.flush_card_memory(game_number, player.position)
            player.old_state = None
        self.match.rl_agent.flush_game_memory()
        self.match.current_starting_position = \
            (self.match.current_starting_position + 1) % self.match.num_players
        self.match.rl_agent.train_game_network()
        if self.game_no % 10000 == 0:
            self.match.rl_agent.save_networks()
