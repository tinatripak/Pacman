import pdb
import pygame
from pygame import *
from const import black_colour, violet_colour, white_colour, \
    DirectionState, SCREEN_SIZE, path_pacman_img, foundation_map, \
    AlgorithmType
from player import Player
from walls import Walls
from ghosts import Ghosts
from dots import Dots
import random
from point import Point
import collections
import time
import queue as Q


def notepad_to_array(path, array):
    with open(path) as f:
        content = f.read().splitlines()
        for s in content:
            temp = []
            for t in s.split(','):
                temp.append(int(t))
            array.append(temp)


def generator(f, n, x1, x2, y1, y2, width, height):
    for i in range(n):
        number1 = (random.randrange(x1, x2, 30))
        number2 = (random.randrange(y1, y2, 30))
        f.writelines(f"{number1},{number2},{width},{height}\n")


def create_mapgenerated(f, width, height):
    generator(f, 4, 30, 364, 30, 150, width, height)
    generator(f, 2, 370, 580, 30, 180, width, height)
    generator(f, 2, 60, 240, 242, 305, width, height)
    generator(f, 2, 370, 520, 242, 305, width, height)
    generator(f, 3, 30, 260, 380, 420, width, height)
    generator(f, 3, 300, 580, 450, 580, width, height)


def create_many_maps_for_levels(walls):
    a = f"maps/Map_{start_level}level.txt"
    f = open(a, 'w')
    create_mapgenerated(f, 30, 30)
    create_mapgenerated(f, 40, 15)
    f.writelines(foundation_map)
    f.close()
    notepad_to_array(a, walls)


screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption('Pac-Man')
board = pygame.image.load("pacman_startgame.png")
board1 = board.get_rect(
    bottomright=(800, 500))
screen.blit(board, board1)
pygame.display.update()


def start_music():
    pygame.init()
    mixer.music.load('music/pacman_beginning.wav')
    mixer.music.play()
    key_pressed = False
    while not key_pressed:
        for event_ in pygame.event.get():
            if event_.type == KEYDOWN and event_.key == K_RETURN:
                key_pressed = True


start_music()

directions_of_pinky = []
directions_of_blinky = []
directions_of_inky = []
directions_of_clyde = []
notepad_to_array("ghosts/ghosts_directions/Pinky_directions.txt", directions_of_pinky)
notepad_to_array("ghosts/ghosts_directions/Blinky_directions.txt", directions_of_blinky)
notepad_to_array("ghosts/ghosts_directions/Inky_directions.txt", directions_of_inky)
notepad_to_array("ghosts/ghosts_directions/Clyde_directions.txt", directions_of_clyde)


def first_map(sprites_list):
    wall_list = pygame.sprite.RenderPlain()
    walls = []
    # x, y, width, height
    if start_level == 1:
        notepad_to_array("maps/Map_1level.txt", walls)
    elif start_level > 1:
        create_many_maps_for_levels(walls)
    for i in walls:
        wall = Walls(i[0], i[1], i[2], i[3], violet_colour)
        wall_list.add(wall)
        sprites_list.add(wall)
    return wall_list


def spawn_setup(sprites_list):
    spawn = pygame.sprite.RenderPlain()
    spawn.add(Walls(281, 242, 44, 3, white_colour))
    sprites_list.add(spawn)
    return spawn


pygame.init()
clock = pygame.time.Clock()
pygame.font.init()
font = pygame.font.Font("trocchi.ttf", 20)
pacman_img = pygame.image.load(path_pacman_img)


