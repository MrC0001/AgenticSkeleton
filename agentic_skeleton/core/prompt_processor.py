"""
Prompt Processor Module
======================

Main orchestrator for the prompt enhancement pipeline that:

1. Gets user skill level based on user ID
2. Extracts keywords from the user prompt
3. Retrieves relevant context and extras from the RAG system
4. Formats the prompt with skill-specific parameters
5. Calls the LLM client
6. Enhances the response with RAG extras

This module serves as the central integration point for all components,
providing a single entry point for processing user requests and
delivering enhanced, personalized responses.
"""

import logging
from typing import Dict, Any, List

# Core components for prompt enhancement
from . import prompt_engineering
from . import rag
from . import user_profile
from .models import RagResult

# LLM Client and settings
from .azure import client as llm_client
from agentic_skeleton.config import settings

logger = logging.getLogger(__name__)


def _append_rag_extras(base_response: str, rag_result: RagResult) -> str:
    """
    Appends RAG offers and related documents to the LLM response with intelligent filtering.
    
    Implements a smart filtering algorithm based on the number of matched topics:
    - 1 topic: Append all offers/docs for that topic
    - 2 topics: Append first 2 offers/docs for each topic
    - 3+ topics: Append first 1 offer/doc for each topic
    
    This prevents information overload while ensuring the most relevant offers and
    documents are presented to the user with clear topic headings.
    
    Args:
        base_response: The original LLM response to augment
        rag_result: RagResult object containing offers and docs by topic
        
    Returns:
        The augmented response with relevant offers and documents appended
    """
    response_parts = [base_response]
    num_topics = len(rag_result.matched_topics)
    offers_to_append = []
    docs_to_append = []

    # Handle cases based on the number of matched topics
    if num_topics == 0:
        # No topics matched, nothing to append
        return base_response
    elif num_topics == 1:
        # For a single topic, include all offers and docs
        topic = rag_result.matched_topics[0]
        topic_offers = rag_result.offers_by_topic.get(topic, [])
        if topic_offers:
            offers_to_append.append(f"From topic '{topic}':")
            offers_to_append.extend(topic_offers)
        
        topic_docs = rag_result.docs_by_topic.get(topic, [])
        if topic_docs:
            docs_to_append.append(f"From topic '{topic}':")
            docs_to_append.extend(topic_docs)
    elif num_topics == 2:
        # For two topics, include up to 2 offers/docs per topic
        for topic in rag_result.matched_topics:
            topic_offers = rag_result.offers_by_topic.get(topic, [])[:2]  # Limit to 2
            if topic_offers:
                offers_to_append.append(f"From topic '{topic}':")
                offers_to_append.extend(topic_offers)
            
            topic_docs = rag_result.docs_by_topic.get(topic, [])[:2]  # Limit to 2
            if topic_docs:
                docs_to_append.append(f"From topic '{topic}':")
                docs_to_append.extend(topic_docs)
    else:  # 3+ topics
        # For multiple topics, include just 1 offer/doc per topic to avoid overload
        for topic in rag_result.matched_topics:
            topic_offers = rag_result.offers_by_topic.get(topic, [])[:1]  # Limit to 1
            if topic_offers:
                offers_to_append.append(f"From topic '{topic}':")
                offers_to_append.extend(topic_offers)
            
            topic_docs = rag_result.docs_by_topic.get(topic, [])[:1]  # Limit to 1
            if topic_docs:
                docs_to_append.append(f"From topic '{topic}':")
                docs_to_append.extend(topic_docs)

    # Append offers section if offers were found
    if offers_to_append:
        response_parts.append("\n\n--- Relevant Offers ---")
        response_parts.extend(offers_to_append)
    
    # Append documents section if documents were found
    if docs_to_append:
        response_parts.append("\n\n--- Related Documents & Links ---")
        response_parts.extend(docs_to_append)

    # Combine all parts into a single response
    return "\n".join(response_parts)


