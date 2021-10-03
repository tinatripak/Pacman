class SquareGrid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.walls = []


class GridWithWeights(SquareGrid):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.weights = {}

    def cost(self, from_node, to_node):
        return self.weights.get(to_node, 1)