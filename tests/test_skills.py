import pytest
from datetime import datetime, timedelta
from app.skills import (
    CodeReviewSkill,
    DatabaseOptimizerSkill,
    TestGeneratorSkill,
    StandupReporterSkill,
    TaskPrioritizerSkill
)


class TestCodeReviewSkill:
    """Test Code Review Skill"""

    def test_review_file_python(self, tmp_path):
        """Test reviewing a Python file"""
        test_file = tmp_path / "test.py"
        test_file.write_text("""
def function_with_many_params(a, b, c, d, e, f, g):
    return a + b + c

import os

try:
    pass
except:
    pass
""")

        reviewer = CodeReviewSkill()
        result = reviewer.review_file(str(test_file))

        assert result["status"] == "reviewed"
        assert result["total_issues"] > 0
        assert any(issue["type"] == "too_many_parameters" for issue in result["issues"])

    def test_review_nonexistent_file(self):
        """Test reviewing a file that doesn't exist"""
        reviewer = CodeReviewSkill()
        result = reviewer.review_file("nonexistent.py")
        assert "error" in result

    def test_review_non_python_file(self):
        """Test reviewing a non-Python file"""
        reviewer = CodeReviewSkill()
        result = reviewer.review_file("test.txt")
        assert "error" in result


class TestDatabaseOptimizerSkill:
    """Test Database Optimizer Skill"""

    def test_analyze_select_star(self):
        """Test detecting SELECT * usage"""
        optimizer = DatabaseOptimizerSkill()
        query = "SELECT * FROM tasks WHERE id = 1"
        result = optimizer.analyze_query(query)

        assert result["status"] == "analyzed"
        assert any(r["type"] == "select_star" for r in result["recommendations"])

    def test_analyze_missing_where(self):
        """Test detecting missing WHERE clause"""
        optimizer = DatabaseOptimizerSkill()
        query = "SELECT id, title FROM tasks"
        result = optimizer.analyze_query(query)

        assert result["total_recommendations"] > 0

    def test_analyze_like_pattern(self):
        """Test detecting inefficient LIKE patterns"""
        optimizer = DatabaseOptimizerSkill()
        query = "SELECT * FROM tasks WHERE title LIKE '%search%'"
        result = optimizer.analyze_query(query)

        assert any(r["type"] == "leading_wildcard" for r in result["recommendations"])

    def test_optimization_score(self):
        """Test optimization score calculation"""
        optimizer = DatabaseOptimizerSkill()
        good_query = "SELECT id, title FROM tasks WHERE status = 'active' LIMIT 100"
        result = optimizer.analyze_query(good_query)

        assert result["optimization_score"] >= 50

    def test_analyze_sqlmodel_code(self):
        """Test analyzing SQLModel code"""
        optimizer = DatabaseOptimizerSkill()
        code = "session.exec(select(Task)).all()"
        result = optimizer.analyze_sqlmodel_code(code)

        assert result["status"] == "analyzed"
        assert any(r["type"] == "missing_limit" for r in result["recommendations"])


class TestTestGeneratorSkill:
    """Test Test Generator Skill"""

    def test_generate_tests_for_model(self):
        """Test generating tests for a model"""
        generator = TestGeneratorSkill()
        result = generator.generate_tests_for_model("Task", "/tasks")

        assert "import pytest" in result
        assert "TestClient" in result
        assert "test_create_task" in result
        assert "test_get_tasks" in result
        assert "test_update_task" in result
        assert "test_delete_task" in result

    def test_generate_get_test(self):
        """Test generating GET test"""
        generator = TestGeneratorSkill()
        test_code = generator._generate_get_test("test_get_item", "/items/1")

        assert "def test_get_item" in test_code
        assert "client.get" in test_code
        assert "assert response.status_code" in test_code

    def test_generate_post_test(self):
        """Test generating POST test"""
        generator = TestGeneratorSkill()
        test_code = generator._generate_post_test("test_create_item", "/items")

        assert "def test_create_item" in test_code
        assert "client.post" in test_code
        assert "test_data" in test_code


