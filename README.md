# AgenticSkeleton

A Flask-based API skeleton for prompt enhancement using Azure OpenAI or mock responses.

## Quick Start

```bash
# Clone repository
git clone <your-repo-url> # Replace with your repo URL
cd AgenticSkeleton

# Set up environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac OR .venv\Scripts\activate for Windows
pip install -r requirements.txt
cp .env.example .env # Or create .env manually based on the Environment Variables section

# ---> Fill in your .env file with necessary credentials if using Azure <---

# Start the server
python -m agentic_skeleton

# In another terminal, test the API using the demo script
chmod +x demo.sh
./demo.sh 
# Or manually: curl http://localhost:8000/health
# Or manually: curl -X POST -H "Content-Type: application/json" -d '{"user_request": "example request", "user_profile": {"expertise": "beginner"}}' http://localhost:8000/enhance_prompt
```

## Project Structure

```
agentic_skeleton/
├── __init__.py             # Package initialization
├── __main__.py             # Main entry point (starts Flask app)
├── api/                    # API endpoints
│   ├── __init__.py
│   └── endpoints.py        # Flask routes (/health, /enhance_prompt)
├── config/                 # Configuration
│   ├── __init__.py
│   ├── mock_rag_data.py    # Mock data for RAG
│   └── settings.py         # Application settings (loads from .env)
├── core/                   # Core prompt processing logic
│   ├── __init__.py
│   ├── prompt_engineering.py # Logic for creating effective prompts
│   ├── prompt_processor.py # Main class orchestrating enhancement
│   ├── rag.py              # Retrieval-Augmented Generation logic
│   ├── user_profile.py     # User profile handling
│   └── azure/              # Azure OpenAI specific components
│       ├── __init__.py
│       └── client.py       # Azure OpenAI client interaction
├── tests/                  # Test suite
│   ├── test_api.py
│   ├── test_azure_client.py
│   ├── test_helpers.py
│   ├── test_integration.py
│   ├── test_main.py
│   ├── test_prompt_engineering.py
│   ├── test_prompt_processor.py
│   ├── test_rag_mock.py
│   ├── test_rag.py
│   └── test_user_profile.py
└── utils/                  # Utility functions
    ├── __init__.py
    └── helpers.py          # Helper functions (logging, etc.)

.env                        # Local environment variables (ignored by git)
.gitignore                  # Git ignore rules
README.md                   # This file
requirements.txt            # Python dependencies
demo.sh                     # Script to demonstrate API usage
```

## Configuration

Configuration is managed via environment variables loaded in `agentic_skeleton/config/settings.py`. Create a `.env` file in the project root.

Key variables:

*   `MOCK_RESPONSES`: Set to `true` (default) for mock mode, `false` for Azure OpenAI.
*   `AZURE_OPENAI_KEY`: Your Azure OpenAI API key (required if `MOCK_RESPONSES=false`).
*   `AZURE_OPENAI_ENDPOINT`: Your Azure OpenAI endpoint URL (required if `MOCK_RESPONSES=false`).
*   `MODEL_PROMPT_ENHANCER`: The Azure deployment name for the enhancement model (default: `gpt-4`).
*   `PORT`: Port for the Flask server (default: `8000`).
*   `FLASK_ENV`: Set to `development` for debug mode (default: not set).
*   `LOG_LEVEL`: Logging level (default: `INFO`).

See the `.env` file created earlier for a full template.

## Usage

### Mock Mode (Default)

Runs without needing Azure credentials.

```bash
# Ensure MOCK_RESPONSES=true or is commented out in .env
python -m agentic_skeleton
```

### Azure OpenAI Mode

Requires Azure credentials in `.env`.

1.  Set `MOCK_RESPONSES=false` in your `.env` file.
2.  Add your `AZURE_OPENAI_KEY` and `AZURE_OPENAI_ENDPOINT`.
3.  Optionally configure `MODEL_PROMPT_ENHANCER`.
4.  Run the application:
    ```bash
    python -m agentic_skeleton
    ```

## API Usage

### Health Check

```
GET /health
```
Response (example):
```json
{
  "status": "healthy",
  "mode": "mock", 
  "version": "..." 
}
```

### Enhance Prompt

