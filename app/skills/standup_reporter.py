"""
Daily Workflow Skill 1: Daily Standup Reporter
Automates the creation of daily standup reports by analyzing
git commits, tasks completed, and work in progress.
"""

import subprocess
from datetime import datetime, timedelta
from typing import List, Dict
import re


class StandupReporterSkill:
    """Automated daily standup report generator"""

    def __init__(self):
        self.report = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "yesterday": [],
            "today": [],
            "blockers": []
        }

    def generate_report(self, git_repo_path: str = ".") -> Dict[str, any]:
        """Generate a complete standup report"""
        try:
            commits = self._get_yesterday_commits(git_repo_path)
            self._parse_commits(commits)
            self._identify_blockers(commits)

            formatted_report = self._format_report()

            return {
                "date": self.report["date"],
                "report": formatted_report,
                "total_commits": len(commits),
                "status": "generated"
            }

        except Exception as e:
            return {"error": str(e)}

    def _get_yesterday_commits(self, repo_path: str) -> List[str]:
        """Get commits from yesterday"""
        try:
            yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
            cmd = [
                "git", "-C", repo_path, "log",
                f"--since={yesterday} 00:00",
                f"--until={yesterday} 23:59",
                "--pretty=format:%s",
                "--author=$(git config user.name)"
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                shell=False
            )

            if result.returncode == 0:
                commits = [c for c in result.stdout.split('\n') if c.strip()]
                return commits
            return []

        except Exception:
            return []

    def _parse_commits(self, commits: List[str]):
        """Parse commits to extract work items"""
        for commit in commits:
            cleaned = self._clean_commit_message(commit)
            if cleaned:
                self.report["yesterday"].append(cleaned)

        if not self.report["yesterday"]:
            self.report["yesterday"].append("Continued work on ongoing projects")

    def _clean_commit_message(self, message: str) -> str:
        """Clean and format commit message"""
        message = re.sub(r'^(fix|feat|docs|style|refactor|test|chore):\s*', '', message, flags=re.IGNORECASE)
        message = re.sub(r'^(fixed|added|updated|removed|created)\s+', '', message, flags=re.IGNORECASE)

        message = message.strip()

        if message and not message[0].isupper():
            message = message[0].upper() + message[1:]

        return message

    def _identify_blockers(self, commits: List[str]):
        """Identify potential blockers from commit messages"""
        blocker_keywords = ['wip', 'todo', 'fixme', 'blocked', 'issue', 'bug']

        for commit in commits:
            lower_commit = commit.lower()
            for keyword in blocker_keywords:
                if keyword in lower_commit:
                    self.report["blockers"].append(
                        f"Potential blocker detected: {commit[:50]}..."
                    )
                    break

        if not self.report["blockers"]:
            self.report["blockers"].append("No blockers")

    def _format_report(self) -> str:
        """Format the standup report as a string"""
        report_lines = [
            f"📅 Daily Standup Report - {self.report['date']}",
            "",
            "✅ Yesterday:",
        ]

        for item in self.report["yesterday"]:
            report_lines.append(f"   • {item}")

        report_lines.extend([
            "",
            "🎯 Today:",
            "   • Continue ongoing tasks",
            "   • Address any blockers",
            "",
            "🚧 Blockers:",
        ])

        for blocker in self.report["blockers"]:
            report_lines.append(f"   • {blocker}")

        return "\n".join(report_lines)

    def generate_from_task_list(self, tasks: List[Dict]) -> Dict[str, any]:
        """Generate standup report from a list of tasks"""
        completed_yesterday = []
        in_progress = []
        blocked = []

        yesterday = datetime.now() - timedelta(days=1)

        for task in tasks:
            if task.get("status") == "completed":
                completed_date = task.get("updated_at", "")
                if isinstance(completed_date, str):
                    completed_date = datetime.fromisoformat(completed_date.replace('Z', '+00:00'))

                if completed_date.date() == yesterday.date():
                    completed_yesterday.append(task["title"])

            elif task.get("status") == "in_progress":
                in_progress.append(task["title"])

            elif task.get("status") == "blocked":
                blocked.append(task["title"])

        self.report["yesterday"] = completed_yesterday or ["Continued work on ongoing projects"]
        self.report["today"] = in_progress or ["Continue ongoing tasks"]
        self.report["blockers"] = blocked or ["No blockers"]

        formatted_report = self._format_task_report()

        return {
            "date": self.report["date"],
            "report": formatted_report,
            "completed_count": len(completed_yesterday),
            "in_progress_count": len(in_progress),
            "blockers_count": len(blocked),
            "status": "generated"
        }

    def _format_task_report(self) -> str:
        """Format task-based standup report"""
        report_lines = [
            f"📅 Daily Standup Report - {self.report['date']}",
            "",
            "✅ Yesterday:",
        ]

        for item in self.report["yesterday"]:
            report_lines.append(f"   • {item}")

        report_lines.extend([
            "",
            "🎯 Today:",
        ])

        for item in self.report["today"]:
            report_lines.append(f"   • {item}")

        report_lines.extend([
            "",
            "🚧 Blockers:",
        ])

        for blocker in self.report["blockers"]:
            report_lines.append(f"   • {blocker}")

        return "\n".join(report_lines)


def main():
    """Example usage"""
    reporter = StandupReporterSkill()

    sample_tasks = [
        {
            "title": "Implement user authentication",
            "status": "completed",
            "updated_at": (datetime.now() - timedelta(days=1)).isoformat()
        },
        {
            "title": "Write API documentation",
            "status": "in_progress",
            "updated_at": datetime.now().isoformat()
        }
    ]

    result = reporter.generate_from_task_list(sample_tasks)
    print(result["report"])


if __name__ == "__main__":
    main()
