"""
Configuration Module
===================

Central configuration management for the prompt enhancement service.

This module:
1. Loads environment variables from .env file (if present)
2. Defines application-wide settings and constants
3. Provides helper functions for configuration validation and access
4. Manages both mock mode (for development/testing) and Azure OpenAI mode

Configuration categories:
- Service settings (mode, endpoints, ports)
- Prompt enhancement parameters (skill levels, templates)
- Mock data (user profiles, RAG database)
"""

import os
import logging
from dotenv import load_dotenv
from typing import Dict, Any

# Load environment variables from .env file if present
load_dotenv()

# -------------------------------------------------
# --- Service Configuration                     ---
# -------------------------------------------------

# Mode Configuration: 
# - Mock mode: For development and testing without real API calls
# - Azure mode: For production with real Azure OpenAI integration
USE_MOCK = os.getenv("MOCK_RESPONSES", "true").lower() == "true"

# Azure OpenAI Configuration (only used if USE_MOCK is False)
AZURE_KEY = os.getenv("AZURE_OPENAI_KEY", "").lower()
AZURE_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "").lower()
AZURE_API_VERSION = "2024-10-21"  # GA version

# Model Configuration: Model deployment name in Azure 
MODEL_PROMPT_ENHANCER = os.getenv("MODEL_PROMPT_ENHANCER", "gpt-4").lower()

# Server Configuration
PORT = int(os.getenv("PORT", "8000"))


# -------------------------------------------------
# --- Prompt Enhancement Configuration          ---
# -------------------------------------------------

# Skill Levels define user expertise tiers to adapt responses
# The system can be extended with new skill levels as needed
SKILL_LEVELS = ('BEGINNER', 'INTERMEDIATE', 'EXPERT', 'BANK_AMBASSADOR_TRAINEE')

# Skill-Based Parameters map configuration values to each skill level
# These determine how the LLM behaves for users of different expertise
SKILL_PARAMS = {
    'BEGINNER': {
        'system_prompt_addon': "Explain concepts simply, provide step-by-step guidance, and define banking terms.",
        'temperature': 0.7,  # Higher temperature for more varied/helpful responses
        'max_tokens': 500    # Longer responses with more explanations
    },
    'INTERMEDIATE': {
        'system_prompt_addon': "Assume some familiarity with banking concepts. Focus on practical application and cross-service connections.",
        'temperature': 0.5,  # Balanced creativity and precision
        'max_tokens': 450    # Moderate length responses
    },
    'EXPERT': {
        'system_prompt_addon': "Provide concise, expert-level insights. Focus on strategic value and advanced integration points.",
        'temperature': 0.3,  # Lower temperature for more precise responses
        'max_tokens': 400    # Shorter, more concise responses
    },
    'BANK_AMBASSADOR_TRAINEE': {
        'system_prompt_addon': "Focus on the basics of bank services and how to talk about them simply. Encourage asking questions.",
        'temperature': 0.8,  # Highest temperature for varied, encouraging responses
        'max_tokens': 550    # Longest responses with more examples
    }
}

# Default Persona defines the base role of the assistant
# This can be overridden in the prompt formatting function
DEFAULT_PERSONA = "You are a helpful Internal Banking Advisor, dedicated to helping colleagues understand and promote the bank's diverse range of services to foster collaboration and ambassadorship."

# Restrictions Template provides guardrails for the LLM responses
# The [topic] placeholder is dynamically replaced based on matched RAG topics
RESTRICTIONS_TEMPLATE = """
Restrictions:
- Prioritize mentioning relevant internal bank services and products.
- Identify potential opportunities for colleagues to act as brand ambassadors for the services discussed.
- Frame answers to encourage collaboration between different bank departments or teams.
- Maintain a positive, professional, and encouraging tone.
- Do not provide external financial advice or competitor comparisons unless specifically asked and framed internally.
- If discussing [topic], ensure alignment with the bank's official messaging on that service.
"""

# -------------------------------------------------
# --- Mock Data for Development/Testing         ---
# -------------------------------------------------

# Mock User Profiles simulate different user types with varying skill levels
# In production, this would be replaced with a real user database
MOCK_USER_PROFILES = {
    "user001": {"name": "Alice", "skill_level": "INTERMEDIATE"},
    "user002": {"name": "Bob", "skill_level": "BEGINNER"},
    "user003": {"name": "Charlie"},  # Default to BEGINNER when no skill_level
    "user005": {"name": "Eve", "skill_level": "EXPERT"},
}

