import random
import math

from itertools import permutations

class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = [[{"module": None, "value": 0, "type": "", "total": 0.0, "adjacency_bonus": 0.0, "bonus": 0.0, "adjacency": False, "tech": None, "supercharge": False} for _ in range(width)] for _ in range(height)]

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
        
    def set_supercharge(self, x, y, supercharge):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.cells[y][x]["supercharge"] = supercharge
        else:
            raise IndexError("Cell out of bounds")

    def set_tech(self, x, y, tech):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.cells[y][x]["tech"] = tech
        else:
            raise IndexError("Cell out of bounds")

    def __str__(self):
        return "\n".join([" ".join(["." if cell["value"] is None else cell["value"] for cell in row]) for row in self.cells])

def optimize_placement(grid, modules, tech, supercharged_slots):
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
    available_positions = [(x, y) for y in range(grid.height) for x in range(grid.width) if grid.get_cell(x, y)["module"] is None]

    # Create a set of supercharged slots for fast membership testing
    supercharged_set = set(supercharged_slots)

    for core_position in available_positions:
        # if core_position in supercharged_set:  # Skip if core is in a supercharged slot
        #     continue

        for bonus_placement in permutations(available_positions, len(bonus_modules)):
            temp_grid = Grid(grid.width, grid.height)
            for y in range(grid.height):
                for x in range(grid.width):
                    cell = grid.get_cell(x, y)
                    temp_grid.set_module(x, y, cell["module"])
                    temp_grid.set_tech(x, y, cell["tech"])
                    temp_grid.set_type(x, y, cell["type"])
                    temp_grid.set_bonus(x, y, cell["bonus"])
                    temp_grid.set_adjacency(x, y, cell["adjacency"])
                    temp_grid.set_supercharge(x, y, cell["supercharge"])
                    temp_grid.set_adjacency_bonus(x, y, cell["adjacency_bonus"])
                    temp_grid.set_total(x, y, cell["total"])

            # Place the core module
            core_x, core_y = core_position
            core_module = core_modules[0]
            place_module(temp_grid, core_x, core_y, core_module["name"], core_module["tech"], core_module["type"], core_module["bonus"], core_module["adjacency"], core_module["supercharge"])

            # Place the bonus modules
            for index, bonus_position in enumerate(bonus_placement):
                x, y = bonus_position
                if temp_grid.get_cell(x, y)["module"] is not None:
                    continue
                bonus_module = bonus_modules[index]
                place_module(temp_grid, x, y, bonus_module["name"], bonus_module["tech"], bonus_module["type"], bonus_module["bonus"], bonus_module["adjacency"], bonus_module["supercharge"])

            # Calculate total bonus for the core module
            populate_adjacency_bonuses(temp_grid, tech)
            populate_module_bonuses(temp_grid, tech, supercharged_slots)
            core_bonus = populate_core_bonus(temp_grid, tech, supercharged_slots)

            # Update optimal placement if current bonus is higher
            iteration += 1
            print('\rIteration {}'.format(iteration), end='')

            if core_bonus > highest_bonus:
                highest_bonus = core_bonus
                optimal_grid = temp_grid
                print()
                print("Iterating tech: {} - highest bonus: {:.2f}".format(tech, highest_bonus))

    return optimal_grid, highest_bonus

