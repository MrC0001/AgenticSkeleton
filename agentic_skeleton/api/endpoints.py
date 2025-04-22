"""
API Module
==========

Provides the Flask API endpoints for the AgenticSkeleton application.
"""

import logging
from flask import Flask, request, jsonify, Response

from agentic_skeleton.config import settings
# Update imports to use the new modular structure properly
from agentic_skeleton.core.mock_core import generate_mock_plan_and_results
from agentic_skeleton.core.azure_core import generate_azure_plan_and_results

# Create Flask application
app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health_check() -> Response:
    """
    Health check endpoint to verify service status.
    
    Returns:
        JSON response with service status information
    """
    status = {
        "status": "healthy",
        "mode": "mock" if settings.is_using_mock() else "azure",
        "version": "1.0.0"
    }
    logging.info(f"Health check: {status}")
    return jsonify(status)

@app.route("/run-agent", methods=["POST"])
def run_agent() -> Response:
    """
    Main endpoint for the agent to process user requests.
    
    Returns:
        JSON response with plan and results
    """
    try:
        # Get user request from JSON payload
        try:
            payload = request.get_json()
            if payload is None:  # A.k.a JSON is malformed
                logging.warning("Malformed JSON in request")
                return jsonify({
                    "error": "Malformed JSON",
                    "message": "The request contains invalid JSON"
                }), 400
        except Exception as e:
            logging.warning(f"Error parsing JSON: {str(e)}")
            return jsonify({
                "error": "Malformed JSON",
                "message": str(e)
            }), 400
            
        if not payload or 'request' not in payload:
            error_msg = "Missing 'request' field in payload"
            logging.warning(error_msg)
            return jsonify({
                "error": error_msg,
                "message": "Please provide a 'request' field in your JSON payload"
            }), 400
            
        user_req = payload["request"]
        req_summary = user_req[:50] + ('...' if len(user_req) > 50 else '')
        logging.info(f"Processing request: '{req_summary}'")
        
        # Process the request
        if settings.is_using_mock():
            subtasks, results = generate_mock_plan_and_results(user_req)
        else:
            subtasks, results = generate_azure_plan_and_results(user_req)
            
        # Return the plan and results
        logging.info(f"Successfully processed request with {len(subtasks)} subtasks")
        return jsonify({
            "plan": subtasks,
            "results": results
        })
        
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        logging.error(error_msg)
        return jsonify({
            "error": error_msg,
            "message": "An unexpected error occurred while processing the request"
        }), 500