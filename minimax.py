from main import *
import math


def minimax(node, alpha, beta, depth):
    optimal = depth % 2 == 0
    if len(get_neighbours(node, 30)) == 0:
        return node

    if optimal:
        best = -math.inf
        for neighbour in get_neighbours(node, 30):
            value = minimax(neighbour, alpha, beta, depth + 1)
            best = max(best, value) \
                if value != None else best
            alpha = max(alpha, best)
            if beta <= alpha:
                break
        node = best
        return best

    else:
        best = math.inf
        for neighbour in get_neighbours(node, 30):
            value = minimax(neighbour, alpha, beta, depth + 1)
            best = min(best, value) \
                if value != None else best
            beta = min(beta, best)
            if beta <= alpha:
                break
        node = best
        return best


def expectimax(node, depth):
    optimal = depth % 2 == 0
    if len(get_neighbours(node, 30)) == 0:
        return node

    if optimal:
        best = -math.inf
        for neighbour in get_neighbours(node, 30):
            value = expectimax(neighbour, depth+1)
            best = max(best, value) \
                if value != None else best
        node = best
        return best

    else:
        values = 0
        for neighbour in get_neighbours(node, 30):
            value = expectimax(neighbour, depth+1)
            values += value \
                if value != None else 0
        node = values / len(get_neighbours(node, 30))
        return node