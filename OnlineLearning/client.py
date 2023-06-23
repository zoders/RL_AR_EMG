import numpy as np
import socket
from emggameenvironment import EmgGameEnvironment
from agent import Agent
import json

# хост AR-устройства
HOST_AR = "192.168.235.29"
PORT_AR = 1234


def send_to_ar(message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_ar:
        s_ar.connect((HOST_AR, PORT_AR))
        s_ar.send(bytes(message.encode()))
        s_ar.close()


TRANSPORT_BLOCK_HEADER_SIZE = 16
SAMPLES_PER_TRANSPORT_BLOCK = 64
TCP_PACKET_SIZE = (TRANSPORT_BLOCK_HEADER_SIZE // 4 + SAMPLES_PER_TRANSPORT_BLOCK) * 4
a = np.zeros(6)
samp = np.zeros(2000)
k = 0.0000228
temp = np.zeros(2000)
dataframes = 0
data = bytearray(2048)
samples = np.array([])

coe = np.loadtxt('filter.txt')
# хост и порт ЭМГ-устройства
HOST = '192.168.235.91'
PORT = 3000


def get_codes(info):
    if info['axis_goal_x'] < 0 and (info['goal_x'] < 0 and info['goal_y'] > 0):
        return 'a'
    if info['axis_goal_x'] > 0 and (info['goal_x'] > 0 and info['goal_y'] > 0):
        return 'b'
    if info['axis_goal_x'] < 0 and (info['goal_x'] < 0 and info['goal_y'] < 0):
        return 'c'
    if info['axis_goal_x'] > 0 and (info['goal_x'] > 0 and info['goal_y'] < 0):
        return 'd'


agent = Agent(epsilon=1.0, batch_size=32, epochs_per_replay=30, state_shape=2000, log=True)
env = EmgGameEnvironment(gamemode='two_moves_corner', field_size=5, log=True, enable_field=True)
env.reset()
send_to_ar(get_codes(env.game.get_current_info()))
# создаем сокет
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # устанавливаем соединение с сервером
    s.connect((HOST, PORT))
    while True:
        # читаем данные
        data = s.recv(272)
        # если данные не получены, завершаем цикл
        if not data:
            break
        for sample in range(16, 272, 4):
            ins = np.array([int.from_bytes(data[sample:sample + 4], byteorder='little', signed=True)])
            samples = np.append(samples, ins)
            if len(samples) == 2001:
                samples = np.delete(samples, 0)
        if len(samples) == 2000:
            for i in range(2000):
                temp[i] = samples[i]
            mean = np.mean(samples)
            temp -= mean
            temp *= k
            temp = np.convolve(temp, coe, "same")
            maxid = np.argmax(temp)
            if 10000 >= temp[maxid] >= 0.1:
                if 968 <= maxid <= 1032:
                    for i in range(2000):
                        samp[i] = temp[i]
                    signal = temp
                    action = agent.act(signal)
                    print(action)
                    q = env.step(action)
                    if str(action) == env.get_expected_action():
                        send_to_ar(str(action))
                    else:
                        send_to_ar('p')
                    agent.remember(state=signal, action=float(0), reward=float(q[0]))
                    agent.remember(state=signal, action=float(1), reward=float(q[1]))
                    agent.replay()
                    if env.penalty <= -5 or env.score == 1.0:
                        env.reset()
                        send_to_ar(get_codes(env.game.get_current_info()))
        dataframes += 1
s.close()
