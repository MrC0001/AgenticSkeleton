import os
import logging
import random
import re
from flask import Flask, request, jsonify
from dotenv import load_dotenv

try:
    from openai import AzureOpenAI
except ImportError:
    pass

# Setup
load_dotenv()
USE_MOCK = os.getenv("MOCK_RESPONSES", "true").lower() == "true"
AZURE_KEY = os.getenv("AZURE_OPENAI_KEY")
AZURE_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
MODEL_PLANNER = os.getenv("MODEL_PLANNER", "gpt-4")
MODEL_EXECUTOR = os.getenv("MODEL_EXECUTOR", "gpt-4")

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

# Mock plans for different request types
MOCK_PLANS = {
    "write": [
        "Research recent (2024-2025) sources and identify 3-5 key insights on the topic",
        "Develop a structured outline with main arguments and supporting evidence",
        "Write a first draft with compelling introduction, evidence-backed body sections, and actionable conclusion",
        "Edit for clarity, flow, and conciseness (aim for 15-20% word reduction)",
        "Format with proper headings, citations, and visual elements if applicable"
    ],
    "analyze": [
        "Collect comprehensive data from primary sources and organize into structured format",
        "Identify 3-5 key patterns, trends, or anomalies in the dataset",
        "Compare findings with industry benchmarks or historical performance metrics",
        "Generate actionable insights and recommendations based on analysis",
        "Create visualization dashboard with key metrics and supporting evidence"
    ],
    "develop": [
        "Define technical requirements and architecture based on user needs and performance criteria",
        "Design system components with clean interfaces, data models, and API specifications",
        "Implement core functionality with appropriate error handling and security practices",
        "Create automated test suite covering critical paths and edge cases",
        "Deploy solution with monitoring, documentation, and maintenance plan"
    ],
    "design": [
        "Research user needs, behaviors, and competitive landscape for the product",
        "Create information architecture and user flow diagrams for key journeys",
        "Develop wireframes and interactive prototypes for critical screens",
        "Design comprehensive UI components with accessibility and responsive considerations",
        "Create design system documentation with implementation guidelines"
    ],
    "data-science": [
        "Collect and preprocess data from relevant sources with quality assessment",
        "Perform exploratory data analysis to identify patterns and potential features",
        "Develop and train multiple models with cross-validation and hyperparameter tuning",
        "Evaluate model performance with appropriate metrics and business impact assessment",
        "Create deployable solution with monitoring for data and prediction drift"
    ],
    "default": [
        "Research the topic thoroughly and identify 3-5 key points",
        "Create a structured outline with logical flow",
        "Develop initial draft with comprehensive content",
        "Revise and optimize for clarity and effectiveness",
        "Finalize with proper formatting and quality assurance"
    ]
}

