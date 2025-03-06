import xgboost as xgb
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import json
import os
import random

# Import from the other files
from nms_optimizer import (
    Grid,
    optimize_placement,
    place_module,
    modules,
    print_grid,
)

# --- Load Configuration ---
config = {
    "width": 4,
    "height": 3,
    "tech": "infra",
    "model_file": "model.json",
    "debug": True,
    "xgb_params": {
        "objective": "multi:softmax",  # changed this line
        "eval_metric": "merror",  # changed this line
        "eta": 0.1,
        "max_depth": 6,
    },
}

# --- Helper Functions from generate_training_data.py (modified slightly) ---

def grid_to_input(grid):
    """Convert Grid to a list of lists of features (suitable for ML)."""
    grid_data = []
    for row in grid.cells:
        for cell in row:
            bonus = cell.get("bonus", 0.0)
            supercharged = 1 if cell.get("supercharged", False) else 0
            active = 1 if cell.get("active", False) else 0
            sc_eligible = 1 if cell.get("sc_eligible", False) else 0

            module = cell.get("module", "")  # Changed to ""
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

def load_encoders(filepath, modules, tech):
    """Load encoders from a JSON file."""
    # Load the tech specific file
    tech_filepath = f"{filepath.replace('.json','')}_{tech}.json" #changed to filepath
    with open(tech_filepath, "r") as f:
        data = json.load(f)
    
    tech_modules = [module for module in modules if module["tech"] == tech]
    all_modules = sorted(list(set([str(module["name"]) for module in tech_modules])))
    all_techs = sorted(list(set([str(module["tech"]) for module in tech_modules])))
    all_types = sorted(list(set([str(module["type"]) for module in tech_modules])))

    # Load encoders from saved data
    module_encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False) #removed min_frequency
    module_encoder.fit(np.array(all_modules).reshape(-1, 1))
    module_encoder.categories_ = [np.array(cat) for cat in data["module_encoder_categories"]]

    tech_encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False) #removed min_frequency
    tech_encoder.fit(np.array(all_techs).reshape(-1, 1))
    tech_encoder.categories_ = [np.array(cat) for cat in data["tech_encoder_categories"]]

    type_encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False) #removed min_frequency
    type_encoder.fit(np.array(all_types).reshape(-1, 1))
    type_encoder.categories_ = [np.array(cat) for cat in data["type_encoder_categories"]]

    scaler = StandardScaler()
    scaler.mean_ = np.array(data["scaler_mean"])
    scaler.scale_ = np.array(data["scaler_scale"])
    scaler.var_ = np.array(data["scaler_var"])

    return module_encoder, tech_encoder, type_encoder, scaler

