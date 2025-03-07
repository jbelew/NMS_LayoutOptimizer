import random
import json
import os
from sklearn.model_selection import train_test_split, KFold
import xgboost as xgb
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder


# Add k-fold cross validation
kfold = KFold(n_splits=5, shuffle=True)

# Import from the other files
from service.optimizer import (
    Grid,
    optimize_placement,
    place_module,
    modules,
    print_grid,
)

# --- Configuration ---
config = {
    "width": 4,
    "height": 3,
    "tech": "infra",
    "num_grids": 10,
    "test_size": 0.2,
    "random_state": 42,
    "data_file": "data/training_data.json",
    "model_file": "model.json",
    "debug": True,
    "xgb_params": {
        "objective": "multi:softmax",  # Changed objective to multi:softmax
        "eval_metric": "merror",  # Changed eval_metric to merror
        "eta": 0.1,
        "max_depth": 6,
    },
}

# --- Helper Functions ---


def generate_empty_grid(width, height):
    """Generates an empty grid."""
    grid = Grid(width, height)
    for row in grid.cells:
        for cell in row:
            cell["module"] = None
            cell["tech"] = None
            cell["type"] = ""
            cell["total"] = 0.0
            cell["adjacency_bonus"] = 0.0
            cell["bonus"] = 0.0
            cell["active"] = True
            cell["adjacency"] = False
            cell["supercharged"] = False
            cell["sc_eligible"] = False
            cell["image"] = None
    return grid


def set_grid_state(
    grid, width, height, num_inactive_percentage=0.10, num_supercharged_max=4
):
    """Sets the active and supercharged states for a grid."""
    all_cells = [(x, y) for x in range(width) for y in range(height)]
    random.shuffle(all_cells)

    # Set approximately n% of cells as inactive
    num_inactive = max(1, int(num_inactive_percentage * width * height))
    inactive_cells = all_cells[:num_inactive]
    for x, y in all_cells:
        grid.set_active(x, y, True)  # set all to true first
    for x, y in inactive_cells:
        grid.set_active(x, y, False)

    # Filter cells to the first 3 rows
    top_three_rows_cells = [
        (x, y)
        for x in range(width)
        for y in range(min(3, height))
        if (x, y) not in inactive_cells
    ]

    # Set supercharged cells (random number between 0 and 4)
    num_supercharged = random.randint(
        0, min(num_supercharged_max, len(top_three_rows_cells))
    )  # max of 4 or how many cells there are

    if len(top_three_rows_cells) >= num_supercharged:
        supercharged_cells = random.sample(top_three_rows_cells, num_supercharged)
    else:
        supercharged_cells = top_three_rows_cells

    for x, y in all_cells:
        grid.set_supercharged(x, y, False)  # set all to false first
    for x, y in supercharged_cells:
        grid.set_supercharged(x, y, True)


def populate_grid(grid, modules, tech):
    """Populates the grid with modules of the specified technology."""
    tech_modules = [module for module in modules if module["tech"] == tech]
    available_positions = [
        (x, y)
        for y in range(grid.height)
        for x in range(grid.width)
        if grid.get_cell(x, y)["active"]
    ]
    random.shuffle(available_positions)

    for module in tech_modules:
        if available_positions:
            x, y = available_positions.pop()
            place_module(
                grid,
                x,
                y,
                module["name"],
                module["tech"],
                module["type"],
                module["bonus"],
                module["adjacency"],
                module["sc_eligible"],
                module["image"],
            )
    return grid


# --- Data Generation ---


def generate_data_from_optimize_placement(
    num_grids, width, height, modules, tech, debug=False
):
    data = []
    tech_modules = [module for module in modules if module["tech"] == tech]

    for _ in range(num_grids):
        empty_grid = generate_empty_grid(width, height)
        set_grid_state(empty_grid, width, height)
        optimal_grid, optimal_bonus = optimize_placement(empty_grid, modules, tech)

        if optimal_grid is None:
            continue

        # Capture grid state, optimal placement, and resulting bonus
        placement_data = {  # Changed to a dictionary
            "initial_state": empty_grid.to_dict(),  # Use to_dict()
            "optimal_state": optimal_grid.to_dict(),  # Use to_dict()
            "module_positions": get_module_positions(optimal_grid),
        }
        data.append(placement_data)

        if debug:
            print(f"Optimal Bonus: {optimal_bonus}")
            print_grid(optimal_grid)

    return data


