"""
Mock Request Classifier
======================

Classifies user requests into predefined categories for the mock response generator.
"""

import logging
from typing import List, Dict, Tuple, Any
from agentic_skeleton.core.mock.constants import REQUEST_CLASSIFIERS, COMPLEX_TASK_INDICATORS, GENERIC_SUBTASK_PATTERNS

def classify_request(user_request: str) -> str:
    """
    Classify a user request into one of the predefined plan types.
    
    Args:
        user_request: The user request text
        
    Returns:
        Plan type as a string (e.g., "write", "analyze", "develop")
    """
    request_lower = user_request.lower()
    
    # 1. Detect explicit complex multi-domain phrases
    explicit_complex_task = (
        any(term in request_lower for term in COMPLEX_TASK_INDICATORS) and 
        len(request_lower.split()) > 15
    )
    
    # 2. Check for multiple domain matches (implicit complex task)
    domain_matches = []
    for classifier in REQUEST_CLASSIFIERS:
        matches = sum(1 for pattern in classifier["patterns"] if pattern in request_lower)
        if matches > 0:
            domain_matches.append((classifier["type"], matches))
    
    # Consider it complex if we match more than one domain type
    implicit_complex_task = len(domain_matches) > 1
    
    # 3. Handle complex tasks
    if explicit_complex_task or implicit_complex_task:
        logging.info(f"Complex task detected - domains: {[d[0] for d in domain_matches]}")
        
        # Use the most dominant theme or data-science as fallback
        if domain_matches:
            dominant_type = max(domain_matches, key=lambda x: x[1])[0]
            logging.info(f"Using dominant classification: {dominant_type}")
            return dominant_type
        else:
            return "data-science"
    
    # 4. Handle simple tasks with a single domain
    if domain_matches:
        plan_type = domain_matches[0][0]
        logging.info(f"Request classified as: {plan_type}")
        return plan_type
    
    # 5. Default classification if no patterns match
    logging.info(f"No specific patterns matched, using default classification")
    return "default"

def detect_domain_specialization(user_request: str) -> Dict[str, Any]:
    """
    Detect specialized domain knowledge required for the request.
    
    Args:
        user_request: The user's request text
        
    Returns:
        Dictionary with domain specialization information
    """
    from agentic_skeleton.core.mock.constants.domain_knowledge import DOMAIN_KNOWLEDGE
    
    request_lower = user_request.lower()
    domain_matches = []
    
    # Check each domain for keyword matches
    for domain_name, domain_data in DOMAIN_KNOWLEDGE.items():
        matches = [kw for kw in domain_data["keywords"] if kw in request_lower]
        if matches:
            domain_matches.append({
                "domain": domain_name,
                "matched_keywords": matches,
                "confidence": 0.9,  # High confidence for direct keyword match
                "subtasks": domain_data["subtasks"]
            })
    
    # No specific domain detected
    if not domain_matches:
        return {}
    
    # For multi-domain requests (like "machine learning in healthcare"), 
    # prioritize domains that may be missed in response generation
    if len(domain_matches) > 1:
        # If we have both ai_ml and healthcare_tech, merge them with healthcare taking precedence
        ai_ml_match = next((match for match in domain_matches if match["domain"] == "ai_ml"), None)
        healthcare_match = next((match for match in domain_matches if match["domain"] == "healthcare_tech"), None)
        
        if ai_ml_match and healthcare_match:
            # Prioritize healthcare
            primary_domain = healthcare_match
            # But include the AI/ML keywords
            primary_domain["additional_domains"] = [ai_ml_match["domain"]]
            primary_domain["additional_keywords"] = ai_ml_match["matched_keywords"]
            return primary_domain
    
    # Return the first match (most dominant) for simple cases
    return domain_matches[0]

def classify_subtask(subtask: str, domain_info: Dict[str, Any]) -> str:
    """
    Classify a subtask to determine the appropriate response template.
    
    Args:
        subtask: The subtask description
        domain_info: Domain specialization information
        
    Returns:
        Subtask type as a string
    """
    subtask_lower = subtask.lower()
    
    # If we have domain-specific information, use it for more accurate classification
    if domain_info and "subtasks" in domain_info:
        domain = domain_info.get("domain")
        subtasks = domain_info.get("subtasks", {})
        
        # Check each subtask type in the domain
        for subtask_type, subtask_data in subtasks.items():
            patterns = subtask_data.get("patterns", [])
            if any(pattern in subtask_lower for pattern in patterns):
                return subtask_type
    
    # Fall back to generic classification if no domain match or no pattern match
    for subtask_type, patterns in GENERIC_SUBTASK_PATTERNS.items():
        if any(pattern in subtask_lower for pattern in patterns):
            return subtask_type
            
    return "default"