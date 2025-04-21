"""
Azure OpenAI Integration
======================

Provides integration with Azure OpenAI for generating plans and executing tasks.
Used in production mode when mock responses are disabled.
"""

import logging
import re
from typing import Dict, List, Any, Optional, Tuple

# Optional: Import Azure OpenAI only when needed
try:
    from openai import AzureOpenAI
except ImportError:
    AzureOpenAI = None

from agentic_skeleton.config import settings
from agentic_skeleton.utils.helpers import extract_subtasks_from_text

# Global client instance
azure_client = None

def initialize_client() -> Optional[Any]:
    """
    Initialize the Azure OpenAI client.
    
    Returns:
        Azure OpenAI client if successful, None if initialization fails
    """
    global azure_client
    
    if azure_client:
        return azure_client
    
    if not settings.validate_azure_config():
        logging.warning("Azure OpenAI credentials not found or incomplete")
        return None
    
    try:
        azure_client = AzureOpenAI(
            api_key=settings.AZURE_KEY,
            azure_endpoint=settings.AZURE_ENDPOINT,
            api_version=settings.AZURE_API_VERSION
        )
        logging.info("Azure OpenAI client initialized successfully")
        return azure_client
    except Exception as e:
        logging.error(f"Failed to initialize Azure OpenAI client: {e}")
        return None





def call_azure_openai(model: str, prompt: str) -> str:
    """
    Call Azure OpenAI API with error handling.
    
    Args:
        model: The model deployment name
        prompt: The prompt to send to the model
        
    Returns:
        Generated response text or error message
    """
    client = initialize_client()
    if not client:
        return "Error: Azure OpenAI client not initialized"
    
    try:
        logging.info(f"Calling Azure OpenAI with model: {model}")
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": prompt}],
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        error_msg = f"Azure OpenAI API call failed: {e}"
        logging.error(error_msg)
        return f"Error: {str(e)}"





def enhance_prompt_with_domain_knowledge(prompt: str, user_request: str) -> str:
    """
    Enhance a prompt with domain-specific knowledge if applicable.
    
    Args:
        prompt: The original prompt template
        user_request: The user's request text
        
    Returns:
        Enhanced prompt with domain knowledge if applicable, original prompt otherwise
    """
    request_lower = user_request.lower()
    
    # Check for domain matches using Azure's domain knowledge
    for domain, info in settings.AZURE_DOMAIN_KNOWLEDGE.items():
        if any(keyword in request_lower for keyword in info["keywords"]):
            # Add the domain-specific context to the prompt
            domain_info = f"\n\nDomain-Specific Context:\n{info['context']}\n"
            
            # Add preferred approach if available
            if "preferred_approach" in info:
                domain_info += f"\nRecommended approach: {info['preferred_approach']}.\n"
            
            return prompt + domain_info
    
    return prompt





def generate_plan(user_request: str) -> List[str]:
    """
    Generate a plan using Azure OpenAI.
    
    Args:
        user_request: The user's request
        
    Returns:
        List of subtasks
    """
    logging.info("Generating plan with Azure OpenAI")
    
    # Enhance prompt with domain knowledge
    planner_prompt = settings.PLANNER_TEMPLATE.format(user_request=user_request)
    enhanced_prompt = enhance_prompt_with_domain_knowledge(planner_prompt, user_request)
    
    plan_text = call_azure_openai(settings.MODEL_PLANNER, enhanced_prompt)
    
    # Extract subtasks from the response
    subtasks = extract_subtasks_from_text(plan_text)
    
    if not subtasks:
        logging.warning(f"Failed to extract subtasks from plan text: {plan_text}")
        # Return a default plan as fallback
        return ["Research the topic", "Organize findings", "Create deliverable"]
        
    return subtasks





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
    
    for i, task in enumerate(subtasks, 1):
        logging.info(f"Executing subtask {i}/{len(subtasks)}: {task[:30]}...")
        
        # Enhance executor prompt with domain knowledge
        executor_prompt = settings.EXECUTOR_TEMPLATE.format(subtask=task)
        enhanced_prompt = enhance_prompt_with_domain_knowledge(executor_prompt, user_request)
        
        result = call_azure_openai(settings.MODEL_EXECUTOR, enhanced_prompt)
        results.append({
            "subtask": task,
            "result": result
        })
    
    return results





def generate_azure_plan_and_results(user_request: str) -> Tuple[List[str], List[Dict]]:
    """
    Generate a plan and results using Azure OpenAI.
    
    Args:
        user_request: The user's request text
        
    Returns:
        Tuple containing (subtasks, results)
    """
    # Generate the plan
    subtasks = generate_plan(user_request)
    
    # Execute each subtask
    results = execute_subtasks(subtasks, user_request)
    
    return subtasks, results