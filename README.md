# AgenticSkeleton

A simple Flask-based AI agent skeleton with both mock responses and Azure OpenAI integration.

## Quick Start

```bash
# Clone repository
git clone https://github.com/MrC0001/AgenticSkeleton.git
cd AgenticSkeleton

# Set up environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac OR .venv\Scripts\activate for Windows
pip install -r requirements.txt
cp .env.example .env

# Start the server
python -m agentic_skeleton

# In another terminal, test the API
python -m agentic_skeleton.tests.test_api
```

## Project Structure

```
agentic_skeleton/
├── __init__.py         # Package initialization
├── __main__.py         # Main entry point
├── api/                # API endpoints
│   └── endpoints.py    # Flask routes
├── config/             # Configuration
│   └── settings.py     # Application settings
├── core/               # Core functionality
│   ├── azure_core.py   # Azure OpenAI integration
│   ├── mock_core.py    # Mock response generation
│   ├── azure/          # Azure OpenAI components
│   │   ├── classifier.py  # Request classification
│   │   ├── client.py      # OpenAI client wrapper
│   │   ├── enhancer.py    # Response enhancement
│   │   ├── generator.py   # Response generation
│   │   └── constants/     # Azure-specific constants
│   └── mock/           # Mock components
│       ├── classifier.py  # Request classification
│       ├── generator.py   # Response generation
│       └── constants/     # Mock response templates
├── misc/               # Miscellaneous utilities
│   ├── simple_primer.py      # Simplified version of the app
│   └── simple_primer_test.py # Test client for the simplified app
├── tests/              # Test suite
│   ├── test_api.py           # API tests
│   ├── test_azure_integration.py  # Azure integration tests
│   ├── test_azure_unit.py    # Azure unit tests
│   ├── test_integration.py   # Integration tests
│   └── test_unit.py          # Unit tests
└── utils/              # Utility functions
    └── helpers.py      # Helper functions
```

## Configuration

By default, the application runs in mock mode which requires no API keys. To switch to Azure OpenAI:

1. Edit your `.env` file:
   ```
   # Change this to false for Azure mode
   MOCK_RESPONSES=true
   
   # Add your Azure OpenAI credentials
   AZURE_OPENAI_KEY=your-key-here
   AZURE_OPENAI_ENDPOINT=your-endpoint-here
   ```

2. Make sure the `openai` dependency is installed:
   ```
   pip install openai
   ```

## Usage

### Mock Mode (Default)

By default, the application runs in mock mode, which doesn't require any Azure credentials.

```bash
# Ensure MOCK_RESPONSES=true in .env file
python -m agentic_skeleton
```

### Azure OpenAI Mode

To use with Azure OpenAI:

1. Set `MOCK_RESPONSES=false` in your `.env` file
2. Add your Azure OpenAI credentials:
   - `AZURE_OPENAI_KEY`
   - `AZURE_OPENAI_ENDPOINT`
3. Run the application

## Domain Specialization

The system is capable of recognizing and adapting to different domains like:

- AI/Machine Learning
- Healthcare Technology
- Cloud Computing
- Data Analysis
- Development
- Writing Tasks

Each domain has specialized templates and responses that ensure relevant information is included in the generated content.

## Simplified Version (Primer)

The project includes a simplified version in the `agentic_skeleton/misc/` directory:

- `simple_primer.py`: A streamlined version of the main application
- `simple_primer_test.py`: A test client for the simplified app

To run the simplified version:

```bash
# Start the server
python -m agentic_skeleton.misc.simple_primer

# In another terminal, test the API
python -m agentic_skeleton.misc.simple_primer_test
```

