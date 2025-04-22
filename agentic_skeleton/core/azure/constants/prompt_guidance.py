"""
Azure Prompt Guidance
======================

Contains guidance templates for different task categories and subtask types.
Used by the prompt enhancer to provide context-specific guidance.
"""

from typing import Dict

# Task category guidance for different request types
TASK_GUIDANCE = {
    "write": "Focus on creating high-quality written content with attention to structure, audience engagement, and clarity.",
    "analyze": "Emphasize data-driven insights, critical evaluation, and actionable recommendations.",
    "develop": "Prioritize technical implementation details, architecture, best practices, and code organization.",
    "design": "Concentrate on user experience, interface design principles, accessibility, and visual coherence.",
    "data-science": "Focus on data processing, model development, validation, and deployment considerations."
}

# Subtask guidance for different subtask types
SUBTASK_GUIDANCE = {
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

# Stage awareness guidance for different task stages
STAGE_GUIDANCE = {
    "research": "This is a research subtask. Be thorough and prioritize breadth and depth of information gathering.",
    "creation": "This is a creation subtask. Focus on generating high-quality, original content.",
    "refinement": "This is a refinement subtask. Focus on enhancing quality, efficiency, and effectiveness."
}