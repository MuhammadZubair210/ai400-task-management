# Daily Standup Reporter Skill

**Type**: Workflow Skill
**Purpose**: Automated daily standup report generation

## Overview

This skill automates the creation of daily standup reports by analyzing git commits and task completion data. It eliminates the need to manually prepare standup updates by extracting work information from your development activity.

## Capabilities

- Extracts yesterday's git commits automatically
- Cleans and formats commit messages
- Identifies potential blockers from keywords
- Generates formatted standup reports
- Supports task-based report generation
- Provides statistics on completed work
- Detects work-in-progress items
- Suggests today's tasks based on context

## Usage

### From Git Commits

```bash
python -m app.skills.standup_reporter
```

Or programmatically:

```python
from app.skills.standup_reporter import StandupReporterSkill

reporter = StandupReporterSkill()
result = reporter.generate_report(".")

print(result["report"])
print(f"Total commits analyzed: {result['total_commits']}")
```

### From Task List

```python
from app.skills.standup_reporter import StandupReporterSkill
from datetime import datetime, timedelta

reporter = StandupReporterSkill()

tasks = [
    {
        "title": "Implement authentication",
        "status": "completed",
        "updated_at": (datetime.now() - timedelta(days=1)).isoformat()
    },
    {
        "title": "Write tests",
        "status": "in_progress",
        "updated_at": datetime.now().isoformat()
    },
    {
        "title": "Fix critical bug",
        "status": "blocked",
        "updated_at": datetime.now().isoformat()
    }
]

result = reporter.generate_from_task_list(tasks)
print(result["report"])
```

## Report Format

```
📅 Daily Standup Report - 2024-01-10

✅ Yesterday:
   • Implemented user authentication
   • Fixed critical bug in task filtering
   • Updated API documentation
   • Added unit tests for user service

🎯 Today:
   • Continue work on task search feature
   • Review pull requests
   • Address feedback from code review

🚧 Blockers:
   • No blockers
```

## Output Format

```json
{
  "date": "2024-01-10",
  "report": "📅 Daily Standup Report...",
  "total_commits": 8,
  "status": "generated"
}
```

### Task-Based Output

```json
{
  "date": "2024-01-10",
  "report": "📅 Daily Standup Report...",
  "completed_count": 3,
  "in_progress_count": 2,
  "blockers_count": 1,
  "status": "generated"
}
```

## Commit Message Cleaning

The skill automatically cleans commit messages by:
- Removing conventional commit prefixes (fix:, feat:, docs:, etc.)
- Removing redundant action words (fixed, added, updated, etc.)
- Capitalizing first letter
- Trimming whitespace

**Before**: `feat: added user authentication feature`
**After**: `User authentication feature`

## Blocker Detection

Automatically identifies potential blockers by detecting keywords:
- wip (work in progress)
- todo
- fixme
- blocked
- issue
- bug

## Real-World Applications

- Automate daily standup preparation (save 5-10 minutes daily)
- Consistent standup format across team
- Track team progress automatically
- Generate weekly summaries from daily reports
- Integration with Slack/Teams for automated posting
- Manager reports and status updates
- Sprint retrospectives with historical data
- Time tracking and accountability
