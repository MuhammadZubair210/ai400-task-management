import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta


class TestRootEndpoints:
    """Test root and health check endpoints"""

    def test_root_endpoint(self, client: TestClient):
        """Test GET /"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data

    def test_health_check(self, client: TestClient):
        """Test GET /health"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}


class TestCreateTask:
    """Test task creation endpoint"""

    def test_create_task_success(self, client: TestClient, sample_task_data):
        """Test creating a task successfully"""
        response = client.post("/tasks/", json=sample_task_data)
        assert response.status_code == 201

        data = response.json()
        assert "id" in data
        assert data["title"] == sample_task_data["title"]
        assert data["description"] == sample_task_data["description"]
        assert data["status"] == sample_task_data["status"]
        assert data["priority"] == sample_task_data["priority"]

    def test_create_task_minimal(self, client: TestClient):
        """Test creating a task with minimal data"""
        minimal_task = {"title": "Minimal Task"}
        response = client.post("/tasks/", json=minimal_task)
        assert response.status_code == 201

        data = response.json()
        assert data["title"] == "Minimal Task"
        assert data["status"] == "todo"
        assert data["priority"] == "medium"

    def test_create_task_invalid_empty_title(self, client: TestClient):
        """Test creating a task with empty title"""
        invalid_task = {"title": ""}
        response = client.post("/tasks/", json=invalid_task)
        assert response.status_code == 422

    def test_create_task_missing_title(self, client: TestClient):
        """Test creating a task without title"""
        invalid_task = {"description": "No title provided"}
        response = client.post("/tasks/", json=invalid_task)
        assert response.status_code == 422

    def test_create_task_with_due_date(self, client: TestClient):
        """Test creating a task with due date"""
        future_date = (datetime.now() + timedelta(days=7)).isoformat()
        task_data = {
            "title": "Task with deadline",
            "due_date": future_date
        }
        response = client.post("/tasks/", json=task_data)
        assert response.status_code == 201
        data = response.json()
        assert data["due_date"] is not None


class TestGetTasks:
    """Test task retrieval endpoints"""

    def test_get_tasks_empty(self, client: TestClient):
        """Test getting tasks when none exist"""
        response = client.get("/tasks/")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_tasks_list(self, client: TestClient, create_test_task):
        """Test getting list of tasks"""
        create_test_task(title="Task 1")
        create_test_task(title="Task 2")
        create_test_task(title="Task 3")

        response = client.get("/tasks/")
        assert response.status_code == 200

        data = response.json()
        assert len(data) == 3
        assert all("id" in task for task in data)

    def test_get_tasks_with_pagination(self, client: TestClient, create_test_task):
        """Test getting tasks with pagination"""
        for i in range(10):
            create_test_task(title=f"Task {i}")

        response = client.get("/tasks/?skip=0&limit=5")
        assert response.status_code == 200
        assert len(response.json()) == 5

        response = client.get("/tasks/?skip=5&limit=5")
        assert response.status_code == 200
        assert len(response.json()) == 5

    def test_get_tasks_filter_by_status(self, client: TestClient, create_test_task):
        """Test filtering tasks by status"""
        create_test_task(title="Todo Task", status="todo")
        create_test_task(title="In Progress Task", status="in_progress")
        create_test_task(title="Completed Task", status="completed")

        response = client.get("/tasks/?status=todo")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["status"] == "todo"

    def test_get_tasks_filter_by_priority(self, client: TestClient, create_test_task):
        """Test filtering tasks by priority"""
        create_test_task(title="Low Priority", priority="low")
        create_test_task(title="High Priority", priority="high")
        create_test_task(title="Urgent Task", priority="urgent")

        response = client.get("/tasks/?priority=urgent")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["priority"] == "urgent"


class TestGetTaskById:
    """Test retrieving a specific task"""

    def test_get_task_success(self, client: TestClient, create_test_task):
        """Test getting a task by ID"""
        task = create_test_task(title="Specific Task")

        response = client.get(f"/tasks/{task.id}")
        assert response.status_code == 200

        data = response.json()
        assert data["id"] == task.id
        assert data["title"] == "Specific Task"

    def test_get_task_not_found(self, client: TestClient):
        """Test getting a non-existent task"""
        response = client.get("/tasks/99999")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()


class TestUpdateTask:
    """Test task update endpoint"""

    def test_update_task_success(self, client: TestClient, create_test_task):
        """Test updating a task"""
        task = create_test_task(title="Original Title")

        update_data = {
            "title": "Updated Title",
            "status": "in_progress"
        }

        response = client.put(f"/tasks/{task.id}", json=update_data)
        assert response.status_code == 200

        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["status"] == "in_progress"

    def test_update_task_partial(self, client: TestClient, create_test_task):
        """Test partial update of a task"""
        task = create_test_task(
            title="Original",
            description="Original Description",
            priority="low"
        )

        update_data = {"priority": "high"}

        response = client.put(f"/tasks/{task.id}", json=update_data)
        assert response.status_code == 200

        data = response.json()
        assert data["title"] == "Original"
        assert data["description"] == "Original Description"
        assert data["priority"] == "high"

    def test_update_task_not_found(self, client: TestClient):
        """Test updating a non-existent task"""
        update_data = {"title": "Updated"}
        response = client.put("/tasks/99999", json=update_data)
        assert response.status_code == 404

    def test_update_task_invalid_data(self, client: TestClient, create_test_task):
        """Test updating with invalid data"""
        task = create_test_task(title="Test Task")

        update_data = {"title": ""}
        response = client.put(f"/tasks/{task.id}", json=update_data)
        assert response.status_code == 422


class TestDeleteTask:
    """Test task deletion endpoint"""

    def test_delete_task_success(self, client: TestClient, create_test_task):
        """Test deleting a task"""
        task = create_test_task(title="Task to Delete")

        response = client.delete(f"/tasks/{task.id}")
        assert response.status_code == 204

        get_response = client.get(f"/tasks/{task.id}")
        assert get_response.status_code == 404

    def test_delete_task_not_found(self, client: TestClient):
        """Test deleting a non-existent task"""
        response = client.delete("/tasks/99999")
        assert response.status_code == 404


class TestTaskWorkflow:
    """Test complete task workflow"""

    def test_complete_crud_workflow(self, client: TestClient):
        """Test complete CRUD workflow"""
        create_data = {
            "title": "Workflow Test Task",
            "description": "Testing complete workflow",
            "priority": "high"
        }
        create_response = client.post("/tasks/", json=create_data)
        assert create_response.status_code == 201
        task_id = create_response.json()["id"]

        read_response = client.get(f"/tasks/{task_id}")
        assert read_response.status_code == 200
        assert read_response.json()["title"] == create_data["title"]

        update_data = {"status": "completed"}
        update_response = client.put(f"/tasks/{task_id}", json=update_data)
        assert update_response.status_code == 200
        assert update_response.json()["status"] == "completed"

        delete_response = client.delete(f"/tasks/{task_id}")
        assert delete_response.status_code == 204

        verify_response = client.get(f"/tasks/{task_id}")
        assert verify_response.status_code == 404
