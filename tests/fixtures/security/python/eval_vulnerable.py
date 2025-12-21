"""
Test Fixture: Eval/Exec Vulnerable Patterns (Python)

This file contains 3+ dynamic code execution patterns that MUST be detected by
SEC-004 rule (devforgeai/ast-grep/rules/python/security/eval-usage.yml).

Expected detections: ≥3 violations
Rule ID: SEC-004
Severity: CRITICAL
"""


# Pattern 1: eval() with user input
def calculate_user_expression(expression: str) -> float:
    """VULNERABLE: eval() allows arbitrary code execution"""

    # SEC-004 should detect eval() usage
    result = eval(expression)

    return result


# Pattern 2: exec() with user input
def execute_user_code(code: str):
    """VULNERABLE: exec() allows arbitrary code execution"""

    # SEC-004 should detect exec() usage
    exec(code)


# Pattern 3: compile() with user input
def compile_user_code(source_code: str):
    """VULNERABLE: compile() creates executable code object"""

    # SEC-004 should detect compile() in exec mode
    code_obj = compile(source_code, '<string>', 'exec')
    exec(code_obj)


# Pattern 4: eval() in calculator function
class Calculator:
    """VULNERABLE: Calculator using eval()"""

    def compute(self, formula: str) -> float:
        """VULNERABLE: eval() for formula evaluation"""

        # SEC-004 should detect eval()
        return eval(formula)


# Pattern 5: Dynamic function creation
def create_dynamic_function(func_body: str):
    """VULNERABLE: exec() for function creation"""
    namespace = {}

    # SEC-004 should detect exec() creating functions
    func_code = f"""
def dynamic_function(x):
    {func_body}
    """

    exec(func_code, namespace)

    return namespace['dynamic_function']


# Pattern 6: eval() with globals/locals
def evaluate_with_context(expression: str, context: dict):
    """VULNERABLE: eval() with custom namespace"""

    # SEC-004 should detect eval() even with custom namespace
    result = eval(expression, globals(), context)

    return result
