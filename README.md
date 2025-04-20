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
python -m agentic_skeleton.misc.simple_primer_test
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
│   ├── azure_integration.py  # Azure OpenAI integration
│   └── mock_responses.py     # Mock response generation
├── misc/               # Miscellaneous utilities
│   ├── simple_primer.py      # Simplified version of the app
│   └── simple_primer_test.py # Test client for the simplified app
├── tests/              # Test suite
│   ├── test_api.py     # API tests
│   ├── test_integration.py  # Integration tests
│   └── test_unit.py    # Unit tests
└── utils/              # Utility functions
    └── helpers.py      # Helper functions
```

## Configuration

By default, the application runs in mock mode which requires no API keys. To switch to Azure OpenAI:

1. Edit your `.env` file:
   ```
   # Change this to false for Azure mode
   MOCK_RESPONSES=false
   
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

## Simplified Version

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

The project includes three different testing approaches, all with enhanced output formatting:

### 1. Basic API Testing

A simple test script demonstrates how to use the API:

```bash
# Start the server in one terminal
python -m agentic_skeleton

# Run the test in another terminal
python -m agentic_skeleton.misc.simple_primer_test
```

Example output:
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
│                                 │ that ai has significant ...         │
├─────────────────────────────────┼─────────────────────────────────────┤
│ Create an outline               │ Here's a concise summary of         │
│                                 │ outline: It represents an ...       │
├─────────────────────────────────┼─────────────────────────────────────┤
│ ... more results ...            │ ...                                 │
└─────────────────────────────────┴─────────────────────────────────────┘
```

### 2. Unit Tests

Comprehensive unit tests validate the core functionality:

```bash
python -m test_unit
```

Example output:
```
=============== Running Unit Tests ===============
✅ test_health_check_endpoint - PASS (12ms)
✅ test_agent_endpoint_mock_mode - PASS (18ms)
✅ test_task_response_generation - PASS (5ms)
✅ test_error_handling - PASS (15ms)
✅ test_topic_extraction - PASS (3ms)

📊 Test Summary:
┌────────────────────────────────┬────────┬───────┐
│ Test Category                  │ Status │ Time  │
├────────────────────────────────┼────────┼───────┤
│ API Endpoints                  │ PASS   │ 30ms  │
│ Response Generation            │ PASS   │ 8ms   │
│ Error Handling                 │ PASS   │ 15ms  │
├────────────────────────────────┼────────┼───────┤
│ TOTAL                          │ 5/5    │ 53ms  │
└────────────────────────────────┴────────┴───────┘
```

### 3. Integration Tests

Integration tests validate the full request-response cycle:

```bash
python -m test_integration
```

Example output:
```
=============== Running Integration Tests ===============
🚀 Starting test server on port 8001
⏳ Waiting for server to start...
✅ Server is running

▶️ Running integration tests:
✅ test_basic_request - PASS (132ms)
✅ test_analytical_request - PASS (118ms)
✅ test_creative_request - PASS (125ms)
✅ test_technical_request - PASS (142ms)
✅ test_error_handling - PASS (28ms)

📈 Performance Metrics:
┌─────────────────────┬───────────┬───────────────┬───────────┐
│ Request Type        │ Status    │ Response Time │ Plan Size │
├─────────────────────┼───────────┼───────────────┼───────────┤
│ Basic               │ ✅ PASS   │ 132ms         │ 5 steps   │
│ Analytical          │ ✅ PASS   │ 118ms         │ 6 steps   │
│ Creative            │ ✅ PASS   │ 125ms         │ 5 steps   │
│ Technical           │ ✅ PASS   │ 142ms         │ 7 steps   │
├─────────────────────┼───────────┼───────────────┼───────────┤
│ AVERAGE             │ 100%      │ 129ms         │ 5.8 steps │
└─────────────────────┴───────────┴───────────────┴───────────┘

🛑 Stopping test server
```

## Enhanced Test Output

All test scripts include enhanced output formatting with:

- ✅ Colorized test results with pass/fail indicators
- ⏱️ Detailed timing metrics for performance analysis
- 📊 Performance comparison tables with response times
- 🔄 Visual progress indicators for long-running tests
- 📋 JSON response visualization with syntax highlighting
- 📈 Summary tables with success rates and statistics

For the best experience, ensure you have the termcolor package installed:

```bash
pip install termcolor
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `MOCK_RESPONSES` | Use mock responses instead of Azure | `true` |
| `AZURE_OPENAI_KEY` | Azure OpenAI API key | N/A |
| `AZURE_OPENAI_ENDPOINT` | Azure OpenAI endpoint URL | N/A |
| `MODEL_PLANNER` | Model for planning tasks | `o3-mini` |
| `MODEL_EXECUTOR` | Model for execution tasks | `claude_3.7_sonnet` |
| `PORT` | Server port | `8000` |

## Dependencies

- Flask: Web framework for the API server
- python-dotenv: Environment variable management
- requests: HTTP client for API calls
- termcolor: For colored test output
- openai: For Azure OpenAI integration (optional)
- gunicorn: For production deployment (optional)

## Development

### Running Tests

```bash
# Run all tests
python -m test_unit && python -m test_integration

# Run a specific test file
python -m test_unit
python -m test_integration

# Run the basic test script (server must be running)
python -m agentic_skeleton.misc.simple_primer_test
```

### Adding New Test Cases

To add new test cases:

1. For unit tests: Add new test methods to `test_unit.py`
2. For integration tests: Add new test methods to `test_integration.py`

Example of adding a new test case:

```python
def test_new_feature(self):
    """Test a new feature of the API"""
    # Setup test data
    test_data = {"request": "Test the new feature"}
    
    # Make request
    response = requests.post(f"{self.base_url}/run-agent", json=test_data)
    
    # Assert expectations
    self.assertEqual(response.status_code, 200)
    data = response.json()
    self.assertIn("plan", data)
    self.assertIn("results", data)
    
    # Additional assertions specific to this test case
    # ...
```

