"""
Azure Fallback Plans
======================

Provides fallback plans to use when plan generation fails.
These are used as a last resort when the Azure OpenAI call fails or returns unusable results.
"""

from typing import Dict, List, Any

# Fallback plans for different request categories
FALLBACK_PLANS = {
    "write": [
        "Research the topic and gather relevant information",
        "Create an outline with key points and structure",
        "Draft the initial content following the outline",
        "Review and revise the content for clarity and coherence",
        "Edit for grammar, style, and formatting",
        "Prepare the final version with any necessary citations"
    ],
    
    "analyze": [
        "Define the scope and objectives of the analysis",
        "Gather and organize relevant data and information",
        "Identify patterns, trends, and insights from the data",
        "Evaluate the findings against established criteria or benchmarks",
        "Draw conclusions based on the analysis",
        "Formulate recommendations based on the conclusions"
    ],
    
    "develop": [
        "Gather requirements and define specifications",
        "Design the system architecture and component interactions",
        "Implement the core functionality and features",
        "Create tests to verify correctness and performance",
        "Debug issues and optimize the implementation",
        "Document the system architecture and usage instructions"
    ],
    
    "design": [
        "Research user needs and create user personas",
        "Define information architecture and user flows",
        "Create wireframes and low-fidelity mockups",
        "Develop high-fidelity visual designs",
        "Prepare prototypes for user testing",
        "Finalize design assets and specifications"
    ],
    
    "data-science": [
        "Define the problem statement and analysis objectives",
        "Collect and prepare the dataset for analysis",
        "Perform exploratory data analysis to understand patterns",
        "Engineer features and preprocess data for modeling",
        "Train and evaluate machine learning models",
        "Deploy the model and create a system for predictions"
    ],
    
    "default": [
        "Research the topic and gather relevant information",
        "Analyze the key components and requirements",
        "Develop an initial solution or approach",
        "Test and validate the solution",
        "Refine and optimize based on testing results",
        "Prepare final documentation and delivery"
    ]
}


def get_fallback_plan(request_category: str, domain_info: Dict[str, Any] = None) -> List[str]:
    """
    Get a fallback plan based on the request category and domain info.
    
    Args:
        request_category: The category of the request
        domain_info: Optional domain specialization information
        
    Returns:
        A list of fallback subtasks
    """
    # If we have domain info, and it has a preferred category, use that
    if domain_info and "preferred_category" in domain_info:
        preferred_category = domain_info["preferred_category"]
        if preferred_category in FALLBACK_PLANS:
            return FALLBACK_PLANS[preferred_category]
    
    # Otherwise use the detected category or fall back to default
    if request_category in FALLBACK_PLANS:
        return FALLBACK_PLANS[request_category]
    else:
        return FALLBACK_PLANS["default"]