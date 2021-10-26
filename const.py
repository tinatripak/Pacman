from enum import Enum
import pygame
from player import Player
from ghosts import Ghosts
from point import Point


start_level = 1

SCREEN_SIZE = (900, 604)

black_colour = (0, 0, 0)
white_colour = (255, 255, 255)
violet_colour = (66, 49, 137)
path_pacman_img = "player/pacman.png"
pacman_img = pygame.image.load(path_pacman_img)
pacman = Player(287, 439, path_pacman_img)
blinky = Ghosts(287, 199, "ghosts/ghosts_img/2469740-blinky.png")
pinky = Ghosts(287, 199, "ghosts/ghosts_img/2469744-pinky.png")
inky = Ghosts(227, 199, "ghosts/ghosts_img/2469741-inky.png")
clyde = Ghosts(287, 199, "ghosts/ghosts_img/2469743-clyde.png")
spawnghost = Point(287, 199)
speed = 30
FILENAME = "results.csv"
header = ["Status game", "Score", "Time", "Algorithm"]
foundation_map = ("0,0,6,200\n"
                  "0,400,6,200\n"
                  "600,0,6,250\n"
                  "600,350,6,250\n"
                  "0,200,63,50\n"
                  "0,355,63,50\n"
                  "0,0,600,6\n"
                  "0,600,606,6\n"
                  "241,242,40,2\n"
                  "325,242,40,2\n"
                  "241,305,125,2\n"
                  "241,242,2,63\n"
                  "364,242,2,63\n"
                  "540,200,63,50\n"
                  "540,350,63,50\n")


def get_enemies_coordinates():
    enemies = [blinky.rect, inky.rect, pinky.rect, clyde.rect]
    return enemies


class DirectionState(Enum):
    right = 1
    left = 2
    up = 3
    down = 4


class AlgorithmType(Enum):
    bfs = 1
    dfs = 2
    ucs = 3
    astar_search = 4
