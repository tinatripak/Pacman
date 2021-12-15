from point import Point
from algorithmshelpers import check_point, get_key, here_isnot_enemy, get_heuristic_path_length

visited_points = []


def get_neighbours(_point, speed):
    top = Point(_point.x, _point.y + speed)
    bottom = Point(_point.x, _point.y - speed)
    right = Point(_point.x + speed, _point.y)
    left = Point(_point.x - speed, _point.y)
    points = [top, bottom, right, left]
    for point in points:
        if check_point(point):
            yield point


def get_neighbours_and_save(_point, speed):
    top = Point(_point.x, _point.y + speed)
    bottom = Point(_point.x, _point.y - speed)
    right = Point(_point.x + speed, _point.y)
    left = Point(_point.x - speed, _point.y)
    points = [top, bottom, right, left]
    for point in points:
        if not visited_points.__contains__(_point) and check_point(point):
            visited_points.append(point)
            yield point


def get_key_value_neighbours(point, speed):
    points = get_neighbours(point, speed)
    key_value = []
    for item in points:
        key_value.append([(point.y / 10 + item.x / 7) * 2, item])
    key_value.sort(key=get_key)
    return key_value


def get_a_search_neighbours(point, speed):
    points = get_neighbours(point, speed)
    key_value = []
    for item in points:
        if here_isnot_enemy(item):
            key_value.append([(point.y / 10 + item.x / 7) * 2 + get_heuristic_path_length(point, item), item])
    key_value.sort(key=get_key)
    return key_value


def get_a_search_neighbourssecond(point, speed):
    points = get_neighbours(point, speed)
    key_value = []
    for item in points:
        if not here_isnot_enemy(item):
            key_value.append([(point.y / 10 + item.x / 7) * 2 + get_heuristic_path_length(point, item), item])
    key_value.sort(key=get_key)
    return key_value