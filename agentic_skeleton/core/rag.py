"""
RAG Mock Module
==============

Implements a mock retrieval-augmented generation (RAG) system that looks up
relevant information based on keywords extracted from user prompts.
"""

import logging
from typing import List, Dict, Any

# Import mock database with fallback for error handling
try:
    from agentic_skeleton.config.settings import MOCK_RAG_DB
except ImportError:
    logging.error("Could not import MOCK_RAG_DB from settings. Ensure settings.py is accessible.")
    MOCK_RAG_DB: Dict[str, Dict[str, Any]] = {}

logger = logging.getLogger(__name__)

# Container class for RAG results
class RagResult:
    """Stores categorized information retrieved from the RAG database."""
    
    def __init__(self):
        self.context: List[str] = []
        self.offers: List[str] = []
        self.tips: List[str] = []
        self.related_docs: List[str] = []

    def is_empty(self) -> bool:
        """Check if all result categories are empty."""
        return not (self.context or self.offers or self.tips or self.related_docs)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, joining context into a single string."""
        return {
            "context": "\n".join(self.context),  # Join contexts for prompt injection
            "offers": self.offers,
            "tips": self.tips,
            "related_docs": self.related_docs
        }


def lookup(keywords: List[str]) -> Dict[str, Any]:
    """
    Looks up keywords in the mock RAG database and returns structured information,
    adjusting the number of offers, tips, and docs based on the number of matched topics.
    
    Logic:
    - 1 matched topic: Return all offers, tips, and docs for that topic.
    - 2 matched topics: Return the first 2 offers, tips, and docs for EACH topic.
    - 3+ matched topics: Return the first 1 offer, tip, and doc for EACH topic.
    
    Args:
        keywords: A list of keywords extracted from the user prompt.

    Returns:
        Dictionary with structured RAG results.
    """
    # Initialize the final result container
    rag_result = RagResult()

    # Early returns for edge cases
    if not MOCK_RAG_DB:
        logger.warning("Mock RAG database is empty or couldn't be loaded.")
        return rag_result.to_dict()

    if not keywords:
        logger.debug("No keywords provided for RAG lookup.")
        return rag_result.to_dict()

    # Normalize keywords for consistent matching
    processed_keywords = {kw.lower().strip() for kw in keywords if kw}
    logger.debug(f"Performing RAG lookup for keywords: {processed_keywords}")

    # Store data for matched topics temporarily
    matched_topic_data: Dict[str, Dict[str, Any]] = {}

    # Search for matches across all topics in the database
    for topic, data in MOCK_RAG_DB.items():
        if topic in matched_topic_data: # Should not happen with dict keys, but safe check
            continue
            
        # Get topic keywords and normalize them
        db_keywords = {kw.lower().strip() for kw in data.get("keywords", [])}
        
        # Check for any intersection between input keywords and topic keywords
        if processed_keywords.intersection(db_keywords):
            logger.info(f"RAG match found for topic '{topic}' based on keywords: {processed_keywords.intersection(db_keywords)}")
            matched_topic_data[topic] = data # Store the data for this matched topic

    # --- NEW LOGIC: Determine limit and collect results based on number of matched topics ---
    num_matched = len(matched_topic_data)
    logger.debug(f"Number of matched topics: {num_matched}")

    limit_per_topic: int | None = None # None means no limit (take all)
    if num_matched == 2:
        limit_per_topic = 2
        logger.debug(f"Applying limit: First {limit_per_topic} items per category per topic.")
    elif num_matched >= 3:
        limit_per_topic = 1
        logger.debug(f"Applying limit: First {limit_per_topic} item per category per topic.")
    else:
        limit_per_topic = None
        logger.debug("No limit applied: All items from the matched topic will be returned.")

    # Collect results from matched topics, applying the limit
    for topic, data in matched_topic_data.items():
        if data.get("context"):
            rag_result.context.append(str(data["context"])) # Context is always added fully
        
        # Apply slicing limit ([:None] takes all items)
        rag_result.offers.extend([str(o) for o in data.get("offers", [])[:limit_per_topic]])
        rag_result.tips.extend([str(t) for t in data.get("tips", [])[:limit_per_topic]])
        rag_result.related_docs.extend([str(d) for d in data.get("related_docs", [])[:limit_per_topic]])

    # Log if nothing was found or if the result is empty after processing
    if rag_result.is_empty():
        if num_matched == 0:
            logger.debug("No matching information found in mock RAG database.")
        else:
            logger.debug("Result is empty after processing matched topics (potentially due to empty categories in matched topics).")

    # Convert to dictionary for return
    result_dict = rag_result.to_dict()
    logger.debug(f"RAG lookup complete. Returning {len(result_dict.get('context', '').splitlines()) if result_dict.get('context') else 0} context line(s), {len(result_dict.get('offers', []))} offer(s), {len(result_dict.get('tips', []))} tip(s), and {len(result_dict.get('related_docs', []))} document(s) after applying limits.")
    
    return result_dict


# Direct module execution for testing
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    # Import the expanded DB if running directly
    try:
        from agentic_skeleton.config.mock_rag_data import MOCK_RAG_DB
    except ImportError:
        print("Could not import expanded MOCK_RAG_DB for testing. Using fallback.")
        # Define a minimal fallback DB for the test to run
        MOCK_RAG_DB = {
            "topic1": {
                "keywords": ["one", "alpha"],
                "context": "Context for topic one.",
                "offers": ["Offer 1a", "Offer 1b", "Offer 1c"],
                "tips": ["Tip 1a", "Tip 1b"],
                "related_docs": ["Doc 1a"]
            },
            "topic2": {
                "keywords": ["two", "beta"],
                "context": "Context for topic two.",
                "offers": ["Offer 2a", "Offer 2b"],
                "tips": ["Tip 2a", "Tip 2b", "Tip 2c"],
                "related_docs": ["Doc 2a", "Doc 2b"]
            },
            "topic3": {
                "keywords": ["three", "gamma"],
                "context": "Context for topic three.",
                "offers": ["Offer 3a"],
                "tips": ["Tip 3a"],
                "related_docs": ["Doc 3a", "Doc 3b", "Doc 3c"]
            },
             "topic4": {
                "keywords": ["four", "delta"],
                "context": "Context for topic four.",
                "offers": ["Offer 4a", "Offer 4b"],
                "tips": ["Tip 4a"],
                "related_docs": ["Doc 4a", "Doc 4b"]
            }
        }


    # Test cases to demonstrate the new logic
    test_cases = [
        (["one"], "1 Match: Expect all from topic1"),                            # 1 match
        (["one", "beta"], "2 Matches: Expect first 2 from topic1 & topic2"),      # 2 matches
        (["alpha", "two", "gamma"], "3 Matches: Expect first 1 from t1, t2, t3"), # 3 matches
        (["one", "two", "three", "four"], "4 Matches: Expect first 1 from t1, t2, t3, t4"), # 4 matches
        (["blockchain"], "0 Matches: Expect empty result")                     # No match
    ]
    
    import json
    for keywords, description in test_cases:
        print(f"\n--- Test Case: {description} (Keywords: {keywords}) ---")
        result = lookup(keywords)
        print(json.dumps(result, indent=2))
