"""
Technical Skill 2: Database Query Optimizer
Analyzes SQL queries and SQLModel code for performance issues
and provides optimization recommendations.
"""

import re
from typing import List, Dict, Tuple


class DatabaseOptimizerSkill:
    """Automated SQL query optimization skill"""

    def __init__(self):
        self.recommendations = []

    def analyze_query(self, query: str) -> Dict[str, any]:
        """Analyze a SQL query for optimization opportunities"""
        self.recommendations = []

        query_upper = query.upper()

        self._check_select_star(query)
        self._check_missing_where(query_upper)
        self._check_missing_limit(query_upper)
        self._check_or_conditions(query_upper)
        self._check_function_in_where(query)
        self._check_subqueries(query_upper)
        self._check_like_pattern(query)
        self._check_distinct_usage(query_upper)

        score = self._calculate_optimization_score()

        return {
            "query": query[:100] + "..." if len(query) > 100 else query,
            "optimization_score": score,
            "total_recommendations": len(self.recommendations),
            "recommendations": self.recommendations,
            "status": "analyzed"
        }

    def _check_select_star(self, query: str):
        """Check for SELECT * usage"""
        if re.search(r'SELECT\s+\*', query, re.IGNORECASE):
            self.recommendations.append({
                "type": "select_star",
                "severity": "medium",
                "issue": "Using SELECT * retrieves all columns",
                "recommendation": "Explicitly specify only the columns you need to reduce data transfer",
                "example": "SELECT id, name, email FROM users"
            })

    def _check_missing_where(self, query_upper: str):
        """Check for queries without WHERE clause"""
        if 'SELECT' in query_upper and 'FROM' in query_upper and 'WHERE' not in query_upper:
            if 'LIMIT' not in query_upper:
                self.recommendations.append({
                    "type": "missing_where",
                    "severity": "high",
                    "issue": "Query has no WHERE clause or LIMIT",
                    "recommendation": "Add WHERE clause to filter data or LIMIT to restrict results",
                    "example": "SELECT * FROM tasks WHERE status = 'active' LIMIT 100"
                })

    def _check_missing_limit(self, query_upper: str):
        """Check for missing LIMIT clause"""
        if 'SELECT' in query_upper and 'LIMIT' not in query_upper and 'WHERE' not in query_upper:
            self.recommendations.append({
                "type": "missing_limit",
                "severity": "medium",
                "issue": "No LIMIT clause found",
                "recommendation": "Add LIMIT to prevent accidentally retrieving too many rows",
                "example": "SELECT * FROM tasks LIMIT 100"
            })

    def _check_or_conditions(self, query_upper: str):
        """Check for multiple OR conditions"""
        or_count = query_upper.count(' OR ')
        if or_count > 3:
            self.recommendations.append({
                "type": "multiple_or",
                "severity": "medium",
                "issue": f"Query has {or_count} OR conditions",
                "recommendation": "Consider using IN clause instead of multiple ORs",
                "example": "WHERE status IN ('todo', 'in_progress', 'completed')"
            })

    def _check_function_in_where(self, query: str):
        """Check for function calls in WHERE clause"""
        if re.search(r'WHERE.*\b(UPPER|LOWER|SUBSTRING|DATE)\s*\(', query, re.IGNORECASE):
            self.recommendations.append({
                "type": "function_in_where",
                "severity": "high",
                "issue": "Function call in WHERE clause prevents index usage",
                "recommendation": "Avoid functions on indexed columns in WHERE clause",
                "example": "Use computed columns or store preprocessed values"
            })

    def _check_subqueries(self, query_upper: str):
        """Check for subqueries in SELECT clause"""
        select_part = query_upper.split('FROM')[0] if 'FROM' in query_upper else query_upper
        if select_part.count('SELECT') > 1:
            self.recommendations.append({
                "type": "subquery_in_select",
                "severity": "medium",
                "issue": "Subquery in SELECT clause",
                "recommendation": "Consider using JOINs instead of subqueries for better performance",
                "example": "SELECT t.*, u.name FROM tasks t JOIN users u ON t.user_id = u.id"
            })

    def _check_like_pattern(self, query: str):
        """Check for inefficient LIKE patterns"""
        if re.search(r"LIKE\s+['\"]%", query, re.IGNORECASE):
            self.recommendations.append({
                "type": "leading_wildcard",
                "severity": "high",
                "issue": "LIKE pattern starts with wildcard (%)",
                "recommendation": "Leading wildcards prevent index usage. Consider full-text search",
                "example": "Use LIKE 'pattern%' or full-text search indexes"
            })

    def _check_distinct_usage(self, query_upper: str):
        """Check for DISTINCT usage"""
        if 'DISTINCT' in query_upper:
            self.recommendations.append({
                "type": "distinct_usage",
                "severity": "low",
                "issue": "DISTINCT requires sorting and deduplication",
                "recommendation": "Verify if DISTINCT is necessary or if the data model can prevent duplicates",
                "example": "Consider using GROUP BY or fixing the join logic"
            })

    def _calculate_optimization_score(self) -> int:
        """Calculate optimization score (0-100)"""
        if not self.recommendations:
            return 100

        severity_weights = {"low": 5, "medium": 15, "high": 25}
        penalty = sum(severity_weights.get(r['severity'], 10) for r in self.recommendations)

        score = max(0, 100 - penalty)
        return score

    def analyze_sqlmodel_code(self, code: str) -> Dict[str, any]:
        """Analyze SQLModel query code"""
        self.recommendations = []

        if '.all()' in code and 'limit' not in code.lower():
            self.recommendations.append({
                "type": "missing_limit",
                "severity": "medium",
                "issue": "Using .all() without limit",
                "recommendation": "Add .limit() to prevent loading excessive data",
                "example": "statement.limit(100)"
            })

        if 'select(' in code and not re.search(r'select\([A-Za-z_]+\)', code):
            self.recommendations.append({
                "type": "missing_specific_columns",
                "severity": "low",
                "issue": "Consider selecting specific columns",
                "recommendation": "Use select with specific columns for better performance",
                "example": "select(Task.id, Task.title)"
            })

        return {
            "code_snippet": code[:100] + "..." if len(code) > 100 else code,
            "total_recommendations": len(self.recommendations),
            "recommendations": self.recommendations,
            "status": "analyzed"
        }


def main():
    """Example usage"""
    optimizer = DatabaseOptimizerSkill()

    query = "SELECT * FROM tasks WHERE UPPER(title) LIKE '%urgent%'"
    result = optimizer.analyze_query(query)

    print(f"Optimization Score: {result['optimization_score']}/100")
    print(f"Recommendations: {result['total_recommendations']}")
    for rec in result['recommendations']:
        print(f"\n[{rec['severity'].upper()}] {rec['issue']}")
        print(f"  → {rec['recommendation']}")


if __name__ == "__main__":
    main()
