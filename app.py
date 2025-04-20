"""
Agentic Skeleton App
====================

A simple Flask API that provides an AI agent with dual operation modes:
1. Mock responses (default for local development without API keys)
2. Azure OpenAI API integration (for production deployments)

Environment Variables:
---------------------
    MOCK_RESPONSES:        Set to "false" to use Azure OpenAI API (default: "true")
    AZURE_OPENAI_KEY:      Your Azure OpenAI API key (required if not in mock mode)
    AZURE_OPENAI_ENDPOINT: Your Azure OpenAI endpoint (required if not in mock mode)
    MODEL_PLANNER:         Model for planning (default: "gpt-4")
    MODEL_EXECUTOR:        Model for execution (default: "gpt-4")
    PORT:                  Server port (default: 8000)
    FLASK_ENV:             Flask environment (default: development)
"""

import os
import sys
import logging
from typing import Dict, List, Any, Optional, Tuple, Union

from flask import Flask, request, jsonify, Response
from dotenv import load_dotenv

# Set up basic logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    stream=sys.stdout
)

# Optional: Import Azure OpenAI only when needed
try:
    from openai import AzureOpenAI
except ImportError:
    logging.info("OpenAI package not installed. Mock mode will still work fine.")

# --------------- Configuration ---------------

load_dotenv()

# Mode configuration

USE_MOCK = os.getenv("MOCK_RESPONSES", "true").lower() == "true"

# Azure OpenAI configuration (only used in production mode)
AZURE_KEY = os.getenv("AZURE_OPENAI_KEY")
AZURE_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_API_VERSION = "2023-05-15"  # Current stable version

# Model configuration
MODEL_PLANNER = os.getenv("MODEL_PLANNER", "gpt-4")
MODEL_EXECUTOR = os.getenv("MODEL_EXECUTOR", "gpt-4")

# Server configuration
PORT = int(os.getenv("PORT", "8000"))

# --------------- Prompt Templates ---------------


PLANNER_TEMPLATE = (
    "You are a task planning assistant.\n"
    "Decompose the following user request into a numbered list of discrete subtasks:\n\n"
    "\"{user_request}\"\n\n"
    "1."
)


EXECUTOR_TEMPLATE = (
    "You are an execution assistant.\n"
    "Perform the subtask below, and respond with just the result:\n\n"
    "Subtask: {subtask}"
)

# --------------- Mock Data ---------------


MOCK_TASKS = [
    "Research the topic thoroughly",
    "Create an outline",
    "Write the first draft",
    "Revise and edit the content",
    "Format according to requirements"
]


MOCK_RESPONSES = {
    "research": "Found multiple sources confirming that {topic} has significant implications.",
    "write": "Here's a concise summary of {topic}: It represents an important development.",
    "default": "Completed the requested task for {topic}."
}

# --------------- Client Initialization ---------------

# Initialize Azure OpenAI client (only in production mode)
azure_client = None
if not USE_MOCK:
    try:
        if not AZURE_KEY or not AZURE_ENDPOINT:
            logging.warning("Azure OpenAI credentials not found in environment. Falling back to mock mode.")
            USE_MOCK = True
        else:
            azure_client = AzureOpenAI(
                api_key=AZURE_KEY,
                azure_endpoint=AZURE_ENDPOINT,
                api_version=AZURE_API_VERSION
            )
            logging.info("Azure OpenAI client initialized successfully.")
    except Exception as e:
        logging.error(f"Failed to initialize Azure OpenAI client: {e}")
        logging.warning("Falling back to mock mode due to initialization error.")
        USE_MOCK = True

# Initialize Flask application
app = Flask(__name__)


# --------------- Helper Functions ---------------

def get_mock_task_response(task: str) -> str:
    """
    Generate a mock response for a specific task.
    
    Args:
        task: The task description to generate a response for
        
    Returns:
        A simulated AI-generated response appropriate for the task type
    """
    words = task.lower().split()
    topic = words[-1] if words else "task"
    
    # Choose appropriate response template based on task keywords
    task_lower = task.lower()
    if "research" in task_lower:
        template = MOCK_RESPONSES["research"]
    elif "write" in task_lower or "draft" in task_lower:
        template = MOCK_RESPONSES["write"]
    else:
        template = MOCK_RESPONSES["default"]
    
    return template.format(topic=topic)


