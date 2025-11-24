import tkinter as tk
from tkinter import ttk, messagebox
import time
import threading

# Import your existing logic
from warehouse.environment import WarehouseGrid
from warehouse.pathfinding import PathFinder
from warehouse.optimizer import RouteOptimizer

class WarehouseGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Intelligent Warehouse Robot - AI Simulation")
        self.root.geometry("900x700")
        self.root.configure(bg="#2c3e50")

        # --- Configuration ---
        self.cell_size = 40
        self.grid_width = 15
        self.grid_height = 12
        self.animation_speed = 150 # ms per step

        # --- Logic Objects ---
        self.grid_obj = None
        self.pf = None
        self.optimizer = None
        self.tasks = {}
        
        # --- UI Layout ---
        self.create_sidebar()
        self.create_canvas()
        
        # Initialize the first map
        self.generate_new_map()

    def create_sidebar(self):
        """Creates the control panel on the left."""
        frame = tk.Frame(self.root, width=250, bg="#34495e", padx=20, pady=20)
        frame.pack(side=tk.LEFT, fill=tk.Y)
        frame.pack_propagate(False)

        # Title
        tk.Label(frame, text="Control Panel", font=("Arial", 16, "bold"), 
                 bg="#34495e", fg="white").pack(pady=(0, 20))

        # Algorithm Selection
        tk.Label(frame, text="Optimization Algo:", bg="#34495e", fg="#bdc3c7").pack(anchor="w")
        self.algo_var = tk.StringVar(value="Genetic Algorithm")
        algo_menu = ttk.Combobox(frame, textvariable=self.algo_var, state="readonly")
        algo_menu['values'] = ("Greedy Search", "Hill Climbing", "Genetic Algorithm")
        algo_menu.pack(fill=tk.X, pady=(0, 20))

        # Buttons
        self.btn_run = tk.Button(frame, text="▶ Run Simulation", bg="#27ae60", fg="white", 
                                 font=("Arial", 12, "bold"), command=self.start_simulation)
        self.btn_run.pack(fill=tk.X, pady=5)

        tk.Button(frame, text="↻ Generate New Map", bg="#e67e22", fg="white", 
                  font=("Arial", 11), command=self.generate_new_map).pack(fill=tk.X, pady=5)

        # Status Log
        tk.Label(frame, text="Mission Log:", bg="#34495e", fg="#bdc3c7").pack(anchor="w", pady=(20, 5))
        self.log_text = tk.Text(frame, height=15, width=25, bg="#2c3e50", fg="#ecf0f1", 
                                font=("Consolas", 9), state="disabled")
        self.log_text.pack(fill=tk.BOTH, expand=True)

    def create_canvas(self):
        """Creates the drawing area for the grid."""
        right_frame = tk.Frame(self.root, bg="#2c3e50")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Center the canvas
        self.canvas = tk.Canvas(right_frame, bg="white", highlightthickness=0)
        self.canvas.pack(anchor="center", expand=True)

    def log(self, message):
        """Adds text to the log window."""
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, "> " + message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")

    def generate_new_map(self):
        """Resets the environment with new random obstacles."""
        self.grid_obj = WarehouseGrid(width=self.grid_width, height=self.grid_height, obstacle_count=35)
        
        # Define tasks (Items A-E)
        import random
        self.tasks = {}
        possible_letters = ['A', 'B', 'C', 'D', 'E']
        
        # Randomly place items away from obstacles
        count = 0
        while count < 5:
            rx, ry = random.randint(0, self.grid_width-1), random.randint(0, self.grid_height-1)
            if self.grid_obj.is_valid(rx, ry) and (rx, ry) != (0,0) and (rx, ry) not in self.tasks.values():
                self.tasks[possible_letters[count]] = (rx, ry)
                count += 1
                
        self.grid_obj.add_items(self.tasks)
        self.pf = PathFinder(self.grid_obj)
        self.optimizer = RouteOptimizer(self.grid_obj.robot_pos, self.tasks, self.pf.a_star)
        
        self.draw_grid()
        self.log("New Map Generated.")
        self.log(f"Tasks: {', '.join(self.tasks.keys())}")

    def draw_grid(self):
        """Redraws the entire visual grid."""
        self.canvas.delete("all")
        
        # Resize canvas to fit grid
        w = self.grid_width * self.cell_size
        h = self.grid_height * self.cell_size
        self.canvas.config(width=w, height=h)

        for y in range(self.grid_height):
            for x in range(self.grid_width):
                x1 = x * self.cell_size
                y1 = y * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                # Determine color
                fill_color = "#ecf0f1" # Empty floor
                outline_color = "#bdc3c7"
                
                if (x, y) in self.grid_obj.obstacles:
                    fill_color = "#34495e" # Obstacle
                
                # Draw Cell
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color, outline=outline_color)

                # Draw Items
                for name, pos in self.tasks.items():
                    if (x, y) == pos:
                        self.canvas.create_oval(x1+5, y1+5, x2-5, y2-5, fill="#e74c3c", outline="")
                        self.canvas.create_text((x1+x2)/2, (y1+y2)/2, text=name, fill="white", font=("Arial", 10, "bold"))

        # Draw Robot
        rx, ry = self.grid_obj.robot_pos
        self.draw_robot(rx, ry)

    def draw_robot(self, x, y):
        """Draws the robot at a specific grid coordinate."""
        self.canvas.delete("robot") # Remove old robot
        x1 = x * self.cell_size
        y1 = y * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        self.canvas.create_rectangle(x1+5, y1+5, x2-5, y2-5, fill="#3498db", outline="", tags="robot")
        self.canvas.create_text((x1+x2)/2, (y1+y2)/2, text="🤖", tags="robot")

    def start_simulation(self):
        """Calculates path and starts animation."""
        self.btn_run.config(state="disabled")
        self.log("Computing Optimal Route...")
        
        # Run in separate thread to not freeze GUI during calculation
        threading.Thread(target=self.run_logic, daemon=True).start()

    def run_logic(self):
        """The AI Logic Execution."""
        selected_algo = self.algo_var.get()
        
        # 1. Optimize Order
        if selected_algo == "Greedy Search":
            route = self.optimizer.greedy_search()
        elif selected_algo == "Hill Climbing":
            route = self.optimizer.hill_climbing()
        else:
            route = self.optimizer.genetic_algorithm()
            
        self.root.after(0, lambda: self.log(f"Optimal Order: {' -> '.join(route)}"))

        # 2. Build Step-by-Step Path
        full_path = []
        current_pos = self.grid_obj.robot_pos
        
        for target_item in route:
            target_coords = self.tasks[target_item]
            path_segment = self.pf.a_star(current_pos, target_coords)
            
            if path_segment:
                full_path.extend(path_segment)
                current_pos = target_coords
            else:
                self.root.after(0, lambda: self.log(f"Error: No path to {target_item}"))
                break

        # 3. Trigger Animation on Main Thread
        self.root.after(0, lambda: self.animate_path(full_path))

    def animate_path(self, path_list):
        """Recursively moves the robot step by step."""
        if not path_list:
            self.log("Mission Complete!")
            self.btn_run.config(state="normal")
            return

        next_pos = path_list.pop(0)
        self.grid_obj.robot_pos = next_pos
        self.draw_robot(next_pos[0], next_pos[1])
        
        # Check if we landed on an item (just for visual log)
        for name, pos in self.tasks.items():
            if next_pos == pos:
                self.log(f"Picked up Item {name}")

        # Schedule next step
        self.root.after(self.animation_speed, lambda: self.animate_path(path_list))

if __name__ == "__main__":
    root = tk.Tk()
    app = WarehouseGUI(root)
    root.mainloop()