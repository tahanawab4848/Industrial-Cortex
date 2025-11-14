import heapq
from collections import deque

class PathFinder:
    def __init__(self, grid_obj):
        self.grid = grid_obj

    def get_neighbors(self, node):
        x, y = node
        # Up, Down, Left, Right movements
        movements = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        result = []
        for dx, dy in movements:
            nx, ny = x + dx, y + dy
            if self.grid.is_valid(nx, ny):
                result.append((nx, ny))
        return result

    def bfs(self, start, goal):
        """Breadth-First Search: Guarantees shortest path in unweighted grid."""
        queue = deque([(start, [start])])
        visited = set([start])

        while queue:
            (current, path) = queue.popleft()
            if current == goal:
                return path

            for neighbor in self.get_neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        return None

    def a_star(self, start, goal):
        """A* Search: Best for intelligent pathfinding using heuristics."""
        def heuristic(a, b):
            # Manhattan distance
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        # Priority Queue: (priority, current_node, path_so_far)
        pq = [(0, start, [start])]
        visited = set()
        cost_so_far = {start: 0}

        while pq:
            _, current, path = heapq.heappop(pq)

            if current == goal:
                return path

            if current in visited:
                continue
            visited.add(current)

            for neighbor in self.get_neighbors(current):
                new_cost = cost_so_far[current] + 1
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + heuristic(neighbor, goal)
                    heapq.heappush(pq, (priority, neighbor, path + [neighbor]))
        return None