class Node:
    def __init__(self, point, value) -> None:
        self.value = value
        self.point = point
        self.children: list[Node] = []