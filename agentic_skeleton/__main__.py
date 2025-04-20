"""
Main Application Entry Point
============================

Starts the AgenticSkeleton API server and serves the Flask application.
"""

import os
import sys
from agentic_skeleton.utils.helpers import ensure_termcolor_installed, setup_logging, format_terminal_header
from agentic_skeleton.config import settings
from agentic_skeleton.api.endpoints import app

def main():
    """
    Main entry point for the application.
    """
    # Ensure termcolor is installed for better output
    ensure_termcolor_installed()
    
    # Set up logging with colored output
    logger = setup_logging()
    
    # Display application header
    format_terminal_header("AgenticSkeleton API", settings.is_using_mock())
    
    # Show endpoint URLs
    from termcolor import colored
    port = settings.PORT
    health_url = colored(f"http://localhost:{port}/health", "cyan")
    agent_url = colored(f"http://localhost:{port}/run-agent", "cyan")
    print(f"🔍 Health Check: {health_url}")
    print(f"🔄 Agent Endpoint: {agent_url}")
    
    # Show configuration details
    print(f"\n{colored('Configuration:', 'blue', attrs=['bold'])}")
    print(f"  {'Port:':<25} {port}")
    print(f"  {'Mode:':<25} {'Mock' if settings.is_using_mock() else 'Azure OpenAI'}")
    
    if not settings.is_using_mock():
        print(f"  {'Planner Model:':<25} {settings.MODEL_PLANNER}")
        print(f"  {'Executor Model:':<25} {settings.MODEL_EXECUTOR}")
        endpoint_display = settings.AZURE_ENDPOINT[:20] + "..." if len(settings.AZURE_ENDPOINT) > 23 else settings.AZURE_ENDPOINT
        print(f"  {'Azure Endpoint:':<25} {endpoint_display}")
    
    # Show test command
    print(f"\n{colored('Quick Test:', 'blue', attrs=['bold'])}")
    test_cmd = colored("python -m agentic_skeleton.tests.test_api", "yellow")
    print(f"  Run {test_cmd} in another terminal to test the API")
    
    print(colored("=" * 69, "blue"))
    print(f"{colored('Starting Flask server...', 'green')}")
    
    # Start the Flask server
    app.run(
        host="0.0.0.0", 
        port=port, 
        debug=(os.getenv("FLASK_ENV") == "development")
    )

if __name__ == "__main__":
    main()