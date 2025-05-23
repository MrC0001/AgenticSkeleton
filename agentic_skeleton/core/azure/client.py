"""
Azure OpenAI Client
======================

Handles Azure OpenAI client initialization and API calls.
"""

import logging
from typing import Dict, Any, Optional

# Optional: Import Azure OpenAI only when needed
try:
    from openai import AzureOpenAI
except ImportError:
    AzureOpenAI = None

from agentic_skeleton.config import settings

# Global client instance
azure_client_instance = None

class AzureOpenAIClient:
    """Client class for Azure OpenAI interactions"""
    
    def __init__(self, api_key=None, azure_endpoint=None, api_version=None):
        self.api_key = api_key or settings.AZURE_KEY
        self.azure_endpoint = azure_endpoint or settings.AZURE_ENDPOINT
        self.api_version = api_version or settings.AZURE_API_VERSION
        self.client = None
        self.initialize()
        
    def initialize(self):
        """Initialize the underlying Azure OpenAI client"""
        try:
            self.client = AzureOpenAI(
                api_key=self.api_key,
                azure_endpoint=self.azure_endpoint,
                api_version=self.api_version
            )
            logging.info("Azure OpenAI client initialized successfully")
            return True
        except Exception as e:
            logging.error(f"Failed to initialize Azure OpenAI client: {e}")
            return False
            
    def generate_completion(self, model, prompt, temperature=0.3):
        """Generate a completion using the Azure OpenAI API"""
        if not self.client:
            return "Error: Azure OpenAI client not initialized"
            
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[{"role": "system", "content": prompt}],
                temperature=temperature
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            error_msg = f"Azure OpenAI API call failed: {e}"
            logging.error(error_msg)
            return f"Error: {str(e)}"


def initialize_client() -> Optional[AzureOpenAIClient]:
    """
    Initialize the Azure OpenAI client.
    
    Returns:
        Azure OpenAI client if successful, None if initialization fails
    """
    global azure_client_instance
    
    # 1. Return existing client if already initialized
    if azure_client_instance and azure_client_instance.client:
        return azure_client_instance
    
    # 2. Validate configuration settings
    if not settings.validate_azure_config():
        logging.warning("Azure OpenAI credentials not found or incomplete")
        return None
    
    # 3. Create new client instance
    azure_client_instance = AzureOpenAIClient()
    if azure_client_instance.client:
        return azure_client_instance
    return None


def call_azure_openai(model: str, prompt: str) -> str:
    """
    Call Azure OpenAI API with error handling.
    
    Args:
        model: The model deployment name
        prompt: The prompt to send to the model
        
    Returns:
        Generated response text or error message
    """
    # 1. Get the client instance
    client_wrapper = initialize_client()
    if not client_wrapper:
        return "Azure OpenAI client not initialized"
    
    # 2. Make API call using the client wrapper
    return client_wrapper.generate_completion(model, prompt)