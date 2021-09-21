class BFS:

    def __init__(self, graph, start, goal):
        self.graph = graph
        self.start = start
        self.goal = goal

    def solve(self):
        print(self.graph)
        explored = []

        queue = [[self.start]]

        if self.start == self.goal:
            return 'That was easy. Start == Goal'

        while queue:
            path = queue.pop(0)
            node = path[-1]

            if node not in explored:
                neighbors = self.graph[node]
                for neighbor in neighbors:
                    new_path = list(path)
                    new_path.append(neighbor)
                    queue.append(new_path)

                    if neighbor == self.goal:
                        return new_path
                explored.append(node)

        return "path not accessible"
