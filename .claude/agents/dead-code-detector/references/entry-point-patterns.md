---
name: entry-point-patterns
description: Entry point exclusion patterns for dead code detection
version: 1.0
---

# Entry Point Patterns

Functions matching these patterns should be EXCLUDED from dead code reports because they are invoked externally (by frameworks, test runners, event systems) rather than through direct code calls.

---

## Python Patterns

### Main Entry Points

| Pattern | Description | Example |
|---------|-------------|---------|
| `main()` | Script entry point | `def main():` |
| `__main__` | Module entry point | `if __name__ == "__main__":` |
| `__init__` | Constructor | `def __init__(self):` |
| `__str__`, `__repr__` | String representations | `def __str__(self):` |
| `__*__` | Any dunder method | `def __eq__(self, other):` |

### Web Framework Decorators

| Pattern | Framework | Example |
|---------|-----------|---------|
| `@app.route` | Flask | `@app.route('/api/users')` |
| `@router.get`, `@router.post` | FastAPI | `@router.get('/items')` |
| `@api_view` | Django REST | `@api_view(['GET'])` |
| `@action` | Django REST ViewSet | `@action(detail=True)` |

### Test Framework Patterns

| Pattern | Framework | Example |
|---------|-----------|---------|
| `@pytest.fixture` | pytest | `@pytest.fixture` |
| `test_*` | pytest/unittest | `def test_user_creation():` |
| `Test*` | pytest class | `class TestUserService:` |
| `setUp`, `tearDown` | unittest | `def setUp(self):` |

### CLI Decorators

| Pattern | Framework | Example |
|---------|-----------|---------|
| `@click.command` | Click | `@click.command()` |
| `@click.group` | Click | `@click.group()` |
| `@app.command` | Typer | `@app.command()` |

### Event/Signal Handlers

| Pattern | Framework | Example |
|---------|-----------|---------|
| `@receiver` | Django signals | `@receiver(post_save)` |
| `@event.listens_for` | SQLAlchemy | `@event.listens_for(Model, 'after_insert')` |
| `on_*` | Event handler naming | `def on_message(msg):` |
| `handle_*` | Handler naming | `def handle_request(req):` |

### Celery/Async Tasks

| Pattern | Framework | Example |
|---------|-----------|---------|
| `@celery.task` | Celery | `@celery.task` |
| `@shared_task` | Celery | `@shared_task` |
| `@app.task` | Celery | `@app.task(bind=True)` |

---

## TypeScript/JavaScript Patterns

### Export Patterns

| Pattern | Description | Example |
|---------|-------------|---------|
| `export default` | Default export | `export default function handler()` |
| `export function` | Named export | `export function processData()` |
| `module.exports` | CommonJS export | `module.exports = { handler }` |

### Framework Decorators (NestJS, Angular)

| Pattern | Framework | Example |
|---------|-----------|---------|
| `@Controller` | NestJS | `@Controller('users')` |
| `@Get`, `@Post`, `@Put`, `@Delete` | NestJS | `@Get(':id')` |
| `@Injectable` | NestJS/Angular | `@Injectable()` |
| `@Component` | Angular | `@Component({...})` |
| `@Directive` | Angular | `@Directive({...})` |

### React Patterns

| Pattern | Description | Example |
|---------|-------------|---------|
| Component functions | PascalCase functions | `function UserProfile()` |
| `use*` hooks | Custom hooks | `function useAuth()` |

### Test Patterns

| Pattern | Framework | Example |
|---------|-----------|---------|
| `describe()` | Jest/Mocha | `describe('UserService', ...)` |
| `it()`, `test()` | Jest/Mocha | `it('should create user', ...)` |
| `beforeEach`, `afterEach` | Jest/Mocha | `beforeEach(() => {...})` |

---

## Rust Patterns

| Pattern | Description | Example |
|---------|-------------|---------|
| `fn main()` | Binary entry point | `fn main() {}` |
| `#[test]` | Test function | `#[test] fn test_add()` |
| `#[tokio::main]` | Async main | `#[tokio::main] async fn main()` |
| `#[actix_web::main]` | Actix main | `#[actix_web::main]` |
| `impl Trait for` | Trait implementations | `impl Display for User` |

---

## Generic Patterns (All Languages)

| Pattern | Reason for Exclusion |
|---------|----------------------|
| `main`, `Main` | Application entry point |
| `test_*`, `Test*` | Test functions/classes |
| `setup`, `teardown` | Test lifecycle |
| `__*__` (dunder) | Magic/special methods |
| Trait/Interface implementations | Called polymorphically |

---

## Usage

When Phase 4 evaluates a zero-caller function:

```python
def matches_entry_point(function):
    # Check function name patterns
    if function.name == "main" or function.name.startswith("__"):
        return True, "main_or_dunder"

    if function.name.startswith("test_") or function.name.startswith("Test"):
        return True, "test_function"

    # Check for decorators in source
    decorators = get_decorators(function)
    entry_point_decorators = [
        "pytest.fixture", "app.route", "router.get", "router.post",
        "click.command", "celery.task", "Controller", "Get", "Post"
    ]
    for decorator in decorators:
        if any(ep in decorator for ep in entry_point_decorators):
            return True, f"decorator:{decorator}"

    return False, None
```

---

## Adding New Patterns

When framework patterns are missing:

1. Add pattern to appropriate section above
2. Update dead-code-detector.md Phase 4 logic
3. Add test case to tests/STORY-403/test_ac5_entry_point_exclusion.py