def get_module_positions(grid):
    """Extract module positions and their contribution to final bonus"""
    positions = []
    for y in range(grid.height):
        for x in range(grid.width):
            cell = grid.get_cell(x, y)
            if cell["module"]:
                positions.append(
                    {
                        "x": x,
                        "y": y,
                        "module": cell["module"],
                        "contribution": cell["total"],
                    }
                )
    return positions


def train_model(X_train, y_train, tech_modules):
    """Trains model to optimize module placement"""
    # Count modules matching our tech type plus empty and inactive states
    num_tech_modules = len([m for m in modules if m["tech"] == tech]) + 2

    model = xgb.XGBClassifier(
        num_class=num_tech_modules,
        objective="multi:softmax",
        eval_metric="merror",
        use_label_encoder=False,
    )

    # Convert one-hot encoded y to class indices
    y_train_indices = np.argmax(y_train, axis=1)

    model.fit(X_train, y_train_indices, verbose=True)

    return model


# --- Preprocessing and ML Training ---


def save_encoders(
    module_encoder,
    tech_encoder,
    type_encoder,
    scaler,
    tech,
    modules,
    filepath="data/encoders.json",
):
    # Serialize the fitted encoders and scaler to a JSON file

    tech_modules = [module for module in modules if module["tech"] == tech]
    all_modules = sorted(list(set([str(module["name"]) for module in tech_modules])))
    all_techs = sorted(list(set([str(module["tech"]) for module in tech_modules])))
    all_types = sorted(list(set([str(module["type"]) for module in tech_modules])))

    encoders_data = {
        "module_encoder_categories": [list(all_modules)],
        "tech_encoder_categories": [list(all_techs)],
        "type_encoder_categories": [list(all_types)],
        "scaler_mean": scaler.mean_.tolist(),
        "scaler_scale": scaler.scale_.tolist(),
        "scaler_var": scaler.var_.tolist(),
    }

    # Create the tech specific file name
    tech_filename = f"{filepath.replace('.json','')}_{tech}.json"  # changed to filepath

    # Check if the directory exists, if not create it
    directory = os.path.dirname(tech_filename)
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(tech_filename, "w") as f:
        json.dump(encoders_data, f, indent=4)


def load_encoders(filepath):
    """Load encoders from a JSON file."""
    with open(filepath, "r") as f:
        data = json.load(f)

    # Load encoders from saved data
    module_encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    module_encoder.categories_ = [
        np.array(cat) for cat in data["module_encoder_categories"]
    ]

    tech_encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    tech_encoder.categories_ = [
        np.array(cat) for cat in data["tech_encoder_categories"]
    ]

    type_encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    type_encoder.categories_ = [
        np.array(cat) for cat in data["type_encoder_categories"]
    ]

    scaler = StandardScaler()
    scaler.mean_ = np.array(data["scaler_mean"])
    scaler.scale_ = np.array(data["scaler_scale"])
    scaler.var_ = np.array(data["scaler_var"])

    return module_encoder, tech_encoder, type_encoder, scaler