def start_game():
    global start_level
    global walls_list
    global dots_list
    global pacman
    global blinky
    global pinky
    global inky
    global clyde
    global random_dot
    global pinky_point
    global inky_point
    global pacman_point

    inky_point = Point(0, 0)
    pacman_point = Point(0, 0)
    pinky_point = Point(0, 0)
    a_type = AlgorithmType.bfs
    timer_enemy1 = 10
    timer_enemy3 = 10
    counter = 10
    ghostlife = 3
    totalscore = 0

    sprites_list = pygame.sprite.RenderPlain()
    walls_list = first_map(sprites_list)
    dots_list = pygame.sprite.RenderPlain()
    spawn = spawn_setup(sprites_list)
    ghosts_list = pygame.sprite.RenderPlain()
    pacman_list = pygame.sprite.RenderPlain()
    big_dots_list = pygame.sprite.RenderPlain()

    blinky_turn = clyde_turn = 0
    blinky_steps = clyde_steps = 0

    pacman = Player(287, 439, path_pacman_img)
    blinky = Ghosts(287, 199, "ghosts/ghosts_img/2469740-blinky.png")
    pinky = Ghosts(287, 199, "ghosts/ghosts_img/2469744-pinky.png")
    inky = Ghosts(227, 199, "ghosts/ghosts_img/2469741-inky.png")
    clyde = Ghosts(287, 199, "ghosts/ghosts_img/2469743-clyde.png")
    spawnghost = Point(287, 199)

    sprites_list.add(pacman)
    pacman_list.add(pacman)
    ghosts_list.add(inky)
    sprites_list.add(inky)
    ghosts_list.add(clyde)
    sprites_list.add(clyde)
    ghosts_list.add(blinky)
    sprites_list.add(blinky)
    ghosts_list.add(pinky)
    sprites_list.add(pinky)

    # TODO Locations for dots
    coordinates_bigdots = [0, 18]
    for row in range(19):
        for column in range(19):
            if (6 < row < 9) and (7 < column < 11):
                continue

            elif any([abs(wall.rect.x - (30 * column) - 15) <= 32
                      and abs(wall.rect.y - (30 * row) - 15) <= 32 and column != 0 for wall in walls_list]):
                continue

            elif coordinates_bigdots.__contains__(column) and coordinates_bigdots.__contains__(row):
                big_dot = Dots(8, 8)
                big_dot.rect.x = 30 * column + 32
                big_dot.rect.y = 30 * row + 32
                dots_list.add(big_dot)
                sprites_list.add(big_dot)

            else:
                dot = Dots(4, 4)
                dot.rect.x = 30 * column + 32
                dot.rect.y = 30 * row + 32

                walls_dots_collide = pygame.sprite.spritecollide(dot, walls_list, False)
                pacman_dots_collide = pygame.sprite.spritecollide(dot, pacman_list, False)

                if walls_dots_collide or pacman_dots_collide:
                    continue
                else:
                    dots_list.add(dot)
                    sprites_list.add(dot)

    score = 0
    done = False
    win_score = len(dots_list)

    random_dot = choose_random_dot()
    pacman_point = random_dot.rect

    while not done:
        for event_ in pygame.event.get():
            if event_.type == pygame.QUIT:
                done = True
            if event_.type == pygame.KEYDOWN:
                if event_.key == pygame.K_UP:
                    pacman.image = set_direction(DirectionState.up.name)
                    pacman.change_speed_player(0, -30)
                if event_.key == pygame.K_DOWN:
                    pacman.image = set_direction(DirectionState.down.name)
                    pacman.change_speed_player(0, 30)
                if event_.key == pygame.K_LEFT:
                    pacman.image = set_direction(DirectionState.left.name)
                    pacman.change_speed_player(-30, 0)
                if event_.key == pygame.K_RIGHT:
                    pacman.image = set_direction(DirectionState.right.name)
                    pacman.change_speed_player(30, 0)
                if event_.key == pygame.K_z:
                    if a_type == AlgorithmType.bfs:
                        a_type = AlgorithmType.dfs
                    elif a_type == AlgorithmType.dfs:
                        a_type = AlgorithmType.ucs
                    elif a_type == AlgorithmType.ucs:
                        a_type = AlgorithmType.astar_search
                    elif a_type == AlgorithmType.astar_search:
                        a_type = AlgorithmType.bfs

            if event_.type == pygame.KEYUP:
                if event_.key == pygame.K_UP:
                    pacman.image = set_direction(DirectionState.up.name)
                    pacman.change_speed_player(0, 30)
                if event_.key == pygame.K_DOWN:
                    pacman.image = set_direction(DirectionState.down.name)
                    pacman.change_speed_player(0, -30)
                if event_.key == pygame.K_LEFT:
                    pacman.image = set_direction(DirectionState.left.name)
                    pacman.change_speed_player(30, 0)
                if event_.key == pygame.K_RIGHT:
                    pacman.image = set_direction(DirectionState.right.name)
                    pacman.change_speed_player(-30, 0)
        screen.blit(pygame.image.load("blue.png"), (random_dot.rect.x, random_dot.rect.y))
        pygame.display.flip()
        if pacman.rect.x == random_dot.rect.x and pacman.rect.y == random_dot.rect.y:
            random_dot = choose_random_dot()
            pacman_point = random_dot.rect

        move_ghosts(pacman, random_dot.rect, pacman_point, 30, False, True) # ----------------------------------------------------
        pacman.new_position_player(walls_list, spawn)

        if not timer_enemy1 == 0:
            timer_enemy1 -= 1
        else:
            timer_enemy1 = 2
            move_ghosts(inky, pacman.rect, inky_point, 30)

        inky.new_position_player(walls_list, False)

        changed_speed_clyde = clyde.change_speed_ghost(directions_of_clyde, False, clyde_turn, clyde_steps,
                                                       len(directions_of_clyde) - 1)
        clyde_turn = changed_speed_clyde[0]
        clyde_steps = changed_speed_clyde[1]
        clyde.change_speed_ghost(directions_of_clyde, "clyde", clyde_turn, clyde_steps, len(directions_of_clyde) - 1)

        clyde.new_position_player(walls_list, spawn)

        if not timer_enemy3 == 0:
            timer_enemy3 -= 1
        else:
            timer_enemy3 = 2
            move_ghosts(pinky, pacman.rect, pinky_point, 30)

        pinky.new_position_player(walls_list, False)

        changed_speed_blinky = blinky.change_speed_ghost(directions_of_blinky, False, blinky_turn, blinky_steps,
                                                         len(directions_of_blinky) - 1)
        blinky_turn = changed_speed_blinky[0]
        blinky_steps = changed_speed_blinky[1]
        blinky.change_speed_ghost(directions_of_blinky, False, blinky_turn, blinky_steps, len(directions_of_blinky) - 1)
        blinky.new_position_player(walls_list, False)

        check_location(pacman)

        check_location(inky)

        check_location(clyde)

        check_location(pinky)

        check_location(blinky)

        pacman_collides_dots = pygame.sprite.spritecollide(pacman, dots_list, True)
        if pacman_collides_dots:

            if len(pacman_collides_dots) > 0:
                score += len(pacman_collides_dots)
            mixer.music.load('music/pacman_chomp.wav')
            mixer.music.play()

        # TODO Clean
        screen.fill(black_colour)
        # TODO Draw
        walls_list.draw(screen)
        spawn.draw(screen)
        sprites_list.draw(screen)
        ghosts_list.draw(screen)

        # TODO Write Score Of Player
        text = font.render("High Score", True, (255, 255, 0))
        screen.blit(text, [690, 10])
        text1 = font.render(str(score) + "/" + str(win_score), True, (255, 255, 0))
        screen.blit(text1, [690, 40])

        text = font.render("Location", True, (255, 255, 0))
        screen.blit(text, [690, 80])
        text1 = font.render("X: " + str(pacman.rect.x) + " Y: " + str(pacman.rect.y), True, (255, 255, 0))
        screen.blit(text1, [690, 110])
        text1 = font.render(f"Your level:{start_level}", True, (255, 255, 0))
        screen.blit(text1, [690, 150])
        text1 = font.render(f"Your lives:{counter}", True, (255, 255, 0))
        screen.blit(text1, [690, 250])

        text = font.render("Time", True, (255, 255, 0))
        screen.blit(text, [690, 190])
        time_algor = 0
        if a_type == AlgorithmType.bfs:
            start_time = time.time()
            bfs_searcher(pinky, pacman)
            bfs_searcher(blinky, pacman)
            bfs_searcher(inky, pacman)
            bfs_searcher(clyde, pacman)
            time_algor = str(round(time.time() - start_time, 5))
        elif a_type == AlgorithmType.dfs:
            start_time = time.time()
            dfs_searcher(pacman, blinky)
            dfs_searcher(pacman, pinky)
            dfs_searcher(pacman, inky)
            dfs_searcher(pacman, clyde)
            time_algor = str(round(time.time() - start_time, 5))
        elif a_type == AlgorithmType.ucs:
            start_time = time.time()
            ucs_searcher(pacman, blinky)
            ucs_searcher(pacman, pinky)
            ucs_searcher(pacman, inky)
            ucs_searcher(pacman, clyde)
            time_algor = str(round(time.time() - start_time, 5))
        elif a_type == AlgorithmType.astar_search:
            start_time = time.time()
            a_star_s_searcher(pacman, blinky)
            a_star_s_searcher(pacman, pinky)
            a_star_s_searcher(pacman, inky)
            a_star_s_searcher(pacman, clyde)
            time_algor = str(round(time.time() - start_time, 5))
        mass_ghost = [pinky, inky, clyde, blinky]
        text = font.render(time_algor + "s", True, (255, 255, 0))
        screen.blit(text, [690, 220])
        for dot in dots_list:
            if dot == Dots(8, 8):
                for ghost in ghosts_list:
                    ghost.image = pygame.image.load("ghosts/ghosts_img/vulnerable.png")
                    now = time.time()
                    future = now + 10
                    while time.time() < future:
                        if pygame.sprite.spritecollide(pacman, ghosts_list, False):
                            for i in mass_ghost:
                                if ghost == i:
                                    killghost(i)
                            totalscore += 400
                        pinky.image = pygame.image.load("ghosts/ghosts_img/2469744-pinky.png")
                        inky.image = pygame.image.load("ghosts/ghosts_img/2469741-inky.png")
                        blinky.image = pygame.image.load("ghosts/ghosts_img/2469740-blinky.png")
                        clyde.image = pygame.image.load("ghosts/ghosts_img/2469743-clyde.png")
                        pass

        if pygame.sprite.spritecollide(pacman, ghosts_list, False):
            mixer.music.load('music/pacman_death.wav')
            mixer.music.play()
            counter -= 1
            if counter == 0:
                finish_game(f"You lose!", 235, sprites_list, dots_list, ghosts_list, pacman_list, walls_list, spawn)
        if score == win_score:
            start_level += 1
            finish_game("You won!", 180, sprites_list, dots_list, ghosts_list, pacman_list, walls_list, spawn)

        pygame.display.flip()
        clock.tick(10)


