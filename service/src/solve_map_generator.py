import argparse
from grid_utils import Grid
from modules import modules
from optimization_algorithms import refine_placement  # Import refine_placement
from grid_display import print_grid, print_grid_compact


def generate_solve_map(tech, grid_width=3, grid_height=3, player_owned_rewards=None):
    """Generates a single solve map for a given technology."""
    grid = Grid(width=grid_width, height=grid_height)
    try:
        optimized_grid, _ = refine_placement(grid, "Exotic", modules, tech, player_owned_rewards)  #Using Exotic ship
        return optimized_grid
    except Exception as e:
        print(f"Error generating solve map for {tech}: {e}")
        return None


def generate_solve_map_template(grid):
    """Generates a solve map template from a Grid object."""
    template = {}
    for y in range(grid.height):
        for x in range(grid.width):
            cell = grid.get_cell(x, y)
            module_id = cell["module"]
            template[(x, y)] = module_id
    return template


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a solve map for a given technology.")
    parser.add_argument("--tech", type=str, default="infra", help="Technology key (e.g., 'pulse', 'infra')")
    args = parser.parse_args()

    tech = args.tech  # Get technology from command line or use default

    solve_map = generate_solve_map(tech, 3, 3, ["PC"])

    if solve_map:
        print(f"\nSolve map for {tech}:")
        print_grid_compact(solve_map)

        # Print the solve map template
        solve_map_template = generate_solve_map_template(solve_map)
        print("\nSolve Map Template:")
        print(f'    "{tech}": {{')
        for (x, y), module_id in solve_map_template.items():
            print(f"        ({x}, {y}): \"{module_id}\",")
        print("    },")

