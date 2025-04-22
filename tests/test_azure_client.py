# tests/test_azure_client.py

import pytest
from unittest.mock import patch, MagicMock, ANY

# Import the class and function under test
from agentic_skeleton.core.azure.client import AzureOpenAIClient, initialize_client
# Import settings to mock its attributes/methods
from agentic_skeleton.config import settings
import agentic_skeleton.core.azure.client as client_module # Import module for patching global

# Mock the ChatCompletion structure returned by the API
class MockMessage:
    def __init__(self, content):
        self.content = content

class MockChoice:
    def __init__(self, content):
        self.message = MockMessage(content)

class MockChatCompletion:
    def __init__(self, content):
        self.choices = [MockChoice(content)]

# --- Tests for AzureOpenAIClient Class ---

@patch('agentic_skeleton.core.azure.client.settings')
@patch('agentic_skeleton.core.azure.client.AzureOpenAIClient.initialize')
def test_client_init_mock_mode(mock_initialize, mock_settings):
    """Test client initialization when mock mode is enabled."""
    mock_settings.is_using_mock.return_value = True
    mock_settings.AZURE_KEY = "dummy_key"
    mock_settings.AZURE_ENDPOINT = "dummy_endpoint"
    mock_settings.AZURE_API_VERSION = "dummy_version"

    client = AzureOpenAIClient()

    assert client.api_key == "dummy_key"
    assert client.azure_endpoint == "dummy_endpoint"
    assert client.api_version == "dummy_version"
    assert client.client is None
    mock_settings.is_using_mock.assert_called_once()
    mock_initialize.assert_not_called() # Initialize should NOT be called in mock mode

@patch('agentic_skeleton.core.azure.client.settings')
@patch('agentic_skeleton.core.azure.client.AzureOpenAIClient.initialize')
def test_client_init_live_mode(mock_initialize, mock_settings):
    """Test client initialization when mock mode is disabled (live mode)."""
    mock_settings.is_using_mock.return_value = False
    mock_settings.AZURE_KEY = "live_key"
    mock_settings.AZURE_ENDPOINT = "live_endpoint"
    mock_settings.AZURE_API_VERSION = "live_version"

    client = AzureOpenAIClient(api_key="override_key") # Test override

    assert client.api_key == "override_key" # Check override
    assert client.azure_endpoint == "live_endpoint"
    assert client.api_version == "live_version"
    mock_settings.is_using_mock.assert_called_once()
    mock_initialize.assert_called_once() # Initialize SHOULD be called in live mode

@patch('agentic_skeleton.core.azure.client.settings')
@patch('agentic_skeleton.core.azure.client.AzureOpenAI', new_callable=MagicMock) # Mock the AzureOpenAI class
def test_client_initialize_success(mock_AzureOpenAI_class, mock_settings):
    """Test successful initialization of the underlying AzureOpenAI client."""
    mock_settings.is_using_mock.return_value = False # Ensure live mode for initialize call
    mock_settings.validate_azure_config.return_value = True
    mock_settings.AZURE_KEY = "valid_key"
    mock_settings.AZURE_ENDPOINT = "valid_endpoint"
    mock_settings.AZURE_API_VERSION = "valid_version"

    # We need an instance to call initialize on
    # Re-initialize the mock for the class instance returned by the constructor
    mock_azure_client_instance = MagicMock()
    mock_AzureOpenAI_class.return_value = mock_azure_client_instance

    client_instance = AzureOpenAIClient() # __init__ will call initialize here

    # Assertions on the result of initialize (called within __init__)
    assert client_instance.client is mock_azure_client_instance # Check that the internal client was created and assigned
    # Check if the mocked AzureOpenAI was called with correct args
    mock_AzureOpenAI_class.assert_called_once_with(
        api_key="valid_key",
        azure_endpoint="valid_endpoint",
        api_version="valid_version"
    )

@patch('agentic_skeleton.core.azure.client.settings')
@patch('agentic_skeleton.core.azure.client.AzureOpenAI', new=None) # Simulate library not installed
def test_client_initialize_no_library(mock_settings):
    """Test initialize failure when AzureOpenAI library is not installed."""
    mock_settings.is_using_mock.return_value = False
    client_instance = AzureOpenAIClient() # __init__ calls initialize

    assert client_instance.client is None
    # Check logs if necessary (requires patching logger)