def choose_random_dot():
    mass = []
    for dot in dots_list:
        mass.append(dot)
    random_dot = random.choice(mass)
    random_dot.rect.x -= 15
    random_dot.rect.y -= 13
    return random_dot


def killghost(ghost):
    ghost.lesslive()
    ghost.rect = spawnghost


def move_ghosts(ghost, point, ghost_point, speed, is_bfs=True, is_pacman=False):
    if is_bfs:
        array_res = bfs(point.x, point.y, ghost.rect.x, ghost.rect.y)
    else:
        array_res = astar_search(point.x, point.y, ghost.rect.x, ghost.rect.y)
    if array_res is not None:
        i = 0
        point = array_res[i]
        if len(array_res) > i + 1:
            ghost_point = array_res[i + 1]
        while point.x == ghost.rect.x and point.y == ghost.rect.y:
            i += 1
            point = array_res[i]
            if len(array_res) > i + 1:
                ghost_point = array_res[i + 1]
    else:
        point = ghost_point
    if point.y < ghost.rect.y and check_point(Point(ghost.rect.x, ghost.rect.y - speed)):
        if is_pacman:
            pacman.image = set_direction(DirectionState.up.name)
        ghost.rect.move_ip(0, -speed)
    elif point.y > ghost.rect.y and check_point(Point(ghost.rect.x, ghost.rect.y + speed)):
        if is_pacman:
            pacman.image = set_direction(DirectionState.down.name)
        ghost.rect.move_ip(0, speed)
    elif point.x < ghost.rect.x and check_point(Point(ghost.rect.x - speed, ghost.rect.y)):
        if is_pacman:
            pacman.image = set_direction(DirectionState.left.name)
        ghost.rect.move_ip(-speed, 0)
    elif point.x > ghost.rect.x and check_point(Point(ghost.rect.x + speed, ghost.rect.y)):
        if is_pacman:
            pacman.image = set_direction(DirectionState.right.name)
        ghost.rect.move_ip(speed, 0)


