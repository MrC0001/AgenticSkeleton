"""
Azure Generator
======================

Provides functionality for generating plans and executing subtasks using Azure OpenAI.
"""

import logging
from typing import Dict, List, Any, Optional, Tuple

from agentic_skeleton.config import settings
from agentic_skeleton.utils.helpers import extract_subtasks_from_text
from agentic_skeleton.core.azure.classifier import classify_request, detect_domain_specialization, classify_subtask
from agentic_skeleton.core.azure.client import call_azure_openai
from agentic_skeleton.core.azure.enhancer import enhance_prompt_with_domain_knowledge, enhance_subtask_prompt
from agentic_skeleton.core.azure.constants.fallback_plans import get_fallback_plan

# ----------------------------------------
#  STEP 1: GENERATE PLAN WITH AZURE OPENAI
# ----------------------------------------
def generate_plan(user_request: str) -> List[str]:
    """
    Generate a plan using Azure OpenAI.
    
    Args:
        user_request: The user's request
        
    Returns:
        List of subtasks
    """
    logging.info("Generating plan with Azure OpenAI")
    
    # 1. Determine request category and domain specialization
    request_category = classify_request(user_request)
    domain_info = detect_domain_specialization(user_request)
    
    # 2. Enhance prompt with domain knowledge
    planner_prompt = settings.PLANNER_TEMPLATE.format(user_request=user_request)
    enhanced_prompt = enhance_prompt_with_domain_knowledge(
        planner_prompt, 
        user_request, 
        request_category,
        domain_info
    )
    
    # 3. Call Azure OpenAI to generate the plan
    plan_text = call_azure_openai(settings.MODEL_PLANNER, enhanced_prompt)
    
    # 4. Extract subtasks from the response
    subtasks = extract_subtasks_from_text(plan_text)
    
    # 5. Provide fallback if extraction failed
    if not subtasks:
        logging.warning(f"Failed to extract subtasks from plan text: {plan_text}")
        # Use appropriate fallback based on request category
        return get_fallback_plan(request_category)
        
    return subtasks


# ----------------------------------------
#  STEP 2: EXECUTE SUBTASKS
# ----------------------------------------
def execute_subtasks(subtasks: List[str], user_request: str) -> List[Dict[str, str]]:
    """
    Execute all subtasks using Azure OpenAI.
    
    Args:
        subtasks: List of subtask descriptions
        user_request: The original user request for domain context
        
    Returns:
        List of dictionaries with subtask descriptions and results
    """
    results = []
    logging.info(f"Executing {len(subtasks)} subtasks")
    
    # 1. Pre-classify request and detect domain for consistent handling
    request_category = classify_request(user_request)
    domain_info = detect_domain_specialization(user_request)
    
    for i, task in enumerate(subtasks, 1):
        logging.info(f"Executing subtask {i}/{len(subtasks)}: {task[:30]}...")
        
        # 2. Detect subtask type for better prompt engineering
        subtask_type = classify_subtask(task, domain_info)
        
        # 3. Enhance executor prompt with domain knowledge and subtask type
        executor_prompt = settings.EXECUTOR_TEMPLATE.format(subtask=task)
        enhanced_prompt = enhance_subtask_prompt(
            executor_prompt, 
            user_request, 
            task, 
            request_category,
            domain_info,
        )
        
        # 4. Call Azure OpenAI to execute the subtask
        try:
            result_text = call_azure_openai(settings.MODEL_EXECUTOR, enhanced_prompt)
            
            # 5. Store the result
            results.append({
                "task": task,
                "result": result_text,
                "type": subtask_type
            })
            
            logging.info(f"Completed subtask {i}/{len(subtasks)}")
        except Exception as e:
            logging.error(f"Error executing subtask {i}: {str(e)}")
            results.append({
                "task": task,
                "result": f"Error: {str(e)}",
                "type": subtask_type
            })
    
    return results