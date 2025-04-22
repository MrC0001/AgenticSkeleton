"""
Azure OpenAI Client
===================

Handles communication with Azure OpenAI API for LLM interactions.
Provides mock response capability based on configuration.
"""

import logging
from typing import Dict, Any, Optional

# Import Azure OpenAI only when needed - optional dependency
try:
    from openai import AzureOpenAI
    from openai.types.chat import ChatCompletion
except ImportError:
    AzureOpenAI = None
    ChatCompletion = None

from agentic_skeleton.config import settings

# Global client instance for singleton pattern
azure_client_instance: Optional['AzureOpenAIClient'] = None

logger = logging.getLogger(__name__)

class AzureOpenAIClient:
    """
    Client wrapper for Azure OpenAI interactions.
    
    Handles:
    - Client initialization with Azure credentials
    - Proper message formatting for chat completions
    - Error handling for API calls
    - Mock responses when configured
    """

    def __init__(self, api_key=None, azure_endpoint=None, api_version=None):
        """
        Initialize the client with Azure OpenAI credentials.
        
        Args:
            api_key: Azure OpenAI API key (defaults to settings.AZURE_KEY)
            azure_endpoint: Azure OpenAI endpoint URL (defaults to settings.AZURE_ENDPOINT)
            api_version: API version string (defaults to settings.AZURE_API_VERSION)
        """
        # Store credentials (use settings as defaults)
        self.api_key = api_key or settings.AZURE_KEY
        self.azure_endpoint = azure_endpoint or settings.AZURE_ENDPOINT
        self.api_version = api_version or settings.AZURE_API_VERSION
        self.client: Optional[AzureOpenAI] = None
        
        # Only initialize the real API client if not in mock mode
        if not settings.is_using_mock():
            self.initialize()
        else:
            logger.info("Mock mode enabled. Skipping Azure client initialization.")

    def initialize(self) -> bool:
        """
        Initialize the underlying Azure OpenAI client.
        
        Returns:
            True if initialization succeeded, False otherwise
        """
        # Check if Azure OpenAI library is installed
        if not AzureOpenAI:
            logger.error("Azure OpenAI library not installed. Cannot initialize client.")
            return False
            
        # Validate configuration
        if not settings.validate_azure_config():
            logger.warning("Azure configuration is invalid or incomplete. Cannot initialize client.")
            return False

        try:
            # Create client instance
            self.client = AzureOpenAI(
                api_key=self.api_key,
                azure_endpoint=self.azure_endpoint,
                api_version=self.api_version
            )
            logger.info("Azure OpenAI client initialized successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize Azure OpenAI client: {e}")
            self.client = None
            return False

    def call_llm(self, model: str, system_prompt: str, user_prompt: str, **kwargs) -> str:
        """
        Generate a completion using Azure OpenAI or return a mock response.
        
        The method:
        1. Handles mock mode by returning a detailed debug string
        2. In live mode, formats prompts as a chat completion with system/user messages
        3. Passes appropriate parameters to the API
        4. Handles errors and response extraction
        
        Args:
            model: Model deployment name in Azure (e.g., "gpt-4")
            system_prompt: System instructions for the model
            user_prompt: User's query or input
            **kwargs: Additional parameters (temperature, max_tokens, etc.)
            
        Returns:
            Generated response text or a mock response string
        """
        # MOCK MODE: Return a detailed mock response for debugging
        if settings.is_using_mock():
            logger.info(f"Mock Mode: Simulating LLM call for model '{model}'")
            mock_response = (
                f"--- MOCK RESPONSE ---\n"
                f"Model: {model}\n"
                f"Temperature: {kwargs.get('temperature', 'default')}\n"
                f"Max Tokens: {kwargs.get('max_tokens', 'default')}\n"
                f"--- System Prompt ---\n{system_prompt}\n"
                f"--- User Prompt ---\n{user_prompt}\n"
                f"--- End Mock --- (This would be the actual LLM output)"
            )
            return mock_response

        # LIVE MODE: Call the actual Azure OpenAI API
        if not self.client:
            error_msg = "Error: Azure OpenAI client not initialized or initialization failed."
            logger.error(error_msg)
            return error_msg

        # Format messages for the chat API
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        # Filter kwargs to include only valid API parameters
        valid_params = {"temperature", "max_tokens", "top_p", "frequency_penalty", "presence_penalty"}
        api_kwargs = {k: v for k, v in kwargs.items() if k in valid_params}

        try:
            # Make the API call
            logger.debug(f"Calling Azure OpenAI model '{model}' with params: {api_kwargs}")
            response: ChatCompletion = self.client.chat.completions.create(
                model=model,
                messages=messages,
                **api_kwargs
            )
            
            # Extract content from response
            if response.choices and response.choices[0].message:
                content = response.choices[0].message.content
                return content.strip() if content else ""
            else:
                logger.warning("Azure OpenAI response structure unexpected or empty.")
                return "Error: Received empty or invalid response from Azure OpenAI."

        except Exception as e:
            error_msg = f"Azure OpenAI API call failed: {e}"
            logger.error(error_msg)
            return f"Error: {str(e)}"


def initialize_client() -> Optional[AzureOpenAIClient]:
    """
    Initialize and return the singleton Azure OpenAI client instance.
    
    Implements the singleton pattern to ensure only one client instance
    exists throughout the application.
    
    Returns:
        Azure OpenAI client instance
    """
    global azure_client_instance

    # Return existing client if already initialized
    if azure_client_instance:
        return azure_client_instance

    # Create new client instance
    azure_client_instance = AzureOpenAIClient()

    # If not mocking, check if the internal client was successfully initialized
    if not settings.is_using_mock() and not azure_client_instance.client:
        logger.error("Azure client instance created, but internal client failed to initialize.")
        # Keep azure_client_instance as the wrapper object exists, but it's not usable for real calls.
        # The call_llm method handles the None client state.

    return azure_client_instance


# Module testing (only executed when running directly)
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    
    print(f"Mock Mode Active: {settings.is_using_mock()}")
    
    # Initialize the client
    client_wrapper = initialize_client()
    
    if client_wrapper:
        # Test parameters
        test_system_prompt = "You are a helpful assistant."
        test_user_prompt = "Explain the concept of RAG in simple terms."
        test_model = settings.MODEL_PROMPT_ENHANCER
        test_params = {"temperature": 0.5, "max_tokens": 150}
        
        # Call the LLM
        response = client_wrapper.call_llm(
            model=test_model,
            system_prompt=test_system_prompt,
            user_prompt=test_user_prompt,
            **test_params
        )
        
        print("\n--- LLM Call Result ---")
        print(response)
    else:
        print("Failed to initialize client wrapper.")