Example output from the simple primer test:
```
=============== Testing Agentic Skeleton API ===============
✅ Server is healthy (Mode: mock)
🔄 Testing request: "Write a short blog post about AI agents"
  ├─ Sending request to http://localhost:8000/run-agent
  ├─ Response time: 79ms
  └─ Plan received with 5 steps
    
📊 Response Summary:
┌─────────────────────────────────┬─────────────────────────────────────┐
│ Subtask                         │ Result                              │
├─────────────────────────────────┼─────────────────────────────────────┤
│ Research the topic thoroughly   │ Found multiple sources confirming   │
│                                 │ that AI agents are transforming...  │
├─────────────────────────────────┼─────────────────────────────────────┤
│ Create an outline               │ Here's a concise outline for the    │
│                                 │ blog post about AI agents...        │
├─────────────────────────────────┼─────────────────────────────────────┤
│ ... more results ...            │ ...                                 │
└─────────────────────────────────┴─────────────────────────────────────┘
```

## Demo Script

You can quickly test the system's capabilities using the included demo script:

```bash
# Activate the virtual environment if not already activated
source .venv/bin/activate

# Make the demo script executable
chmod +x demo.sh

# Run the demo
./demo.sh
```

This will showcase different domain capabilities with nicely formatted output:

```
============================================
    AgenticSkeleton API Demonstration      
============================================

>> AI/ML Domain Example
Request: Design a machine learning system for predictive maintenance in manufacturing

Plan:
  1. Define system requirements and objectives
  2. Collect relevant data sources for training
  3. Preprocess and clean the data
  4. Select appropriate machine learning algorithms
  5. Train and validate the model
  6. Implement monitoring and feedback loops

Results:
  Task 1: Define system requirements and objectives
    [MOCK] System requirements for predictive maintenance in manufacturing should include real-time monitoring capabilities, integration with...

  Task 2: Collect relevant data sources for training
    [MOCK] For predictive maintenance, collected relevant data from sensors including vibration data, temperature readings, acoustic emissions...

  ... more results ...
```

## API Usage

### Health Check
```
GET /health
```
Response:
```json
{
  "status": "healthy",
  "mode": "mock",  // or "azure" in production mode
  "version": "1.0.0"
}
```

### Run Agent
```
POST /run-agent
Body: {"request": "your user request here"}
```

Response:
```json
{
  "plan": [
    "Research the topic thoroughly",
    "Create an outline",
    "Write the first draft",
    "Revise and edit the content",
    "Format according to requirements"
  ],
  "results": [
    {
      "subtask": "Research the topic thoroughly",
      "result": "Found multiple sources confirming that thoroughly has significant implications."
    },
    // Additional results...
  ]
}
```

## Testing

The project includes several testing approaches with rich, colored output for better visualization of test results.

### Running All Tests

```bash
# Run all tests
python -m pytest agentic_skeleton/tests
```

### Running Specific Tests

```bash
# Unit tests
python -m pytest agentic_skeleton/tests/test_unit.py

# Integration tests
python -m pytest agentic_skeleton/tests/test_integration.py

# API tests
python -m pytest agentic_skeleton/tests/test_api.py

# Azure tests (when in Azure mode)
python -m pytest agentic_skeleton/tests/test_azure_unit.py
python -m pytest agentic_skeleton/tests/test_azure_integration.py
```

### Rich Test Output Examples

#### Unit Tests Output
```
🤖 Unit Tests
==============================================
Running in MOCK mode

Testing health endpoint...

Health endpoint response:
  {
    "status": "healthy",
    "mode": "mock",
    "version": "1.0.0"
  }
✅ Health endpoint verified

Testing error handling with malformed JSON...

Error response:
  {
    "error": "Invalid JSON input"
  }

Testing error handling with missing request field...

Error response:
  {
    "error": "Missing 'request' field in JSON input"
  }

Testing task classification...

Format: [Query] → [Detected Type] (Expected Type)
  ✓ [Write a blog post about AI] → [write] (write)
  ✓ [Analyze market trends in renewable energy] → [analyze] (analyze)
  ✓ [Develop a Python API for data processing] → [develop] (develop)
  ✓ [Design a user interface for a mobile app] → [design] (design)
  ✓ [Train a machine learning model for NLP] → [data-science] (data-science)

Testing topic extraction for technical terms...

Input: Implement a REST API for user authentication
Result: [MOCK] Based on my research on rest api technology, the key considerations for implementing user authentication...
Extracted term: rest api

Input: Design a neural network architecture for image recognition
Result: [MOCK] After researching neural network architectures for image recognition, I recommend considering convolutional...
Extracted term: neural network

// ... more test output ...

📊 Test Run Summary:
──────────────────────────────────────────────────
  Total tests: 15
  Passed: 15
  Failed: 0
  Errors: 0
  Skipped: 0
  Success rate: 100.0%
```

