"""
Daily Workflow Skill 2: Task Prioritizer
Intelligently prioritizes tasks based on deadlines, dependencies,
effort estimates, and urgency using a scoring algorithm.
"""

from datetime import datetime
from typing import List, Dict, Optional
from enum import Enum


class PriorityLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class TaskPrioritizerSkill:
    """Automated task prioritization skill"""

    def __init__(self):
        self.priority_scores = {
            "urgent": 100,
            "high": 75,
            "medium": 50,
            "low": 25
        }

    def prioritize_tasks(self, tasks: List[Dict]) -> Dict[str, any]:
        """Prioritize a list of tasks"""
        scored_tasks = []

        for task in tasks:
            score = self._calculate_priority_score(task)
            scored_tasks.append({
                **task,
                "priority_score": score,
                "recommended_order": 0
            })

        scored_tasks.sort(key=lambda x: x["priority_score"], reverse=True)

        for idx, task in enumerate(scored_tasks, 1):
            task["recommended_order"] = idx

        recommendations = self._generate_recommendations(scored_tasks)

        return {
            "total_tasks": len(tasks),
            "prioritized_tasks": scored_tasks,
            "recommendations": recommendations,
            "status": "prioritized"
        }

    def _calculate_priority_score(self, task: Dict) -> float:
        """Calculate priority score for a task"""
        score = 0.0

        base_priority = task.get("priority", "medium").lower()
        score += self.priority_scores.get(base_priority, 50)

        due_date = task.get("due_date")
        if due_date:
            score += self._calculate_urgency_score(due_date)

        if task.get("status") == "in_progress":
            score += 20

        tags = task.get("tags", "")
        if tags:
            if "urgent" in tags.lower():
                score += 30
            if "critical" in tags.lower():
                score += 25
            if "blocked" in tags.lower():
                score -= 40

        description = task.get("description", "")
        if description:
            if "asap" in description.lower():
                score += 20
            if "deadline" in description.lower():
                score += 15

        return score

    def _calculate_urgency_score(self, due_date: str) -> float:
        """Calculate urgency score based on due date"""
        try:
            if isinstance(due_date, str):
                due = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
            else:
                due = due_date

            now = datetime.now(due.tzinfo) if due.tzinfo else datetime.now()
            days_until_due = (due - now).days

            if days_until_due < 0:
                return 50
            elif days_until_due == 0:
                return 45
            elif days_until_due == 1:
                return 40
            elif days_until_due <= 3:
                return 30
            elif days_until_due <= 7:
                return 20
            elif days_until_due <= 14:
                return 10
            else:
                return 5

        except Exception:
            return 0

    def _generate_recommendations(self, sorted_tasks: List[Dict]) -> List[str]:
        """Generate recommendations based on prioritized tasks"""
        recommendations = []

        if len(sorted_tasks) == 0:
            return ["No tasks to prioritize"]

        top_task = sorted_tasks[0]
        recommendations.append(
            f"🎯 Focus on: '{top_task.get('title', 'Untitled')}' (Score: {top_task['priority_score']:.1f})"
        )

        overdue_tasks = [
            t for t in sorted_tasks
            if self._is_overdue(t.get("due_date"))
        ]
        if overdue_tasks:
            recommendations.append(
                f"⚠️  {len(overdue_tasks)} overdue task(s) need immediate attention"
            )

        in_progress = [
            t for t in sorted_tasks
            if t.get("status") == "in_progress"
        ]
        if in_progress:
            recommendations.append(
                f"🔄 {len(in_progress)} task(s) currently in progress - consider completing before starting new ones"
            )

        urgent_tasks = [
            t for t in sorted_tasks[:5]
            if t.get("priority", "").lower() in ["urgent", "high"]
        ]
        if len(urgent_tasks) >= 3:
            recommendations.append(
                "🔥 Multiple high-priority tasks detected - consider delegation or timeline adjustment"
            )

        blocked_tasks = [
            t for t in sorted_tasks
            if "blocked" in t.get("tags", "").lower()
        ]
        if blocked_tasks:
            recommendations.append(
                f"🚧 {len(blocked_tasks)} blocked task(s) - address blockers to improve flow"
            )

        return recommendations

    def _is_overdue(self, due_date: Optional[str]) -> bool:
        """Check if a task is overdue"""
        if not due_date:
            return False

        try:
            if isinstance(due_date, str):
                due = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
            else:
                due = due_date

            now = datetime.now(due.tzinfo) if due.tzinfo else datetime.now()
            return due < now

        except Exception:
            return False

    def suggest_daily_tasks(self, all_tasks: List[Dict], max_tasks: int = 5) -> Dict[str, any]:
        """Suggest top tasks to focus on today"""
        result = self.prioritize_tasks(all_tasks)

        daily_tasks = result["prioritized_tasks"][:max_tasks]

        return {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "suggested_tasks": daily_tasks,
            "total_suggested": len(daily_tasks),
            "recommendations": result["recommendations"],
            "status": "suggested"
        }

    def estimate_daily_capacity(self, tasks: List[Dict]) -> Dict[str, any]:
        """Estimate if tasks fit within daily capacity"""
        result = self.prioritize_tasks(tasks)

        urgent_count = sum(
            1 for t in result["prioritized_tasks"]
            if t.get("priority", "").lower() in ["urgent", "high"]
        )

        capacity_warning = None
        if urgent_count > 5:
            capacity_warning = "⚠️  Too many high-priority tasks for one day - consider rescheduling"
        elif urgent_count > 3:
            capacity_warning = "⚡ Heavy workload today - stay focused and minimize distractions"
        else:
            capacity_warning = "✅ Workload appears manageable"

        return {
            "total_tasks": len(tasks),
            "urgent_high_priority": urgent_count,
            "capacity_assessment": capacity_warning,
            "top_5_tasks": result["prioritized_tasks"][:5],
            "status": "assessed"
        }


def main():
    """Example usage"""
    prioritizer = TaskPrioritizerSkill()

    sample_tasks = [
        {
            "id": 1,
            "title": "Fix critical production bug",
            "priority": "urgent",
            "status": "todo",
            "due_date": datetime.now().isoformat(),
            "tags": "critical,bug"
        },
        {
            "id": 2,
            "title": "Write documentation",
            "priority": "low",
            "status": "todo",
            "due_date": None,
            "tags": ""
        },
        {
            "id": 3,
            "title": "Review pull request",
            "priority": "medium",
            "status": "in_progress",
            "due_date": (datetime.now()).isoformat(),
            "tags": "review"
        }
    ]

    result = prioritizer.prioritize_tasks(sample_tasks)

    print("📊 Task Prioritization Results\n")
    for task in result["prioritized_tasks"]:
        print(f"{task['recommended_order']}. {task['title']}")
        print(f"   Priority Score: {task['priority_score']:.1f}")
        print()

    print("💡 Recommendations:")
    for rec in result["recommendations"]:
        print(f"   {rec}")


if __name__ == "__main__":
    main()
