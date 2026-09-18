# Documentation Writer - Output Format Reference

Documentation is produced in the following structured format:

```
# Documentation Deliverables

## 1. API Documentation (if applicable)
- **Format**: OpenAPI 3.0.0 YAML/JSON
- **Location**: docs/api/ or docs/api/{component}.md
- **Contents**: Endpoints, parameters, request/response schemas, authentication, error codes

## 2. Code Documentation (inline)
- **Format**: Language-specific (JSDoc, docstrings, XML comments)
- **Location**: Source files modified in-place
- **Contents**: Function/class descriptions, parameters, return types, examples, exceptions

## 3. Architecture Documentation
- **Format**: Markdown with embedded Mermaid diagrams
- **Location**: docs/architecture/
- **Contents**: C4 diagrams, sequence diagrams, data flow, integration points

## 4. User Guides
- **Format**: Markdown with code examples
- **Location**: docs/guides/
- **Contents**: Prerequisites, setup, configuration, use cases, troubleshooting, FAQ

## 5. README Files
- **Format**: Markdown
- **Location**: Project root and major subdirectories
- **Contents**: Overview, features, installation, configuration, usage, contributing
```

**Documentation Report:** Coverage percentage, files documented, documentation types generated, consistency verification.
