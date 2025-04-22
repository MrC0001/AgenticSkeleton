"""
Azure Domain Knowledge
======================

Contains domain-specific knowledge and guidance for different specializations.
Used to enhance prompts with domain-specific context and terminology.
"""

from typing import Dict, Any

# Specialized domain knowledge and guidance for different domains
DOMAIN_KNOWLEDGE = {
    "cloud_computing": {
        "keywords": ["cloud platform", "microsoft azure", "aws", "amazon web services", 
                    "google cloud", "azure", "cloud computing", "cloud infrastructure",
                    "cloud services", "cloud migration", "cloud native", "serverless", 
                    "multi-region", "cloud costs", "cloud deployment"],
        "subtasks": {
            "research": ["research", "analyze", "compare", "evaluate", "assess", "study", "investigate"],
            "implement": ["implement", "deploy", "build", "create", "construct", "develop", "integrate"],
            "optimize": ["optimize", "improve", "enhance", "refine", "streamline", "tune", "refactor", "costs"]
        },
        "guidance": "Focus on cloud architecture best practices, cost optimization, and security considerations. Include relevant service names and deployment patterns.",
        "preferred_category": "develop"
    },
    
    "ai_ml": {
        "keywords": ["artificial intelligence", "machine learning", "neural network", "deep learning", 
                  "nlp", "natural language processing", "computer vision", "predictive model", 
                  "data science", "ai model", "ml pipeline", "generative ai", "large language model", "ai"],
        "subtasks": {
            "research": ["research", "analyze", "compare", "evaluate", "assess", "study", "investigate", "impact"],
            "data": ["data", "collect", "preprocess", "clean", "prepare", "gather", "dataset"],
            "model": ["model", "train", "develop", "build", "create", "implement", "design"],
            "deploy": ["deploy", "implement", "integrate", "release", "publish", "operationalize", "serve"],
            "impact": ["impact", "effect", "influence", "outcome", "result"]
        },
        "guidance": "Incorporate ML/AI best practices including data preprocessing, model selection criteria, evaluation metrics, and deployment considerations.",
        "preferred_category": "data-science"
    },
    
    "healthcare_tech": {
        "keywords": ["healthcare", "medical", "health informatics", "clinical", "patient care", 
                  "telehealth", "health monitoring", "medical imaging", "healthcare ai", 
                  "medical technology", "health records", "ehr", "remote patient monitoring",
                  "patient outcomes", "medical diagnosis"],
        "subtasks": {
            "research": ["research", "analyze", "investigate", "evaluate", "assess", "study", "review", "impact"],
            "design": ["design", "architect", "plan", "blueprint", "outline", "framework", "structure"],
            "implement": ["implement", "develop", "build", "create", "construct", "deploy", "integrate"],
            "evaluate": ["evaluate", "assess", "measure", "analyze", "test", "validate", "verify"],
            "impact": ["impact", "effect", "influence", "affect", "outcome"]
        },
        "guidance": "Address healthcare-specific concerns including regulatory compliance (HIPAA, GDPR), clinical workflows, and patient data privacy.",
        "preferred_category": "analyze"
    },
    
    "cybersecurity": {
        "keywords": ["security", "cybersecurity", "threat", "vulnerability", "encryption", 
                    "firewall", "intrusion detection", "malware", "ransomware", "zero trust", 
                    "security posture", "penetration testing", "security audit", "authentication",
                    "authorization", "identity management"],
        "subtasks": {
            "research": ["research", "analyze", "assess", "evaluate", "investigate", "study", "review"],
            "design": ["design", "architect", "plan", "outline", "structure", "framework"],
            "implement": ["implement", "deploy", "build", "create", "construct", "develop", "integrate"],
            "test": ["test", "verify", "validate", "check", "audit", "evaluate", "penetration test"],
            "monitor": ["monitor", "detect", "observe", "track", "log", "alert", "respond"]
        },
        "guidance": "Prioritize security best practices, defense-in-depth strategies, threat modeling, and compliance requirements.",
        "preferred_category": "develop"
    },
    
    "web_development": {
        "keywords": ["web", "website", "web application", "frontend", "backend", "full stack", 
                    "responsive design", "spa", "single page application", "progressive web app", 
                    "web architecture", "web framework", "web performance", "javascript", 
                    "html", "css", "react", "angular", "vue", "node"],
        "subtasks": {
            "design": ["design", "wireframe", "mockup", "sketch", "layout", "ui", "ux"],
            "frontend": ["frontend", "client-side", "ui", "ux", "html", "css", "javascript", "component"],
            "backend": ["backend", "server-side", "database", "api", "service", "middleware", "endpoint"],
            "deploy": ["deploy", "host", "publish", "release", "serve", "distribute", "deliver"],
            "optimize": ["optimize", "improve", "enhance", "refine", "tune", "performance"]
        },
        "guidance": "Consider responsive design, accessibility standards, performance optimization, and cross-browser compatibility.",
        "preferred_category": "develop"
    }
}