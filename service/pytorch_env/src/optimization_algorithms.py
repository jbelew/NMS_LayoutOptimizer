import random
import math
from grid_utils import Grid
from modules_data import get_tech_modules, get_tech_modules_for_training
from bonus_calculations import (
    populate_adjacency_bonuses,
    populate_module_bonuses,
    populate_core_bonus,
    calculate_potential_adjacency_bonus,
    count_supercharged_slots,
)
from module_placement import place_module
from itertools import permutations


def optimize_placement(grid, ship, modules, tech):
    optimal_grid = None
    highest_bonus = 0.0
    tech_modules = get_tech_modules(modules, ship, tech)
    core_modules = [module for module in tech_modules if module["type"] == "core"]
    bonus_modules = [module for module in tech_modules if module["type"] == "bonus"]
    if not core_modules:
        raise ValueError("No core modules specified")
    available_positions = [
        (x, y)
        for y in range(grid.height)
        for x in range(grid.width)
        if grid.get_cell(x, y)["module"] is None and grid.get_cell(x, y)["active"]
    ]
    for core_position in available_positions:
        bonus_permutations = (
            [permutations(available_positions, len(bonus_modules))]
            if bonus_modules
            else [[]]
        )
        for bonus_placement in bonus_permutations[0]:
            temp_grid = Grid.from_dict(grid.to_dict())
            core_x, core_y = core_position
            core_module = core_modules[0]
            place_module(
                temp_grid,
                core_x,
                core_y,
                core_module["id"],
                core_module["label"],
                tech,
                core_module["type"],
                core_module["bonus"],
                core_module["adjacency"],
                core_module["sc_eligible"],
                core_module["image"],
            )
            for index, bonus_position in enumerate(bonus_placement):
                x, y = bonus_position
                if temp_grid.get_cell(x, y)["module"] is not None:
                    continue
                bonus_module = bonus_modules[index]
                place_module(
                    temp_grid,
                    x,
                    y,
                    bonus_module["id"],
                    bonus_module["label"],
                    tech,
                    bonus_module["type"],
                    bonus_module["bonus"],
                    bonus_module["adjacency"],
                    bonus_module["sc_eligible"],
                    bonus_module["image"],
                )
            populate_adjacency_bonuses(temp_grid, tech)
            populate_module_bonuses(temp_grid, tech)
            core_bonus = populate_core_bonus(temp_grid, tech)
            if core_bonus > highest_bonus:
                highest_bonus = core_bonus
                optimal_grid = Grid.from_dict(temp_grid.to_dict())
    return optimal_grid, highest_bonus


def simulated_annealing_optimization(
    grid,
    ship,
    modules,
    tech,
    initial_temp=100,
    cooling_rate=0.999,
    max_iterations=20000,
    patience=200,
    decay_factor=0.995,
    restart_probability=0.05,
    stagnation_threshold=1000,
    max_supercharged=4,
):
    best_grid = Grid.from_dict(grid.to_dict())
    best_bonus = -float("inf")
    current_grid = Grid.from_dict(grid.to_dict())
    temperature = initial_temp
    iteration_without_improvement = 0
    stagnation_counter = 0
    num_acceptances = 0
    total_iterations = 0
    for iteration in range(max_iterations):
        total_iterations += 1
        neighbor_grid = generate_neighbor_grid_with_movement(
            current_grid,
            modules,
            ship,
            tech,
            temperature,
            initial_temp,
            max_supercharged,
        )
        if count_supercharged_slots(neighbor_grid, tech) > max_supercharged:
            continue
        populate_adjacency_bonuses(neighbor_grid, tech)
        populate_module_bonuses(neighbor_grid, tech)
        neighbor_bonus = populate_core_bonus(neighbor_grid, tech)
        if neighbor_bonus > best_bonus:
            best_bonus = neighbor_bonus
            best_grid = Grid.from_dict(neighbor_grid.to_dict())
            iteration_without_improvement = 0
            stagnation_counter = 0
            num_acceptances += 1
        else:
            iteration_without_improvement += 1
            stagnation_counter += 1
        energy_diff = neighbor_bonus - populate_core_bonus(current_grid, tech)
        if energy_diff < 0:
            acceptance_probability = math.exp(energy_diff / temperature)
            if random.random() < acceptance_probability:
                current_grid = Grid.from_dict(neighbor_grid.to_dict())
                num_acceptances += 1
        if iteration_without_improvement >= patience:
            temperature *= decay_factor
            iteration_without_improvement = 0
        temperature *= cooling_rate
        if stagnation_counter >= stagnation_threshold:
            if random.random() < restart_probability:
                current_grid = perturb_grid(best_grid, modules, ship, tech)
                temperature = initial_temp
                stagnation_counter = 0
                iteration_without_improvement = 0
            else:
                temperature = initial_temp
                stagnation_counter = 0
        if iteration % 1000 == 0:
            print(
                f"simulated_annealing_optimization - tech: {tech} - Iteration {iteration}/{max_iterations}, Temp: {temperature:.2f}, Best Bonus: {best_bonus:.2f}, Cooling Rate: {cooling_rate:.4f}"
            )
    acceptance_rate = num_acceptances / total_iterations if total_iterations > 0 else 0
    print(f"Acceptance Rate: {acceptance_rate:.4f}")
    return best_grid, best_bonus


