"""
Azure Prompt Enhancer
======================

Enhances prompts with domain-specific knowledge and request context for Azure OpenAI.
"""

import logging
from typing import Dict, List, Any, Optional
from agentic_skeleton.core.azure.constants.prompt_guidance import TASK_GUIDANCE, SUBTASK_GUIDANCE, STAGE_GUIDANCE

def enhance_prompt_with_domain_knowledge(prompt: str, user_request: str, 
                                        request_category: str = "", 
                                        domain_info: Dict[str, Any] = {}) -> str:
    """
    Enhance a prompt with domain-specific knowledge and request categorization.
    
    Args:
        prompt: The original prompt template
        user_request: The user's request text
        request_category: The classified request category
        domain_info: Domain specialization information
        
    Returns:
        Enhanced prompt with relevant knowledge and context
    """
    enhanced_prompt = prompt
    
    # 1. Add request category information
    if request_category:
        category_guidance = TASK_GUIDANCE.get(request_category, "")
        if category_guidance:
            enhanced_prompt += f"\n\nTask Category: {request_category.capitalize()}\n{category_guidance}\n"
    
    # 2. Add domain-specific knowledge if available
    if domain_info:
        domain_prompt = f"\n\nDomain Specialization: {domain_info['name']}\n"
        domain_prompt += f"{domain_info.get('guidance', '')}\n"
        
        if domain_info.get('matched_keyword'):
            domain_prompt += f"Topic keyword: {domain_info['matched_keyword']}\n"
            
        enhanced_prompt += domain_prompt
    
    # 3. Check for technical and professional tone
    if any(term in user_request.lower() for term in ["technical", "professional", "formal", "detailed"]):
        enhanced_prompt += "\n\nPlease maintain a formal, technical tone appropriate for professional audiences."
    
    return enhanced_prompt


def enhance_subtask_prompt(prompt: str, user_request: str, subtask: str, 
                          request_category: str = "", 
                          domain_info: Dict[str, Any] = {}, 
                          subtask_type: str = "") -> str:
    """
    Create specialized prompts for subtask execution based on domain and subtask type.
    
    Args:
        prompt: The original prompt template
        user_request: The user's request text
        subtask: The specific subtask being executed
        request_category: The classified request category
        domain_info: Domain specialization information
        subtask_type: The classified subtask type
        
    Returns:
        Enhanced prompt optimized for the specific subtask
    """
    # Start with domain knowledge enhancement
    enhanced_prompt = enhance_prompt_with_domain_knowledge(prompt, user_request, request_category, domain_info)
    
    # Add subtask-specific guidance
    if subtask_type:
        guidance = SUBTASK_GUIDANCE.get(subtask_type, "")
        if guidance:
            enhanced_prompt += f"\n\nSubtask Type: {subtask_type.capitalize()}\n{guidance}\n"
    
    # Add stage awareness
    subtask_lower = subtask.lower()
    if "research" in subtask_lower and any(term in user_request.lower() for term in ["comprehensive", "thorough", "detailed"]):
        enhanced_prompt += f"\n\n{STAGE_GUIDANCE['research']}"
    elif any(term in subtask_lower for term in ["draft", "create", "write", "develop"]):
        enhanced_prompt += f"\n\n{STAGE_GUIDANCE['creation']}"
    elif any(term in subtask_lower for term in ["refine", "improve", "optimize", "edit"]):
        enhanced_prompt += f"\n\n{STAGE_GUIDANCE['refinement']}"
    
    return enhanced_prompt