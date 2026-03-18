# Architecture Review Workflow (Phase 8)

Detailed workflow for reviewing generated context files via the architect-reviewer subagent.

## Why This Phase Exists

Context files are generated through a series of questions and template customizations. The generation process optimizes for completeness — capturing every decision — but can produce constraints that conflict with each other, are impractical to enforce, or miss important concerns. An independent review catches these issues before they become embedded in every downstream story.

## Step 8.1: Invoke architect-reviewer

Dispatch the architect-reviewer subagent with all 6 context files:

```
Task(
  subagent_type="architect-reviewer",
  prompt="Review the generated context files in devforgeai/specs/context/ for:

  1. Architectural soundness - Do layer boundaries prevent tight coupling?
  2. Technology coherence - Are selected technologies compatible?
  3. Completeness - Are all project concerns addressed?
  4. Consistency - Do files align with each other?
  5. Practicality - Are constraints realistic and enforceable?

  Focus on critical issues that would cause problems during development.
  Provide specific recommendations for any concerns."
)
```

The subagent returns a structured review with concerns categorized by severity.

## Step 8.2: Present Concerns

If the reviewer raises concerns, present them to the user via AskUserQuestion:

```
AskUserQuestion:
  Question: "Architecture review found [N] concerns. How would you like to proceed?"
  Options:
    - Accept all recommendations and update files
    - Keep current approach (document rationale in ADR)
    - Hybrid approach (review each concern individually)
```

If "Hybrid" selected, present each concern individually with accept/reject options.

## Step 8.3: Apply Approved Changes

For each accepted recommendation:
1. Use `Edit` tool to apply the change to the relevant context file
2. If the change is significant (technology swap, constraint removal, layer restructure), create an ADR documenting the review decision

For rejected recommendations:
1. Document the rationale for rejection
2. Optionally create an ADR explaining why the current approach was preserved

## Step 8.4: Re-validate (if changes made)

If any context files were modified:
1. Re-read all 6 files to verify consistency
2. Check that accepted changes don't introduce new contradictions
3. If new issues found, present to user (one more round only — avoid infinite loops)

## Graceful Degradation

If the architect-reviewer subagent fails or times out:
- Display WARNING with the error
- Continue to Phase 9 (review is valuable but not blocking)
- Log the failure for follow-up
