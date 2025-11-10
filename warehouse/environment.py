import random
import os

class WarehouseGrid:
    def __init__(self, width=10, height=10, obstacle_count=15):
        self.width = width
        self.height = height
        self.grid = [['.' for _ in range(width)] for _ in range(height)]
        self.obstacles = set()
        self.items = {}
        self.robot_pos = (0, 0)
        self.generate_obstacles(obstacle_count)

    def generate_obstacles(self, count):
        """Randomly places obstacles (X) on the grid."""
        while len(self.obstacles) < count:
            x, y = random.randint(0, self.width-1), random.randint(0, self.height-1)
            # Keep (0,0) clear for the robot
            if (x, y) != (0, 0):
                self.obstacles.add((x, y))
                self.grid[y][x] = '#'

    def add_items(self, items_dict):
        """Place items (A, B, C...) on the map."""
        self.items = items_dict
        for name, (x, y) in items_dict.items():
            if (x, y) in self.obstacles:
                self.obstacles.remove((x, y)) # Remove obstacle if item spawns there
            self.grid[y][x] = name

    def is_valid(self, x, y):
        """Check if a coordinate is within bounds and not an obstacle."""
        return 0 <= x < self.width and 0 <= y < self.height and (x, y) not in self.obstacles

    def display(self, path=None):
        """Renders the grid to the console. Optionally overlays a path."""
        print("-" * (self.width * 2 + 2))
        temp_grid = [row[:] for row in self.grid]
        
        # Mark path
        if path:
            for (px, py) in path:
                if temp_grid[py][px] in ['.', 'S']:
                    temp_grid[py][px] = '*'

        # Mark Robot
        rx, ry = self.robot_pos
        temp_grid[ry][rx] = 'R'

        for row in temp_grid:
            print("|" + " ".join(row) + "|")
        print("-" * (self.width * 2 + 2))