def bfs_searcher(player, enemy):
    array_res = bfs(player.rect.x, player.rect.y, enemy.rect.x, enemy.rect.y)
    if array_res is not None:
        for i in array_res:
            screen.blit(pygame.image.load("blue.png"), (i.x, i.y))
            pygame.display.flip()


def dfs_searcher(player, enemy):
    array_res = dfs(player.rect.x, player.rect.y, enemy.rect.x, enemy.rect.y)
    if array_res is not None:
        for i in array_res:
            screen.blit(pygame.image.load("pink.png"), (i.x, i.y))
            pygame.display.flip()


def ucs_searcher(player, enemy):
    array_res = ucs(player.rect.x, player.rect.y, enemy.rect.x, enemy.rect.y)
    if array_res is not None:
        for i in array_res:
            screen.blit(pygame.image.load("yellow.png"), (i.x, i.y))
            pygame.display.flip()


def a_star_s_searcher(player, enemy):
    array_res = astar_search(player.rect.x, player.rect.y, enemy.rect.x, enemy.rect.y)
    if array_res is not None:
        for i in array_res:
            screen.blit(pygame.image.load("purple.png"), (i.x, i.y))
            pygame.display.flip()


def set_direction(direction):
    if direction == "right":
        return pacman_img
    if direction == "up":
        return pygame.transform.rotate(pacman_img, 90)
    if direction == "left":
        return pygame.transform.rotate(pacman_img, 180)
    if direction == "down":
        return pygame.transform.rotate(pacman_img, 270)


