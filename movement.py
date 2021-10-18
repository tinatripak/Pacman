from algorithms import bfs, astar_search
from algorithmshelpers import check_point
from point import Point
from const import DirectionState, pacman_img, pacman
import pygame


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


def set_direction(direction):
    if direction == "right":
        return pacman_img
    if direction == "up":
        return pygame.transform.rotate(pacman_img, 90)
    if direction == "left":
        return pygame.transform.rotate(pacman_img, 180)
    if direction == "down":
        return pygame.transform.rotate(pacman_img, 270)