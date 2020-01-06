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
        self.played_cards = []
        self.skip = False
        self.log_msgs = []

    def start(self):
        self.log_msgs.append("New game {0}. Starting position is {1}".format(self.game_no, self.starting_position))
        for i in range(self.match.num_players):
            if self.game_no % 30 == 0:
                self.match.rl_agent.explore = False
            else:
                self.match.rl_agent.explore = True
            self.match.players[i].game_points = 0
            current_position = (self.starting_position + i) % self.match.num_players
            player = self.match.players[current_position]
            cards_per_player = len(self.deck) // self.match.num_players
            player.cards = self.deck[i*cards_per_player:i*cards_per_player+cards_per_player]
            game_type = player.decide_on_game(self)
            self.log_msgs.append("Player {0} wants to play {1}".format(current_position, game_type))
            self.games_called.append(game_type)
        self.game_type = Rules.calc_highest_game(self.games_called)
        if self.game_type["game"] == "no_game":
            self.skip = True
        else:
            self.log_msgs.append("We play: {0}".format(self.game_type))
        for player in self.match.players:
            for card in player.cards:
                card.is_trump = Rules.is_card_trump(card, self.game_type)
            Rules.order_cards(player.cards, self)
            self.log_msgs.append("Player: {0}".format(str(player)))

    def run(self):
        while self.playing and not self.skip:
            game_round = Game_round(
                self,
                self.starting_position
            )
            game_round.start()
            game_round.run()
            game_round.end()
            self.game_rounds.append(game_round)

    def end(self):
        if self.skip:
            return
        self.winners = Rules.calc_game_winner(self)
        if len(self.winners) == 1 and self.match.rl_agent.explore == False:
            self.log_msgs.append("WINNER WINNER")
        self.payout = Rules.calc_game_payout(self)
        #print("Points: ", list(map(lambda player: player.game_points, self.match.players)))
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
        self.log_msgs.append("Player(s) {0} won this game. Rewards: {1}".format(list(map(lambda player: player.position, self.winners)), rewards))
        for i, reward in enumerate(rewards):
            # Update game memory and card memory with reward - 8.0 is number of cards
            per_card_reward = reward / 8.0
            self.match.rl_agent.update_game_memory_with_reward(self.match.players[i].position, reward)
            self.match.rl_agent.update_card_memory_with_next_state(self.match.players[i].position, None, True)
            self.match.rl_agent.update_card_memory_with_reward(self.match.players[i].position, per_card_reward)
            self.match.players[i].old_state = None
        self.match.rl_agent.flush_card_memory(self.game_type["game"])
        self.match.rl_agent.flush_game_memory()
        self.match.current_starting_position = \
            (self.match.current_starting_position + 1) % self.match.num_players
        self.match.rl_agent.train_game_network()
        # only print logs if caller won the game
        if len(self.winners) == 1:
            print("\n".join(self.log_msgs))
