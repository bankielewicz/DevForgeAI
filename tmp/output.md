bryan@DESKTOP-88FARC5:/mnt/c/Projects/DevForgeAI2$   # Generate full coverage mapping (the slow command)
  .devforgeai/traceability/coverage-mapper.sh --generate-coverage

  # Or for faster individual tests that work:
  .devforgeai/traceability/coverage-mapper.sh --stories-for-epic EPIC-015
  .devforgeai/traceability/coverage-mapper.sh --epic-for-story STORY-084
  .devforgeai/traceability/coverage-mapper.sh --validate-linkage STORY-084

{
  "aggregate": {
    "total_coverage_percentage": 46,
    "total_covered": 36,
    "total_features": 77
  },
  "epic_coverage": {
    "EPIC-002": {
      "coverage_percentage": 0,
      "covered_features": 0,
      "total_features": 3
    },
    "EPIC-003": {
      "coverage_percentage": 0,
      "covered_features": 0,
      "total_features": 1
    },
    "EPIC-004": {
      "coverage_percentage": 100,
      "covered_features": 3,
      "total_features": 3
    },
    "EPIC-005": {
      "coverage_percentage": 0,
      "covered_features": 0,
      "total_features": 3
    },
    "EPIC-006": {
      "coverage_percentage": 100,
      "covered_features": 12,
      "total_features": 4
    },
    "EPIC-007": {
      "coverage_percentage": 100,
      "covered_features": 7,
      "total_features": 6
    },
    "EPIC-008": {
      "coverage_percentage": 100,
      "covered_features": 1,
      "total_features": 1
    },
    "EPIC-009": {
      "coverage_percentage": 0,
      "covered_features": 8,
      "total_features": 0
    },
    "EPIC-010": {
      "coverage_percentage": 0,
      "covered_features": 9,
      "total_features": 0
    },
    "EPIC-011": {
      "coverage_percentage": 100,
      "covered_features": 10,
      "total_features": 9
    },
    "EPIC-012": {
      "coverage_percentage": 80,
      "covered_features": 4,
      "total_features": 5
    },
    "EPIC-013": {
      "coverage_percentage": 0,
      "covered_features": 0,
      "total_features": 6
    },
    "EPIC-014": {
      "coverage_percentage": 16,
      "covered_features": 1,
      "total_features": 6
    },
    "EPIC-015": {
      "coverage_percentage": 85,
      "covered_features": 6,
      "total_features": 7
    },
    "EPIC-016": {
      "coverage_percentage": 100,
      "covered_features": 4,
      "total_features": 2
    },
    "EPIC-017": {
      "coverage_percentage": 0,
      "covered_features": 0,
      "total_features": 7
    },
    "EPIC-018": {
      "coverage_percentage": 0,
      "covered_features": 0,
      "total_features": 5
    },
    "EPIC-019": {
      "coverage_percentage": 0,
      "covered_features": 0,
      "total_features": 5
    },
    "EPIC-020": {
      "coverage_percentage": 0,
      "covered_features": 0,
      "total_features": 4
    }
  },
  "epic_to_stories": {
    "EPIC-004": [
      "STORY-013",
      "STORY-016",
      "STORY-017"
    ],
    "EPIC-006": [
      "STORY-021",
      "STORY-022",
      "STORY-023",
      "STORY-024",
      "STORY-025",
      "STORY-026",
      "STORY-027",
      "STORY-028",
      "STORY-029",
      "STORY-030",
      "STORY-031",
      "STORY-032"
    ],
    "EPIC-007": [
      "STORY-034",
      "STORY-035",
      "STORY-036",
      "STORY-037",
      "STORY-038",
      "STORY-039",
      "STORY-049"
    ],
    "EPIC-008": [
      "STORY-040"
    ],
    "EPIC-009": [
      "STORY-041",
      "STORY-042",
      "STORY-043",
      "STORY-044",
      "STORY-045",
      "STORY-046",
      "STORY-047",
      "STORY-048"
    ],
    "EPIC-010": [
      "STORY-090",
      "STORY-091",
      "STORY-092",
      "STORY-093",
      "STORY-094",
      "STORY-095",
      "STORY-096",
      "STORY-097",
      "STORY-098"
    ],
    "EPIC-011": [
      "STORY-052",
      "STORY-053",
      "STORY-054",
      "STORY-055",
      "STORY-056",
      "STORY-057",
      "STORY-058",
      "STORY-059",
      "STORY-064",
      "STORY-065"
    ],
    "EPIC-012": [
      "STORY-066",
      "STORY-067",
      "STORY-068",
      "STORY-069"
    ],
    "EPIC-014": [
      "STORY-082"
    ],
    "EPIC-015": [
      "STORY-083",
      "STORY-084",
      "STORY-085",
      "STORY-087",
      "STORY-088",
      "STORY-089"
    ],
    "EPIC-016": [
      "STORY-099",
      "STORY-100",
      "STORY-101",
      "STORY-102"
    ]
  },
  "orphaned_stories": [
    "STORY-014",
    "STORY-015",
    "STORY-051",
    "STORY-061",
    "STORY-062",
    "STORY-063",
    "/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-007-post-operation-retrospective-conversation.story.md",
    "/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-008-adaptive-questioning-engine.story.md",
    "/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-009-skip-pattern-tracking.story.md",
    "/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-010-feedback-template-engine.story.md",
    "/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-011-configuration-management.story.md",
    "/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-012-template-customization.story.md",
    "/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-018-event-driven-hook-system.story.md",
    "/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-019-operation-lifecycle-integration.story.md",
    "/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-020-feedback-cli-commands.story.md",
    "/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-033-wire-hooks-into-audit-deferrals-command.story.md",
    "/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-050-refactor-audit-deferrals-budget-compliance.story.md",
    "/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-060-operational-sync.story.md",
    "/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-070-framework-release-automation.story.md",
    "/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-071-wizard-driven-interactive-ui.story.md",
    "/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-072-pre-flight-validation-checks.story.md",
    "/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-073-auto-detection.story.md",
    "/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-074-comprehensive-error-handling.story.md",
    "/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-075-installation-reporting-logging.story.md",
    "/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-076-claudemd-smart-merge.story.md",
    "/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-077-version-detection-compatibility.story.md",
    "/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-078-upgrade-mode-migration-scripts.story.md",
    "/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-079-fix-repair-installation-mode.story.md",
    "/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-080-rollback-previous-version.story.md",
    "/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-081-uninstall-user-content-preservation.story.md",
    "/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-086-coverage-reporting-system.story.md"
  ],
  "story_to_epic": {
    "STORY-013": "EPIC-004",
    "STORY-016": "EPIC-004",
    "STORY-017": "EPIC-004",
    "STORY-021": "EPIC-006",
    "STORY-022": "EPIC-006",
    "STORY-023": "EPIC-006",
    "STORY-024": "EPIC-006",
    "STORY-025": "EPIC-006",
    "STORY-026": "EPIC-006",
    "STORY-027": "EPIC-006",
    "STORY-028": "EPIC-006",
    "STORY-029": "EPIC-006",
    "STORY-030": "EPIC-006",
    "STORY-031": "EPIC-006",
    "STORY-032": "EPIC-006",
    "STORY-034": "EPIC-007",
    "STORY-035": "EPIC-007",
    "STORY-036": "EPIC-007",
    "STORY-037": "EPIC-007",
    "STORY-038": "EPIC-007",
    "STORY-039": "EPIC-007",
    "STORY-040": "EPIC-008",
    "STORY-041": "EPIC-009",
    "STORY-042": "EPIC-009",
    "STORY-043": "EPIC-009",
    "STORY-044": "EPIC-009",
    "STORY-045": "EPIC-009",
    "STORY-046": "EPIC-009",
    "STORY-047": "EPIC-009",
    "STORY-048": "EPIC-009",
    "STORY-049": "EPIC-007",
    "STORY-052": "EPIC-011",
    "STORY-053": "EPIC-011",
    "STORY-054": "EPIC-011",
    "STORY-055": "EPIC-011",
    "STORY-056": "EPIC-011",
    "STORY-057": "EPIC-011",
    "STORY-058": "EPIC-011",
    "STORY-059": "EPIC-011",
    "STORY-064": "EPIC-011",
    "STORY-065": "EPIC-011",
    "STORY-066": "EPIC-012",
    "STORY-067": "EPIC-012",
    "STORY-068": "EPIC-012",
    "STORY-069": "EPIC-012",
    "STORY-082": "EPIC-014",
    "STORY-083": "EPIC-015",
    "STORY-084": "EPIC-015",
    "STORY-085": "EPIC-015",
    "STORY-087": "EPIC-015",
    "STORY-088": "EPIC-015",
    "STORY-089": "EPIC-015",
    "STORY-090": "EPIC-010",
    "STORY-091": "EPIC-010",
    "STORY-092": "EPIC-010",
    "STORY-093": "EPIC-010",
    "STORY-094": "EPIC-010",
    "STORY-095": "EPIC-010",
    "STORY-096": "EPIC-010",
    "STORY-097": "EPIC-010",
    "STORY-098": "EPIC-010",
    "STORY-099": "EPIC-016",
    "STORY-100": "EPIC-016",
    "STORY-101": "EPIC-016",
    "STORY-102": "EPIC-016"
  },
  "uncovered_features": [],
  "validation": {
    "broken_references": [],
    "intentionally_standalone": [
      "STORY-014",
      "STORY-015",
      "STORY-051",
      "STORY-061",
      "STORY-062",
      "STORY-063"
    ],
    "missing_metadata": [
      "/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-007-post-operation-retrospective-conversation.story.md",
      "/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-008-adaptive-questioning-engine.story.md",
      "/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-009-skip-pattern-tracking.story.md",
      "/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-010-feedback-template-engine.story.md",
      "/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-011-configuration-management.story.md",
      "/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-012-template-customization.story.md",
      "/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-018-event-driven-hook-system.story.md",
      "/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-019-operation-lifecycle-integration.story.md",
      "/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-020-feedback-cli-commands.story.md",
      "/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-033-wire-hooks-into-audit-deferrals-command.story.md",
      "/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-050-refactor-audit-deferrals-budget-compliance.story.md",
      "/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-060-operational-sync.story.md",
      "/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-070-framework-release-automation.story.md",
      "/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-071-wizard-driven-interactive-ui.story.md",
      "/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-072-pre-flight-validation-checks.story.md",
      "/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-073-auto-detection.story.md",
      "/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-074-comprehensive-error-handling.story.md",
      "/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-075-installation-reporting-logging.story.md",
      "/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-076-claudemd-smart-merge.story.md",
      "/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-077-version-detection-compatibility.story.md",
      "/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-078-upgrade-mode-migration-scripts.story.md",
      "/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-079-fix-repair-installation-mode.story.md",
      "/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-080-rollback-previous-version.story.md",
      "/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-081-uninstall-user-content-preservation.story.md",
      "/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-086-coverage-reporting-system.story.md"
    ],
    "summary": {
      "total_orphans": 31
    }
  }
}
[
  "STORY-083",
  "STORY-084",
  "STORY-085",
  "STORY-087",
  "STORY-088",
  "STORY-089"
]
EPIC-015
{"is_valid":true,"referenced_epic":"EPIC-015","epic_exists":true,"epic_title":"Epic Coverage Validation & Requirements Traceability"}
bryan@DESKTOP-88FARC5:/mnt/c/Projects/DevForgeAI2$