# Mock responses by task category
MOCK_RESPONSES = {
    "research": [
        "[MOCK] Research complete: Found 7 recent sources on {topic} (2024-2025). Key insights: 42% increase in enterprise adoption since Q1 2024, 3 emerging applications in healthcare (telemedicine, remote monitoring, predictive diagnostics), and integration with quantum computing starting Q3 2025.",
        "[MOCK] Completed research on {topic}. Analysis of 12 academic papers shows consensus on core principles (87% agreement) but significant divergence on implementation approaches (4 competing methodologies). Latest 2025 paper suggests hybrid approach combining methods A and C.",
        "[MOCK] Research findings on {topic}: Market size reached $3.8B in Q1 2025 (27% YoY growth), projected to reach $6.2B by 2027. Identified 3 enterprise solutions (market leaders) and 5 promising open-source alternatives with active development communities."
    ],
    "write": [
        "[MOCK] Draft completed for {topic}. The 850-word document covers historical context (2010-2023), current applications (2024-2025), and future trends (2026+). Includes 5 key points with supporting examples and 8 expert quotes from industry leaders.",
        "[MOCK] Created a comprehensive overview of {topic} (1,200 words). Introduction establishes business impact ($4.2B market by 2026), three main sections explore technical, economic, and social dimensions, with conclusion highlighting implementation roadmap for 2025-2026.",
        "[MOCK] Written content on {topic} now ready for review (950 words). Structured in problem-solution format with balanced perspective on advantages (7 identified benefits) and limitations (4 current challenges). Includes case studies from leading organizations implementing in 2025."
    ],
    "analyze": [
        "[MOCK] Analysis shows {topic} has 3 distinct patterns: increasing enterprise adoption (42% YoY in 2025), shifting demographics (technical professionals +23%, executives +15%), and evolving use cases (productivity +40%, security enhancements +68%, entertainment -12%).",
        "[MOCK] Completed comparative analysis of {topic} technologies. Solution A outperforms in speed (32% faster) and resource usage (18% lower), while Solution B excels in accuracy (17% fewer errors) and compatibility (supports 8 more platforms). ROI analysis shows Solution B superior for enterprise deployment.",
        "[MOCK] Trend analysis for {topic}: Identified cyclical pattern with 6-month periodicity. Peak performance in Q2 and Q4 (32% and 28% above baseline). Three anomalies detected in 2024-2025 data, correlating with market disruptions. Recommend quarterly review cycle with automated anomaly detection."
    ],
    "develop": [
        "[MOCK] Implemented core functionality for {topic}. Created 6 microservices with clean domain boundaries, 87% test coverage (unit + integration), and automated CI/CD pipeline. Performance benchmarks show 250ms average response time under simulated load of 1000 concurrent users.",
        "[MOCK] Architecture design for {topic} complete. Includes infrastructure-as-code templates, serverless function workflows, and real-time data processing pipeline. Scalability tested to 10M daily active users with 99.99% uptime projections and disaster recovery protocol.",
        "[MOCK] Finished {topic} implementation with GraphQL API (32 queries, 18 mutations). Added OAuth 2.0 authentication, rate limiting (5000 req/min), and comprehensive error handling with structured responses. Interactive documentation deployed with 28 executable examples."
    ],
    "design": [
        "[MOCK] Created wireframes for {topic} interface. Includes 8 key screens with responsive layouts for desktop, tablet, and mobile. Accessibility review complete (WCAG 2.2 AAA compliance) with dark mode support and voice navigation integration.",
        "[MOCK] Completed user flow diagrams for {topic}. Optimized task completion from 12 steps to 5 steps for core journeys. Added personalization pathways based on user behavior and accessibility preferences. Compliance with 2025 EU Digital Services Act verified.",
        "[MOCK] Design system for {topic} now ready with 42 reusable components, neural-adaptive color system, typography optimized for 8 languages, and motion design principles supporting spatial computing environments. Component library published with Figma and code integration."
    ],
    "data-science": [
        "[MOCK] Data preprocessing complete for {topic}: Cleaned 32,450 records (removed duplicates, handled missing values), feature engineering added 8 derived variables, and dimensional reduction applied using PCA maintaining 92% variance with 6 components.",
        "[MOCK] Model evaluation results for {topic}: Ensemble approach outperformed baseline by 37%. Final model combines gradient boosting (65% weight) and transformer architecture (35% weight) with F1-score of 0.92 and latency under 100ms on standard hardware.",
        "[MOCK] Deployed {topic} prediction pipeline with real-time inferencing capability (handling 2,000 req/sec). Implementation includes bias monitoring dashboard, data drift detection with automated alerts, and A/B testing framework for continuous improvement."
    ],
    "default": [
        "[MOCK] Completed the requested task for {topic}. Results ready for review and next steps. Documentation included with implementation details and recommendations for future enhancements.",
        "[MOCK] Task finished successfully. The {topic} has been processed according to specifications with all acceptance criteria met. Performance metrics show 35% improvement over baseline.",
        "[MOCK] Completed work on {topic}. Deliverables include comprehensive documentation, implementation code, and validation tests. Security audit passed with zero critical findings."
    ]
}

