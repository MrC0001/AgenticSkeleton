# tests/test_rag.py

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


# --- Setup for rag tests ---

@pytest.fixture(autouse=True)
def setup_rag():
    """Fixture to inject the local mock DB before each test and restore afterwards."""
    original_db = getattr(rag, 'MOCK_RAG_DB', None)
    rag.MOCK_RAG_DB = MOCK_RAG_DB_FOR_TEST
    yield  # Test runs here
    rag.MOCK_RAG_DB = original_db  # Restore original DB


# --- Tests for rag.lookup using local MOCK_RAG_DB_FOR_TEST ---

def test_rag_lookup_no_keywords_provided():
    """Test RAG lookup with no keywords provided. Expect empty result."""
    print("\nTesting RAG lookup: No Keywords Provided")
    result = rag.lookup([])
    print(f"  Result: {result}")
    assert result['context'] == "", "Context should be empty for no keywords"
    assert result.get('offers', []) == [], "Offers should be empty for no keywords"
    assert result.get('tips', []) == [], "Tips should be empty for no keywords"
    assert result.get('related_docs', []) == [], "Related docs should be empty for no keywords"
    print("  test_rag_lookup_no_keywords_provided PASSED")


def test_rag_lookup_no_match_found():
    """Test RAG lookup when no keywords match any topic."""
    print("\nTesting RAG lookup: No Match Found")
    keywords = ["nonexistent", "keyword"]
    result = rag.lookup(keywords)
    print(f"  Input Keywords: {keywords}")
    print(f"  Result: {result}")
    assert result['context'] == "", "Context should be empty for no match"
    assert result.get('offers', []) == [], "Offers should be empty for no match"
    assert result.get('tips', []) == [], "Tips should be empty for no match"
    assert result.get('related_docs', []) == [], "Related docs should be empty for no match"
    print("  test_rag_lookup_no_match_found PASSED")


def test_rag_lookup_one_match_found():
    """Test RAG lookup when keywords match exactly one topic (expect all items)."""
    print("\nTesting RAG lookup: One Match Found")
    keywords = ["alpha"]  # Matches topic1
    result = rag.lookup(keywords)
    print(f"  Input Keywords: {keywords}")
    print(f"  Result: {result}")
    expected_data = MOCK_RAG_DB_FOR_TEST["topic1"]
    assert result.get('context', '') == expected_data["context"], "Context from topic1 expected"
    assert len(result.get('offers', [])) == 3, "Should return all 3 offers for topic1"
    assert len(result.get('tips', [])) == 2, "Should return all 2 tips for topic1"
    assert len(result.get('related_docs', [])) == 1, "Should return all 1 related doc for topic1"
    assert sorted(result.get('offers', [])) == sorted(expected_data["offers"]), "Offers should match topic1"
    assert sorted(result.get('tips', [])) == sorted(expected_data["tips"]), "Tips should match topic1"
    assert sorted(result.get('related_docs', [])) == sorted(expected_data["related_docs"]), "Docs should match topic1"
    print("  test_rag_lookup_one_match_found PASSED")


