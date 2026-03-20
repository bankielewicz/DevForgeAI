# CI Answers Protocol

## Purpose

When Claude runs in headless mode (GitHub Actions), it cannot interactively ask the user questions via AskUserQuestion. The `ci-answers.yaml` file provides pre-configured responses that Claude reads instead of prompting.

## How It Works

1. **During headless execution**, Claude detects it is running in CI (via `CI=true` environment variable)
2. **When AskUserQuestion would normally fire**, Claude reads `ci-answers.yaml` instead
3. **Pattern matching** determines which pre-configured answer to use
4. **Fallback response** is used when no pattern matches

## ci-answers.yaml Format

```yaml
answers:
  - pattern: "regex pattern to match question text"
    response: "pre-configured answer"

  - pattern: "another pattern"
    response: "another answer"
```

### Pattern Matching Rules

1. Patterns are tested in order (first match wins)
2. Patterns are case-insensitive regex
3. The `.*` wildcard pattern acts as a catch-all fallback
4. If no pattern matches and no catch-all exists, the workflow logs a warning and uses framework defaults

## Default Answers

The template provides these default answers covering common AskUserQuestion scenarios:

| Question Category | Pattern | Default Response |
|-------------------|---------|-----------------|
| Technology decisions | `technology\|framework\|library` | Use tech-stack.md |
| Architecture decisions | `architecture\|design pattern` | Follow architecture-constraints.md |
| Ambiguity resolution | `multiple approaches\|which approach` | Use simplest approach meeting ACs |
| Deferral decisions | `defer\|skip\|postpone` | Do not defer without justification |
| Test strategy | `test strategy\|coverage` | Follow TDD, 95%/85%/80% thresholds |
| Catch-all | `.*` | Use framework defaults from context files |

## Customization

Users should review and customize `ci-answers.yaml` for their project. Common customizations:

### Project-Specific Technology Answers

```yaml
- pattern: "database|data store"
  response: "Use PostgreSQL as specified in tech-stack.md"

- pattern: "frontend framework"
  response: "Use React with TypeScript"
```

### Team-Specific Process Answers

```yaml
- pattern: "code review|reviewer"
  response: "Skip manual review in CI, rely on automated QA"

- pattern: "branch strategy"
  response: "Create feature branches from main"
```

## Validation

During Phase 02 (Configuration Loading), verify the ci-answers.yaml:

1. File exists at `devforgeai/config/ci/ci-answers.yaml`
2. File is valid YAML
3. Contains `answers:` key with at least 1 entry
4. Each entry has both `pattern:` and `response:` keys
5. At least one catch-all pattern (`.*`) exists

## Important Notes

- ci-answers.yaml is a **living document** -- teams should update it as they discover new question patterns
- Answers should be conservative -- prefer safe defaults over aggressive automation
- The file is checked into the repository and reviewed like any other configuration
- Changes to ci-answers.yaml should be tested by running a /dev workflow in CI
