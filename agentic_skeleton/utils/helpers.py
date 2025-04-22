"""
Utility Functions
================

Provides helper functions for the application including:
- Terminal output formatting
- Text processing
- Mock response generation
- Azure OpenAI integration
"""

import sys
import logging
import random
import re
import subprocess
from typing import Dict, List, Any, Optional, Tuple, Union

_termcolor_imported = False  # Flag to track if termcolor was successfully imported

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

    Returns:
        None
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        stream=sys.stdout
    )

    # Enhance logging with colored output
    original_factory = logging.getLogRecordFactory()

    def colored_record_factory(*args, **kwargs):
        record = original_factory(*args, **kwargs)

        # Add color based on log level
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

    Args:
        app_name: The name of the application
        use_mock: Whether the app is using mock mode

    Returns:
        None (prints to terminal)
    """
    border = colored("=" * 69, "blue")
    print(border)

    # Show the app header with mode info
    title = colored(f"🤖 {app_name}", "cyan", attrs=["bold"])
    mode = colored("MOCK", "yellow", attrs=["bold"]) if use_mock else colored("AZURE", "green", attrs=["bold"])
    print(f"{title} - Running in {mode} mode")