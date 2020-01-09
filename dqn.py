import tensorflow as tf
import random
import numpy as np

from replay_memory import Replay_Memory
from collections import deque

# Deep Q-learning Agent
class DQN:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=10000)
        self.gamma = 0.99    # discount rate
        self.epsilon = 0.1  # exploration rate
        self.epsilon_min = 0.01
        self.learning_rate = 0.00025
        self.model = self._build_model()
        self.debug_i = 1
        # only a debug reference
        self.match = None

    def set_match(self, match):
        self.match = match

    def _build_model(self):
        # Neural Net for Deep-Q learning Model
        model = tf.keras.Sequential()
        model.add(tf.keras.layers.Dense(64, input_dim=self.state_size, activation='relu'))
        model.add(tf.keras.layers.Dense(32, activation='relu'))
        model.add(tf.keras.layers.Dense(self.action_size, activation='linear'))
        model.compile(loss='mse',
                      optimizer=tf.keras.optimizers.SGD(lr=self.learning_rate))
        return model

    def save_checkpoint(self, filename):
        self.model.save(filename)

    def remember(self, state, action, reward, state_2, done):
        self.memory.append((state, action, reward, state_2, done))


    def predict(self, state, allowed_idxs, explore):
        if explore and np.random.rand() <= self.epsilon:
            self.match.game.log_msgs.append("RANDOM")
            if len(state) == 9:
                self.match.game.random_game = True
            return allowed_idxs[np.random.choice(len(allowed_idxs))]
        act_values = self.model.predict(np.array([state]))
        self.match.game.log_msgs.append("{0}".format(act_values))
        return allowed_idxs[np.argmax(act_values[0][allowed_idxs])]

    def replay(self, batch_size):
        if len(self.memory) < batch_size: return
        minibatch = random.sample(self.memory, batch_size)
        states = []
        target_fs = []
        for state, action, reward, state_2, done in minibatch:
            target = reward
            if not done:
                q_max = np.amax(self.model.predict(np.array([state_2]))[0])
                target = reward + self.gamma * q_max
            target_f = self.model.predict(np.array([state]))
            target_f[0][action] = target
            target_fs.append(target_f.flatten().tolist())
            states.append(state)
        self.model.fit(np.array(states), np.array(target_fs), epochs=1, verbose=0)