def generate_neighbor_grid_with_movement(
    grid, modules, ship, tech, temperature, initial_temp, max_supercharged
):
    neighbor_grid = Grid.from_dict(grid.to_dict())
    tech_modules = get_tech_modules(modules, ship, tech)
    core_modules = [module for module in tech_modules if module["type"] == "core"]
    bonus_modules = [module for module in tech_modules if module["type"] == "bonus"]
    occupied_positions = [
        (x, y)
        for y in range(grid.height)
        for x in range(grid.width)
        if neighbor_grid.get_cell(x, y)["module"] is not None
    ]
    available_positions = [
        (x, y)
        for y in range(grid.height)
        for x in range(grid.width)
        if neighbor_grid.get_cell(x, y)["module"] is None
        and neighbor_grid.get_cell(x, y)["active"]
    ]
    supercharged_positions = [
        (x, y)
        for y in range(grid.height)
        for x in range(grid.width)
        if neighbor_grid.get_cell(x, y)["supercharged"]
    ]
    unoccupied_supercharged_positions = [
        pos for pos in supercharged_positions if pos not in occupied_positions
    ]
    move_count = max(1, int(5 * min(temperature / initial_temp, 1.0)))
    if not occupied_positions:
        random.shuffle(unoccupied_supercharged_positions)
        for core_module in core_modules:
            if unoccupied_supercharged_positions:
                x, y = unoccupied_supercharged_positions.pop()
                place_module(
                    neighbor_grid,
                    x,
                    y,
                    core_module["id"],
                    core_module["label"],
                    tech,
                    core_module["type"],
                    core_module["bonus"],
                    core_module["adjacency"],
                    core_module["sc_eligible"],
                    core_module["image"],
                )
            elif available_positions:
                x, y = random.choice(available_positions)
                place_module(
                    neighbor_grid,
                    x,
                    y,
                    core_module["id"],
                    core_module["label"],
                    tech,
                    core_module["type"],
                    core_module["bonus"],
                    core_module["adjacency"],
                    core_module["sc_eligible"],
                    core_module["image"],
                )
        for bonus_module in bonus_modules:
            if (
                unoccupied_supercharged_positions
                and count_supercharged_slots(neighbor_grid, tech) < max_supercharged
            ):
                x, y = unoccupied_supercharged_positions.pop()
                place_module(
                    neighbor_grid,
                    x,
                    y,
                    bonus_module["id"],
                    bonus_module["label"],
                    tech,
                    bonus_module["type"],
                    bonus_module["bonus"],
                    bonus_module["adjacency"],
                    bonus_module["sc_eligible"],
                    bonus_module["image"],
                )
            elif available_positions:
                x, y = random.choice(available_positions)
                place_module(
                    neighbor_grid,
                    x,
                    y,
                    bonus_module["id"],
                    bonus_module["label"],
                    tech,
                    bonus_module["type"],
                    bonus_module["bonus"],
                    bonus_module["adjacency"],
                    bonus_module["sc_eligible"],
                    bonus_module["image"],
                )
    else:
        for _ in range(move_count):
            if not occupied_positions or not available_positions:
                break
            if unoccupied_supercharged_positions:
                non_supercharged_occupied = [
                    pos
                    for pos in occupied_positions
                    if pos not in supercharged_positions
                ]
                if non_supercharged_occupied:
                    old_x, old_y = random.choice(non_supercharged_occupied)
                else:
                    old_x, old_y = random.choice(occupied_positions)
            else:
                old_x, old_y = random.choice(occupied_positions)
            occupied_positions.remove((old_x, old_y))
            old_cell = neighbor_grid.get_cell(old_x, old_y)
            old_module = old_cell["module"]
            place_module(
                neighbor_grid, old_x, old_y, None, None, None, "", 0, False, False, None
            )
            if unoccupied_supercharged_positions:
                new_x, new_y = unoccupied_supercharged_positions.pop()
            else:
                new_x, new_y = find_best_available_position(
                    neighbor_grid, old_cell["tech"], available_positions
                )
                if (new_x, new_y) in available_positions:
                    available_positions.remove((new_x, new_y))
            is_supercharged = (
                old_cell["supercharged"]
                and count_supercharged_slots(neighbor_grid, tech) < max_supercharged
            )
            if neighbor_grid.get_cell(new_x, new_y)["module"] is None:
                place_module(
                    neighbor_grid,
                    new_x,
                    new_y,
                    old_module,
                    old_cell["label"],
                    old_cell["tech"],
                    old_cell["type"],
                    old_cell["bonus"],
                    old_cell["adjacency"],
                    is_supercharged,
                    old_cell["image"],
                )
    return neighbor_grid


