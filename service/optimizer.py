import random
import math
import copy

from itertools import permutations
from flask import Flask, request, jsonify

from service.models.modules import modules


class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = [
            [
                {
                    "module": None,
                    "value": 0,
                    "type": "",
                    "total": 0.0,
                    "adjacency_bonus": 0.0,
                    "bonus": 0.0,
                    "active": True,
                    "adjacency": False,
                    "tech": None,
                    "supercharged": False,
                    "sc_eligible": False,
                    "image": None,
                }
                for _ in range(width)
            ]
            for _ in range(height)
        ]

    def get_cell(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.cells[y][x]
        else:
            raise IndexError("Cell out of bounds")

    def set_cell(self, x, y, value):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.cells[y][x]["value"] = value
        else:
            raise IndexError("Cell out of bounds")

    def set_supercharged(self, x, y, value):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.cells[y][x]["supercharged"] = value
        else:
            raise IndexError("Cell out of bounds")

    def set_active(self, x, y, value):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.cells[y][x]["active"] = value
        else:
            raise IndexError("Cell out of bounds")

    def is_supercharged(self, x, y):
        return self.get_cell(x, y)["supercharged"]

    def set_adjacency_bonus(self, x, y, bonus):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.cells[y][x]["adjacency_bonus"] = bonus
        else:
            raise IndexError("Cell out of bounds")

    def set_bonus(self, x, y, bonus):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.cells[y][x]["bonus"] = bonus
        else:
            raise IndexError("Cell out of bounds")

    def set_type(self, x, y, type):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.cells[y][x]["type"] = type
        else:
            raise IndexError("Cell out of bounds")

    def set_value(self, x, y, value):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.cells[y][x]["value"] = value
        else:
            raise IndexError("Cell out of bounds")

    def set_total(self, x, y, total):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.cells[y][x]["total"] = total
        else:
            raise IndexError("Cell out of bounds")

    def set_module(self, x, y, module):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.cells[y][x]["module"] = module
        else:
            raise IndexError("Cell out of bounds")

    def set_adjacency(self, x, y, adjacency):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.cells[y][x]["adjacency"] = adjacency
        else:
            raise IndexError("Cell out of bounds")

    def set_tech(self, x, y, tech):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.cells[y][x]["tech"] = tech
        else:
            raise IndexError("Cell out of bounds")

    def set_sc_eligible(self, x, y, sc_eligible):
        """Set whether the cell at (x, y) is eligible for supercharging."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.cells[y][x]["sc_eligible"] = sc_eligible
        else:
            raise IndexError("Cell out of bounds")

    def set_image(self, x, y, image):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.cells[y][x]["image"] = image
        else:
            raise IndexError("Cell out of bounds")

    def to_dict(self):
        """Convert the grid into a JSON-serializable dictionary."""
        return {"width": self.width, "height": self.height, "cells": self.cells}

    @classmethod
    def from_dict(cls, data: dict) -> "Grid":
        """Create a Grid instance from a dictionary."""
        grid = cls(data["width"], data["height"])
        for y, row in enumerate(data["cells"]):
            for x, cell_data in enumerate(row):
                cell = grid.get_cell(x, y)
                cell.update(
                    {
                        "module": cell_data["module"],
                        "value": cell_data["value"],
                        "type": cell_data["type"],
                        "total": cell_data["total"],
                        "active": cell_data["active"],
                        "adjacency_bonus": cell_data["adjacency_bonus"],
                        "bonus": cell_data["bonus"],
                        "adjacency": cell_data["adjacency"],
                        "tech": cell_data["tech"],
                        "supercharged": cell_data["supercharged"],
                        "sc_eligible": cell_data["sc_eligible"],
                        "image": cell_data["image"],
                    }
                )
        return grid

    def __str__(self):
        """Generate a string representation of the grid."""
        return "\n".join(
            " ".join("." if cell["value"] == 0 else str(cell["value"]) for cell in row)
            for row in self.cells
        )


def optimize_placement(grid, modules, tech):
    optimal_grid = None
    highest_bonus = 0.0
    iteration = 0

    # Filter modules based on tech
    tech_modules = [module for module in modules if module["tech"] == tech]

    # Separate core and bonus modules
    core_modules = [module for module in tech_modules if module["type"] == "core"]
    bonus_modules = [module for module in tech_modules if module["type"] == "bonus"]

    if not bonus_modules or not core_modules:
        raise ValueError("No bonus or core modules specified")

    # Find all valid positions in the grid
    available_positions = [
        (x, y)
        for y in range(grid.height)
        for x in range(grid.width)
        if grid.get_cell(x, y)["module"] is None and grid.get_cell(x, y)["active"]
    ]

    for core_position in available_positions:
        for bonus_placement in permutations(available_positions, len(bonus_modules)):
            temp_grid = Grid.from_dict(grid.to_dict())  # changed to from_dict

            # Place the core module
            core_x, core_y = core_position
            core_module = core_modules[0]
            place_module(
                temp_grid,
                core_x,
                core_y,
                core_module["name"],
                core_module["tech"],
                core_module["type"],
                core_module["bonus"],
                core_module["adjacency"],
                core_module["sc_eligible"],
                core_module["image"],
            )

            # Place the bonus modules
            for index, bonus_position in enumerate(bonus_placement):
                x, y = bonus_position
                if temp_grid.get_cell(x, y)["module"] is not None:
                    continue
                bonus_module = bonus_modules[index]
                place_module(
                    temp_grid,
                    x,
                    y,
                    bonus_module["name"],
                    bonus_module["tech"],
                    bonus_module["type"],
                    bonus_module["bonus"],
                    bonus_module["adjacency"],
                    bonus_module["sc_eligible"],
                    bonus_module["image"],
                )

            # Calculate total bonus for the core module
            populate_adjacency_bonuses(temp_grid, tech)
            populate_module_bonuses(temp_grid, tech)
            core_bonus = populate_core_bonus(temp_grid, tech)

            # Update optimal placement if current bonus is higher
            iteration += 1

            if core_bonus > highest_bonus:
                highest_bonus = core_bonus
                optimal_grid = Grid.from_dict(
                    temp_grid.to_dict()
                )  # changed to from_dict

    return optimal_grid, highest_bonus


def simulated_annealing_optimization(
    grid,
    modules,
    tech,
    initial_temp=8000,
    cooling_rate=0.9997,
    max_iterations=200000,
    patience=500,
    decay_factor=0.995,
    max_supercharged=4,
):  # New constraint parameter
    best_grid = Grid.from_dict(grid.to_dict())  # changed to from_dict
    best_bonus = -float("inf")

    current_grid = Grid.from_dict(grid.to_dict())  # changed to from_dict

    temperature = initial_temp
    iteration_without_improvement = (
        0  # Track the number of iterations without improvement
    )

    for iteration in range(max_iterations):
        # Generate a neighbor solution by randomly changing the placement of modules
        neighbor_grid = generate_neighbor_grid_with_movement(
            current_grid, modules, tech, temperature, initial_temp, max_supercharged
        )

        # Ensure neighbor grid does not exceed max_supercharged
        if count_supercharged_slots(neighbor_grid, tech) > max_supercharged:
            continue  # Skip this iteration if it exceeds the limit

        # Calculate the bonus for the neighbor grid
        populate_adjacency_bonuses(neighbor_grid, tech)
        populate_module_bonuses(neighbor_grid, tech)
        neighbor_bonus = populate_core_bonus(neighbor_grid, tech)

        # If the neighbor solution is better, accept it and copy the grid to the best grid
        if neighbor_bonus > best_bonus:
            best_bonus = neighbor_bonus
            best_grid = Grid.from_dict(neighbor_grid.to_dict())  # changed to from_dict
            iteration_without_improvement = 0  # Reset improvement counter
        else:
            iteration_without_improvement += 1

        # Calculate energy difference
        energy_diff = neighbor_bonus - populate_core_bonus(current_grid, tech)

        # If the new solution is worse, decide whether to accept it based on temperature
        if energy_diff < 0:
            acceptance_probability = math.exp(energy_diff / temperature)
            if random.random() < acceptance_probability:
                current_grid = Grid.from_dict(
                    neighbor_grid.to_dict()
                )  # changed to from_dict

        if iteration_without_improvement >= patience:
            temperature *= decay_factor
            iteration_without_improvement = 0

        # Decrease temperature using the cooling rate
        temperature *= cooling_rate

        # Print progress
        # if iteration % 100 == 0:
        #     print(f"simulated_annealing_optimization - tech: {tech} - Iteration {iteration}/{max_iterations}, Temp: {temperature:.2f}, Best Bonus: {best_bonus:.2f}, Cooling Rate: {cooling_rate:.4f}")

    return best_grid, best_bonus


def generate_neighbor_grid_with_movement(
    grid, modules, tech, temperature, initial_temp, max_supercharged
):
    """Generate a new grid by modifying the existing grid with new module placements while enforcing a supercharged slot limit."""
    neighbor_grid = Grid.from_dict(grid.to_dict())

    tech_modules = [module for module in modules if module["tech"] == tech]
    core_modules = [module for module in tech_modules if module["type"] == "core"]
    bonus_modules = [module for module in tech_modules if module["type"] == "bonus"]

    occupied_positions = [
        (x, y)
        for y in range(grid.height)
        for x in range(grid.width)
        if neighbor_grid.get_cell(x, y)["module"] is not None
        and neighbor_grid.get_cell(x, y)["tech"] == tech
    ]
    available_positions = [
        (x, y)
        for y in range(grid.height)
        for x in range(grid.width)
        if neighbor_grid.get_cell(x, y)["module"] is None
        and neighbor_grid.get_cell(x, y)["active"]
    ]

    move_count = max(
        1, int(5 * (temperature / initial_temp))
    )  # More moves when temp is high

    if not occupied_positions:
        random.shuffle(available_positions)
        for core_module in core_modules:
            if available_positions:
                x, y = available_positions.pop()
                place_module(
                    neighbor_grid,
                    x,
                    y,
                    core_module["name"],
                    core_module["tech"],
                    core_module["type"],
                    core_module["bonus"],
                    core_module["adjacency"],
                    core_module["sc_eligible"],
                    core_module["image"],
                )

        for bonus_module in bonus_modules:
            if (
                available_positions
                and count_supercharged_slots(neighbor_grid, tech) < max_supercharged
            ):
                x, y = available_positions.pop()
                place_module(
                    neighbor_grid,
                    x,
                    y,
                    bonus_module["name"],
                    bonus_module["tech"],
                    bonus_module["type"],
                    bonus_module["bonus"],
                    bonus_module["adjacency"],
                    bonus_module["sc_eligible"],
                    bonus_module["image"],
                )
    else:
        for _ in range(move_count):
            if not occupied_positions:
                break
            old_x, old_y = random.choice(occupied_positions)
            occupied_positions.remove((old_x, old_y))
            old_cell = neighbor_grid.get_cell(old_x, old_y)
            old_module = old_cell["module"]

            place_module(
                neighbor_grid, old_x, old_y, None, None, None, 0, False, False, None
            )

            if available_positions:
                new_x, new_y = random.choice(available_positions)
                available_positions.remove((new_x, new_y))

                # Enforce supercharged slot limit when placing a module
                is_supercharged = (
                    old_cell["supercharged"]
                    and count_supercharged_slots(neighbor_grid, tech) < max_supercharged
                )

                place_module(
                    neighbor_grid,
                    new_x,
                    new_y,
                    old_module,
                    old_cell["tech"],
                    old_cell["type"],
                    old_cell["bonus"],
                    old_cell["adjacency"],
                    is_supercharged,
                    old_cell["image"],
                )

    return neighbor_grid


def count_supercharged_slots(grid, tech):
    count = 0
    for y in range(grid.height):
        for x in range(grid.width):
            if (
                grid.get_cell(x, y)["supercharged"]
                and grid.get_cell(x, y)["tech"] == tech
            ):
                count += 1
    return count


def place_module(grid, x, y, module, tech, type, bonus, adjacency, sc_eligible, image):
    grid.set_module(x, y, module)
    grid.set_tech(x, y, tech)
    grid.set_type(x, y, type)
    grid.set_bonus(x, y, bonus)
    grid.set_adjacency(x, y, adjacency)
    grid.set_sc_eligible(x, y, sc_eligible)
    grid.set_image(x, y, image)


def calculate_adjacency_bonus(grid, x, y):
    cell = grid.get_cell(x, y)
    if not cell["adjacency"]:
        return 0.0

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Only orthogonal directions
    adjacency_bonus = 0.0

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < grid.width and 0 <= ny < grid.height:
            neighbor = grid.get_cell(nx, ny)
            if neighbor["module"] is not None and neighbor["tech"] == cell["tech"]:
                if neighbor["adjacency"] is True:
                    adjacency_bonus += 0.1
                    grid.set_adjacency_bonus(x, y, adjacency_bonus)

    return adjacency_bonus


def populate_adjacency_bonuses(grid, tech):
    for row in range(grid.height):
        for col in range(grid.width):
            current_cell = grid.get_cell(col, row)
            if current_cell["module"] is not None and current_cell["tech"] == tech:
                calculate_adjacency_bonus(grid, col, row)


def calculate_module_bonus(grid, x, y):
    cell = grid.get_cell(x, y)
    base_bonus = cell["bonus"]
    adjacency_bonus = cell["adjacency_bonus"]
    is_supercharged = cell["supercharged"]
    is_sc_eligible = cell["sc_eligible"]

    total_bonus = base_bonus + adjacency_bonus
    if is_supercharged & is_sc_eligible == True:
        total_bonus *= 1.25

    grid.set_total(x, y, total_bonus)
    return total_bonus


def populate_module_bonuses(grid, tech):
    for row in range(grid.height):
        for col in range(grid.width):
            current_cell = grid.get_cell(col, row)
            if current_cell["type"] == "bonus" and current_cell["tech"] == tech:
                calculate_module_bonus(grid, col, row)


def calculate_core_bonus(grid, tech):
    """
    Calculate the core bonus by summing the total bonus of all bonus modules and adding in the core module's total.
    """
    bonus_total = 0
    core_total = 0

    for row in range(grid.height):
        for col in range(grid.width):
            cell = grid.get_cell(col, row)
            if cell["type"] == "bonus" and cell["tech"] == tech:
                bonus_total += cell["total"]
            elif cell["type"] == "core" and cell["tech"] == tech:
                core_total = cell["bonus"] + cell["adjacency_bonus"]

    return bonus_total + core_total


def populate_core_bonus(grid, tech):
    core_bonus = calculate_core_bonus(grid, tech)
    final_bonus = 0
    for row in range(grid.height):
        for col in range(grid.width):
            cell = grid.get_cell(col, row)
            if cell["type"] == "core" and cell["tech"] == tech:
                final_bonus = core_bonus
                grid.set_total(col, row, final_bonus)

    return final_bonus


def print_grid(grid):
    """Display the grid with module info, total value, and active state (+/-) instead of '.'."""
    # Format and print the grid
    for y, row in enumerate(grid.cells):
        formatted_row = []

        for x, cell in enumerate(row):
            cell_data = copy.deepcopy(
                grid.get_cell(x, y)
            )  # make a copy of the data to ensure we don't modify it
            is_supercharged = cell_data["supercharged"]
            is_shield = cell_data["tech"] == "shield"
            is_infra = cell_data["tech"] == "infra"
            active_state = (
                " +" if cell_data["active"] else " -"
            )  # what to show if there is no module

            formatted_row.append(
                f"\033[93m{active_state if cell_data['module'] is None else cell_data['module']} (T: {cell_data['total']:.2f}) (B: {cell_data['bonus']:.2f}) (A: {cell_data['adjacency_bonus']:.2f})\033[0m"
                if is_supercharged
                else (
                    f"\033[96m{active_state if cell_data['module'] is None else cell_data['module']} (T: {cell_data['total']:.2f}) (B: {cell_data['bonus']:.2f}) (A: {cell_data['adjacency_bonus']:.2f})\033[0m"
                    if is_shield
                    else (
                        f"\033[91m{active_state if cell_data['module'] is None else cell_data['module']} (T: {cell_data['total']:.2f}) (B: {cell_data['bonus']:.2f}) (A: {cell_data['adjacency_bonus']:.2f})\033[0m"
                        if is_infra
                        else f"{active_state if cell_data['module'] is None else cell_data['module']} (T: {cell_data['total']:.2f}) (B: {cell_data['bonus']:.2f}) (A: {cell_data['adjacency_bonus']:.2f})"
                    )
                )
            )
        print(" | ".join(formatted_row))
    print()
