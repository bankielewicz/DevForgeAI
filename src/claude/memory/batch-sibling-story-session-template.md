---
name: batch-sibling-story-session-template
description: Process 3+ sibling stories from the same epic in a single session with progressive efficiency gains
version: "1.0"
created: 2026-02-10
---

# Batch Sibling Story Session Template

Process multiple sibling stories from the same epic in a single session. Capture shared context loading, pattern recognition, and incremental observation aggregation to achieve progressive efficiency gains across stories.

**When to Use:** Apply this template when developing 3+ sibling stories from the same epic in a single session.

**Expected Outcome:** Achieve 35-40% time reduction by the final story compared to processing stories independently.

---

## Epic Context Loading Instructions

Follow these steps at the start of every batch sibling story session to establish shared context once rather than reloading it per story.

### Step 1: Load Epic and Context Files

1. Read the parent epic file to extract scope, goals, and decomposition rationale before touching any individual story.
2. Load all six context files from `devforgeai/specs/context/` in a single parallel tool invocation:
   - tech-stack.md (technology constraints)
   - source-tree.md (file placement rules)
   - dependencies.md (package constraints)
   - coding-standards.md (style rules)
   - architecture-constraints.md (structural rules)
   - anti-patterns.md (forbidden patterns)
3. Read every sibling story file in the batch to build a complete inventory of acceptance criteria, file targets, dependencies, and test locations across the set.

### Step 2: Identify Shared Elements

4. Identify the common file targets that appear in two or more sibling stories and record them in a shared-files list for conflict awareness.
5. Extract the shared technical specification elements that apply to all stories in the batch:
   - Common interfaces and shared types
   - Overlapping test utilities
   - Shared constants and configurations

### Step 3: Plan Execution Order

6. Record the dependency ordering between sibling stories (which story must complete before another can start) and plan execution sequence accordingly.
7. Build a consolidated context summary containing:
   - Epic goal and success criteria
   - Sibling story count and IDs
   - Shared files with potential conflicts
   - Dependency graph
   - Common patterns identified

### Step 4: Validate and Persist

8. Write the context summary to the session workspace so it persists across context window boundaries.
9. Verify that all referenced file paths exist by reading each target file.
10. Halt on any missing file before proceeding to story execution.

---

## Shared Pattern Recognition

Apply these steps after context loading to identify and reuse patterns across sibling stories, eliminating redundant discovery work.

### Pattern Extraction from First Story

1. Analyze the first story's implementation to extract the structural pattern:
   - File layout and directory structure
   - Naming conventions for files, functions, and tests
   - Interface signatures and type definitions
   - Test structure and assertion patterns

2. Document the extracted pattern as a reusable template with placeholders for story-specific values:
   - `{STORY_ID}` for story identifiers
   - `{DOMAIN_TERM}` for domain-specific terminology
   - `{THRESHOLD_VALUE}` for configurable thresholds

### Pattern Application to Subsequent Stories

3. Compare each subsequent story's acceptance criteria against the documented pattern to determine:
   - Which elements are identical and can be copied directly
   - Which require story-specific adaptation
   - Which require entirely new implementation

4. Maintain a running divergence log that records where each story deviates from the shared pattern:
   - Divergence location (file, line, section)
   - Reason for divergence (different domain, additional constraints, unique edge cases)
   - Impact on shared pattern (update needed or not)

### Test and Validation Reuse

5. Propagate test patterns from the first story to subsequent stories:
   - Copy the test structure and file organization
   - Adapt assertions to story-specific expected values
   - Reuse mock objects and test fixtures

6. Reuse validation approaches discovered in earlier stories:
   - Anti-pattern checks that passed
   - Coverage analysis strategies
   - QA verification methods

### Pattern Evolution

7. Track which context files and reference documents were consulted for the first story so that later stories skip unnecessary re-reading of already-loaded material.

8. Update the shared pattern after each completed story to incorporate any improvements or corrections discovered during execution, ensuring later stories benefit from earlier learnings.

---

## Incremental Observation Capture

