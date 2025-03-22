# modules_data.py
import json
from modules import modules

def get_tech_modules(modules, ship, tech_key):
    """Retrieves modules for a specified ship and technology key, ignoring technology type."""
    ship_data = modules.get(ship)
    if ship_data is None:
        print(f"Error: Ship '{ship}' not found in modules data.")
        return None

    types_data = ship_data.get("types")
    if types_data is None:
        print(f"Error: 'types' key not found for ship '{ship}'.")
        return None

    for tech_type in types_data:
        tech_category = types_data.get(tech_type)
        if tech_category is None:
            print(f"Error: Technology type '{tech_type}' not found for ship '{ship}'.")
            continue #skip this type and check the next
        
        for technology in tech_category:
            if technology.get("key") == tech_key:
                modules_list = technology.get("modules")
                if modules_list is None:
                    print(f"Error: 'modules' key not found for technology '{tech_key}' within type '{tech_type}' on ship '{ship}'.")
                    return None
                return modules_list

    print(f"Error: Technology '{tech_key}' not found for ship '{ship}'.")
    return None

def get_tech_modules_for_training(modules, ship, tech_key):
    """Retrieves modules for training, returning the modules as they are in modules_refactored.py."""
    ship_data = modules.get(ship)
    if ship_data is None:
        print(f"Error: Ship '{ship}' not found in modules data.")
        return []

    types_data = ship_data.get("types")
    if types_data is None:
        print(f"Error: 'types' key not found for ship '{ship}'.")
        return []

    for tech_list in types_data.values():
        for tech_data in tech_list:
            if tech_data.get("key") == tech_key:
                return tech_data.get("modules", [])
    return []


def get_tech_tree_json(ship):
    """Generates a technology tree for a given ship and returns it as JSON."""
    try:
        tech_tree = get_tech_tree(ship)  # Call your existing function
        if "error" in tech_tree:
            return json.dumps({"error": tech_tree["error"]})  # Return error as JSON
        else:
            return json.dumps(tech_tree, indent=2)  # Return tree as JSON with indentation for readability
    except Exception as e:
        return json.dumps({"error": str(e)})  # Catch any errors during tree generation

def get_tech_tree(ship):
    """Generates a technology tree for a given ship."""
    ship_data = modules.get(ship)
    if ship_data is None:
        return {"error": f"Ship '{ship}' not found."}

    types_data = ship_data.get("types")
    if types_data is None:
        return {"error": f"'types' key not found for ship '{ship}'."}

    tech_tree = {}
    for tech_type, tech_list in types_data.items():
        tech_tree[tech_type] = []
        for tech in tech_list:
            tech_tree[tech_type].append(
                {
                    "label": tech["label"],
                    "key": tech["key"],
                    # Add other relevant fields if needed
                }
            )

    return tech_tree

__all__ = ["get_tech_modules", "get_tech_modules_for_training", "get_tech_tree", "get_tech_tree_json"]
