import math

from point import Point
from node import Node
from const import pacman, get_enemies_coordinates, speed
from neighbours import get_neighbours_and_save
import random


def evaluate(target: Point):
    enemy_distance = math.inf
    player_coord = pacman.rect
    if target == player_coord:
        return -math.inf
    enemies_coords = get_enemies_coordinates()

    for enemy in enemies_coords:
        distance = math.sqrt(math.pow(
            enemy.x - player_coord.x, 2) + math.pow(enemy.y - player_coord.y, 2))
        if enemy_distance is None or enemy_distance > distance:
            enemy_distance = distance
    target_distance = math.sqrt(math.pow(
        target.x - player_coord.x, 2) + math.pow(target.y - player_coord.y, 2))
    output = -(target_distance + enemy_distance) / 2

    return output


def tree_build(start: Point, target):
    start_node = Node(start, None)
    tree_build_recursive(start_node, 1, target)
    return start_node


def tree_build_recursive(current_node: Node, depth, target):
    if depth > 5:
        current_node.value = evaluate(target)
        return None

    player_coord = pacman.rect
    enemies_coords = get_enemies_coordinates()

    if depth % 2 == 1:
        neighboring_nodes = get_neighbours_and_save(player_coord, speed)

        new_nodes = list(map(lambda item: Node(item, None), neighboring_nodes))

        current_node.children = new_nodes

    else:
        neighboring_nodes = []

        for coord in enemies_coords:
            next_nodes = get_neighbours_and_save(coord, speed)
            neighboring_nodes.append(list(map(lambda node: node.x, next_nodes)))
        variations = get_variations(neighboring_nodes)
        new_nodes = []
        for variant in variations:
            if player_coord in variant:
                continue
            point = enemies_coords[random.randrange(0, 3)]

            new_nodes.append(Node(point, None))
        current_node.children = new_nodes
    for child in current_node.children:
        tree_build_recursive(child, depth + 1, target)


def get_variations(arr):
    result = []

    def get_variations_recurs(last_arr, res):
        if len(last_arr) == 0:
            result.append(res)
            return
        curr_arr = last_arr[0]
        for item in curr_arr:
            get_variations_recurs(last_arr[1:], res + [item])

    get_variations_recurs(arr, [])
    return result