def check_location(player):
    if (player.rect.x < 17) and (259 <= player.rect.y <= 319):
        player.rect.x = 587

    if (player.rect.x > 587) and (259 <= player.rect.y <= 319):
        player.rect.x = 17


def finish_game(message, left, sprites_list, dots_list, ghosts_list, pacman_list, walls_list, spawn):
    while True:

        for event_ in pygame.event.get():
            if event_.type == pygame.QUIT:
                pygame.quit()
                pdb.set_trace()
            if event_.type == pygame.KEYDOWN:
                if event_.key == pygame.K_ESCAPE:
                    pygame.quit()
                    pdb.set_trace()
                if event_.key == pygame.K_RETURN:
                    del sprites_list
                    del dots_list
                    del ghosts_list
                    del pacman_list
                    del walls_list
                    del spawn
                    start_game()

        # TODO Window output: win or loss
        window = pygame.Surface((300, 170))
        window.set_alpha(10)
        window.fill((255, 0, 0))
        screen.blit(window, (160, 220))

        text1 = font.render(message, True, (255, 246, 212))
        screen.blit(text1, [left, 233])
        text2 = font.render("ENTER to PLAY again", True, (255, 246, 212))
        screen.blit(text2, [180, 303])
        text3 = font.render("ESC to FINISH this game", True, (255, 246, 212))
        screen.blit(text3, [180, 333])

        pygame.display.flip()
        clock.tick(10)


def get_neighbours(_point, speed):
    top = Point(_point.x, _point.y + speed)
    bottom = Point(_point.x, _point.y - speed)
    right = Point(_point.x + speed, _point.y)
    left = Point(_point.x - speed, _point.y)
    points = [top, bottom, right, left]
    result = []
    for point in points:
        if check_point(point):
            result.append(point)
    return result


def get_key_value_neighbours(point, speed):
    points = get_neighbours(point, speed)
    key_value = []
    for item in points:
        key_value.append([(point.y / 10 + item.x / 7) * 2, item])
    key_value.sort(key=get_key)
    return key_value


def get_a_search_neighbours(point, speed):
    points = get_neighbours(point, speed)
    key_value = []
    for item in points:
        if here_isnot_enemy(item):
            key_value.append([(point.y / 10 + item.x / 7) * 2 + get_heuristic_path_length(point, item), item])
    key_value.sort(key=get_key)
    return key_value


def here_isnot_enemy(point):
    if point.x == blinky.rect.x and point.y == blinky.rect.y:
        return False
    if point.x == pinky.rect.x and point.y == pinky.rect.y:
        return False
    if point.x == inky.rect.x and point.y == inky.rect.y:
        return False
    if point.x == clyde.rect.x and point.y == clyde.rect.y:
        return False
    return True


