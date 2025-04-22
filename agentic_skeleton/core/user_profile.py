"""
User Profile Utilities
=====================

Handles retrieving user skill levels from mock profiles.
"""

import logging
from typing import Dict, Any

# Import settings with fallback for error handling
try:
    from agentic_skeleton.config.settings import MOCK_USER_PROFILES, SKILL_LEVELS
except ImportError:
    logging.error("Could not import MOCK_USER_PROFILES or SKILL_LEVELS from settings. Ensure settings.py is accessible.")
    # Provide fallback defaults
    MOCK_USER_PROFILES: Dict[str, Dict[str, Any]] = {}
    SKILL_LEVELS = ('BEGINNER',) # Ensure BEGINNER is always available as default

logger = logging.getLogger(__name__)

# Define the default skill level
DEFAULT_SKILL_LEVEL = 'BEGINNER'

def get_user_skill_level(user_id: str) -> str:
    """
    Retrieves the skill level for a given user ID from the mock user profiles.

    Args:
        user_id: The unique identifier for the user.

    Returns:
        The user's skill level string (e.g., 'INTERMEDIATE', 'BEGINNER').
        Defaults to 'BEGINNER' if the user ID is not found, has no skill level
        specified, or the specified skill level is invalid.
    """
    if not user_id:
        logger.warning("No user ID provided. Defaulting to BEGINNER skill level.")
        return DEFAULT_SKILL_LEVEL

    user_profile = MOCK_USER_PROFILES.get(user_id)

    if not user_profile:
        logger.warning(f"User ID '{user_id}' not found in mock profiles. Defaulting to BEGINNER skill level.")
        return DEFAULT_SKILL_LEVEL

    skill_level = user_profile.get('skill_level')

    if not skill_level:
        logger.info(f"Skill level not specified for user ID '{user_id}'. Defaulting to BEGINNER.")
        return DEFAULT_SKILL_LEVEL

    # Validate the skill level against the defined list
    normalized_skill = str(skill_level).upper().strip()
    if normalized_skill not in SKILL_LEVELS:
        logger.warning(f"Invalid skill level '{skill_level}' found for user ID '{user_id}'. Defaulting to BEGINNER.")
        return DEFAULT_SKILL_LEVEL

    logger.debug(f"Retrieved skill level '{normalized_skill}' for user ID '{user_id}'.")
    return normalized_skill

# Example Usage (only used when running this file directly)
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    
    # Test with different user profiles
    test_users = ["user001", "user002", "user003", "user004", "user005", "user999", ""]
    for user in test_users:
        skill = get_user_skill_level(user)
        print(f"User: '{user if user else 'N/A'}' -> Skill Level: {skill}")
