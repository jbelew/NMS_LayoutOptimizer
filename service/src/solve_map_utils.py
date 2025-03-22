# solve_map_utils.py
from modules_data import get_tech_modules

def filter_solves(solves, ship, modules, tech, player_owned_rewards=None):
    """
    Filters the solves dictionary to remove modules that the player does not own.

    Args:
        solves (dict): The solves dictionary.
        ship (str): The ship type.
        modules (dict): The modules data.
        tech (str): The technology key.
        player_owned_rewards (list, optional): A list of reward module IDs owned by the player. Defaults to None.

    Returns:
        dict: A new solves dictionary with unowned modules removed from the solve map.
    """
    filtered_solves = {}
    if ship in solves:
        filtered_solves[ship] = {}
        if tech in solves[ship]:
            filtered_solves[ship][tech] = {}
            tech_solve = solves[ship][tech]
            tech_modules = get_tech_modules(modules, ship, tech, player_owned_rewards)
            if tech_modules is None:
                print(f"Error: No modules found for ship '{ship}' and tech '{tech}'.")
                return {}
            owned_module_ids = {module["id"] for module in tech_modules}
            for position, module_id in tech_solve.items():
                if module_id is None or module_id in owned_module_ids:
                    filtered_solves[ship][tech][position] = module_id
    return filtered_solves