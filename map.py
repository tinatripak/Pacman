import pygame
import random
from const import start_level, violet_colour, foundation_map
from walls import Walls


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


sprites_list = pygame.sprite.RenderPlain()
walls_list = first_map(sprites_list)
