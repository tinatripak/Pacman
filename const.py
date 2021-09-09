from enum import Enum


black_colour = (0, 0, 0)
white_colour = (255, 255, 255)
violet_colour = (66, 49, 137)


class DirectionState(Enum):
    right = 1
    left = 2
    up = 3
    down = 4
