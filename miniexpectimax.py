import math
from tree import tree_build
from node import Node


def move_by_alorithm(point, target_position):
    root_node = tree_build(point, target_position)
    # best_value = minimax(root_node, -math.inf, math.inf, 0)
    best_value = expectimax(root_node, 0)

    for child in root_node.children:
        if child.value == best_value:
            new_position = child.point
            return [new_position]


def minimax(curr_node: Node, alpha, beta, depth):
    is_max = depth % 2 == 0
    if len(curr_node.children) == 0:
        return curr_node.value

    if is_max:
        best_value = -math.inf
        for child in curr_node.children:
            value = minimax(child, alpha, beta, depth+1)
            best_value = max(
                best_value, value) if value is not None else best_value
            alpha = max(alpha, best_value)
            if beta <= alpha:
                break
        curr_node.value = best_value
        return best_value

    else:
        best_value = math.inf
        for child in curr_node.children:
            value = minimax(child, alpha, beta, depth+1)
            best_value = min(
                best_value, value) if value is not None else best_value
            beta = min(beta, best_value)
            if beta <= alpha:
                break
        curr_node.value = best_value
        return best_value


def expectimax(curr_node: Node, depth):
    is_max = depth % 2 == 0
    if len(curr_node.children) == 0:
        return curr_node.value

    if is_max:
        best_value = -math.inf
        for child in curr_node.children:
            value = expectimax(child, depth+1)
            best_value = max(
                best_value, value) if value is not None else best_value
        curr_node.value = best_value
        return best_value

    else:
        values = 0
        for child in curr_node.children:
            value = expectimax(child, depth+1)
            values += value if value is not None else 0
        curr_node.value = values / len(curr_node.children)
        return curr_node.value