# Initialize Azure client
azure_client = None
if not USE_MOCK:
    try:
        if not AZURE_KEY or not AZURE_ENDPOINT:
            print("Warning: Azure credentials missing. Using mock mode.")
            USE_MOCK = True
        else:
            azure_client = AzureOpenAI(
                api_key=AZURE_KEY,
                azure_endpoint=AZURE_ENDPOINT,
                api_version="2025-04-20"
            )
            print("Azure OpenAI client initialized")
    except Exception as e:
        print(f"Azure client initialization failed: {e}")
        print("Using mock mode instead")
        USE_MOCK = True

app = Flask(__name__)


def get_mock_task_response(task):
    """Generate a relevant mock response for a task with improved topic extraction"""
    # List of technical patterns
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
            return match.group(0).lower()
    
    # Stopwords list
    stopwords = [
        'with', 'from', 'then', 'than', 'that', 'this', 'these', 'those',
        'and', 'but', 'for', 'nor', 'yet', 'the', 'all', 'any', 'each', 
        'proper', 'just', 'very', 'such', 'will', 'shall', 'should', 'would',
        'high', 'low', 'many', 'much', 'have', 'most', 'what', 'when', 'how',
        'where', 'which', 'best', 'better', 'good', 'great', 'more', 'less',
        'who', 'whom', 'whose', 'they', 'them', 'their', 'some', 'other', 'about'
    ]
    
    words = [w.lower() for w in task.split()]
    
    # Look for proper nouns
    named_entity_patterns = [
        # Company or product name pattern
        r'\b[A-Z][a-zA-Z]*([\s-][A-Z][a-zA-Z]*)+\b',
        # Technology with version pattern
        r'\b[A-Z][a-zA-Z]*\s\d+(\.\d+)*\b',
        # Single capitalized words (likely proper nouns)
        r'\b[A-Z][a-zA-Z]{2,}\b'
    ]
    
    for pattern in named_entity_patterns:
        matches = re.findall(pattern, task)
        if matches:
            return matches[0].lower()
    
    priority_words = [
        # Modern tech terms
        "LLM", "GPT", "prompt engineering", "vector database", "RAG",
        "multimodal", "zero-shot", "few-shot", "fine-tuning", "embedding",
        # Standard tech terms
        "API", "REST", "GraphQL", "SQL", "NoSQL", "database", "server",
        "client", "website", "application", "function", "algorithm", "system",
        "platform", "framework", "architecture", "code", "data", "model",
        "analysis", "design", "interface", "report", "visualization", "dashboard",
        "authentication", "authorization", "deployment", "testing", "monitoring"
    ]
    
    # Check for priority terms (case-insensitive)
    for word in priority_words:
        if any(w.lower() == word.lower() for w in words):
            return word.lower()
        
    # Extract noun phrases
    noun_phrases = []
    for i in range(len(words) - 1):
        # Adjective + Noun pattern
        if (len(words[i]) > 3 and len(words[i+1]) > 3 and
            words[i] not in stopwords and words[i+1] not in stopwords):
            noun_phrases.append(f"{words[i]} {words[i+1]}")
    
    if noun_phrases:
        return noun_phrases[-1]  # Use the last noun phrase
    
    # Filter out stopwords and short words, prioritize nouns and technical terms
    potential_topics = [w for w in words if len(w) > 3 and w not in stopwords]
    
    if len(potential_topics) >= 2:
        return potential_topics[-2]  # Second-to-last word is often meaningful
    
    # Fallback topic
    topic = (random.choice(potential_topics) if potential_topics 
             else words[-1] if words else "task")
    
    task_lower = task.lower()
    
    if any(term in task_lower for term in ["data preprocess", "clean data", "feature engineer", 
                                          "train model", "machine learn", "deep learn", "neural", 
                                          "predict", "classif", "cluster", "regress"]):
        templates = MOCK_RESPONSES["data-science"]
    elif any(term in task_lower for term in ["research", "gather", "find", "collect", 
                                            "source", "information", "background"]):
        templates = MOCK_RESPONSES["research"]
    elif any(term in task_lower for term in ["write", "draft", "blog", "article", "post", 
                                            "essay", "content", "document", "report"]):
        templates = MOCK_RESPONSES["write"]
    elif any(term in task_lower for term in ["analyz", "analysis", "assess", "evaluate", 
                                            "review", "compar", "trend", "pattern", "insight"]):
        templates = MOCK_RESPONSES["analyze"]
    elif any(term in task_lower for term in ["develop", "implement", "code", "program", 
                                            "build", "construct", "function", "algorithm"]):
        templates = MOCK_RESPONSES["develop"]
    elif any(term in task_lower for term in ["design", "wireframe", "mockup", "sketch", 
                                            "prototype", "interface", "ui", "ux"]):
        templates = MOCK_RESPONSES["design"]
    elif any(term in task_lower for term in ["format", "revise", "edit", "proofread", 
                                            "style", "layout", "structure"]):
        templates = MOCK_RESPONSES["format"]
    else:
        templates = MOCK_RESPONSES["default"]
    
    # Return formatted response
    return random.choice(templates).format(topic=topic)


