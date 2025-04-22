"""
Main Application Entry Point
============================

Starts the Prompt Enhancement API server and serves the Flask application.
"""

import os
from agentic_skeleton.utils.helpers import ensure_termcolor_installed, setup_logging, format_terminal_header
from agentic_skeleton.config import settings
from agentic_skeleton.api.endpoints import app

def main():
    """
    Main entry point for the application.
    
    Initializes logging, displays server information, and starts the Flask server.
    """
    # Ensure termcolor is installed for better terminal output
    ensure_termcolor_installed()
    
    # Set up logging with colored output
    logger = setup_logging()
    
    # Display application header
    format_terminal_header("Prompt Enhancement API", settings.is_using_mock())
    
    # Import termcolor after ensuring it's installed
    from termcolor import colored
    
    # Show endpoint URLs
    port = settings.PORT
    health_url = colored(f"http://localhost:{port}/health", "cyan")
    enhance_url = colored(f"http://localhost:{port}/enhance_prompt", "cyan")
    print(f"🔍 Health Check: {health_url}")
    print(f"🔄 Enhance Prompt Endpoint: {enhance_url}")
    
    # Show configuration details
    print(f"\n{colored('Configuration:', 'blue', attrs=['bold'])}")
    print(f"  {'Port:':<25} {port}")
    print(f"  {'Mode:':<25} {'Mock' if settings.is_using_mock() else 'Azure OpenAI'}")
    
    if not settings.is_using_mock():
        print(f"  {'LLM Model:':<25} {settings.MODEL_PROMPT_ENHANCER}")
        endpoint_display = settings.AZURE_ENDPOINT[:20] + "..." if len(settings.AZURE_ENDPOINT) > 23 else settings.AZURE_ENDPOINT
        print(f"  {'Azure Endpoint:':<25} {endpoint_display}")
    
    # Show demo script information
    print(f"\n{colored('Quick Demo:', 'blue', attrs=['bold'])}")
    demo_cmd = colored("./demo.sh", "yellow")
    print(f"  Run {demo_cmd} from the project root to test the API")
    
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