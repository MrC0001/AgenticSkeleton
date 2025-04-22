"""
Mock Request Classifier
======================

Classifies user requests into predefined categories for the mock response generator.
"""

import logging
from typing import List, Dict, Tuple, Any

def classify_request(user_request: str) -> str:
    """
    Classify a user request into one of the predefined plan types.
    
    Args:
        user_request: The user request text
        
    Returns:
        Plan type as a string (e.g., "write", "analyze", "develop")
    """
    request_lower = user_request.lower()
    
    # Define classifiers with their patterns also priority fallback in case of = pattern matches... 1st match wins... call it a feature (:
    request_classifiers = [
        {
            "type": "data-science",
            "patterns": [
                "machine learning", "ml model", "predictive model", "data mining", 
                "train model", "neural network", "clustering", "classification algorithm",
                "regression", "feature engineering", "data preprocessing", "dataset",
                "predict", "forecasting", "ai model", "customer churn", "nlp", "train"
            ]
        },
        {
            "type": "analyze",
            "patterns": [
                "analyze", "analysis", "evaluate", "assess", "review", "study", 
                "research", "compare", "investigate", "examine", "trends", "patterns",
                "market analysis", "competitive analysis", "impact", "implications"
            ]
        },
        {
            "type": "design",
            "patterns": [
                "design", "wireframe", "sketch", "mock up", "prototype", "ui", "ux",
                "user interface", "user experience", "layout", "visual", "graphics",
                "augmented reality interface", "ar", "vr", "user flow", "design system"
            ]
        },
        {
            "type": "write",
            "patterns": [
                "write", "draft", "blog", "article", "post", "essay", "content", 
                "copywriting", "script", "document", "report", "whitepaper", "create content"
            ]
        },
        {
            "type": "develop",
            "patterns": [
                "develop", "build", "implement", "code", "program", 
                "website", "backend", "frontend", "software", "function", "class", 
                "module", "database", "rest api"
            ]
        }
    ]
    
    # 1. Detect explicit complex multi-domain phrases
    explicit_complex_task = (
        any(term in request_lower for term in [
            "comprehensive plan", "end-to-end", "full stack", "multi-phase", 
            "platform", "ecosystem", "integrated system", "launch"
        ]) and len(request_lower.split()) > 15
    )
    
    # 2. Check for multiple domain matches (implicit complex task)
    domain_matches = []
    for classifier in request_classifiers:
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
    # This function should be implemented based on the domain knowledge constants
    # It would check if the user request contains keywords from specific domains
    # For now, return a simple placeholder
    return {"domain": "general", "confidence": 1.0}

def classify_subtask(subtask: str, domain_info: Dict[str, Any]) -> str:
    """
    Classify a subtask to determine the appropriate response template.
    
    Args:
        subtask: The subtask description
        domain_info: Domain specialization information
        
    Returns:
        Subtask type as a string
    """
    # Placeholder implementation
    subtask_lower = subtask.lower()
    
    if any(term in subtask_lower for term in ["research", "analyze", "study", "investigate"]):
        return "research"
    elif any(term in subtask_lower for term in ["implement", "build", "code", "develop", "create"]):
        return "develop"
    elif any(term in subtask_lower for term in ["design", "sketch", "prototype"]):
        return "design"
    elif any(term in subtask_lower for term in ["write", "draft", "document"]):
        return "write"
    elif any(term in subtask_lower for term in ["train", "model", "data"]):
        return "data-science"
    else:
        return "default"