"""
Demo data script to populate the database with sample tasks
for demonstration purposes.
"""

import requests
from datetime import datetime, timedelta

API_BASE_URL = "http://localhost:8000"


def create_demo_tasks():
    """Create sample tasks for demo"""
    tasks = [
        {
            "title": "Implement user authentication",
            "description": "Add JWT-based authentication to the API",
            "status": "in_progress",
            "priority": "high",
            "due_date": (datetime.now() + timedelta(days=2)).isoformat(),
            "tags": "security,backend,api"
        },
        {
            "title": "Write API documentation",
            "description": "Create comprehensive API documentation with examples",
            "status": "todo",
            "priority": "medium",
            "due_date": (datetime.now() + timedelta(days=5)).isoformat(),
            "tags": "documentation,api"
        },
        {
            "title": "Fix bug in task filtering",
            "description": "Tasks with multiple tags not filtering correctly",
            "status": "todo",
            "priority": "urgent",
            "due_date": datetime.now().isoformat(),
            "tags": "bug,urgent,backend"
        },
        {
            "title": "Add task comments feature",
            "description": "Allow users to add comments to tasks",
            "status": "todo",
            "priority": "low",
            "due_date": (datetime.now() + timedelta(days=14)).isoformat(),
            "tags": "feature,backend"
        },
        {
            "title": "Implement task search",
            "description": "Add full-text search capability for tasks",
            "status": "todo",
            "priority": "medium",
            "due_date": (datetime.now() + timedelta(days=7)).isoformat(),
            "tags": "feature,search"
        },
        {
            "title": "Set up CI/CD pipeline",
            "description": "Configure GitHub Actions for automated testing and deployment",
            "status": "completed",
            "priority": "high",
            "tags": "devops,automation"
        },
        {
            "title": "Optimize database queries",
            "description": "Review and optimize slow queries identified in production",
            "status": "in_progress",
            "priority": "high",
            "due_date": (datetime.now() + timedelta(days=3)).isoformat(),
            "tags": "performance,database"
        },
        {
            "title": "Create user dashboard",
            "description": "Design and implement user dashboard with task statistics",
            "status": "todo",
            "priority": "medium",
            "due_date": (datetime.now() + timedelta(days=10)).isoformat(),
            "tags": "frontend,ui"
        }
    ]

    created_tasks = []
    for task in tasks:
        try:
            response = requests.post(f"{API_BASE_URL}/tasks/", json=task)
            if response.status_code == 201:
                created_task = response.json()
                created_tasks.append(created_task)
                print(f"✓ Created: {task['title']}")
            else:
                print(f"✗ Failed to create: {task['title']} - {response.status_code}")
        except Exception as e:
            print(f"✗ Error creating task: {e}")

    return created_tasks


def display_task_summary():
    """Display summary of all tasks"""
    try:
        response = requests.get(f"{API_BASE_URL}/tasks/")
        if response.status_code == 200:
            tasks = response.json()
            print(f"\n📊 Task Summary:")
            print(f"   Total Tasks: {len(tasks)}")

            statuses = {}
            priorities = {}

            for task in tasks:
                status = task.get('status', 'unknown')
                priority = task.get('priority', 'unknown')

                statuses[status] = statuses.get(status, 0) + 1
                priorities[priority] = priorities.get(priority, 0) + 1

            print(f"\n   By Status:")
            for status, count in statuses.items():
                print(f"     - {status}: {count}")

            print(f"\n   By Priority:")
            for priority, count in priorities.items():
                print(f"     - {priority}: {count}")

    except Exception as e:
        print(f"✗ Error fetching tasks: {e}")


def clear_all_tasks():
    """Clear all tasks from the database"""
    try:
        response = requests.get(f"{API_BASE_URL}/tasks/")
        if response.status_code == 200:
            tasks = response.json()
            for task in tasks:
                delete_response = requests.delete(f"{API_BASE_URL}/tasks/{task['id']}")
                if delete_response.status_code == 204:
                    print(f"✓ Deleted: {task['title']}")
                else:
                    print(f"✗ Failed to delete: {task['title']}")
    except Exception as e:
        print(f"✗ Error clearing tasks: {e}")


def main():
    """Main demo data script"""
    print("=" * 60)
    print("Task Management API - Demo Data Script")
    print("=" * 60)

    print("\n🚀 Creating demo tasks...")
    created = create_demo_tasks()

    print(f"\n✅ Successfully created {len(created)} tasks")

    display_task_summary()

    print("\n" + "=" * 60)
    print("Demo data loaded successfully!")
    print("Open http://localhost:8000/docs to explore the API")
    print("=" * 60)


if __name__ == "__main__":
    main()
