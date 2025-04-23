"""
Main Application Entry Point
============================

Starts the Prompt Enhancement API server and serves the Flask application.
This module initializes all necessary components and provides a user-friendly
console output with configuration details and available endpoints.
"""

import os
from agentic_skeleton.utils.helpers import ensure_termcolor_installed, setup_logging, format_terminal_header
from agentic_skeleton.config import settings
from agentic_skeleton.api.endpoints import app

def main():
    """
    Main entry point for the application.
    
    This function:
    1. Ensures required dependencies are installed
    2. Sets up logging with proper configuration
    3. Displays a formatted header and endpoint information
    4. Shows the current configuration (port, mode, LLM model)
    5. Starts the Flask server with appropriate debug settings
    
    The server mode (mock or Azure) is determined by the settings module,
    and debugging is enabled when FLASK_ENV is set to "development".
    """
    # Ensure termcolor is installed for better terminal output
    ensure_termcolor_installed()
    
    # Set up logging with colored output and proper logging levels
    logger = setup_logging()
    
    # Display formatted application header with mode indication
    format_terminal_header("Prompt Enhancement API", settings.is_using_mock())
    
    # Import termcolor after ensuring it's installed
    from termcolor import colored
    
    # Show endpoint URLs for easy access
    port = settings.PORT
    health_url = colored(f"http://localhost:{port}/health", "cyan")
    enhance_url = colored(f"http://localhost:{port}/enhance_prompt", "cyan")
    print(f"🔍 Health Check: {health_url}")
    print(f"🔄 Enhance Prompt Endpoint: {enhance_url}")
    
    # Display application configuration details
    print(f"\n{colored('Configuration:', 'blue', attrs=['bold'])}")
    print(f"  {'Port:':<25} {port}")
    print(f"  {'Mode:':<25} {'Mock' if settings.is_using_mock() else 'Azure OpenAI'}")
    
    # Show Azure-specific configuration when not in mock mode
    if not settings.is_using_mock():
        print(f"  {'LLM Model:':<25} {settings.MODEL_PROMPT_ENHANCER}")
        # Truncate long endpoint URLs for better display
        endpoint_display = settings.AZURE_ENDPOINT[:20] + "..." if len(settings.AZURE_ENDPOINT) > 23 else settings.AZURE_ENDPOINT
        print(f"  {'Azure Endpoint:':<25} {endpoint_display}")
    
    # Show information about the demo script
    print(f"\n{colored('Quick Demo:', 'blue', attrs=['bold'])}")
    demo_cmd = colored("./demo.sh", "yellow")
    print(f"  Run {demo_cmd} from the project root to test the API")
    
    # Visual separator before server start message
    print(colored("=" * 69, "blue"))
    print(f"{colored('Starting Flask server...', 'green')}")
    
    # Start the Flask server with appropriate configuration
    # Debug mode is enabled only in development environment
    app.run(
        host="0.0.0.0",  # Listen on all network interfaces
        port=port,       # Use the configured port
        debug=(os.getenv("FLASK_ENV") == "development")  # Enable debug mode in development
    )

if __name__ == "__main__":
    main()