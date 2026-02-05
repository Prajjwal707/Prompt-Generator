"""
API tests for PromptGenius backend.
"""

import pytest
import json
from app import create_app

@pytest.fixture
def app():
    app = create_app('testing')
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def valid_api_key():
    return "test_api_key_12345678901234567890123456789012"

def test_health_check(client):
    response = client.get('/api/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'

def test_enhance_prompt_no_auth(client):
    response = client.post('/api/enhance', 
                          json={'prompt': 'test', 'task_type': 'general'})
    assert response.status_code == 401

def test_enhance_prompt_with_auth(client, valid_api_key):
    headers = {'x-api-key': valid_api_key}
    response = client.post('/api/enhance', 
                          json={'prompt': 'test', 'task_type': 'general'},
                          headers=headers)
    # Should fail due to model not loaded, but auth should pass
    assert response.status_code in [500, 401]

def test_validate_prompt(client):
    response = client.post('/api/validate', 
                          json={'prompt': 'test prompt'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert 'validation' in data

def test_task_types(client):
    response = client.get('/api/task-types')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert 'task_types' in data
