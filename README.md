# AI-400 Task Management API + Skills Development

A comprehensive Task Management API built with FastAPI, SQLModel, and SQLite, featuring reusable AI agent skills for workflow automation.

## Project Overview

This project demonstrates three core competencies:
1. **Agent Skills Development**: Reusable skills extracted from daily workflows
2. **Modern API Development**: FastAPI with test-driven development using pytest
3. **Database Design**: SQLModel for efficient database operations

## Tech Stack

- **FastAPI**: Modern Python web framework for building APIs
- **SQLModel**: SQL database ORM with Python type hints
- **SQLite**: Lightweight, file-based database (zero configuration!)
- **pytest**: Testing framework for TDD

## Project Structure

```
ai400-task-management/
├── app/
│   ├── api/          # API endpoints
│   ├── models/       # Database models
│   ├── database/     # Database configuration
│   └── skills/       # Agent skills
├── tests/            # Test suite
├── requirements.txt  # Dependencies
└── .env              # Environment variables
```

## Quick Setup

Use the automated setup script:
```bash
./setup.sh
```

Or follow manual steps:

### Manual Setup

1. **Clone and Navigate**
   ```bash
   cd ai400-task-management
   ```

2. **Run Setup Script**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

3. **Start the API Server** (database creates automatically!)
   ```bash
   source venv/bin/activate
   uvicorn app.main:app --reload
   ```

4. **Load Demo Data (Optional)**
   ```bash
   python demo_data.py
   ```

5. **Run Tests**
   ```bash
   pytest -v
   ```

## API Endpoints

Full CRUD operations for Task Management:

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/tasks/` | Create a new task |
| GET | `/tasks/` | List all tasks (with filtering & pagination) |
| GET | `/tasks/{task_id}` | Get a specific task |
| PUT | `/tasks/{task_id}` | Update a task |
| DELETE | `/tasks/{task_id}` | Delete a task |
| GET | `/` | API information |
| GET | `/health` | Health check |

### Query Parameters

- `status`: Filter by task status (todo, in_progress, completed, cancelled)
- `priority`: Filter by priority (low, medium, high, urgent)
- `skip`: Pagination offset (default: 0)
- `limit`: Number of results (default: 100, max: 100)

## Skills Included

### Technical Skills (3)

1. **Code Review Skill** (`app/skills/code_review.py`)
   - Automated Python code quality analysis
   - Detects bugs, style violations, and code smells
   - AST-based analysis
   - Run: `python -m app.skills.code_review`

2. **Database Query Optimizer** (`app/skills/db_optimizer.py`)
   - SQL query performance analysis
   - Optimization score (0-100)
   - Actionable recommendations
   - Run: `python -m app.skills.db_optimizer`

3. **API Test Generator** (`app/skills/test_generator.py`)
   - Automatic pytest test generation
   - Complete CRUD test suites
   - Reduces boilerplate
   - Run: `python -m app.skills.test_generator`

### Workflow Skills (2)

1. **Daily Standup Reporter** (`app/skills/standup_reporter.py`)
   - Generate standup reports from git commits
   - Task-based report generation
   - Blocker identification
   - Run: `python -m app.skills.standup_reporter`

2. **Task Prioritizer** (`app/skills/task_prioritizer.py`)
   - Intelligent task prioritization
   - Multi-factor scoring algorithm
   - Daily capacity estimation
   - Run: `python -m app.skills.task_prioritizer`

See [SKILLS_DOCUMENTATION.md](SKILLS_DOCUMENTATION.md) for comprehensive skill documentation.

## Testing

Comprehensive test coverage for both API and skills:

```bash
# Run all tests
pytest -v

# Run specific test file
pytest tests/test_api.py -v
pytest tests/test_skills.py -v

# Run with coverage
pytest --cov=app --cov-report=html
```

## Project Files

- [README.md](README.md) - This file
- [SKILLS_DOCUMENTATION.md](SKILLS_DOCUMENTATION.md) - Comprehensive skills documentation
- [DEMO_SCRIPT.md](DEMO_SCRIPT.md) - Demo video script and recording guide
- [requirements.txt](requirements.txt) - Python dependencies
- [setup.sh](setup.sh) - Automated setup script
- [demo_data.py](demo_data.py) - Demo data loader

## Demo Video

See [DEMO_SCRIPT.md](DEMO_SCRIPT.md) for the complete demo script and recording guide.

**Recording Checklist**:
- [ ] Run API server (database creates automatically)
- [ ] Demo all 5 skills
- [ ] Show API CRUD operations
- [ ] Run tests
- [ ] Keep video 60-90 seconds

## Submission Deliverables

✅ **4-5 Skills** (3 Technical + 1-2 Workflow)
- Code Review Skill
- Database Optimizer Skill
- Test Generator Skill
- Standup Reporter Skill
- Task Prioritizer Skill

✅ **Task Management API** with Full CRUD
- All endpoints implemented
- Filtering and pagination
- SQLModel database design
- Complete test coverage

✅ **Demo Video Script**
- 60-90 second structure
- Technical setup guide
- Recording checklist

## Author

Muhammad Zubair
AI-400 Class 1 Project
January 2026
# ai400-task-management
