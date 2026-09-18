# Documentation Writer - Examples

### Example 1: API Documentation Generation

```
Task(
  subagent_type="documentation-writer",
  description="Document REST API endpoints",
  prompt="Generate OpenAPI documentation for the payment processing API. Source files: src/api/payments/ and src/handlers/payment*.ts. Include all POST, GET, PATCH endpoints with request/response examples, error codes, and authentication requirements. Output to docs/api/payments.yaml following OpenAPI 3.0.0 spec."
)
```

### Example 2: Codebase Documentation

```
Task(
  subagent_type="documentation-writer",
  description="Add code documentation and user guide",
  prompt="Add JSDoc comments to all exported functions in src/utils/data-processing.ts. Minimum 80% coverage. Also create a user guide in docs/guides/data-processing-guide.md with setup instructions, configuration options, and 3-4 practical examples. Check tech-stack.md for terminology consistency."
)
```

---

**Token Budget**: < 30K per invocation
**Priority**: MEDIUM
**Implementation Day**: Day 8
**Model**: Sonnet (clear technical writing)
