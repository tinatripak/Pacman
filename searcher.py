import pygame
from const import SCREEN_SIZE
from algorithms import bfs, dfs, ucs, astar_search

screen = pygame.display.set_mode(SCREEN_SIZE)


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