```
POST /enhance_prompt
Body: 
{
  "user_request": "your user request here",
  "user_profile": { // Optional user profile details
    "expertise": "beginner", 
    "preferences": ["concise", "step-by-step"] 
  },
  "context": { // Optional context
    "previous_interaction": "...",
    "document_snippets": ["..."] 
  }
}
```

Response (example):
```json
{
  "enhanced_prompt": "A detailed, enhanced prompt generated based on the input...",
  "processing_details": {
    "mode": "mock", // or "azure"
    "model_used": "mock_processor" // or Azure model name
    // ... other details
  }
}
```

## Testing

Run tests using pytest:

```bash
# Run all tests
python -m pytest tests/

# Run specific test files
python -m pytest tests/test_api.py
python -m pytest tests/test_prompt_processor.py 
# etc.
```

Tests are designed to run in both Mock and Azure modes (controlled by `MOCK_RESPONSES` in `.env`). Some tests might be skipped if Azure credentials are not available when `MOCK_RESPONSES=false`.

## Environment Variables

| Variable                | Description                                       | Default      | Required for Azure |
|-------------------------|---------------------------------------------------|--------------|:------------------:|
| `MOCK_RESPONSES`        | Use mock responses (`true`) or Azure (`false`)    | `true`       | ✓                  |
| `PORT`                  | API Server port                                   | `8000`       |                    |
| `FLASK_ENV`             | Set to `development` for Flask debug mode         | `None`       |                    |
| `LOG_LEVEL`             | Logging level (DEBUG, INFO, etc.)                 | `INFO`       |                    |
| `AZURE_OPENAI_KEY`      | Azure OpenAI API key                              | `""`         | ✓                  |
| `AZURE_OPENAI_ENDPOINT` | Azure OpenAI endpoint URL                         | `""`         | ✓                  |
| `MODEL_PROMPT_ENHANCER` | Azure deployment name for prompt enhancer model | `gpt-4`      | ✓                  |
| `AZURE_API_VERSION`     | *Optional:* Azure API version                     | Not set      |                    |
| `MAX_TOKENS`            | *Optional:* Max tokens for Azure response         | Not set      |                    |
| `TEMPERATURE`           | *Optional:* Temperature for Azure response        | Not set      |                    |

*(Note: Variables marked Optional are not directly used in the current core logic but might be relevant for specific Azure client configurations or future features).*

### Environment Setup Examples

For Mock mode (default):
```bash
# .env file
MOCK_RESPONSES=true
PORT=8000
LOG_LEVEL=INFO
FLASK_ENV=development 
```

For Azure mode:
```bash
# .env file
MOCK_RESPONSES=false
AZURE_OPENAI_KEY=your-api-key-here
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
MODEL_PROMPT_ENHANCER=your-deployment-name # e.g., gpt-4
PORT=8000
LOG_LEVEL=INFO
FLASK_ENV=development # Optional for debugging
```

## Dependencies

Key dependencies listed in `requirements.txt`:

*   **Flask**: Web framework
*   **python-dotenv**: Loads `.env` files
*   **pytest**: Testing framework
*   **requests**: For HTTP requests (used in tests/demo)
*   **termcolor**: Colored terminal output
*   **openai**: Azure OpenAI client library (required for Azure mode)
*   **tiktoken**: Token counting for OpenAI models

Install all: `pip install -r requirements.txt`

For development (linters, formatters):
```bash
pip install black flake8 isort pytest-cov
```

## Development

### Code Style and Formatting

*   Format with Black: `black .`
*   Sort imports with isort: `isort .`
*   Lint with flake8: `flake8 .`
*   Check test coverage: `pytest --cov=agentic_skeleton tests/`

### Extending Functionality

*   **Prompt Engineering:** Modify logic in `agentic_skeleton/core/prompt_engineering.py`.
*   **RAG:** Update data sources or retrieval logic in `agentic_skeleton/core/rag.py` and potentially `agentic_skeleton/config/mock_rag_data.py`.
*   **Azure Client:** Adjust interaction with Azure in `agentic_skeleton/core/azure/client.py`.
*   **API Endpoints:** Add or modify routes in `agentic_skeleton/api/endpoints.py`.

Remember to add corresponding tests for any new features or changes.

