from enum import Enum


SCREEN_SIZE = (900, 604)

black_colour = (0, 0, 0)
white_colour = (255, 255, 255)
violet_colour = (66, 49, 137)
path_pacman_img = "player/pacman.png"
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


class DirectionState(Enum):
    right = 1
    left = 2
    up = 3
    down = 4
