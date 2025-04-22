"""
Mock Constants
======================

Provides access to constants used in mock implementation.
"""

from typing import Dict, List, Any

from agentic_skeleton.core.mock.constants.domain_knowledge import DOMAIN_KNOWLEDGE
from agentic_skeleton.core.mock.constants.mock_plans import MOCK_PLANS
from agentic_skeleton.core.mock.constants.mock_responses import MOCK_RESPONSES
from agentic_skeleton.core.mock.constants.request_classification import REQUEST_CLASSIFIERS, COMPLEX_TASK_INDICATORS, GENERIC_SUBTASK_PATTERNS

# Export the constants
__all__ = [
    'DOMAIN_KNOWLEDGE',
    'MOCK_PLANS',
    'MOCK_RESPONSES',
    'REQUEST_CLASSIFIERS',
    'COMPLEX_TASK_INDICATORS',
    'GENERIC_SUBTASK_PATTERNS'
]