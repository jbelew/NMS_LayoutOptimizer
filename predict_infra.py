import xgboost as xgb
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import json
import os
import sklearn

# Import necessary functions from other files (assuming these are in the same directory)
from nms_optimizer import Grid, place_module, modules, print_grid
from generate_training_data import grid_to_input


# --- Load Configuration ---
config = {
    "width": 4,
    "height": 3,
    "tech": "infra",
    "model_file": "model.json",
    "encoders_file": "data/encoders_infra.json",
    "debug": True,
}

def load_encoders(filepath):
    """Loads and potentially fits encoders from a JSON file."""
    module_encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False, min_frequency=0)
    tech_encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False, min_frequency=0)
    type_encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False, min_frequency=0)
    scaler = StandardScaler()

    try:
        with open(filepath, 'r') as f:
            data = json.load(f)

        # Load the categories directly
        module_encoder.categories_ = [np.array(data["module_encoder_categories"][0])]
        tech_encoder.categories_ = [np.array(data["tech_encoder_categories"][0])]
        type_encoder.categories_ = [np.array(data["type_encoder_categories"][0])]

        scaler.mean_ = np.array(data["scaler_mean"])
        scaler.scale_ = np.array(data["scaler_scale"])
        scaler.var_ = np.array(data["scaler_var"])

    except (FileNotFoundError, json.JSONDecodeError, KeyError, IndexError) as e:
        print(f"Warning: Error loading encoders from {filepath}: {e}. Encoders will be fitted later.")

    return module_encoder, tech_encoder, type_encoder, scaler

def preprocess_new_grid(grid, module_encoder, tech_encoder, type_encoder, scaler, tech_modules):
    """Preprocesses a new grid for ML prediction, handling unseen categories."""
    X = grid_to_input(grid, tech_modules)
    X = np.array(X)

    # Separate features
    modules_data = X[:, 0]
    techs = X[:, 1]
    types = X[:, 2]
    bonuses = X[:, 3].astype(np.float64)
    supercharged = X[:, 4].astype(np.int32)
    active = X[:, 5].astype(np.int32)
    sc_eligible = X[:, 6].astype(np.int32)

    #Handle potential missing values
    modules_data = np.where(modules_data == None, "", modules_data)
    techs = np.where(techs == None, "", techs)
    types = np.where(types == None, "", types)
    
    # Transforming the data
    modules_encoded = module_encoder.transform(modules_data.reshape(-1, 1))
    techs_encoded = tech_encoder.transform(techs.reshape(-1, 1))
    types_encoded = type_encoder.transform(types.reshape(-1, 1))

    #Check if sparse matrix and convert if needed
    if isinstance(modules_encoded, sklearn.sparse.csr.csr_matrix):
        modules_encoded = modules_encoded.toarray()
    if isinstance(techs_encoded, sklearn.sparse.csr.csr_matrix):
        techs_encoded = techs_encoded.toarray()
    if isinstance(types_encoded, sklearn.sparse.csr.csr_matrix):
        types_encoded = types_encoded.toarray()

    #Scale numerical features
    bonuses_scaled = scaler.transform(bonuses.reshape(-1, 1))

    # Concatenate features
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
    return X_processed


# --- Main Prediction Function ---
def predict_grid(grid, model, module_encoder, tech_encoder, type_encoder, scaler, tech_modules):
    """Predicts module placement for a given grid."""
    processed_grid = preprocess_new_grid(grid, module_encoder, tech_encoder, type_encoder, scaler, tech_modules)
    probabilities = model.predict_proba(processed_grid)
    predictions = np.argmax(probabilities, axis=1)
    return predictions


