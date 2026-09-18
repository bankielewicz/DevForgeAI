# Usage Examples

**Purpose:** Task invocation examples for the dev-result-interpreter subagent. Loaded via `Read()` from the Examples section of the core agent file.

---

## Example 1: Interpret Success Result

```
Task(
  subagent_type="dev-result-interpreter",
  description="Interpret dev results for STORY-567",
  prompt="Interpret development workflow results for STORY-567. Story file: devforgeai/specs/Stories/STORY-567-user-auth.story.md. Workflow status: Dev Complete. Parse story file to extract all TDD phases completed (Phase 0-6), DoD items completed (12/12), test results (48/48 passing, 94% coverage), and code quality metrics. Generate success template with implementation summary and next steps recommending QA validation."
)
```

## Example 2: Interpret Incomplete with Deferrals

```
Task(
  subagent_type="dev-result-interpreter",
  description="Interpret dev results with deferrals for STORY-890",
  prompt="Interpret development workflow results for STORY-890. Story file: devforgeai/specs/Stories/STORY-890-payment-processing.story.md. Workflow status: In Development. Extract TDD phases (Phase 0-3 complete, Phase 4-6 pending), DoD items (8/12 completed, 4 deferred due to external API delays), test results (36/48 passing). Determine overall result (INCOMPLETE with deferrals). Generate deferrals template with deferral reasons and resolution options. Recommend option 1 (continue development) or option 3 (create follow-up stories)."
)
```