@patch('agentic_skeleton.core.azure.client.settings')
@patch('agentic_skeleton.core.azure.client.AzureOpenAI', new_callable=MagicMock)
def test_client_initialize_invalid_config(mock_AzureOpenAI_class, mock_settings):
    """Test initialize failure when Azure config validation fails."""
    mock_settings.is_using_mock.return_value = False
    mock_settings.validate_azure_config.return_value = False # Simulate invalid config

    client_instance = AzureOpenAIClient()

    assert client_instance.client is None
    mock_settings.validate_azure_config.assert_called_once()
    mock_AzureOpenAI_class.assert_not_called() # Client shouldn't be created

@patch('agentic_skeleton.core.azure.client.settings')
@patch('agentic_skeleton.core.azure.client.AzureOpenAI') # Patch to raise error
def test_client_initialize_api_error(mock_AzureOpenAI, mock_settings):
    """Test initialize failure when AzureOpenAI constructor raises an error."""
    mock_settings.is_using_mock.return_value = False
    mock_settings.validate_azure_config.return_value = True
    mock_AzureOpenAI.side_effect = Exception("Connection error") # Simulate API error

    client_instance = AzureOpenAIClient()

    assert client_instance.client is None
    mock_AzureOpenAI.assert_called_once()
    # Check logs if necessary

# --- Tests for initialize_client Singleton ---

# Need to reset the global instance between tests that use it
@pytest.fixture(autouse=True)
def reset_singleton():
    """Reset the global client instance before each test."""
    client_module.azure_client_instance = None
    yield
    client_module.azure_client_instance = None

@patch('agentic_skeleton.core.azure.client.AzureOpenAIClient')
def test_initialize_client_first_call(MockAzureClient):
    """Test that the first call to initialize_client creates an instance."""
    mock_instance = MagicMock()
    MockAzureClient.return_value = mock_instance

    client1 = initialize_client()

    assert client1 is mock_instance # Check if the created instance is returned
    MockAzureClient.assert_called_once() # Ensure constructor was called

@patch('agentic_skeleton.core.azure.client.AzureOpenAIClient')
def test_initialize_client_singleton(MockAzureClient):
    """Test that subsequent calls to initialize_client return the same instance."""
    mock_instance = MagicMock()
    MockAzureClient.return_value = mock_instance

    client1 = initialize_client()
    client2 = initialize_client()

    assert client1 is mock_instance
    assert client2 is client1 # Check if the second call returned the same instance
    MockAzureClient.assert_called_once() # Constructor should only be called once

@patch('agentic_skeleton.core.azure.client.settings')
@patch('agentic_skeleton.core.azure.client.AzureOpenAIClient')
def test_initialize_client_live_mode_init_failure(MockAzureClient, mock_settings):
    """Test initialize_client when in live mode but internal client init fails."""
    mock_settings.is_using_mock.return_value = False

    # Simulate the AzureOpenAIClient instance being created, but its internal .client is None
    mock_client_wrapper_instance = MagicMock()
    mock_client_wrapper_instance.client = None # Simulate failed internal init
    MockAzureClient.return_value = mock_client_wrapper_instance

    client_instance = initialize_client()

    assert client_instance is mock_client_wrapper_instance
    # Check that the wrapper instance is stored globally, even if internal init failed
    assert client_module.azure_client_instance is mock_client_wrapper_instance
    mock_settings.is_using_mock.assert_called_once()
    # We expect logs indicating the failure, could patch logger to check

# --- Tests for call_llm Method ---

@patch('agentic_skeleton.core.azure.client.settings')
def test_call_llm_mock_mode(mock_settings):
    """Test call_llm when mock mode is enabled."""
    mock_settings.is_using_mock.return_value = True
    # No need to mock initialize, as it won't be called in mock mode init
    client = AzureOpenAIClient()

    model = "test-model"
    system_prompt = "System instructions"
    user_prompt = "User query"
    kwargs = {"temperature": 0.7, "max_tokens": 100}

    response = client.call_llm(model, system_prompt, user_prompt, **kwargs)

    # Assert the response is the detailed mock string
    assert "--- MOCK RESPONSE ---" in response
    assert f"Model: {model}" in response
    assert f"Temperature: {kwargs['temperature']}" in response
    assert f"Max Tokens: {kwargs['max_tokens']}" in response
    assert f"--- System Prompt ---\n{system_prompt}" in response
    assert f"--- User Prompt ---\n{user_prompt}" in response
    assert "--- End Mock ---" in response
    mock_settings.is_using_mock.assert_called() # Check mock mode was checked

