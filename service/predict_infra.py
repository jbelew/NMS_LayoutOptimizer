import xgboost as xgb
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import json
import os
import sklearn
import pdb  # Import the debugger

# Import necessary functions from other files
from service.optimizer import Grid, place_module, modules, print_grid
from service.generate_training_data import grid_to_input

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
    module_encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
    tech_encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
    type_encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
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

def preprocess_new_grid(X, module_encoder, tech_encoder, type_encoder, scaler):
    """Preprocesses a new grid for ML prediction."""
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
    #We no longer handle empty values.
    #Transforming the data
    #replace all -1 with a string
    modules_data = np.where(modules_data == -1, "NO_MODULE", modules_data)

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
    X = grid_to_input(grid, tech_modules)
    processed_grid = preprocess_new_grid(X, module_encoder, tech_encoder, type_encoder, scaler)

    if processed_grid is None:
        print("Error: could not process new grid, exiting")
        return None

    probabilities = model.predict_proba(processed_grid)
    predictions = np.argmax(probabilities, axis=1)
    return predictions

# --- Main Execution ---
if __name__ == "__main__":
    # Load the model
    model = xgb.XGBClassifier()
    model.load_model(config["model_file"])

    # Load encoders
    module_encoder, tech_encoder, type_encoder, scaler = load_encoders(config["encoders_file"])

    #Larger Grid Data (replace with your actual grid loading)
    grid_data = {
        "cells": [
            [
                {"adjacency": False, "adjacency_bonus": 0.0, "bonus": 0.0, "image": None, "module": None, "sc_eligible": False, "supercharged": True, "tech": None, "total": 0.0, "type": "", "value": 0, "active": True},
                {"adjacency": False, "adjacency_bonus": 0.0, "bonus": 0.0, "image": None, "module": None, "sc_eligible": False, "supercharged": True, "tech": None, "total": 0.0, "type": "", "value": 0, "active": True},
                {"adjacency": False, "adjacency_bonus": 0.0, "bonus": 0.0, "image": None, "module": None, "sc_eligible": False, "supercharged": False, "tech": None, "total": 0.0, "type": "", "value": 0, "active": True},
                {"adjacency": False, "adjacency_bonus": 0.0, "bonus": 0.0, "image": None, "module": None, "sc_eligible": False, "supercharged": False, "tech": None, "total": 0.0, "type": "", "value": 0, "active": True}
            ],
            [
                {"adjacency": False, "adjacency_bonus": 0.0, "bonus": 0.0, "image": None, "module": None, "sc_eligible": False, "supercharged": False, "tech": None, "total": 0.0, "type": "", "value": 0, "active": True},
                {"adjacency": False, "adjacency_bonus": 0.0, "bonus": 0.0, "image": None, "module": None, "sc_eligible": False, "supercharged": False, "tech": None, "total": 0.0, "type": "", "value": 0, "active": True},
                {"adjacency": False, "adjacency_bonus": 0.0, "bonus": 0.0, "image": None, "module": None, "sc_eligible": False, "supercharged": False, "tech": None, "total": 0.0, "type": "", "value": 0, "active": True},
                {"adjacency": False, "adjacency_bonus": 0.0, "bonus": 0.0, "image": None, "module": None, "sc_eligible": False, "supercharged": False, "tech": None, "total": 0.0, "type": "", "value": 0, "active": True}
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
    print(json.dumps(predefined_grid.to_dict(), indent=4)) #print it here.

    # Get tech modules
    tech_modules = [module for module in modules if module["tech"] == config["tech"]]

    # Make predictions
    predictions = predict_grid(predefined_grid, model, module_encoder, tech_encoder, type_encoder, scaler, tech_modules)

    if predictions is None:
        print("Error: Predictions were not able to be made.")
    else:
        print(f"Predictions: {predictions}")

        # Place modules (example - adapt to your placement logic)
        prediction_index = 0
        for row in range(predefined_grid.height):
            for col in range(predefined_grid.width):
                module_index = predictions[prediction_index]
                cell = predefined_grid.get_cell(col, row)
                if module_index == 0:  # empty
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
                elif module_index == 1:  # inactive
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
                    module_to_place = tech_modules[module_index - 2]
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
