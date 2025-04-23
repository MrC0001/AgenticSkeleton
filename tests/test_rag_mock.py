# tests/test_unit.py

import pytest

# Local Mock RAG DB for consistent testing within this file
MOCK_RAG_DB_FOR_TEST = {
    "topic1": {
        "keywords": ["one", "alpha", "test"],
        "context": "Context for topic one.",
        "offers": ["Offer 1a", "Offer 1b", "Offer 1c"],
        "tips": ["Tip 1a", "Tip 1b"],
        "related_docs": ["Doc 1a"]
    },
    "topic2": {
        "keywords": ["two", "beta", "test"],
        "context": "Context for topic two.",
        "offers": ["Offer 2a", "Offer 2b", "Offer 2c"],
        "tips": ["Tip 2a", "Tip 2b", "Tip 2c"],
        "related_docs": ["Doc 2a", "Doc 2b"]
    },
    "topic3": {
        "keywords": ["three", "gamma"],
        "context": "Context for topic three.",
        "offers": ["Offer 3a"],
        "tips": ["Tip 3a", "Tip 3b"],
        "related_docs": ["Doc 3a", "Doc 3b", "Doc 3c"]
    },
    "topic4": {
        "keywords": ["four", "delta"],
        "context": "Context for topic four.",
        "offers": ["Offer 4a", "Offer 4b"],
        "tips": ["Tip 4a"],
        "related_docs": ["Doc 4a", "Doc 4b", "Doc 4c"]
    }
}

# Import the functions to test
from agentic_skeleton.core import rag
from agentic_skeleton.core.models import RagEntry, RagResult


# --- Setup for rag tests ---

@pytest.fixture(autouse=True)
def setup_rag():
    """Fixture to inject the local mock DB before each test and restore afterwards."""
    original_db = getattr(rag, 'MOCK_RAG_DB', None)
    original_validated_db = getattr(rag, 'VALIDATED_RAG_DB', {})
    # Set the mock data
    rag.MOCK_RAG_DB = MOCK_RAG_DB_FOR_TEST
    # Validate the mock data
    rag.VALIDATED_RAG_DB = {}
    for topic, data in MOCK_RAG_DB_FOR_TEST.items():
        try:
            rag.VALIDATED_RAG_DB[topic] = RagEntry(**data)
        except Exception as e:
            print(f"Error validating mock data for topic '{topic}': {e}")
    
    yield  # Test runs here
    
    # Restore original DBs
    rag.MOCK_RAG_DB = original_db
    rag.VALIDATED_RAG_DB = original_validated_db


# --- Tests for rag.lookup using local MOCK_RAG_DB_FOR_TEST ---

def test_rag_lookup_no_keywords_provided():
    """Test RAG lookup with no keywords provided. Expect empty result."""
    print("\nTesting RAG lookup: No Keywords Provided")
    result = rag.lookup([])
    print(f"  Result: {result}")
    assert result.rag_context == "No specific context found.", "Context should be empty for no keywords"
    assert result.offers_by_topic == {}, "Offers should be empty for no keywords"
    assert result.docs_by_topic == {}, "Docs should be empty for no keywords"
    assert result.matched_topics == [], "Matched topics should be empty for no keywords"
    print("  test_rag_lookup_no_keywords_provided PASSED")


def test_rag_lookup_no_match_found():
    """Test RAG lookup when no keywords match any topic."""
    print("\nTesting RAG lookup: No Match Found")
    keywords = ["nonexistent", "keyword"]
    result = rag.lookup(keywords)
    print(f"  Input Keywords: {keywords}")
    print(f"  Result: {result}")
    assert result.rag_context == "No specific context found.", "Context should be empty for no match"
    assert result.offers_by_topic == {}, "Offers should be empty for no match"
    assert result.docs_by_topic == {}, "Docs should be empty for no match"
    assert result.matched_topics == [], "Matched topics should be empty for no match"
    print("  test_rag_lookup_no_match_found PASSED")


def test_rag_lookup_one_match_found():
    """Test RAG lookup when keywords match exactly one topic (expect all items)."""
    print("\nTesting RAG lookup: One Match Found")
    keywords = ["alpha"]  # Matches topic1
    result = rag.lookup(keywords)
    print(f"  Input Keywords: {keywords}")
    print(f"  Result: {result}")
    expected_data = rag.VALIDATED_RAG_DB["topic1"]
    
    # Check that topic1 is in the matched topics
    assert "topic1" in result.matched_topics, "topic1 should be in matched_topics"
    
    # Check that the context contains the expected content
    assert expected_data.context in result.rag_context, "Context from topic1 expected"
    
    # Check offers for topic1
    assert "topic1" in result.offers_by_topic, "topic1 should be in offers_by_topic"
    assert len(result.offers_by_topic["topic1"]) == 3, "Should have 3 offers for topic1"
    
    # Check docs for topic1
    assert "topic1" in result.docs_by_topic, "topic1 should be in docs_by_topic"
    assert len(result.docs_by_topic["topic1"]) == 1, "Should have 1 doc for topic1"
    
    print("  test_rag_lookup_one_match_found PASSED")


