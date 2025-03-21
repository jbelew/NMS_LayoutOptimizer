# bonus_calculations.py
from grid_utils import Grid


def calculate_adjacency_bonus(grid: Grid, x: int, y: int) -> float:
    """Calculates the adjacency bonus for a module at a given position."""
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
                adjacency_bonus += 1
                grid.set_adjacency_bonus(x, y, adjacency_bonus)

    return adjacency_bonus


def populate_adjacency_bonuses(grid: Grid, tech: str) -> None:
    """Populates the adjacency bonuses for all modules in the grid."""
    for row in range(grid.height):
        for col in range(grid.width):
            current_cell = grid.get_cell(col, row)
            if current_cell["module"] is not None and current_cell["tech"] == tech:
                calculate_adjacency_bonus(grid, col, row)


def calculate_module_bonus(grid: Grid, x: int, y: int) -> float:
    """Calculates the total bonus for a module at a given position."""
    cell = grid.get_cell(x, y)

    base_bonus = cell["bonus"]
    adjacency_bonus = cell["adjacency_bonus"]
    is_supercharged = cell["supercharged"]
    is_sc_eligible = cell["sc_eligible"]

    total_bonus = base_bonus * adjacency_bonus

    if is_supercharged and is_sc_eligible:
        total_bonus *= 1.25

    grid.set_total(x, y, total_bonus)
    return total_bonus


def populate_module_bonuses(grid: Grid, tech: str) -> None:
    """Populates the total bonuses for all bonus modules in the grid."""
    for row in range(grid.height):
        for col in range(grid.width):
            current_cell = grid.get_cell(col, row)
            if current_cell["type"] == "bonus" and current_cell["tech"] == tech:
                calculate_module_bonus(grid, col, row)


def calculate_core_bonus(grid: Grid, tech: str) -> float:
    """Calculates the core bonus for the grid, requiring bonus modules to be adjacent."""
    bonus_total = 0
    core_total = 0
    core_x, core_y = None, None

    # First, find the core module's coordinates
    for row in range(grid.height):
        for col in range(grid.width):
            cell = grid.get_cell(col, row)
            if cell["type"] == "core" and cell["tech"] == tech:
                core_x, core_y = col, row
                core_total = cell["bonus"] + cell["adjacency_bonus"] # Let's keep this part

    # Now, iterate to calculate bonus based on adjacent 'bonus' modules
    if core_x is not None and core_y is not None:
        for row in range(grid.height):
            for col in range(grid.width):
                cell = grid.get_cell(col, row)
                if cell["type"] == "bonus" and cell["tech"] == tech:
                    # Check for adjacency to the core module
                    if (abs(col - core_x) == 1 and row == core_y) or (abs(row - core_y) == 1 and col == core_x):
                        bonus_total += cell["total"] * cell["adjacency_bonus"]

    return bonus_total

def populate_core_bonus(grid: Grid, tech: str) -> float:
    """Populates the core bonus and includes adjacency bonuses."""
    core_bonus = calculate_core_bonus(grid, tech)
    final_bonus = 0
    adjacency_total_bonus = 0

    for row in range(grid.height):
        for col in range(grid.width):
            cell = grid.get_cell(col, row)
            if cell["type"] == "core" and cell["tech"] == tech:
                if cell["sc_eligible"] and cell["supercharged"]:
                    final_bonus = core_bonus * 1.25
                else:
                    final_bonus = core_bonus
                grid.set_total(col, row, final_bonus)
            if cell["module"] is not None and cell["tech"] == tech:  # Consider bonuses for all modules
                adjacency_total_bonus += cell["adjacency_bonus"]

    # Add the total adjacency bonus (you might want to adjust the weight here)
    final_bonus += adjacency_total_bonus * 0.1  # Example weight of 0.1

    return final_bonus


def calculate_potential_adjacency_bonus(grid: Grid, x: int, y: int, tech: str) -> int:
    """Calculate the potential adjacency bonus if a module were placed at (x, y)."""
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    adjacency_bonus = 0

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < grid.width and 0 <= ny < grid.height:
            neighbor = grid.get_cell(nx, ny)
            if neighbor["module"] is not None and neighbor["tech"] == tech:
                adjacency_bonus += 1
    return adjacency_bonus


def count_supercharged_slots(grid: Grid, tech: str) -> int:
    """Counts the number of supercharged slots in the grid for a given tech."""
    count = 0
    for y in range(grid.height):
        for x in range(grid.width):
            if (
                grid.get_cell(x, y)["supercharged"]
                and grid.get_cell(x, y)["tech"] == tech
            ):
                count += 1
    return count
