"""
Simple API Test Script
====================

A simplified entry point for testing the AgenticSkeleton API.
This file provides basic API testing functionality and can also
run both unit and integration tests.
"""

import requests
import json
import time
import os
import sys
import textwrap
import argparse
from termcolor import colored

# Try to import from our package
try:
    from agentic_skeleton.config import settings
    from agentic_skeleton.utils.helpers import format_terminal_header
    BASE_URL = f"http://localhost:{settings.PORT}"
except ImportError:
    # Fallback if running from outside the package context
    BASE_URL = f"http://localhost:{os.getenv('PORT', '8000')}"
    
    def format_terminal_header(title, is_mock=True):
        mode = colored("MOCK", "yellow", attrs=["bold"]) if is_mock else colored("AZURE", "green", attrs=["bold"])
        header_text = f"{title}"
        print("\n" + "=" * 70)
        print(f"{colored(header_text, 'cyan', attrs=['bold'])} - Mode: {mode}")
        print("=" * 70)

# Endpoint URLs
HEALTH_ENDPOINT = f"{BASE_URL}/health"
AGENT_ENDPOINT = f"{BASE_URL}/run-agent"

def pretty_print_json(data, title=None, indent=2):
    """Pretty print a JSON response with colored keys"""
    if title:
        print(f"\n{colored(title, 'blue', attrs=['bold'])}")
    
    json_str = json.dumps(data, indent=indent)
    # Add color to keys
    colored_json = ""
    in_quotes = False
    in_key = False
    
    for i, char in enumerate(json_str):
        if char == '"':
            in_quotes = not in_quotes
            if in_quotes and i + 1 < len(json_str) and json_str[i+1] == ":":
                in_key = True
            elif not in_quotes and in_key:
                in_key = False
        
        if in_key:
            colored_json += colored(char, 'yellow')
        else:
            colored_json += char
            
    for line in colored_json.split('\n'):
        print(f"  {line}")

def test_health():
    """Test the health check endpoint"""
    print(f"\n{colored('🔍 Testing Health Endpoint', 'cyan', attrs=['bold'])}")
    print(f"{colored('-' * 50, 'blue')}")
    
    try:
        response = requests.get(HEALTH_ENDPOINT)
        response.raise_for_status()
        
        data = response.json()
        
        # Display the full health response
        pretty_print_json(data, "Health Endpoint Response:")
        
        mode = colored(data.get('mode', 'unknown'), 'cyan')
        print(f"\n{colored('✓', 'green')} Server is {colored('running', 'green')} in {mode} mode")
        
        # Use assertions for proper pytest behavior
        assert response.status_code == 200
        assert data.get('status') == 'healthy'
        
    except requests.exceptions.ConnectionError:
        print(f"\n{colored('✗ Connection Error:', 'red')} The server is not running.")
        print(f"  {colored('Hint:', 'yellow')} Start the server with 'python -m agentic_skeleton' first.")
        assert False, "Server is not running"
        
    except Exception as e:
        print(f"\n{colored('✗ Error:', 'red')} {str(e)}")
        assert False, f"Test failed with error: {str(e)}"

