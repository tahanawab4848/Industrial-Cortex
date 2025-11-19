import random
import itertools

class RouteOptimizer:
    def __init__(self, start_pos, items_dict, distance_callback):
        self.start_pos = start_pos
        self.items = list(items_dict.keys()) # ['A', 'B', 'C']
        self.items_coords = items_dict       # {'A': (2,3), ...}
        self.get_dist = distance_callback    # Function to calculate A* distance

    def calculate_total_distance(self, route):
        """Calculates total cost of a specific route sequence."""
        current_pos = self.start_pos
        total_dist = 0
        
        for item_name in route:
            target_pos = self.items_coords[item_name]
            dist = len(self.get_dist(current_pos, target_pos)) - 1 # -1 because path includes start
            total_dist += dist
            current_pos = target_pos
        return total_dist

    # --- ALGORITHM 1: GREEDY ---
    def greedy_search(self):
        """Always goes to the nearest item next."""
        current_pos = self.start_pos
        remaining_items = self.items[:]
        route = []

        while remaining_items:
            # Find nearest item from current position
            nearest_item = None
            min_dist = float('inf')

            for item in remaining_items:
                path = self.get_dist(current_pos, self.items_coords[item])
                if path and len(path) < min_dist:
                    min_dist = len(path)
                    nearest_item = item
            
            if nearest_item:
                route.append(nearest_item)
                remaining_items.remove(nearest_item)
                current_pos = self.items_coords[nearest_item]
            else:
                break # unreachable
        return route

    # --- ALGORITHM 2: HILL CLIMBING ---
    def hill_climbing(self, iterations=1000):
        """Starts random, makes small swaps, keeps if better."""
        current_route = self.items[:]
        random.shuffle(current_route)
        current_score = self.calculate_total_distance(current_route)

        for _ in range(iterations):
            # Create a neighbor by swapping two random cities
            neighbor = current_route[:]
            i, j = random.sample(range(len(neighbor)), 2)
            neighbor[i], neighbor[j] = neighbor[j], neighbor[i]

            neighbor_score = self.calculate_total_distance(neighbor)
            
            # If neighbor is better (shorter distance), move there
            if neighbor_score < current_score:
                current_route = neighbor
                current_score = neighbor_score
                
        return current_route

    # --- ALGORITHM 3: GENETIC ALGORITHM ---
    def genetic_algorithm(self, population_size=10, generations=50):
        """Simulates evolution to find the best route."""
        
        def create_route():
            r = self.items[:]
            random.shuffle(r)
            return r

        population = [create_route() for _ in range(population_size)]

        for gen in range(generations):
            # Sort population by fitness (shortest distance is best)
            population.sort(key=lambda r: self.calculate_total_distance(r))
            
            # Selection: Keep top 50%
            survivors = population[:population_size//2]
            next_gen = survivors[:]

            # Crossover & Mutation to fill rest
            while len(next_gen) < population_size:
                parent1, parent2 = random.sample(survivors, 2)
                
                # Simple Crossover (Take half from P1, rest from P2)
                split = len(parent1) // 2
                child = parent1[:split] + [item for item in parent2 if item not in parent1[:split]]
                
                # Mutation (Small chance to swap)
                if random.random() < 0.2:
                    i, j = random.sample(range(len(child)), 2)
                    child[i], child[j] = child[j], child[i]
                
                next_gen.append(child)
            
            population = next_gen

        # Return best of final generation
        return min(population, key=lambda r: self.calculate_total_distance(r))