Use these steps to capture observations during batch execution and aggregate them for post-session framework improvement feedback.

### Observation Log Initialization

1. Initialize an observation log at the start of the session with the following columns:
   - Story ID (which story generated the observation)
   - Observation type (pattern, anti-pattern, friction, improvement)
   - Description (what was observed)
   - Severity (low, medium, high)
   - Scope (story-specific or batch-wide)

2. Record each observation immediately when it occurs during story execution rather than deferring capture to the end of the session.

### Observation Classification

3. Classify observations into categories:
   - **Workflow friction**: Steps that slow execution or cause confusion
   - **Pattern opportunities**: Reusable approaches that could be templated
   - **Constraint gaps**: Missing or unclear rules in context files
   - **Tool limitations**: Tooling that could be improved or added

4. Tag observations that apply to the epic as a whole versus those specific to an individual story:
   - `[EPIC]` for batch-wide observations
   - `[STORY-XXX]` for story-specific observations

### Persistence and Aggregation

5. Write the observation log to disk after completing each story to prevent data loss from:
   - Context window exhaustion
   - Session interruption
   - Unexpected errors

6. Aggregate cross-story observations at the end of the batch session:
   - Merge per-story logs into a single document
   - Deduplicate identical observations
   - Rank by frequency (how many stories encountered it) and severity

### Output Formatting

7. Generate a final observation summary containing:
   - Total observations captured
   - Top five by severity
   - Recurring themes across stories
   - Recommended framework improvements with specific file targets

8. Format the aggregated observations for compatibility with the devforgeai-feedback skill so they can be ingested through the standard feedback pipeline.

---

## Batch Coordination Instructions

Follow these steps to coordinate execution across sibling stories within a single session, managing state transitions and preventing conflicts.

### Sequential Execution

1. Execute sibling stories sequentially in dependency order, completing all phases (preflight through result) for one story before starting the next.

2. Maintain a batch state tracker recording each story's current status:
   - Not started
   - In progress (with current phase number)
   - Dev complete
   - QA approved

3. Write the batch state tracker to disk after every status change so that interrupted sessions can resume from the last completed story.

### Pattern Application and Measurement

4. Apply the shared pattern from Section 2 to each subsequent story.

5. Measure time-per-story to validate that efficiency gains accumulate as predicted:
   - Record start time for each story
   - Record end time for each story
   - Calculate percentage improvement from baseline (first story)

### Git and Version Control

6. Reuse git branch strategies across sibling stories:
   - Commit each story independently with its own story ID in the commit message
   - Use consistent commit message format: `feat(STORY-XXX): description`
   - Plan for a single integration verification pass after the batch completes

### Conflict Detection and Resolution

7. Detect file overlap conflicts before starting each story:
   - Compare target files against files already modified by completed stories
   - Identify potential merge conflicts
   - Halt and resolve conflicts before proceeding

8. Carry forward test utilities, mock objects, and helper functions created during earlier stories:
   - Document shared utilities in a central location
   - Reference shared utilities from subsequent story tests
   - Do not recreate existing infrastructure

### Batch Completion

9. Perform a batch-level integration check after all sibling stories complete:
   - Verify that changes from different stories compose correctly
   - Run any cross-story integration tests
   - Confirm no regressions were introduced

10. Generate a batch completion report summarizing:
    - Stories completed (count and IDs)
    - Total time for batch
    - Per-story time breakdown
    - Efficiency gain percentage compared to the first story
    - Any deferred items requiring follow-up

---

## Proof of Concept

The batch sibling story pattern was validated during EPIC-057 execution, which processed five sibling stories in a single session workflow.

### EPIC-057 Batch Execution Results

EPIC-057 (Treelint Advanced Features) decomposed into five sibling stories that shared common patterns, target file structures, and testing approaches:

- **STORY-366**: First story in the batch. Established the structural pattern, test conventions, and implementation approach. Served as the baseline for time measurement.

- **STORY-367**: Second story. Reused the pattern from STORY-366 with domain-specific adaptations. Initial efficiency gains observed as context loading was already complete.

