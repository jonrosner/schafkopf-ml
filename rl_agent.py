from dqn import DQN
from game_network import Game_network
import numpy as np

class Rl_Agent:
    def __init__(self):
        self.game_network = Game_network()
        self.action_network = DQN()
        self.game_replay_memory = np.array([])
        self.epsilon = 0.1

    def predict_game(self, state, allowed_games_idxs):
        if np.random.uniform() > self.epsilon:
            predictions = self.game_network.predict(state)
            # TODO: probably shape problem here
            prediction = np.argmax(allowed_games_idxs[predictions[allowed_games_idxs]])
        else:
            prediction = allowed_games_idxs[np.random.choice(len(allowed_games_idxs))]
        return prediction

    def predict_action(self, state):
        self.action_network.predict(state)
        return 0

    def init_action_memory(self, num_players):
        self.game_memory = {}
        for i in range(num_players):
            self.game_memory[i] = []

    def update_action_memory(self, player_pos, state_n, action_n, state_n1):
        self.game_memory[player_pos].append([state_n, action_n, state_n1])

    def update_action_memory_with_reward(self, player_pos, reward):
        for mem in self.game_memory[player_pos]:
            mem.append(reward)

    def init_game_memory(self, num_players):
        self.game_memory = {}
        for i in range(num_players):
            self.game_memory[i] = {}

    def update_game_memory(self, player_pos, state, game):
        self.game_memory[player_pos] = {
            'state': state,
            'action': game
        }

    def update_game_memory_with_reward(self, player_pos, reward):
        self.game_memory[player_pos]['reward'] = reward
        # calc delta
        state = self.game_memory[player_pos]['state']
        action = self.game_memory[player_pos]['action']
        predicted_reward = self.game_network.predict(state)[0][action]
        self.game_memory[player_pos]['delta'] = (reward - predicted_reward)**2

    def flush_game_memory(self):
        for key in self.game_memory:
            self.game_replay_memory.append(self.game_memory[key])
            self.game_memory[key] = np.array([])

    def train_game_network(self):
        # do not train if replay memory is too small
        if len(self.game_replay_memory) < 32:
            return
        idxs = np.random.choice(len(self.game_replay_memory), size=32)
        samples = self.game_replay_memory[idxs]
        states = np.array([])
        actions = np.array([])
        rewards = np.array([])
        for transition in samples:
            states.append(transition['state'])
            actions.append(transition['action'])
            rewards.append(transition['reward'])
        self.game_network.train_step(X, y)