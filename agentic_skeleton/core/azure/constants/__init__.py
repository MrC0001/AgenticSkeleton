"""
Azure Constants
======================

Provides access to constants used in Azure integration.
"""

from typing import Dict, List, Any

from agentic_skeleton.core.azure.constants.fallback_plans import get_fallback_plan, FALLBACK_PLANS

# Export the constants and functions
__all__ = ['get_fallback_plan', 'FALLBACK_PLANS']