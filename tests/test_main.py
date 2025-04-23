# tests/test_main.py
import pytest
from unittest.mock import MagicMock
import os

# Import the function to test
from agentic_skeleton.__main__ import main

@pytest.fixture
def mock_dependencies(monkeypatch):
    """Set up all mocked dependencies for testing main"""
    # Create all mock objects
    mocks = {
        'app': MagicMock(),
        'settings': MagicMock(),
        'ensure_termcolor': MagicMock(),
        'setup_logging': MagicMock(),
        'format_header': MagicMock(),
        'print': MagicMock(),
        'colored': MagicMock(side_effect=lambda x, *args, **kwargs: x)
    }
    
    # Set up the logger mock
    mocks['logger'] = MagicMock()
    mocks['setup_logging'].return_value = mocks['logger']
    
    # Apply all monkeypatches
    monkeypatch.setattr('agentic_skeleton.__main__.app', mocks['app'])
    monkeypatch.setattr('agentic_skeleton.__main__.settings', mocks['settings'])
    monkeypatch.setattr('agentic_skeleton.__main__.ensure_termcolor_installed', mocks['ensure_termcolor'])
    monkeypatch.setattr('agentic_skeleton.__main__.setup_logging', mocks['setup_logging'])
    monkeypatch.setattr('agentic_skeleton.__main__.format_terminal_header', mocks['format_header'])
    monkeypatch.setattr('builtins.print', mocks['print'])
    monkeypatch.setattr('termcolor.colored', mocks['colored'])
    
    return mocks

def test_main_mock_mode(mock_dependencies):
    """Test the main function when running in mock mode."""
    # --- Arrange ---
    # Configure mock settings module attributes
    mock_dependencies['settings'].is_using_mock.return_value = True
    mock_dependencies['settings'].PORT = 5001
    
    # Set FLASK_ENV for debug=True in app.run
    original_flask_env = os.environ.get("FLASK_ENV")
    os.environ["FLASK_ENV"] = "development"
    
    try:
        # --- Act ---
        main()
        
        # --- Assert ---
        # Check setup functions were called
        mock_dependencies['ensure_termcolor'].assert_called_once()
        mock_dependencies['setup_logging'].assert_called_once()
        # format_terminal_header uses the result of is_using_mock() method
        mock_dependencies['format_header'].assert_called_once_with("Prompt Enhancement API", True)
        
        # Check print calls for configuration details
        print_calls = mock_dependencies['print'].call_args_list
        printed_text = "\n".join([c.args[0] for c in print_calls if c.args])
        assert "Mode:" in printed_text
        assert "Mock" in printed_text
        assert "Port:" in printed_text
        assert "5001" in printed_text
        assert "Quick Demo:" in printed_text
        assert "./demo.sh" in printed_text
        assert "Starting Flask server..." in printed_text
        
        # Ensure Azure details are NOT printed in mock mode
        assert "LLM Model:" not in printed_text
        assert "Azure Endpoint:" not in printed_text
        
        # Check Flask app run was called correctly
        mock_dependencies['app'].run.assert_called_once_with(host="0.0.0.0", port=5001, debug=True)
    
    finally:
        # Restore FLASK_ENV
        if original_flask_env is None:
            if "FLASK_ENV" in os.environ:
                del os.environ["FLASK_ENV"]
        else:
            os.environ["FLASK_ENV"] = original_flask_env

def test_main_live_mode(mock_dependencies):
    """Test the main function when running in live (Azure) mode."""
    # --- Arrange ---
    # Configure mock settings module attributes
    mock_dependencies['settings'].is_using_mock.return_value = False
    mock_dependencies['settings'].PORT = 5002
    mock_dependencies['settings'].MODEL_PROMPT_ENHANCER = "gpt-live-model"
    mock_dependencies['settings'].AZURE_ENDPOINT = "https://my-live-endpoint.openai.azure.com/"
    
    # Unset FLASK_ENV for debug=False in app.run
    original_flask_env = os.environ.get("FLASK_ENV")
    if "FLASK_ENV" in os.environ:
        del os.environ["FLASK_ENV"]
    
    try:
        # --- Act ---
        main()
        
        # --- Assert ---
        # Check setup functions were called
        mock_dependencies['ensure_termcolor'].assert_called_once()
        mock_dependencies['setup_logging'].assert_called_once()
        # format_terminal_header uses the result of is_using_mock() method
        mock_dependencies['format_header'].assert_called_once_with("Prompt Enhancement API", False)
        
        # Check print calls for configuration details
        print_calls = mock_dependencies['print'].call_args_list
        printed_text = "\n".join([c.args[0] for c in print_calls if c.args])
        assert "Mode:" in printed_text
        assert "Azure OpenAI" in printed_text
        assert "Port:" in printed_text
        assert "5002" in printed_text
        
        # Ensure Azure details ARE printed in live mode
        assert "LLM Model:" in printed_text
        assert "gpt-live-model" in printed_text
        # The endpoint is truncated in the display, so we should check for the truncated version
        truncated_endpoint = "https://my-live-endp..."
        assert f"Azure Endpoint:" in printed_text
        assert truncated_endpoint in printed_text
        
        assert "Quick Demo:" in printed_text
        assert "./demo.sh" in printed_text
        assert "Starting Flask server..." in printed_text
        
        # Check Flask app run was called correctly (debug=False)
        mock_dependencies['app'].run.assert_called_once_with(host="0.0.0.0", port=5002, debug=False)
    
    finally:
        # Restore FLASK_ENV
        if original_flask_env is not None:
            os.environ["FLASK_ENV"] = original_flask_env