def optimize_placement_greedy(grid, modules, tech, supercharged_slots):
    optimal_grid = None
    highest_bonus = 0.0

    # Filter modules based on tech
    tech_modules = [module for module in modules if module["tech"] == tech]

    # Separate core and bonus modules
    core_modules = [module for module in tech_modules if module["type"] == "core"]
    bonus_modules = [module for module in tech_modules if module["type"] == "bonus"]

    if not bonus_modules or not core_modules:
        raise ValueError("No bonus or core modules specified")

    # Find all valid positions in the grid
    available_positions = [(x, y) for y in range(grid.height) for x in range(grid.width) if grid.get_cell(x, y)["module"] is None]

    # Create a set of supercharged slots for fast membership testing
    supercharged_set = set(supercharged_slots)

    for core_position in available_positions:
        if core_position in supercharged_set:  # Skip if core is in a supercharged slot
            continue

        for bonus_placement in permutations(available_positions, len(bonus_modules)):
            temp_grid = Grid(grid.width, grid.height)
            for y in range(grid.height):
                for x in range(grid.width):
                    cell = grid.get_cell(x, y)
                    temp_grid.set_module(x, y, cell["module"])
                    temp_grid.set_tech(x, y, cell["tech"])
                    temp_grid.set_type(x, y, cell["type"])
                    temp_grid.set_bonus(x, y, cell["bonus"])
                    temp_grid.set_adjacency(x, y, cell["adjacency"])
                    temp_grid.set_adjacency_bonus(x, y, cell["adjacency_bonus"])
                    temp_grid.set_total(x, y, cell["total"])

            # Place the core module
            core_x, core_y = core_position
            core_module = core_modules[0]
            place_module(temp_grid, core_x, core_y, core_module["name"], core_module["tech"], core_module["type"], core_module["bonus"], core_module["adjacency"])

            # Place the bonus modules
            for index, bonus_position in enumerate(bonus_placement):
                x, y = bonus_position
                if temp_grid.get_cell(x, y)["module"] is not None:
                    continue
                bonus_module = bonus_modules[index]
                place_module(temp_grid, x, y, bonus_module["name"], bonus_module["tech"], bonus_module["type"], bonus_module["bonus"], bonus_module["adjacency"])

            # Calculate total bonus for the core module
            populate_adjacency_bonuses(temp_grid, tech)
            populate_module_bonuses(temp_grid, tech, supercharged_slots)
            core_bonus = populate_core_bonus(temp_grid, tech)

            # Update optimal placement if current bonus is higher
            if core_bonus > highest_bonus:
                highest_bonus = core_bonus
                optimal_grid = temp_grid
                print("Iterating tech: {} - highest bonus: {:.2f}".format(tech, highest_bonus))
                print_grid(optimal_grid, supercharged_slots)

    return optimal_grid, highest_bonus

def simulated_annealing_optimization(grid, modules, tech, supercharged_slots, initial_temp=10000, cooling_rate=0.9999, max_iterations=100000, patience=200, decay_factor=0.999):
    best_grid = Grid(grid.width, grid.height)
    best_bonus = -float('inf')
    
    current_grid = Grid(grid.width, grid.height)
    for y in range(grid.height):
        for x in range(grid.width):
            current_cell = grid.get_cell(x, y)
            current_grid.set_module(x, y, current_cell["module"])
            current_grid.set_tech(x, y, current_cell["tech"])
            current_grid.set_type(x, y, current_cell["type"])
            current_grid.set_bonus(x, y, current_cell["bonus"])
            current_grid.set_adjacency(x, y, current_cell["adjacency"])
            current_grid.set_supercharge(x, y, current_cell["supercharge"])
            current_grid.set_adjacency_bonus(x, y, current_cell["adjacency_bonus"])
            current_grid.set_total(x, y, current_cell["total"])

    temperature = initial_temp
    iteration_without_improvement = 0  # Track the number of iterations without improvement
    for iteration in range(max_iterations):

        # Generate a neighbor solution by randomly changing the placement of modules
        movement_size = "large" if temperature > 5 else "small"
        neighbor_grid = generate_neighbor_grid_with_movement(current_grid, modules, tech, supercharged_slots, movement_size)

        # Calculate the bonus for the current and neighbor grid
        populate_adjacency_bonuses(neighbor_grid, tech)
        populate_module_bonuses(neighbor_grid, tech, supercharged_slots)
        neighbor_bonus = populate_core_bonus(neighbor_grid, tech, supercharged_slots)

        # If the neighbor solution is better, accept it and copy the grid to the best grid
        if neighbor_bonus > best_bonus:            
            best_bonus = neighbor_bonus
            for y in range(grid.height):
                for x in range(grid.width):
                    best_grid.cells[y][x] = neighbor_grid.cells[y][x].copy()
            iteration_without_improvement = 0  # Reset improvement counter
        else:
            iteration_without_improvement += 1

        # Calculate energy difference
        energy_diff = neighbor_bonus - populate_core_bonus(current_grid, tech, supercharged_slots)

        # If the new solution is worse, decide whether to accept it based on temperature
        if energy_diff < 0:
            acceptance_probability = math.exp(energy_diff / temperature)
            if random.random() < acceptance_probability:
                current_grid = neighbor_grid

        if iteration_without_improvement >= patience:
            temperature *= decay_factor  # Slow down cooling
            iteration_without_improvement = 0  # Reset the patience counter

        # Decrease temperature using the cooling rate
        temperature *= cooling_rate

        # Print progress
        if iteration % 100 == 0:
            print(f"Iteration {iteration}/{max_iterations}, Temp: {temperature:.2f}, Best Bonus: {best_bonus:.2f}, Cooling Rate: {cooling_rate:.4f}")

    return best_grid, best_bonus