#### Integration Tests Output
```
🧪 Integration Tests
==============================================
Running in MOCK mode

Testing complete workflow for writing task

Calling run-agent endpoint...

Generated plan:
  1. Research machine learning applications in healthcare
  2. Create an outline for the blog post
  3. Write an engaging introduction
  4. Develop the main content sections
  5. Create a compelling conclusion

Results:
  Task 1: Research machine learning applications in healthcare
    Result sample: [MOCK] Research findings indicate that machine learning has transformative applications in healthcare...
  Task 2: Create an outline for the blog post
    Result sample: [MOCK] The outline for the blog post on machine learning applications in healthcare includes the following...
  Task 3: Write an engaging introduction
    Result sample: [MOCK] Introduction: The healthcare industry stands on the brink of a technological revolution, with machine...
  Task 4: Develop the main content sections
    Result sample: [MOCK] Main Content: First, let's explore diagnostic applications. Machine learning algorithms have demonst...
  Task 5: Create a compelling conclusion
    Result sample: [MOCK] Conclusion: As we've explored, machine learning applications in healthcare represent a paradigm shif...

✓ Successfully generated ML-focused writing task response

Testing complete workflow for analysis task

Calling run-agent endpoint...

// ... more test output ...

📊 Test Run Summary:
──────────────────────────────────────────────────
  Total tests: 5
  Passed: 5
  Failed: 0
  Errors: 0
  Skipped: 0
  Success rate: 100.0%
```

#### API Tests Output
```
=============== Testing API Endpoints ===============
✅ Health endpoint - PASS
  Mode: mock, Status: healthy

✅ Run-agent endpoint - PASS
  Plan generated with 5 steps
  Results generated for all subtasks

✅ Error handling - PASS
  Invalid requests properly rejected with 400 status

Test summary: 3 passed, 0 failed
```

#### Azure Unit Tests Output
```
🧪 Azure Unit Tests
==============================================
Running in AZURE mode

Testing Azure client initialization...
✅ Azure client initialized successfully

Testing Azure client initialization with invalid credentials...
✅ Error handling worked as expected

Testing completion generation...

Generated completion:
  "This is a test response"
✅ Completion generation verified

Testing call_azure_openai helper function...

Azure API call result:
  "This is a test response"
✅ Azure API call verified

Testing Azure API call with invalid configuration...

Error response:
  "Configuration validation failed"
✅ Validation failure handling verified

Testing writing request classification...

Format: [Query] → [Detected Type]
  ✓ [Write a blog post about AI] → [write]
  ✓ [Draft a technical whitepaper on blockchain] → [write]
  ✓ [Create content for our company website] → [write]
  ✓ [Compose an email newsletter about recent events] → [write]
✅ Writing request classification verified

// ... more test output ...

📊 Test Run Summary:
──────────────────────────────────────────────────
  Total tests: 20
  Passed: 20
  Failed: 0
  Errors: 0
  Skipped: 0
  Success rate: 100.0%
```

