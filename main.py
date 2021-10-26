import csv
import pdb
import random

import pygame
from pygame import *

from const import black_colour, white_colour, DirectionState, SCREEN_SIZE, AlgorithmType, FILENAME

from searcher import bfs_searcher, dfs_searcher, ucs_searcher, a_star_s_searcher
from movement import move_ghosts, set_direction, pacman
from map import notepad_to_array, sprites_list, walls_list
from const import  inky, blinky, pinky, clyde

from dots import Dots
from point import Point
from walls import Walls
import time
import math

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


graph = {}
start_music()

directions_of_pinky = []
directions_of_blinky = []
directions_of_inky = []
directions_of_clyde = []
notepad_to_array("ghosts/ghosts_directions/Pinky_directions.txt", directions_of_pinky)
notepad_to_array("ghosts/ghosts_directions/Blinky_directions.txt", directions_of_blinky)
notepad_to_array("ghosts/ghosts_directions/Inky_directions.txt", directions_of_inky)
notepad_to_array("ghosts/ghosts_directions/Clyde_directions.txt", directions_of_clyde)


def spawn_setup(sprites_list):
    spawn = pygame.sprite.RenderPlain()
    spawn.add(Walls(281, 242, 44, 3, white_colour))
    sprites_list.add(spawn)
    return spawn


pygame.init()
clock = pygame.time.Clock()
pygame.font.init()
font = pygame.font.Font("trocchi.ttf", 20)


def create_reqursive_graph():
    for item in self.road_blocks:
        if not isinstance(item, NullRoad) and not isinstance(item, GhostBlock):
            self.graph[item] = {}
            for direction in item.directions.values():
                if not isinstance(direction, NullRoad) and not isinstance(direction, GhostBlock):
                    if isinstance(item, PortalBlock) and isinstance(direction, PortalBlock):
                        self.graph[item][direction] = 0
                    else:
                        self.graph[item][direction] = \
                            (item.position - direction.position).magnitude_squared()

