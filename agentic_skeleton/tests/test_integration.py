"""
Integration Tests
================

Tests that verify multiple components working together.
These tests focus on end-to-end scenarios, not unit functionality.
"""

import unittest
import json
import os
import logging
import sys
import time
from unittest.mock import patch, MagicMock

# Import necessary modules from our package
from agentic_skeleton.api.endpoints import app
from agentic_skeleton.config import settings
from agentic_skeleton.utils.helpers import colored, format_terminal_header

# Configure logging for tests
logging.basicConfig(level=logging.ERROR)

class TestAgenticSkeletonIntegration(unittest.TestCase):
    """Integration tests for the AgenticSkeleton API"""
    
    def setUp(self):
        """Set up test client and other test variables"""
        self.app = app.test_client()
        self.app.testing = True
    
    def test_complete_workflow_writing(self):
        """Test the complete workflow for a writing task"""
        print(f"\n{colored('Testing complete workflow for writing task', 'blue')}")
        
        # 1. Define the request
        request_data = {
            "request": "Write a blog post about machine learning applications in healthcare"
        }
        
        # 2. Call the endpoint
        print(f"{colored('Calling run-agent endpoint...', 'yellow')}")
        response = self.app.post('/run-agent', json=request_data)
        self.assertEqual(response.status_code, 200)
        
        # 3. Verify response structure
        data = json.loads(response.data)
        self.assertIn('plan', data)
        self.assertIn('results', data)
        self.assertTrue(len(data['plan']) >= 3)
        
        # 4. Print and verify results
        print(f"\n{colored('Generated plan:', 'green')}")
        for i, task in enumerate(data['plan'], 1):
            print(f"  {i}. {task}")
        
        print(f"\n{colored('Results:', 'green')}")
        for i, result in enumerate(data['results'], 1):
            print(f"  Task {i}: {result['subtask']}")
            if 'result' in result:
                print(f"    Result sample: {result['result'][:100]}...")
            else:
                print(f"    No result found")
        
        # 5. Verify results content contains healthcare and ML terms
        all_results = ' '.join([r.get('result', '') for r in data['results'] if 'result' in r]).lower()
        healthcare_terms = ['healthcare', 'medical', 'patient', 'diagnosis', 'treatment', 'hospital']
        ml_terms = ['machine learning', 'algorithm', 'model', 'prediction', 'classification', 'training']
        
        found_healthcare = any(term in all_results for term in healthcare_terms)
        found_ml = any(term in all_results for term in ml_terms)
        
        self.assertTrue(found_healthcare, "No healthcare terms found in response")
        self.assertTrue(found_ml, "No machine learning terms found in response")
    
    def test_complete_workflow_analysis(self):
        """Test the complete workflow for an analysis task"""
        print(f"\n{colored('Testing complete workflow for analysis task', 'blue')}")
        
        # 1. Define the request
        request_data = {
            "request": "Analyze the current market trends"
        }
        
        # 2. Call the endpoint
        print(f"{colored('Calling run-agent endpoint...', 'yellow')}")
        response = self.app.post('/run-agent', json=request_data)
        self.assertEqual(response.status_code, 200)
        
        # 3. Verify response structure
        data = json.loads(response.data)
        self.assertIn('plan', data)
        self.assertIn('results', data)
        
        # 4. Verify plan and results contents
        self.assertTrue(len(data['plan']) >= 3)
        self.assertTrue(len(data['results']) >= 3)
        
        # 5. Verify analysis contains relevant generic analysis terms
        all_results = ' '.join([r.get('result', '') for r in data['results'] if 'result' in r]).lower()
        analysis_terms = ['analysis', 'trends', 'data', 'research', 'findings', 'report', 'evaluate', 'assessment']
        
        found_analysis = any(term in all_results for term in analysis_terms)
        
        self.assertTrue(found_analysis, "No analysis terms found in response")
    
    def test_complete_workflow_development(self):
        """Test the complete workflow for a development task"""
        print(f"\n{colored('Testing complete workflow for development task', 'blue')}")
        
        # 1. Define the request
        request_data = {
            "request": "Develop a simple REST API for a bookstore application"
        }
        
        # 2. Call the endpoint
        print(f"{colored('Calling run-agent endpoint...', 'yellow')}")
        response = self.app.post('/run-agent', json=request_data)
        self.assertEqual(response.status_code, 200)
        
        # 3. Verify response structure
        data = json.loads(response.data)
        self.assertIn('plan', data)
        self.assertIn('results', data)
        
        # 4. Verify plan and results contents
        self.assertTrue(len(data['plan']) >= 3)
        self.assertTrue(len(data['results']) >= 3)
        
        # 5. Verify development content contains general API development terms only
        all_results = ' '.join([r.get('result', '') for r in data['results'] if 'result' in r]).lower()
        api_terms = ['api', 'endpoint', 'http', 'rest', 'request', 'response', 'server', 'route', 'json', 'service']
        
        found_api = any(term in all_results for term in api_terms)
        
        self.assertTrue(found_api, "No API development terms found in response")
    
    def test_system_resilience(self):
        """Test system resilience with multiple sequential requests"""
        print(f"\n{colored('Testing system resilience with multiple sequential requests', 'blue')}")
        
        # Define a list of test requests
        test_requests = [
            "Write a short story about time travel",
            "Analyze trends in cryptocurrency markets",
            "Develop a Python script for data cleaning",
            "Design a logo for a tech startup",
            "Create a machine learning model for sentiment analysis"
        ]
        
        # Process each request in sequence
        for i, request_text in enumerate(test_requests, 1):
            print(f"\n{colored(f'Request {i}/{len(test_requests)}: {request_text}', 'yellow')}")
            
            response = self.app.post('/run-agent', json={"request": request_text})
            
            # Verify basic response structure
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertIn('plan', data)
            self.assertIn('results', data)
            
            # Print brief summary
            print(f"  Plan: {len(data['plan'])} steps")
            print(f"  Results: {len(data['results'])} result items")
            
            # Add a small delay to prevent overwhelming the system
            time.sleep(0.5)
    
    def test_error_recovery(self):
        """Test the system's ability to recover from errors"""
        print(f"\n{colored('Testing error recovery capabilities', 'blue')}")
        
        # First, send a malformed request to trigger an error
        print(f"{colored('Sending malformed request...', 'yellow')}")
        bad_response = self.app.post(
            '/run-agent',
            data="This is not valid JSON",
            content_type='application/json'
        )
        self.assertEqual(bad_response.status_code, 400)
        
        # Now send a valid request to verify the system recovers
        print(f"{colored('Sending valid request after error...', 'yellow')}")
        good_response = self.app.post(
            '/run-agent',
            json={"request": "Summarize the main features of Python 3.10"}
        )
        
        # Verify the system processed the valid request correctly
        self.assertEqual(good_response.status_code, 200)
        data = json.loads(good_response.data)
        self.assertIn('plan', data)
        self.assertIn('results', data)
        
        print(f"{colored('✅ System successfully recovered from error', 'green')}")
    
    def test_mode_switching(self):
        """Test that the system can switch between mock and Azure modes"""
        # If we're running in mock mode, test mock functionality
        with patch('agentic_skeleton.config.settings.is_using_mock', return_value=True):
            print(f"\n{colored('Testing MOCK mode operation', 'blue')}")
            response = self.app.get('/health')
            data = json.loads(response.data)
            self.assertEqual(data['mode'], 'mock')
            
            # Verify a request works in mock mode
            task_response = self.app.post(
                '/run-agent',
                json={"request": "Write a short poem about AI"}
            )
            self.assertEqual(task_response.status_code, 200)
        
        # Test switching to Azure mode
        with patch('agentic_skeleton.config.settings.is_using_mock', return_value=False):
            # Also patch the Azure client to avoid real API calls
            with patch('agentic_skeleton.core.azure.client.initialize_client'):
                print(f"\n{colored('Testing AZURE mode operation', 'blue')}")
                response = self.app.get('/health')
                data = json.loads(response.data)
                self.assertEqual(data['mode'], 'azure')


if __name__ == "__main__":
    # Print header with ASCII art
    header = format_terminal_header("🧪 Integration Tests", settings.is_using_mock())
    print(header)
    
    # Print mode information
    print(f"Running in {colored('MOCK' if settings.is_using_mock() else 'AZURE', 'yellow')} mode")
    
    # Run the tests
    result = unittest.main(exit=False)
    
    # Print summary
    total = result.result.testsRun
    failures = len(result.result.failures)
    errors = len(result.result.errors)
    skipped = len(result.result.skipped)
    passed = total - failures - errors - skipped
    success_rate = (passed / total) * 100 if total > 0 else 0
    
    print("\n📊 Test Run Summary:")
    print("──────────────────────────────────────────────────")
    print(f"  Total tests: {total}")
    print(f"  Passed: {passed}")
    print(f"  Failed: {failures}")
    print(f"  Errors: {errors}")
    print(f"  Skipped: {skipped}")
    print(f"  Success rate: {success_rate:.1f}%")