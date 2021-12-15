import pygame
from ai import DQN

dqn_params = {
    "width": 21,
    "height": 18,
    "num_training": 10000,

    # Model backups
    'load_file': None,
    'save_file': None,

    # Training parameters
    'train_start': 3000,    # Episodes before training starts
    'batch_size': 32,       # Replay memory batch size
    'mem_size': 100000,     # Replay memory size

    'discount': 0.95,       # Discount rate (gamma value)
    'lr': .0002,            # Learning reate

    # Epsilon value (epsilon-greedy)
    'eps': 1.0,             # Epsilon start value
    'eps_final': 0.1,       # Epsilon end value
    'eps_step': 10000       # Epsilon steps between start and end (linear)
}

qnet = DQN(dqn_params)


class Player(pygame.sprite.Sprite):
    change_x = 0
    change_y = 0

    def __init__(self, x, y, width, matrix, args, *groups: AbstractGroup):
        Player.__init__(self, x, y, width, matrix, args)
        super().__init__(*groups)
        self.score = 0
        self.find_way = True
        self.angry_mode = False
        self.win = False
        self.time_counter = 0
        self.path = []
        self.speed = 1
        self.target = None
        self.last_action = None
        self.frame = 0
        self.terminal = True
        self.ep_rew = 0
        self.debounceCounter = 0

    def lesslive(self):
        self.live -= 1

    def change_speed_player(self, x, y):
        if self.rect.x > 587:
            self.rect.x = 17
        if self.rect.x < 17:
            self.rect.x = 587
        self.change_x += x
        self.change_y += y

    def clear_speed_player(self):
        self.prev_x = self.change_x
        self.prev_y = self.change_y

    def new_position_player(self, walls, spawn):
        old_x = self.rect.left
        new_x = old_x + self.change_x
        self.rect.left = new_x
        old_y = self.rect.top
        new_y = old_y + self.change_y

        x_sprite_collide = pygame.sprite.spritecollide(self, walls, False)
        if x_sprite_collide:
            self.rect.left = old_x
            self.rect.top=self.prev_y
            y_sprite_collide = pygame.sprite.spritecollide(self, walls, False)
            if y_sprite_collide:
                self.rect.top=old_y
        else:

            self.rect.top = new_y

            y_sprite_collide = pygame.sprite.spritecollide(self, walls, False)
            if y_sprite_collide:
                self.rect.top = old_y
                self.rect.left=self.prev_x
                x_sprite_collide = pygame.sprite.spritecollide(self, walls, False)
                if x_sprite_collide:
                    self.rect.left=old_x

        if spawn:
            spawn_sprite_collide = pygame.sprite.spritecollide(self, spawn, False)
            if spawn_sprite_collide:
                self.rect.left = old_x
                self.rect.top = old_y


def pacman_distance(x1, x2, dimension):
    if x1 > x2:
        x1, x2 = x2, x1
    return min(x2 - x1, x1 + dimension - x2)


def get_available_directions_coordinates(grid, i, j):
    dimension_x = len(grid)
    dimension_y = len(grid[0])
    coordinates_list = [[(i + 1) % dimension_x, j, 'down'], [(i - 1) % dimension_x, j, 'up'],
                        [i, (j + 1) % dimension_y, 'right'],
                        [i, (j - 1) % dimension_y, 'left']]
    result = []
    for coordinates in coordinates_list:
        if grid[coordinates[0]][coordinates[1]] != 0:
            result.append(coordinates)

    return result