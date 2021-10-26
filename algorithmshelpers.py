from const import blinky, inky, pinky, clyde
from map import walls_list


def here_isnot_enemy(point):
    if point.x == blinky.rect.x and point.y == blinky.rect.y:
        return False
    if point.x == pinky.rect.x and point.y == pinky.rect.y:
        return False
    if point.x == inky.rect.x and point.y == inky.rect.y:
        return False
    if point.x == clyde.rect.x and point.y == clyde.rect.y:
        return False
    return True


def get_heuristic_path_length(point, item):
    return abs(point.x - item.x) + abs(point.y - item.y)


def get_key(item):
    return item[0]


def check_point(point):
    x_def = 13
    y_def = 11
    if point.x < 17 or point.x > 559 or point.y < 17 or point.y > 559 \
            or (229 <= point.y <= 289) and (227 <= point.x <= 347):
        return False
    for wall in walls_list:
        if wall.rect.x - x_def == point.x and wall.rect.y - y_def == point.y:
            return False
        if wall.rect.x - x_def <= point.x <= wall.rect.x - x_def + wall.rect.width and \
                wall.rect.y - y_def <= point.y <= wall.rect.y - y_def + wall.rect.height:
            return False
    return True


def get_path(path, end):
    result = []
    point = end
    result.append(point)
    dict_value = get_form_dict(path, point)
    while dict_value is not None:
        result.append(dict_value)
        point = dict_value
        dict_value = get_form_dict(path, point)
    return result


def contains_point(point, array):
    for item in array:
        if item.x == point.x and item.y == point.y:
            return True
    return False


def get_form_dict(path, _key):
    for item in path.items():
        if item[0].x == _key.x and item[0].y == _key.y:
            return item[1]
    return None
