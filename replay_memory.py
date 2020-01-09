from sumtree import SumTree
import random

"""
The Memory that is used for Prioritized Experience Replay
"""
class Replay_Memory:
    def __init__(self):
        self.memory_len = 10000
        self.memory_bias = .01
        self.memory_pow = .6
        self.tree = SumTree(self.memory_len)

    def add(self, error, sample):
        priority = (error + self.memory_bias) ** self.memory_pow
        self.tree.add(priority, sample)

    def sample(self, batch_size):
        """
         Get a sample batch of the replay memory
        Returns:
         batch: a batch with one sample from each segment of the memory
        """
        batch = []
        #we want one representative of all distribution-segments in the batch
        #e.g BATCH_SIZE=2: batch contains one sample from [min,median]
        #and from [median,max]
        segment = self.tree.total() / batch_size
        for i in range(batch_size):
            minimum = segment * i
            maximum = segment * (i+1)
            s = random.uniform(minimum, maximum)
            (idx, _, data) = self.tree.get(s)
            batch.append((idx, data))
        return batch

    def update(self, idx, error):
        """
         Updates one entry in the replay memory
        Args:
         idx: the position of the outdated transition in the memory
         error: the newly calculated error
        """
        priority = (error + self.memory_bias) ** self.memory_pow
        self.tree.update(idx, priority)