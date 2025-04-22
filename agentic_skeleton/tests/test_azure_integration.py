"""
Azure Integration Tests
======================

Tests that verify Azure-specific components working together.
These tests focus on Azure-specific integration scenarios.
"""

import unittest
from unittest.mock import patch, MagicMock
import logging
import sys
import json
import time

# Updated imports to match the new modular structure
from agentic_skeleton.core.azure.classifier import classify_request, detect_domain_specialization, classify_subtask
from agentic_skeleton.core.azure.generator import generate_plan, execute_subtasks
from agentic_skeleton.core.azure.client import call_azure_openai
from agentic_skeleton.core.azure.enhancer import (
    enhance_prompt_with_domain_knowledge,
    enhance_subtask_prompt
)
from agentic_skeleton.core.azure.constants.fallback_plans import get_fallback_plan
from agentic_skeleton.utils.helpers import colored, format_terminal_header
from agentic_skeleton.config import settings
from agentic_skeleton.api.endpoints import app

class TestAzureIntegration(unittest.TestCase):
    """Integration tests for the Azure components of the AgenticSkeleton API"""
    
    def setUp(self):
        """Set up test client and other test variables"""
        # Disable logging during tests
        logging.disable(logging.CRITICAL)
        self.app = app.test_client()
        self.app.testing = True
    
    def tearDown(self):
        """Clean up after tests"""
        # Re-enable logging after tests
        logging.disable(logging.NOTSET)
    
    def test_request_classification(self):
        """Test the request classification functionality"""
        print(f"\n{colored('Testing request classification with various task types...', 'blue')}")
        
        test_cases = [
            {"request": "Train a machine learning model for customer churn", "expected": "data-science"},
            {"request": "Analyze market trends in renewable energy", "expected": "analyze"},
            {"request": "Develop a REST API for user authentication", "expected": "develop"},
            {"request": "Design a user interface for a mobile app", "expected": "design"},
            {"request": "Write a blog post about sustainable technology", "expected": "write"}
        ]
        
        print(f"\n{colored('Format: [Query] → [Detected Type] (Expected Type)', 'green')}")
        for case in test_cases:
            result = classify_request(case["request"])
            success = result == case["expected"]
            mark = colored("✓", "green") if success else colored("✗", "red")
            print(f"  {mark} [{case['request']}] → [{colored(result, 'cyan')}] ({colored(case['expected'], 'yellow')})")
            self.assertEqual(result, case["expected"])
        
        # Complex multi-domain request test
        print(f"\n{colored('Testing complex, multi-domain request classification...', 'blue')}")
        complex_request = "Create a comprehensive end-to-end platform for analyzing customer data, " \
                         "predicting churn and automatically generating personalized retention emails"
        
        result = classify_request(complex_request)
        success = result == "data-science"
        mark = colored("✓", "green") if success else colored("✗", "red")
        
        print(f"\n{colored('Complex request:', 'green')}")
        print(f"  \"{complex_request}\"")
        print(f"\n{colored('Classification result:', 'green')}")
        print(f"  {mark} [{colored(result, 'cyan')}]")
        
        self.assertEqual(result, "data-science")
        print(f"{colored('✅ Request classification verified for all task types', 'green')}")
    
    def test_domain_specialization_detection(self):
        """Test the domain specialization detection functionality"""
        print(f"\n{colored('Testing domain specialization detection...', 'blue')}")
        
        # Cloud computing domain
        cloud_request = "Design a multi-region cloud deployment architecture for our application"
        cloud_domain = detect_domain_specialization(cloud_request)
        
        print(f"\n{colored('Cloud computing request:', 'green')}")
        print(f"  \"{cloud_request}\"")
        print(f"{colored('Detected domain:', 'green')}")
        print(f"  Name: {colored(cloud_domain['name'], 'cyan')}")
        print(f"  Preferred category: {colored(cloud_domain['preferred_category'], 'cyan')}")
        
        self.assertEqual(cloud_domain['name'], "cloud_computing")
        self.assertIn("guidance", cloud_domain)
        self.assertEqual(cloud_domain['preferred_category'], "develop")
        
        print(f"{colored('✅ Cloud computing domain detection verified', 'green')}")
        
        # AI/ML domain
        ai_request = "Develop a generative AI model for creating marketing content"
        ai_domain = detect_domain_specialization(ai_request)
        
        print(f"\n{colored('AI/ML request:', 'green')}")
        print(f"  \"{ai_request}\"")
        print(f"{colored('Detected domain:', 'green')}")
        print(f"  Name: {colored(ai_domain['name'], 'cyan')}")
        print(f"  Preferred category: {colored(ai_domain['preferred_category'], 'cyan')}")
        
        self.assertEqual(ai_domain['name'], "ai_ml")
        self.assertIn("guidance", ai_domain)
        self.assertEqual(ai_domain['preferred_category'], "data-science")
        
        print(f"{colored('✅ AI/ML domain detection verified', 'green')}")
        
        # Healthcare domain
        health_request = "Build a telehealth platform for remote patient monitoring"
        health_domain = detect_domain_specialization(health_request)
        
        print(f"\n{colored('Healthcare request:', 'green')}")
        print(f"  \"{health_request}\"")
        print(f"{colored('Detected domain:', 'green')}")
        print(f"  Name: {colored(health_domain['name'], 'cyan')}")
        print(f"  Preferred category: {colored(health_domain['preferred_category'], 'cyan')}")
        
        self.assertEqual(health_domain['name'], "healthcare_tech")
        self.assertIn("guidance", health_domain)
        self.assertEqual(health_domain['preferred_category'], "analyze")
        
        print(f"{colored('✅ Healthcare tech domain detection verified', 'green')}")
        
        # Generic domain
        generic_request = "Write a blog post about company culture"
        generic_domain = detect_domain_specialization(generic_request)
        
        print(f"\n{colored('Generic request:', 'green')}")
        print(f"  \"{generic_request}\"")
        print(f"{colored('Detected domain:', 'green')}")
        print(f"  No specific domain detected")
        
        self.assertEqual(generic_domain, {})
        
        print(f"{colored('✅ Generic domain detection verified', 'green')}")
    
    def test_subtask_classification(self):
        """Test the subtask classification functionality"""
        print(f"\n{colored('Testing subtask classification...', 'blue')}")
        
        # Basic subtask classification
        basic_subtasks = [
            {"subtask": "Research recent advances in natural language processing", "expected": "research"},
            {"subtask": "Implement a user authentication system", "expected": "implement"},
            {"subtask": "Design a database schema for user profiles", "expected": "design"},
            {"subtask": "Test the API endpoints for performance", "expected": "evaluate"},
            {"subtask": "Document the system architecture", "expected": "document"}
        ]
        
        print(f"\n{colored('Basic subtask classification:', 'green')}")
        for case in basic_subtasks:
            result = classify_subtask(case["subtask"], {})
            success = result == case["expected"]
            mark = colored("✓", "green") if success else colored("✗", "red")
            print(f"  {mark} [{case['subtask']}] → [{colored(result, 'cyan')}]")
            self.assertEqual(result, case["expected"])
        
        # Domain-specific subtask classification
        print(f"\n{colored('AI/ML domain subtask classification:', 'green')}")
        ai_domain = detect_domain_specialization("Train a machine learning model for text classification")
        
        ai_subtasks = [
            {"subtask": "Gather and preprocess training data", "expected": "data"},
            {"subtask": "Train the classification model", "expected": "model"},
            {"subtask": "Deploy the model as a prediction API", "expected": "deploy"}
        ]
        
        for case in ai_subtasks:
            result = classify_subtask(case["subtask"], ai_domain)
            success = result == case["expected"]
            mark = colored("✓", "green") if success else colored("✗", "red")
            print(f"  {mark} [{case['subtask']}] → [{colored(result, 'cyan')}]")
            self.assertEqual(result, case["expected"])
        
        print(f"\n{colored('Cloud computing domain subtask classification:', 'green')}")
        cloud_domain = detect_domain_specialization("Optimize cloud costs for our multi-region deployment")
        
        cloud_subtasks = [
            {"subtask": "Research cost optimization strategies", "expected": "research"},
            {"subtask": "Implement auto-scaling policies", "expected": "implement"},
            {"subtask": "Optimize resource allocation", "expected": "optimize"}
        ]
        
        for case in cloud_subtasks:
            result = classify_subtask(case["subtask"], cloud_domain)
            success = result == case["expected"]
            mark = colored("✓", "green") if success else colored("✗", "red")
            print(f"  {mark} [{case['subtask']}] → [{colored(result, 'cyan')}]")
            self.assertEqual(result, case["expected"])
            
        print(f"{colored('✅ Subtask classification verified for all types', 'green')}")
    
    def test_prompt_enhancement(self):
        """Test the prompt enhancement functionality"""
        print(f"\n{colored('Testing prompt enhancement capabilities...', 'blue')}")
        
        # Test basic prompt enhancement
        test_prompt = "Generate a response for the following task:"
        user_request = "Build a machine learning model for customer churn prediction"
        request_category = "data-science"
        
        enhanced_prompt = enhance_prompt_with_domain_knowledge(
            test_prompt, 
            user_request, 
            request_category
        )
        
        print(f"\n{colored('Basic prompt enhancement:', 'green')}")
        print(f"  Original prompt: \"{test_prompt}\"")
        print(f"  User request: \"{user_request}\"")
        print(f"  Category: \"{request_category}\"")
        print(f"  Enhanced prompt length: {len(enhanced_prompt)} chars")
        
        # Check that the category guidance is included
        self.assertIn("data-science", enhanced_prompt.lower())
        self.assertIn("model development", enhanced_prompt.lower())
        
        # Test domain-specific prompt enhancement
        ai_request = "Train a neural network for image recognition"
        ai_domain = detect_domain_specialization(ai_request)
        domain_enhanced_prompt = enhance_prompt_with_domain_knowledge(
            test_prompt, 
            ai_request,
            "data-science",
            ai_domain
        )
        
        print(f"\n{colored('Domain-specific prompt enhancement:', 'green')}")
        print(f"  Original prompt: \"{test_prompt}\"")
        print(f"  User request: \"{ai_request}\"")
        print(f"  Domain: \"{ai_domain['name']}\"")
        print(f"  Enhanced prompt length: {len(domain_enhanced_prompt)} chars")
        
        # Check that domain guidance is included
        self.assertIn("domain specialization", domain_enhanced_prompt.lower())
        self.assertIn("ai_ml", domain_enhanced_prompt.lower())
        
        # Test subtask prompt enhancement
        subtask = "Preprocess and augment the image dataset"
        subtask_enhanced_prompt = enhance_subtask_prompt(
            test_prompt,
            ai_request,
            subtask,
            "data-science",
            ai_domain,
            "data"  # Adding the required subtask_type parameter
        )
        
        print(f"\n{colored('Subtask prompt enhancement:', 'green')}")
        print(f"  Original prompt: \"{test_prompt}\"")
        print(f"  User request: \"{ai_request}\"")
        print(f"  Subtask: \"{subtask}\"")
        print(f"  Subtask type: \"data\"")
        print(f"  Enhanced prompt length: {len(subtask_enhanced_prompt)} chars")
        
        # Check that subtask-specific guidance is included
        self.assertIn("subtask type", subtask_enhanced_prompt.lower())
        self.assertIn("data", subtask_enhanced_prompt.lower())
        
        print(f"{colored('✅ Prompt enhancement verified for all scenarios', 'green')}")
    
    def test_get_fallback_plan(self):
        """Test the fallback plan generation functionality"""
        print(f"\n{colored('Testing fallback plan generation...', 'blue')}")
        
        # Test domain-specific fallback plan
        ai_domain = detect_domain_specialization("Train a machine learning model for text classification")
        ai_fallback_plan = get_fallback_plan("data-science", ai_domain)
        
        print(f"\n{colored('AI/ML domain fallback plan:', 'green')}")
        for i, step in enumerate(ai_fallback_plan, 1):
            print(f"  {i}. {step}")
        
        # Verify the AI-specific fallback plan
        self.assertTrue(any("data" in step.lower() for step in ai_fallback_plan))
        self.assertTrue(any("model" in step.lower() for step in ai_fallback_plan))
        self.assertTrue(any("train" in step.lower() for step in ai_fallback_plan))
        
        # Test category-specific fallback plan with no domain
        write_fallback_plan = get_fallback_plan("write", {})
        
        print(f"\n{colored('Writing category fallback plan:', 'green')}")
        for i, step in enumerate(write_fallback_plan, 1):
            print(f"  {i}. {step}")
        
        # Verify the writing-specific fallback plan
        self.assertTrue(any("draft" in step.lower() for step in write_fallback_plan))
        self.assertTrue(any("edit" in step.lower() for step in write_fallback_plan))
        
        # Test default fallback plan
        default_fallback_plan = get_fallback_plan("unknown", {})
        
        print(f"\n{colored('Default fallback plan:', 'green')}")
        for i, step in enumerate(default_fallback_plan, 1):
            print(f"  {i}. {step}")
        
        # Verify the default fallback plan - updated to expect 6 steps
        self.assertEqual(len(default_fallback_plan), 6)  # Should have 6 steps
        self.assertTrue(any("research" in step.lower() for step in default_fallback_plan))
        
        print(f"{colored('✅ Fallback plan generation verified for all scenarios', 'green')}")
    
    @patch('agentic_skeleton.core.azure.generator.call_azure_openai')
    @patch('agentic_skeleton.core.azure.generator.extract_subtasks_from_text')
    def test_generate_plan(self, mock_extract, mock_call_azure):
        """Test the plan generation with mocked Azure OpenAI call"""
        print(f"\n{colored('Testing plan generation with Azure...', 'blue')}")
        
        # Mock the Azure call to return a plan
        user_request = "Create a chatbot with natural language processing capabilities"
        mock_plan_text = """
        Here's my plan:
        1. Research recent advances in natural language processing
        2. Analyze the requirements for the chatbot system
        3. Design the conversation flow and user interactions
        4. Implement the core NLP processing pipeline
        5. Test the chatbot with sample user interactions
        6. Document the system and create user guidelines
        """
        mock_call_azure.return_value = mock_plan_text
        
        # Mock the extraction function to return our predefined subtasks
        expected_subtasks = [
            "Research recent advances in natural language processing",
            "Analyze the requirements for the chatbot system",
            "Design the conversation flow and user interactions",
            "Implement the core NLP processing pipeline",
            "Test the chatbot with sample user interactions",
            "Document the system and create user guidelines"
        ]
        mock_extract.return_value = expected_subtasks
        
        print(f"\n{colored('User request:', 'green')}")
        print(f"  \"{user_request}\"")
        
        # Generate a plan
        plan = generate_plan(user_request)
        
        print(f"\n{colored('Generated plan:', 'green')}")
        for i, task in enumerate(plan, 1):
            print(f"  {i}. {task}")
        
        # Verify the plan structure
        self.assertEqual(len(plan), 6)
        self.assertEqual(plan, expected_subtasks)
        self.assertTrue(any("research" in step.lower() for step in plan))
        self.assertTrue(any("implement" in step.lower() for step in plan))
        
        # Verify that Azure OpenAI was called correctly
        mock_call_azure.assert_called_once()
        
        print(f"{colored('✅ Plan generation with Azure verified', 'green')}")
    
    @patch('agentic_skeleton.core.azure.generator.call_azure_openai')
    def test_execute_subtasks(self, mock_call_azure):
        """Test the subtask execution with mocked Azure OpenAI call"""
        print(f"\n{colored('Testing subtask execution with Azure...', 'blue')}")
        
        # Mock the Azure call to return results
        user_request = "Create an NLP chatbot"
        mock_results = [
            "Result for subtask 1: Based on recent research in NLP, the most effective techniques for intent recognition include transformer-based models and BERT variants...",
            "Result for subtask 2: The recommended architecture for the chatbot system includes a natural language understanding component, dialog management, and response generation..."
        ]
        mock_call_azure.side_effect = mock_results
        
        # Subtasks to execute
        subtasks = [
            "Research NLP techniques for intent recognition",
            "Design an architecture for the chatbot system"
        ]
        
        print(f"\n{colored('User request:', 'green')}")
        print(f"  \"{user_request}\"")
        
        print(f"\n{colored('Subtasks to execute:', 'green')}")
        for i, task in enumerate(subtasks, 1):
            print(f"  {i}. {task}")
        
        # Execute subtasks
        results = execute_subtasks(subtasks, user_request)
        
        # Verify the results structure
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["task"], subtasks[0])
        self.assertEqual(results[0]["result"], mock_results[0])
        self.assertIn("type", results[0])
        self.assertEqual(results[1]["task"], subtasks[1])
        self.assertEqual(results[1]["result"], mock_results[1])
        self.assertIn("type", results[1])
        
        print(f"\n{colored('Results:', 'green')}")
        for i, result in enumerate(results, 1):
            print(f"  Task {i}: {result['task']}")
            print(f"    Type: {colored(result['type'], 'cyan')}")
            print(f"    Result sample: {result['result'][:100]}...")
        
        # Verify that Azure OpenAI was called correctly
        self.assertEqual(mock_call_azure.call_count, 2)
        
        print(f"{colored('✅ Subtask execution with Azure verified', 'green')}")
    
    @patch('agentic_skeleton.core.azure.client.initialize_client')
    def test_complete_workflow_with_azure(self, mock_initialize_client):
        """Test the complete workflow with Azure integration"""
        print(f"\n{colored('Testing complete workflow with Azure integration', 'blue')}")
        
        # Setup the client mocking
        mock_client = MagicMock()
        mock_initialize_client.return_value = mock_client
        
        # Mock the client response for the plan
        mock_client.generate_completion.side_effect = [
            "1. Research recent AI applications in healthcare\n2. Analyze medical data processing techniques\n3. Explore diagnostic use cases\n4. Evaluate machine learning models for patient care\n5. Examine ethical considerations",
            "Result 1 for healthcare AI research...",
            "Result 2 for medical data analysis...",
            "Result 3 for diagnostic applications...",
            "Result 4 for patient care models...",
            "Result 5 for ethical considerations..."
        ]
        
        # Patch settings to use Azure mode
        with patch('agentic_skeleton.config.settings.is_using_mock', return_value=False):
            # Define the request
            request_data = {
                "request": "Analyze AI applications in healthcare"
            }
            
            # Call the endpoint
            print(f"{colored('Calling run-agent endpoint in Azure mode...', 'yellow')}")
            response = self.app.post('/run-agent', json=request_data)
            
            # Verify response
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            
            # Verify the response structure
            self.assertIn('plan', data)
            self.assertIn('results', data)
            
            # Print the plan
            print(f"\n{colored('Generated plan:', 'green')}")
            for i, task in enumerate(data['plan'], 1):
                print(f"  {i}. {task}")
            
            # Print results
            print(f"\n{colored('Results:', 'green')}")
            for i, result in enumerate(data['results'], 1):
                print(f"  Task {i}: {result['subtask']}")
                if 'result' in result:
                    print(f"    Result sample: {result['result'][:100]}...")
                else:
                    print(f"    No result found")
            
            # Validate that healthcare and AI terms are mentioned
            all_results = ' '.join([r.get('result', '') for r in data['results'] if 'result' in r]).lower()
            healthcare_terms = ['healthcare', 'medical', 'patient', 'diagnosis', 'clinical', 'treatment']
            ai_terms = ['ai', 'artificial intelligence', 'machine learning', 'algorithm', 'model', 'neural']
            
            found_healthcare = any(term in all_results for term in healthcare_terms)
            found_ai = any(term in all_results for term in ai_terms)
            
            self.assertTrue(found_healthcare, "No healthcare terms found in response")
            self.assertTrue(found_ai, "No AI terms found in response")
            
            print(f"{colored('✓ Successfully generated healthcare AI analysis with Azure integration', 'green')}")

if __name__ == "__main__":
    # Print header with ASCII art
    header = format_terminal_header("🧪 Azure Integration Tests", settings.is_using_mock())
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