#### Azure Integration Tests Output
```
🧪 Azure Integration Tests
==============================================
Running in AZURE mode

Testing request classification with various task types...

Format: [Query] → [Detected Type] (Expected Type)
  ✓ [Train a machine learning model for customer churn] → [data-science] (data-science)
  ✓ [Analyze market trends in renewable energy] → [analyze] (analyze)
  ✓ [Develop a REST API for user authentication] → [develop] (develop)
  ✓ [Design a user interface for a mobile app] → [design] (design)
  ✓ [Write a blog post about sustainable technology] → [write] (write)

Testing complex, multi-domain request classification...

Complex request:
  "Create a comprehensive end-to-end platform for analyzing customer data, predicting churn and automatically generating personalized retention emails"

Classification result:
  ✓ [data-science]
✅ Request classification verified for all task types

Testing domain specialization detection...

Cloud computing request:
  "Design a multi-region cloud deployment architecture for our application"
Detected domain:
  Name: cloud_computing
  Preferred category: develop
✅ Cloud computing domain detection verified

AI/ML request:
  "Develop a generative AI model for creating marketing content"
Detected domain:
  Name: ai_ml
  Preferred category: data-science
✅ AI/ML domain detection verified

Healthcare request:
  "Build a telehealth platform for remote patient monitoring"
Detected domain:
  Name: healthcare_tech
  Preferred category: analyze
✅ Healthcare tech domain detection verified

Generic request:
  "Write a blog post about company culture"
Detected domain:
  No specific domain detected
✅ Generic domain detection verified

Testing subtask classification...

Basic subtask classification:
  ✓ [Research recent advances in natural language processing] → [research]
  ✓ [Implement a user authentication system] → [implement]
  ✓ [Design a database schema for user profiles] → [design]
  ✓ [Test the API endpoints for performance] → [evaluate]
  ✓ [Document the system architecture] → [document]

AI/ML domain subtask classification:
  ✓ [Gather and preprocess training data] → [data]
  ✓ [Train the classification model] → [model]
  ✓ [Deploy the model as a prediction API] → [deploy]

Cloud computing domain subtask classification:
  ✓ [Research cost optimization strategies] → [research]
  ✓ [Implement auto-scaling policies] → [implement]
  ✓ [Optimize resource allocation] → [optimize]
✅ Subtask classification verified for all types

Testing prompt enhancement capabilities...

Basic prompt enhancement:
  Original prompt: "Generate a response for the following task:"
  User request: "Build a machine learning model for customer churn prediction"
  Category: "data-science"
  Enhanced prompt length: 161 chars

Domain-specific prompt enhancement:
  Original prompt: "Generate a response for the following task:"
  User request: "Train a neural network for image recognition"
  Domain: "ai_ml"
  Enhanced prompt length: 362 chars

Subtask prompt enhancement:
  Original prompt: "Generate a response for the following task:"
  User request: "Train a neural network for image recognition"
  Subtask: "Preprocess and augment the image dataset"
  Subtask type: "data"
  Enhanced prompt length: 471 chars
✅ Prompt enhancement verified for all scenarios

Testing fallback plan generation...

AI/ML domain fallback plan:
  1. Define the problem statement and analysis objectives
  2. Collect and prepare the dataset for analysis
  3. Perform exploratory data analysis to understand patterns
  4. Engineer features and preprocess data for modeling
  5. Train and evaluate machine learning models
  6. Deploy the model and create a system for predictions

Writing category fallback plan:
  1. Research the topic and gather relevant information
  2. Create an outline with key points and structure
  3. Draft the initial content following the outline
  4. Review and revise the content for clarity and coherence
  5. Edit for grammar, style, and formatting
  6. Prepare the final version with any necessary citations

Default fallback plan:
  1. Research the topic and gather relevant information
  2. Analyze the key components and requirements
  3. Develop an initial solution or approach
  4. Test and validate the solution
  5. Refine and optimize based on testing results
  6. Prepare final documentation and delivery
✅ Fallback plan generation verified for all scenarios

Testing plan generation with Azure...

User request:
  "Create a chatbot with natural language processing capabilities"

Generated plan:
  1. Research recent advances in natural language processing
  2. Analyze the requirements for the chatbot system
  3. Design the conversation flow and user interactions
  4. Implement the core NLP processing pipeline
  5. Test the chatbot with sample user interactions
  6. Document the system and create user guidelines
✅ Plan generation with Azure verified

Testing subtask execution with Azure...

User request:
  "Create an NLP chatbot"

Subtasks to execute:
  1. Research NLP techniques for intent recognition
  2. Design an architecture for the chatbot system

Results:
  Task 1: Research NLP techniques for intent recognition
    Type: research
    Result sample: Result for subtask 1: Based on recent research in NLP, the most effective techniques for intent reco...
  Task 2: Design an architecture for the chatbot system
    Type: design
    Result sample: Result for subtask 2: The recommended architecture for the chatbot system includes a natural languag...
✅ Subtask execution with Azure verified

Testing complete workflow with Azure integration

Calling run-agent endpoint in Azure mode...

Generated plan:
  1. Research recent AI applications in healthcare
  2. Analyze medical data processing techniques
  3. Explore diagnostic use cases
  4. Evaluate machine learning models for patient care
  5. Examine ethical considerations

Results:
  Task 1: Research recent AI applications in healthcare
    Result sample: Result 1 for healthcare AI research...
  Task 2: Analyze medical data processing techniques
    Result sample: Result 2 for medical data analysis...
  Task 3: Explore diagnostic use cases
    Result sample: Result 3 for diagnostic applications...
  Task 4: Evaluate machine learning models for patient care
    Result sample: Result 4 for patient care models...
  Task 5: Examine ethical considerations
    Result sample: Result 5 for ethical considerations...
✓ Successfully generated healthcare AI analysis with Azure integration

📊 Test Run Summary:
──────────────────────────────────────────────────
  Total tests: 8
  Passed: 8
  Failed: 0
  Errors: 0
  Skipped: 0
  Success rate: 100.0%
```

