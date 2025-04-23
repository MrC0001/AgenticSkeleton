"""
RAG Mock Module
==============

Implements a mock retrieval-augmented generation (RAG) system that looks up
relevant information based on keywords extracted from user prompts.

This module provides:
1. A validated RAG database loaded from mock data
2. A lookup function to match keywords to topics
3. Logic to aggregate context, tips, offers, and related documents
"""

import logging
from typing import List, Dict
# Use the mock data directly for simplicity in this example
# In a real scenario, this might connect to a vector DB or other service
from ..config.mock_rag_data import MOCK_RAG_DB
from .models import RagEntry, RagResult  # Import Pydantic models

logger = logging.getLogger(__name__)

# Load and validate mock data using Pydantic models
VALIDATED_RAG_DB: Dict[str, RagEntry] = {}
for topic, data in MOCK_RAG_DB.items():
    try:
        VALIDATED_RAG_DB[topic] = RagEntry(**data)
    except Exception as e:
        logger.error(f"Failed to validate RAG data for topic '{topic}': {e}")
        continue

logger.info(f"Validated and loaded {len(VALIDATED_RAG_DB)} RAG entries.")


def lookup(keywords: List[str]) -> RagResult:
    """
    Looks up relevant information in the RAG database based on keywords.
    
    Performs case-insensitive matching of keywords against topic keywords.
    When a match is found, the topic's context, tips, offers, and related
    documents are collected. Multiple matches are aggregated into a
    comprehensive result.

    Args:
        keywords: A list of keywords extracted from the user prompt.

    Returns:
        A RagResult object containing:
        - Aggregated context and tips for prompt enrichment
        - Offers organized by matched topic
        - Related documents organized by matched topic
        - List of matched topics
    """
    matched_topics_set = set()
    rag_context_parts = []
    rag_tips_parts = []
    offers_by_topic: Dict[str, List[str]] = {}
    docs_by_topic: Dict[str, List[str]] = {}

    # Skip processing if no keywords provided
    if not keywords:
        logger.info("No keywords provided for RAG lookup")
        return RagResult(
            rag_context="No specific context found.",
            offers_by_topic={},
            docs_by_topic={},
            matched_topics=[]
        )

    # Simple keyword matching algorithm (case-insensitive)
    for keyword in keywords:
        kw_lower = keyword.lower()
        for topic, entry in VALIDATED_RAG_DB.items():
            # Check if keyword matches any of the topic's keywords
            if any(kw_lower in rag_kw.lower() for rag_kw in entry.keywords):
                # Only process each topic once, even if multiple keywords match
                if topic not in matched_topics_set:
                    matched_topics_set.add(topic)
                    logger.info(f"RAG match found for keyword '{keyword}' on topic: {topic}")
                    
                    # Gather context information
                    if entry.context:
                        rag_context_parts.append(f"Topic: {topic}\nContext: {entry.context}")
                    
                    # Gather tips with proper formatting
                    if entry.tips:
                        rag_tips_parts.extend([f"- {tip}" for tip in entry.tips])
                    
                    # Store offers and docs associated with this specific topic
                    if entry.offers:
                        offers_by_topic[topic] = [f"- {offer}" for offer in entry.offers]
                    if entry.related_docs:
                        docs_by_topic[topic] = [f"- {doc}" for doc in entry.related_docs]

    # Combine context and tips with proper formatting and organization
    combined_context = "\n\n".join(rag_context_parts) if rag_context_parts else "No specific context found."
    if rag_tips_parts:
        combined_context += "\n\nRelevant Tips for Context:\n" + "\n".join(rag_tips_parts)

    # Convert set to list for the result
    matched_topics_list = list(matched_topics_set)

    # Create the result object using our Pydantic model
    result = RagResult(
        rag_context=combined_context,
        offers_by_topic=offers_by_topic,
        docs_by_topic=docs_by_topic,
        matched_topics=matched_topics_list
    )

    logger.debug(f"RAG Lookup Result: Matched Topics={result.matched_topics}, Context Length={len(result.rag_context)}")
    return result


# Example usage (for testing purposes)
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    test_keywords = ["mortgage", "first time buyer", "advice"]
    rag_info = lookup(test_keywords)
    print("--- RAG Lookup Example ---")
    print(f"Matched Topics: {rag_info.matched_topics}")
    print("\n--- Context for Prompt Enrichment ---")
    print(rag_info.rag_context)
    print("\n--- Offers by Topic ---")
    print(rag_info.offers_by_topic)
    print("\n--- Docs by Topic ---")
    print(rag_info.docs_by_topic)
    print("-------------------------")

    test_keywords_2 = ["internal job", "career"]
    rag_info_2 = lookup(test_keywords_2)
    print("\n--- RAG Lookup Example 2 ---")
    print(f"Matched Topics: {rag_info_2.matched_topics}")
    print("\n--- Context for Prompt Enrichment ---")
    print(rag_info_2.rag_context)
    print("\n--- Offers by Topic ---")
    print(rag_info_2.offers_by_topic)
    print("\n--- Docs by Topic ---")
    print(rag_info_2.docs_by_topic)
    print("-------------------------")