def generate_neighbor_grid(grid, modules, tech, supercharged_slots):
    """Generate a new grid by modifying the existing grid with new module placements."""
    # Create a new grid, starting by copying the original grid's state
    neighbor_grid = Grid(grid.width, grid.height)

    # Copy the current state of the grid to the new grid
    for y in range(grid.height):
        for x in range(grid.width):
            current_cell = grid.get_cell(x, y)
            neighbor_grid.set_module(x, y, current_cell["module"])
            neighbor_grid.set_tech(x, y, current_cell["tech"])
            neighbor_grid.set_type(x, y, current_cell["type"])
            neighbor_grid.set_bonus(x, y, current_cell["bonus"])
            neighbor_grid.set_adjacency(x, y, current_cell["adjacency"])
            neighbor_grid.set_supercharge(x, y, current_cell["supercharge"])
            neighbor_grid.set_adjacency_bonus(x, y, current_cell["adjacency_bonus"])
            neighbor_grid.set_total(x, y, current_cell["total"])

    # Randomly shuffle module placements for available spaces (empty spots)
    available_positions = [(x, y) for y in range(grid.height) for x in range(grid.width) if grid.get_cell(x, y)["module"] is None]
    random.shuffle(available_positions)

    # Filter the tech-specific modules
    tech_modules = [module for module in modules if module["tech"] == tech]
    core_modules = [module for module in tech_modules if module["type"] == "core"]
    bonus_modules = [module for module in tech_modules if module["type"] == "bonus"]

    # Place core modules first
    for core_module in core_modules:
        if available_positions:  # Ensure there is an available spot
            x, y = available_positions.pop()
            place_module(neighbor_grid, x, y, core_module["name"], core_module["tech"], core_module["type"], core_module["bonus"], core_module["adjacency"], core_module["supercharge"])

    # Place bonus modules next
    for bonus_module in bonus_modules:
        if available_positions:  # Ensure there is an available spot
            x, y = available_positions.pop()
            place_module(neighbor_grid, x, y, bonus_module["name"], bonus_module["tech"], bonus_module["type"], bonus_module["bonus"], bonus_module["adjacency"], bonus_module["supercharge"])

    return neighbor_grid  # Return the modified grid with updated module placements

def generate_neighbor_grid_with_movement(grid, modules, tech, supercharged_slots, movement_size="small"):
    """Generate a new grid by modifying the existing grid with new module placements."""
    neighbor_grid = Grid(grid.width, grid.height)
    for y in range(grid.height):
        for x in range(grid.width):
            current_cell = grid.get_cell(x, y)
            neighbor_grid.set_module(x, y, current_cell["module"])
            neighbor_grid.set_tech(x, y, current_cell["tech"])
            neighbor_grid.set_type(x, y, current_cell["type"])
            neighbor_grid.set_bonus(x, y, current_cell["bonus"])
            neighbor_grid.set_adjacency(x, y, current_cell["adjacency"])
            neighbor_grid.set_supercharge(x, y, current_cell["supercharge"])
            neighbor_grid.set_adjacency_bonus(x, y, current_cell["adjacency_bonus"])
            neighbor_grid.set_total(x, y, current_cell["total"])

    # Filter the tech-specific modules
    tech_modules = [module for module in modules if module["tech"] == tech]
    core_modules = [module for module in tech_modules if module["type"] == "core"]
    bonus_modules = [module for module in tech_modules if module["type"] == "bonus"]

    # Identify all positions currently occupied by the tech modules
    occupied_positions = [(x, y) for y in range(grid.height) for x in range(grid.width) if grid.get_cell(x, y)["module"] is not None and grid.get_cell(x, y)["tech"] == tech]

    # Collect available positions for placement (empty spots)
    available_positions = [(x, y) for y in range(grid.height) for x in range(grid.width) if grid.get_cell(x, y)["module"] is None]


    # if no modules are on the board, generate a fresh board
    if not occupied_positions:
        random.shuffle(available_positions)
        for core_module in core_modules:
            if available_positions:
                x, y = available_positions.pop()
                place_module(neighbor_grid, x, y, core_module["name"], core_module["tech"], core_module["type"], core_module["bonus"], core_module["adjacency"], core_module["supercharge"])

        for bonus_module in bonus_modules:
            if available_positions:
                x, y = available_positions.pop()
                place_module(neighbor_grid, x, y, bonus_module["name"], bonus_module["tech"], bonus_module["type"], bonus_module["bonus"], bonus_module["adjacency"], bonus_module["supercharge"])
    else:
        # randomly choose a position from the occupied positions to move a module
        old_x, old_y = random.choice(occupied_positions)
        old_cell = neighbor_grid.get_cell(old_x, old_y)
        old_module = old_cell["module"]

        # clear out the old module
        place_module(neighbor_grid, old_x, old_y, None, None, None, 0, False, False)

        # randomly choose a new location from the available positions to place the module
        new_x, new_y = random.choice(available_positions)

        # replace the module in the new location
        place_module(neighbor_grid, new_x, new_y, old_module, old_cell["tech"], old_cell["type"], old_cell["bonus"], old_cell["adjacency"], old_cell["supercharge"])

    return neighbor_grid

