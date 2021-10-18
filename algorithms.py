from point import Point
import collections
from neighbours import get_neighbours, get_key_value_neighbours, get_a_search_neighbours
from algorithmshelpers import contains_point, get_path
import queue as Q


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


def heuristic(from_, to):
    return abs(from_.x - to.x) + abs(from_.y - to.y)