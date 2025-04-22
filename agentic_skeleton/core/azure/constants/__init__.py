"""
Azure Constants
======================

Provides access to constants used in Azure integration.
"""

from typing import Dict, List, Any

from agentic_skeleton.core.azure.constants.fallback_plans import get_fallback_plan, FALLBACK_PLANS
from agentic_skeleton.core.azure.constants.domain_knowledge import DOMAIN_KNOWLEDGE
from agentic_skeleton.core.azure.constants.prompt_guidance import TASK_GUIDANCE, SUBTASK_GUIDANCE, STAGE_GUIDANCE
from agentic_skeleton.core.azure.constants.request_classification import REQUEST_CLASSIFIERS, COMPLEX_TASK_INDICATORS, GENERIC_SUBTASK_PATTERNS

# Export the constants and functions
__all__ = [
    'get_fallback_plan', 
    'FALLBACK_PLANS', 
    'DOMAIN_KNOWLEDGE',
    'TASK_GUIDANCE',
    'SUBTASK_GUIDANCE',
    'STAGE_GUIDANCE',
    'REQUEST_CLASSIFIERS',
    'COMPLEX_TASK_INDICATORS',
    'GENERIC_SUBTASK_PATTERNS'
]