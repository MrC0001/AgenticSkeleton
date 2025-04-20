"""
Consolidated Integration Tests
============================

Unified integration tests for the AgenticSkeleton API.
These tests verify the full request-response cycle.
"""

import unittest
import multiprocessing
import time
import requests
import json
import os
import sys
import textwrap
from typing import Dict, Any, Optional, List, Union

# Import the app and configuration
from agentic_skeleton.api.endpoints import app
from agentic_skeleton.config import settings
from agentic_skeleton.utils.helpers import colored, format_terminal_header

# Configure test port (different from main app port to allow parallel testing)
TEST_PORT = int(os.getenv("TEST_PORT", "8001"))
BASE_URL = f"http://localhost:{TEST_PORT}"


# Start server process
def run_flask_server(port):
    """Run a Flask server in a separate process"""
    # Disable werkzeug logging
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    
    # Start server
    app.run(host='localhost', port=port, debug=False, use_reloader=False)


class IntegrationTestCase(unittest.TestCase):
    """Base class for integration tests"""
    
    server_process = None
    
    @classmethod
    def setUpClass(cls):
        """Start a test server before running the tests"""
        print(f"{colored('🚀 Starting test server on port', 'cyan')} {TEST_PORT}")
        
        # Create a server process
        cls.server_process = multiprocessing.Process(
            target=run_flask_server,
            args=(TEST_PORT,)
        )
        cls.server_process.daemon = True
        cls.server_process.start()
        
        # Wait for server to start
        print(f"{colored('⏳ Waiting for server to start...', 'yellow')}")
        server_ready = False
        for _ in range(50):  # Try for 5 seconds
            try:
                response = requests.get(f"{BASE_URL}/health")
                if response.status_code == 200:
                    server_ready = True
                    break
            except requests.exceptions.ConnectionError:
                pass
            time.sleep(0.1)
            
        if server_ready:
            print(f"{colored('✅ Server is running', 'green')}")
        else:
            print(f"{colored('❌ Server failed to start', 'red')}")
            if cls.server_process.is_alive():
                cls.server_process.terminate()
            raise RuntimeError("Test server failed to start")
            
        # Set up common test variables
        cls.base_url = BASE_URL
        cls.health_endpoint = f"{BASE_URL}/health"
        cls.agent_endpoint = f"{BASE_URL}/run-agent"
        
    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests have run"""
        print(f"\n{colored('🛑 Stopping test server', 'yellow')}")
        # Terminate the server process if it's still running
        if cls.server_process and cls.server_process.is_alive():
            cls.server_process.terminate()
            cls.server_process.join(timeout=1)
        
    def pretty_print_json(self, data, title=None, indent=2):
        """Print a JSON object with colored formatting"""
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


class TestAgenticSkeletonAPI(IntegrationTestCase):
    """Integration tests for the AgenticSkeleton API"""
    
    def setUp(self):
        """Set up before each test"""
        self.test_results = []
        
    def tearDown(self):
        """Clean up after each test"""
        pass
    
    def log_test_result(self, name, status, response_time, plan_size=None):
        """Log a test result for later reporting"""
        self.test_results.append({
            "name": name,
            "status": status,
            "response_time": response_time,
            "plan_size": plan_size
        })
    
    def print_test_summary(self):
        """Print a summary of test results"""
        if not self.test_results:
            return
            
        print(f"\n{colored('📈 Performance Metrics:', 'cyan', attrs=['bold'])}")
        print(f"{'─' * 80}")
        print(f"  {'Request Type':<20} | {'Status':<10} | {'Response Time':<15} | {'Plan Size':<10}")
        print(f"  {'-' * 20} | {'-' * 10} | {'-' * 15} | {'-' * 10}")
        
        total_time = 0
        total_plan_size = 0
        success_count = 0
        
        for result in self.test_results:
            status = colored("✅ PASS", 'green') if result["status"] else colored("❌ FAIL", 'red')
            plan_size_str = f"{result['plan_size']} steps" if result["plan_size"] else "N/A"
            print(f"  {result['name']:<20} | {status:<10} | {result['response_time']:.2f}ms{' ' * 8} | {plan_size_str}")
            
            total_time += result["response_time"]
            if result["plan_size"]:
                total_plan_size += result["plan_size"]
            if result["status"]:
                success_count += 1
        
        # Print averages
        avg_time = total_time / len(self.test_results)
        avg_plan_size = total_plan_size / sum(1 for r in self.test_results if r["plan_size"]) if sum(1 for r in self.test_results if r["plan_size"]) > 0 else 0
        success_rate = success_count / len(self.test_results) * 100
        
        print(f"  {'-' * 20} | {'-' * 10} | {'-' * 15} | {'-' * 10}")
        print(f"  {'AVERAGE':<20} | {f'{success_rate:.0f}%':<10} | {avg_time:.2f}ms{' ' * 8} | {avg_plan_size:.1f} steps")
        
    def test_health_check(self):
        """Test the health check endpoint"""
        print(f"\n{colored('Testing health endpoint', 'blue')}")
        
        start_time = time.time()
        response = requests.get(self.health_endpoint)
        response_time_ms = (time.time() - start_time) * 1000
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.pretty_print_json(data, "Health response:")
        
        # Verify the response contains expected fields
        self.assertEqual(data['status'], 'healthy')
        self.assertIn('mode', data)
        self.assertIn(data['mode'], ['mock', 'azure'])
        
        print(f"{colored('✅ Health check passed', 'green')} ({response_time_ms:.2f}ms)")
        self.log_test_result("Health Check", True, response_time_ms)
    
    def test_basic_request(self):
        """Test a basic request to the run-agent endpoint"""
        request = "Write a short blog post about artificial intelligence"
        print(f"\n{colored('Testing basic request', 'blue')}: {request}")
        
        start_time = time.time()
        response = requests.post(
            self.agent_endpoint,
            json={"request": request}
        )
        response_time_ms = (time.time() - start_time) * 1000
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Verify the response structure
        self.assertIn('plan', data)
        self.assertIn('results', data)
        
        # Print the first and last steps for verification
        plan = data['plan']
        print(f"\n{colored('Plan:', 'green')} {len(plan)} steps")
        print(f"  First step: {plan[0]}")
        print(f"  Last step: {plan[-1]}")
        
        first_result = data['results'][0]['result']
        print(f"\n{colored('First result:', 'green')}")
        print(textwrap.fill(first_result[:100] + "...", width=80, initial_indent="  ", subsequent_indent="  "))
        
        print(f"{colored('✅ Basic request test passed', 'green')} ({response_time_ms:.2f}ms)")
        self.log_test_result("Basic Request", True, response_time_ms, len(plan))
    
    def test_analytical_request(self):
        """Test an analytical request to the run-agent endpoint"""
        request = "Analyze market trends in renewable energy"
        print(f"\n{colored('Testing analytical request', 'blue')}: {request}")
        
        start_time = time.time()
        response = requests.post(
            self.agent_endpoint,
            json={"request": request}
        )
        response_time_ms = (time.time() - start_time) * 1000
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Verify analysis-related keywords in the plan
        plan = data['plan']
        plan_text = ' '.join(plan).lower()
        self.assertTrue(
            'analyze' in plan_text or 
            'trends' in plan_text or 
            'data' in plan_text or
            'patterns' in plan_text
        )
        
        print(f"{colored('✅ Analytical request test passed', 'green')} ({response_time_ms:.2f}ms)")
        self.log_test_result("Analytical Request", True, response_time_ms, len(plan))
    
    def test_technical_request(self):
        """Test a technical request to the run-agent endpoint"""
        request = "Develop a REST API for user authentication"
        print(f"\n{colored('Testing technical request', 'blue')}: {request}")
        
        start_time = time.time()
        response = requests.post(
            self.agent_endpoint,
            json={"request": request}
        )
        response_time_ms = (time.time() - start_time) * 1000
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Verify technical keywords in the plan
        plan = data['plan']
        plan_text = ' '.join(plan).lower()
        self.assertTrue(
            'api' in plan_text or 
            'develop' in plan_text or 
            'implement' in plan_text or
            'architecture' in plan_text
        )
        
        print(f"{colored('✅ Technical request test passed', 'green')} ({response_time_ms:.2f}ms)")
        self.log_test_result("Technical Request", True, response_time_ms, len(plan))
    
    def test_creative_request(self):
        """Test a creative request to the run-agent endpoint"""
        request = "Design a logo for a technology startup"
        print(f"\n{colored('Testing creative request', 'blue')}: {request}")
        
        start_time = time.time()
        response = requests.post(
            self.agent_endpoint,
            json={"request": request}
        )
        response_time_ms = (time.time() - start_time) * 1000
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Verify creative keywords in the plan
        plan = data['plan']
        plan_text = ' '.join(plan).lower()
        self.assertTrue(
            'design' in plan_text or 
            'create' in plan_text or 
            'concept' in plan_text or
            'visual' in plan_text
        )
        
        print(f"{colored('✅ Creative request test passed', 'green')} ({response_time_ms:.2f}ms)")
        self.log_test_result("Creative Request", True, response_time_ms, len(plan))
    
    def test_data_science_request(self):
        """Test a data science request to the run-agent endpoint"""
        request = "Train a machine learning model to predict stock prices"
        print(f"\n{colored('Testing data science request', 'blue')}: {request}")
        
        start_time = time.time()
        response = requests.post(
            self.agent_endpoint,
            json={"request": request}
        )
        response_time_ms = (time.time() - start_time) * 1000
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Verify data science keywords in the plan
        plan = data['plan']
        plan_text = ' '.join(plan).lower()
        self.assertTrue(
            'data' in plan_text or 
            'model' in plan_text or 
            'train' in plan_text or
            'predict' in plan_text
        )
        
        print(f"{colored('✅ Data science request test passed', 'green')} ({response_time_ms:.2f}ms)")
        self.log_test_result("Data Science Request", True, response_time_ms, len(plan))
    
    def test_error_handling(self):
        """Test error handling for invalid requests"""
        print(f"\n{colored('Testing error handling', 'blue')}")
        
        # Test malformed JSON
        start_time = time.time()
        response = requests.post(
            self.agent_endpoint,
            data="This is not JSON",
            headers={"Content-Type": "application/json"}
        )
        response_time_ms = (time.time() - start_time) * 1000
        
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertIn('error', data)
        
        # Test missing request field
        start_time = time.time()
        response = requests.post(
            self.agent_endpoint,
            json={"not_request": "This is missing the request field"}
        )
        response_time_ms = (time.time() - start_time) * 1000
        
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertIn('error', data)
        self.assertIn('Missing', data['error'])
        
        print(f"{colored('✅ Error handling test passed', 'green')} ({response_time_ms:.2f}ms)")
        self.log_test_result("Error Handling", True, response_time_ms)
    
    def runTest(self):
        """Run all tests in sequence and print a summary"""
        print(f"\n{colored('▶️ Running integration tests:', 'cyan', attrs=['bold'])}")
        
        # Run tests
        self.test_health_check()
        self.test_basic_request()
        self.test_analytical_request()
        self.test_technical_request()
        self.test_creative_request()
        self.test_data_science_request()
        self.test_error_handling()
        
        # Print performance summary
        self.print_test_summary()


def run_tests():
    """Run the integration tests"""
    # Configure colored output
    format_terminal_header("Integration Tests", settings.is_using_mock())
    
    # Run tests
    test_runner = unittest.TextTestRunner(verbosity=2)
    test_suite = unittest.TestSuite()
    test_suite.addTest(TestAgenticSkeletonAPI())
    test_runner.run(test_suite)


if __name__ == "__main__":
    run_tests()