# tests/test_helpers.py

import pytest
import logging # Import logging for creating mock records
import sys # Import sys for mocking sys.executable
import subprocess # Import subprocess for CalledProcessError
from unittest.mock import patch, call, MagicMock
from agentic_skeleton.utils import helpers

# --- Tests for format_terminal_header ---

# Use patch to mock 'colored' and 'print' within the helpers module
@patch('agentic_skeleton.utils.helpers.colored')
@patch('builtins.print')
def test_format_terminal_header_mock_mode(mock_print, mock_colored):
    """Test header formatting when use_mock is True."""
    # Configure the mock for 'colored' to just return a formatted string
    # for easier assertion
    def side_effect(text, color, *args, **kwargs):
        attrs = kwargs.get('attrs', [])
        attr_str = f"_{'_'.join(attrs)}" if attrs else ""
        return f"[{color}{attr_str}]{text}[/{color}{attr_str}]"
    mock_colored.side_effect = side_effect

    app_name = "TestApp"
    helpers.format_terminal_header(app_name, use_mock=True)

    # Define expected calls to print
    expected_border = "[blue]=====================================================================[/blue]"
    expected_title = "[cyan_bold]🤖 TestApp[/cyan_bold]"
    expected_mode = "[yellow_bold]MOCK[/yellow_bold]"
    expected_header_line = f"{expected_title} - Running in {expected_mode} mode"

    # Check that print was called with the expected arguments
    expected_calls = [
        call(expected_border),
        call(expected_header_line)
    ]
    mock_print.assert_has_calls(expected_calls)
    assert mock_print.call_count == 2 # Ensure only these two calls were made

@patch('agentic_skeleton.utils.helpers.colored')
@patch('builtins.print')
def test_format_terminal_header_azure_mode(mock_print, mock_colored):
    """Test header formatting when use_mock is False."""
    # Configure the mock for 'colored'
    def side_effect(text, color, *args, **kwargs):
        attrs = kwargs.get('attrs', [])
        attr_str = f"_{'_'.join(attrs)}" if attrs else ""
        return f"[{color}{attr_str}]{text}[/{color}{attr_str}]"
    mock_colored.side_effect = side_effect

    app_name = "AnotherApp"
    helpers.format_terminal_header(app_name, use_mock=False)

    # Define expected calls to print
    expected_border = "[blue]=====================================================================[/blue]"
    expected_title = "[cyan_bold]🤖 AnotherApp[/cyan_bold]"
    expected_mode = "[green_bold]AZURE[/green_bold]" # Changed for Azure mode
    expected_header_line = f"{expected_title} - Running in {expected_mode} mode"

    # Check that print was called with the expected arguments
    expected_calls = [
        call(expected_border),
        call(expected_header_line)
    ]
    mock_print.assert_has_calls(expected_calls)
    assert mock_print.call_count == 2

# --- Tests for setup_logging ---

@patch('agentic_skeleton.utils.helpers.logging')
@patch('agentic_skeleton.utils.helpers.colored')
def test_setup_logging_calls(mock_colored, mock_logging_module):
    """Test that setup_logging calls the expected logging functions."""
    # Mock the return value of getLogRecordFactory
    mock_original_factory = MagicMock()
    mock_logging_module.getLogRecordFactory.return_value = mock_original_factory

    # Call the function
    returned_logger = helpers.setup_logging()

    # Assert basicConfig was called
    mock_logging_module.basicConfig.assert_called_once()
    # Check specific args if needed, e.g., level=logging.INFO

    # Assert factory functions were called
    mock_logging_module.getLogRecordFactory.assert_called_once()
    mock_logging_module.setLogRecordFactory.assert_called_once()

    # Assert it returns the logging module itself
    assert returned_logger == mock_logging_module

@patch('agentic_skeleton.utils.helpers.colored')
@patch('agentic_skeleton.utils.helpers.logging')
def test_setup_logging_colored_factory_behavior(mock_logging_module, mock_colored):
    """Test the behavior of the colored_record_factory set by setup_logging."""
    # Mock the original factory and capture the new factory function
    mock_original_factory = MagicMock()
    mock_logging_module.getLogRecordFactory.return_value = mock_original_factory

    # Call setup_logging to set the new factory
    helpers.setup_logging()

    # Capture the factory function passed to setLogRecordFactory
    new_factory_func = mock_logging_module.setLogRecordFactory.call_args[0][0]

    # --- Test the captured factory function ---
    # Mock the record returned by the original factory
    mock_record = MagicMock(spec=logging.LogRecord)
    mock_original_factory.return_value = mock_record

    # Define test cases for different log levels
    test_cases = [
        ('DEBUG', 'cyan', []),
        ('INFO', 'green', []),
        ('WARNING', 'yellow', []),
        ('ERROR', 'red', []),
        ('CRITICAL', 'red', ['bold']),
        ('OTHER', None, []) # Test a level that shouldn't be colored
    ]

    for levelname, expected_color, expected_attrs in test_cases:
        mock_record.levelname = levelname
        mock_colored.reset_mock() # Reset mock for each case

        # Call the captured factory function
        result_record = new_factory_func('arg1', kwarg1='value1') # Pass dummy args

        # Assert the original factory was called
        mock_original_factory.assert_called_with('arg1', kwarg1='value1')

        # Assert colored was called (or not called) correctly
        if expected_color:
            if expected_attrs:
                mock_colored.assert_called_once_with(levelname, expected_color, attrs=expected_attrs)
            else:
                mock_colored.assert_called_once_with(levelname, expected_color)
            # Assert the record's levelname was updated with the colored version
            assert result_record.levelname == mock_colored.return_value
        else:
            mock_colored.assert_not_called()
            # Assert the record's levelname remains unchanged
            assert result_record.levelname == levelname

