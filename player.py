import pygame


class Player(pygame.sprite.Sprite):
    change_x = 0
    change_y = 0

    def __init__(self, x, y, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename)
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x
        self.prev_x = x
        self.prev_y = y
        self.live = 3
        self.min_algorithm = self.min_turn

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
        # x_sprite_collide = pygame.sprite.spritecollide(self, walls, False)
        # if x_sprite_collide:
        #     self.rect.left = old_x
        # else:
        #     self.rect.top = new_y
        #     y_sprite_collide = pygame.sprite.spritecollide(self, walls, False)
        #     if y_sprite_collide:
        #         self.rect.top = old_y

        if spawn:
            spawn_sprite_collide = pygame.sprite.spritecollide(self, spawn, False)
            if spawn_sprite_collide:
                self.rect.left = old_x
                self.rect.top = old_y

    def alfa_betta_pruning(self):
        j = self.rect.topleft[0]
        i = self.rect.topleft[1]
        all_coins = self.all_coins_indexes()
        recursion_index = 18
        betta = float('inf')
        v = float('-inf')
        best_direction = ''

        grid = self.grid
        all_directions = get_available_directions_coordinates(grid, i, j)

        for direction_i, direction_j, direction in all_directions:
            new_enemies = list(map(lambda enemy: copy(enemy), self.enemies.sprites()))
            count = 0
            available_coins = list(all_coins)
            if len(available_coins) == 0:
                return float('+inf')
            if (direction_i, direction_j) in available_coins:
                available_coins.remove((direction_i, direction_j))
                count += 10
            count += 1
            result = self.min_algorithm(direction_i, direction_j, count, all_coins, v, betta, recursion_index - 1,
                                        (i, j),
                                        new_enemies)
            if result >= v:
                v = result
                best_direction = direction
        return best_direction

    def all_coins_indexes(self):
        return tuple(map(lambda topleft: ((topleft[1] - 12), (topleft[0] - 12)),
                         map(lambda coin: coin.rect.topleft, self.dots_group.sprites())))

    def max_turn(self, i, j, score, dots, alfa, betta, recursion_index, previous, enemies) -> float:
        if recursion_index == 0:
            return score

        v = float('-inf')

        all_directions = get_available_directions_coordinates(self.grid, i, j)
        for direction_i, direction_j, direction in all_directions:
            if (direction_i, direction_j) == previous and len(all_directions) != 1:
                continue

            available_coins = list(dots)
            new_score = score
            if (direction_i, direction_j) in available_coins:
                available_coins.remove((direction_i, direction_j))
                new_score += 1
            result = self.min_algorithm(direction_i, direction_j, new_score, available_coins, max(alfa, v), betta,
                                        recursion_index - 1, (i, j), enemies)
            if result > v:
                v = result
                if v > betta:
                    return v
        if v > 0:
            return v

        for direction_i, direction_j, direction in all_directions:
            if (direction_i, direction_j) != previous or len(all_directions) == 1:
                continue

            available_coins = list(dots)
            new_score = score
            if (direction_i, direction_j) in available_coins:
                available_coins.remove((direction_i, direction_j))
                new_score += 10
            result = self.min_algorithm(direction_i, direction_j, new_score, available_coins, max(alfa, v), betta,
                                        recursion_index - 1, (i, j), enemies)
            if result > v:
                v = result
                if v > betta:
                    return v
        return v

    def min_turn(self, i, j, score, dots, alfa, betta, recursion_index, previous, enemies) -> float:
        new_enemies = list(map(lambda enemy: copy(enemy), enemies))

        x_dimension = len(self.grid)
        y_dimension = len(self.grid[0])

        for enemy in new_enemies:
            enemy.rect = enemy.rect.copy()
            enemy.update(i, j)
            enemy_i, enemy_j = enemy.get_coordinates()
            if pacman_distance(i, enemy_i, x_dimension) + pacman_distance(j, enemy_j, y_dimension) < 3:
                return float('-inf')

        return self.max_turn(i, j, score, dots, alfa, betta, recursion_index, previous, new_enemies)

    def expect_turn(self, i, j, score, dots, alfa, betta, recursion_index, previous, enemies) -> float:
        new_enemies = list(map(lambda enemy: copy(enemy), enemies))

        x_dimension = len(self.grid)
        y_dimension = len(self.grid[0])

        for enemy in new_enemies:
            enemy.rect = enemy.rect.copy()
            enemy.update(i, j)
            enemy_i, enemy_j = enemy.get_coordinates()
            if pacman_distance(i, enemy_i, x_dimension) + pacman_distance(j, enemy_j, y_dimension) < 3 \
                    and not isinstance(enemy, Pinky):
                return float('-inf')

        for enemy in new_enemies:
            enemy_i, enemy_j = enemy.get_coordinates()
            if pacman_distance(i, enemy_i, x_dimension) + pacman_distance(j, enemy_j, y_dimension) < 3:
                return 1 / 3 * self.max_turn(i, j, score, dots, alfa, betta, recursion_index, previous, new_enemies)

        return self.max_turn(i, j, score, dots, alfa, betta, recursion_index, previous, new_enemies)


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
