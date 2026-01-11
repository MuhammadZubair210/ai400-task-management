# Agent Skills Documentation

This document provides comprehensive documentation for all agent skills included in this project.

## Overview

The project includes **5 reusable agent skills**:
- **3 Technical Skills**: Automation for development tasks
- **2 Workflow Skills**: Automation for daily workflow tasks

All skills are designed to be modular, reusable, and easily integrated into AI agent workflows.

---

## Technical Skills

### 1. Code Review Skill

**File**: `app/skills/code_review.py`

**Purpose**: Automatically analyzes Python code for quality issues, style violations, and potential bugs.

**Key Features**:
- AST (Abstract Syntax Tree) analysis
- Detects functions with too many parameters
- Identifies missing docstrings
- Finds bare except clauses
- Checks for empty exception handlers
- Validates line length (120 chars)
- Verifies import placement

**Usage**:
```python
from app.skills import CodeReviewSkill

reviewer = CodeReviewSkill()
result = reviewer.review_file("path/to/file.py")

print(f"Total issues: {result['total_issues']}")
for issue in result['issues']:
    print(f"Line {issue['line']}: [{issue['severity']}] {issue['message']}")
```

**Command Line**:
```bash
python -m app.skills.code_review
```

**Return Format**:
```json
{
  "file": "path/to/file.py",
  "total_issues": 5,
  "issues": [
    {
      "type": "missing_docstring",
      "severity": "low",
      "line": 10,
      "message": "Function 'example' missing docstring"
    }
  ],
  "status": "reviewed"
}
```

**Severity Levels**:
- `critical`: Syntax errors that prevent code execution
- `high`: Serious issues like bare except clauses
- `medium`: Code smells like too many parameters
- `low`: Style issues like missing docstrings

**Real-World Application**:
- Pre-commit hooks for code quality
- CI/CD pipeline integration
- Automated code review in pull requests
- Developer training and feedback

---

### 2. Database Query Optimizer Skill

**File**: `app/skills/db_optimizer.py`

**Purpose**: Analyzes SQL queries and SQLModel code for performance issues and provides optimization recommendations.

**Key Features**:
- Detects SELECT * usage
- Identifies missing WHERE clauses
- Flags missing LIMIT clauses
- Detects multiple OR conditions (suggests IN clause)
- Identifies function calls in WHERE clause
- Finds subqueries in SELECT
- Detects leading wildcards in LIKE patterns
- Checks DISTINCT usage
- Calculates optimization score (0-100)

**Usage**:
```python
from app.skills import DatabaseOptimizerSkill

optimizer = DatabaseOptimizerSkill()
result = optimizer.analyze_query(
    "SELECT * FROM tasks WHERE UPPER(title) LIKE '%urgent%'"
)

print(f"Optimization Score: {result['optimization_score']}/100")
for rec in result['recommendations']:
    print(f"[{rec['severity']}] {rec['issue']}")
    print(f"  → {rec['recommendation']}")
```

**Command Line**:
```bash
python -m app.skills.db_optimizer
```

**Return Format**:
```json
{
  "query": "SELECT * FROM tasks...",
  "optimization_score": 45,
  "total_recommendations": 3,
  "recommendations": [
    {
      "type": "select_star",
      "severity": "medium",
      "issue": "Using SELECT * retrieves all columns",
      "recommendation": "Explicitly specify only the columns you need",
      "example": "SELECT id, name, email FROM users"
    }
  ],
  "status": "analyzed"
}
```

**Optimization Score**:
- 90-100: Excellent optimization
- 70-89: Good optimization
- 50-69: Moderate optimization needed
- 0-49: Significant optimization needed

**Real-World Application**:
- Performance optimization reviews
- Database query auditing
- Developer training on SQL best practices
- Automated performance monitoring

---

### 3. API Test Generator Skill

**File**: `app/skills/test_generator.py`

**Purpose**: Automatically generates pytest test cases for FastAPI endpoints by analyzing route definitions.

