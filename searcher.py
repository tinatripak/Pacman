from main import *

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


def check_location(player):
    if (player.rect.x < 17) and (259 <= player.rect.y <= 319):
        player.rect.x = 587

    if (player.rect.x > 587) and (259 <= player.rect.y <= 319):
        player.rect.x = 17


def get_neighbours(_point, speed):
    top = Point(_point.x, _point.y + speed)
    bottom = Point(_point.x, _point.y - speed)
    right = Point(_point.x + speed, _point.y)
    left = Point(_point.x - speed, _point.y)
    points = [top, bottom, right, left]
    result = []
    for point in points:
        if check_point(point):
            result.append(point)
    return result


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


def bfs(start_x, start_y, end_x, end_y):
    start = Point(start_x, start_y)
    end = Point(end_x, end_y)
    visited, queue = set(), collections.deque([start])
    visited.add(start)
    path = {start: None}
    while len(queue) > 0:
        vertex = queue.popleft()

        for neighbour in get_neighbours(vertex, 30):
            if not contains_point(neighbour, visited):
                visited.add(neighbour)
                if not contains_point(neighbour, queue):
                    queue.append(neighbour)
                    path[neighbour] = vertex

            if neighbour.x == end.x and neighbour.y == end.y:
                return get_path(path, end)


def dfs(start_x, start_y, end_x, end_y):
    start = Point(start_x, start_y)
    end = Point(end_x, end_y)
    visited, queue = set(), collections.deque([start])
    visited.add(start)
    path = {start: None}
    while len(queue) > 0:
        vertex = queue.pop()

        for neighbour in get_neighbours(vertex, 30):
            if not contains_point(neighbour, visited):
                visited.add(neighbour)
                if not contains_point(neighbour, queue):
                    queue.append(neighbour)
                    path[neighbour] = vertex

            if neighbour.x == end.x and neighbour.y == end.y:
                return get_path(path, end)


def ucs(start_x, start_y, end_x, end_y):
    start = Point(start_x, start_y)
    end = Point(end_x, end_y)

    visited = [start]
    queue = Q.PriorityQueue()
    queue.put((0, start))
    path = {start: None}

    while not queue.empty():
        vertex_temp = queue.get()
        vertex = vertex_temp[len(vertex_temp) - 1]

        for neighbour in get_key_value_neighbours(vertex, 30):
            if not contains_point(neighbour[1], visited):
                visited.append(neighbour[1])
                if neighbour not in (x for x in queue.queue):
                    queue.put((neighbour[0], neighbour[1]))
                    path[neighbour[1]] = vertex

            if neighbour[1].x == end.x and neighbour[1].y == end.y:
                return get_path(path, end)


def heuristic(from_, to):
    return abs(from_.x - to.x) + abs(from_.y - to.y)


def astar_search(start_x, start_y, end_x, end_y):
    start = Point(start_x, start_y)
    end = Point(end_x, end_y)

    visited = [start]
    queue = Q.PriorityQueue()
    queue.put((0, start))
    path = {start: None}

    while not queue.empty():
        vertex_temp = queue.get()
        vertex = vertex_temp[len(vertex_temp) - 1]

        for neighbour in get_a_search_neighbours(vertex, 30):
            if not contains_point(neighbour[1], visited):
                visited.append(neighbour[1])
                if neighbour not in (x for x in queue.queue):
                    queue.put((neighbour[0], neighbour[1]))
                    path[neighbour[1]] = vertex

            if neighbour[1].x == end.x and neighbour[1].y == end.y:
                return get_path(path, end)


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