def get_move_count(temperature, initial_temp):
    return max(1, int(10 * math.sqrt(temperature / initial_temp)))


def perturb_grid(grid, modules, ship, tech):
    perturbed_grid = Grid.from_dict(grid.to_dict())
    tech_modules = get_tech_modules_for_training(modules, ship, tech)
    available_positions = [
        (x, y)
        for y in range(perturbed_grid.height)
        for x in range(perturbed_grid.width)
        if perturbed_grid.get_cell(x, y)["module"] is None
    ]
    occupied_positions = [
        (x, y)
        for y in range(perturbed_grid.height)
        for x in range(perturbed_grid.width)
        if perturbed_grid.get_cell(x, y)["module"] is not None
    ]
    num_to_remove = int(0.5 * len(occupied_positions))
    if num_to_remove > 0:
        modules_to_relocate = random.sample(occupied_positions, num_to_remove)
        for x, y in modules_to_relocate:
            module_to_remove = perturbed_grid.get_cell(x, y)["module"]
            place_module(
                perturbed_grid, x, y, None, None, None, "", 0, False, False, None
            )
            available_positions.append((x, y))
        random.shuffle(available_positions)
        for x, y in modules_to_relocate:
            if available_positions:
                new_x, new_y = available_positions.pop()
                module_to_place = next(
                    (m for m in tech_modules if m["id"] == module_to_remove), None
                )
                if module_to_place:
                    place_module(
                        perturbed_grid,
                        new_x,
                        new_y,
                        module_to_place["id"],
                        module_to_place["label"],
                        tech,
                        module_to_place["type"],
                        module_to_place["bonus"],
                        module_to_place["adjacency"],
                        module_to_place["sc_eligible"],
                        module_to_place["image"],
                    )
                else:
                    print(
                        f"Warning: Module with id {module_to_remove} not found in tech_modules. Available keys: {list(tech_modules[0].keys()) if tech_modules else []}"
                    )
    return perturbed_grid


def find_best_available_position(grid, tech, available_positions):
    best_position = None
    max_weighted_score = -1
    for x, y in available_positions:
        adjacency_bonus = calculate_potential_adjacency_bonus(grid, x, y, tech)
        is_supercharged = grid.get_cell(x, y)["supercharged"]
        weighted_score = (adjacency_bonus * 2) + (0.25 if is_supercharged else 0)
        if weighted_score > max_weighted_score:
            max_weighted_score = weighted_score
            best_position = (x, y)
    return best_position if best_position else random.choice(available_positions)
