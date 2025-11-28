# 🤖 Industrial Cortex (Intelligent Warehouse Robot - AI Simulation)

Welcome to the **Industrial Cortex** project! This project simulates an autonomous robotic agent navigating a grid-based warehouse to efficiently collect a set of scattered items. It leverages foundational Artificial Intelligence concepts, integrating **A* Pathfinding** for navigation and various **Optimization Algorithms** to solve the traveling salesperson-style routing problem.

---

## 🌟 Key Features

* **Grid-Based Environment (`warehouse.environment`)**: A dynamically generated warehouse floor map with random obstacles.
* **A* Pathfinding (`warehouse.pathfinding`)**: Ensures the robot finds the shortest collision-free path between any two points in the warehouse.
* **Route Optimization (`warehouse.optimizer`)**: Determines the best order to pick up the items using three different algorithms:
  * **Greedy Search**: Fast, heuristic-based nearest-neighbor approach.
  * **Hill Climbing**: Local search optimization to iteratively improve the route.
  * **Genetic Algorithm**: Evolutionary approach that breeds the best routes to find a near-global optimum.
* **Dual Interface**:
  * **CLI Mode (`main.py`)**: A terminal-based simulation comparing the execution times of all three algorithms.
  * **GUI Mode (`gui_app.py`)**: An interactive Tkinter-based dashboard to visualize the algorithms, watch the robot animate step-by-step, and generate new warehouse maps on the fly.

---

## 🛠️ Technologies Used

* **Language**: Python 3.x
* **GUI Framework**: Tkinter (Standard Python library)
* **Algorithms**: A* Search, Genetic Algorithms, Hill Climbing, Greedy Algorithms

---

## 📂 Project Structure

```text
AI_project/
├── main.py                  # CLI benchmark and execution script
├── gui_app.py               # Interactive Graphical User Interface
├── .gitignore               # Git ignore file for pycache and scripts
└── warehouse/               # Core AI modules package
    ├── __init__.py          
    ├── environment.py       # Manages the grid, obstacles, and item placement
    ├── pathfinding.py       # Implements the A* search algorithm
    └── optimizer.py         # Implements Greedy, Hill Climbing, and Genetic Algos
```
*(Note: `warehouse/README.txt` currently contains GUI codebase logic as a backup/reference.)*

---

## 🚀 How to Run

### 1. Run the GUI Simulation (Recommended)
Watch the robot navigate the warehouse in real-time!
```bash
python gui_app.py
```
* **Features**: Generate new maps, select an optimization algorithm from the sidebar, and click "Run Simulation" to watch the robot collect items.

### 2. Run the CLI Benchmark
To see a text-based output comparing the execution times and results of the different routing algorithms:
```bash
python main.py
```

---

## 🧠 How It Works
1. The **Environment** generates a `15x12` grid with obstacles and 5 target items.
2. The **Route Optimizer** uses the A* algorithm to pre-compute the true travel distance between all items.
3. The selected **Algorithm** (Greedy, Hill Climbing, or Genetic) calculates the most efficient order to visit the nodes.
4. Finally, the **Pathfinder** guides the robot step-by-step along that optimal route!

---
*Created as an AI pathfinding and optimization project.*
