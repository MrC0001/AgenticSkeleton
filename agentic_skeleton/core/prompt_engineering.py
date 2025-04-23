"""
Prompt Engineering Module
========================

This module is responsible for the intelligent handling of user prompts:

1. Keyword extraction from user prompts for RAG lookup
2. Skill-based parameter retrieval to adapt responses to user expertise
3. Structured prompt formatting according to the Persona-Query-Restrictions pattern
   to ensure consistent, high-quality responses from the LLM

The PQR pattern structures prompts with:
- Persona: The role/style the LLM should adopt
- Query: The actual user question/request
- Restrictions: Guidelines to control the response format/content
"""

import logging
from typing import List, Dict, Tuple, Optional
import re

try:
    from ..config import settings
except ImportError:
    logging.error("Could not import settings. Ensure settings.py is accessible.")
    # Provide fallback defaults to prevent crashes
    settings = type('obj', (object,), {
        'SKILL_LEVELS': ('BEGINNER',),
        'SKILL_PARAMS': {'BEGINNER': {'skill_level_addon': '', 'temperature': 0.7, 'max_tokens': 500}},
        'DEFAULT_PERSONA': "You are a helpful assistant.",
        'RESTRICTIONS_TEMPLATE': "Restrictions: None.",
        'NUM_KEYWORDS': 5  # Add fallback
    })()

from .models import RagResult  # Import RagResult model

logger = logging.getLogger(__name__)


def extract_keywords_simple(text: str, num_keywords: int = 5) -> List[str]:
    """
    Extracts simple keywords from text using basic NLP techniques.
    
    This function performs:
    1. Text cleaning (punctuation removal, lowercase conversion)
    2. Word splitting
    3. Stop word filtering
    4. Short word removal
    5. Selection of top N keywords
    
    Note: This is a basic implementation. For production, consider more robust
    NLP techniques like TF-IDF, entity extraction, or embedding-based keyword extraction.

    Args:
        text: The input text to extract keywords from.
        num_keywords: The maximum number of keywords to return.

    Returns:
        A list of potential keywords, limited to num_keywords.
    """
    # Handle empty input
    if not text:
        logger.debug("Empty text provided for keyword extraction")
        return []
        
    # First clean the input text - remove punctuation and normalize
    cleaned_text = re.sub(r'[^\w\s]', ' ', text.lower())
    
    # Split into words
    words = cleaned_text.split()
    
    # Common English stop words to filter out (short list for simplicity)
    stop_words = {'a', 'an', 'the', 'and', 'or', 'but', 'is', 'are', 'was', 
                 'were', 'be', 'been', 'being', 'in', 'on', 'at', 'to', 'for',
                 'with', 'about', 'me', 'my', 'i', 'it', 'its', 'of', 'that', 'this'}
    
    # Filter out stop words and short words
    filtered_words = [word for word in words if word not in stop_words and len(word) > 2]
    
    # Take the top N keywords
    keywords = filtered_words[:num_keywords]
    
    logger.debug(f"Extracted keywords from '{text[:30]}...': {keywords}")
    return keywords


def get_skill_based_params(skill_level: str) -> Dict:
    """
    Retrieves LLM parameters and system prompt additions based on user skill level.
    
    This function ensures the LLM response is tailored to the user's expertise level by:
    1. Adjusting the temperature (creativity vs. precision)
    2. Setting appropriate token limits
    3. Adding skill-specific guidance to the system prompt
    
    The skill levels are configured in settings.SKILL_LEVELS with corresponding
    parameters in settings.SKILL_PARAMS.

    Args:
        skill_level: The user's skill level string (e.g., 'BEGINNER', 'INTERMEDIATE', 'EXPERT').

    Returns:
        A dictionary containing parameters like:
        - 'temperature': Controls randomness (lower = more deterministic)
        - 'max_tokens': Controls response length 
        - 'skill_level_addon': Text to add to system prompt
        
        Returns BEGINNER defaults if skill level is unknown.
    """
    # Clean and normalize the skill level
    cleaned_skill_level = skill_level.strip().upper() if skill_level else ''
    
    # Check if the cleaned skill level is in our valid levels
    if cleaned_skill_level in settings.SKILL_LEVELS:
        logger.info(f"Found skill parameters for level: {cleaned_skill_level}")
        # Return a copy to prevent accidental modification of the original
        return settings.SKILL_PARAMS.get(cleaned_skill_level, {}).copy()
    else:
        logger.warning(f"Skill level '{skill_level}' not recognized. Using default BEGINNER parameters.")
        # Fallback to BEGINNER
        return settings.SKILL_PARAMS.get('BEGINNER', {}).copy()


