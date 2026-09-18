# Observation Extractor - Invocation Pattern

```markdown
Task(
  subagent_type="observation-extractor",
  description="Extract observations from phase {phase_number} subagent outputs",
  prompt="""
  Extract observations from the following subagent outputs.

  Phase: {phase_number}
  Context: {subagent_output_json}

  Apply extraction rules for:
  - test-automator (if present)
  - code-reviewer (if present)
  - backend-architect (if present)
  - ac-compliance-verifier (if present)

  Return observations array conforming to output schema.
  """
)
```