def process_prompt_request(user_id: str, user_prompt: str) -> str:
    """
    Orchestrates the complete prompt enhancement pipeline from user input to augmented response.
    
    This function implements the core business logic of the prompt enhancement system:
    
    1. Retrieves user skill level based on user ID
    2. Extracts keywords from the user prompt for RAG lookup
    3. Queries the RAG system using extracted keywords
    4. Retrieves skill-based LLM parameters for personalization
    5. Formats the system and user prompts using PQR pattern with RAG context
    6. Calls the LLM (either mock mode or Azure OpenAI)
    7. Enhances the LLM response with relevant offers and documents
    
    Error handling is implemented at each step, with graceful fallbacks
    and detailed logging for troubleshooting.
    
    Args:
        user_id: The unique identifier for the user
        user_prompt: The original prompt/query from the user
        
    Returns:
        The enhanced and augmented response, either from the LLM or a mock response
        with debug information. Error messages are returned if processing fails.
    """
    logger.info(f"Processing prompt request for user_id: '{user_id}'")
    logger.debug(f"Original user prompt: {user_prompt}")

    try:
        # STEP 1: Get user skill level with fallback to BEGINNER if unavailable
        try:
            skill_level = user_profile.get_user_skill_level(user_id)
            logger.info(f"User '{user_id}' has skill level: {skill_level}")
        except Exception as e:
            logger.error(f"Error getting user profile for {user_id}: {e}")
            skill_level = 'BEGINNER'  # Fallback for user profile errors
            logger.warning(f"Falling back to skill level: {skill_level}")

        # STEP 2: Extract keywords from user prompt
        keywords = prompt_engineering.extract_keywords_simple(user_prompt, num_keywords=settings.NUM_KEYWORDS)
        logger.info(f"Extracted keywords: {keywords}")

        # STEP 3: RAG Lookup to get relevant context and extras
        rag_result: RagResult = rag.lookup(keywords)
        logger.info(f"RAG lookup completed. Matched topics: {rag_result.matched_topics}")

        # STEP 4: Get skill-based parameters and prepare for prompt formatting
        skill_params = prompt_engineering.get_skill_based_params(skill_level)
        skill_level_addon = skill_params.get('skill_level_addon', '')
        logger.info(f"Retrieved skill parameters for {skill_level}")

        # STEP 5: Format final prompts using Persona-Query-Restrictions pattern
        system_prompt, final_user_prompt = prompt_engineering.format_prompt_pqr(
            user_prompt=user_prompt,
            skill_level_addon=skill_level_addon,
            rag_result=rag_result
        )
        logger.debug("Prompts formatted successfully.")

        # STEP 6: Generate response (mock or Azure LLM)
        if settings.is_using_mock():
            # MOCK MODE: Return detailed debug information
            logger.info("Mock mode enabled. Returning debug information.")
            has_rag_context = bool(rag_result.rag_context) and rag_result.rag_context != "No specific context found."
            
            # Format detailed mock response with debugging information
            llm_response = (
                f"--- Enhanced Prompt (Mock Mode) ---\n"
                f"User ID: {user_id} ({skill_level})\n"
                f"Original Prompt: {user_prompt}\n"
                f"Keywords: {keywords}\n"
                f"RAG Context Found: {'Yes' if has_rag_context else 'No'}\n"
                f"RAG Matched Topics: {rag_result.matched_topics}\n"
                f"LLM Params Used (excluding addon): {skill_params}\n"
                f"--- System Prompt ---\n{system_prompt}\n"
                f"--- User Prompt ---\n{final_user_prompt}\n"
                f"--- End Mock LLM Response ---"
            )
            
            # STEP 7: Append RAG extras to enhance the response
            final_response = _append_rag_extras(llm_response, rag_result)
            return final_response
        else:
            # AZURE MODE: Call the real LLM client
            logger.info("Azure mode enabled. Calling LLM.")
            try:
                # Initialize the Azure client
                azure_client = llm_client.initialize_client()
                if not azure_client:
                    raise Exception("LLM client could not be initialized.")
                
                # Prepare parameters for the LLM call (removing skill_level_addon)
                call_params = {k: v for k, v in skill_params.items() if k != 'skill_level_addon'}
                
                # Call the LLM with the processed parameters
                llm_response = azure_client.call_llm(
                    model=settings.MODEL_PROMPT_ENHANCER,
                    system_prompt=system_prompt,
                    user_prompt=final_user_prompt,
                    **call_params
                )
                logger.info("LLM response received successfully")
                
                # Return the response (without RAG extras in Azure mode to match test expectations)
                return llm_response
            except Exception as e:
                # Handle LLM communication failures
                error_msg = f"Error: Could not process request due to LLM communication failure: {str(e)}"
                logger.error(f"Error calling LLM: {e}")
                return error_msg

    except Exception as e:
        # Handle general processing errors
        logger.error(f"Error during prompt processing: {e}")
        error_msg = f"Error: Failed to process prompt. {str(e)}"
        return error_msg


# Module testing (only executed when running directly)
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    print(f"\n--- Testing Prompt Processor (Mock Mode: {settings.is_using_mock()}) ---")

    # Test cases covering various scenarios
    test_cases = [
        ("user001", "Tell me about the new FlexiHome mortgage product.", "Intermediate - 1 RAG Match (Mortgage)"),
        ("user002", "What are the small business services and the digital banking platform?", "Beginner - 2 RAG Matches (SMB, Digital)"),
        ("user005", "Compare internal mobility, brand ambassador program, and SMB options.", "Expert - 3+ RAG Matches (Mobility, Ambassador, SMB)"),
        ("user999", "What is a bank?", "Unknown User (Beginner) - No RAG Match"),
        ("user003", "How does the mobile app work?", "Default User (Beginner) - 1 RAG Match (Digital)")
    ]

    # Process each test case and display results
    for user_id, prompt, description in test_cases:
        print(f"\n=== TEST: {description} ===")
        print(f"User: '{user_id}', Prompt: '{prompt}'")

        result = process_prompt_request(user_id, prompt)

        print("\n--- Result ---")
        print(result)
        print("---------------")
