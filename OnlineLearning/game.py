import random
from utils import (draw_game_field, get_dist, get_reward)
import numpy as np


class Game(object):
    player_x = 0
    player_y = 0
    axis_goal_x = 0
    axis_goal_y = 0
    axis_goal = False
    goal = False

    def __init__(self, size=1, enable_field=False, gamemode='random', ):
        self.goal_x = 0
        self.goal_y = 0
        self.size = size
        self.enable_field = enable_field
        if gamemode == 'random':
            while self.goal_x == 0 or self.goal_y == 0:
                self.goal_x = random.randint(-size, size)
                self.goal_y = random.randint(-size, size)
        if gamemode == 'corner':
            self.goal_x = size * random.choice([-1, 1])
            self.goal_y = size * random.choice([-1, 1])

        if random.choice([True, False]):
            self.axis_goal_x = self.goal_x
        else:
            self.axis_goal_y = self.goal_y
        if gamemode == 'axis':
            if random.choice([True, False]):
                self.goal_x = 0
                self.goal_y = size * random.choice([-1, 1])
            else:
                self.goal_x = size * random.choice([-1, 1])
                self.goal_y = 0
            self.axis_goal_x = self.goal_x
            self.axis_goal_y = self.goal_y

        if gamemode == 'x_axis':
            self.goal_x = size * random.choice([-1, 1])
            self.axis_goal_x = self.goal_x
            self.goal_y = 0
            self.axis_goal_y = 0

        self.__two_moves_mode = False
        if gamemode == 'two_moves_corner':
            self.__two_moves_mode = True
            self.axis_goal_x = size * random.choice([-1, 1])
            self.axis_goal_y = 0
            self.goal_x = self.axis_goal_x
            self.goal_y = size * random.choice([-1, 1])

        self.start_dist = get_dist((self.player_x, self.player_y), (self.goal_x, self.goal_y))
        self.step_reward = 1 / self.start_dist
        if enable_field:
            draw_game_field(self.size, (self.player_x, self.player_y), (self.axis_goal_x, self.axis_goal_y),
                            (self.goal_x, self.goal_y))
        self.score = 0

    def check_goals(self):
        if self.player_x == self.axis_goal_x and self.player_y == self.axis_goal_y:
            self.axis_goal = True
        if self.player_x == self.goal_x and self.player_y == self.goal_y:
            self.goal = True

    def up(self):
        self.player_y += 1

    def down(self):
        self.player_y -= 1

    def left(self):
        self.player_x -= 1

    def right(self):
        self.player_x += 1

    def __get_move(self):
        if not self.axis_goal:
            if self.player_x != self.axis_goal_x:
                if self.player_x > self.axis_goal_x:
                    return 'left'
                elif self.player_x < self.axis_goal_x:
                    return 'right'
            if self.player_y != self.axis_goal_y:
                if self.player_y < self.axis_goal_y:
                    return 'up'
                elif self.player_y > self.axis_goal_y:
                    return 'down'
        if self.axis_goal and not self.goal:
            if self.player_x != self.goal_x:
                if self.player_x > self.goal_x:
                    return 'left'
                elif self.player_x < self.goal_x:
                    return 'right'
            if self.player_y != self.goal_y:
                if self.player_y < self.goal_y:
                    return 'up'
                elif self.player_y > self.goal_y:
                    return 'down'
        return 'finish'

    def get_expected_move(self):
        if self.__two_moves_mode and self.axis_goal:
            if self.__get_move() == 'up':
                if self.goal_x >= 0:
                    return 'left'
                else:
                    return 'right'
            if self.__get_move() == 'down':
                if self.goal_x >= 0:
                    return 'right'
                else:
                    return 'left'
        return self.__get_move()

    def move(self):
        if self.__get_move() == 'left':
            self.left()
        if self.__get_move() == 'right':
            self.right()
        if self.__get_move() == 'up':
            self.up()
        if self.__get_move() == 'down':
            self.down()
        self.check_goals()
        if self.enable_field:
            draw_game_field(self.size, (self.player_x, self.player_y), (self.axis_goal_x, self.axis_goal_y),
                            (self.goal_x, self.goal_y))
        self.score = get_reward(self.start_dist, get_dist((self.player_x, self.player_y), (self.goal_x, self.goal_y)))

    def get_current_info(self, to_np_array=False):

        current_info = {
            'player_x': self.player_x,
            'player_y': self.player_y,
            'axis_goal_x': self.axis_goal_x,
            'axis_goal_y': self.axis_goal_y,
            'goal_x': self.goal_x,
            'goal_y': self.goal_y,
            'start_dist': self.start_dist,
            'dist_to_goal': get_dist((self.player_x, self.player_y), (self.goal_x, self.goal_y)),
            'score': self.score,
        }
        if to_np_array:
            return np.asarray(list(current_info.values()), dtype='float32')
        else:
            return current_info
