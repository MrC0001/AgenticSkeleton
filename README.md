# AgenticSkeleton

A simple Flask-based AI agent skeleton with both mock responses and Azure OpenAI integration.
Perfect starting point for hackathons!

## Features

- **Dual Mode Operation**: 
  - Mock mode for local development without Azure credentials
  - Azure OpenAI integration for production use
- **Simple API**:
  - Single endpoint that generates a plan and executes tasks
  - Health check endpoint for monitoring
- **Easy Configuration**:
  - Environment variables for all settings
  - Defaults that work out of the box

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
python app.py

# In another terminal, test the API
python test.py
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
python app.py
```

### Azure OpenAI Mode

To use with Azure OpenAI:

1. Set `MOCK_RESPONSES=false` in your `.env` file
2. Add your Azure OpenAI credentials:
   - `AZURE_OPENAI_KEY`
   - `AZURE_OPENAI_ENDPOINT`
3. Run the application
## API Usage

### Health Check
```
GET /health
```
Response:
```json
{
  "status": "healthy",
  "mode": "mock"  // or "azure" in production mode
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

The included test script demonstrates how to use the API:

```bash
# Start the server in one terminal
python app.py

# Run the test in another terminal
python test.py
```

| Variable | Description | Default |
|----------|-------------|---------|
| `MOCK_RESPONSES` | Use mock responses instead of Azure | `true` |
| `AZURE_OPENAI_KEY` | Azure OpenAI API key | N/A |
| `AZURE_OPENAI_ENDPOINT` | Azure OpenAI endpoint URL | N/A |
| `MODEL_PLANNER` | Model for planning tasks | `gpt-4` |
| `MODEL_EXECUTOR` | Model for execution tasks | `gpt-4` |
| `PORT` | Server port | `8000` |

