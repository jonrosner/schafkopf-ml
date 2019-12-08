from dqn import DQN
import numpy as np

class Rl_Agent:
    def __init__(self):
        self.dqn = DQN()
        pass

    def predict_game(self, state):
        self.dqn.predict(state)
        return 5

    def predict_action(self, state):
        self.dqn.predict(state)
        return 0

    def init_game_memory(self, num_players):
        self.game_memory = {}
        for i in range(num_players):
            self.game_memory[i] = []

    def update_game_memory(self, player_pos, state_n, action_n, state_n1):
        self.game_memory[player_pos].append([state_n, action_n, state_n1])

    def update_game_memory_with_reward(self, player_pos, reward):
        for mem in self.game_memory[player_pos]:
            mem.append(reward)

    def flush_game_memory(self):
        pass