### Test Output Formatting Features

All tests now include rich output formatting with:

- ✅ Colorized test results with pass/fail indicators
- 🟢 Green checkmarks for passed tests and 🔴 red X's for failed tests
- 📋 Detailed test plans and results shown in an organized format
- 🔍 Sample results with preview of content for quick verification
- 📊 Complete test summary with statistics
- 🎨 Color-coded output for different types of information:
  - Blue: Test section headers
  - Green: Success messages and section labels
  - Cyan: Test outputs and detected values
  - Yellow: Expected values and important information
  - Red: Error messages and failures

### Cross-Mode Testing

The test suite supports both Mock mode and Azure mode:

- In Mock mode: All tests run without external dependencies
- In Azure mode: Azure-specific tests verify proper integration with Azure OpenAI services

Switch between modes by changing the `MOCK_RESPONSES` environment variable in your `.env` file.

## Environment Variables

| Variable | Description | Default | Required for Azure Mode |
|----------|-------------|---------|:----------------------:|
| `MOCK_RESPONSES` | Use mock responses instead of Azure | `true` | ✓ |
| `AZURE_OPENAI_KEY` | Azure OpenAI API key | N/A | ✓ |
| `AZURE_OPENAI_ENDPOINT` | Azure OpenAI endpoint URL | N/A | ✓ |
| `AZURE_API_VERSION` | Azure OpenAI API version | `2023-05-15` | ✓ |
| `MODEL_DEPLOYMENT` | Azure OpenAI model deployment name | `gpt-4` | ✓ |
| `PORT` | Server port | `8000` | |
| `LOG_LEVEL` | Logging level (DEBUG, INFO, WARNING, ERROR) | `INFO` | |
| `MAX_TOKENS` | Maximum tokens for Azure OpenAI responses | `1000` | |
| `TEMPERATURE` | Temperature for response generation | `0.7` | |

### Environment Setup Examples

For Mock mode (default):
```bash
MOCK_RESPONSES=true
PORT=8000
LOG_LEVEL=INFO
```

For Azure mode:
```bash
MOCK_RESPONSES=false
AZURE_OPENAI_KEY=your-api-key-here
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_API_VERSION=2023-05-15
MODEL_DEPLOYMENT=gpt-4
PORT=8000
LOG_LEVEL=INFO
```

