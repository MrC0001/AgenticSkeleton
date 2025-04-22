"""
Mock Response Generator
======================

Provides mock data and mock response generation for the agent.
Used in development and testing mode when Azure OpenAI is not available.
"""

import logging
from typing import Dict, List, Tuple

from agentic_skeleton.core.mock.classifier import classify_request, detect_domain_specialization
from agentic_skeleton.core.mock.generator import get_mock_task_response
from agentic_skeleton.core.mock.constants.mock_plans import MOCK_PLANS

def generate_mock_plan_and_results(user_request: str) -> Tuple[List[str], List[Dict]]:
    """
    Generate a mock plan and results for a user request.
    
    Args:
        user_request: The user's request text
        
    Returns:
        Tuple containing (subtasks, results)
    """
    logging.info("Starting mock plan generation and execution")
    
    # Get appropriate plan based on request classification
    plan_type = classify_request(user_request)
    subtasks = MOCK_PLANS[plan_type]
    
    # Generate results for each subtask
    results = []
    for task in subtasks:
        # Get a dynamic response for this task
        response = get_mock_task_response(task)
        
        results.append({
            "subtask": task,
            "result": response
        })
        
    return subtasks, results