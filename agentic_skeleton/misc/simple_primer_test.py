#!/usr/bin/env python3
"""
Simple Test Client for AgenticSkeleton API

This script demonstrates basic usage of the AgenticSkeleton API:
1. Checking the health endpoint
2. Making requests to the run-agent endpoint

Use this as a starting point for testing your AI agent implementation.
"""

import requests
import json
import os
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API configuration
BASE_URL = f"http://localhost:{os.getenv('PORT', '8000')}"
HEALTH_ENDPOINT = f"{BASE_URL}/health"
AGENT_ENDPOINT = f"{BASE_URL}/run-agent"

# Test queries
TEST_QUERIES = [
    "Write a short blog post about artificial intelligence",
    "Analyze the trends in renewable energy adoption",
    "Develop a simple REST API for a todo application"
]

def test_health():
    """Test the health check endpoint"""
    print("\nTesting Health Endpoint")
    print("-" * 40)
    
    try:
        response = requests.get(HEALTH_ENDPOINT)
        response.raise_for_status()
        
        data = response.json()
        print("Health Endpoint Response:")
        print(json.dumps(data, indent=2))
        
        print(f"\nServer is running in {data.get('mode', 'unknown')} mode")
        return True
        
    except requests.exceptions.ConnectionError:
        print("\nConnection Error: The server is not running.")
        print("Hint: Start the server with 'python -m agentic_skeleton.misc.simple_primer' first.")
        return False
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        return False

def test_agent_query(query="Write a short blog post about artificial intelligence"):
    """Test the run-agent endpoint with a specific query"""
    print(f"\nTesting Query: \"{query}\"")
    print("-" * 40)
    
    try:
        # Make the request
        print("Sending request...")
        start_time = time.time()
        response = requests.post(
            AGENT_ENDPOINT, 
            json={"request": query}
        )
        response.raise_for_status()
        elapsed = time.time() - start_time
        
        # Process the response
        data = response.json()
        
        # Display success message
        print(f"Response received! ({elapsed:.2f}s)")
        
        # Display plan
        print("\nGenerated Plan:")
        for i, task in enumerate(data.get("plan", []), 1):
            print(f"  {i}. {task}")
        
        # Display results
        results = data.get("results", [])
        if results:
            print("\nResults:")
            for result in results:
                print(f"  Task: {result.get('subtask')}")
                print(f"  Result: {result.get('result')}")
                print()
        
        return True
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def run_tests():
    """Run all tests"""
    print("=" * 50)
    print("AgenticSkeleton API Test")
    print("=" * 50)
    
    if not test_health():
        return
    
    for query in TEST_QUERIES:
        test_agent_query(query)
        print("-" * 50)
    
    print("\nAll tests completed.")

if __name__ == "__main__":
    run_tests()