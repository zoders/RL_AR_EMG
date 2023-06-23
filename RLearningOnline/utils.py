import matplotlib.pyplot as plt
import os
import numpy as np
import random


def draw_game_field(size, pos_player=(0, 0), pos_axis_goal=(10, 0),  pos_goal=(10, 0)):
    plt.figure(figsize=(1, 1))
    fig, ax = plt.subplots()
    ax.set_xlim([-size - 1, size + 1])
    ax.set_ylim([-size - 1, size + 1])
    ax.set_aspect('equal', adjustable='box')
    ax.set_xticks(range(-size - 1, size + 2, 1))
    ax.set_yticks(range(-size - 1, size + 2, 1))
    ax.scatter(pos_player[0], pos_player[1], color='red')
    ax.scatter(pos_axis_goal[0], pos_axis_goal[1], color='yellow')
    ax.scatter(pos_goal[0], pos_goal[1], color='green')
    plt.grid(True)
    plt.show()
    plt.close()


def get_dist(pos_player=(0, 0), pos_goal=(10, 0)):
    # манхэттенское расстояние
    return abs(pos_player[0] - pos_goal[0]) + abs(pos_player[1] - pos_goal[1])
  

def get_reward(start_dist, dist):
    return 1 - dist / start_dist


def get_dataset(dataset_path="/content/emg_datasets/full_dataset"):
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


def reshape_state(state):
    state_reshaped = np.asarray(state, dtype=np.float64)
    state_reshaped = state_reshaped.reshape((1, state_reshaped.shape[0]))
    return state_reshaped