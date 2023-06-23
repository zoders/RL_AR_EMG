from emggameenvironment import EmgGameEnvironment
import os
import numpy as np
import random
from agent import Agent
import socket
import json
import time
import matplotlib.pyplot as plt


# хост AR-устройства
HOST_AR = "192.168.0.190"
PORT_AR = 1234


def send_to_ar(message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_ar:
        s_ar.connect((HOST_AR, PORT_AR))
        s_ar.send(bytes(message.encode()))
        s_ar.close()


def get_dataset(dataset_path="moves"):
    data = []
    labels = []
    muap_paths = []
    for folder in os.listdir(dataset_path):
        for muap_path in os.listdir("{}/{}".format(dataset_path, folder)):
            path = "{}/{}/{}".format(dataset_path, folder, muap_path)
            muap_paths.append(path)
    random.seed(42)
    random.shuffle(muap_paths)
    for muap_path in muap_paths:
        muap = np.loadtxt(muap_path)
        data.append(muap)
        label = muap_path.split(os.path.sep)[-2]
        labels.append(label)
    data = np.asarray(data, dtype=np.float32)
    labels = np.asarray(labels)
    return data, labels


class Signals(object):

    def __init__(self, signals, actions):
        self.signals = dict()
        self.actions_count = [-1, -1, -1, -1, ]
        s0 = []
        s1 = []
        s2 = []
        s3 = []
        for i in range(len(actions)):
            if actions[i] == '0':
                s0.append(signals[i])
            if actions[i] == '1':
                s1.append(signals[i])
            if actions[i] == '2':
                s2.append(signals[i])
            if actions[i] == '3':
                s3.append(signals[i])
        s0 = np.asarray(s0)
        s1 = np.asarray(s1)
        s2 = np.asarray(s2)
        s3 = np.asarray(s3)
        self.signals['0'] = s0
        self.signals['1'] = s1
        self.signals['2'] = s2
        self.signals['3'] = s3

    def get_signal(self, action):
        self.actions_count[int(action)] = self.actions_count[int(action)] + 1
        return self.signals[action][self.actions_count[int(action)]]


log = True
signals, actions = get_dataset("moves")

s = Signals(signals, actions)
agent = Agent(epsilon=1.0, batch_size=32, epochs_per_replay=30, state_shape=2000, log=True)
env = EmgGameEnvironment(gamemode='two_moves_corner', field_size=5, log=True, enable_field=True)


def get_codes(info):
    if info['axis_goal_x'] < 0 and (info['goal_x'] < 0 and info['goal_y'] > 0):
        return 'a'
    if info['axis_goal_x'] > 0 and (info['goal_x'] > 0 and info['goal_y'] > 0):
        return 'b'
    if info['axis_goal_x'] < 0 and (info['goal_x'] < 0 and info['goal_y'] < 0):
        return 'c'
    if info['axis_goal_x'] > 0 and (info['goal_x'] > 0 and info['goal_y'] < 0):
        return 'd'


env.reset()
# использовать только чтобы визуализировать симуляцию агента в режиме AR
# send_to_ar(get_codes(env.game.get_current_info()))
counter = 0

h = []
rewards = []
reward = 0
game_info = []
game = 0
while counter < 2000:
    time.sleep(0.5)
    print(f'iteration: {counter}')
    current_info = env.game.get_current_info()
    current_info['game'] = game
    game_info.append(current_info)
    exp_action = env.get_expected_action()
    signal = s.get_signal(exp_action)
    action = agent.act(signal)
    q = env.step(action)
    reward += q[int(action)]
    print('q', q)
    # if str(action) == env.get_expected_action():
    #     send_to_ar(str(action))
    # else:
    #     send_to_ar('p')
    agent.remember(state=signal, action=float(0), reward=float(q[0]))
    agent.remember(state=signal, action=float(1), reward=float(q[1]))
    h.append(agent.replay())
    if env.penalty <= -5 or env.score == 1.0:
        game += 1
        if env.score == 1.0:
            current_info = env.game.get_current_info()
            current_info['game'] = game
            game_info.append(current_info)
        env.reset()
        # send_to_ar(get_codes(env.game.get_current_info()))
        rewards.append(reward)
        reward = 0
        print(f'epsilon: {agent.epsilon}')
    counter += 1

rewards = np.asarray(rewards, dtype='int32')


plt.figure()
plt.title('потери')
plt.plot(h)
plt.show()
plt.figure()
plt.title('награды')
plt.plot(rewards)
np.savetxt('rewards.txt', rewards)
plt.show()
agent.save('model.h5')
import json

with open("game_info.json", "w") as json_file:
    json.dump(game_info, json_file)