def test_rag_lookup_two_matches_found():
    """Test RAG lookup when keywords match two topics (expect first 2 items from each)."""
    print("\nTesting RAG lookup: Two Matches Found")
    keywords = ["test"]  # Matches topic1 and topic2
    result = rag.lookup(keywords)
    print(f"  Input Keywords: {keywords}")
    print(f"  Result: {result}")

    # Check if both contexts are present in the combined string
    assert rag.VALIDATED_RAG_DB["topic1"].context in result.rag_context, "Context from topic1 expected"
    assert rag.VALIDATED_RAG_DB["topic2"].context in result.rag_context, "Context from topic2 expected"
    
    # Check matched topics
    assert "topic1" in result.matched_topics, "topic1 should be in matched_topics"
    assert "topic2" in result.matched_topics, "topic2 should be in matched_topics"
    
    # Check offers for both topics
    assert "topic1" in result.offers_by_topic, "topic1 should be in offers_by_topic"
    assert "topic2" in result.offers_by_topic, "topic2 should be in offers_by_topic"
    assert len(result.offers_by_topic["topic1"]) == 3, "Should have 3 offers for topic1"
    assert len(result.offers_by_topic["topic2"]) == 3, "Should have 3 offers for topic2"
    
    # Check docs for both topics
    assert "topic1" in result.docs_by_topic, "topic1 should be in docs_by_topic"
    assert "topic2" in result.docs_by_topic, "topic2 should be in docs_by_topic"
    assert len(result.docs_by_topic["topic1"]) == 1, "Should have 1 doc for topic1"
    assert len(result.docs_by_topic["topic2"]) == 2, "Should have 2 docs for topic2"
    
    print("  test_rag_lookup_two_matches_found PASSED")


def test_rag_lookup_three_matches_found():
    """Test RAG lookup when keywords match three topics (expect first 1 item from each)."""
    print("\nTesting RAG lookup: Three Matches Found")
    keywords = ["one", "beta", "gamma"]  # Matches topic1, topic2, topic3
    result = rag.lookup(keywords)
    print(f"  Input Keywords: {keywords}")
    print(f"  Result: {result}")

    # Check if all three contexts are present
    assert rag.VALIDATED_RAG_DB["topic1"].context in result.rag_context, "Context from topic1 expected"
    assert rag.VALIDATED_RAG_DB["topic2"].context in result.rag_context, "Context from topic2 expected"
    assert rag.VALIDATED_RAG_DB["topic3"].context in result.rag_context, "Context from topic3 expected"
    
    # Check matched topics
    assert "topic1" in result.matched_topics, "topic1 should be in matched_topics"
    assert "topic2" in result.matched_topics, "topic2 should be in matched_topics"
    assert "topic3" in result.matched_topics, "topic3 should be in matched_topics"
    
    # Check offers for all topics
    assert "topic1" in result.offers_by_topic, "topic1 should be in offers_by_topic"
    assert "topic2" in result.offers_by_topic, "topic2 should be in offers_by_topic"
    assert "topic3" in result.offers_by_topic, "topic3 should be in offers_by_topic"
    
    # Check docs for all topics
    assert "topic1" in result.docs_by_topic, "topic1 should be in docs_by_topic"
    assert "topic2" in result.docs_by_topic, "topic2 should be in docs_by_topic"
    assert "topic3" in result.docs_by_topic, "topic3 should be in docs_by_topic"
    
    print("  test_rag_lookup_three_matches_found PASSED")


def test_rag_lookup_four_matches_found():
    """Test RAG lookup when keywords match four topics (expect first 1 item from each)."""
    print("\nTesting RAG lookup: Four Matches Found")
    keywords = ["one", "two", "three", "four"]  # Matches all topics
    result = rag.lookup(keywords)
    print(f"  Input Keywords: {keywords}")
    print(f"  Result: {result}")

    # Check if all four contexts are present
    assert rag.VALIDATED_RAG_DB["topic1"].context in result.rag_context, "Context from topic1 expected"
    assert rag.VALIDATED_RAG_DB["topic2"].context in result.rag_context, "Context from topic2 expected"
    assert rag.VALIDATED_RAG_DB["topic3"].context in result.rag_context, "Context from topic3 expected"
    assert rag.VALIDATED_RAG_DB["topic4"].context in result.rag_context, "Context from topic4 expected"
    
    # Check matched topics
    assert "topic1" in result.matched_topics, "topic1 should be in matched_topics"
    assert "topic2" in result.matched_topics, "topic2 should be in matched_topics"
    assert "topic3" in result.matched_topics, "topic3 should be in matched_topics"
    assert "topic4" in result.matched_topics, "topic4 should be in matched_topics"
    
    # Check offers for all topics
    assert "topic1" in result.offers_by_topic, "topic1 should be in offers_by_topic"
    assert "topic2" in result.offers_by_topic, "topic2 should be in offers_by_topic"
    assert "topic3" in result.offers_by_topic, "topic3 should be in offers_by_topic"
    assert "topic4" in result.offers_by_topic, "topic4 should be in offers_by_topic"
    
    # Check docs for all topics
    assert "topic1" in result.docs_by_topic, "topic1 should be in docs_by_topic"
    assert "topic2" in result.docs_by_topic, "topic2 should be in docs_by_topic"
    assert "topic3" in result.docs_by_topic, "topic3 should be in docs_by_topic"
    assert "topic4" in result.docs_by_topic, "topic4 should be in docs_by_topic"
    
    print("  test_rag_lookup_four_matches_found PASSED")
