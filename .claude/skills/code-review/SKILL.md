# Code Review Skill

**Type**: Technical Skill
**Purpose**: Automated Python code quality analysis

## Overview

This skill automatically analyzes Python code for quality issues, style violations, and potential bugs using AST (Abstract Syntax Tree) analysis.

## Capabilities

- Detects functions with too many parameters (>5)
- Identifies missing docstrings
- Finds bare except clauses
- Checks for empty exception handlers
- Validates line length (max 120 chars)
- Verifies import placement at top of file

## Usage

```bash
python -m app.skills.code_review
```

Or programmatically:

```python
from app.skills.code_review import CodeReviewSkill

reviewer = CodeReviewSkill()
result = reviewer.review_file("path/to/file.py")

print(f"Total issues: {result['total_issues']}")
for issue in result['issues']:
    print(f"Line {issue['line']}: [{issue['severity']}] {issue['message']}")
```

## Output Format

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

## Severity Levels

- **critical**: Syntax errors that prevent execution
- **high**: Serious issues like bare except clauses
- **medium**: Code smells like too many parameters
- **low**: Style issues like missing docstrings

## Real-World Applications

- Pre-commit hooks for code quality
- CI/CD pipeline integration
- Automated code review in pull requests
- Developer training and feedback
