"""
Tests for the prompt processor module
"""

import pytest
from unittest.mock import MagicMock, patch

# Import the module to test
from agentic_skeleton.core import prompt_processor
from agentic_skeleton.core.models import RagResult

# --- Fixtures ---

@pytest.fixture
def mock_dependencies(monkeypatch):
    """Mocks all external dependencies for prompt_processor"""
    # Create a mock for the AzureOpenAIClient instance
    mock_azure_client_instance = MagicMock()
    mock_azure_client_instance.call_llm.return_value = "Generated Azure Response"

    # Create a mock RagResult object
    mock_rag_result = RagResult(
        rag_context="RAG system unavailable.",
        offers_by_topic={},
        docs_by_topic={},
        matched_topics=[]
    )

    mocks = {
        'get_user_skill_level': MagicMock(return_value='BEGINNER'),
        'extract_keywords_simple': MagicMock(return_value=['keyword1', 'keyword2']),
        'lookup': MagicMock(return_value=mock_rag_result),
        'get_skill_based_params': MagicMock(return_value={'skill_level_addon': 'Beginner addon', 'temperature': 0.7, 'max_tokens': 500}),
        'format_prompt_pqr': MagicMock(return_value=('Formatted System Prompt', 'Formatted User Prompt')),
        # Mock the initialize_client function to return our mock instance
        'initialize_client': MagicMock(return_value=mock_azure_client_instance),
        'is_using_mock': MagicMock(return_value=True) # Default to mock mode
    }

    monkeypatch.setattr('agentic_skeleton.core.user_profile.get_user_skill_level', mocks['get_user_skill_level'])
    monkeypatch.setattr('agentic_skeleton.core.prompt_engineering.extract_keywords_simple', mocks['extract_keywords_simple'])
    monkeypatch.setattr('agentic_skeleton.core.rag.lookup', mocks['lookup'])
    monkeypatch.setattr('agentic_skeleton.core.prompt_engineering.get_skill_based_params', mocks['get_skill_based_params'])
    monkeypatch.setattr('agentic_skeleton.core.prompt_engineering.format_prompt_pqr', mocks['format_prompt_pqr'])
    # Corrected: Mock initialize_client in the azure.client module
    monkeypatch.setattr('agentic_skeleton.core.azure.client.initialize_client', mocks['initialize_client'])
    monkeypatch.setattr('agentic_skeleton.config.settings.is_using_mock', mocks['is_using_mock'])

    # Store the mock client instance for assertion checks later
    mocks['mock_azure_client_instance'] = mock_azure_client_instance
    return mocks

# --- Test Cases ---

def test_process_prompt_request_mock_mode_success(mock_dependencies):
    """Test successful processing in mock mode with RAG context."""
    user_id = "user123"
    user_prompt = "Tell me about topic A"

    # Set mock mode
    mock_dependencies['is_using_mock'].return_value = True

    # Update the mock_rag_result with content
    mock_rag_result = RagResult(
        rag_context="Mock RAG context",
        offers_by_topic={"topic1": ["Offer 1"]},
        docs_by_topic={"topic1": ["Doc 1"]},
        matched_topics=["topic1"]
    )
    mock_dependencies['lookup'].return_value = mock_rag_result

    result = prompt_processor.process_prompt_request(user_id, user_prompt)

    # Assertions
    mock_dependencies['get_user_skill_level'].assert_called_once_with(user_id)
    mock_dependencies['extract_keywords_simple'].assert_called_once_with(user_prompt, num_keywords=5)
    mock_dependencies['lookup'].assert_called_once_with(['keyword1', 'keyword2'])
    mock_dependencies['get_skill_based_params'].assert_called_once_with('BEGINNER')
    mock_dependencies['format_prompt_pqr'].assert_called_once_with(
        user_prompt=user_prompt,
        skill_level_addon='Beginner addon',
        rag_result=mock_rag_result
    )
    # In mock mode, initialize_client and call_llm should NOT be called
    mock_dependencies['initialize_client'].assert_not_called()
    mock_dependencies['mock_azure_client_instance'].call_llm.assert_not_called()

    # Check the result (mock mode returns a formatted string)
    assert "--- Enhanced Prompt (Mock Mode) ---" in result
    assert f"User ID: {user_id} (BEGINNER)" in result
    assert f"Original Prompt: {user_prompt}" in result
    assert "Keywords: ['keyword1', 'keyword2']" in result
    assert "RAG Context Found: Yes" in result
    assert "RAG Matched Topics: ['topic1']" in result
    assert "LLM Params Used (excluding addon): {'skill_level_addon': 'Beginner addon', 'temperature': 0.7, 'max_tokens': 500}" in result
    assert "--- System Prompt ---\nFormatted System Prompt" in result
    assert "--- User Prompt ---\nFormatted User Prompt" in result
    assert "--- End Mock LLM Response ---" in result


