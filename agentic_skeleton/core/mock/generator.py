"""
Mock Response Generator
======================

Generates mock responses for tasks based on the request classification and domain knowledge.
"""

import random
import re
import logging
from typing import Dict, List, Any, Optional, Tuple, Union

from agentic_skeleton.core.mock.constants.mock_responses import MOCK_RESPONSES
from agentic_skeleton.core.mock.constants.mock_plans import MOCK_PLANS
from agentic_skeleton.core.mock.constants.domain_knowledge import DOMAIN_KNOWLEDGE
from agentic_skeleton.core.mock.classifier import classify_request, classify_subtask


class MockResponseGenerator:
    """
    Generates simulated responses for different types of requests.
    """
    
    def __init__(self):
        """Initialize the mock response generator."""
        self.mock_responses = MOCK_RESPONSES
    
    def get_mock_response(self, user_request: str, topic: Optional[str] = None) -> str:
        """
        Generate a mock response based on the user request.
        
        Args:
            user_request: The user request text
            topic: Optional topic to use in the response
            
        Returns:
            A mock response string
        """
        # Extract topic from request if not provided
        if not topic:
            # Simple extraction - in production would use NLP to better extract topics
            words = user_request.split()
            # Extract potential topic phrases (nouns and noun phrases)
            topic_candidates = [w for w in words if len(w) > 3 and w.lower() not in 
                              ["about", "with", "that", "what", "when", "where", "which", "how"]]
            
            if topic_candidates:
                # Use the last longer phrase as topic (heuristic)
                topic = topic_candidates[-1]
            else:
                topic = "the requested topic"
        
        # Classify the request
        request_type = classify_request(user_request)
        
        # Select a response from the appropriate category
        if request_type in self.mock_responses:
            responses = self.mock_responses[request_type]
            selected_response = random.choice(responses)
        else:
            # Fallback to default response
            selected_response = random.choice(self.mock_responses["default"])
        
        # Format the response with topic
        formatted_response = selected_response.format(topic=topic)
        
        return formatted_response
    
    def get_specialized_response(self, 
                               user_request: str, 
                               domain: str, 
                               subtask_type: str, 
                               topic: str) -> str:
        """
        Generate a specialized domain response.
        
        Args:
            user_request: The user request text
            domain: The specialized domain
            subtask_type: The type of subtask
            topic: The topic for the response
            
        Returns:
            A domain-specialized mock response
        """
        # This would use domain-specific knowledge to generate a response
        # For now, fall back to the standard response
        return self.get_mock_response(user_request, topic)


def generate_mock_response(user_request: str, topic: Optional[str] = None) -> str:
    """
    Convenience function to generate a mock response.
    
    Args:
        user_request: The user request text
        topic: Optional topic to use in the response
        
    Returns:
        A mock response string
    """
    generator = MockResponseGenerator()
    return generator.get_mock_response(user_request, topic)


def generate_mock_plan_and_results(user_request: str) -> Tuple[List[str], List[Dict]]:
    """
    Generate a mock plan and results for a user request.
    
    Args:
        user_request: The user's request text
        
    Returns:
        Tuple containing (subtasks, results)
    """
    # Get appropriate plan based on request classification
    plan_type = classify_request(user_request)
    subtasks = MOCK_PLANS[plan_type]
    
    # Generate results for each subtask
    results = []
    for task in subtasks:
        # Get a dynamic response for this task
        response = get_mock_task_response(task)
        
        # Ensure we never have empty responses
        if not response or not response.strip() or "[MOCK]" not in response:
            # Generate a fallback response with task text embedded
            words = task.lower().split()
            topic = next((w for w in words if len(w) > 4 and w not in ["with", "from", "then", "than", "that", "this"]), "task")
            
            templates = MOCK_RESPONSES["default"]
            response = random.choice(templates).format(topic=topic)
            
        results.append({
            "subtask": task,
            "result": response
        })
        
    return subtasks, results


