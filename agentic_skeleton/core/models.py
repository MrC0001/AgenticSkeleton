"""
Data Models Module
================

This module defines the core data models used throughout the application.
These Pydantic models provide type safety, validation, and clear structure
for RAG (Retrieval Augmented Generation) data.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class RagEntry(BaseModel):
    """
    Represents a single entry in the RAG database.
    
    Each entry corresponds to a specific topic and contains:
    - Keywords for matching user queries to this topic
    - Context information to enrich the prompt
    - Offers related to the topic for response enhancement
    - Tips for better prompt handling of this topic
    - Related documents/links to provide additional resources
    """
    keywords: List[str] = Field(..., description="Keywords associated with the topic.")
    context: str = Field(..., description="Contextual information for prompt enrichment.")
    offers: List[str] = Field(default_factory=list, description="Promotional offers to append to the response.")
    tips: List[str] = Field(default_factory=list, description="Tips for prompt enrichment.")
    related_docs: List[str] = Field(default_factory=list, description="Related documents/links to append to the response.")

class RagResult(BaseModel):
    """
    Represents the result of a RAG lookup operation.
    
    This model aggregates information from multiple matched RAG entries:
    - Combined context text for prompt enrichment
    - Offers organized by topic for selective inclusion in the response
    - Related documents organized by topic for selective inclusion
    - List of matched topics for tracking and logging purposes
    
    The granular organization by topic enables intelligent filtering
    based on the number of matched topics.
    """
    rag_context: str = Field(..., description="Combined context and tips from matched RAG entries for prompt enrichment.")
    offers_by_topic: Dict[str, List[str]] = Field(default_factory=dict, description="Offers grouped by the matched topic.")
    docs_by_topic: Dict[str, List[str]] = Field(default_factory=dict, description="Related documents/links grouped by the matched topic.")
    matched_topics: List[str] = Field(default_factory=list, description="List of topics that matched the keywords.")

