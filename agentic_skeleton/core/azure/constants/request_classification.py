"""
Request Classification Constants
======================

Contains constants used for request classification in the Azure implementation.
"""

from typing import List, Dict, Any

# Shared request classification patterns
REQUEST_CLASSIFIERS = [
    {
        "type": "data-science",
        "patterns": [
            "machine learning", "ml model", "predictive model", "data mining", 
            "train model", "neural network", "clustering", "classification algorithm",
            "regression", "feature engineering", "data preprocessing", "dataset",
            "predict", "forecasting", "ai model", "customer churn", "nlp", "train"
        ]
    },
    {
        "type": "analyze",
        "patterns": [
            "analyze", "analysis", "evaluate", "assess", "review", "study", 
            "research", "compare", "investigate", "examine", "trends", "patterns",
            "market analysis", "competitive analysis", "impact", "implications"
        ]
    },
    {
        "type": "design",
        "patterns": [
            "design", "wireframe", "sketch", "mock up", "prototype", "ui", "ux",
            "user interface", "user experience", "layout", "visual", "graphics",
            "augmented reality interface", "ar", "vr", "user flow", "design system"
        ]
    },
    {
        "type": "write",
        "patterns": [
            "write", "draft", "blog", "article", "post", "essay", "content", 
            "copywriting", "script", "document", "report", "whitepaper", "create content"
        ]
    },
    {
        "type": "develop",
        "patterns": [
            "develop", "build", "implement", "code", "program", 
            "website", "backend", "frontend", "software", "function", "class", 
            "module", "database", "rest api", "web interface", "responsive"
        ]
    }
]

# Complex task indicators
COMPLEX_TASK_INDICATORS = [
    "comprehensive plan", "end-to-end", "full stack", "multi-phase", 
    "platform", "ecosystem", "integrated system", "launch"
]

# Generic subtask patterns for fallback
GENERIC_SUBTASK_PATTERNS = {
    "document": ["document", "write documentation", "create documentation", "documentation"],
    "research": ["research", "analyze", "study", "investigate", "explore", "examine", "review", "collect"],
    "implement": ["implement", "build", "create", "develop", "code", "program", "construct"],
    "design": ["design", "architect", "plan", "outline", "sketch", "wireframe", "draft"],
    "evaluate": ["evaluate", "assess", "test", "verify", "validate", "measure", "analyze"],
    "optimize": ["optimize", "improve", "enhance", "refine", "tune", "streamline", "refactor"],
    "data": ["train", "model", "data", "dataset", "preprocess", "feature"]
}