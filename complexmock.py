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
    "You are a task planning assistant.\n"
    "Decompose the following user request into a numbered list of discrete subtasks:\n\n"
    "\"{user_request}\"\n\n"
    "1."
)

EXECUTOR_TEMPLATE = (
    "You are an execution assistant.\n"
    "Perform the subtask below, and respond with just the result:\n\n"
    "Subtask: {subtask}"
)

# Mock plans for different request types
MOCK_PLANS = {
    "write": [
        "Research the topic thoroughly",
        "Create an outline with key points",
        "Write the first draft with introduction, body, and conclusion",
        "Revise and edit the content for clarity and flow",
        "Format according to requirements and add citations"
    ],
    "analyze": [
        "Gather relevant data about the subject",
        "Identify key patterns and trends in the data",
        "Perform comparative analysis with similar cases",
        "Formulate insights based on the analysis",
        "Create visualizations to support findings"
    ],
    "develop": [
        "Define technical requirements and specifications",
        "Design the high-level architecture",
        "Implement core functionality with proper error handling",
        "Create tests to verify correct behavior",
        "Document the implementation for future reference"
    ],
    "default": [
        "Research the topic thoroughly",
        "Create an outline",
        "Write the first draft",
        "Revise and edit the content",
        "Format according to requirements"
    ]
}