def preprocess_data(data, modules, tech, debug=True):
    """Preprocesses data for ML."""
    tech_modules = [module for module in modules if module["tech"] == tech]
    # Unpack the existing data structure
    input_grids, optimized_grids, modules_list = zip(*data)

    # Convert both input and optimized grids to input format
    X_features = [grid_to_input(grid, tech_modules) for grid in input_grids]
    y_features = []

    # make the encoder here, so we can use it in grid_to_prediction()
    all_modules = sorted(
        list(set([str(module["name"]) for module in tech_modules]))
    )  # only get modules of the correct tech
    all_modules.append("") # Add "" as an accepted module.
    module_encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    module_encoder.fit(np.array(all_modules).reshape(-1, 1))

    for grid in optimized_grids:
        y_features.extend(
            grid_to_prediction(grid, tech_modules, tech, module_encoder)
        )  # changed this to only use tech modules

    # Flatten lists of lists
    X_features = [cell for grid in X_features for cell in grid]

    # Handle case where X_features or y_features is empty
    if not X_features or not y_features:
        print("Error: No data found for training. Skipping data processessing.")
        return np.array([]), np.array([]), None, None, None, None

    X = np.array(X_features)
    y = np.array(y_features)

    if debug:
        print("X shape before preprocessing:", X.shape)
        print("Sample X data before preprocessing:", X[:5])
        print("y shape:", np.array(y).shape)
        print("Sample y data:", np.array(y)[:5])

    # Separate features
    modules_data = np.array(X)[:, 0]  # Every nth element starting from 0
    techs = X[:, 1]  # Every nth element starting from 1
    types = X[:, 2]  # Every nth element starting from 2
    bonuses = np.array(X[:, 3].astype(np.float64))  # Every nth element starting from 3
    supercharged = np.array(
        X[:, 4].astype(np.int32)
    )  # Every nth element starting from 4
    active = X[:, 5].astype(np.int32)  # Every nth element starting from 5
    sc_eligible = np.array(
        X[:, 6].astype(np.int32)
    )  # Every nth element starting from 6

    # make all the modules, techs, and types
    all_techs = sorted(
        list(set([str(module["tech"]) for module in tech_modules]))
    )  # only get techs of the correct tech
    all_types = sorted(
        list(set([str(module["type"]) for module in tech_modules]))
    )  # only get types of the correct tech

    # One-Hot Encoding
    tech_encoder = OneHotEncoder(
        handle_unknown="ignore", sparse_output=False
    )  # removed min_frequency
    type_encoder = OneHotEncoder(
        handle_unknown="ignore", sparse_output=False
    )  # removed min_frequency

    tech_encoder.fit(np.array(all_techs).reshape(-1, 1))
    type_encoder.fit(np.array(all_types).reshape(-1, 1))

    # Replace None with empty strings for encoding
    modules_data[modules_data == None] = ""
    techs[techs == None] = ""
    types[types == None] = ""

    modules_encoded = module_encoder.transform(modules_data.reshape(-1, 1))
    techs_encoded = tech_encoder.transform(techs.reshape(-1, 1))
    types_encoded = type_encoder.transform(types.reshape(-1, 1))

    # Create y_modules_encoded here
    num_classes = len(tech_modules) + 2  # Modules + empty + inactive
    y_modules_encoded = np.zeros((len(y), num_classes))

    for index, cell in enumerate(y):
        if cell == -2:
            y_modules_encoded[index][1] = 1  # inactive
        elif cell == -1:
            y_modules_encoded[index][0] = 1  # empty
        else:
            y_modules_encoded[index][cell + 2] = 1  # add 2 to offset empty and inactive

    # Check if .toarray() is needed
    if hasattr(modules_encoded, "toarray"):
        modules_encoded = modules_encoded.toarray()
    if hasattr(techs_encoded, "toarray"):
        techs_encoded = techs_encoded.toarray()
    if hasattr(types_encoded, "toarray"):
        types_encoded = types_encoded.toarray()

    # Scale Numerical Features
    scaler = StandardScaler()
    bonuses_scaled = scaler.fit_transform(bonuses.reshape(-1, 1))

    # Combine the data again
    X_processed = np.concatenate(  # changed to numpy concat
        (
            modules_encoded,
            techs_encoded,
            types_encoded,
            bonuses_scaled,
            supercharged.reshape(-1, 1),
            active.reshape(-1, 1),
            sc_eligible.reshape(-1, 1),
        ),
        axis=1,
    )

    y_processed = y_modules_encoded  # changed to just use the modules

    if debug:
        print("X shape after preprocessing:", X_processed.shape)
        print("y shape after preprocessing:", y_processed.shape)

    return X_processed, y_processed, module_encoder, tech_encoder, type_encoder, scaler


def train_model(X_train, y_train, tech_modules):
    """Trains model to optimize module placement"""
    # Count modules matching our tech type plus empty and inactive states
    num_tech_modules = len(tech_modules) + 2

    model = xgb.XGBClassifier(
        num_class=num_tech_modules,
        objective="multi:softmax",
        eval_metric="merror",
    )

    # Convert one-hot encoded y to class indices
    y_train_indices = np.argmax(y_train, axis=1)

    model.fit(X_train, y_train_indices, verbose=True)

    return model


