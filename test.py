#!/usr/bin/env python3
"""
Test client for AgenticSkeleton API

This script demonstrates how to use the AgenticSkeleton API by:
1. Checking the health endpoint
2. Making requests to the run-agent endpoint with different query types

It shows the variety of mock responses available in the skeleton app.
"""

import requests
import json
import time
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration
BASE_URL = f"http://localhost:{os.getenv('PORT', '8000')}"
HEALTH_ENDPOINT = f"{BASE_URL}/health"
AGENT_ENDPOINT = f"{BASE_URL}/run-agent"

# Test queries for the agent to demonstrate different response types
TEST_QUERIES = [
    {
        "name": "Writing Task",
        "query": "Write a short blog post about artificial intelligence"
    },
    {
        "name": "Analysis Task",
        "query": "Analyze the trends in renewable energy adoption"
    },
    {
        "name": "Development Task",
        "query": "Develop a simple REST API for a todo application"
    }
]

def test_health():
    """Test the health check endpoint"""
    print("\n1️⃣ Testing health check endpoint...\n")
    
    try:
        response = requests.get(HEALTH_ENDPOINT)
        response.raise_for_status()
        
        data = response.json()
        print(f"✅ Status: {data.get('status')}")
        print(f"✅ Mode: {data.get('mode')}")
        print("\nHealth check successful! The server is running.")
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: The server is not running.")
        print("   Start the server with 'python app.py' first.")
        return False
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_agent_query(query, query_name=None, query_num=None, total_queries=None):
    """Test the run-agent endpoint with a specific query"""
    # Display query info with numbering if provided
    if query_num is not None and total_queries is not None:
        print(f"\n2️⃣ Testing run-agent endpoint ({query_num}/{total_queries}): {query_name}\n")
    else:
        print(f"\n2️⃣ Testing run-agent endpoint: {query_name}\n")
        
    print(f"📝 Query: \"{query}\"\n")
    
    try:
        # Make the request
        start_time = time.time()
        response = requests.post(
            AGENT_ENDPOINT, 
            json={"request": query}
        )
        response.raise_for_status()
        end_time = time.time()
        
        # Process the response
        data = response.json()
        
        # Display plan
        print("📋 Plan:")
        for i, task in enumerate(data.get("plan", []), 1):
            print(f"  {i}. {task}")
        
        # Display all results
        print("\n🔍 Results:")
        for i, result in enumerate(data.get("results", []), 1):
            print(f"  Task {i}: {result.get('subtask')}")
            print(f"  Result: {result.get('result')}")
            print("  " + "-" * 40)  # Separator line for readability
        
        # Show more info about response
        print(f"\n✅ Total tasks: {len(data.get('plan', []))}")
        print(f"✅ Response time: {end_time - start_time:.2f} seconds")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def test_all_queries():
    """Run tests for all predefined queries"""
    success = True
    
    for i, test_case in enumerate(TEST_QUERIES, 1):
        # Add a separator between tests
        if i > 1:
            print("\n" + "=" * 70 + "\n")
            
        # Run the test for this query
        result = test_agent_query(
            test_case["query"],
            test_case["name"],
            i,
            len(TEST_QUERIES)
        )
        
        # Track overall success
        success = success and result
        
    return success

if __name__ == "__main__":
    print("🧪 AgenticSkeleton API Test 🧪")
    
    # First check if the server is healthy
    if test_health():
        # Then test all agent queries
        test_all_queries()
    
    print("\n✨ Test complete ✨")