## Dependencies

The project requires the following key dependencies:

- **Flask**: Web framework for the API server
- **python-dotenv**: Environment variable management
- **pytest**: For running tests
- **requests**: HTTP client for API calls
- **termcolor**: For colored terminal output
- **openai**: For Azure OpenAI integration (required for Azure mode)

Install all dependencies with:
```bash
pip install -r requirements.txt
```

For development environments, additional tools are recommended:
```bash
pip install black flake8 isort pytest-cov
```

## Development

### Adding New Domain Knowledge

To extend the system with new domain specializations:

1. Edit `agentic_skeleton/core/mock/constants/domain_knowledge.py`:

```python
DOMAIN_KNOWLEDGE = {
    # ... existing domains ...
    
    "new_domain_name": {
        "keywords": ["keyword1", "keyword2", "keyword3"],
        "preferred_category": "write",  # or another category
        "guidance": "Specific guidance for this domain...",
        "subtasks": {
            "data": ["data-related", "terms", "for", "this", "domain"],
            "analysis": ["analysis-related", "terms", "for", "this", "domain"],
            # Add other subtask types specific to this domain
        }
    }
}
```

2. Add corresponding mock responses in `agentic_skeleton/core/mock/constants/mock_responses.py`:

```python
MOCK_RESPONSES = {
    # ... existing responses ...
    
    "new_domain_specific": [
        "Domain-specific response template for {topic}...",
        "Another domain-specific response about {topic}...",
    ]
}
```

### Adding New Response Templates

To add new response templates:

1. Add new entries to `agentic_skeleton/core/mock/constants/mock_responses.py`
2. Update domain knowledge in `agentic_skeleton/core/mock/constants/domain_knowledge.py` if needed

Example:
```python
# In mock_responses.py
MOCK_RESPONSES["data-science"].append(
    "[MOCK] Data analysis of {topic} shows three significant trends: first, the increasing adoption of..."
)
```

### Adding New Test Cases

To add new test cases:

1. For unit tests: Add new test methods to `test_unit.py` or `test_azure_unit.py`
2. For integration tests: Add new test methods to `test_integration.py` or `test_azure_integration.py`

Example of adding a new test case:

```python
def test_new_feature(self):
    """Test a new feature of the API"""
    # Setup test data
    test_data = {"request": "Test the new feature"}
    
    # Make request
    response = self.app.post('/run-agent', json=test_data)
    
    # Assert expectations
    self.assertEqual(response.status_code, 200)
    data = json.loads(response.data)
    self.assertIn("plan", data)
    self.assertIn("results", data)
    
    # Add rich output formatting
    print(f"\n{colored('Testing new feature...', 'blue')}")
    print(f"\n{colored('Response:', 'green')}")
    print(f"  Plan steps: {len(data['plan'])}")
    print(f"  Results: {len(data['results'])}")
    
    # Additional assertions specific to this test case
    # ...
```

### Code Style and Formatting

Maintain consistent code style following these guidelines:

- Use [Black](https://black.readthedocs.io/) for code formatting: `black agentic_skeleton/`
- Sort imports with [isort](https://pycqa.github.io/isort/): `isort agentic_skeleton/`
- Validate code with [flake8](https://flake8.pycqa.org/): `flake8 agentic_skeleton/`
- Maintain test coverage with pytest-cov: `pytest --cov=agentic_skeleton`

### Continuous Integration

When contributing, ensure all tests pass in both Mock and Azure modes:

```bash
# Test in Mock mode
export MOCK_RESPONSES=true
python -m pytest

# Test in Azure mode (if you have Azure credentials)
export MOCK_RESPONSES=false
export AZURE_OPENAI_KEY=your-key
export AZURE_OPENAI_ENDPOINT=your-endpoint
python -m pytest agentic_skeleton/tests/test_azure_unit.py
python -m pytest agentic_skeleton/tests/test_azure_integration.py
```

