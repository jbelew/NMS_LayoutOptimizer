import random
import json
import os
from sklearn.model_selection import train_test_split
import xgboost as xgb
from sklearn.metrics import mean_squared_error
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder

# Import from the other files
from nms_optimizer import (
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
    "num_grids": 100,
    "test_size": 0.2,
    "random_state": 42,
    "data_file": "data/training_data.json",
    "model_file": "model.json",
    "debug": True,
    "xgb_params": {
        "objective": "reg:squarederror",
        "eval_metric": "rmse",
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

def set_grid_state(grid, width, height, num_inactive_percentage=0.10, num_supercharged_max=4):
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

    # Set supercharged cells (random number between 0 and 4)
    num_supercharged = random.randint(0, 4)

    #create a new active cell list
    active_cells = [cell for cell in all_cells if cell not in inactive_cells]
    if len(active_cells) >= num_supercharged:
        supercharged_cells = random.sample(active_cells, num_supercharged)
    else:
        supercharged_cells = active_cells
    
    for x, y in all_cells:
        grid.set_supercharged(x,y,False) #set all to false first
    for x, y in supercharged_cells:
        grid.set_supercharged(x, y, True)

def populate_grid(grid, modules, tech):
    """Populates the grid with modules of the specified technology."""
    tech_modules = [module for module in modules if module["tech"] == tech]
    available_positions = [(x, y) for y in range(grid.height) for x in range(grid.width) if grid.get_cell(x, y)["active"]]
    random.shuffle(available_positions)

    for module in tech_modules:
        if available_positions:
            x, y = available_positions.pop()
            place_module(grid, x, y, module["name"], module["tech"], module["type"], module["bonus"], module["adjacency"], module["sc_eligible"], module["image"])
    return grid

# --- Data Generation ---

def generate_data_from_optimize_placement(num_grids, width, height, modules, tech, debug=False):
    data = []
    for _ in range(num_grids):
        empty_grid = generate_empty_grid(width, height)
        set_grid_state(empty_grid, width, height)

        optimal_grid, optimal_bonus = optimize_placement(empty_grid, modules, tech)

        if optimal_grid is None:
            print("optimize_placement returned None. Skipping this grid.")
            continue

        input_features = grid_to_input(optimal_grid)  
        output_label = optimal_bonus
        data.append((input_features, output_label))

        if debug:
            print(f"Optimal Bonus: {optimal_bonus}")
            print_grid(optimal_grid)

    return data

# --- Preprocessing and ML Training ---
def save_encoders(module_encoder, tech_encoder, type_encoder, scaler, filename="data/encoders.json"):
    # Serialize the fitted encoders and scaler to a JSON file
    encoders_data = {
        "module_encoder_categories": [list(cat) for cat in module_encoder.categories],
        "tech_encoder_categories": [list(cat) for cat in tech_encoder.categories],
        "type_encoder_categories": [list(cat) for cat in type_encoder.categories],
        "scaler_mean": scaler.mean_.tolist(),
        "scaler_scale": scaler.scale_.tolist(),
        "scaler_var": scaler.var_.tolist(),
    }

    # Check if the directory exists, if not create it
    directory = os.path.dirname(filename)
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    with open(filename, "w") as f:
        json.dump(encoders_data, f, indent=4)

def load_encoders(filepath):
    """Load encoders from a JSON file."""
    with open(filepath, "r") as f:
        data = json.load(f)

    # Load encoders from saved data
    module_encoder = OneHotEncoder(handle_unknown="ignore")
    module_encoder.categories = [np.array(cat) for cat in data["module_encoder_categories"]]
    tech_encoder = OneHotEncoder(handle_unknown="ignore")
    tech_encoder.categories = [np.array(cat) for cat in data["tech_encoder_categories"]]
    type_encoder = OneHotEncoder(handle_unknown="ignore")
    type_encoder.categories = [np.array(cat) for cat in data["type_encoder_categories"]]

    scaler = StandardScaler()
    scaler.mean_ = np.array(data["scaler_mean"])
    scaler.scale_ = np.array(data["scaler_scale"])
    scaler.var_ = np.array(data["scaler_var"])

    return module_encoder, tech_encoder, type_encoder, scaler

def preprocess_data(data, debug=True):
    """Preprocesses data for ML."""
    if not data or not isinstance(data, list) or len(data) == 0:
        print("Warning: No data to preprocess.")
        return np.empty((0, 0)), np.empty(0)

    X, y = zip(*data)  
    X = np.array([np.array(sublist).flatten() for sublist in X])
    y = np.array(y)   

    if debug:
        print("X shape before preprocessing:", X.shape)
        print("Sample X data before preprocessing:", X[:5])
        print("y shape:", np.array(y).shape)
        print("Sample y data:", np.array(y)[:5])

    
    # Separate features
    num_features = X.shape[1]
    modules_data = X[:, 0::7]  # Every 7th element starting from 0
    techs = X[:, 1::7]  # Every 7th element starting from 1
    types = X[:, 2::7]  # Every 7th element starting from 2
    bonuses = X[:, 3::7].astype(np.float64)  # Every 7th element starting from 3
    supercharged = X[:, 4::7].astype(np.int32)  # Every 7th element starting from 4
    active = X[:, 5::7].astype(np.int32)  # Every 7th element starting from 5
    sc_eligible = X[:, 6::7].astype(np.int32)  # Every 7th element starting from 6
    
    # One-Hot Encoding
    module_encoder = OneHotEncoder(handle_unknown="ignore")
    tech_encoder = OneHotEncoder(handle_unknown="ignore")
    type_encoder = OneHotEncoder(handle_unknown="ignore")
    
    # Scale Numerical Features
    scaler = StandardScaler()
    
    if X.size != 0:
        module_encoder = module_encoder.fit(modules_data.flatten().reshape(-1, 1))
        tech_encoder = tech_encoder.fit(techs.flatten().reshape(-1, 1))
        type_encoder = type_encoder.fit(types.flatten().reshape(-1, 1))
        scaler = scaler.fit(bonuses.flatten().reshape(-1, 1))
    else:
        module_encoder = module_encoder.fit([[""]])
        tech_encoder = tech_encoder.fit([[""]])
        type_encoder = type_encoder.fit([[""]])
        scaler = scaler.fit([[0]])

    modules_encoded = module_encoder.transform(modules_data.flatten().reshape(-1, 1)).toarray().reshape(X.shape[0], -1)
    techs_encoded = tech_encoder.transform(techs.flatten().reshape(-1, 1)).toarray().reshape(X.shape[0], -1)
    types_encoded = type_encoder.transform(types.flatten().reshape(-1, 1)).toarray().reshape(X.shape[0], -1)
    bonuses_scaled = scaler.transform(bonuses.flatten().reshape(-1, 1)).reshape(X.shape[0], -1)

    # Combine the data again
    X_processed = np.concatenate(
        (
            modules_encoded,
            techs_encoded,
            types_encoded,
            bonuses_scaled,
            supercharged,
            active,
            sc_eligible,
        ),
        axis=1,
    )

    if debug:
        print("X shape after preprocessing:", X_processed.shape)
        # print("Sample X data after preprocessing:", X_processed[:5])

    return X_processed, np.array(y), module_encoder, tech_encoder, type_encoder, scaler

def train_model(X_train, y_train, xgb_params):
    """Trains an XGBoost model."""
    dtrain = xgb.DMatrix(data=X_train, label=y_train)
    model = xgb.train(xgb_params, dtrain)
    return model

def grid_to_input(grid):
    """Convert Grid to a list of lists of features (suitable for ML)."""
    grid_data = []
    for row in grid.cells:
        for cell in row:
            bonus = cell.get("bonus", 0.0)
            supercharged = 1 if cell.get("supercharged", False) else 0
            active = 1 if cell.get("active", False) else 0
            sc_eligible = 1 if cell.get("sc_eligible", False) else 0

            module = cell.get("module", "")
            tech = cell.get("tech", "")
            type = cell.get("type", "")

            grid_data.append(
                [
                    module,
                    tech,
                    type,
                    bonus,
                    supercharged,
                    active,
                    sc_eligible,
                ]
            )
    return grid_data

def convert_data_for_json(data):
    """Convert data containing NumPy arrays to a JSON-serializable format."""
    json_ready_data = []
    if not data:
        return json_ready_data  # return empty list if there is no data
    for item in data:
        if isinstance(item, (list, tuple)):
            new_item = []
            for sub_item in item:
                if isinstance(sub_item, (list, tuple)):
                    new_sub_item = []
                    for sub_sub_item in sub_item:
                        if isinstance(sub_sub_item, np.ndarray):
                           new_sub_item.append(sub_sub_item.tolist())
                        else:
                            new_sub_item.append(sub_sub_item)
                    new_item.append(new_sub_item)
                elif isinstance(sub_item, np.ndarray):
                    new_item.append(sub_item.tolist())
                else:
                    new_item.append(sub_item)
            json_ready_data.append(new_item)

        elif isinstance(item, np.ndarray):
             json_ready_data.append(item.tolist())

        else:
            json_ready_data.append(item)
    return json_ready_data
    

def save_data(data, filename):
    """Save the training data to a JSON file."""
    # Check if the directory exists, if not create it
    directory = os.path.dirname(filename)
    if not os.path.exists(directory):
        os.makedirs(directory)
    json_ready_data = convert_data_for_json(data)
    #print(json_ready_data)
    with open(filename, "w") as f:
        json.dump(json_ready_data, f, indent=4)

def load_data(filename):
    """Load training data from a JSON file."""
    with open(filename, "r") as f:
        data = json.load(f)
    return data

# --- Main Execution ---

if __name__ == "__main__":
    # Extract parameters from config
    width = config["width"]
    height = config["height"]
    tech = config["tech"]
    num_grids = config['num_grids']
    test_size = config["test_size"]
    random_state = config["random_state"]
    data_file = config["data_file"]
    model_file = config["model_file"]
    debug = config["debug"]
    xgb_params = config["xgb_params"]

    combined_data = generate_data_from_optimize_placement(num_grids, width, height, modules, tech, debug=debug)

    # Remove old training data if it exists
    if os.path.exists(data_file):
        os.remove(data_file)
    save_data(combined_data, data_file)
    print("Training data saved to data/training_data.json")

    # Load and preprocess
    data = load_data(data_file)
    X, y, module_encoder, tech_encoder, type_encoder, scaler = preprocess_data(data, debug=debug)
    
    save_encoders(module_encoder, tech_encoder, type_encoder, scaler)

    if X.size == 0:
        print("Not enough data was made, skipping the rest of the code.")
    else:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

        # Train and evaluate
        model = train_model(X_train, y_train, xgb_params)
        dtest = xgb.DMatrix(data=X_test)
        predictions = model.predict(dtest)
        rmse = mean_squared_error(y_test, predictions, squared=False)
        print(f"RMSE: {rmse}")

        # Save Model
        model.save_model(model_file)
        print(f"Model saved to {model_file}")

