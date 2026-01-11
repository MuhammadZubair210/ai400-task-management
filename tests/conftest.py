import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session, StaticPool
from app.main import app
from app.database import get_session
from app.models import Task


@pytest.fixture(name="session")
def session_fixture():
    """Create a test database session"""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    """Create a test client with dependency override"""
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture
def sample_task_data():
    """Sample task data for testing"""
    return {
        "title": "Test Task",
        "description": "This is a test task",
        "status": "todo",
        "priority": "medium",
        "tags": "test,automation"
    }


@pytest.fixture
def create_test_task(session: Session):
    """Fixture to create a test task"""
    def _create_task(**kwargs):
        task = Task(
            title=kwargs.get("title", "Test Task"),
            description=kwargs.get("description", "Test Description"),
            status=kwargs.get("status", "todo"),
            priority=kwargs.get("priority", "medium"),
            tags=kwargs.get("tags", "test")
        )
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    return _create_task