# --- Main Execution ---
if __name__ == "__main__":
    # Load the model
    model = xgb.XGBClassifier()
    model.load_model(config["model_file"])

    # Load encoders (will fit if necessary)
    module_encoder, tech_encoder, type_encoder, scaler = load_encoders(config["encoders_file"])

    #Larger Grid Data (replace with your actual grid loading)
    grid_data = {
        "cells": [
            [
                {"adjacency": False, "adjacency_bonus": 0.0, "bonus": 0.0, "image": None, "module": None, "sc_eligible": False, "supercharged": True, "tech": None, "total": 0.0, "type": "", "value": 0, "active": True},
                {"adjacency": False, "adjacency_bonus": 0.0, "bonus": 0.0, "image": None, "module": None, "sc_eligible": False, "supercharged": True, "tech": None, "total": 0.0, "type": "", "value": 0, "active": True},
                {"adjacency": False, "adjacency_bonus": 0.0, "bonus": 0.0, "image": None, "module": None, "sc_eligible": False, "supercharged": False, "tech": None, "total": 0.0, "type": "", "value": 0, "active": True},
                {"adjacency": False, "adjacency_bonus": 0.0, "bonus": 0.0, "image": None, "module": None, "sc_eligible": False, "supercharged": False, "tech": None, "total": 0.0, "type": "", "value": 0, "active": True},
            ],
            [
                {"adjacency": False, "adjacency_bonus": 0.0, "bonus": 0.0, "image": None, "module": None, "sc_eligible": False, "supercharged": False, "tech": None, "total": 0.0, "type": "", "value": 0, "active": True},
                {"adjacency": False, "adjacency_bonus": 0.0, "bonus": 0.0, "image": None, "module": None, "sc_eligible": False, "supercharged": False, "tech": None, "total": 0.0, "type": "", "value": 0, "active": True},
                {"adjacency": False, "adjacency_bonus": 0.0, "bonus": 0.0, "image": None, "module": None, "sc_eligible": False, "supercharged": False, "tech": None, "total": 0.0, "type": "", "value": 0, "active": True},
                {"adjacency": False, "adjacency_bonus": 0.0, "bonus": 0.0, "image": None, "module": None, "sc_eligible": False, "supercharged": False, "tech": None, "total": 0.0, "type": "", "value": 0, "active": True},
            ],
            [
                {"adjacency": False, "adjacency_bonus": 0.0, "bonus": 0.0, "image": None, "module": None, "sc_eligible": False, "supercharged": False, "tech": None, "total": 0.0, "type": "", "value": 0, "active": True},
                {"adjacency": False, "adjacency_bonus": 0.0, "bonus": 0.0, "image": None, "module": None, "sc_eligible": False, "supercharged": False, "tech": None, "total": 0.0, "type": "", "value": 0, "active": True},
                {"adjacency": False, "adjacency_bonus": 0.0, "bonus": 0.0, "image": None, "module": None, "sc_eligible": False, "supercharged": False, "tech": None, "total": 0.0, "type": "", "value": 0, "active": True},
                {"adjacency": False, "adjacency_bonus": 0.0, "bonus": 0.0, "image": None, "module": None, "sc_eligible": False, "supercharged": False, "tech": None, "total": 0.0, "type": "", "value": 0, "active": True}
            ]
        ],
        "height": 3,
        "width": 4
    }

    predefined_grid = Grid.from_dict(grid_data)
    print_grid(predefined_grid)

    # Get tech modules (assuming 'modules' is defined elsewhere - likely in nms_optimizer.py)
    tech_modules = [module for module in modules if module["tech"] == config["tech"]]

    # Make predictions
    predictions = predict_grid(predefined_grid, model, module_encoder, tech_encoder, type_encoder, scaler, tech_modules)

    print(f"Predictions: {predictions}")

    # Place modules (example - adapt to your placement logic)
    prediction_index = 0
    for row in range(predefined_grid.height):
        for col in range(predefined_grid.width):
            module_index = predictions[prediction_index]
            cell = predefined_grid.get_cell(col, row)
            if module_index == 0: #empty
                place_module(
                    predefined_grid,
                    col,
                    row,
                    None,
                    None,
                    None,
                    0,
                    False,
                    False,
                    None,
                )
            elif module_index == 1: # inactive
                cell["active"] = False
                place_module(
                    predefined_grid,
                    col,
                    row,
                    None,
                    None,
                    None,
                    0,
                    False,
                    False,
                    None,
                )
            elif module_index > 1:  # Offset for empty and inactive
                module_to_place = tech_modules[module_index - 2]  # Offset for empty and inactive
                place_module(
                    predefined_grid,
                    col,
                    row,
                    module_to_place["name"],
                    module_to_place["tech"],
                    module_to_place["type"],
                    module_to_place["bonus"],
                    module_to_place["adjacency"],
                    module_to_place["sc_eligible"],
                    module_to_place["image"],
                )
            prediction_index += 1

    print("\nGrid after module placement:")
    print_grid(predefined_grid)
