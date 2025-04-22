"""
Prompt Processor Module
======================

Main orchestrator for the prompt enhancement pipeline:
1. Gets user skill level based on user ID
2. Extracts keywords from the user prompt
3. Retrieves relevant context and extras from the RAG system
4. Formats the prompt with skill-specific parameters
5. Calls the LLM client
6. Enhances the response with RAG extras
"""

import logging
from typing import Dict, Any, List

# Core components for prompt enhancement
from . import prompt_engineering
from . import rag
from . import user_profile

# LLM Client and settings
from agentic_skeleton.core.azure import client as llm_client
from agentic_skeleton.config import settings

logger = logging.getLogger(__name__)

def process_prompt_request(user_id: str, user_prompt: str) -> str:
    """
    Orchestrates the entire prompt enhancement pipeline.
    
    Flow:
    1. Retrieves user skill level from the profile service
    2. Extracts keywords from the user's prompt
    3. Queries the RAG system with those keywords
    4. Gets skill-specific parameters and formatting
    5. Calls the LLM with the enhanced prompt
    6. Appends additional information to the LLM response
    
    Args:
        user_id: The ID of the user making the request
        user_prompt: The raw prompt text from the user
        
    Returns:
        Enhanced response string with LLM output and RAG extras
    """
    logger.info(f"Processing prompt request for user_id: '{user_id}'")
    logger.debug(f"Original user prompt: {user_prompt}")

    # STEP 1: Get user's skill level
    skill_level = user_profile.get_user_skill_level(user_id)
    logger.info(f"User '{user_id}' has skill level: {skill_level}")

    # STEP 2: Extract keywords from user prompt
    keywords = prompt_engineering.extract_keywords_simple(user_prompt, num_keywords=5)
    logger.info(f"Extracted keywords: {keywords}")

    # STEP 3: RAG Lookup - get context and enhancement extras
    rag_data = rag.lookup(keywords)
    # Split the data into context for prompt and extras for response enhancement
    rag_context = rag_data.get("context", "")
    rag_offers = rag_data.get("offers", [])
    rag_tips = rag_data.get("tips", [])
    rag_docs = rag_data.get("related_docs", [])
    
    has_context = bool(rag_context.strip())
    logger.info(f"RAG lookup: found context: {has_context}, offers: {len(rag_offers)}, " 
                f"tips: {len(rag_tips)}, docs: {len(rag_docs)}")

    # STEP 4: Get skill-based parameters and prepare prompt
    skill_params = prompt_engineering.get_skill_based_params(skill_level)
    
    # Extract system_prompt_addon and keep the rest as hyperparameters
    skill_addon = skill_params.pop('system_prompt_addon', '')
    
    # Use first keyword as topic guess for restrictions
    topic_guess = keywords[0] if keywords else "the user's query"
    
    # Format the prompt components
    system_prompt, final_user_prompt = prompt_engineering.format_prompt_pqr(
        original_prompt=user_prompt,
        skill_system_addon=skill_addon,
        rag_context=rag_context,
        topic=topic_guess
    )

    # STEP 5 & 6: Call LLM (or Mock) and Append RAG Extras
    if settings.is_using_mock():
        # MOCK MODE: Return detailed debug info instead of calling LLM
        logger.info("Mock mode enabled. Returning debug information.")
        # Construct the mock response string (similar to previous version)
        llm_response = (
            f"--- Enhanced Prompt (Mock Mode) ---\n"
            f"User ID: {user_id} ({skill_level})\n"
            f"Original Prompt: {user_prompt}\n"
            f"Keywords: {keywords}\n"
            f"RAG Context Found: {'Yes' if has_context else 'No'}\n"
            f"LLM Params Used (excluding addon): {skill_params}\n"
            f"--- System Prompt ---\n{system_prompt}\n"
            f"--- User Prompt ---\n{final_user_prompt}\n"
            f"--- End Mock LLM Response ---"
        )
    else:
        # AZURE MODE: Initialize client and call LLM
        logger.info("Azure mode enabled. Calling LLM.")
        azure_client = llm_client.initialize_client()
        if not azure_client:
            logger.error("LLM client could not be initialized.")
            return "Error: Could not process request due to LLM client initialization failure."
        
        # Call the model with system prompt, user prompt, and skill-based hyperparameters
        llm_response = azure_client.call_llm(
            model=settings.MODEL_PROMPT_ENHANCER,
            system_prompt=system_prompt,
            user_prompt=final_user_prompt,
            **skill_params  # Pass hyperparameters like temperature, max_tokens
        )
        logger.info("LLM response received")

    # STEP 6 (cont.): Append RAG extras to the LLM response (or mock response)
    final_response_parts = [llm_response]

    # Add offers if available
    if rag_offers:
        final_response_parts.append("\n\n--- Relevant Offers ---")
        final_response_parts.extend([f"- {offer}" for offer in rag_offers])

    # Add tips if available
    if rag_tips:
        final_response_parts.append("\n\n--- Tips & Tricks ---")
        final_response_parts.extend([f"- {tip}" for tip in rag_tips])

    # Add document references if available
    if rag_docs:
        final_response_parts.append("\n\n--- Related Documents/Links ---")
        final_response_parts.extend([f"- {doc}" for doc in rag_docs])

    # Combine all parts into the final response
    final_response = "\n".join(final_response_parts).strip()
    logger.debug("Final response constructed with LLM output and RAG enhancements")

    return final_response


# Direct module execution for testing
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    
    print(f"\n--- Testing Prompt Processor (Mock Mode: {settings.is_using_mock()}) ---")
    
    # Test with different user types and prompts
    test_cases = [
        ("user001", "Tell me about the new FlexiHome mortgage product.", "Intermediate User - Mortgage"),
        ("user004", "How can I promote our small business services?", "Ambassador Trainee - SMB"),
        ("user999", "What is internal mobility?", "Unknown User (Beginner) - Career")
    ]
    
    for user_id, prompt, description in test_cases:
        print(f"\n=== TEST: {description} ===")
        print(f"User: '{user_id}', Prompt: '{prompt}'")
        
        result = process_prompt_request(user_id, prompt)
        
        print("\n--- Result ---")
        # Print just the first 200 chars to keep output manageable
        preview = result[:200] + "..." if len(result) > 200 else result
        print(preview)
        print("---------------")
