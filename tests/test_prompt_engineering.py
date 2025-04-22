# tests/test_prompt_engineering.py

import pytest
from agentic_skeleton.core import prompt_engineering

# --- Tests for extract_keywords_simple ---

@pytest.mark.parametrize(
    "text, num_keywords, expected",
    [
        ("Tell me about the new mortgage product", 5, ["new", "mortgage", "product"]),
        ("How can I grow my career here?", 3, ["can", "grow", "career"]),
        ("Simple query", 5, ["simple", "query"]),
        ("Lots of stop words a the an is are in on", 5, ["lots", "stop", "words"]),
        ("", 5, []),
        ("Punctuation! Does it matter?", 5, ["punctuation", "does", "matter"]),
        ("Short text", 1, ["short"]),
        ("Very long text with many potential keywords like mortgage savings credit card loan", 3, ["very", "long", "text"]),
    ]
)
def test_extract_keywords_simple(text, num_keywords, expected):
    """Test extract_keywords_simple with various inputs."""
    result = prompt_engineering.extract_keywords_simple(text, num_keywords)
    assert result == expected

# --- Tests for get_skill_based_params ---

# Mock settings for testing get_skill_based_params
MOCK_SKILL_LEVELS = ('BEGINNER', 'INTERMEDIATE', 'EXPERT')
MOCK_SKILL_PARAMS = {
    'BEGINNER': {'system_prompt_addon': 'Explain simply.', 'temperature': 0.7, 'max_tokens': 500},
    'INTERMEDIATE': {'system_prompt_addon': 'Provide some detail.', 'temperature': 0.6, 'max_tokens': 700},
    'EXPERT': {'system_prompt_addon': 'Be concise and technical.', 'temperature': 0.5, 'max_tokens': 1000}
}

@pytest.mark.parametrize(
    "skill_level, expected_key",
    [
        ("BEGINNER", "BEGINNER"),
        ("beginner", "BEGINNER"), # Test case insensitivity
        (" intermediate ", "INTERMEDIATE"), # Test stripping whitespace
        ("EXPERT", "EXPERT"),
        ("INVALID_SKILL", "BEGINNER"), # Test fallback for invalid skill
        ("", "BEGINNER"), # Test fallback for empty skill
    ]
)
def test_get_skill_based_params(monkeypatch, skill_level, expected_key):
    """Test get_skill_based_params with different skill levels and mocking settings."""
    # Mock the settings within the prompt_engineering module
    monkeypatch.setattr(prompt_engineering, 'SKILL_LEVELS', MOCK_SKILL_LEVELS)
    monkeypatch.setattr(prompt_engineering, 'SKILL_PARAMS', MOCK_SKILL_PARAMS)

    result = prompt_engineering.get_skill_based_params(skill_level)
    expected_params = MOCK_SKILL_PARAMS[expected_key]

    # Check if the result is a copy, not the original dict
    assert result is not expected_params
    assert result == expected_params

# --- Tests for format_prompt_pqr ---

MOCK_DEFAULT_PERSONA = "Mock Assistant Persona."
MOCK_RESTRICTIONS_TEMPLATE = "Mock Restrictions: Do not mention [topic]."

@pytest.mark.parametrize(
    "original_prompt, skill_addon, rag_context, persona, restrictions, topic, expected_system_contains, expected_user",
    [
        # Scenario 1: All args provided, topic placeholder used
        ("User query 1", "Skill addon 1", "RAG context 1", "Custom Persona 1", "Custom Restrictions: [topic]", "Topic1",
         ["Custom Persona 1", "Skill addon 1", "RAG context 1", "Custom Restrictions: Topic1"], "User query 1"),

        # Scenario 2: Default persona and restrictions, no RAG, no topic placeholder
        ("User query 2", "Skill addon 2", None, None, None, "Topic2",
         [MOCK_DEFAULT_PERSONA, "Skill addon 2", MOCK_RESTRICTIONS_TEMPLATE.replace('[topic]', 'Topic2')], "User query 2"), # Topic still replaces if present

        # Scenario 3: No skill addon, RAG context present
        ("User query 3", "", "RAG context 3", None, "Restrictions 3 (no placeholder)", None,
         [MOCK_DEFAULT_PERSONA, "RAG context 3", "Restrictions 3 (no placeholder)"], "User query 3"),

        # Scenario 4: Empty prompt, minimal args
        ("", "", None, None, None, None,
         [MOCK_DEFAULT_PERSONA, MOCK_RESTRICTIONS_TEMPLATE], ""),

        # Scenario 5: RAG context, default restrictions with topic
         ("User query 5", "Skill addon 5", "RAG context 5", None, None, "Topic5",
         [MOCK_DEFAULT_PERSONA, "Skill addon 5", "RAG context 5", MOCK_RESTRICTIONS_TEMPLATE.replace('[topic]', 'Topic5')], "User query 5"),
    ]
)
def test_format_prompt_pqr(monkeypatch, original_prompt, skill_addon, rag_context, persona, restrictions, topic, expected_system_contains, expected_user):
    """Test format_prompt_pqr with various inputs and mocked defaults."""
    # Mock the default settings
    monkeypatch.setattr(prompt_engineering, 'DEFAULT_PERSONA', MOCK_DEFAULT_PERSONA)
    monkeypatch.setattr(prompt_engineering, 'RESTRICTIONS_TEMPLATE', MOCK_RESTRICTIONS_TEMPLATE)

    system_prompt, user_prompt = prompt_engineering.format_prompt_pqr(
        original_prompt=original_prompt,
        skill_system_addon=skill_addon,
        rag_context=rag_context,
        persona=persona,
        restrictions=restrictions,
        topic=topic
    )

    # Check user prompt
    assert user_prompt == expected_user

    # Check system prompt contains expected parts
    for part in expected_system_contains:
        assert part in system_prompt

    # Check structure - ensure RAG context is framed correctly if present
    if rag_context:
        assert "--- Relevant Context ---" in system_prompt
        assert "Use the context above" in system_prompt
    else:
         assert "--- Relevant Context ---" not in system_prompt

    # Check structure - ensure skill guidance is framed correctly if present
    if skill_addon:
        assert "--- Skill Level Guidance ---" in system_prompt
    else:
        assert "--- Skill Level Guidance ---" not in system_prompt

    # Check structure - ensure restrictions are always present and framed
    assert "--- Mock Restrictions:" in system_prompt or "--- Custom Restrictions:" in system_prompt or "--- Restrictions 3" in system_prompt
