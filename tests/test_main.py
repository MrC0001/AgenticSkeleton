# tests/test_main.py
import pytest
from unittest.mock import patch, MagicMock, call
import os

# Import the function to test
from agentic_skeleton.__main__ import main

# Mock the app object before it's imported by __main__
@patch('agentic_skeleton.__main__.app', new_callable=MagicMock)
# Mock settings module where it's imported into __main__
@patch('agentic_skeleton.__main__.settings', new_callable=MagicMock)
# Mock the USE_MOCK variable directly where it's used in __main__
@patch('agentic_skeleton.__main__.settings.USE_MOCK', False) # Patch the module variable
# Mock helper functions
@patch('agentic_skeleton.__main__.ensure_termcolor_installed')
@patch('agentic_skeleton.__main__.setup_logging')
@patch('agentic_skeleton.__main__.format_terminal_header')
# Mock print to capture output
@patch('builtins.print')
# Mock termcolor dynamically imported
@patch('termcolor.colored', MagicMock(side_effect=lambda x, *args, **kwargs: x))
def test_main_mock_mode(
    mock_app, mock_settings_module, mock_use_mock, mock_ensure_termcolor, 
    mock_setup_logging, mock_format_header, mock_print, mock_colored # Correct order (bottom-up)
):
    """Test the main function when running in mock mode."""
    # --- Arrange ---
    # Configure mock settings module attributes
    mock_use_mock.return_value = True # Override for mock mode test
    mock_settings_module.PORT = 5001
    # Mock logger returned by setup_logging
    mock_logger = MagicMock()
    mock_setup_logging.return_value = mock_logger
    # Set FLASK_ENV for debug=True in app.run
    original_flask_env = os.environ.get("FLASK_ENV")
    os.environ["FLASK_ENV"] = "development"

    # --- Act ---
    main()

    # --- Assert ---
    # Check setup functions were called
    mock_ensure_termcolor.assert_called_once()
    mock_setup_logging.assert_called_once()
    # format_terminal_header uses the result of USE_MOCK directly
    mock_format_header.assert_called_once_with("Prompt Enhancement API", True) # True for mock mode

    # Check print calls for configuration details (simplified check)
    print_calls = mock_print.call_args_list
    printed_text = "\n".join([c.args[0] for c in print_calls if c.args]) # Get text from print calls
    assert "Mode:" in printed_text
    assert "Mock" in printed_text # Check Mode uses the module variable result
    assert "Port:" in printed_text
    assert "5001" in printed_text
    assert "Quick Demo:" in printed_text
    assert "./demo.sh" in printed_text
    assert "Starting Flask server..." in printed_text
    # Ensure Azure details are NOT printed in mock mode
    assert "LLM Model:" not in printed_text
    assert "Azure Endpoint:" not in printed_text

    # Check Flask app run was called correctly
    mock_app.run.assert_called_once_with(host="0.0.0.0", port=5001, debug=True)

    # Restore FLASK_ENV
    if original_flask_env is None:
        if "FLASK_ENV" in os.environ:
             del os.environ["FLASK_ENV"]
    else:
        os.environ["FLASK_ENV"] = original_flask_env

@patch('agentic_skeleton.__main__.app', new_callable=MagicMock)
# Mock settings module where it's imported into __main__
@patch('agentic_skeleton.__main__.settings', new_callable=MagicMock)
# Mock the USE_MOCK variable directly where it's used in __main__
@patch('agentic_skeleton.__main__.settings.USE_MOCK', False) # Patch the module variable (default is False for live)
@patch('agentic_skeleton.__main__.ensure_termcolor_installed')
@patch('agentic_skeleton.__main__.setup_logging')
@patch('agentic_skeleton.__main__.format_terminal_header')
@patch('builtins.print')
# Mock termcolor dynamically imported
@patch('termcolor.colored', MagicMock(side_effect=lambda x, *args, **kwargs: x))
def test_main_live_mode(
    mock_app, mock_settings_module, mock_use_mock, mock_ensure_termcolor, 
    mock_setup_logging, mock_format_header, mock_print, mock_colored # Correct order (bottom-up)
):
    """Test the main function when running in live (Azure) mode."""
    # --- Arrange ---
    # Configure mock settings module attributes (USE_MOCK handled by patch)
    mock_settings_module.PORT = 5002
    mock_settings_module.MODEL_PROMPT_ENHANCER = "gpt-live-model"
    mock_settings_module.AZURE_ENDPOINT = "https://my-live-endpoint.openai.azure.com/"
    # Mock logger
    mock_logger = MagicMock()
    mock_setup_logging.return_value = mock_logger
    # Unset FLASK_ENV for debug=False in app.run
    original_flask_env = os.environ.get("FLASK_ENV")
    if "FLASK_ENV" in os.environ:
        del os.environ["FLASK_ENV"]

    # --- Act ---
    main()

    # --- Assert ---
    # Check setup functions
    mock_ensure_termcolor.assert_called_once()
    mock_setup_logging.assert_called_once()
    # format_terminal_header uses the result of USE_MOCK directly
    mock_format_header.assert_called_once_with("Prompt Enhancement API", False) # False for live mode

    # Check print calls for configuration details
    print_calls = mock_print.call_args_list
    printed_text = "\n".join([c.args[0] for c in print_calls if c.args])
    assert "Mode:" in printed_text
    assert "Azure OpenAI" in printed_text # Check Mode uses the module variable result
    assert "Port:" in printed_text
    assert "5002" in printed_text
    # Ensure Azure details ARE printed in live mode
    assert "LLM Model:" in printed_text
    assert "gpt-live-model" in printed_text
    # Assert the exact formatted line for the endpoint
    expected_endpoint_line = f"  {'Azure Endpoint:':<25} https://my-live-endpoint.openai.azure.com/"
    assert expected_endpoint_line in printed_text # Check exact formatted line

    assert "Quick Demo:" in printed_text
    assert "./demo.sh" in printed_text
    assert "Starting Flask server..." in printed_text

    # Check Flask app run was called correctly (debug=False)
    mock_app.run.assert_called_once_with(host="0.0.0.0", port=5002, debug=False)

    # Restore FLASK_ENV
    if original_flask_env is not None:
        os.environ["FLASK_ENV"] = original_flask_env
