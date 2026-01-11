"""
Technical Skill 1: Code Review Skill
Automates code review by analyzing Python files for common issues,
style violations, and potential bugs.
"""

import ast
import os
from typing import List, Dict
from pathlib import Path


class CodeReviewSkill:
    """Automated code review skill for Python files"""

    def __init__(self):
        self.issues = []

    def review_file(self, file_path: str) -> Dict[str, any]:
        """Review a single Python file"""
        self.issues = []

        if not os.path.exists(file_path):
            return {"error": f"File not found: {file_path}"}

        if not file_path.endswith('.py'):
            return {"error": "Only Python files are supported"}

        with open(file_path, 'r') as f:
            content = f.read()

        try:
            tree = ast.parse(content)
            self._analyze_ast(tree)
        except SyntaxError as e:
            self.issues.append({
                "type": "syntax_error",
                "severity": "critical",
                "line": e.lineno,
                "message": str(e)
            })

        self._check_style(content)

        return {
            "file": file_path,
            "total_issues": len(self.issues),
            "issues": self.issues,
            "status": "reviewed"
        }

    def _analyze_ast(self, tree: ast.AST):
        """Analyze AST for code issues"""
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if len(node.args.args) > 5:
                    self.issues.append({
                        "type": "too_many_parameters",
                        "severity": "medium",
                        "line": node.lineno,
                        "message": f"Function '{node.name}' has {len(node.args.args)} parameters (max recommended: 5)"
                    })

                if not ast.get_docstring(node):
                    self.issues.append({
                        "type": "missing_docstring",
                        "severity": "low",
                        "line": node.lineno,
                        "message": f"Function '{node.name}' missing docstring"
                    })

            elif isinstance(node, ast.Try):
                if len(node.handlers) == 0:
                    self.issues.append({
                        "type": "empty_exception_handler",
                        "severity": "high",
                        "line": node.lineno,
                        "message": "Try block without exception handlers"
                    })

                for handler in node.handlers:
                    if handler.type is None:
                        self.issues.append({
                            "type": "bare_except",
                            "severity": "high",
                            "line": handler.lineno,
                            "message": "Bare except clause (catches all exceptions)"
                        })

    def _check_style(self, content: str):
        """Check style guidelines"""
        lines = content.split('\n')

        for i, line in enumerate(lines, 1):
            if len(line) > 120:
                self.issues.append({
                    "type": "line_too_long",
                    "severity": "low",
                    "line": i,
                    "message": f"Line exceeds 120 characters ({len(line)} chars)"
                })

            if line.strip().startswith('import ') or line.strip().startswith('from '):
                if i > 1 and lines[i-2].strip() and not (
                    lines[i-2].strip().startswith('import ') or
                    lines[i-2].strip().startswith('from ')
                ):
                    self.issues.append({
                        "type": "import_not_at_top",
                        "severity": "medium",
                        "line": i,
                        "message": "Imports should be at the top of the file"
                    })

    def review_directory(self, directory_path: str) -> Dict[str, any]:
        """Review all Python files in a directory"""
        results = []
        path = Path(directory_path)

        for py_file in path.rglob('*.py'):
            result = self.review_file(str(py_file))
            results.append(result)

        total_issues = sum(r.get('total_issues', 0) for r in results)

        return {
            "directory": directory_path,
            "files_reviewed": len(results),
            "total_issues": total_issues,
            "results": results
        }


def main():
    """Example usage"""
    reviewer = CodeReviewSkill()
    result = reviewer.review_file("app/main.py")
    print(f"Review complete: {result['total_issues']} issues found")
    for issue in result['issues']:
        print(f"  Line {issue['line']}: [{issue['severity']}] {issue['message']}")


if __name__ == "__main__":
    main()