def grid_to_input(grid, tech_modules):
    """Convert Grid to a list of lists of features (suitable for ML)."""
    grid_data = []
    for row in grid.cells:
        for cell in row:
            # Handle module index
            module_index = -1  # Default for empty
            if not cell.get("active", True):
                module_index = -2  # Inactive cells get distinct index
            else:
                for index, module in enumerate(tech_modules):
                    if cell["module"] == module["name"]:
                        module_index = index
                        break

            bonus = cell.get("bonus", 0.0)
            supercharged = 1 if cell.get("supercharged", False) else 0
            active = 1 if cell.get("active", True) else 0
            sc_eligible = 1 if cell.get("sc_eligible", False) else 0
            tech = cell.get("tech", "")
            type = cell.get("type", "")

            grid_data.append(
                [
                    module_index,
                    tech,
                    type,
                    bonus,
                    supercharged,
                    active,
                    sc_eligible,
                ]
            )
    return grid_data


def grid_to_prediction(grid, tech_modules, tech, module_encoder):
    """Convert optimized Grid to a list of lists of features (suitable for ML)."""
    grid_data = []
    for row in grid.cells:
        for cell in row:
            module_index = -1  # empty
            if not cell.get("active", True):
                module_index = -2  # inactive
            elif cell["module"] is not None:
                for index, module in enumerate(tech_modules):
                    if cell["module"] == module["name"]:
                        module_index = index
                        break

            grid_data.append(module_index)

    return grid_data


def save_data(data, filename):
    """Save the training data to a JSON file."""
    # Check if the directory exists, if not create it
    directory = os.path.dirname(filename)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


def load_data(filename):
    """Load training data from a JSON file."""
    with open(filename, "r") as f:
        data = json.load(f)

    reconstructed_data = []
    for sample in data:
        reconstructed_input_grid = Grid.from_dict(sample["initial_state"])
        reconstructed_optimal_grid = Grid.from_dict(sample["optimal_state"])
        reconstructed_data.append(
            (
                reconstructed_input_grid,
                reconstructed_optimal_grid,
                sample["module_positions"],
            )
        )

    return reconstructed_data


if __name__ == "__main__":
    # Extract parameters from config
    width = config["width"]
    height = config["height"]
    tech = config["tech"]
    num_grids = config["num_grids"]
    test_size = config["test_size"]
    random_state = config["random_state"]
    data_file = config["data_file"]
    model_file = config["model_file"]
    debug = config["debug"]

    combined_data = generate_data_from_optimize_placement(
        num_grids, width, height, modules, tech, debug=debug
    )

    # Remove old training data if it exists
    if os.path.exists(data_file):
        os.remove(data_file)
    save_data(combined_data, data_file)
    print("Training data saved to data/training_data.json")

    # Load and preprocess
    data = load_data(data_file)

    tech_modules = [module for module in modules if module["tech"] == tech]
    X, y, module_encoder, tech_encoder, type_encoder, scaler = preprocess_data(
        data, modules, tech, debug=debug
    )  # added modules and tech here

    save_encoders(
        module_encoder,
        tech_encoder,
        type_encoder,
        scaler,
        tech,
        modules,
        "data/encoders.json",
    )  # added modules and tech here, and changed the filename

    if X.size == 0:
        print("Not enough data was made, skipping the rest of the code.")
    else:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )

    # Initialize and train the model
    model = train_model(X_train, y_train, tech_modules)

    # Make predictions
    predictions = model.predict(X_test)
    y_test_labels = np.argmax(y_test, axis=1)

    # Calculate accuracy
    correct_predictions = np.sum(predictions == y_test_labels)
    accuracy = correct_predictions / len(predictions)

    print(f"\nModel Performance:")
    print(f"Total predictions: {len(predictions)}")
    print(f"Correct predictions: {correct_predictions}")
    print(f"Accuracy: {accuracy:.2f}")

    # Save the model
    model.save_model(model_file)
    print(f"Model saved to {model_file}")
