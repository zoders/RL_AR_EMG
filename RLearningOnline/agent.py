from keras.optimizers import Adam
from custommodel import CustomModel
from replaymemory import ReplayMemory
import numpy as np


class Agent(object):
    def __init__(
            self,
            mem_size=2500,
            state_shape=2000,
            learning_rate=5e-5,
            batch_size=32,
            epochs_per_replay=30,
            epsilon=1.0,
            epsilon_decay=0.995,
            epsilon_min=0.0,
            action_size=2,
            log=False,
    ):
        self.memory = ReplayMemory(capacity=mem_size)
        self.q_net = self.create_custom_model(state_shape, learning_rate)
        self.batch_size = batch_size
        self.epochs_per_replay = epochs_per_replay
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        self.action_size = action_size
        self.log = log
        self.state_shape = state_shape

    @staticmethod
    def create_custom_model(state_shape, learning_rate):
        num_sensors = 1
        model = CustomModel(state_shape, num_sensors)
        model.compile(loss='mse', optimizer=Adam(learning_rate), run_eagerly=False)
        return model

    def act(self, state):
        actions = np.array([1., -1.])
        if np.random.rand() <= self.epsilon:
            if self.log:
                print('random move: ', end=' ')
            r = np.random.choice([-1, 1])
            return np.argmax(r * actions)
        actions[0] = self.q_net.predict(np.append(state, float(0)).reshape(1, self. state_shape + 1))
        actions[1] = self.q_net.predict(np.append(state, float(1)).reshape(1, self. state_shape + 1))
        if self.log:
            print('predicted move: ', end=' ')
        print('actions:', actions)
        return np.argmax(actions)

    def remember(self, state, action, reward):
        self.memory.push(state, action, reward)

    def replay(self):
        if len(self.memory) < self.batch_size:
            return

        print('starting replay...')
        minibatch = self.memory.last_sample(self.batch_size)
        states = [
            np.append(d.state, d.action)
            for d in minibatch
        ]
        states = np.array(states, dtype='float32')
        rewards = [np.array([d.reward]) for d in minibatch]
        rewards = np.array(rewards, dtype='float32')
        history = self.q_net.fit(states, rewards, epochs=self.epochs_per_replay, verbose=0,
                                 batch_size=self.batch_size)
        print(history.history['loss'][-1])
        print('replay stopped...')
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
        return history.history['loss'][-1]

    def load(self, name):
        self.q_net.load_weights(name)

    def save(self, name):
        self.q_net.save_weights(name)
