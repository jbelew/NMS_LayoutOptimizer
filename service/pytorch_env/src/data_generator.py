import random
import numpy as np
import torch
import torch.utils.data as data
from optimizer import simulated_annealing_optimization, Grid, modules, get_tech_modules_for_training, print_grid_compact

# --- Data Generation ---
def generate_training_data(num_samples, grid_width, grid_height, max_supercharged, ship, num_techs, tech_filter):
    X_train = []
    y_train = []
    bonus_scores = []  # Store bonus scores
    module_id_mapping = {}  # Initialize module_id_mapping *outside* the loop

    for i in range(num_samples):
        grid = Grid(grid_width, grid_height)
        num_supercharged = random.randint(0, max_supercharged)
        supercharged_positions = random.sample(
            [(x, y) for y in range(grid_height) for x in range(grid_width)],
            num_supercharged,
        )
        for x, y in supercharged_positions:
            grid.set_supercharged(x, y, True)

        # Use the specified technology
        tech = tech_filter

        try:
            optimized_grid, best_bonus = simulated_annealing_optimization(grid, ship, modules, tech)
            print(f"Sample {i + 1} - Best Bonus: {best_bonus}")
            print_grid_compact(optimized_grid)
        except Exception as e:
            print(f"Error during optimization for sample {i + 1}: {e}")
            continue  # Skip this sample if optimization fails

        # Encode the grid and solution (integer matrix encoding)
        input_matrix = np.zeros((grid_height, grid_width), dtype=int)
        output_matrix = np.zeros((grid_height, grid_width), dtype=int)

        none_count = 0  # Count 'None' modules
        for y in range(grid_height):
            for x in range(grid_width):
                input_matrix[y, x] = int(grid.get_cell(x, y)["supercharged"])
                module_id = optimized_grid.get_cell(x, y)["module"]
                if module_id is None:
                    none_count += 1
                    output_matrix[y, x] = 0  # Map None to class 0 (background)
                else:
                    # Create the unique ID on the fly
                    unique_id = f"{ship}-{tech}-{module_id}"
                    # Add to the mapping if it doesn't exist
                    if unique_id not in module_id_mapping:
                        module_id_mapping[unique_id] = len(module_id_mapping) + 1
                    output_matrix[y, x] = module_id_mapping[unique_id]


        X_train.append(input_matrix)
        y_train.append(output_matrix)
        bonus_scores.append(best_bonus)  # Store the bonus score

    # Determine the maximum number of output classes
    max_output_classes = len(module_id_mapping) if module_id_mapping else 0
    if not X_train:
        print("X_train is empty. Check data generation logic.")
        return [], [], [], 0

    print(f"Number of output classes: {max_output_classes}")  # Debugging
    print(f"Length of X_train: {len(X_train)}")
    print(f"Length of y_train: {len(y_train)}")
    print(f"Length of bonus_scores: {len(bonus_scores)}")

    return X_train, y_train, bonus_scores, max_output_classes

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

# Example usage:
num_samples = 32  # Adjust this to a larger number for better results
grid_width = 10
grid_height = 6
max_supercharged = 4
ship = "Exotic"
num_techs = len([tech_data["key"] for tech_data in modules[ship]["types"]["weapons"]])
tech_filter = "infra" # Set the tech filter here

X_train, y_train, bonus_scores, num_output_classes = generate_training_data(num_samples, grid_width, grid_height, max_supercharged, ship, num_techs, tech_filter)

X_train = torch.tensor(np.array(X_train), dtype=torch.float32)
X_train = X_train.view(-1, 1, grid_height, grid_width) # Reshape here
y_train = torch.tensor(np.array(y_train), dtype=torch.long)
bonus_scores = torch.tensor(np.array(bonus_scores), dtype=torch.float32) # Convert bonus scores to tensor

# Create a custom dataset that includes bonus scores
class BonusDataset(data.Dataset):
    def __init__(self, X, y, bonus):
        self.X = X
        self.y = y
        self.bonus = bonus

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        return self.X[idx], self.y[idx], self.bonus[idx]

train_dataset = BonusDataset(X_train, y_train, bonus_scores)
train_loader = data.DataLoader(train_dataset, batch_size=32, shuffle=True)

print(f"Number of output classes: {num_output_classes}")