def test_agent_query(query="Tell me about Python programming language"):
    """Test the run-agent endpoint with a specific query"""
    print(f"\n{colored('📝 Testing Agent Query', 'cyan', attrs=['bold'])}")
    print(f"{colored('-' * 50, 'blue')}")
    print(f"{colored('Request:', 'blue')} \"{query}\"")
    
    try:
        # Make the request
        print(f"\n{colored('Sending request...', 'yellow')}")
        start_time = time.time()
        response = requests.post(
            AGENT_ENDPOINT, 
            json={"request": query}
        )
        response.raise_for_status()
        end_time = time.time()
        elapsed = end_time - start_time
        
        # Process the response
        data = response.json()
        
        # Display success message with timing
        print(f"{colored('✓', 'green')} {colored('Response received!', 'green')} ({elapsed:.2f}s)")
        
        # Display plan
        print(f"\n{colored('Generated Plan:', 'green', attrs=['bold'])}")
        for i, task in enumerate(data.get("plan", []), 1):
            print(f"  {i}. {task}")
        
        # Display results in a table format
        results = data.get("results", [])
        if results:
            print(f"\n{colored('📊 Response Summary:', 'green', attrs=['bold'])}")
            print(f"┌{'─' * 50}┬{'─' * 50}┐")
            print(f"│ {'Subtask':<48} │ {'Result':<48} │")
            print(f"├{'─' * 50}┼{'─' * 50}┤")
            
            for result in results:
                # Truncate and format subtask and result for table display
                subtask = result.get('subtask', '')
                result_text = result.get('result', '')
                
                # Show first 30 chars of subtask with ellipsis if needed
                if len(subtask) > 48:
                    subtask = subtask[:45] + "..."
                
                # Show first 30 chars of result with ellipsis if needed
                if len(result_text) > 48:
                    result_text = result_text[:45] + "..."
                
                print(f"│ {subtask:<48} │ {result_text:<48} │")
            
            print(f"└{'─' * 50}┴{'─' * 50}┘")
        
        # Print summary
        print(f"\n{colored('Summary:', 'blue', attrs=['bold'])}")
        print(f"  {colored('Total tasks:', 'blue')} {len(data.get('plan', []))}")
        print(f"  {colored('Response time:', 'blue')} {elapsed:.2f} seconds")
        
        # Use assertions for proper pytest behavior
        assert response.status_code == 200
        assert "plan" in data
        assert isinstance(data["plan"], list)
        assert len(data["plan"]) > 0
        
    except Exception as e:
        print(f"{colored('✗ Error:', 'red')} {str(e)}")
        assert False, f"Test failed with error: {str(e)}"

def run_unit_tests():
    """Run the unit tests"""
    try:
        import pytest
        import sys
        print(f"\n{colored('Running Unit Tests', 'blue', attrs=['bold'])}")
        sys.argv = [sys.argv[0], 'agentic_skeleton/tests/test_unit.py', '-v']
        pytest.main()
    except ImportError as e:
        print(f"{colored('✗ Error:', 'red')} Could not import pytest: {e}")
        print(f"  {colored('Hint:', 'yellow')} Make sure pytest is installed in your environment.")

def run_integration_tests():
    """Run the integration tests"""
    try:
        import pytest
        import sys
        print(f"\n{colored('Running Integration Tests', 'blue', attrs=['bold'])}")
        sys.argv = [sys.argv[0], 'agentic_skeleton/tests/test_integration.py', '-v']
        pytest.main()
    except ImportError as e:
        print(f"{colored('✗ Error:', 'red')} Could not import pytest: {e}")
        print(f"  {colored('Hint:', 'yellow')} Make sure pytest is installed in your environment.")

def main():
    """Run the API test client with command line options"""
    parser = argparse.ArgumentParser(description='AgenticSkeleton API Test Client')
    parser.add_argument('--query', '-q', help='Test the API with a specific query')
    parser.add_argument('--unit', '-u', action='store_true', help='Run unit tests')
    parser.add_argument('--integration', '-i', action='store_true', help='Run integration tests')
    parser.add_argument('--all', '-a', action='store_true', help='Run all tests')
    
    args = parser.parse_args()
    
    # Print header
    format_terminal_header("Testing Agentic Skeleton API", 
                           hasattr(settings, 'is_using_mock') and settings.is_using_mock())
    
    if args.unit or args.all:
        run_unit_tests()
        
    if args.integration or args.all:
        run_integration_tests()
        
    if args.query:
        if test_health():
            test_agent_query(args.query)
    elif not (args.unit or args.integration or args.all):
        # If no options specified, run the standard test with default query
        if test_health():
            test_agent_query("Write a short blog post about AI agents")
    
    print(f"\n{colored('Test completed.', 'cyan')}")

if __name__ == "__main__":
    main()