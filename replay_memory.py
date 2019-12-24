import numpy as np

class Replay_memory:
    def __init__(self):
        # dimension: N x (X, y)
        self.memory = np.array([])

    def add(self, samples):
        self.memory = np.concatenate(self.memory, samples)