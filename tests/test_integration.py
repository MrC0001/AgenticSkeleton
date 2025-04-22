# tests/test_integration.py

import pytest
import json # Import json for payload handling
from unittest.mock import patch # Import patch for mocking
from agentic_skeleton.api.endpoints import app # Import the Flask app instance

# Fixture to provide the Flask test client
@pytest.fixture
def client():
    app.config['TESTING'] = True # Enable testing mode
    # Disable CSRF protection if it were enabled (good practice for testing)
    # app.config['WTF_CSRF_ENABLED'] = False
    with app.test_client() as client:
        yield client

# First real integration test: /health endpoint
def test_health_check(client):
    """Test the /health endpoint."""
    response = client.get('/health')

    # Assert status code is 200 OK
    assert response.status_code == 200

    # Assert content type is application/json
    assert response.content_type == 'application/json'

    # Parse the JSON response
    data = json.loads(response.data)

    # Assert expected keys and basic structure
    assert 'status' in data
    assert 'mode' in data
    assert 'llm_model' in data
    assert 'version' in data
    assert data['status'] == 'healthy'
    # We can add more specific checks for mode/model if needed,
    # potentially based on environment variables or settings mocks

# --- Tests for /enhance_prompt ---

def test_enhance_prompt_malformed_json(client):
    """Test /enhance_prompt with malformed JSON."""
    response = client.post('/enhance_prompt',
                           data='not valid json',
                           content_type='application/json')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert data['error'] == 'Malformed JSON'

def test_enhance_prompt_missing_payload(client):
    """Test /enhance_prompt with no JSON payload."""
    response = client.post('/enhance_prompt', content_type='application/json')
    # Depending on Flask version/config, this might be caught as malformed JSON or handled differently.
    # Let's assume it results in a 400 based on the endpoint's explicit check for `payload is None`.
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    # The error message might vary slightly, check for key error types
    assert data['error'] in ['Malformed JSON', 'Invalid Payload']


def test_enhance_prompt_missing_fields(client):
    """Test /enhance_prompt with missing fields in payload."""
    # Missing 'prompt'
    response = client.post('/enhance_prompt',
                           json={'user_id': 'test_user'})
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert data['error'] == 'Invalid Payload'
    assert 'Missing' in data['message']

    # Missing 'user_id'
    response = client.post('/enhance_prompt',
                           json={'prompt': 'hello world'})
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert data['error'] == 'Invalid Payload'
    assert 'Missing' in data['message']

def test_enhance_prompt_incorrect_types(client):
    """Test /enhance_prompt with incorrect field types in payload."""
    # 'user_id' is not a string
    response = client.post('/enhance_prompt',
                           json={'user_id': 123, 'prompt': 'hello'})
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert data['error'] == 'Invalid Payload Type'
    assert 'must be strings' in data['message']

    # 'prompt' is not a string
    response = client.post('/enhance_prompt',
                           json={'user_id': 'test_user', 'prompt': ['list']})
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert data['error'] == 'Invalid Payload Type'
    assert 'must be strings' in data['message']

# Test for successful request
@patch('agentic_skeleton.api.endpoints.prompt_processor.process_prompt_request')
def test_enhance_prompt_success(mock_process_prompt, client):
    """Test /enhance_prompt successful request."""
    # Configure the mock to return a specific value
    expected_response_text = "This is the enhanced prompt."
    mock_process_prompt.return_value = expected_response_text

    user_id = "user123"
    prompt = "Enhance this please."
    payload = {'user_id': user_id, 'prompt': prompt}

    response = client.post('/enhance_prompt', json=payload)

    # Assert status code is 200 OK
    assert response.status_code == 200
    assert response.content_type == 'application/json'

    # Assert the mock was called correctly
    mock_process_prompt.assert_called_once_with(user_id, prompt)

    # Assert the response data is correct
    data = json.loads(response.data)
    assert 'enhanced_response' in data
    assert data['enhanced_response'] == expected_response_text

# Test for internal server error
@patch('agentic_skeleton.api.endpoints.prompt_processor.process_prompt_request')
def test_enhance_prompt_internal_error(mock_process_prompt, client):
    """Test /enhance_prompt when an unexpected error occurs."""
    # Configure the mock to raise an exception
    error_message = "Something went wrong internally!"
    mock_process_prompt.side_effect = Exception(error_message)

    user_id = "user_error"
    prompt = "This will cause an error."
    payload = {'user_id': user_id, 'prompt': prompt}

    response = client.post('/enhance_prompt', json=payload)

    # Assert status code is 500 Internal Server Error
    assert response.status_code == 500
    assert response.content_type == 'application/json'

    # Assert the mock was called
    mock_process_prompt.assert_called_once_with(user_id, prompt)

    # Assert the response data indicates an internal error
    data = json.loads(response.data)
    assert 'error' in data
    assert data['error'] == 'Internal Server Error'
    assert 'message' in data # Check for the generic message