**Key Features**:
- Analyzes FastAPI router files
- Detects route decorators
- Generates test functions for each endpoint
- Creates appropriate assertions for each HTTP method
- Generates complete CRUD test suites
- Supports fixtures for test data

**Usage**:
```python
from app.skills import TestGeneratorSkill

generator = TestGeneratorSkill()

# Generate tests for a specific model
test_code = generator.generate_tests_for_model("Task", "/tasks")

# Save to file
with open("tests/test_generated.py", "w") as f:
    f.write(test_code)
```

**Command Line**:
```bash
python -m app.skills.test_generator
```

**Generated Test Structure**:
```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_task():
    """Test POST /tasks"""
    test_data = {...}
    response = client.post("/tasks", json=test_data)
    assert response.status_code == 201
    assert "id" in response.json()

def test_get_tasks():
    """Test GET /tasks"""
    response = client.get("/tasks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
```

**Real-World Application**:
- Accelerate test-driven development
- Ensure API endpoint coverage
- Generate boilerplate test code
- Maintain consistent test structure

---

## Workflow Skills

### 4. Daily Standup Reporter Skill

**File**: `app/skills/standup_reporter.py`

**Purpose**: Automates the creation of daily standup reports by analyzing git commits and task completion data.

**Key Features**:
- Extracts yesterday's git commits
- Cleans and formats commit messages
- Identifies potential blockers
- Generates formatted standup reports
- Supports task-based report generation
- Provides statistics on completed work

**Usage**:

**From Git Commits**:
```python
from app.skills import StandupReporterSkill

reporter = StandupReporterSkill()
result = reporter.generate_report(".")

print(result["report"])
```

**From Task List**:
```python
tasks = [
    {
        "title": "Implement authentication",
        "status": "completed",
        "updated_at": "2024-01-09T12:00:00"
    },
    {
        "title": "Write tests",
        "status": "in_progress",
        "updated_at": "2024-01-10T09:00:00"
    }
]

result = reporter.generate_from_task_list(tasks)
print(result["report"])
```

**Command Line**:
```bash
python -m app.skills.standup_reporter
```

**Report Format**:
```
📅 Daily Standup Report - 2024-01-10

✅ Yesterday:
   • Implemented user authentication
   • Fixed critical bug in task filtering
   • Updated API documentation

🎯 Today:
   • Continue work on task search feature
   • Review pull requests
   • Address feedback from code review

🚧 Blockers:
   • No blockers
```

**Real-World Application**:
- Automate daily standup preparation
- Save time in agile ceremonies
- Track team progress automatically
- Generate weekly summaries

---

### 5. Task Prioritizer Skill

**File**: `app/skills/task_prioritizer.py`

**Purpose**: Intelligently prioritizes tasks based on deadlines, dependencies, effort estimates, and urgency using a scoring algorithm.

**Key Features**:
- Multi-factor priority scoring algorithm
- Due date urgency calculation
- Status-based prioritization
- Tag-based priority boosting
- Overdue task detection
- Daily capacity estimation
- Actionable recommendations

**Scoring Algorithm**:
- Base priority (low: 25, medium: 50, high: 75, urgent: 100)
- Due date urgency (0-50 points based on days until due)
- In-progress status boost (+20 points)
- Tag modifiers (urgent: +30, critical: +25, blocked: -40)
- Description keywords (asap: +20, deadline: +15)

**Usage**:
```python
from app.skills import TaskPrioritizerSkill

prioritizer = TaskPrioritizerSkill()

tasks = [
    {
        "title": "Fix critical bug",
        "priority": "urgent",
        "status": "todo",
        "due_date": "2024-01-10T17:00:00"
    },
    {
        "title": "Write documentation",
        "priority": "low",
        "status": "todo",
        "due_date": None
    }
]

result = prioritizer.prioritize_tasks(tasks)

for task in result["prioritized_tasks"]:
    print(f"{task['recommended_order']}. {task['title']}")
    print(f"   Score: {task['priority_score']:.1f}")
```

