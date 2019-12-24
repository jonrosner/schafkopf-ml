import tensorflow as tf
import numpy as np

class Game_network:
    def __init__(self):
        self.model = tf.keras.Sequential()
        self.model.add(tf.keras.layers.Dense(32))
        self.model.add(tf.keras.layers.Dense(3, activation='softmax'))
        self.model.compile(loss='mse', optimizer='sgd')

    def train_step(self, X, y):
        self.model.fit(X, y)

    def predict(self, state):
        prediction = self.model.predict(state)
        return prediction