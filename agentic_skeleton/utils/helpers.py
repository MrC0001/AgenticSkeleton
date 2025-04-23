"""
Utility Functions
================

Provides helper functions for the application including:
- Terminal output formatting and colored logging
- Dependency management (auto-installation)
- Application initialization utilities

These utilities support the core functionality of the application
by providing common helper functions used across multiple modules.
"""

import sys
import logging
import random
import re
import subprocess
from typing import Dict, List, Any, Optional, Tuple, Union

# Flag to track if termcolor was successfully imported
_termcolor_imported = False

# Try to import termcolor for colored terminal output
try:
    from termcolor import colored
    _termcolor_imported = True  # Set flag if import succeeds
except ImportError:
    # Define a dummy colored function if termcolor is not installed
    def colored(text, *args, **kwargs):
        return text
    # _termcolor_imported remains False


def ensure_termcolor_installed():
    """
    Check if termcolor is installed and install it if not.
    
    This function:
    1. Checks if termcolor is already imported successfully
    2. If not, attempts to install it using pip
    3. Re-imports and updates the global function if installation succeeds
    4. Gracefully continues with a basic implementation if installation fails
    
    This approach allows the application to work even without the
    termcolor package while providing enhanced output when available.

    Returns:
        None
    """
    try:
        # Check the flag instead of comparing code objects
        if not _termcolor_imported:
            print("Installing termcolor for better output formatting...")
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "termcolor"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True  # Added check=True to raise CalledProcessError on failure
            )
            # Re-import termcolor after installation and update the flag
            # Use __import__ to avoid potential shadowing if 'colored' was the dummy
            new_colored = __import__('termcolor').colored
            globals()['colored'] = new_colored
            globals()['_termcolor_imported'] = True  # Update flag after successful install & import
    except (subprocess.CalledProcessError, ImportError, Exception) as e:
        # If installation or re-import fails, continue with dummy function (or whatever 'colored' is)
        pass


def setup_logging():
    """
    Configure logging for the application with colored output.
    
    Sets up:
    1. Basic logging configuration with timestamp and level
    2. Enhanced logging with color-coded log levels for better readability
    3. Custom log record factory for output formatting
    
    Returns:
        logging: Configured logging module
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        stream=sys.stdout
    )

    # Enhance logging with colored output using a custom record factory
    original_factory = logging.getLogRecordFactory()

    def colored_record_factory(*args, **kwargs):
        record = original_factory(*args, **kwargs)

        # Add color based on log level for better visual distinction
        levelname = record.levelname
        if levelname == 'DEBUG':
            record.levelname = colored(levelname, 'cyan')
        elif levelname == 'INFO':
            record.levelname = colored(levelname, 'green')
        elif levelname == 'WARNING':
            record.levelname = colored(levelname, 'yellow')
        elif levelname == 'ERROR':
            record.levelname = colored(levelname, 'red')
        elif levelname == 'CRITICAL':
            record.levelname = colored(levelname, 'red', attrs=['bold'])

        return record

    logging.setLogRecordFactory(colored_record_factory)

    return logging


def format_terminal_header(app_name: str, use_mock: bool):
    """
    Format a nice header for terminal output.
    
    Creates an eye-catching, colored terminal header that:
    1. Clearly identifies the application by name
    2. Indicates whether the application is running in mock mode
    3. Provides visual separation from other terminal output
    
    Args:
        app_name: The name of the application to display
        use_mock: Boolean indicating if mock mode is active
        
    Returns:
        None (prints directly to terminal)
    """
    # Create a border line
    border = colored("=" * 69, "blue")
    
    # Format the app name with robot emoji and proper styling
    app_title = colored(f"🤖 {app_name}", "cyan", attrs=["bold"])
    
    # Format the mode indication based on mock status
    mode_text = colored("MOCK", "yellow", attrs=["bold"]) if use_mock else colored("AZURE", "green", attrs=["bold"])
    
    # Format the complete header line
    header_line = f"{app_title} - Running in {mode_text} mode"
    
    # Print the formatted header
    print(border)
    print(header_line)

# More utility functions could be added here as the application grows