"""
API Module
==========

Provides Flask API endpoints for the prompt enhancement service:
- /health: Service health check and configuration info
- /enhance_prompt: Primary endpoint for enhancing user prompts
"""

import logging
from flask import Flask, request, jsonify, Response
from flask_cors import CORS

from agentic_skeleton.config import settings
from agentic_skeleton.core import prompt_processor

# Create Flask application
app = Flask(__name__)
# Enable CORS for all routes and origins
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/health", methods=["GET"])
def health_check() -> Response:
    """
    Health check endpoint to verify service status.
    
    Returns information about:
    - Service operational status
    - Whether mock mode is active
    - Which LLM model is configured
    - Current version

    Returns:
        JSON response with service status information
    """
    status = {
        "status": "healthy",
        "mode": "mock" if settings.is_using_mock() else "azure",
        "llm_model": settings.MODEL_PROMPT_ENHANCER, 
        "version": "1.1.0"
    }
    logging.info(f"Health check: {status}")
    return jsonify(status)

@app.route("/enhance_prompt", methods=["POST"])
def enhance_prompt() -> Response:
    """
    Primary endpoint for enhancing user prompts.
    
    The enhancement process:
    1. Extracts user_id and prompt from request body
    2. Uses the prompt_processor to transform the prompt based on:
       - User's skill level
       - RAG context matching
       - Skill-specific parameters
    3. Returns the enhanced response with embedded RAG extras
    
    Expects JSON payload: {"user_id": "string", "prompt": "string"}
    
    Returns:
        JSON response with {"enhanced_response": "string"} or error details
    """
    try:
        # Parse and validate the JSON request payload
        try:
            payload = request.get_json()
            if payload is None:
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

        # Validate required fields exist
        if not payload or 'user_id' not in payload or 'prompt' not in payload:
            error_msg = "Missing 'user_id' or 'prompt' field in payload"
            logging.warning(error_msg)
            return jsonify({
                "error": "Invalid Payload",
                "message": error_msg
            }), 400

        # Extract the payload fields
        user_id = payload["user_id"]
        user_prompt = payload["prompt"]

        # Validate field types
        if not isinstance(user_id, str) or not isinstance(user_prompt, str):
             error_msg = "'user_id' and 'prompt' fields must be strings"
             logging.warning(error_msg)
             return jsonify({
                 "error": "Invalid Payload Type",
                 "message": error_msg
             }), 400

        # Log the request (truncated for privacy/length)
        req_summary = user_prompt[:50] + ('...' if len(user_prompt) > 50 else '')
        logging.info(f"Processing prompt enhancement for user '{user_id}': '{req_summary}'")

        # Process the request through the prompt enhancement pipeline
        enhanced_response = prompt_processor.process_prompt_request(user_id, user_prompt)

        # Return the enhanced response
        logging.info(f"Successfully processed request for user '{user_id}'")
        return jsonify({
            "enhanced_response": enhanced_response
        })

    except Exception as e:
        # Catch-all for unexpected errors
        error_msg = f"Unexpected error: {str(e)}"
        logging.exception(error_msg)  # Log full traceback
        return jsonify({
            "error": "Internal Server Error",
            "message": "An unexpected error occurred while processing the request"
        }), 500