from dqn import DQN
import numpy as np

class Rl_Agent:
    def __init__(self):
        self.game_network = DQN(9, 6)
        self.wenz_network = DQN(36, 8)
        self.solo_network = DQN(37, 8)
        self.match = None
        self.game_memory = {}
        self.card_memory = {}
        self.explore = True

    def set_match(self, match):
        self.match = match
        self.game_network.set_match(match)
        self.wenz_network.set_match(match)
        self.solo_network.set_match(match)

    def predict_game(self, state):
        prediction = self.game_network.predict(state, [0,1,2,3,4,5], self.explore)
        return prediction

    def predict_action(self, state, allowed_idxs, game_type, explore):
        assert game_type in ['wenz', 'solo']
        if game_type == 'wenz':
            prediction = self.wenz_network.predict(state, allowed_idxs, explore)
        if game_type == 'solo':
            prediction = self.solo_network.predict(state, allowed_idxs, explore)
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
            self.game_network.remember(self.game_memory[key]['state'],
                self.game_memory[key]['action'],
                self.game_memory[key]['reward'],
                None,
                True
            )
            self.game_memory[key] = {}

    def update_card_memory(self, player_pos, state, action):
        try:
            self.card_memory[player_pos].append({
            'state': state,
            'action': action
        })
        except:
            self.card_memory[player_pos] =[{
            'state': state,
            'action': action
        }]

    def update_card_memory_with_reward(self, player_pos, reward):
        for i in range(len(self.card_memory[player_pos])):
            self.card_memory[player_pos][i]['reward'] = reward

    def update_card_memory_with_next_state(self, player_pos, state_2, done):
        self.card_memory[player_pos][-1]['state_2'] = state_2
        self.card_memory[player_pos][-1]['done'] = done

    def flush_card_memory(self, game_type):
        assert game_type in ['wenz', 'solo']
        for key in self.card_memory.keys():
                for d in self.card_memory[key]:
                    if game_type == 'wenz':
                        self.wenz_network.remember(
                            d['state'],
                            d['action'],
                            d['reward'],
                            d['state_2'],
                            d['done']
                        )
                    else:
                        self.solo_network.remember(
                            d['state'],
                            d['action'],
                            d['reward'],
                            d['state_2'],
                            d['done']
                        )
                    self.card_memory[key] = []

    def train_game_network(self):
        self.game_network.replay(32)

    def train_action_network(self, game_type):
        assert game_type in ['wenz', 'solo']
        if game_type == 'wenz':
            self.wenz_network.replay(32)
        else:
            self.solo_network.replay(32)

    def save_networks(self):
        print('SAVING NETWORK')
        self.game_network.save_checkpoint('game.h5df')
        self.wenz_network.save_checkpoint('wenz.h5df')
        self.solo_network.save_checkpoint('solo.h5df')
