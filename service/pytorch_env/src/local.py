# local.py
from optimizer import (
    simulated_annealing_optimization,
    optimize_placement,
    print_grid,
    print_grid_compact,
    Grid,
)
from modules_refactored import modules

# Define the grid dimensions
grid_width = 4
grid_height = 3

# Create a new grid
grid = Grid(width=grid_width, height=grid_height)

# Define the initial grid configuration (optional)
initial_grid_config = {
    "cells": [
        [
            {
                "adjacency": False,
                "adjacency_bonus": 0.0,
                "bonus": 0.0,
                "image": None,
                "module": None,
                "sc_eligible": False,
                "supercharged": False,
                "tech": None,
                "total": 0.0,
                "type": "",
                "value": 0,
                "active": True,
                "label": "",
            }
            for _ in range(grid_width)
        ]
        for _ in range(grid_height)
    ],
    "height": grid_height,
    "width": grid_width,
}

# Set supercharged slots in the initial grid (optional)
supercharged_positions = [(1, 0), (3, 0)]  # Example: (x, y) coordinates
for x, y in supercharged_positions:
    initial_grid_config["cells"][y][x]["supercharged"] = True

# Load the initial grid configuration
grid = Grid.from_dict(initial_grid_config)

# Define the optimization parameters
ship = "Exotic"
tech = "infra"
initial_temp = 8000
cooling_rate = 0.9997
max_iterations = 20000
patience = 500
decay_factor = 0.995

# Run the simulated annealing optimization
# grid, max_bonus = simulated_annealing_optimization(
#     grid,
#     ship,
#     modules,
#     tech,
#     initial_temp=initial_temp,
#     cooling_rate=cooling_rate,
#     max_iterations=max_iterations,
#     patience=patience,
#     decay_factor=decay_factor,
# )

# Print the results
#print(f"Optimized layout for {ship} ({tech}) -- Max Bonus: {max_bonus}")
#print_grid_compact(grid)

# Alternative: Run the brute-force optimization (uncomment to use)
grid, max_bonus = optimize_placement(grid, ship, modules, tech)
print(f"Optimized layout (brute-force) for {ship} ({tech}) -- Max Bonus: {max_bonus}")
print_grid(grid)