def place_module(grid, x, y, module, tech, type, bonus, adjacency, supercharge):
    grid.set_module(x, y, module)
    grid.set_tech(x, y, tech)
    grid.set_type(x, y, type)
    grid.set_bonus(x, y, bonus)
    grid.set_adjacency(x, y, adjacency)
    grid.set_supercharge(x, y, supercharge)

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

def calculate_module_bonus(grid, x, y, supercharged_slots):
    cell = grid.get_cell(x, y)
    base_bonus = cell["bonus"]
    adjacency_bonus = cell["adjacency_bonus"]
    is_supercharged = (x, y) in supercharged_slots

    total_bonus = base_bonus + adjacency_bonus
    if is_supercharged:
        if cell["supercharge"]:
            total_bonus *= 1.25

    grid.set_total(x, y, total_bonus)
    return total_bonus

def populate_module_bonuses(grid, tech, supercharged_slots):
    for row in range(grid.height):
        for col in range(grid.width):
            current_cell = grid.get_cell(col, row)
            if current_cell["type"] == "bonus" and current_cell["tech"] == tech:
                calculate_module_bonus(grid, col, row, supercharged_slots)

def calculate_core_bonus(grid, tech, supercharged_slots):
    """
    Calculates the core bonus by summing the total bonus of all bonus modules and adding in the core module's total.
    """
    core_bonus = 0
    core_module_bonus = 0

    for row in range(grid.height):
        for col in range(grid.width):
            cell = grid.get_cell(col, row)
            if cell["type"] == "bonus" and cell["tech"] == tech:
                core_bonus += cell["total"]
            elif cell["type"] == "core" and cell["tech"] == tech:
                core_module_bonus = cell["bonus"] + cell["adjacency_bonus"]
    return core_bonus + core_module_bonus

def populate_core_bonus(grid, tech, supercharged_slots):
    core_bonus = calculate_core_bonus(grid, tech, supercharged_slots)
    final_bonus = 0
    for row in range(grid.height):
        for col in range(grid.width):
            cell = grid.get_cell(col, row)
            if cell["type"] == "core" and cell["tech"] == tech:
                final_bonus = core_bonus
                grid.set_total(col, row, final_bonus)

    return final_bonus

