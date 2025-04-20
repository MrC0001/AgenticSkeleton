"""
Configuration Module
===================

Handles loading of environment variables and configuration settings for the application.
Supports both mock and Azure OpenAI modes.
"""

import os
import logging
from dotenv import load_dotenv
from typing import Dict, Any, Optional

# Load environment variables
load_dotenv()

# Mode configuration
USE_MOCK = os.getenv("MOCK_RESPONSES", "true").lower() == "true"

# Azure OpenAI configuration (only used in production mode)
AZURE_KEY = os.getenv("AZURE_OPENAI_KEY")
AZURE_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_API_VERSION = "2025-04-20"

# Model configuration
MODEL_PLANNER = os.getenv("MODEL_PLANNER", "gpt-4")
MODEL_EXECUTOR = os.getenv("MODEL_EXECUTOR", "gpt-4")

# Server configuration
PORT = int(os.getenv("PORT", "8000"))

# Prompt templates
PLANNER_TEMPLATE = (
    "You are a task planning assistant specialized in breaking down complex requests.\n"
    "Your goal is to decompose the following user request into 3-7 concrete, actionable subtasks.\n"
    "Each subtask should be specific, self-contained, and clearly contribute to the overall goal.\n"
    "Order the subtasks logically from initial research to final delivery.\n\n"
    "User request: \"{user_request}\"\n\n"
    "Subtasks:\n"
    "1."
)

EXECUTOR_TEMPLATE = (
    "You are an execution assistant specialized in completing individual tasks with precision.\n"
    "Complete the subtask below thoroughly and provide a concise, specific result.\n"
    "Focus on providing actionable information and concrete outputs.\n"
    "Include key metrics, specific findings, or deliverables in your response.\n\n"
    "Subtask: {subtask}\n\n"
    "Result:"
)

def get_config() -> Dict[str, Any]:
    """
    Get the full application configuration as a dictionary.
    
    Returns:
        Dict containing all configuration settings
    """
    return {
        "use_mock": USE_MOCK,
        "azure_key": AZURE_KEY,
        "azure_endpoint": AZURE_ENDPOINT,
        "azure_api_version": AZURE_API_VERSION,
        "model_planner": MODEL_PLANNER,
        "model_executor": MODEL_EXECUTOR,
        "port": PORT,
        "planner_template": PLANNER_TEMPLATE,
        "executor_template": EXECUTOR_TEMPLATE
    }

def is_using_mock() -> bool:
    """
    Check if the application is using mock mode.
    
    Returns:
        True if using mock mode, False if using Azure
    """
    return USE_MOCK

def validate_azure_config() -> bool:
    """
    Validate Azure OpenAI configuration.
    
    Returns:
        True if the configuration is valid, False otherwise
    """
    return bool(AZURE_KEY and AZURE_ENDPOINT)