def preprocess_new_grid(grid, module_encoder, tech_encoder, type_encoder, scaler, modules, tech, debug=True):
    """Preprocesses a new grid for ML prediction."""
    tech_modules = [module for module in modules if module["tech"] == tech]
    # Convert grid to list of lists
    X = grid_to_input(grid)
    X = np.array(X)

    # Separate features
    modules_data = np.array(X)[:, 0]  # Every nth element starting from 0
    techs = np.array(X)[:, 1]  # Every nth element starting from 1
    types = np.array(X)[:, 2]  # Every nth element starting from 2
    bonuses = np.array(X)[:, 3].astype(np.float64)  # Every nth element starting from 3
    supercharged = np.array(X)[:, 4].astype(np.int32)  # Every nth element starting from 4
    active = np.array(X)[:, 5].astype(np.int32)  # Every nth element starting from 5
    sc_eligible = np.array(X)[:, 6].astype(np.int32)  # Every nth element starting from 6

    # One-Hot Encoding
    # Replace None values with empty strings for one-hot encoding
    modules_data[modules_data == None] = ""
    techs[techs == None] = ""
    types[types == None] = ""

    # ---Handle Unknown---
    # If the category is not found in training data, it will be filled with all 0s
    def transform_with_unknown(encoder, data):
        # Convert data to a 2D array if it's not already
        if len(data.shape) == 1:
            data = data.reshape(-1, 1)
        encoded = encoder.transform(data)
        if hasattr(encoded, "toarray"):
            encoded = encoded.toarray()
        return encoded

    modules_encoded = transform_with_unknown(module_encoder, modules_data.reshape(-1, 1))
    techs_encoded = transform_with_unknown(tech_encoder, techs.reshape(-1, 1))
    types_encoded = transform_with_unknown(type_encoder, types.reshape(-1, 1))
    # ---End Handle Unknown---
    
    # Scale Numerical Features
    bonuses_scaled = scaler.transform(bonuses.reshape(-1, 1))

    # Combine the data again
    X_processed = np.concatenate(
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

    if debug:
        print("X shape after preprocessing:", X_processed.shape)

    return X_processed


# --- Main Execution ---
if __name__ == "__main__":
    # Extract parameters from config
    tech = config["tech"]
    # --- Load the Trained XGBoost Model ---
    model_file = config["model_file"]
    try:
        model = xgb.Booster()
        model.load_model(model_file)
    except xgb.core.XGBoostError:
        print("Error: Could not load model. Please run generate_training_data.py first.")
        exit()

    # --- Load encoders ---
    module_encoder, tech_encoder, type_encoder, scaler = load_encoders("data/encoders.json", modules, tech) #added modules here

    # --- Create a New Grid ---
    # We will now load the input grid from a dict
    grid_data = {
        "cells": [
            [
                {"adjacency": False, "adjacency_bonus": 0.0, "bonus": 0.0, "image": None, "module": None, "sc_eligible": False, "supercharged": True, "tech": "infra", "total": 0.0, "type": "", "value": 0, "active": True},
                {"adjacency": False, "adjacency_bonus": 0.0, "bonus": 0.0, "image": None, "module": None, "sc_eligible": False, "supercharged": True, "tech": "infra", "total": 0.0, "type": "", "value": 0, "active": True},
                {"adjacency": False, "adjacency_bonus": 0.0, "bonus": 0.0, "image": None, "module": None, "sc_eligible": False, "supercharged": False, "tech": "infra", "total": 0.0, "type": "", "value": 0, "active": True},
                {"adjacency": False, "adjacency_bonus": 0.0, "bonus": 0.0, "image": None, "module": None, "sc_eligible": False, "supercharged": False, "tech": "infra", "total": 0.0, "type": "", "value": 0, "active": True},
            ],
            [
                {"adjacency": False, "adjacency_bonus": 0.0, "bonus": 0.0, "image": None, "module": None, "sc_eligible": False, "supercharged": False, "tech": "infra", "total": 0.0, "type": "", "value": 0, "active": True},
                {"adjacency": False, "adjacency_bonus": 0.0, "bonus": 0.0, "image": None, "module": None, "sc_eligible": False, "supercharged": False, "tech": "infra", "total": 0.0, "type": "", "value": 0, "active": True},
                {"adjacency": False, "adjacency_bonus": 0.0, "bonus": 0.0, "image": None, "module": None, "sc_eligible": False, "supercharged": False, "tech": "infra", "total": 0.0, "type": "", "value": 0, "active": True},
                {"adjacency": False, "adjacency_bonus": 0.0, "bonus": 0.0, "image": None, "module": None, "sc_eligible": False, "supercharged": False, "tech": "infra", "total": 0.0, "type": "", "value": 0, "active": True},
            ],
            [
                {"adjacency": False, "adjacency_bonus": 0.0, "bonus": 0.0, "image": None, "module": None, "sc_eligible": False, "supercharged": False, "tech": "infra", "total": 0.0, "type": "", "value": 0, "active": True},
                {"adjacency": False, "adjacency_bonus": 0.0, "bonus": 0.0, "image": None, "module": None, "sc_eligible": False, "supercharged": False, "tech": "infra", "total": 0.0, "type": "", "value": 0, "active": True},
                {"adjacency": False, "adjacency_bonus": 0.0, "bonus": 0.0, "image": None, "module": None, "sc_eligible": False, "supercharged": False, "tech": "infra", "total": 0.0, "type": "", "value": 0, "active": True},
                {"adjacency": False, "adjacency_bonus": 0.0, "bonus": 0.0, "image": None, "module": None, "sc_eligible": False, "supercharged": False, "tech": "infra", "total": 0.0, "type": "", "value": 0, "active": True}
            ]
        ],
        "height": 3,
        "width": 4
    }
    new_grid = Grid(config["width"], config["height"])
    for y, row in enumerate(grid_data["cells"]):
        for x, cell_data in enumerate(row):
            cell = new_grid.get_cell(x, y)
            cell.update({
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
            })

    
    # --- Preprocess the New Grid ---
    tech_modules = [module for module in modules if module["tech"] == tech]
    new_grid_processed = preprocess_new_grid(new_grid, module_encoder, tech_encoder, type_encoder, scaler, modules, config["tech"])

    # --- Make a Prediction ---
    dnew_grid = xgb.DMatrix(new_grid_processed)
    predictions = model.predict(dnew_grid).astype(int) #added .astype(int)

    # --- Place Modules Based on Predictions ---
    prediction_index = 0
    for row in range(new_grid.height):
        for col in range(new_grid.width):
            module_index = predictions[prediction_index] #get the prediction for this cell
            if module_index != -1:
                current_module = tech_modules[module_index] #Changed to only show modules that match the tech
                place_module(
                    new_grid,
                    col,
                    row,
                    current_module["name"],
                    current_module["tech"],
                    current_module["type"],
                    current_module["bonus"],
                    current_module["adjacency"],
                    current_module["sc_eligible"],
                    current_module["image"],
                )
            prediction_index +=1

    # --- Print the Grid and the Prediction ---
    print("New Grid:")
    print_grid(new_grid)
    print(f"Prediction:")
    print(json.dumps(predictions.tolist()))