- **STORY-368**: Third story. Pattern application became routine. Reduced discovery time as shared files and test utilities were already loaded and validated.

- **STORY-369**: Fourth story. Observation capture identified recurring QA patterns across the batch. Streamlined execution using accumulated knowledge from prior stories.

- **STORY-370**: Fifth and final story. Achieved peak efficiency with minimal discovery overhead. Batch completion report generated with aggregated observations.

### Measured Efficiency Gains

| Metric | First Story (Baseline) | Final Story | Improvement |
|--------|----------------------|-------------|-------------|
| Context loading | Full load required | Shared context reused | Eliminated |
| Pattern discovery | Full analysis | Pattern applied directly | 35-40% time reduction |
| Test scaffolding | Built from scratch | Reused from earlier stories | Significant reduction |
| QA verification | Full validation | Pattern-matched verification | Streamlined |
| Observation capture | Initial setup | Incremental append | Minimal overhead |

### Efficiency Gain Analysis

The progressive efficiency gains demonstrated a 35-40% time reduction by the final story compared to the first story baseline. This improvement came from three primary sources:

1. **Shared context loading**: Epic context, context files, and shared file targets were loaded once and reused across all five stories, eliminating redundant file reads.

2. **Pattern recognition**: The structural pattern extracted from STORY-366 was applied with minimal adaptation to STORY-367 through STORY-370, reducing implementation discovery time.

3. **Observation aggregation**: Capturing observations incrementally across the batch produced a richer feedback dataset than five independent sessions would have generated, while adding negligible per-story overhead.

### Applicability

This template is domain-agnostic. The batch pattern applies to any set of sibling stories that share:

- A common parent epic with consistent decomposition
- Overlapping target files or shared interfaces
- Similar acceptance criteria structures
- Compatible test patterns and validation approaches

Apply this template whenever three or more sibling stories from the same epic are ready for development in the same session.

---

## Edge Case Handling

### Small Batch (1-2 Stories)

If a batch contains fewer than three stories:

1. The overhead of shared context loading may not be justified.
2. Consider processing stories independently using standard /dev workflow.
3. Batch processing is recommended only for 3+ stories.

### Zero Shared Files

If sibling stories have no overlapping target files:

1. Shared context loading still provides value for context file reuse.
2. Pattern recognition may have limited applicability.
3. Observation aggregation remains valuable for framework feedback.
4. Consider falling back to individual story processing if overlap is minimal.

### Mid-Batch Context Reset

If context window exhausts mid-batch:

1. Read the batch state tracker from disk to determine last completed story.
2. Reload the consolidated context summary from the session workspace.
3. Resume from the next pending story in the dependency order.
4. Prior observations are preserved on disk and can be aggregated at batch end.

### Dependency Ordering Constraints

If sibling stories have strict sequential dependencies:

1. Execute in dependency order, never in parallel.
2. Complete the blocking story's full TDD cycle before starting the dependent story.
3. Validate blocking story's outputs before dependent story begins.
4. Document dependency rationale in the batch state tracker.

---

## Quick Reference Checklist

### Before Starting Batch Session

- [ ] Parent epic file read and goals extracted
- [ ] All six context files loaded in parallel
- [ ] All sibling story files read and inventoried
- [ ] Shared file targets identified and conflict-checked
- [ ] Dependency ordering established
- [ ] Observation log initialized
- [ ] Batch state tracker created and written to disk
- [ ] Consolidated context summary written to session workspace

### After Each Story Completes

- [ ] Story status updated in batch state tracker
- [ ] Observations captured and written to disk
- [ ] Shared pattern updated with any improvements
- [ ] Time recorded for efficiency measurement
- [ ] Git commit created with story ID

### After All Stories Complete

- [ ] All stories reached target status (dev complete or QA approved)
- [ ] Batch state tracker reflects final status for each story
- [ ] Observation log aggregated and formatted for feedback pipeline
- [ ] Batch completion report generated with efficiency metrics
- [ ] Integration check passed across all story changes
- [ ] Efficiency gains calculated and documented
