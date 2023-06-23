from collections import namedtuple, deque
import random
import itertools

Transition = namedtuple('Transition',
                        ('state', 'action', 'reward'))


class ReplayMemory(object):

    def __init__(self, capacity):
        self.memory = deque([], maxlen=capacity)
        self.capacity = capacity

    def push(self, *args):
        self.memory.append(Transition(*args))

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def last_sample(self, batch_size):
        return list(itertools.islice(
            self.memory, len(self.memory) - batch_size,
            len(self.memory)))

    def __len__(self):
        return len(self.memory)
