from game import Game


class EmgGameEnvironment(object):
    def __init__(self, field_size=5, gamemode='random', log=False, enable_field=False):
        self.game = None
        self.field_size = field_size
        self.gamemode = gamemode
        self.penalty = 0
        self.current_action = None
        self.log = log
        self.score = 0
        self.enable_field = enable_field

    def get_expected_action(self):
        expected_move = self.game.get_expected_move()
        if expected_move == 'left':
            return '0'
        if expected_move == 'right':
            return '1'
        if expected_move == 'up':
            return '2'
        if expected_move == 'down':
            return '3'
        return expected_move

    def reset(self):
        # сброс окружения к начальному состоянию
        self.penalty = 0
        self.score = 0
        print("... n e w   g a m e ...")
        if self.game:
            del self.game
        self.game = Game(enable_field=self.enable_field, size=self.field_size, gamemode=self.gamemode)
        self.current_action = self.get_expected_action()

    def step(self, action):
        actions = [1, 1]
        print("score", self.score)
        if self.log:
            print(f'(action: {action}, actual_move: {self.current_action})')
        if str(action) != str(self.current_action):
            self.penalty -= 1
            actions[int(action)] = -1
        else:
            for i in range(len(actions)):
                if i != int(action):
                    actions[i] = -1
            self.game.move()
            self.score = self.game.score

        self.current_action = self.get_expected_action()
        if self.log:
            if self.score == 1.0:
                print('completed')
        return actions