def get_mock_task_response(task: str) -> str:
    """
    Generate a relevant mock response for a task with improved topic extraction.
    
    Args:
        task: The task to generate a response for
        
    Returns:
        Mock response text
    """
    task_lower = task.lower()
    topic = None
    template_category = None
    
    # 1. Domain-specific response
    for domain_name, domain_data in DOMAIN_KNOWLEDGE.items():
        domain_match = any(keyword in task_lower for keyword in domain_data["keywords"])
        
        # Specific topic extraction for domain matching
        if domain_match:
            # Extract the matching keyword to use as the topic
            matching_keyword = next((kw for kw in domain_data["keywords"] if kw in task_lower), domain_data["keywords"][0])
            
            # Match subtask patterns
            for subtask_type, subtask_data in domain_data["subtasks"].items():
                subtask_match = any(pattern in task_lower for pattern in subtask_data["patterns"])
                if subtask_match:
                    # Generate dynamic values from variable functions
                    dynamic_values = {name: generator() for name, generator in subtask_data["variables"].items()}
                    dynamic_values["topic"] = matching_keyword
                    return subtask_data["template"].format(**dynamic_values)
            
            # If no specific subtask pattern matched but domain matched, 
            # find a suitable subtask pattern based on general terms in the task
            general_verbs = {
                "research": ["research", "analyze", "study", "evaluate", "assess", "compare", "investigate"],
                "implement": ["implement", "build", "create", "develop", "deploy", "construct", "integrate"],
                "design": ["design", "architect", "plan", "blueprint", "outline", "sketch", "wireframe"],
                "optimize": ["optimize", "improve", "enhance", "refine", "tune", "streamline", "refactor"],
                "evaluate": ["evaluate", "test", "verify", "validate", "measure", "assess"],
                "model": ["model", "train", "learn", "predict"],
                "data": ["data", "dataset", "preprocess", "clean", "prepare"]
            }
            
            # Find a matching general verb category
            for verb_category, verb_list in general_verbs.items():
                if any(verb in task_lower for verb in verb_list):
                    # See if this domain has this verb category
                    if verb_category in domain_data["subtasks"]:
                        subtask_data = domain_data["subtasks"][verb_category]
                        dynamic_values = {name: generator() for name, generator in subtask_data["variables"].items()}
                        dynamic_values["topic"] = matching_keyword
                        return subtask_data["template"].format(**dynamic_values)
                    # Otherwise, find the closest subtask category
                    else:
                        # Choose a suitable alternative subtask
                        fallback_subtask = next(iter(domain_data["subtasks"]))
                        subtask_data = domain_data["subtasks"][fallback_subtask]
                        dynamic_values = {name: generator() for name, generator in subtask_data["variables"].items()}
                        dynamic_values["topic"] = matching_keyword
                        return subtask_data["template"].format(**dynamic_values)
            
            # Last resort fallback - use the first subtask in the domain
            fallback_subtask = next(iter(domain_data["subtasks"]))
            subtask_data = domain_data["subtasks"][fallback_subtask]
            dynamic_values = {name: generator() for name, generator in subtask_data["variables"].items()}
            dynamic_values["topic"] = matching_keyword
            return subtask_data["template"].format(**dynamic_values)


    
    # 2. Fallback: tech keywords → categorize
    tech_patterns = [
        r"REST API", r"GraphQL API", r"machine learning", r"deep learning", 
        r"artificial intelligence", r"generative AI", r"large language model",
        r"data science", r"cloud computing", r"neural network", r"transformer model",
        r"user interface", r"UI/UX", r"database schema", r"microservices",
        r"web application", r"mobile app", r"DevOps pipeline", r"CI/CD",
        r"microservice architecture", r"serverless", r"kubernetes", r"data engineering",
        r"quantum computing", r"blockchain", r"edge computing", r"IoT devices",
        r"augmented reality", r"virtual reality", r"mixed reality", r"spatial computing"
    ]
    
    # Check for specific technical terms with higher priority
    for pattern in tech_patterns:
        match = re.search(pattern, task, re.IGNORECASE)
        if match:
            topic = match.group(0).lower()
            # Select appropriate template category based on the technical term
            if any(term in topic for term in ["intelligence", "learning", "neural", "model"]):
                template_category = "analyze"
            elif any(term in topic for term in ["api", "architecture", "engineering", "DevOps"]):
                template_category = "develop"
            elif any(term in topic for term in ["interface", "UI", "UX", "design"]):
                template_category = "design"
            else:
                template_category = "default"
            break
    
    # 3. Fallback: extract named entities
    if not topic:
        # Named entity patterns
        named_entity_patterns = [
            r'\b[A-Z][a-zA-Z]*([\s-][A-Z][a-zA-Z]*)+\b',  # Multi-word proper nouns
            r'\b[A-Z][a-zA-Z]*\s\d+(\.\d+)*\b',           # Product with version
            r'\b[A-Z][a-zA-Z]{2,}\b',                      # Single capitalized words
            r'\b[A-Z]{2,}\b'                               # Acronyms
        ]
        
        # Extract named entities
        for pattern in named_entity_patterns:
            matches = re.findall(pattern, task)
            if matches:
                if isinstance(matches[0], tuple):
                    entity = matches[0][0] if matches[0][0] else matches[0]
                else:
                    entity = matches[0]
                    
                topic = entity.strip().lower()
                template_category = "research"
                break
    
    # 4. Fallback: classify by verb or keyword
    if not template_category:
        if any(term in task_lower for term in ["data", "preprocess", "train", "model", "machine", "predict"]):
            template_category = "data-science"
        elif any(term in task_lower for term in ["research", "gather", "find", "collect"]):
            template_category = "research"
        elif any(term in task_lower for term in ["write", "draft", "blog", "article", "post"]):
            template_category = "write"
        elif any(term in task_lower for term in ["analyz", "analysis", "assess", "evaluate"]):
            template_category = "analyze"
        elif any(term in task_lower for term in ["develop", "implement", "code", "program"]):
            template_category = "develop"
        elif any(term in task_lower for term in ["design", "wireframe", "mockup", "sketch"]):
            template_category = "design"
        elif any(term in task_lower for term in ["format", "revise", "edit", "proofread"]):
            template_category = "default"
        else:
            template_category = "default"
    
    # Extract topic if not already determined
    if not topic:
        # Stopwords for filtering
        stopwords = [
            'with', 'from', 'then', 'than', 'that', 'this', 'these', 'those',
            'the', 'and', 'but', 'for', 'yet', 'so', 'or', 'nor', 'as', 'at',
            'by', 'for', 'in', 'to', 'is', 'on', 'been', 'was', 'were', 'of'
        ]
        
        # Get significant words from the task
        words = [word.lower() for word in re.findall(r'\b[a-zA-Z]{4,}\b', task) 
                if word.lower() not in stopwords]
        
        # Use the most significant word as topic (simple heuristic)
        topic = words[-1] if words else "task"
    
    # Ensure template_category is used for selecting the mock response
    # This was the key issue - template_category was set but not consistently used
    if template_category and template_category in MOCK_RESPONSES:
        templates = MOCK_RESPONSES[template_category]
    else:
        templates = MOCK_RESPONSES["default"]
    
    # Select a random template and format with topic
    template = random.choice(templates)
    
    # Apply topic with proper formatting and add mock identifier
    mock_response = template.format(topic=topic)
    if "[MOCK]" not in mock_response:
        mock_response = f"[MOCK] {mock_response}"
    
    return mock_response