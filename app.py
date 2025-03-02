# app.py
from flask import Flask, jsonify, request
from nms_optimizer import simulated_annealing_optimization, Grid, modules

import logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

@app.route('/optimize', methods=['POST'])
def optimize_grid():
    data = request.get_json()
    logging.info(data)

    tech = data.get('tech')
    if tech is None:
        return jsonify({'error': 'No tech specified'}), 400

    grid_size = data.get('grid_size')
    if grid_size is None:
        return jsonify({'error': 'No grid size specified'}), 400

    initial_temp = data.get('initial_temp', 10000)
    cooling_rate = data.get('cooling_rate', 0.9999)
    max_iterations = data.get('max_iterations', 10000)
    patience = data.get('patience', 200)
    decay_factor = data.get('decay_factor', 0.99)

    grid = Grid(grid_size, grid_size)
    
    try:
        grid, max_bonus = simulated_annealing_optimization(grid, modules, "infra", initial_temp=10000, cooling_rate=0.9999, max_iterations=10000, patience=200, decay_factor=0.99)
        # optimized_grid, max_bonus = simulated_annealing_optimization(
        #     grid, modules, tech,
        #     initial_temp=initial_temp,
        #     cooling_rate=cooling_rate,
        #     max_iterations=max_iterations,
        #     patience=patience,
        #     decay_factor=decay_factor

        return jsonify({'grid': grid.to_dict(), 'max_bonus': max_bonus})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)