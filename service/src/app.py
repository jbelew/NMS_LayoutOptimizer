# app.py
from flask import Flask, jsonify, request, Response
from flask_cors import CORS

from optimizer import optimize_placement, get_tech_tree_json, Grid
from modules import modules
from optimization_algorithms import set_message_queue # Import the function

import logging
import json
import time
import threading
import queue

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Message queue for SSE
message_queue = queue.Queue()

# Set the message queue in optimization_algorithms
set_message_queue(message_queue)

def send_messages():
    """Generator function for SSE to send messages from the queue."""
    while True:
        message = message_queue.get()
        if message is None:
            break  # Signal to stop the thread
        yield f"data: {message}\n\n"
        time.sleep(0.1)  # Adjust as needed

@app.route('/stream')
def stream():
    """SSE endpoint to stream messages to the client."""
    return Response(send_messages(), mimetype='text/event-stream')

@app.route('/optimize', methods=['POST'])
def optimize_grid():
    """Endpoint to optimize the grid and send status updates via SSE."""
    data = request.get_json()

    ship = data.get("ship")
    tech = data.get('tech')
    if tech is None:
        return jsonify({'error': 'No tech specified'}), 400

    grid_data = data.get('grid')
    if grid_data is None:
        return jsonify({'error': 'No grid specified'}), 400

    grid = Grid.from_dict(grid_data)
    
    message_queue.put(json.dumps({"status": "info", "message": "Starting optimization..."}))
    grid, max_bonus = optimize_placement(grid, ship, modules, tech)
    message_queue.put(json.dumps({"status": "success", "message": "Optimization complete!"}))
    return jsonify({'grid': grid.to_dict(), 'max_bonus': max_bonus})
    
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
