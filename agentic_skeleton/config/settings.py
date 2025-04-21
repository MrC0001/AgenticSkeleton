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
AZURE_KEY = os.getenv("AZURE_OPENAI_KEY", "").lower()
AZURE_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "").lower()
AZURE_API_VERSION = "2024-10-21" # GA version, theres also 2025-03-01-preview

# Model configuration
MODEL_PLANNER = os.getenv("MODEL_PLANNER", "gpt-4").lower()
MODEL_EXECUTOR = os.getenv("MODEL_EXECUTOR", "gpt-4").lower()
# Server configuration
PORT = int(os.getenv("PORT", "8000"))





# Azure Domain Knowledge - realistic data for production use
AZURE_DOMAIN_KNOWLEDGE = {
    "cloud_platforms": {
        "keywords": ["microsoft azure", "aws", "amazon web services", "google cloud", "azure", "cloud platform"],
        "context": (
            "This request involves cloud platforms. Consider these important aspects: "
            "1) Enterprise integration capabilities vary across platforms: Azure excels in Microsoft ecosystem, "
            "AWS offers extensive third-party integrations, GCP strengths in data analytics. "
            "2) Pricing models differ significantly: Azure has pay-as-you-go with enterprise agreements, "
            "AWS offers reserved instances and savings plans, GCP emphasizes sustained-use discounts. "
            "3) Current market shares: AWS 32%, Azure 22%, GCP 10%, others 36%."
        ),
        "preferred_approach": "analytical comparison with specific metrics and use cases"
    },
    "healthcare_ai": {
        "keywords": ["healthcare ai", "medical ai", "health informatics", "clinical ai"],
        "context": (
            "This healthcare AI request requires careful consideration of: "
            "1) Regulatory frameworks: FDA clearance processes for AI/ML as medical devices, "
            "HIPAA compliance requirements, EU MDR rules for health software. "
            "2) Key metrics: diagnostic accuracy benchmarks by clinical domain (radiology: 92-97%, "
            "pathology: 89-95%, clinical decision support: 78-85%), implementation timeframes (6-18 months). "
            "3) Leading implementations: Mayo Clinic clinical workflow augmentation, Cleveland Clinic "
            "diagnostic imaging support, Kaiser Permanente preventative care initiatives."
        ),
        "preferred_approach": "evidence-based analysis with clinical validation metrics"
    },
    "generative_ai": {
        "keywords": ["generative ai", "gen ai", "llm", "large language model", "text generation", "image generation"],
        "context": (
            "This generative AI topic requires focus on: "
            "1) Model architectures: Transformer-based (GPT family, LLaMA variants), Diffusion models (Stable Diffusion, DALL-E), "
            "Hybrid approaches (multimodal models like GPT-4V, Claude Opus). "
            "2) Performance considerations: Inference latency (200-500ms for hosted solutions), throughput requirements, "
            "fine-tuning costs ($5K-50K depending on model size and data volume). "
            "3) Implementation approaches: API integration (OpenAI, Anthropic, Mistral), "
            "on-premises deployment (optimized 7B-14B parameter models), hybrid architectures."
        ),
        "preferred_approach": "structured analysis of capabilities, limitations, and implementation paths"
    }
}





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
        "azure_domain_knowledge": AZURE_DOMAIN_KNOWLEDGE,
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