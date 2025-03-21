# app.py
from flask import Flask, jsonify, request
from flask_cors import CORS

from optimizer import simulated_annealing_optimization, get_tech_tree_json, Grid
from modules_refactored import modules

import logging
import json
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app)  # This will allow all domains by default

@app.route('/optimize', methods=['POST'])
def optimize_grid():
    data = request.get_json()
    #logging.info(data)

    # raw_data = request.data.decode('utf-8')  # Raw request body
    # print("Raw request body:", raw_data)

    # json_data = request.get_json()
    # print("Parsed JSON:", json_data)

    ship = data.get("ship")
    tech = data.get('tech')
    if tech is None:
        return jsonify({'error': 'No tech specified'}), 400

    initial_temp = data.get('initial_temp', 10000)
    cooling_rate = data.get('cooling_rate', 0.9999)
    max_iterations = data.get('max_iterations', 10000)
    patience = data.get('patience', 200)
    decay_factor = data.get('decay_factor', 0.99)

    grid_data = data.get('grid')
    if grid_data is None:
        return jsonify({'error': 'No grid specified'}), 400

    grid = Grid.from_dict(grid_data)
    
    try:
        grid, max_bonus = simulated_annealing_optimization(grid, ship, modules, tech, initial_temp, cooling_rate, max_iterations, patience, decay_factor)
        return jsonify({'grid': grid.to_dict(), 'max_bonus': max_bonus})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/tech_tree/<ship_name>')
def get_technology_tree(ship_name):
    """Endpoint to get the technology tree for a given ship."""
    try:
        tree_data = get_tech_tree_json(ship_name)  # Get JSON data
        return tree_data  # Directly return the JSON response from get_tech_tree_json

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)