@patch('agentic_skeleton.core.azure.client.settings')
@patch('agentic_skeleton.core.azure.client.AzureOpenAI', new_callable=MagicMock)
def test_call_llm_live_mode_success(mock_AzureOpenAI_class, mock_settings):
    """Test call_llm in live mode with a successful API call."""
    mock_settings.is_using_mock.return_value = False
    mock_settings.validate_azure_config.return_value = True # Ensure init succeeds
    mock_settings.AZURE_KEY = "valid_key"
    mock_settings.AZURE_ENDPOINT = "valid_endpoint"
    mock_settings.AZURE_API_VERSION = "valid_version"

    # Mock the instance returned by AzureOpenAI() and its methods
    mock_client_instance = MagicMock()
    mock_AzureOpenAI_class.return_value = mock_client_instance

    # Configure the mock response from chat.completions.create
    expected_content = " This is the LLM response. "
    mock_api_response = MockChatCompletion(content=expected_content)
    mock_client_instance.chat.completions.create.return_value = mock_api_response

    # Create the client (this will initialize the mocked internal client)
    client = AzureOpenAIClient()
    assert client.client is mock_client_instance # Verify internal client is set

    model = "gpt-live"
    system_prompt = "System instructions live"
    user_prompt = "User query live"
    kwargs = {"temperature": 0.8, "max_tokens": 150, "invalid_param": "ignore"}

    response = client.call_llm(model, system_prompt, user_prompt, **kwargs)

    # Assert the actual API call was made with correct parameters
    mock_client_instance.chat.completions.create.assert_called_once_with(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.8, # Check valid params are passed
        max_tokens=150
        # 'invalid_param' should be filtered out
    )

    # Assert the response is the stripped content from the mock API response
    assert response == expected_content.strip()

@patch('agentic_skeleton.core.azure.client.settings')
def test_call_llm_live_mode_client_not_initialized(mock_settings):
    """Test call_llm in live mode when the client failed to initialize."""
    mock_settings.is_using_mock.return_value = False
    # Simulate init failure by not mocking AzureOpenAI or setting validate_config to False
    mock_settings.validate_azure_config.return_value = False

    client = AzureOpenAIClient() # Init will fail, client.client will be None
    assert client.client is None

    response = client.call_llm("model", "system", "user")

    assert "Error: Azure OpenAI client not initialized" in response

@patch('agentic_skeleton.core.azure.client.settings')
@patch('agentic_skeleton.core.azure.client.AzureOpenAI', new_callable=MagicMock)
def test_call_llm_live_mode_api_error(mock_AzureOpenAI_class, mock_settings):
    """Test call_llm in live mode when the API call raises an exception."""
    mock_settings.is_using_mock.return_value = False
    mock_settings.validate_azure_config.return_value = True
    mock_client_instance = MagicMock()
    mock_AzureOpenAI_class.return_value = mock_client_instance

    # Configure the mock API call to raise an error
    error_message = "API connection timed out"
    mock_client_instance.chat.completions.create.side_effect = Exception(error_message)

    client = AzureOpenAIClient()
    response = client.call_llm("model", "system", "user")

    # Assert an error message is returned, containing the exception text
    assert "Error:" in response
    assert error_message in response
    mock_client_instance.chat.completions.create.assert_called_once() # Ensure call was attempted

@patch('agentic_skeleton.core.azure.client.settings')
@patch('agentic_skeleton.core.azure.client.AzureOpenAI', new_callable=MagicMock)
def test_call_llm_live_mode_empty_response(mock_AzureOpenAI_class, mock_settings):
    """Test call_llm in live mode when the API returns an empty/invalid structure."""
    mock_settings.is_using_mock.return_value = False
    mock_settings.validate_azure_config.return_value = True
    mock_client_instance = MagicMock()
    mock_AzureOpenAI_class.return_value = mock_client_instance

    # Configure an empty or malformed response
    mock_empty_response = MagicMock()
    mock_empty_response.choices = [] # No choices
    mock_client_instance.chat.completions.create.return_value = mock_empty_response

    client = AzureOpenAIClient()
    response = client.call_llm("model", "system", "user")

    assert "Error: Received empty or invalid response" in response
    mock_client_instance.chat.completions.create.assert_called_once()