def test_rag_lookup_two_matches_found():
    """Test RAG lookup when keywords match two topics (expect first 2 items from each)."""
    print("\nTesting RAG lookup: Two Matches Found")
    keywords = ["test"]  # Matches topic1 and topic2
    result = rag.lookup(keywords)
    print(f"  Input Keywords: {keywords}")
    print(f"  Result: {result}")

    expected_context = [MOCK_RAG_DB_FOR_TEST["topic1"]["context"], MOCK_RAG_DB_FOR_TEST["topic2"]["context"]]
    expected_offers = MOCK_RAG_DB_FOR_TEST["topic1"]["offers"][:2] + MOCK_RAG_DB_FOR_TEST["topic2"]["offers"][:2]
    expected_tips = MOCK_RAG_DB_FOR_TEST["topic1"]["tips"][:2] + MOCK_RAG_DB_FOR_TEST["topic2"]["tips"][:2]
    expected_docs = MOCK_RAG_DB_FOR_TEST["topic1"]["related_docs"][:2] + MOCK_RAG_DB_FOR_TEST["topic2"]["related_docs"][:2]

    assert isinstance(result.get('context', ''), str), "Context should be a string"
    # Check if both contexts are present in the combined string
    assert MOCK_RAG_DB_FOR_TEST["topic1"]["context"] in result.get('context', ''), "Context from topic1 expected"
    assert MOCK_RAG_DB_FOR_TEST["topic2"]["context"] in result.get('context', ''), "Context from topic2 expected"

    assert len(result.get('offers', [])) == 4, "Should return 2 offers from topic1 + 2 from topic2"
    assert len(result.get('tips', [])) == 4, "Should return 2 tips from topic1 + 2 from topic2"
    assert len(result.get('related_docs', [])) == 3, "Should return 1 doc from topic1 + 2 from topic2"

    # Check content (order might vary, so check membership)
    for offer in expected_offers:
        assert offer in result.get('offers', []), f"Expected offer '{offer}' not found"
    for tip in expected_tips:
        assert tip in result.get('tips', []), f"Expected tip '{tip}' not found"
    for doc in expected_docs:
        assert doc in result.get('related_docs', []), f"Expected doc '{doc}' not found"
    print("  test_rag_lookup_two_matches_found PASSED")


def test_rag_lookup_three_matches_found():
    """Test RAG lookup when keywords match three topics (expect first 1 item from each)."""
    print("\nTesting RAG lookup: Three Matches Found")
    keywords = ["one", "beta", "gamma"]  # Matches topic1, topic2, topic3
    result = rag.lookup(keywords)
    print(f"  Input Keywords: {keywords}")
    print(f"  Result: {result}")

    expected_context = [
        MOCK_RAG_DB_FOR_TEST["topic1"]["context"],
        MOCK_RAG_DB_FOR_TEST["topic2"]["context"],
        MOCK_RAG_DB_FOR_TEST["topic3"]["context"]
    ]
    expected_offers = (MOCK_RAG_DB_FOR_TEST["topic1"]["offers"][:1] +
                       MOCK_RAG_DB_FOR_TEST["topic2"]["offers"][:1] +
                       MOCK_RAG_DB_FOR_TEST["topic3"]["offers"][:1])
    expected_tips = (MOCK_RAG_DB_FOR_TEST["topic1"]["tips"][:1] +
                     MOCK_RAG_DB_FOR_TEST["topic2"]["tips"][:1] +
                     MOCK_RAG_DB_FOR_TEST["topic3"]["tips"][:1])
    expected_docs = (MOCK_RAG_DB_FOR_TEST["topic1"]["related_docs"][:1] +
                     MOCK_RAG_DB_FOR_TEST["topic2"]["related_docs"][:1] +
                     MOCK_RAG_DB_FOR_TEST["topic3"]["related_docs"][:1])

    # Filter out empty lists that result from [:1] on an empty list in the source data
    expected_offers = [o for o in expected_offers if o]
    expected_tips = [t for t in expected_tips if t]
    expected_docs = [d for d in expected_docs if d]

    assert isinstance(result.get('context', ''), str), "Context should be a string"
    # Check if all three contexts are present
    assert MOCK_RAG_DB_FOR_TEST["topic1"]["context"] in result.get('context', ''), "Context from topic1 expected"
    assert MOCK_RAG_DB_FOR_TEST["topic2"]["context"] in result.get('context', ''), "Context from topic2 expected"
    assert MOCK_RAG_DB_FOR_TEST["topic3"]["context"] in result.get('context', ''), "Context from topic3 expected"

    assert len(result.get('offers', [])) == 3, "Should return 1 offer from topic1 + 1 from topic2 + 1 from topic3"
    assert len(result.get('tips', [])) == 3, "Should return 1 tip from topic1 + 1 from topic2 + 1 from topic3"
    assert len(result.get('related_docs', [])) == 3, "Should return 1 doc from topic1 + 1 from topic2 + 1 from topic3"

    # Check content (order might vary, so check membership)
    for offer in expected_offers:
        assert offer in result.get('offers', []), f"Expected offer '{offer}' not found"
    for tip in expected_tips:
        assert tip in result.get('tips', []), f"Expected tip '{tip}' not found"
    for doc in expected_docs:
        assert doc in result.get('related_docs', []), f"Expected doc '{doc}' not found"
    print("  test_rag_lookup_three_matches_found PASSED")


