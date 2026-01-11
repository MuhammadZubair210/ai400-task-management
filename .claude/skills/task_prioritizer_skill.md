# Task Prioritizer Skill

**Type**: Workflow Skill
**Purpose**: Intelligent task prioritization using multi-factor scoring

## Overview

This skill intelligently prioritizes tasks based on deadlines, dependencies, effort estimates, and urgency using a sophisticated scoring algorithm. It helps you focus on what matters most by calculating priority scores and providing actionable recommendations.

## Capabilities

- Multi-factor priority scoring algorithm
- Due date urgency calculation
- Status-based prioritization
- Tag-based priority boosting
- Overdue task detection
- Daily capacity estimation
- Actionable recommendations
- Workload balancing suggestions
- Blocker identification

## Scoring Algorithm

The skill uses a comprehensive scoring system:

**Base Priority Scores:**
- Urgent: 100 points
- High: 75 points
- Medium: 50 points
- Low: 25 points

**Due Date Urgency (0-50 points):**
- Overdue: +50 points
- Due today: +45 points
- Due tomorrow: +40 points
- Due in 2-3 days: +30 points
- Due in 4-7 days: +20 points
- Due in 8-14 days: +10 points
- Due later: +5 points

**Status Modifiers:**
- In Progress: +20 points (continue what you started)

**Tag Modifiers:**
- "urgent" tag: +30 points
- "critical" tag: +25 points
- "blocked" tag: -40 points (deprioritize until unblocked)

**Description Keywords:**
- "asap": +20 points
- "deadline": +15 points

## Usage

### Basic Prioritization

```bash
python -m app.skills.task_prioritizer
```

Or programmatically:

```python
from app.skills.task_prioritizer import TaskPrioritizerSkill

prioritizer = TaskPrioritizerSkill()

tasks = [
    {
        "title": "Fix critical bug",
        "priority": "urgent",
        "status": "todo",
        "due_date": "2024-01-10T17:00:00",
        "tags": "critical,bug"
    },
    {
        "title": "Write documentation",
        "priority": "low",
        "status": "todo",
        "due_date": None,
        "tags": ""
    },
    {
        "title": "Review pull request",
        "priority": "medium",
        "status": "in_progress",
        "due_date": "2024-01-11T12:00:00",
        "tags": "review"
    }
]

result = prioritizer.prioritize_tasks(tasks)

for task in result["prioritized_tasks"]:
    print(f"{task['recommended_order']}. {task['title']}")
    print(f"   Score: {task['priority_score']:.1f}")
```

### Daily Task Suggestions

```python
# Get top 5 tasks to focus on today
result = prioritizer.suggest_daily_tasks(all_tasks, max_tasks=5)

print(f"📋 Focus on these {result['total_suggested']} tasks today:")
for task in result["suggested_tasks"]:
    print(f"  • {task['title']} (Score: {task['priority_score']:.1f})")
```

### Capacity Estimation

```python
result = prioritizer.estimate_daily_capacity(tasks)

print(result["capacity_assessment"])
# Output: "✅ Workload appears manageable"
# or "⚠️ Too many high-priority tasks for one day"
# or "⚡ Heavy workload today - stay focused"

print(f"High-priority tasks: {result['urgent_high_priority']}")
```

## Output Format

```json
{
  "total_tasks": 10,
  "prioritized_tasks": [
    {
      "id": 1,
      "title": "Fix critical bug",
      "priority": "urgent",
      "priority_score": 165.0,
      "recommended_order": 1
    }
  ],
  "recommendations": [
    "🎯 Focus on: 'Fix critical bug' (Score: 165.0)",
    "⚠️ 2 overdue task(s) need immediate attention",
    "🔄 3 task(s) currently in progress - consider completing before starting new ones"
  ],
  "status": "prioritized"
}
```

## Recommendations Generated

The skill provides intelligent recommendations:

- **Top Priority**: Identifies the most important task to focus on
- **Overdue Warnings**: Alerts you to tasks past their deadline
- **In-Progress Reminders**: Encourages completing started tasks
- **Capacity Overload**: Warns when too many urgent tasks exist
- **Blocker Notifications**: Highlights tasks that are blocked

## Real-World Applications

- **Daily Work Planning**: Start each day with clear priorities
- **Sprint Planning**: Assist in sprint backlog prioritization
- **Time Management**: Optimize time allocation across tasks
- **Workload Balancing**: Prevent burnout with capacity estimation
- **Team Coordination**: Share prioritized lists with team members
- **Manager Reports**: Show what you're focusing on and why
- **Deadline Management**: Never miss critical deadlines
- **Context Switching**: Minimize by focusing on top priorities

## Integration Examples

### Morning Workflow

```python
# 1. Get daily task suggestions
daily_plan = prioritizer.suggest_daily_tasks(all_tasks, max_tasks=5)

# 2. Check capacity
capacity = prioritizer.estimate_daily_capacity(daily_plan["suggested_tasks"])

# 3. Send to calendar/task manager
for task in daily_plan["suggested_tasks"]:
    add_to_calendar(task)
```

### With Standup Reporter

```python
from app.skills import StandupReporterSkill, TaskPrioritizerSkill

# Generate standup
standup = StandupReporterSkill().generate_report()

# Prioritize today's tasks
prioritizer = TaskPrioritizerSkill()
priorities = prioritizer.suggest_daily_tasks(today_tasks, max_tasks=5)

# Combine into morning briefing
briefing = f"{standup['report']}\n\n{priorities['recommendations']}"
send_to_slack(briefing)
```

## Example Output

```
📊 Task Prioritization Results

1. Fix critical production bug
   Priority Score: 165.0

2. Submit client deliverable
   Priority Score: 145.0

3. Review urgent pull request
   Priority Score: 125.0

4. Update documentation
   Priority Score: 55.0

5. Refactor legacy code
   Priority Score: 30.0

💡 Recommendations:
   🎯 Focus on: 'Fix critical production bug' (Score: 165.0)
   ⚠️ 1 overdue task(s) need immediate attention
   🔄 2 task(s) currently in progress - consider completing before starting new ones
   🔥 Multiple high-priority tasks detected - consider delegation or timeline adjustment
```
