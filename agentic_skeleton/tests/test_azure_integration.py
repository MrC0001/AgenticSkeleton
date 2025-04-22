"""
Unit Tests for Azure Integration Module
============================

Tests the enhanced Azure integration functionality independently.
"""

import unittest
from unittest.mock import patch, MagicMock
import logging

# Updated imports to match the new modular structure
from agentic_skeleton.core.azure.classifier import classify_request, detect_domain_specialization, classify_subtask
from agentic_skeleton.core.azure.generator import generate_plan, execute_subtasks
from agentic_skeleton.core.azure.client import call_azure_openai
from agentic_skeleton.core.azure.enhancer import (
    enhance_prompt_with_domain_knowledge,
    enhance_subtask_prompt
)
from agentic_skeleton.core.azure.constants.fallback_plans import get_fallback_plan

class TestAzureIntegration(unittest.TestCase):
    """Unit tests for the enhanced Azure integration module"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Disable logging during tests
        logging.disable(logging.CRITICAL)
    
    def tearDown(self):
        """Clean up after tests"""
        # Re-enable logging after tests
        logging.disable(logging.NOTSET)
    
    def test_request_classification(self):
        """Test the request classification functionality"""
        # Data Science requests
        self.assertEqual(classify_request("Train a machine learning model for customer churn"), "data-science")
        self.assertEqual(classify_request("Create a neural network for image classification"), "data-science")
        self.assertEqual(classify_request("Build a predictive model for sales forecasting"), "data-science")
        
        # Analytical requests
        self.assertEqual(classify_request("Analyze market trends in renewable energy"), "analyze")
        self.assertEqual(classify_request("Investigate the impact of remote work on productivity"), "analyze")
        self.assertEqual(classify_request("Research consumer behavior patterns in e-commerce"), "analyze")
        
        # Development requests
        self.assertEqual(classify_request("Develop a REST API for user authentication"), "develop")
        self.assertEqual(classify_request("Create a backend database schema"), "develop")
        self.assertEqual(classify_request("Build a responsive web interface"), "develop")
        
        # Design requests
        self.assertEqual(classify_request("Design a user interface for a mobile app"), "design")
        self.assertEqual(classify_request("Create wireframes for an e-commerce website"), "design")
        self.assertEqual(classify_request("Design an augmented reality interface"), "design")
        
        # Writing requests
        self.assertEqual(classify_request("Write a blog post about sustainable technology"), "write")
        self.assertEqual(classify_request("Draft a technical whitepaper on blockchain"), "write")
        self.assertEqual(classify_request("Create content for a software product launch"), "write")
        
        # Complex multi-domain requests
        complex_request = "Create a comprehensive end-to-end platform for analyzing customer data, " \
                          "predicting churn and automatically generating personalized retention emails"
        # This should be classified as data-science since it's the dominant theme
        self.assertEqual(classify_request(complex_request), "data-science")
    
    def test_domain_specialization_detection(self):
        """Test the domain specialization detection functionality"""
        # Cloud computing domain
        cloud_request = "Design a multi-region cloud deployment architecture for our application"
        cloud_domain = detect_domain_specialization(cloud_request)
        self.assertEqual(cloud_domain['name'], "cloud_computing")
        self.assertIn("guidance", cloud_domain)
        self.assertEqual(cloud_domain['preferred_category'], "develop")
        
        # AI/ML domain
        ai_request = "Develop a generative AI model for creating marketing content"
        ai_domain = detect_domain_specialization(ai_request)
        self.assertEqual(ai_domain['name'], "ai_ml")
        self.assertIn("guidance", ai_domain)
        self.assertEqual(ai_domain['preferred_category'], "data-science")
        
        # Healthcare domain
        health_request = "Build a telehealth platform for remote patient monitoring"
        health_domain = detect_domain_specialization(health_request)
        self.assertEqual(health_domain['name'], "healthcare_tech")
        self.assertIn("guidance", health_domain)
        self.assertEqual(health_domain['preferred_category'], "analyze")
        
        # No specific domain
        generic_request = "Write a blog post about company culture"
        generic_domain = detect_domain_specialization(generic_request)
        self.assertEqual(generic_domain, {})
    
    def test_subtask_classification(self):
        """Test the subtask classification functionality"""
        # Basic subtask classification
        self.assertEqual(classify_subtask("Research recent advances in natural language processing", {}), "research")
        self.assertEqual(classify_subtask("Implement a user authentication system", {}), "implement")
        self.assertEqual(classify_subtask("Design a database schema for user profiles", {}), "design")
        self.assertEqual(classify_subtask("Test the API endpoints for performance", {}), "evaluate")
        self.assertEqual(classify_subtask("Document the system architecture", {}), "document")
        
        # Domain-specific subtask classification
        ai_domain = detect_domain_specialization("Train a machine learning model for text classification")
        self.assertEqual(classify_subtask("Gather and preprocess training data", ai_domain), "data")
        self.assertEqual(classify_subtask("Train the classification model", ai_domain), "model")
        self.assertEqual(classify_subtask("Deploy the model as a prediction API", ai_domain), "deploy")
        
        cloud_domain = detect_domain_specialization("Optimize cloud costs for our multi-region deployment")
        self.assertEqual(classify_subtask("Research cost optimization strategies", cloud_domain), "research")
        self.assertEqual(classify_subtask("Implement auto-scaling policies", cloud_domain), "implement")
        self.assertEqual(classify_subtask("Optimize resource allocation", cloud_domain), "optimize")
    
    def test_prompt_enhancement(self):
        """Test the prompt enhancement functionality"""
        # Test basic prompt enhancement
        test_prompt = "Generate a response for the following task:"
        enhanced_prompt = enhance_prompt_with_domain_knowledge(
            test_prompt, 
            "Build a machine learning model for customer churn prediction", 
            "data-science"
        )
        
        # Check that the category guidance is included
        self.assertIn("data-science", enhanced_prompt.lower())
        self.assertIn("model development", enhanced_prompt.lower())
        
        # Test domain-specific prompt enhancement
        ai_domain = detect_domain_specialization("Train a neural network for image recognition")
        domain_enhanced_prompt = enhance_prompt_with_domain_knowledge(
            test_prompt, 
            "Train a neural network for image recognition",
            "data-science",
            ai_domain
        )
        
        # Check that domain guidance is included
        self.assertIn("domain specialization", domain_enhanced_prompt.lower())
        self.assertIn("ai_ml", domain_enhanced_prompt.lower())
        
        # Test subtask prompt enhancement
        subtask_enhanced_prompt = enhance_subtask_prompt(
            test_prompt,
            "Train a neural network for image recognition",
            "Preprocess and augment the image dataset",
            "data-science",
            ai_domain,
            "data"
        )
        
        # Check that subtask-specific guidance is included
        self.assertIn("subtask type", subtask_enhanced_prompt.lower())
        self.assertIn("data", subtask_enhanced_prompt.lower())
    
    def test_get_fallback_plan(self):
        """Test the fallback plan generation functionality"""
        # Test domain-specific fallback plan
        ai_domain = detect_domain_specialization("Train a machine learning model for text classification")
        ai_fallback_plan = get_fallback_plan("data-science", ai_domain)
        
        # Verify the AI-specific fallback plan
        self.assertTrue(any("data" in step.lower() for step in ai_fallback_plan))
        self.assertTrue(any("model" in step.lower() for step in ai_fallback_plan))
        self.assertTrue(any("train" in step.lower() for step in ai_fallback_plan))
        
        # Test category-specific fallback plan with no domain
        write_fallback_plan = get_fallback_plan("write", {})
        
        # Verify the writing-specific fallback plan
        self.assertTrue(any("draft" in step.lower() for step in write_fallback_plan))
        self.assertTrue(any("edit" in step.lower() for step in write_fallback_plan))
        
        # Test default fallback plan
        default_fallback_plan = get_fallback_plan("unknown", {})
        
        # Verify the default fallback plan
        self.assertEqual(len(default_fallback_plan), 5)  # Should have 5 steps
        self.assertTrue(any("research" in step.lower() for step in default_fallback_plan))
    
    @patch('agentic_skeleton.core.azure.client.call_azure_openai')
    def test_generate_plan(self, mock_call_azure):
        """Test the plan generation with mocked Azure OpenAI call"""
        # Mock the Azure call to return a plan
        mock_plan_text = """
        Here's my plan:
        1. Research recent advances in natural language processing
        2. Analyze the requirements for the chatbot system
        3. Design the conversation flow and user interactions
        4. Implement the core NLP processing pipeline
        5. Test the chatbot with sample user interactions
        """
        mock_call_azure.return_value = mock_plan_text
        
        # Generate a plan
        plan = generate_plan("Create a chatbot with natural language processing capabilities")
        
        # Verify the plan structure
        self.assertEqual(len(plan), 5)
        self.assertTrue(any("research" in step.lower() for step in plan))
        self.assertTrue(any("implement" in step.lower() for step in plan))
        
        # Verify that Azure OpenAI was called correctly
        mock_call_azure.assert_called_once()
    
    @patch('agentic_skeleton.core.azure.client.call_azure_openai')
    def test_execute_subtasks(self, mock_call_azure):
        """Test the subtask execution with mocked Azure OpenAI call"""
        # Mock the Azure call to return results
        mock_results = ["Result for subtask 1", "Result for subtask 2"]
        mock_call_azure.side_effect = mock_results
        
        # Execute subtasks
        subtasks = [
            "Research NLP techniques for intent recognition",
            "Design an architecture for the chatbot system"
        ]
        results = execute_subtasks(subtasks, "Create an NLP chatbot")
        
        # Verify the results structure
        self.assertEqual(len(results), 2)
        # Updated to use 'task' key to match the implementation in generator.py
        self.assertEqual(results[0]["task"], subtasks[0])
        self.assertEqual(results[0]["result"], mock_results[0])
        self.assertEqual(results[1]["task"], subtasks[1])
        self.assertEqual(results[1]["result"], mock_results[1])
        
        # Verify that Azure OpenAI was called correctly
        self.assertEqual(mock_call_azure.call_count, 2)

if __name__ == "__main__":
    unittest.main()