# Mock RAG Database maps topics to their keywords, context, and extras
# This simulates a knowledge base that would normally be in a vector database
MOCK_RAG_DB = {
    "internal_mobility_program": {
        "keywords": ["internal mobility", "career growth", "job openings", "internal transfer"],
        "context": "Our Internal Mobility Program facilitates career progression within the bank.",
        "offers": ["Sign up for a 1-on-1 career counseling session this month!", "Priority access to new internal job postings for program participants."],
        "tips": ["Update your internal profile regularly.", "Network with managers in departments you're interested in.", "Use the 'Job Alert' feature on the internal portal."],
        "related_docs": ["Internal Mobility Policy (doc_id: IMP001)", "Career Development Resources (link: /intranet/career-dev)"]
    },
    "new_mortgage_product": {
        "keywords": ["mortgage", "home loan", "property financing", "new product launch", "flexihome"],
        "context": "The 'FlexiHome' mortgage offers flexible rate options and a digital application.",
        "offers": ["Limited-time offer: Reduced processing fee for internal staff applications.", "Refer a colleague and get a bonus voucher!"],
        "tips": ["Familiarize yourself with the eligibility criteria.", "Highlight the quick pre-approval time when discussing with clients/colleagues.", "Use the internal calculator for estimations."],
        "related_docs": ["FlexiHome Product Guide (pdf_id: FHMG001)", "Internal Staff Mortgage Benefits (doc_id: ISMB003)"]
    },
    "small_business_services": {
        "keywords": ["smb", "small business", "business banking", "entrepreneur support"],
        "context": "We provide tailored solutions like loans, merchant services, and advisory for SMBs.",
        "offers": ["Discounted setup fee for merchant services for businesses referred internally.", "Free initial consultation with a business advisor."],
        "tips": ["Identify colleagues whose clients might benefit from SMB services.", "Understand the referral process.", "Focus on the advisory aspect as a key differentiator."],
        "related_docs": ["SMB Services Overview (pdf_id: SMB001)", "Internal Referral Guide (doc_id: IRG005)"]
    },
    "brand_ambassador_program": {
        "keywords": ["ambassador program", "brand advocacy", "internal promotion", "employee advocacy"],
        "context": "The Bank Ambassador Program empowers colleagues to confidently share information about our services.",
        "offers": ["Complete the training module and receive exclusive bank merchandise.", "Top ambassadors featured in the internal newsletter."],
        "tips": ["Focus on 1-2 services you know well.", "Share success stories.", "Use the official talking points available on the intranet."],
        "related_docs": ["Ambassador Program Handbook (doc_id: BAP001)", "Latest Service Talking Points (link: /intranet/talking-points)"]
    },
    "digital_banking_platform": {
        "keywords": ["online banking", "mobile app", "digital platform", "fintech"],
        "context": "Our enhanced Digital Banking Platform includes AI insights and budgeting tools.",
        "offers": ["Early access beta program for new features - sign up now!", "Feedback providers get entered into a monthly draw."],
        "tips": ["Walk through the new features yourself first.", "Highlight the AI insights feature to colleagues/clients.", "Promote the security aspects of the platform."],
        "related_docs": ["Digital Platform User Guide (pdf_id: DBP007)", "Feature Roadmap (link: /intranet/digital-roadmap)"]
    }
}

# RAG Configuration
NUM_KEYWORDS = 5  # Number of keywords to extract for RAG lookup


# -------------------------------------------------
# --- Configuration Utility Functions           ---
# -------------------------------------------------

def get_config() -> Dict[str, Any]:
    """
    Retrieve the full application configuration as a dictionary.
    
    This function is useful for:
    - Debugging configuration issues
    - Passing the full configuration to other components
    - Exposing configuration through admin endpoints
    
    Returns:
        Dict containing all configuration settings
    """
    config = {
        "use_mock": USE_MOCK,
        "port": PORT,
        "azure_key": AZURE_KEY[:5] + "..." if AZURE_KEY else "",  # Redacted for security
        "azure_endpoint": AZURE_ENDPOINT,
        "azure_api_version": AZURE_API_VERSION,
        "model_prompt_enhancer": MODEL_PROMPT_ENHANCER,
        "skill_levels": SKILL_LEVELS,
        "skill_params": SKILL_PARAMS,
        "default_persona": DEFAULT_PERSONA,
        "restrictions_template": RESTRICTIONS_TEMPLATE,
        "mock_user_profiles": MOCK_USER_PROFILES,
        "mock_rag_db_topics": list(MOCK_RAG_DB.keys()),  # Just the topics, not the full data
    }
    return config


def is_using_mock() -> bool:
    """
    Check if the application is configured to use mock responses instead of real LLM calls.
    
    This is used throughout the application to determine:
    - Whether to initialize Azure clients
    - Which response generation path to take
    - What information to display in debug/logging
    
    Returns:
        True if using mock mode, False if using Azure
    """
    return USE_MOCK


def validate_azure_config() -> bool:
    """
    Validate the Azure OpenAI configuration when not using mock mode.
    
    Checks:
    - API key is provided
    - Endpoint URL is provided
    - Model deployment name is provided
    
    In mock mode, validation always passes as Azure config isn't needed.
    
    Returns:
        True if the configuration is valid for Azure use or mock mode is enabled
    """
    if USE_MOCK:
        return True
    return bool(AZURE_KEY and AZURE_ENDPOINT and MODEL_PROMPT_ENHANCER)


# -------------------------------------------------
# --- Logging Configuration                     ---
# -------------------------------------------------

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Log configuration status on module import
if is_using_mock():
    logger.info("Application configured to use MOCK responses.")
else:
    logger.info("Application configured to use AZURE OpenAI.")
    if not validate_azure_config():
        logger.warning("Azure configuration is incomplete. Azure API calls will fail.")
    else:
        logger.info(f"Azure configuration appears valid. Using model: {MODEL_PROMPT_ENHANCER}")