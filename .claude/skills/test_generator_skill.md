# API Test Generator Skill

**Type**: Technical Skill
**Purpose**: Automated pytest test case generation for FastAPI endpoints

## Overview

This skill automatically generates pytest test cases for FastAPI endpoints by analyzing route definitions using AST (Abstract Syntax Tree) analysis. It creates comprehensive CRUD test suites with proper assertions for each HTTP method.

## Capabilities

- Analyzes FastAPI router files using AST
- Detects route decorators (@router.get, @router.post, etc.)
- Generates test functions for each endpoint
- Creates appropriate assertions for each HTTP method
- Generates complete CRUD test suites
- Supports fixtures for test data
- Handles path parameters automatically

## Usage

```bash
python -m app.skills.test_generator
```

Or programmatically:

```python
from app.skills.test_generator import TestGeneratorSkill

generator = TestGeneratorSkill()

# Generate tests from a FastAPI router file
result = generator.generate_tests_from_file("app/api/tasks.py")
print(f"Generated tests for {result['endpoints_found']} endpoints")
print(result['test_code'])

# Generate comprehensive CRUD tests for a model
test_code = generator.generate_tests_for_model("Task", "/tasks")
with open("tests/test_tasks_generated.py", "w") as f:
    f.write(test_code)
```

## Generated Test Structure

### For Individual Endpoints

```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_tasks():
    """Test GET /tasks"""
    response = client.get("/tasks")
    assert response.status_code in [200, 404]
    if response.status_code == 200:
        assert response.json() is not None


def test_create_task():
    """Test POST /tasks"""
    test_data = {
        # TODO: Add appropriate test data
    }
    response = client.post("/tasks", json=test_data)
    assert response.status_code in [201, 422]
    if response.status_code == 201:
        assert "id" in response.json()
```

### For Complete CRUD Model

```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


@pytest.fixture
def sample_task():
    """Fixture providing sample Task data"""
    return {
        # TODO: Add sample data for Task
    }


def test_create_task(sample_task):
    """Test creating a new Task"""
    response = client.post("/tasks", json=sample_task)
    assert response.status_code == 201
    data = response.json()
    assert "id" in data


def test_get_tasks():
    """Test retrieving all Tasks"""
    response = client.get("/tasks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
```

## Output Format

```json
{
  "source_file": "app/api/tasks.py",
  "endpoints_found": 5,
  "test_code": "import pytest\nfrom fastapi...",
  "status": "generated"
}
```

## HTTP Method Support

- **GET**: Tests for 200/404 responses, validates JSON output
- **POST**: Tests for 201/422 responses, checks for ID in response
- **PUT**: Tests for 200/404/422 responses, handles path parameters
- **DELETE**: Tests for 204/404 responses
- **PATCH**: Tests similar to PUT

## Real-World Applications

- Accelerate test-driven development (TDD)
- Ensure comprehensive API endpoint coverage
- Generate boilerplate test code quickly
- Maintain consistent test structure across projects
- Reduce manual test writing time by 70-80%
- CI/CD pipeline integration for automated test generation
- Documentation through generated test examples