def test_process_prompt_request_mock_mode_no_rag(mock_dependencies):
    """Test successful processing in mock mode without RAG context."""
    user_id = "user456"
    user_prompt = "General question"

    # Setup mocks for this scenario
    mock_dependencies['is_using_mock'].return_value = True
    mock_dependencies['extract_keywords_simple'].return_value = ['general', 'question']
    
    # Create an empty RAG result
    mock_rag_result = RagResult(
        rag_context="",
        offers_by_topic={},
        docs_by_topic={},
        matched_topics=[]
    )
    mock_dependencies['lookup'].return_value = mock_rag_result

    result = prompt_processor.process_prompt_request(user_id, user_prompt)

    # Assertions
    mock_dependencies['get_user_skill_level'].assert_called_once_with(user_id)
    mock_dependencies['extract_keywords_simple'].assert_called_once_with(user_prompt, num_keywords=5)
    mock_dependencies['lookup'].assert_called_once_with(['general', 'question'])
    mock_dependencies['get_skill_based_params'].assert_called_once_with('BEGINNER')
    mock_dependencies['format_prompt_pqr'].assert_called_once_with(
        user_prompt=user_prompt,
        skill_level_addon='Beginner addon',
        rag_result=mock_rag_result
    )
    # In mock mode, initialize_client and call_llm should NOT be called
    mock_dependencies['initialize_client'].assert_not_called()
    mock_dependencies['mock_azure_client_instance'].call_llm.assert_not_called()

    # Check the result
    assert "--- Enhanced Prompt (Mock Mode) ---" in result
    assert f"User ID: {user_id} (BEGINNER)" in result
    assert f"Original Prompt: {user_prompt}" in result
    assert "Keywords: ['general', 'question']" in result
    assert "RAG Context Found: No" in result
    assert "RAG Matched Topics: []" in result
    assert "LLM Params Used (excluding addon): {'skill_level_addon': 'Beginner addon', 'temperature': 0.7, 'max_tokens': 500}" in result
    assert "--- System Prompt ---\nFormatted System Prompt" in result
    assert "--- User Prompt ---\nFormatted User Prompt" in result
    assert "--- End Mock LLM Response ---" in result


def test_process_prompt_request_azure_mode_success(mock_dependencies):
    """Test successful processing in Azure mode."""
    user_id = "user789"
    user_prompt = "Ask Azure something"

    # Setup mocks for Azure mode
    mock_dependencies['is_using_mock'].return_value = False # Switch to Azure mode
    mock_dependencies['extract_keywords_simple'].return_value = ['azure', 'something']
    
    # Create a RAG result with content
    mock_rag_result = RagResult(
        rag_context="Azure RAG",
        offers_by_topic={"azure": ["Azure offer"]},
        docs_by_topic={"azure": ["Azure doc"]},
        matched_topics=["azure"]
    )
    mock_dependencies['lookup'].return_value = mock_rag_result

    result = prompt_processor.process_prompt_request(user_id, user_prompt)

    # Assertions
    mock_dependencies['get_user_skill_level'].assert_called_once_with(user_id)
    mock_dependencies['extract_keywords_simple'].assert_called_once_with(user_prompt, num_keywords=5)
    mock_dependencies['lookup'].assert_called_once_with(['azure', 'something'])
    mock_dependencies['get_skill_based_params'].assert_called_once_with('BEGINNER')
    mock_dependencies['format_prompt_pqr'].assert_called_once_with(
        user_prompt=user_prompt,
        skill_level_addon='Beginner addon',
        rag_result=mock_rag_result
    )
    # In Azure mode, initialize_client SHOULD be called
    mock_dependencies['initialize_client'].assert_called_once()
    # And call_llm on the returned instance SHOULD be called
    mock_dependencies['mock_azure_client_instance'].call_llm.assert_called_once_with(
        model=prompt_processor.settings.MODEL_PROMPT_ENHANCER, # Check model from settings
        system_prompt='Formatted System Prompt',
        user_prompt='Formatted User Prompt',
        temperature=0.7,
        max_tokens=500
    )

    # Check the result (should be the response from the mocked call_llm)
    assert result == "Generated Azure Response"


def test_process_prompt_request_user_not_found(mock_dependencies):
    """Test processing when get_user_skill_level returns default."""
    user_id = "unknown_user"
    user_prompt = "Who am I?"

    # Setup mocks for unknown user
    mock_dependencies['is_using_mock'].return_value = True
    mock_dependencies['get_user_skill_level'].return_value = 'BEGINNER' # Default skill level

    result = prompt_processor.process_prompt_request(user_id, user_prompt)

    # Assertions
    mock_dependencies['get_user_skill_level'].assert_called_once_with(user_id)
    # Check that get_skill_based_params was called with the default skill level
    mock_dependencies['get_skill_based_params'].assert_called_once_with('BEGINNER')

    # Check result details
    assert f"User ID: {user_id} (BEGINNER)" in result


def test_process_prompt_request_exception_handling(mock_dependencies):
    """Test that exceptions during processing are handled gracefully."""
    user_id = "error_user"
    user_prompt = "Cause an error"

    # Setup a mock to raise an exception
    mock_dependencies['is_using_mock'].return_value = True
    expected_exception_message = "RAG lookup failed!"
    mock_dependencies['lookup'].side_effect = Exception(expected_exception_message)

    # The function should catch the exception and return a formatted error response
    result = prompt_processor.process_prompt_request(user_id, user_prompt)
    
    # Check that the error message is in the result
    assert "Error:" in result
    assert expected_exception_message in result