def format_prompt_pqr(
    user_prompt: str,
    skill_level_addon: str,
    rag_result: RagResult,
    persona: str = None,
    restrictions_template: str = None
) -> Tuple[str, str]:
    """
    Formats the system and user prompts using the Persona-Query-Restrictions (PQR) pattern.
    
    The PQR pattern helps structure prompts consistently for better LLM responses by:
    1. Defining a clear persona for the LLM to adopt
    2. Preserving the original user query
    3. Setting explicit restrictions to guide the response format/content
    4. Incorporating relevant context from RAG and skill-level adaptations
    
    Args:
        user_prompt: The original query from the user.
        skill_level_addon: Text to add to the system prompt based on skill level.
        rag_result: The RagResult object containing context and matched topics.
        persona: The persona the LLM should adopt. Uses settings.DEFAULT_PERSONA if None.
        restrictions_template: Guidelines for response. Uses settings.RESTRICTIONS_TEMPLATE if None.

    Returns:
        A tuple containing:
        - system_prompt: The formatted system prompt with persona, context, and restrictions
        - user_prompt: The original user query (unchanged)
    """
    # Use default values from settings if not provided
    persona = persona or settings.DEFAULT_PERSONA
    restrictions_template = restrictions_template or settings.RESTRICTIONS_TEMPLATE
    
    # Determine the primary topic for restrictions
    # If RAG found matching topics, use the first one, otherwise use a default
    primary_topic = rag_result.matched_topics[0] if rag_result.matched_topics else "general banking"
    logger.debug(f"Using primary topic '{primary_topic}' for restrictions template.")

    # Fill placeholders in the restrictions template
    formatted_restrictions = restrictions_template.replace("[topic]", primary_topic)

    # Build system prompt in sections
    system_prompt_parts = [persona]
    
    # Add skill level guidance section if provided
    if skill_level_addon:
        system_prompt_parts.extend([
            "\n--- Skill Level Guidance ---",
            skill_level_addon
        ])
    
    # Add RAG context section if available
    if rag_result.rag_context and rag_result.rag_context != "No specific context found.":
        system_prompt_parts.extend([
            "\n--- Relevant Context ---",
            rag_result.rag_context,
            "Use the context above to inform your response."
        ])
    
    # Add restrictions section
    system_prompt_parts.extend([
        "\n--- Restrictions ---",
        formatted_restrictions
    ])
    
    # Combine all parts, filtering out any empty strings
    system_prompt = "\n".join(filter(None, system_prompt_parts))

    # The user prompt remains the original user query
    final_user_prompt = user_prompt

    logger.debug(f"Formatted System Prompt (length: {len(system_prompt)})")
    logger.debug(f"Formatted User Prompt (length: {len(final_user_prompt)})")

    return system_prompt, final_user_prompt


# Module testing (only executed when running directly)
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    # Sample test data
    test_prompt = "Tell me about the new mortgage product and how I can grow my career here."
    test_skill = 'intermediate'

    # Test keyword extraction
    print("--- Testing Keyword Extraction ---")
    keywords = extract_keywords_simple(test_prompt, num_keywords=settings.NUM_KEYWORDS)
    print(f"Keywords: {keywords}")

    # Test skill parameter retrieval
    print("\n--- Testing Skill Parameters ---")
    skill_params = get_skill_based_params(test_skill)
    print(f"Parameters for '{test_skill}': {skill_params}")
    invalid_skill_params = get_skill_based_params('NONEXISTENT')
    print(f"Parameters for invalid skill: {invalid_skill_params}")

    # Test prompt formatting with RAG context
    print("\n--- Testing Prompt Formatting (with RAG) ---")
    mock_rag = RagResult(
        rag_context="Topic: new_mortgage_product\nContext: The 'FlexiHome' mortgage offers flexible rate options and a digital application.\n\nTopic: internal_mobility_program\nContext: Our Internal Mobility Program facilitates career progression within the bank.\n\nRelevant Tips for Context:\n- Familiarize yourself with the eligibility criteria.\n- Highlight the quick pre-approval time when discussing with clients/colleagues.\n- Use the internal calculator for estimations.\n- Update your internal profile regularly.\n- Network with managers in departments you're interested in.\n- Use the 'Job Alert' feature on the internal portal.",
        offers_by_topic={
            "new_mortgage_product": ["- Offer M1", "- Offer M2"],
            "internal_mobility_program": ["- Offer I1"]
        },
        docs_by_topic={
            "new_mortgage_product": ["- Doc M1"],
            "internal_mobility_program": ["- Doc I1", "- Doc I2"]
        },
        matched_topics=["new_mortgage_product", "internal_mobility_program"]
    )
    system_p, user_p = format_prompt_pqr(
        user_prompt=test_prompt,
        skill_level_addon=skill_params.get('skill_level_addon', ''),
        rag_result=mock_rag
    )
    print(f"\nSystem Prompt:\n{system_p}")
    print(f"\nUser Prompt: {user_p}")

    # Test prompt formatting without RAG context
    print("\n--- Testing Formatting (No RAG) ---")
    mock_rag_no_context = RagResult(
        rag_context="",
        offers_by_topic={},
        docs_by_topic={},
        matched_topics=[]
    )
    system_p_no_rag, user_p_no_rag = format_prompt_pqr(
        user_prompt="What are the business banking options?",
        skill_level_addon=get_skill_based_params('BEGINNER').get('skill_level_addon', ''),
        rag_result=mock_rag_no_context
    )
    print(f"\nSystem Prompt:\n{system_p_no_rag}")
    print(f"\nUser Prompt: {user_p_no_rag}")
