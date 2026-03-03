---
name: code-analyzer-analysis-patterns
description: Detailed architecture pattern detection rules, API extraction patterns, and workflow analysis procedures
version: "1.0"
status: Reference (loaded on demand)
---

# Code Analyzer Analysis Patterns

**Version**: 1.0
**Purpose**: Detailed detection rules for architecture patterns, API extraction, and workflow analysis.

---

## Architecture Pattern Detection Rules

### MVC Pattern Detection

```
IF directories match ["controllers", "models", "views"]:
    pattern = "MVC"
    confidence = "HIGH" if all 3 present, "MEDIUM" if 2 present
    layers = {
        "presentation": "views/",
        "business_logic": "controllers/",
        "data": "models/"
    }
```

### Clean Architecture Detection

```
IF directories match ["domain", "application", "infrastructure", "presentation"]:
    pattern = "Clean Architecture"
    confidence = "HIGH" if all 4 present, "MEDIUM" if 3 present
    layers = {
        "domain": "domain/",
        "application": "application/",
        "infrastructure": "infrastructure/",
        "presentation": "presentation/"
    }
```

### Layered Architecture Detection

```
IF directories match patterns like ["api", "services", "data", "dal", "bll", "ui"]:
    pattern = "Layered"
    confidence = "MEDIUM"
    layers = auto-detect from names
```

### DDD Detection

```
IF directories match ["aggregates", "entities", "repositories", "value-objects"]:
    pattern = "Domain-Driven Design"
    confidence = "HIGH" if 3+ present
```

### Fallback

```
IF no pattern matches:
    pattern = "Custom"
    confidence = "LOW"
    layers = top-level directories
```

---

## Public API Extraction Patterns

### Python

```
Grep(pattern="^def [a-z_]+\\(", type="py", output_mode="content")
Grep(pattern="^class [A-Z][a-zA-Z]+", type="py", output_mode="content")
```

Parse results for:
- Function signatures
- Class definitions
- Method signatures (public only, no __ prefix)
- Docstrings (if present)

### JavaScript/TypeScript

```
Grep(pattern="export (function|class|const)", type="js", output_mode="content")
Grep(pattern="export (function|class|const)", type="ts", output_mode="content")
```

Parse results for:
- Exported functions
- Exported classes
- Exported constants

### C#

```
Grep(pattern="public (class|interface|enum)", type="cs", output_mode="content")
Grep(pattern="public.*\\(", type="cs", output_mode="content")
```

Parse results for:
- Public classes/interfaces
- Public methods

### API Metadata Format

```json
{
    "endpoint": "createTask",
    "signature": "createTask(title: string, description: string): Promise<Task>",
    "location": "src/controllers/TaskController.ts:42",
    "documented": false,
    "docstring": null
}
```

---

## Dependency Analysis Patterns

### External Dependencies

**Python** (requirements.txt, pyproject.toml):
```
IF requirements.txt exists:
    Read(file_path="requirements.txt")
    Parse package names and versions

IF pyproject.toml exists:
    Read(file_path="pyproject.toml")
    Parse [dependencies] section
```

**JavaScript** (package.json):
```
Read(file_path="package.json")
Parse: dependencies, devDependencies
Extract: package names and versions
```

**C#** (*.csproj):
```
Glob(pattern="**/*.csproj")
Read each .csproj file
Grep(pattern="<PackageReference Include=")
Parse package names and versions
```

### Internal Dependencies

```
Grep(pattern="^import |^from .* import", type="py")
Grep(pattern="^import .* from|^require\\(", type="js")
Grep(pattern="^using ", type="cs")
```

Build dependency graph:
- Which modules import which
- Cross-layer dependencies (check for violations)
- Circular dependencies (flag as issue)

---

## Entry Point Discovery

### Python
```
Grep(pattern="if __name__ == '__main__':", type="py")
Glob(pattern="**/main.py")
Glob(pattern="**/app.py")
Glob(pattern="**/__main__.py")
```

### JavaScript/TypeScript
```
Read(file_path="package.json")
Extract: "main" field, "scripts.start"

Common entry points:
- src/index.ts, src/main.ts, src/app.ts, src/server.ts
```

### C#
```
Grep(pattern="static void Main\\(", type="cs")
Glob(pattern="**/Program.cs")
```

---

## Workflow Analysis

### Find Controllers/Handlers

```
Grep(pattern="@app\\.route|@app\\.get|@app\\.post", type="py")
Grep(pattern="app\\.(get|post|put|delete)\\(", type="js")
Grep(pattern="\\[HttpGet\\]|\\[HttpPost\\]", type="cs")
```

### Build Workflow Chains

Trace calls from endpoint to database:
```
User -> API -> Controller -> Use Case -> Repository -> Database
```

Generate sequence for each major workflow.

---

## Documentation Gap Analysis

### Coverage Calculation

```
total_public_apis = count all public functions/classes/methods
documented_apis = count APIs with docstrings/comments
coverage = (documented_apis / total_public_apis) * 100
```

### Missing Documentation Files

Check for standard documentation:
- README.md
- CONTRIBUTING.md
- docs/API.md
- docs/DEVELOPER.md
- docs/ARCHITECTURE.md

### Undocumented Item Format

```json
{
    "api": "createTask",
    "location": "src/controllers/TaskController.ts:42",
    "type": "function",
    "priority": "high"
}
```

---

## References

- Clean Architecture (Robert C. Martin)
- Domain-Driven Design (Eric Evans)
- MVC Pattern documentation
