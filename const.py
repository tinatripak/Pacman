from enum import Enum
import pygame


SCREEN_SIZE = (900, 604)

black_colour = (0, 0, 0)
white_colour = (255, 255, 255)
violet_colour = (66, 49, 137)
path_pacman_img = "pacman.png"
font = pygame.font.Font("trocchi.ttf", 20)


class DirectionState(Enum):
    right = 1
    left = 2
    up = 3
    down = 4