def call_azure_openai(model: str, prompt: str) -> str:
    """
    Call Azure OpenAI API with the given model and prompt.
    
    Args:
        model: The model deployment name to use
        prompt: The prompt to send to the model
        
    Returns:
        The generated response text
        
    Raises:
        Exception: If the API call fails
    """
    try:
        # Create a chat completion with the given model and prompt
        response = azure_client.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": prompt}],
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"Azure OpenAI API call failed: {e}")
        return f"Error: {str(e)}"


# --------------- API Endpoints ---------------

@app.route("/health", methods=["GET"])
def health_check() -> Response:
    """
    Health check endpoint to verify service status.
    
    Returns:
        JSON response with service status and current operating mode
    """
    return jsonify({
        "status": "healthy",
        "mode": "mock" if USE_MOCK else "azure",
        "version": "1.0.0"
    })


@app.route("/run-agent", methods=["POST"])
def run_agent() -> Response:
    """
    Main endpoint to run the planning and execution agent.
    
    Expects a JSON payload with a 'request' field containing the user's request.
    
    Returns:
        JSON response with a plan (list of subtasks) and results (outputs for each subtask)
    """
    try:
        # Get user request from JSON payload
        payload = request.get_json()
        if not payload or 'request' not in payload:
            logging.warning("Missing 'request' field in payload")
            return jsonify({
                "error": "Missing required field: 'request'",
                "message": "Please provide a 'request' field in your JSON payload"
            }), 400

        user_request = payload["request"]
        logging.info(f"Processing request: '{user_request[:50]}{'...' if len(user_request) > 50 else ''}'")
        
        if USE_MOCK:
            logging.debug("Using mock mode - generating simulated responses")
            subtasks = MOCK_TASKS
            
            results = []
            for task in subtasks:
                results.append({
                    "subtask": task,
                    "result": get_mock_task_response(task)
                })
        else:
            logging.debug("Using Azure mode - calling OpenAI API")
            
            # Step 1: Generate a plan
            planner_prompt = PLANNER_TEMPLATE.format(user_request=user_request)
            logging.debug(f"Calling planner model: {MODEL_PLANNER}")
            plan_text = call_azure_openai(MODEL_PLANNER, planner_prompt)
            
            # Step 2: Extract subtasks from the numbered list in the response
            subtasks = [
                line.partition(" ")[2].strip()
                for line in plan_text.splitlines()
                if line and line[0].isdigit()
            ]
            
            if not subtasks:
                logging.warning(f"Failed to extract subtasks from plan text: {plan_text}")
                return jsonify({
                    "error": "Failed to generate a plan with subtasks",
                    "message": "The AI model did not generate a properly formatted plan"
                }), 500
            
            # Step 3: Execute each subtask
            results = []
            for i, task in enumerate(subtasks, 1):
                logging.debug(f"Executing subtask {i}/{len(subtasks)}: '{task}'")
                executor_prompt = EXECUTOR_TEMPLATE.format(subtask=task)
                result = call_azure_openai(MODEL_EXECUTOR, executor_prompt)
                results.append({
                    "subtask": task,
                    "result": result
                })
        
        # Return the plan as JSON
        return jsonify({
            "plan": subtasks,
            "results": results
        })
        
    except Exception as e:
        logging.error(f"Error processing request: {str(e)}", exc_info=True)
        return jsonify({
            "error": "Internal server error",
            "message": str(e)
        }), 500


# --------------- Main Entry Point ---------------

if __name__ == "__main__":
    print("=" * 69)
    print(f"🤖 Agentic Skeleton App - Running in {'MOCK' if USE_MOCK else 'AZURE'} mode")
    print(f"🔍 Health Check: http://localhost:{PORT}/health")
    print("=" * 69)
    
    # Start the Flask server
    app.run(host="0.0.0.0", port=PORT, debug=(os.getenv("FLASK_ENV") == "development"))
