# Output Schema

**Purpose:** Structured JSON output schema for the dev-result-interpreter subagent. Loaded via `Read()` from Step 9 of the core agent file.

---

## Return Structured Result Format

```json
{
  "status": "SUCCESS|INCOMPLETE|FAILURE",
  "story_id": "STORY-XXX",
  "story_title": "Story title or description",
  "timestamp": "2025-11-18T15:45:00Z",

  "workflow_summary": {
    "overall_result": "SUCCESS|INCOMPLETE|FAILURE",
    "final_status": "Dev Complete|In Development|Failed",
    "completion_percentage": 100,
    "duration_seconds": 1847,
    "phases_completed": ["Phase 0", "Phase 1", "Phase 2", "Phase 3", "Phase 4", "Phase 5", "Phase 6"],
    "phases_pending": []
  },

  "implementation_status": {
    "dod_completed": 12,
    "dod_total": 12,
    "dod_completion_percentage": 100,
    "incomplete_items": [],
    "deferred_items": [],
    "deferred_count": 0
  },

  "test_results": {
    "total_tests": 48,
    "passing_tests": 48,
    "failing_tests": 0,
    "skipped_tests": 0,
    "pass_rate": "100%",
    "coverage_percentage": 94,
    "coverage_by_layer": {
      "business_logic": 95,
      "application": 92,
      "infrastructure": 87
    }
  },

  "code_quality": {
    "average_complexity": 6.2,
    "max_complexity": 9,
    "duplication_percentage": 2.1,
    "issues_detected": 0,
    "maintainability_index": 78
  },

  "git_workflow": {
    "commit_hash": "a1b2c3d4",
    "branch_name": "STORY-042",
    "files_changed": 8,
    "lines_added": 342,
    "lines_deleted": 47
  },

  "phases_detail": [
    {
      "phase": "Phase 0",
      "name": "Pre-Flight Validation",
      "status": "PASSED",
      "duration_seconds": 23,
      "checks": ["Git status verified", "Context files validated", "Tech stack detected"]
    },
    {
      "phase": "Phase 1",
      "name": "Red Phase (Test Generation)",
      "status": "PASSED",
      "duration_seconds": 156,
      "artifacts": ["tests/STORY-042.test.js"],
      "tests_generated": 12
    },
    {
      "phase": "Phase 2",
      "name": "Green Phase (Implementation)",
      "status": "PASSED",
      "duration_seconds": 487,
      "artifacts": ["src/STORY-042.js"],
      "tests_passing": 12
    },
    {
      "phase": "Phase 3",
      "name": "Refactor Phase",
      "status": "PASSED",
      "duration_seconds": 234,
      "improvements": ["Complexity reduced from 8.1 to 6.2", "Removed 47 duplicated lines"]
    },
    {
      "phase": "Phase 4",
      "name": "Integration Phase",
      "status": "PASSED",
      "duration_seconds": 312,
      "integration_tests": 8,
      "scenarios_validated": 5
    },
    {
      "phase": "Phase 5",
      "name": "Deferral Challenge",
      "status": "PASSED",
      "duration_seconds": 89,
      "deferrals_reviewed": 0,
      "deferrals_approved": 0
    },
    {
      "phase": "Phase 6",
      "name": "Git Workflow",
      "status": "PASSED",
      "duration_seconds": 45,
      "commit": "a1b2c3d4",
      "files_staged": 8
    }
  ],

  "display": {
    "template": "dev_success_complete",
    "content": "... full markdown template from Step 6 ...",
    "title": "✅ Development Complete - STORY-042: User Authentication",
    "summary_lines": [
      "TDD workflow completed successfully",
      "All 12 DoD items completed",
      "48/48 tests passing (100%)",
      "Coverage: 94% (all layers above threshold)"
    ]
  },

  "next_steps": [
    "Development complete and ready for quality validation",
    "Run: `/qa STORY-042` to validate implementation",
    "If QA passes: `/release STORY-042` to deploy",
    "View detailed workflow: devforgeai/specs/Stories/STORY-042.story.md"
  ],

  "workflow_metrics": {
    "total_duration_minutes": 30.8,
    "phases_count": 7,
    "success_rate": "100%",
    "code_files_created": 1,
    "test_files_created": 1,
    "git_commits": 1
  },

  "story_file_location": "devforgeai/specs/Stories/STORY-042-user-authentication.story.md",
  "execution_completed_at": "2025-11-18T16:15:47Z"
}
```