# Mock responses by task category
MOCK_RESPONSES = {
    "research": [
        "[MOCK] Research complete: Found 7 recent sources on {topic}. Key insights include growing adoption in industry, significant improvements in 2024, and new applications in healthcare.",
        "[MOCK] Completed research on {topic}. Analysis of 12 academic papers shows consensus on core principles but disagreement on implementation approaches.",
        "[MOCK] Research findings on {topic}: Market size of $3.2B in 2024, projected growth of 27% annually. Main competitors include 3 enterprise solutions and 2 open-source alternatives."
    ],
    "write": [
        "[MOCK] Draft completed for {topic}. The 750-word document covers historical context, current applications, and future trends. Includes 5 key points with supporting examples.",
        "[MOCK] Created a comprehensive overview of {topic} with introduction establishing importance, three main sections exploring key dimensions, and conclusion highlighting implications.",
        "[MOCK] Written content on {topic} now ready for review. Structured as problem-solution format with balanced perspective on advantages and limitations."
    ],
    "analyze": [
        "[MOCK] Analysis shows {topic} has 3 distinct patterns: increasing adoption (27% YoY), shifting demographics (younger users +15%), and evolving use cases (productivity +40%, entertainment -12%).",
        "[MOCK] Completed comparative analysis of {topic}. Method A outperforms in speed (32% faster), while Method B excels in accuracy (17% fewer errors). Cost analysis suggests Method B provides better ROI.",
        "[MOCK] Trend analysis for {topic}: Identified cyclical pattern with 6-month periodicity. Peak performance in Q2 and Q4. Three anomalies detected in historical data requiring further investigation."
    ],
    "develop": [
        "[MOCK] Implemented core functionality for {topic}. Created 4 classes with proper inheritance structure. All unit tests passing with 92% code coverage.",
        "[MOCK] Architecture design for {topic} complete. Includes data flow diagrams, component interfaces, and third-party integration points. Scalability considerations documented.",
        "[MOCK] Finished {topic} implementation with RESTful API endpoints. Added authentication, rate limiting, and comprehensive error handling. Sample requests included in documentation."
    ],
    "design": [
        "[MOCK] Created wireframes for {topic} interface. Includes 5 key screens with responsive layouts and accessibility considerations.",
        "[MOCK] Completed user flow diagrams for {topic}. Optimized for minimal steps to complete common tasks, with special attention to error recovery paths.",
        "[MOCK] Design system for {topic} now ready with component library, color palette, typography guidelines, and animation principles."
    ],
    "format": [
        "[MOCK] Formatting complete for {topic}. Applied consistent styling, added proper citations, and ensured compliance with requested guidelines.",
        "[MOCK] Finalized document structure for {topic} with table of contents, section numbering, and properly formatted references.",
        "[MOCK] Completed formatting with enhanced readability: proper headings, bullet points for key items, and consistent paragraph structure."
    ],
    "default": [
        "[MOCK] Completed the requested task for {topic}. Results ready for next steps.",
        "[MOCK] Task finished successfully. The {topic} has been processed according to requirements.",
        "[MOCK] Completed work on {topic}. All specified criteria have been met."
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
    """Generate a relevant mock response for a task"""
    # Try to extract a meaningful topic from the task
    tech_patterns = [
        r"REST API", r"machine learning", r"artificial intelligence",
        r"data science", r"cloud computing", r"neural network",
        r"user interface", r"database schema", r"web application",
        r"mobile app", r"DevOps pipeline", r"CI/CD",
        r"microservice architecture"
    ]
    
    # Check for technical terms
    for pattern in tech_patterns:
        match = re.search(pattern, task, re.IGNORECASE)
        if match:
            return match.group(0).lower()
    
    # Common words to filter out
    stopwords = [
        'with', 'from', 'then', 'than', 'that', 'this', 'these', 'those',
        'and', 'but', 'for', 'nor', 'yet', 'the', 'all', 'any', 
        'proper', 'just', 'very', 'such', 'will', 'shall', 'should',
        'high', 'low', 'many', 'much', 'have', 'most', 'what', 'when',
        'where', 'which', 'best', 'better', 'good', 'great'
    ]
    
    words = [w.lower() for w in task.split()]
    
    # Look for proper nouns
    capitalized_words = re.findall(r'\b[A-Z][a-z]+ [A-Z][a-z]+\b', task)
    if capitalized_words:
        return capitalized_words[0].lower()
    
    # Important technical terms
    priority_words = [
        "API", "REST", "GraphQL", "database", "server", "client", "website",
        "application", "function", "algorithm", "system", "platform",
        "framework", "architecture", "code", "data", "model", "analysis",
        "design", "interface", "report", "visualization", "dashboard",
        "authentication", "authorization", "deployment", "testing"
    ]
    
    # Check for priority terms
    for word in priority_words:
        if word.lower() in [w.lower() for w in words]:
            return word.lower()
    
    # Filter out stopwords and short words
    potential_topics = [w for w in words if len(w) > 3 and w not in stopwords]
    
    if len(potential_topics) >= 2:
        return potential_topics[-2]
    
    # Fallback
    topic = random.choice(potential_topics) if potential_topics else words[-1] if words else "task"
    
    # Select response template based on task type
    task_lower = task.lower()
    if "research" in task_lower or "gather" in task_lower or "find" in task_lower:
        templates = MOCK_RESPONSES["research"]
    elif "write" in task_lower or "draft" in task_lower or "create" in task_lower:
        templates = MOCK_RESPONSES["write"]
    elif "analyze" in task_lower or "analysis" in task_lower or "identify" in task_lower:
        templates = MOCK_RESPONSES["analyze"]
    elif "develop" in task_lower or "implement" in task_lower or "code" in task_lower:
        templates = MOCK_RESPONSES["develop"]
    elif "design" in task_lower or "wireframe" in task_lower or "sketch" in task_lower:
        templates = MOCK_RESPONSES["design"]
    elif "format" in task_lower or "revise" in task_lower or "edit" in task_lower:
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
        # Classify request type
        request_lower = user_req.lower()
        
        if any(kw in request_lower for kw in ["write", "draft", "blog", "article", "post", "essay"]):
            plan_type = "write"
        elif any(kw in request_lower for kw in ["analyze", "analysis", "evaluate", "assess", "review", "study", "research"]):
            plan_type = "analyze"
        elif any(kw in request_lower for kw in ["develop", "build", "create", "implement", "code", "program", "app", "application", "api"]):
            plan_type = "develop"
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