"""
Prompt Engineering Module
========================

Handles:
1. Keyword extraction from user prompts
2. Skill-based parameter retrieval
3. Structured prompt formatting according to the Persona-Query-Restrictions pattern
"""

import logging
import re
from typing import List, Dict, Any, Tuple, Optional

# Import settings with fallback for error handling
try:
    from agentic_skeleton.config.settings import SKILL_PARAMS, SKILL_LEVELS, DEFAULT_PERSONA, RESTRICTIONS_TEMPLATE
except ImportError:
    logging.error("Could not import settings from agentic_skeleton.config.settings. Ensure settings.py is accessible.")
    # Provide fallback defaults to prevent crashes
    SKILL_LEVELS = ('BEGINNER',)
    SKILL_PARAMS = {'BEGINNER': {'system_prompt_addon': '', 'temperature': 0.7, 'max_tokens': 500}}
    DEFAULT_PERSONA = "You are a helpful assistant."
    RESTRICTIONS_TEMPLATE = "Restrictions: None."

logger = logging.getLogger(__name__)


def extract_keywords_simple(text: str, num_keywords: int = 5) -> List[str]:
    """
    Extracts keywords from user prompt text using a simple rule-based approach.
    
    The function:
    1. Splits text on word boundaries
    2. Filters out common stop words and short terms
    3. Returns unique keywords up to the specified limit
    
    Args:
        text: The input text (user prompt)
        num_keywords: Maximum number of keywords to return
        
    Returns:
        List of extracted keywords (lowercase)
    """
    if not text:
        return []

    # Split by word boundaries and lowercase everything
    words = re.findall(r'\b\w+\b', text.lower())
    
    # Basic stop words to filter out common terms
    stop_words = set([
        "a", "an", "the", "is", "are", "in", "on", "it", 
        "and", "or", "for", "to", "of", "how", "what", 
        "why", "tell", "me", "about"
    ])
    
    # Filter out stop words and short words
    keywords = [word for word in words if word not in stop_words and len(word) > 2]

    # Get unique keywords while maintaining original order
    unique_keywords = list(dict.fromkeys(keywords))
    
    logger.debug(f"Extracted keywords: {unique_keywords[:num_keywords]}")
    return unique_keywords[:num_keywords]


def get_skill_based_params(skill_level: str) -> Dict[str, Any]:
    """
    Retrieves parameters tailored to a specific user skill level.
    
    Parameters include:
    - system_prompt_addon: Guidance text based on skill level
    - temperature: Controls randomness of LLM outputs (lower=more deterministic)
    - max_tokens: Maximum length of generated response
    
    Args:
        skill_level: User's skill level (e.g., 'BEGINNER', 'EXPERT')
        
    Returns:
        Dictionary of parameters for the specified skill level, 
        or BEGINNER parameters if skill level is invalid
    """
    # Normalize skill level input for consistent matching
    normalized_skill = skill_level.upper().strip()

    # Validate against known skill levels
    if normalized_skill not in SKILL_LEVELS:
        logger.warning(f"Invalid skill level provided: '{skill_level}'. Defaulting to BEGINNER parameters.")
        normalized_skill = 'BEGINNER'  # Fallback to beginner

    # Get parameters for this skill level
    params = SKILL_PARAMS.get(normalized_skill, SKILL_PARAMS['BEGINNER'])
    logger.debug(f"Retrieved parameters for skill level '{normalized_skill}': {params}")
    
    # Return a copy to prevent modification of original settings
    return params.copy()


def format_prompt_pqr(
    original_prompt: str,
    skill_system_addon: str,
    rag_context: Optional[str] = None,
    persona: Optional[str] = None,
    restrictions: Optional[str] = None,
    topic: Optional[str] = None
) -> Tuple[str, str]:
    """
    Formats prompts using the Persona-Query-Restrictions pattern with RAG context.
    
    The function constructs:
    1. System prompt with persona, skill guidance, relevant context, and restrictions
    2. User prompt containing the original query
    
    Args:
        original_prompt: Raw query from the user
        skill_system_addon: Skill-specific guidance text
        rag_context: Contextual information from RAG lookup
        persona: LLM persona text (defaults to settings.DEFAULT_PERSONA)
        restrictions: Guardrails for LLM (defaults to settings.RESTRICTIONS_TEMPLATE)
        topic: Topic to replace [topic] placeholder in restrictions
        
    Returns:
        Tuple containing (system_prompt, user_prompt)
    """
    # Use defaults if not provided
    final_persona = persona if persona else DEFAULT_PERSONA
    final_restrictions = restrictions if restrictions else RESTRICTIONS_TEMPLATE

    # Fill topic placeholder in restrictions if provided
    if topic and '[topic]' in final_restrictions:
        final_restrictions = final_restrictions.replace('[topic]', topic)
        logger.debug(f"Filled '[topic]' placeholder in restrictions with: {topic}")

    # Build system prompt in sections
    system_prompt_parts = [final_persona]

    # Add skill guidance if provided
    if skill_system_addon:
        system_prompt_parts.append(f"\n--- Skill Level Guidance ---\n{skill_system_addon}")

    # Add RAG context if provided
    if rag_context:
        system_prompt_parts.append(f"\n--- Relevant Context ---\n{rag_context}")
        system_prompt_parts.append("\nUse the context above to inform your response, particularly regarding internal services and ambassadorship opportunities.")

    # Always include restrictions
    system_prompt_parts.append(f"\n--- {final_restrictions}")

    # Join all parts into final system prompt
    system_prompt = "\n".join(system_prompt_parts).strip()

    # User prompt is simply the original query
    user_prompt = original_prompt.strip()

    logger.debug(f"Formatted System Prompt:\n{system_prompt}")
    logger.debug(f"Formatted User Prompt: {user_prompt}")

    return system_prompt, user_prompt


# Module testing (only executed when running directly)
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    # Sample test data
    test_prompt = "Tell me about the new mortgage product and how I can grow my career here."
    test_skill = 'intermediate'
    test_topic = "mortgage product"

    # Test keyword extraction
    print("--- Testing Keyword Extraction ---")
    keywords = extract_keywords_simple(test_prompt)
    print(f"Keywords: {keywords}")

    # Test skill parameter retrieval
    print("\n--- Testing Skill Parameters ---")
    skill_params = get_skill_based_params(test_skill)
    print(f"Parameters for '{test_skill}': {skill_params}")
    invalid_skill_params = get_skill_based_params('NONEXISTENT')
    print(f"Parameters for invalid skill: {invalid_skill_params}")

    # Test prompt formatting with RAG context
    print("\n--- Testing Prompt Formatting (with RAG) ---")
    mock_rag = "The 'FlexiHome' mortgage is new. The Internal Mobility Program helps with career growth."
    system_p, user_p = format_prompt_pqr(
        original_prompt=test_prompt,
        skill_system_addon=skill_params.get('system_prompt_addon', ''),
        rag_context=mock_rag,
        topic=test_topic
    )
    print(f"\nSystem Prompt:\n{system_p}")
    print(f"\nUser Prompt: {user_p}")

    # Test prompt formatting without RAG context
    print("\n--- Testing Formatting (No RAG) ---")
    system_p_no_rag, user_p_no_rag = format_prompt_pqr(
        original_prompt="What are the business banking options?",
        skill_system_addon=get_skill_based_params('BEGINNER').get('system_prompt_addon', ''),
        rag_context=None,
        topic="business banking"
    )
    print(f"\nSystem Prompt:\n{system_p_no_rag}")
    print(f"\nUser Prompt: {user_p_no_rag}")
