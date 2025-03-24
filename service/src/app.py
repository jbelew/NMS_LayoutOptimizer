# app.py
from flask import Flask, jsonify, request, Response
from flask_cors import CORS

from optimizer import optimize_placement, get_tech_tree_json, Grid
from modules import modules
from optimization_algorithms import set_message_queue  # Import the function

import logging
import time
import json
import queue

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)  # Get a logger instance

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Message queue for SSE
message_queue = queue.Queue()

# Set the message queue in optimization_algorithms
set_message_queue(message_queue)


def format_sse(data: str, event=None) -> str:
    """Formats the data into an SSE message."""
    msg = f"data: {data}\n\n"
    if event is not None:
        msg = f"event: {event}\n{msg}"
    return msg


def send_messages():
    """Generator function for SSE to send messages from the queue."""
    while True:
        message = message_queue.get()
        if message is None:
            break  # Signal to stop the thread
        logger.info(f"Sending message: {message}")  # Log the message being sent
        yield format_sse(json.dumps(message))
        time.sleep(0.1)  # Adjust as needed


@app.route("/stream")
def stream():
    """SSE endpoint to stream messages to the client."""
    logger.info("Client connected to /stream")  # Log when a client connects
    return Response(send_messages(), mimetype="text/event-stream")


@app.route("/optimize", methods=["POST"])
def optimize_grid():
    """Endpoint to optimize the grid and send status updates via SSE."""
    logger.info("Received optimization request")  # Log when the endpoint is hit
    data = request.get_json()

    ship = data.get("ship")
    tech = data.get("tech")
    clientUUID = data.get("clientUUID")  # Get the client UUID
    if tech is None:
        logger.error("No tech specified in optimization request")
        return jsonify({"error": "No tech specified"}), 400
    if clientUUID is None:
        logger.error("No clientUUID specified in optimization request")
        return jsonify({"error": "No clientUUID specified"}), 400

    grid_data = data.get("grid")
    if grid_data is None:
        logger.error("No grid specified in optimization request")
        return jsonify({"error": "No grid specified"}), 400

    grid = Grid.from_dict(grid_data)

    message_data = {
        "status": "info",
        "message": "Starting optimization...",
        "clientUUID": clientUUID,  # Include the client UUID in the message
    }
    logger.info(f"Adding message to queue: {message_data}")  # Log the message
    message_queue.put(message_data)
    try:
        grid, max_bonus = optimize_placement(grid, ship, modules, tech)
    except Exception as e:
        logger.error(f"Error during optimization: {e}")
        error_message_data = {
            "status": "error",
            "message": f"Optimization failed: {e}",
            "clientUUID": clientUUID,
        }
        logger.info(f"Adding message to queue: {error_message_data}")
        message_queue.put(error_message_data)
        return jsonify({"error": str(e)}), 500

    message_data = {
        "status": "success",
        "message": "Optimization complete!",
        "clientUUID": clientUUID,  # Include the client UUID in the message
    }
    logger.info(f"Adding message to queue: {message_data}")  # Log the message
    message_queue.put(message_data)

    return jsonify({"grid": grid.to_dict(), "max_bonus": max_bonus})


@app.route("/tech_tree/<ship_name>")
def get_technology_tree(ship_name):
    """Endpoint to get the technology tree for a given ship."""
    logger.info(f"Received request for tech tree: {ship_name}")
    try:
        tree_data = get_tech_tree_json(ship_name)  # Get JSON data
        return tree_data  # Directly return the JSON response from get_tech_tree_json

    except Exception as e:
        logger.error(f"Error getting tech tree: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