def test_rag_lookup_four_matches_found():
    """Test RAG lookup when keywords match four topics (expect first 1 item from each)."""
    print("\nTesting RAG lookup: Four Matches Found")
    keywords = ["one", "two", "three", "four"]  # Matches all topics
    result = rag.lookup(keywords)
    print(f"  Input Keywords: {keywords}")
    print(f"  Result: {result}")

    expected_context = [
        MOCK_RAG_DB_FOR_TEST["topic1"]["context"],
        MOCK_RAG_DB_FOR_TEST["topic2"]["context"],
        MOCK_RAG_DB_FOR_TEST["topic3"]["context"],
        MOCK_RAG_DB_FOR_TEST["topic4"]["context"]
    ]
    expected_offers = (MOCK_RAG_DB_FOR_TEST["topic1"]["offers"][:1] +
                       MOCK_RAG_DB_FOR_TEST["topic2"]["offers"][:1] +
                       MOCK_RAG_DB_FOR_TEST["topic3"]["offers"][:1] +
                       MOCK_RAG_DB_FOR_TEST["topic4"]["offers"][:1])
    expected_tips = (MOCK_RAG_DB_FOR_TEST["topic1"]["tips"][:1] +
                     MOCK_RAG_DB_FOR_TEST["topic2"]["tips"][:1] +
                     MOCK_RAG_DB_FOR_TEST["topic3"]["tips"][:1] +
                     MOCK_RAG_DB_FOR_TEST["topic4"]["tips"][:1])
    expected_docs = (MOCK_RAG_DB_FOR_TEST["topic1"]["related_docs"][:1] +
                     MOCK_RAG_DB_FOR_TEST["topic2"]["related_docs"][:1] +
                     MOCK_RAG_DB_FOR_TEST["topic3"]["related_docs"][:1] +
                     MOCK_RAG_DB_FOR_TEST["topic4"]["related_docs"][:1])

    # Filter out empty lists
    expected_offers = [o for o in expected_offers if o]
    expected_tips = [t for t in expected_tips if t]
    expected_docs = [d for d in expected_docs if d]

    assert isinstance(result.get('context', ''), str), "Context should be a string"
    # Check if all four contexts are present
    assert MOCK_RAG_DB_FOR_TEST["topic1"]["context"] in result.get('context', ''), "Context from topic1 expected"
    assert MOCK_RAG_DB_FOR_TEST["topic2"]["context"] in result.get('context', ''), "Context from topic2 expected"
    assert MOCK_RAG_DB_FOR_TEST["topic3"]["context"] in result.get('context', ''), "Context from topic3 expected"
    assert MOCK_RAG_DB_FOR_TEST["topic4"]["context"] in result.get('context', ''), "Context from topic4 expected"

    assert len(result.get('offers', [])) == 4, "Should return 1 offer from each of the 4 topics"
    assert len(result.get('tips', [])) == 4, "Should return 1 tip from each of the 4 topics"
    assert len(result.get('related_docs', [])) == 4, "Should return 1 doc from each of the 4 topics"

    # Check content (order might vary, so check membership)
    for offer in expected_offers:
        assert offer in result.get('offers', []), f"Expected offer '{offer}' not found"
    for tip in expected_tips:
        assert tip in result.get('tips', []), f"Expected tip '{tip}' not found"
    for doc in expected_docs:
        assert doc in result.get('related_docs', []), f"Expected doc '{doc}' not found"
    print("  test_rag_lookup_four_matches_found PASSED")