class TestStandupReporterSkill:
    """Test Standup Reporter Skill"""

    def test_generate_from_task_list(self):
        """Test generating standup from task list"""
        reporter = StandupReporterSkill()

        yesterday = datetime.now() - timedelta(days=1)
        tasks = [
            {
                "title": "Implement feature X",
                "status": "completed",
                "updated_at": yesterday.isoformat()
            },
            {
                "title": "Write tests",
                "status": "in_progress",
                "updated_at": datetime.now().isoformat()
            }
        ]

        result = reporter.generate_from_task_list(tasks)

        assert result["status"] == "generated"
        assert result["completed_count"] == 1
        assert result["in_progress_count"] == 1
        assert "Daily Standup Report" in result["report"]

    def test_format_report(self):
        """Test report formatting"""
        reporter = StandupReporterSkill()
        reporter.report["yesterday"] = ["Task 1", "Task 2"]
        reporter.report["blockers"] = ["No blockers"]

        formatted = reporter._format_report()

        assert "Yesterday:" in formatted
        assert "Today:" in formatted
        assert "Blockers:" in formatted

    def test_clean_commit_message(self):
        """Test cleaning commit messages"""
        reporter = StandupReporterSkill()

        cleaned = reporter._clean_commit_message("fix: Fixed authentication bug")
        assert cleaned == "Authentication bug"  # "Fixed" gets removed as a prefix

        cleaned = reporter._clean_commit_message("added new feature")
        assert cleaned == "New feature"


class TestTaskPrioritizerSkill:
    """Test Task Prioritizer Skill"""

    def test_prioritize_tasks_basic(self):
        """Test basic task prioritization"""
        prioritizer = TaskPrioritizerSkill()

        tasks = [
            {
                "id": 1,
                "title": "Low priority task",
                "priority": "low",
                "status": "todo"
            },
            {
                "id": 2,
                "title": "Urgent task",
                "priority": "urgent",
                "status": "todo"
            },
            {
                "id": 3,
                "title": "Medium priority task",
                "priority": "medium",
                "status": "todo"
            }
        ]

        result = prioritizer.prioritize_tasks(tasks)

        assert result["status"] == "prioritized"
        assert result["total_tasks"] == 3
        assert result["prioritized_tasks"][0]["priority"] == "urgent"
        assert result["prioritized_tasks"][0]["recommended_order"] == 1

    def test_prioritize_with_due_dates(self):
        """Test prioritization with due dates"""
        prioritizer = TaskPrioritizerSkill()

        today = datetime.now()
        tasks = [
            {
                "id": 1,
                "title": "Task due today",
                "priority": "medium",
                "status": "todo",
                "due_date": today.isoformat()
            },
            {
                "id": 2,
                "title": "Task due next week",
                "priority": "medium",
                "status": "todo",
                "due_date": (today + timedelta(days=7)).isoformat()
            }
        ]

        result = prioritizer.prioritize_tasks(tasks)

        assert result["prioritized_tasks"][0]["title"] == "Task due today"

    def test_calculate_urgency_score(self):
        """Test urgency score calculation"""
        prioritizer = TaskPrioritizerSkill()

        today = datetime.now().isoformat()
        score = prioritizer._calculate_urgency_score(today)
        assert score > 30

        future = (datetime.now() + timedelta(days=30)).isoformat()
        score = prioritizer._calculate_urgency_score(future)
        assert score < 10

    def test_suggest_daily_tasks(self):
        """Test daily task suggestions"""
        prioritizer = TaskPrioritizerSkill()

        tasks = [
            {"id": i, "title": f"Task {i}", "priority": "medium", "status": "todo"}
            for i in range(10)
        ]

        result = prioritizer.suggest_daily_tasks(tasks, max_tasks=5)

        assert result["status"] == "suggested"
        assert result["total_suggested"] == 5
        assert len(result["suggested_tasks"]) == 5

    def test_estimate_daily_capacity(self):
        """Test daily capacity estimation"""
        prioritizer = TaskPrioritizerSkill()

        tasks = [
            {"id": i, "title": f"Urgent {i}", "priority": "urgent", "status": "todo"}
            for i in range(6)
        ]

        result = prioritizer.estimate_daily_capacity(tasks)

        assert result["status"] == "assessed"
        assert result["urgent_high_priority"] == 6
        assert "capacity_assessment" in result

    def test_is_overdue(self):
        """Test overdue detection"""
        prioritizer = TaskPrioritizerSkill()

        past_date = (datetime.now() - timedelta(days=1)).isoformat()
        assert prioritizer._is_overdue(past_date) is True

        future_date = (datetime.now() + timedelta(days=1)).isoformat()
        assert prioritizer._is_overdue(future_date) is False

        assert prioritizer._is_overdue(None) is False
