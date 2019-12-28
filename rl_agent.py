from dqn import DQN
import numpy as np

class Rl_Agent:
    def __init__(self):
        self.game_network = DQN(9, 3)
        self.action_networks = [DQN(11, 8) for i in range(3)]
        self.dqn = None
        self.game_memory = {}
        self.card_memory = {}

    def predict_game(self, state, allowed_games_idxs):
        prediction = self.game_network.predict(state, allowed_games_idxs)
        return prediction

    def predict_action(self, state, allowed_idxs, game_no):
        prediction = self.action_networks[game_no].predict(state, allowed_idxs)
        return prediction

    def update_game_memory(self, player_pos, state, game):
        self.game_memory[player_pos] = {
            'state': state,
            'action': game
        }

    def update_game_memory_with_reward(self, player_pos, reward):
        self.game_memory[player_pos]['reward'] = reward

    def flush_game_memory(self):
        for key in self.game_memory:
            print(key, self.game_memory[key])
            self.game_network.remember(self.game_memory[key]['state'],
                self.game_memory[key]['action'],
                self.game_memory[key]['reward'],
                None,
                True
            )
            self.game_memory[key] = {}

    def update_card_memory(self, player_pos, state, action):
        self.card_memory[player_pos] = {
            'state': state,
            'action': action
        }

    def update_card_memory_with_reward(self, player_pos, reward):
        self.card_memory[player_pos]['reward'] = reward

    def update_card_memory_with_next_state(self, player_pos, state_2, done):
        self.card_memory[player_pos]['state_2'] = state_2
        self.card_memory[player_pos]['done'] = done

    def flush_card_memory(self, game_no, player_position):
        self.action_networks[game_no].remember(
                self.card_memory[player_position]['state'],
                self.card_memory[player_position]['action'],
                self.card_memory[player_position]['reward'],
                self.card_memory[player_position]['state_2'],
                self.card_memory[player_position]['done']
            )

    def train_game_network(self):
        self.game_network.replay(32)

    def train_action_network(self, game_no):
        self.action_networks[game_no].replay(32)

    def save_networks(self):
        print('SAVING NETWORK')
        self.game_network.save_checkpoint('game.h5df')
