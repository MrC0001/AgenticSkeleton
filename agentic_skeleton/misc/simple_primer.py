"""
Simple Agentic Skeleton App
==========================

A minimal Flask API skeleton that provides an AI agent with dual operation modes:
1. Mock responses (default for development without API keys)
2. Azure OpenAI API integration

Environment Variables:
- MOCK_RESPONSES: Set to "false" to use Azure OpenAI API (default: "true")
- AZURE_OPENAI_KEY: Your Azure OpenAI API key
- AZURE_OPENAI_ENDPOINT: Your Azure OpenAI endpoint
- PORT: Server port (default: 8000)
"""

import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
USE_MOCK = os.getenv("MOCK_RESPONSES", "true").lower() == "true"
AZURE_KEY = os.getenv("AZURE_OPENAI_KEY")
AZURE_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
PORT = int(os.getenv("PORT", "8000"))

# Prompt templates
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

# Mock data
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

# Initialize Flask app
app = Flask(__name__)

# Initialize Azure OpenAI client if needed
azure_client = None
if not USE_MOCK:
    try:
        from openai import AzureOpenAI
        azure_client = AzureOpenAI(
            api_key=AZURE_KEY,
            azure_endpoint=AZURE_ENDPOINT,
            api_version="2023-05-15"
        )
    except Exception:
        print("Failed to initialize Azure OpenAI client. Falling back to mock mode.")
        USE_MOCK = True

# Helper Functions
def get_mock_response(task):
    """Generate a mock response for a task"""
    words = task.lower().split()
    topic = words[-1] if words else "task"
    
    if "research" in task.lower():
        template = MOCK_RESPONSES["research"]
    elif "write" in task.lower() or "draft" in task.lower():
        template = MOCK_RESPONSES["write"]
    else:
        template = MOCK_RESPONSES["default"]
    
    return template.format(topic=topic)

def call_azure_openai(model, prompt):
    """Call Azure OpenAI API"""
    try:
        response = azure_client.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": prompt}],
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"

# API Endpoints
@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "mode": "mock" if USE_MOCK else "azure",
        "version": "1.0.0"
    })

@app.route("/run-agent", methods=["POST"])
def run_agent():
    """Main agent endpoint"""
    try:
        # Get request data
        payload = request.get_json()
        if not payload or 'request' not in payload:
            return jsonify({
                "error": "Missing required field: 'request'"
            }), 400

        user_request = payload["request"]
        
        if USE_MOCK:
            # Use mock data in development mode
            subtasks = MOCK_TASKS
            results = []
            for task in subtasks:
                results.append({
                    "subtask": task,
                    "result": get_mock_response(task)
                })
        else:
            # Use Azure OpenAI in production mode
            # Step 1: Generate a plan
            planner_prompt = PLANNER_TEMPLATE.format(user_request=user_request)
            plan_text = call_azure_openai("gpt-4", planner_prompt)
            
            # Step 2: Extract subtasks from the response
            subtasks = [
                line.partition(" ")[2].strip()
                for line in plan_text.splitlines()
                if line and line[0].isdigit()
            ]
            
            if not subtasks:
                return jsonify({
                    "error": "Failed to generate a plan with subtasks"
                }), 500
            
            # Step 3: Execute each subtask
            results = []
            for task in subtasks:
                executor_prompt = EXECUTOR_TEMPLATE.format(subtask=task)
                result = call_azure_openai("gpt-4", executor_prompt)
                results.append({
                    "subtask": task,
                    "result": result
                })
        
        # Return the plan and results
        return jsonify({
            "plan": subtasks,
            "results": results
        })
        
    except Exception as e:
        return jsonify({
            "error": "Internal server error",
            "message": str(e)
        }), 500

# Main entry point
def main():
    """Run the Flask application"""
    print(f"Starting AgenticSkeleton in {'mock' if USE_MOCK else 'Azure'} mode")
    print(f"Health endpoint: http://localhost:{PORT}/health")
    print(f"Agent endpoint: http://localhost:{PORT}/run-agent")
    app.run(host="0.0.0.0", port=PORT)

if __name__ == "__main__":
    main()