def print_grid(grid, supercharged_slots):
    """Display the grid with only 'Val' for the total value of each slot."""

    # Format and print the grid
    for y, row in enumerate(grid.cells):
        formatted_row = []

        for x, cell in enumerate(row):
            cell_data = grid.get_cell(x, y)
            total_value = cell_data['value']
            is_supercharged = (x, y) in supercharged_slots
            is_shield = cell_data['tech'] == 'shield'
            is_infra = cell_data['tech'] == 'infra'

            formatted_row.append(
                f"\033[93m{cell_data['module'] if cell_data['module'] else '.'} (T: {cell_data['total']:.2f}) (B: {cell_data['bonus']:.2f}) (A: {cell_data['adjacency_bonus']:.2f})\033[0m"
                if is_supercharged else
                f"\033[96m{cell_data['module'] if cell_data['module'] else '.'} (T: {cell_data['total']:.2f}) (B: {cell_data['bonus']:.2f}) (A: {cell_data['adjacency_bonus']:.2f})\033[0m"
                if is_shield else
                f"\033[91m{cell_data['module'] if cell_data['module'] else '.'} (T: {cell_data['total']:.2f}) (B: {cell_data['bonus']:.2f}) (A: {cell_data['adjacency_bonus']:.2f})\033[0m"
                if is_infra else
                f"{cell_data['module'] if cell_data['module'] else '.'} (T: {cell_data['total']:.2f}) (B: {cell_data['bonus']:.2f}) (A: {cell_data['adjacency_bonus']:.2f})"
                )
        print(" | ".join(formatted_row))
    print()

# Grid and Supercharged Slots
grid = Grid(5, 6)
supercharged_slots = [(1, 1), (1, 2), (4, 3), (2,4)]  # Example supercharged slots

# Module Definitions
modules = [
    {"name": "S", "tech": "shield", "type": "core", "bonus": 0, "adjacency": True, "supercharge": True},  # Defensive Shield
    {"name": "A", "tech": "shield", "type": "bonus", "bonus": .07, "adjacency": True, "supercharge": False},  # Ablative Armor
    {"name": "X", "tech": "shield", "type": "bonus", "bonus": 0.3, "adjacency": True, "supercharge": True},  # Shield Upgrade Sigma
    {"name": "X", "tech": "shield", "type": "bonus", "bonus": 0.3, "adjacency": True, "supercharge": True},  # Shield Upgrade Tau
    {"name": "X", "tech": "shield", "type": "bonus", "bonus": 0.3, "adjacency": True, "supercharge": True},  # Shield Upgrade Theta
    {"name": "I", "tech": "infra", "type": "core", "bonus": .1, "adjacency": True, "supercharge": True},
    {"name": "R", "tech": "infra", "type": "bonus", "bonus": .1, "adjacency": True, "supercharge": True},
    {"name": "X", "tech": "infra", "type": "bonus", "bonus": 0.2, "adjacency": True, "supercharge": True},  # Shield Upgrade Sigma
    {"name": "X", "tech": "infra", "type": "bonus", "bonus": 0.2, "adjacency": True, "supercharge": True},  # Shield Upgrade Tau
    {"name": "X", "tech": "infra", "type": "bonus", "bonus": 0.2, "adjacency": True, "supercharge": True},  # Shield Upgrade Theta    
    {"name": "P", "tech": "photon", "type": "core", "bonus": .1, "adjacency": True, "supercharge": True},
    {"name": "X", "tech": "photon", "type": "bonus", "bonus": 0.2, "adjacency": True, "supercharge": True},  # Shield Upgrade Sigma
    {"name": "X", "tech": "photon", "type": "bonus", "bonus": 0.2, "adjacency": True, "supercharge": True},  # Shield Upgrade Tau
    {"name": "X", "tech": "photon", "type": "bonus", "bonus": 0.2, "adjacency": True, "supercharge": True},  # Shield Upgrade Theta    
] 

# Optimize placement for modules
#grid, max_bonus = optimize_placement(grid, modules, "shield", supercharged_slots)
#grid, max_bonus = optimize_placement(grid, modules, "infra", supercharged_slots)grid, max_bonus = simulated_annealing_optimization(grid, modules, "infra", supercharged_slots)
grid, max_bonus = simulated_annealing_optimization(grid, modules, "shield", supercharged_slots, initial_temp=10000, cooling_rate=0.9999, max_iterations=1500, patience=200, decay_factor=0.99)
grid, max_bonus = simulated_annealing_optimization(grid, modules, "infra", supercharged_slots, initial_temp=10000, cooling_rate=0.9999, max_iterations=1500, patience=200, decay_factor=0.99)
grid, max_bonus = simulated_annealing_optimization(grid, modules, "photon", supercharged_slots, initial_temp=10000, cooling_rate=0.9999, max_iterations=1500, patience=200, decay_factor=0.99)

print("Optimized layout --")
print_grid(grid, supercharged_slots)