def call_azure_openai(model, prompt):
    """Call Azure OpenAI API"""
    try:
        response = azure_client.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": prompt}],
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Azure OpenAI API call failed: {e}")
        return f"Error: {str(e)}"


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "mode": "mock" if USE_MOCK else "azure"
    })


@app.route("/run-agent", methods=["POST"])
def run_agent():
    """Main endpoint for the agent"""
    user_req = request.get_json().get("request", "")
    
    if USE_MOCK:
        # Enhanced request classification with more specific categories
        request_lower = user_req.lower()
        
        # Data science tasks
        if any(term in request_lower for term in [
            "machine learning", "ml model", "predictive model", "data mining", 
            "train model", "neural network", "clustering", "classification algorithm",
            "regression", "feature engineering", "data preprocessing", "dataset"
        ]):
            plan_type = "data-science"
            
        # Writing tasks    
        elif any(term in request_lower for term in [
            "write", "draft", "blog", "article", "post", "essay", "content", 
            "copywriting", "script", "document", "report", "whitepaper"
        ]):
            plan_type = "write"
            
        # Analysis tasks    
        elif any(term in request_lower for term in [
            "analyze", "analysis", "evaluate", "assess", "review", "study", 
            "research", "compare", "investigate", "examine", "trends", "patterns"
        ]):
            plan_type = "analyze"
            
        # Development tasks    
        elif any(term in request_lower for term in [
            "develop", "build", "create", "implement", "code", "program", 
            "app", "application", "api", "website", "backend", "frontend", 
            "software", "function", "class", "module", "database"
        ]):
            plan_type = "develop"
            
        # Design tasks    
        elif any(term in request_lower for term in [
            "design", "wireframe", "sketch", "mock up", "prototype", "ui", "ux",
            "user interface", "user experience", "layout", "visual", "graphics"
        ]):
            plan_type = "design"
            
        # Default fallback    
        else:
            plan_type = "default"
            
        # Get plan and generate results
        subtasks = MOCK_PLANS[plan_type]
        results = []
        for task in subtasks:
            results.append({
                "subtask": task,
                "result": get_mock_task_response(task)
            })
    else:
        try:
            # Generate plan
            planner_prompt = PLANNER_TEMPLATE.format(user_request=user_req)
            plan_text = call_azure_openai(MODEL_PLANNER, planner_prompt)
            
            # Extract tasks from numbered list
            subtasks = [
                line.partition(" ")[2].strip()
                for line in plan_text.splitlines()
                if line and line[0].isdigit()
            ]
            
            # Execute each task
            results = []
            for task in subtasks:
                executor_prompt = EXECUTOR_TEMPLATE.format(subtask=task)
                result = call_azure_openai(MODEL_EXECUTOR, executor_prompt)
                results.append({
                    "subtask": task,
                    "result": result
                })
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    return jsonify({"plan": subtasks, "results": results})


if __name__ == "__main__":
    print(f"Running in {'MOCK' if USE_MOCK else 'AZURE'} mode")
    app.run(host="0.0.0.0", port=8000)