def start_game():
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


    start_level = 1
    totalscore = 0
    is_time_to_kill_ghost = False
    time_to_kill = -1
    inky_point = Point(0, 0)
    pacman_point = Point(0, 0)
    pinky_point = Point(0, 0)
    a_type = AlgorithmType.bfs
    timer_enemy1 = 10
    timer_enemy3 = 10
    counter = 1

    dots_list = pygame.sprite.RenderPlain()
    spawn = spawn_setup(sprites_list)
    ghosts_list = pygame.sprite.RenderPlain()
    pacman_list = pygame.sprite.RenderPlain()

    blinky_turn = clyde_turn = 0
    blinky_steps = clyde_steps = 0

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
    game_time = time.time()
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

        move_ghosts(pacman, random_dot.rect, pacman_point, 30, False, True)
        # ---------------------------------------
        pacman.new_position_player(walls_list, spawn)

        # if not timer_enemy1 == 0:
        #     timer_enemy1 -= 1
        # else:
        #     timer_enemy1 = 2
            #move_ghosts(inky, pacman.rect, inky_point, 30)

        #inky.new_position_player(walls_list, False)

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
            for dot in dots_list:
                if dot.rect.height == 8 and dot.rect.width == 8 \
                        and ((pacman.rect.x == 17 and pacman.rect.y == 19) or
                             (pacman.rect.x == 17 and pacman.rect.y == 559) or
                             (pacman.rect.x == 557 and pacman.rect.y == 19) or
                             (pacman.rect.x == 557 and pacman.rect.y == 559)):

                    # 17 + 30*18, 17 + 30*0, 19 + 30*0, 19 + 30*18
                    is_time_to_kill_ghost = True
                    time_to_kill = 50
                    # distance1 = math.hypot(abs(pacman.rect.x - inky.rect.x), abs(pacman.rect.y - inky.rect.y))
                    # distance2 = math.hypot(abs(pacman.rect.x - blinky.rect.x), abs(pacman.rect.y - blinky.rect.y))
                    # distance3 = math.hypot(abs(pacman.rect.x - pinky.rect.x), abs(pacman.rect.y - pinky.rect.y))
                    # distance4 = math.hypot(abs(pacman.rect.x - clyde.rect.x), abs(pacman.rect.y - clyde.rect.y))
                    # mass_distance = [distance1, distance2, distance3, distance4]
                    # mindistance = my_min(mass_distance)
                    # if mindistance == distance1:
                    #     move_ghosts(pacman, inky.rect, pacman_point, 30, True, True)
                    #     pacman.new_position_player(walls_list, spawn)
                    # if mindistance == distance2:
                    #     move_ghosts(pacman, blinky.rect, pacman_point, 30, True, True)
                    #     pacman.new_position_player(walls_list, spawn)
                    # if mindistance == distance3:
                    #     move_ghosts(pacman, pinky.rect, pacman_point, 30, True, True)
                    #     pacman.new_position_player(walls_list, spawn)
                    # if mindistance == distance4:
                    #     move_ghosts(pacman, clyde.rect, pacman_point, 30, True, True)
                    #     pacman.new_position_player(walls_list, spawn)
                    # --------------------------------------------------------------------------------------------------------------------------------------------------
                    # move_ghosts(pacman, Point(227, 199), pacman_point,30,True,True)
                    move_ghosts(pacman, inky.rect, pacman_point, 30, True, True)
                    pacman.new_position_player(walls_list, spawn)
                    pinky.image = pygame.image.load("ghosts/ghosts_img/vulnerable.png")
                    inky.image = pygame.image.load("ghosts/ghosts_img/vulnerable.png")
                    blinky.image = pygame.image.load("ghosts/ghosts_img/vulnerable.png")
                    clyde.image = pygame.image.load("ghosts/ghosts_img/vulnerable.png")

        if time_to_kill > 0:
            time_to_kill -= 1
        elif time_to_kill == 0:
            time_to_kill = -1
            is_time_to_kill_ghost = False
            pinky.image = pygame.image.load("ghosts/ghosts_img/2469744-pinky.png")
            inky.image = pygame.image.load("ghosts/ghosts_img/2469741-inky.png")
            blinky.image = pygame.image.load("ghosts/ghosts_img/2469740-blinky.png")
            clyde.image = pygame.image.load("ghosts/ghosts_img/2469743-clyde.png")
            move_ghosts(pacman, random_dot.rect, pacman_point, 30, False, True)
            pacman.new_position_player(walls_list, spawn)

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
        text = font.render(time_algor + "s", True, (255, 255, 0))
        screen.blit(text, [690, 220])

        if pygame.sprite.spritecollide(pacman, ghosts_list, False):
            if is_time_to_kill_ghost:
                for ghost in ghosts_list:
                    if pacman.rect.x == ghost.rect.x and pacman.rect.y == ghost.rect.y:
                        killghost(ghost)
                        totalscore += 400
            else:
                mixer.music.load('music/pacman_death.wav')
                mixer.music.play()
                counter -= 1
                if counter == 0:
                    row_contents = ['lose', score, str(round(time.time() - game_time, 5)), 'algorithm']
                    append_list_as_row(FILENAME, row_contents)
                    finish_game(f"You lose!", 235, sprites_list, dots_list, ghosts_list, pacman_list, walls_list, spawn)
        if score == win_score:
            start_level += 1
            row_contents = ['win', score, str(round(time.time() - game_time, 5)), 'algorithm']
            append_list_as_row(FILENAME, row_contents)
            finish_game("You won!", 180, sprites_list, dots_list, ghosts_list, pacman_list, walls_list, spawn)

        pygame.display.flip()
        clock.tick(10)


def append_list_as_row(file_name, list_of_elem):
    with open(file_name, 'a+', newline='') as write_obj:
        csv_writer = csv.writer(write_obj)
        csv_writer.writerow(list_of_elem)


def my_min(sequence):
    low = sequence[0]
    for i in sequence:
        if i < low:
            low = i
    return low


def choose_random_dot():
    mass = []
    for dot in dots_list:
        mass.append(dot)
    random_dot = random.choice(mass)
    random_dot.rect.x -= 15
    random_dot.rect.y -= 13
    return random_dot


def killghost(ghost):
    # ghost.rect = spawnghost
    ghost.rect.x = 287
    ghost.rect.x = 199


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


start_level = 1

start_game()
pygame.quit()
pdb.set_trace()
