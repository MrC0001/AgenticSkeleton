"""
Azure Prompt Enhancer
======================

Enhances prompts with domain-specific knowledge and request context for Azure OpenAI.
"""

import logging
from typing import Dict, List, Any, Optional

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
        task_guidance = {
            "write": "Focus on creating high-quality written content with attention to structure, audience engagement, and clarity.",
            "analyze": "Emphasize data-driven insights, critical evaluation, and actionable recommendations.",
            "develop": "Prioritize technical implementation details, architecture, best practices, and code organization.",
            "design": "Concentrate on user experience, interface design principles, accessibility, and visual coherence.",
            "data-science": "Focus on data processing, model development, validation, and deployment considerations."
        }
        
        category_guidance = task_guidance.get(request_category, "")
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
        subtask_guidance = {
            "research": "Provide comprehensive, well-structured findings with cited sources and a focus on recent developments.",
            "implement": "Detail the implementation approach with consideration for scalability, maintainability, and best practices.",
            "design": "Present the design with clear rationale, addressing user needs and technical constraints.",
            "evaluate": "Offer data-based evaluation with clear metrics, comparison points, and actionable insights.",
            "optimize": "Focus on specific improvements, quantifying benefits and implementation complexity.",
            "document": "Create clear, structured documentation with appropriate technical depth.",
            "data": "Detail data sources, preprocessing steps, quality assessments, and feature engineering.",
            "model": "Explain model selection, training approach, hyperparameter choices, and performance metrics.",
            "deploy": "Address deployment architecture, scaling considerations, monitoring, and maintenance.",
            "impact": "Analyze effects across multiple dimensions with quantified metrics and stakeholder considerations."
        }
        
        guidance = subtask_guidance.get(subtask_type, "")
        if guidance:
            enhanced_prompt += f"\n\nSubtask Type: {subtask_type.capitalize()}\n{guidance}\n"
    
    # Add stage awareness
    if "research" in subtask.lower() and any(term in user_request.lower() for term in ["comprehensive", "thorough", "detailed"]):
        enhanced_prompt += "\n\nThis is a research subtask. Be thorough and prioritize breadth and depth of information gathering."
    elif any(term in subtask.lower() for term in ["draft", "create", "write", "develop"]):
        enhanced_prompt += "\n\nThis is a creation subtask. Focus on generating high-quality, original content."
    elif any(term in subtask.lower() for term in ["refine", "improve", "optimize", "edit"]):
        enhanced_prompt += "\n\nThis is a refinement subtask. Focus on enhancing quality, efficiency, and effectiveness."
    
    return enhanced_prompt