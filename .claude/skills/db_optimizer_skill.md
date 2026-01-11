# Database Query Optimizer Skill

**Type**: Technical Skill
**Purpose**: SQL query performance analysis and optimization recommendations

## Overview

Analyzes SQL queries and SQLModel code for performance issues and provides actionable optimization recommendations with a scoring system (0-100).

## Capabilities

- Detects SELECT * usage
- Identifies missing WHERE clauses
- Flags missing LIMIT clauses
- Detects multiple OR conditions (suggests IN clause)
- Identifies function calls in WHERE clause
- Finds subqueries in SELECT
- Detects leading wildcards in LIKE patterns
- Checks DISTINCT usage
- Calculates optimization score (0-100)

## Usage

```bash
python -m app.skills.db_optimizer
```

Or programmatically:

```python
from app.skills.db_optimizer import DatabaseOptimizerSkill

optimizer = DatabaseOptimizerSkill()
result = optimizer.analyze_query(
    "SELECT * FROM tasks WHERE UPPER(title) LIKE '%urgent%'"
)

print(f"Optimization Score: {result['optimization_score']}/100")
for rec in result['recommendations']:
    print(f"[{rec['severity']}] {rec['issue']}")
    print(f"  → {rec['recommendation']}")
```

## Output Format

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

## Optimization Score Ranges

- **90-100**: Excellent optimization
- **70-89**: Good optimization
- **50-69**: Moderate optimization needed
- **0-49**: Significant optimization needed

## Real-World Applications

- Performance optimization reviews
- Database query auditing
- Developer training on SQL best practices
- Automated performance monitoring
- Pre-deployment query validation