def get_heuristic_path_length(point, item):
    return abs(point.x - item.x) + abs(point.y - item.y)


def get_key(item):
    return item[0]


def check_point(point):
    x_def = 13
    y_def = 11
    if point.x < 17 or point.x > 559 or point.y < 17 or point.y > 559 \
            or (229 <= point.y <= 289) and (227 <= point.x <= 347):
        return False
    for wall in walls_list:
        if wall.rect.x - x_def == point.x and wall.rect.y - y_def == point.y:
            return False
        if wall.rect.x - x_def <= point.x <= wall.rect.x - x_def + wall.rect.width and \
                wall.rect.y - y_def <= point.y <= wall.rect.y - y_def + wall.rect.height:
            return False
    return True


def bfs(start_x, start_y, end_x, end_y):
    start = Point(start_x, start_y)
    end = Point(end_x, end_y)
    visited, queue = set(), collections.deque([start])
    visited.add(start)
    path = {start: None}
    while len(queue) > 0:
        vertex = queue.popleft()

        for neighbour in get_neighbours(vertex, 30):
            if not contains_point(neighbour, visited):
                visited.add(neighbour)
                if not contains_point(neighbour, queue):
                    queue.append(neighbour)
                    path[neighbour] = vertex

            if neighbour.x == end.x and neighbour.y == end.y:
                return get_path(path, end)


def dfs(start_x, start_y, end_x, end_y):
    start = Point(start_x, start_y)
    end = Point(end_x, end_y)
    visited, queue = set(), collections.deque([start])
    visited.add(start)
    path = {start: None}
    while len(queue) > 0:
        vertex = queue.pop()

        for neighbour in get_neighbours(vertex, 30):
            if not contains_point(neighbour, visited):
                visited.add(neighbour)
                if not contains_point(neighbour, queue):
                    queue.append(neighbour)
                    path[neighbour] = vertex

            if neighbour.x == end.x and neighbour.y == end.y:
                return get_path(path, end)


def ucs(start_x, start_y, end_x, end_y):
    start = Point(start_x, start_y)
    end = Point(end_x, end_y)

    visited = [start]
    queue = Q.PriorityQueue()
    queue.put((0, start))
    path = {start: None}

    while not queue.empty():
        vertex_temp = queue.get()
        vertex = vertex_temp[len(vertex_temp) - 1]

        for neighbour in get_key_value_neighbours(vertex, 30):
            if not contains_point(neighbour[1], visited):
                visited.append(neighbour[1])
                if neighbour not in (x for x in queue.queue):
                    queue.put((neighbour[0], neighbour[1]))
                    path[neighbour[1]] = vertex

            if neighbour[1].x == end.x and neighbour[1].y == end.y:
                return get_path(path, end)


def heuristic(from_, to):
    return abs(from_.x - to.x) + abs(from_.y - to.y)


def astar_search(start_x, start_y, end_x, end_y):
    start = Point(start_x, start_y)
    end = Point(end_x, end_y)

    visited = [start]
    queue = Q.PriorityQueue()
    queue.put((0, start))
    path = {start: None}

    while not queue.empty():
        vertex_temp = queue.get()
        vertex = vertex_temp[len(vertex_temp) - 1]

        for neighbour in get_a_search_neighbours(vertex, 30):
            if not contains_point(neighbour[1], visited):
                visited.append(neighbour[1])
                if neighbour not in (x for x in queue.queue):
                    queue.put((neighbour[0], neighbour[1]))
                    path[neighbour[1]] = vertex

            if neighbour[1].x == end.x and neighbour[1].y == end.y:
                return get_path(path, end)


def get_path(path, end):
    result = []
    point = end
    result.append(point)
    dict_value = get_form_dict(path, point)
    while dict_value is not None:
        result.append(dict_value)
        point = dict_value
        dict_value = get_form_dict(path, point)
    return result


def contains_point(point, array):
    for item in array:
        if item.x == point.x and item.y == point.y:
            return True
    return False


def get_form_dict(path, _key):
    for item in path.items():
        if item[0].x == _key.x and item[0].y == _key.y:
            return item[1]
    return None


start_level = 1

start_game()
pygame.quit()
pdb.set_trace()
