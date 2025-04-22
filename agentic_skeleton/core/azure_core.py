"""
Azure OpenAI Integration
======================

Entry point for Azure OpenAI integration. Orchestrates the modular components
for generating plans and executing tasks. Used in production mode.
"""

import logging
from typing import Dict, List, Tuple, Any

from agentic_skeleton.core.azure.generator import generate_plan as _generate_plan, execute_subtasks as _execute_subtasks
from agentic_skeleton.core.azure.constants.fallback_plans import get_fallback_plan as _get_fallback_plan

# Re-export functions needed by tests
generate_plan = _generate_plan
execute_subtasks = _execute_subtasks
get_fallback_plan = _get_fallback_plan

def generate_azure_plan_and_results(user_request: str) -> Tuple[List[str], List[Dict[str, Any]]]:
    """
    Generate a plan and results using Azure OpenAI.
    
    Args:
        user_request: The user's request text
        
    Returns:
        Tuple containing (subtasks, results)
    """
    logging.info("Starting Azure OpenAI plan generation and execution")
    
    # Generate the plan using the modular generator
    subtasks = generate_plan(user_request)
    
    # Execute each subtask using the modular executor
    results = execute_subtasks(subtasks, user_request)
    
    return subtasks, results