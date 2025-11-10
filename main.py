import time
from warehouse.environment import WarehouseGrid
from warehouse.pathfinding import PathFinder
from warehouse.optimizer import RouteOptimizer

def main():
    print("==========================================")
    print(" INTELLIGENT WAREHOUSE ROBOT SYSTEM ")
    print("==========================================\n")

    # 1. Setup Environment
    print("[INFO] Initializing Warehouse Grid...")
    grid = WarehouseGrid(width=15, height=10, obstacle_count=30)
    
    # Define tasks (Items to pick up)
    tasks = {
        'A': (1, 8), 'B': (13, 1), 'C': (10, 8), 
        'D': (5, 5), 'E': (12, 7)
    }
    grid.add_items(tasks)
    grid.display()

    # 2. Setup Modules
    pf = PathFinder(grid)
    
    # We pass the A* function to the optimizer so it knows true travel distances
    optimizer = RouteOptimizer(grid.robot_pos, tasks, pf.a_star)

    # 3. Optimization Phase
    print("\n[INFO] Calculating optimal route order...")
    
    # -- Greedy --
    start_time = time.time()
    greedy_route = optimizer.greedy_search()
    print(f"-> Greedy Route: {greedy_route} (Time: {time.time()-start_time:.4f}s)")
    
    # -- Hill Climbing --
    start_time = time.time()
    hc_route = optimizer.hill_climbing()
    print(f"-> Hill Climbing Route: {hc_route} (Time: {time.time()-start_time:.4f}s)")

    # -- Genetic Algo --
    start_time = time.time()
    ga_route = optimizer.genetic_algorithm()
    print(f"-> Genetic Algo Route: {ga_route} (Time: {time.time()-start_time:.4f}s)")

    # Select the Genetic Algorithm result for the final demo
    final_route = ga_route
    print(f"\n[DECISION] Executing Route: {final_route}")

    # 4. Execution Phase
    current_pos = grid.robot_pos
    full_path = []
    
    for target_item in final_route:
        target_coords = tasks[target_item]
        print(f"\n[NAVIGATING] Robot moving from {current_pos} to Item {target_item} {target_coords} using A*...")
        
        path_segment = pf.a_star(current_pos, target_coords)
        
        if path_segment:
            full_path.extend(path_segment)
            grid.robot_pos = target_coords
            current_pos = target_coords
            grid.display(path=path_segment)
            print(f"   -> Reached Item {target_item}!")
            time.sleep(1) # Pause for effect
        else:
            print(f"   -> ERROR: Path to {target_item} is blocked!")
            break

    print("\n[MISSION COMPLETE] All items collected.")

if __name__ == "__main__":
    main()