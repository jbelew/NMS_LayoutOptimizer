from optimizer import simulated_annealing_optimization, optimize_placement, print_grid, Grid
from modules_refactored import modules

grid = Grid(
    width=4,
    height=3
)

grid = Grid.from_dict(
    {
        "cells": [
            [
                {"adjacency": False, "adjacency_bonus": 0.0, "bonus": 0.0, "image": None, "module": None, "sc_eligible": False, "supercharged": False, "tech": None, "total": 0.0, "type": "", "value": 0, "active": True, "label": ""},
                {"adjacency": False, "adjacency_bonus": 0.0, "bonus": 0.0, "image": None, "module": None, "sc_eligible": False, "supercharged": False, "tech": None, "total": 0.0, "type": "", "value": 0, "active": True, "label": ""},
                {"adjacency": False, "adjacency_bonus": 0.0, "bonus": 0.0, "image": None, "module": None, "sc_eligible": False, "supercharged": False, "tech": None, "total": 0.0, "type": "", "value": 0, "active": True, "label": ""},
                {"adjacency": False, "adjacency_bonus": 0.0, "bonus": 0.0, "image": None, "module": None, "sc_eligible": False, "supercharged": False, "tech": None, "total": 0.0, "type": "", "value": 0, "active": True, "label": ""},
            ],
            [
                {"adjacency": False, "adjacency_bonus": 0.0, "bonus": 0.0, "image": None, "module": None, "sc_eligible": False, "supercharged": False, "tech": None, "total": 0.0, "type": "", "value": 0, "active": True, "label": ""},
                {"adjacency": False, "adjacency_bonus": 0.0, "bonus": 0.0, "image": None, "module": None, "sc_eligible": False, "supercharged": False, "tech": None, "total": 0.0, "type": "", "value": 0, "active": True, "label": ""},
                {"adjacency": False, "adjacency_bonus": 0.0, "bonus": 0.0, "image": None, "module": None, "sc_eligible": False, "supercharged": False, "tech": None, "total": 0.0, "type": "", "value": 0, "active": True, "label": ""},
                {"adjacency": False, "adjacency_bonus": 0.0, "bonus": 0.0, "image": None, "module": None, "sc_eligible": False, "supercharged": False, "tech": None, "total": 0.0, "type": "", "value": 0, "active": True, "label": ""},
            ],
            [
                {"adjacency": False, "adjacency_bonus": 0.0, "bonus": 0.0, "image": None, "module": None, "sc_eligible": False, "supercharged": False, "tech": None, "total": 0.0, "type": "", "value": 0, "active": True, "label": ""},
                {"adjacency": False, "adjacency_bonus": 0.0, "bonus": 0.0, "image": None, "module": None, "sc_eligible": False, "supercharged": False, "tech": None, "total": 0.0, "type": "", "value": 0, "active": True, "label": ""},
                {"adjacency": False, "adjacency_bonus": 0.0, "bonus": 0.0, "image": None, "module": None, "sc_eligible": False, "supercharged": False, "tech": None, "total": 0.0, "type": "", "value": 0, "active": True, "label": ""},
                {"adjacency": False, "adjacency_bonus": 0.0, "bonus": 0.0, "image": None, "module": None, "sc_eligible": False, "supercharged": False, "tech": None, "total": 0.0, "type": "", "value": 0, "active": True, "label": ""}
            ]
        ],
        "height": 3,
        "width": 4
    }
)

#grid, max_bonus = simulated_annealing_optimization(grid, "Exotic", modules, "infra", initial_temp=5000, cooling_rate=0.9999, max_iterations=20000, patience=500, decay_factor=0.995)
grid, max_bonus = optimize_placement(grid, "Exotic", modules, "infra")

print("Optimized layout --" + str(max_bonus))
print_grid(grid)