# --- Tests for ensure_termcolor_installed ---

@patch('agentic_skeleton.utils.helpers.subprocess.run')
@patch('builtins.print')
@patch('agentic_skeleton.utils.helpers._termcolor_imported', True) # Patch the flag to True
def test_ensure_termcolor_already_installed(mock_print, mock_subprocess_run):
    """Test ensure_termcolor_installed when flag indicates termcolor is present."""
    helpers.ensure_termcolor_installed()

    # Assert that print and subprocess.run were NOT called
    mock_print.assert_not_called()
    mock_subprocess_run.assert_not_called()

@patch('agentic_skeleton.utils.helpers.subprocess.run')
@patch('builtins.print')
@patch('builtins.__import__')
@patch('agentic_skeleton.utils.helpers.globals') # Keep globals mock to check update
@patch('agentic_skeleton.utils.helpers._termcolor_imported', False) # Patch the flag to False
def test_ensure_termcolor_needs_install_success(mock_globals, mock_import, mock_print, mock_subprocess_run):
    """Test ensure_termcolor_installed when flag indicates termcolor needs install (success)."""
    # Mock the successful import of termcolor
    mock_termcolor_module = MagicMock()
    mock_new_colored_func = MagicMock()
    mock_termcolor_module.colored = mock_new_colored_func
    mock_import.return_value = mock_termcolor_module

    # Mock subprocess.run to simulate success
    mock_subprocess_run.return_value = MagicMock() # returncode isn't strictly needed now with check=True

    # Prepare mock globals dict to check updates
    mock_globals_dict = {'colored': None, '_termcolor_imported': False} # Simulate initial state
    mock_globals.return_value = mock_globals_dict

    # Mock sys.executable
    with patch('agentic_skeleton.utils.helpers.sys.executable', '/path/to/python'):
        helpers.ensure_termcolor_installed()

    # Assert print was called
    mock_print.assert_called_once_with("Installing termcolor for better output formatting...")

    # Assert subprocess.run was called correctly
    expected_pip_command = [
        '/path/to/python', "-m", "pip", "install", "termcolor"
    ]
    mock_subprocess_run.assert_called_once_with(
        expected_pip_command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True # Check that check=True is passed
    )

    # Assert __import__ was called to get the new 'colored'
    mock_import.assert_called_once_with('termcolor')

    # Assert that the global 'colored' and the flag were updated
    assert mock_globals_dict['colored'] == mock_new_colored_func
    assert mock_globals_dict['_termcolor_imported'] is True

@patch('agentic_skeleton.utils.helpers.subprocess.run')
@patch('builtins.print')
@patch('builtins.__import__')
@patch('agentic_skeleton.utils.helpers.globals')
@patch('agentic_skeleton.utils.helpers._termcolor_imported', False) # Patch the flag to False
def test_ensure_termcolor_install_subprocess_fails(mock_globals, mock_import, mock_print, mock_subprocess_run):
    """Test ensure_termcolor_installed when pip install fails (raises CalledProcessError)."""
    # Prepare mock globals dict to check updates
    mock_globals_dict = {'colored': None, '_termcolor_imported': False}
    mock_globals.return_value = mock_globals_dict

    # Mock subprocess.run to simulate failure by raising CalledProcessError
    mock_subprocess_run.side_effect = subprocess.CalledProcessError(1, "pip install termcolor")

    # Mock sys.executable
    with patch('agentic_skeleton.utils.helpers.sys.executable', '/path/to/python'):
        # Call the function - it should catch the exception and continue
        helpers.ensure_termcolor_installed()

    # Assert print was called
    mock_print.assert_called_once_with("Installing termcolor for better output formatting...")

    # Assert subprocess.run was called
    mock_subprocess_run.assert_called_once() # Args checked in previous test

    # Assert __import__ was NOT called because installation failed
    mock_import.assert_not_called()

    # Assert that the global 'colored' and flag remain unchanged
    assert mock_globals_dict['colored'] is None
    assert mock_globals_dict['_termcolor_imported'] is False

@patch('agentic_skeleton.utils.helpers.subprocess.run')
@patch('builtins.print')
@patch('builtins.__import__')
@patch('agentic_skeleton.utils.helpers.globals')
@patch('agentic_skeleton.utils.helpers._termcolor_imported', False) # Patch the flag to False
def test_ensure_termcolor_install_import_fails(mock_globals, mock_import, mock_print, mock_subprocess_run):
    """Test ensure_termcolor_installed when pip install succeeds but import fails."""
    # Prepare mock globals dict to check updates
    mock_globals_dict = {'colored': None, '_termcolor_imported': False}
    mock_globals.return_value = mock_globals_dict

    # Mock subprocess.run to simulate success
    mock_subprocess_run.return_value = MagicMock() # No need to check returncode

    # Mock __import__ to raise an ImportError
    mock_import.side_effect = ImportError("Cannot import termcolor")

    # Mock sys.executable
    with patch('agentic_skeleton.utils.helpers.sys.executable', '/path/to/python'):
        # Call the function - it should catch the exception and continue
        helpers.ensure_termcolor_installed()

    # Assert print was called
    mock_print.assert_called_once_with("Installing termcolor for better output formatting...")

    # Assert subprocess.run was called
    mock_subprocess_run.assert_called_once()

    # Assert __import__ was called
    mock_import.assert_called_once_with('termcolor')

    # Assert that the global 'colored' and flag remain unchanged because import failed
    assert mock_globals_dict['colored'] is None
    assert mock_globals_dict['_termcolor_imported'] is False
