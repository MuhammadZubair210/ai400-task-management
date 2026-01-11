"""
Technical Skill 3: API Test Generator
Automatically generates pytest test cases for FastAPI endpoints
by analyzing route definitions.
"""

import ast
import re
from typing import List, Dict


class TestGeneratorSkill:
    """Automated test case generator for FastAPI endpoints"""

    def __init__(self):
        self.tests = []

    def generate_tests_from_file(self, file_path: str) -> Dict[str, any]:
        """Generate test cases from a FastAPI router file"""
        self.tests = []

        try:
            with open(file_path, 'r') as f:
                content = f.read()

            tree = ast.parse(content)
            self._analyze_routes(tree, content)

            test_code = self._generate_test_code()

            return {
                "source_file": file_path,
                "endpoints_found": len(self.tests),
                "test_code": test_code,
                "status": "generated"
            }

        except Exception as e:
            return {"error": str(e)}

    def _analyze_routes(self, tree: ast.AST, content: str):
        """Analyze AST to find route decorators"""
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                for decorator in node.decorator_list:
                    route_info = self._extract_route_info(decorator, node)
                    if route_info:
                        self.tests.append(route_info)

    def _extract_route_info(self, decorator: ast.expr, func_node: ast.FunctionDef) -> Dict:
        """Extract route information from decorator"""
        if isinstance(decorator, ast.Attribute):
            if decorator.attr in ['get', 'post', 'put', 'delete', 'patch']:
                method = decorator.attr.upper()
                path = "/"

                if isinstance(decorator.value, ast.Name):
                    router_name = decorator.value.id

                return {
                    "method": method,
                    "path": path,
                    "function_name": func_node.name,
                    "parameters": [arg.arg for arg in func_node.args.args]
                }

        elif isinstance(decorator, ast.Call):
            if isinstance(decorator.func, ast.Attribute):
                method = decorator.func.attr.upper()
                path = "/"

                if decorator.args and isinstance(decorator.args[0], ast.Constant):
                    path = decorator.args[0].value

                return {
                    "method": method,
                    "path": path,
                    "function_name": func_node.name,
                    "parameters": [arg.arg for arg in func_node.args.args]
                }

        return None

    def _generate_test_code(self) -> str:
        """Generate complete pytest test code"""
        imports = '''import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

'''

        test_functions = []

        for test_info in self.tests:
            test_func = self._generate_test_function(test_info)
            test_functions.append(test_func)

        return imports + '\n\n'.join(test_functions)

    def _generate_test_function(self, test_info: Dict) -> str:
        """Generate a single test function"""
        method = test_info['method']
        path = test_info['path']
        func_name = test_info['function_name']

        test_name = f"test_{func_name}"

        if method == 'GET':
            return self._generate_get_test(test_name, path)
        elif method == 'POST':
            return self._generate_post_test(test_name, path)
        elif method == 'PUT':
            return self._generate_put_test(test_name, path)
        elif method == 'DELETE':
            return self._generate_delete_test(test_name, path)
        else:
            return f"def {test_name}():\n    # TODO: Implement test for {method} {path}\n    pass"

    def _generate_get_test(self, test_name: str, path: str) -> str:
        """Generate GET endpoint test"""
        has_param = '{' in path
        if has_param:
            path_test = re.sub(r'\{[^}]+\}', '1', path)
        else:
            path_test = path

        return f'''def {test_name}():
    """Test GET {path}"""
    response = client.get("{path_test}")
    assert response.status_code in [200, 404]
    if response.status_code == 200:
        assert response.json() is not None'''

    def _generate_post_test(self, test_name: str, path: str) -> str:
        """Generate POST endpoint test"""
        return f'''def {test_name}():
    """Test POST {path}"""
    test_data = {{
        # TODO: Add appropriate test data
    }}
    response = client.post("{path}", json=test_data)
    assert response.status_code in [201, 422]
    if response.status_code == 201:
        assert "id" in response.json()'''

    def _generate_put_test(self, test_name: str, path: str) -> str:
        """Generate PUT endpoint test"""
        has_param = '{' in path
        if has_param:
            path_test = re.sub(r'\{[^}]+\}', '1', path)
        else:
            path_test = path

        return f'''def {test_name}():
    """Test PUT {path}"""
    update_data = {{
        # TODO: Add appropriate update data
    }}
    response = client.put("{path_test}", json=update_data)
    assert response.status_code in [200, 404, 422]'''

    def _generate_delete_test(self, test_name: str, path: str) -> str:
        """Generate DELETE endpoint test"""
        has_param = '{' in path
        if has_param:
            path_test = re.sub(r'\{[^}]+\}', '1', path)
        else:
            path_test = path

        return f'''def {test_name}():
    """Test DELETE {path}"""
    response = client.delete("{path_test}")
    assert response.status_code in [204, 404]'''

    def generate_tests_for_model(self, model_name: str, base_path: str) -> str:
        """Generate comprehensive CRUD tests for a model"""
        return f'''import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


@pytest.fixture
def sample_{model_name.lower()}():
    """Fixture providing sample {model_name} data"""
    return {{
        # TODO: Add sample data for {model_name}
    }}


def test_create_{model_name.lower()}(sample_{model_name.lower()}):
    """Test creating a new {model_name}"""
    response = client.post("{base_path}", json=sample_{model_name.lower()})
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    return data["id"]


def test_get_{model_name.lower()}s():
    """Test retrieving all {model_name}s"""
    response = client.get("{base_path}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_{model_name.lower()}_by_id():
    """Test retrieving a specific {model_name}"""
    response = client.get("{base_path}/1")
    assert response.status_code in [200, 404]


def test_update_{model_name.lower()}(sample_{model_name.lower()}):
    """Test updating a {model_name}"""
    response = client.put("{base_path}/1", json=sample_{model_name.lower()})
    assert response.status_code in [200, 404, 422]


def test_delete_{model_name.lower()}():
    """Test deleting a {model_name}"""
    response = client.delete("{base_path}/1")
    assert response.status_code in [204, 404]
'''


def main():
    """Example usage"""
    generator = TestGeneratorSkill()

    result = generator.generate_tests_for_model("Task", "/tasks")
    print("Generated Test Code:")
    print(result)


if __name__ == "__main__":
    main()