**Daily Task Suggestions**:
```python
# Get top 5 tasks to focus on today
result = prioritizer.suggest_daily_tasks(all_tasks, max_tasks=5)

print(f"📋 Focus on these {result['total_suggested']} tasks today:")
for task in result["suggested_tasks"]:
    print(f"  • {task['title']}")
```

**Capacity Estimation**:
```python
result = prioritizer.estimate_daily_capacity(tasks)
print(result["capacity_assessment"])
# Output: "✅ Workload appears manageable"
# or "⚠️ Too many high-priority tasks for one day"
```

**Command Line**:
```bash
python -m app.skills.task_prioritizer
```

**Recommendations Generated**:
- Top priority task to focus on
- Overdue task warnings
- In-progress task reminders
- Capacity overload alerts
- Blocker notifications

**Real-World Application**:
- Daily work planning
- Sprint planning assistance
- Time management optimization
- Workload balancing
- Burnout prevention

---

## Integration Examples

### Using Skills Together

**Morning Workflow Automation**:
```python
# 1. Generate standup report
standup = StandupReporterSkill().generate_report()

# 2. Get prioritized task list
prioritizer = TaskPrioritizerSkill()
daily_tasks = prioritizer.suggest_daily_tasks(all_tasks, max_tasks=5)

# 3. Send to team channel
send_to_slack(standup["report"])
send_to_slack(daily_tasks["suggested_tasks"])
```

**Pre-Commit Hook**:
```python
# Review changed files before commit
reviewer = CodeReviewSkill()
changed_files = get_git_changed_files()

for file in changed_files:
    result = reviewer.review_file(file)
    if result["total_issues"] > 0:
        print(f"⚠️  {file} has {result['total_issues']} issues")
        for issue in result["issues"]:
            if issue["severity"] in ["critical", "high"]:
                raise Exception("Critical issues found!")
```

**Database Migration Review**:
```python
# Review SQL before deployment
optimizer = DatabaseOptimizerSkill()

with open("migration.sql") as f:
    queries = f.read().split(";")

for query in queries:
    result = optimizer.analyze_query(query)
    if result["optimization_score"] < 70:
        print(f"⚠️  Query needs optimization: {result['recommendations']}")
```

---

## API Integration

All skills can be exposed as API endpoints:

```python
from fastapi import APIRouter
from app.skills import CodeReviewSkill

skills_router = APIRouter(prefix="/skills", tags=["skills"])

@skills_router.post("/code-review")
def review_code(file_path: str):
    reviewer = CodeReviewSkill()
    return reviewer.review_file(file_path)
```

---

## Testing

All skills include comprehensive test coverage in `tests/test_skills.py`.

Run tests:
```bash
pytest tests/test_skills.py -v
```

---

## Future Enhancements

Potential improvements for each skill:

1. **Code Review**:
   - Multi-language support (JavaScript, Java, etc.)
   - Integration with code quality tools (pylint, flake8)
   - AI-powered suggestions

2. **Database Optimizer**:
   - EXPLAIN plan analysis
   - Index recommendation
   - Query execution time estimation

3. **Test Generator**:
   - Integration with OpenAPI schemas
   - Snapshot testing generation
   - Mock data generation

4. **Standup Reporter**:
   - Integration with JIRA/Linear
   - Natural language processing for commit messages
   - Team-wide report aggregation

5. **Task Prioritizer**:
   - Machine learning for personalized prioritization
   - Dependency graph analysis
   - Historical completion time analysis

---

## Contributing

To add new skills:

1. Create a new file in `app/skills/`
2. Implement the skill class with clear methods
3. Add comprehensive docstrings
4. Create tests in `tests/test_skills.py`
5. Update this documentation
6. Add usage examples

---

## License

These skills are part of the AI-400 Class 1 Project and are provided for educational purposes.
