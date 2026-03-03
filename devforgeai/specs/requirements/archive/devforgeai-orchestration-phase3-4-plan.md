# DevForgeAI Phases 3 & 4 - Orchestration & Automation

**Date Created:** 2025-10-30
**Status:** Planning
**Context:** Detailed implementation plan for orchestration skill and automation scripts

## Executive Summary

This document provides detailed plans for:

**Phase 3:** devforgeai-orchestration skill - Coordinates Epic → Sprint → Story → Dev → QA → Release workflow
**Phase 4:** Automation scripts - Python utilities for QA analysis tasks

## Phase 3: DevForgeAI Orchestration Skill

### Overview

The orchestration skill is the **workflow coordinator** that manages the entire spec-driven development lifecycle:

```
Epic → Sprint → Story → Architecture → Development → QA → Release
```

### Core Responsibilities

#### 1. Project Management Integration
- Support Epic → Sprint → Story hierarchy
- All work translates to stories for developers
- Track story status through workflow stages
- Enforce workflow sequence

#### 2. Skill Coordination
- Auto-invoke designing-systems if context missing
- Sequence devforgeai-development for implementation
- Invoke devforgeai-qa for validation (light + deep)
- Hand off to devforgeai-release when approved

#### 3. State Management
- Track current story status across workflow
- Validate state transitions
- Prevent skipping workflow stages
- Maintain workflow history

#### 4. Quality Gates
- Context validation gate (before development)
- Test passing gate (before QA)
- QA approval gate (before release)
- Release readiness gate

### Story Workflow States

```
1. Backlog → Not started, awaiting prioritization
2. Architecture → Context files being created/validated
3. Ready for Dev → Context complete, can start development
4. In Development → Implementing with TDD
5. Dev Complete → All tests pass, ready for QA
6. QA In Progress → Light or deep validation running
7. QA Failed → Violations detected, requires fixes
8. QA Approved → All quality gates passed, ready for release
9. Releasing → Deployment in progress
10. Released → Deployed to production
11. Blocked → Waiting for external dependency
```

### State Transition Rules

```
Backlog → Architecture
  Trigger: Story assigned to sprint
  Action: Invoke designing-systems
  Validation: Story has clear acceptance criteria

Architecture → Ready for Dev
  Trigger: All 6 context files exist and validated
  Action: Update story status
  Validation: No architecture violations

Ready for Dev → In Development
  Trigger: Developer starts work
  Action: Invoke devforgeai-development
  Validation: Context files loaded

In Development → Dev Complete
  Trigger: All tests pass (Phase 5 of dev workflow)
  Action: Update story status
  Validation: Build succeeds, tests pass

Dev Complete → QA In Progress
  Trigger: Developer requests QA or auto-triggered
  Action: Invoke devforgeai-qa --mode=deep
  Validation: No compilation errors

QA In Progress → QA Approved
  Trigger: Deep validation PASS
  Action: Update story status, create QA report
  Validation: All quality gates passed

QA In Progress → QA Failed
  Trigger: Deep validation FAIL
  Action: Create action items, return to dev
  Validation: At least one violation detected

QA Failed → In Development
  Trigger: Developer starts fixing issues
  Action: Re-invoke devforgeai-development
  Validation: Action items documented

QA Approved → Releasing
  Trigger: Release initiated
  Action: Invoke devforgeai-release
  Validation: QA report exists with PASS status

Releasing → Released
  Trigger: Deployment successful
  Action: Update story status, close story
  Validation: Deployment confirmation

ANY STATE → Blocked
  Trigger: External dependency needed
  Action: Document blocker, notify team
  Validation: Blocker reason documented
```

### SKILL.md Structure

#### Section 1: Purpose & Philosophy (~2,000 tokens)

**Purpose:**
- Coordinate spec-driven development workflow
- Enforce quality gates
- Manage story lifecycle
- Ensure architectural integrity

**Philosophy:**
- Epic → Sprint → Story decomposition
- Story is atomic unit of work
- Quality over speed
- No skipping workflow stages
- Automated skill invocation

**When to Use:**
- Starting new epic/sprint
- Creating stories
- Managing story workflow
- Checking story status
- Enforcing quality gates

#### Section 2: Epic → Sprint → Story Workflow (~3,000 tokens)

**Epic Creation:**
```
INPUT: High-level business initiative
PROCESS:
  1. Create epic document in ai_docs/Epics/[epic-id].epic.md
  2. Define business goals
  3. Identify success metrics
  4. Estimate scope (story points)
  5. Break down into sprints

OUTPUT: Epic document with sprint breakdown
```

**Sprint Planning:**
```
INPUT: Epic with goals
PROCESS:
  1. Create sprint in ai_docs/Sprints/[sprint-id].sprint.md
  2. Select stories from epic backlog
  3. Estimate capacity
  4. Prioritize stories
  5. Assign story points
  6. Define sprint goals

OUTPUT: Sprint plan with story list
```

**Story Creation:**
```
INPUT: Sprint requirement
PROCESS:
  1. Use story template
  2. Define acceptance criteria (testable, specific)
  3. Define technical spec (API contracts, data models)
  4. Define NFRs (performance, security)
  5. Estimate story points
  6. Set priority
  7. Initialize status: Backlog

OUTPUT: Story document in ai_docs/Stories/[story-id].story.md

TEMPLATE:
---
id: STORY-001
title: [Story Title]
epic: EPIC-001
sprint: SPRINT-001
status: Backlog
points: 3
priority: High
assigned_to: [Developer]
created: 2025-10-30
---

# Story: [Title]

## Description
[User story format: As a [role], I want [feature], so that [benefit]]

## Acceptance Criteria
1. [ ] [Testable criterion 1]
2. [ ] [Testable criterion 2]
3. [ ] [Testable criterion 3]

## Technical Specification

### API Endpoints
- POST /api/[endpoint]
  - Request: { ... }
  - Response: { ... }

### Data Models
- [Model definitions]

### Business Rules
- [Domain logic rules]

## Non-Functional Requirements
- Performance: [target]
- Security: [requirements]
- Scalability: [requirements]

## Dependencies
- [External dependencies]
- [Prerequisite stories]

## Workflow Status
- [ ] Architecture phase complete
- [ ] Development phase complete
- [ ] QA phase complete
- [ ] Released

## Notes
[Additional context]
```

#### Section 3: Workflow Orchestration Logic (~4,000 tokens)

**Workflow Entry Point:**
```
Command: Skill(command="devforgeai-orchestration --story=STORY-001")

ORCHESTRATION WORKFLOW:
  Phase 1: Load Story
  Phase 2: Validate Prerequisites
  Phase 3: Execute Workflow Stage
  Phase 4: Update Story Status
  Phase 5: Determine Next Action
```

**Phase 1: Load Story**
```
Read(file_path="ai_docs/Stories/{story_id}.story.md")

Extract:
  - Current status
  - Acceptance criteria
  - Technical spec
  - Dependencies
  - Workflow checkboxes

Validate:
  - Story file exists
  - Required sections present
  - Status is valid state
```

**Phase 2: Validate Prerequisites**
```
CASE status == "Backlog":
  Check: Is story assigned to sprint?
  Check: Does story have acceptance criteria?
  Check: Are dependencies resolved?

  IF prerequisites met:
    Transition to: Architecture
  ELSE:
    BLOCK: Document missing prerequisites

CASE status == "Architecture":
  Check: Do all 6 context files exist?

  Read(file_path="devforgeai/context/tech-stack.md")
  Read(file_path="devforgeai/context/source-tree.md")
  Read(file_path="devforgeai/context/dependencies.md")
  Read(file_path="devforgeai/context/coding-standards.md")
  Read(file_path="devforgeai/context/architecture-constraints.md")
  Read(file_path="devforgeai/context/anti-patterns.md")

  IF all exist:
    Transition to: Ready for Dev
  ELSE:
    Action: Invoke designing-systems
    Wait: For architecture skill to complete

CASE status == "Ready for Dev":
  Check: Are context files up to date?
  Check: Is developer ready?

  IF ready:
    Transition to: In Development
  ELSE:
    Wait: For developer to start

CASE status == "In Development":
  Check: Is development complete?

  IF dev workflow Phase 5 (Git) complete:
    Transition to: Dev Complete
  ELSE:
    Status: Still in development

CASE status == "Dev Complete":
  Check: Did all tests pass?
  Check: Is build successful?

  IF all checks pass:
    Transition to: QA In Progress
    Action: Invoke devforgeai-qa --mode=deep
  ELSE:
    BLOCK: Fix test failures first

CASE status == "QA In Progress":
  Wait: For QA skill to complete

CASE status == "QA Failed":
  Check: Are action items addressed?

  IF developer ready to fix:
    Transition to: In Development
  ELSE:
    Wait: For fixes

CASE status == "QA Approved":
  Check: Is release ready?

  IF ready:
    Transition to: Releasing
  ELSE:
    Wait: For release trigger

CASE status == "Releasing":
  Action: Invoke devforgeai-release
  Wait: For deployment

CASE status == "Released":
  Complete: Story finished
```

**Phase 3: Execute Workflow Stage**
```
SKILL INVOCATION LOGIC:

IF status == "Architecture" AND context_missing:
  Skill(command="designing-systems")

  WAIT for completion

  PARSE architecture results:
    - Context files created
    - ADRs documented
    - No violations

  UPDATE story:
    - Check "Architecture phase complete"
    - Update status to "Ready for Dev"

IF status == "In Development":
  Skill(command="devforgeai-development --story={story_id}")

  MONITOR progress through phases:
    1. Context Validation
    2. Test-First (Red)
    3. Implementation (Green)
    4. Refactor
    5. Integration
    6. Git workflow

  DURING development, devforgeai-qa invoked automatically:
    - After Phase 2 (light validation)
    - After Phase 3 (light validation)
    - After Phase 4 (light validation)

  WHEN Phase 6 complete:
    UPDATE story:
      - Check "Development phase complete"
      - Update status to "Dev Complete"

IF status == "Dev Complete":
  Skill(command="devforgeai-qa --mode=deep --story={story_id}")

  WAIT for QA completion

  PARSE QA results:
    - Overall status (PASS/FAIL)
    - Coverage percentages
    - Violation counts
    - Action items

  IF QA PASS:
    UPDATE story:
      - Check "QA phase complete"
      - Update status to "QA Approved"
      - Append QA report section

  IF QA FAIL:
    UPDATE story:
      - Update status to "QA Failed"
      - Append QA report section
      - Create action items
      - Notify developer

IF status == "QA Approved":
  Skill(command="devforgeai-release --story={story_id}")

  WAIT for release completion

  PARSE release results:
    - Deployment status
    - Version number
    - Environment

  IF release successful:
    UPDATE story:
      - Check "Released"
      - Update status to "Released"
      - Close story
```

**Phase 4: Update Story Status**
```
Edit(file_path="ai_docs/Stories/{story_id}.story.md",
     old_string="status: {old_status}",
     new_string="status: {new_status}")

# Update workflow checkboxes
IF architecture_complete:
    Edit(file_path="...",
         old_string="- [ ] Architecture phase complete",
         new_string="- [x] Architecture phase complete")

# Add workflow history
history_entry = f"""
## Workflow History

### {timestamp} - {status_change}
- Previous: {old_status}
- Current: {new_status}
- Action: {action_taken}
- Result: {result}
"""

Edit(file_path="...",
     old_string="## Notes",
     new_string=history_entry + "\n\n## Notes")
```

**Phase 5: Determine Next Action**
```
DECISION TREE:

IF status == "Blocked":
  Report: Story blocked - {blocker_reason}
  Action: Notify team, wait for resolution

IF status == "QA Failed":
  Report: QA violations detected
  Action: Return to development
  Next: Developer fixes issues

IF status == "QA Approved":
  Report: Story ready for release
  Action: Can proceed to release or wait

IF status == "Released":
  Report: Story complete
  Action: Close story, update sprint progress

ELSE:
  Report: Story in progress - {status}
  Action: Continue workflow
```

#### Section 4: Quality Gates (~2,000 tokens)

**Gate 1: Context Validation (Before Development)**
```
PURPOSE: Ensure architectural foundation exists

CHECKS:
  - All 6 context files exist
  - Files are not empty
  - No placeholder content (TODO, TBD)
  - Architecture constraints defined
  - Tech stack locked
  - Source tree documented

PASS: Allow development to start
FAIL: Block, invoke designing-systems
```

**Gate 2: Test Passing (Before QA)**
```
PURPOSE: Ensure basic quality before deep validation

CHECKS:
  - Build succeeds
  - All tests pass
  - No compilation errors
  - Light validation passed

PASS: Allow deep QA validation
FAIL: Block, return to development
```

**Gate 3: QA Approval (Before Release)**
```
PURPOSE: Ensure production readiness

CHECKS:
  - Deep validation PASS
  - Coverage meets thresholds (95%/85%/80%)
  - Zero CRITICAL violations
  - Zero HIGH violations (or approved)
  - All acceptance criteria validated
  - QA report generated

PASS: Allow release
FAIL: Block, create action items, return to dev
```

**Gate 4: Release Readiness (Before Production)**
```
PURPOSE: Final safety check

CHECKS:
  - QA approved
  - All story checkboxes complete
  - No blocking dependencies
  - Deployment plan exists
  - Rollback plan exists

PASS: Allow release to production
FAIL: Block, resolve issues
```

#### Section 5: AskUserQuestion Patterns (~1,500 tokens)

**Pattern 1: Story Priority Conflict**
```
SCENARIO: Multiple stories ready, capacity limited

AskUserQuestion:
Question: "Sprint has 3 stories ready but capacity for 2. Which should be prioritized?"
Header: "Priority"
Options:
  - "STORY-001: User authentication (High, 5 points)"
  - "STORY-002: Order history (Medium, 3 points)"
  - "STORY-003: Admin dashboard (Low, 8 points)"
multiSelect: true

Parse answer → Update story priorities
```

**Pattern 2: Workflow Skip Request**
```
SCENARIO: Developer wants to skip QA

AskUserQuestion:
Question: "Developer requested to skip QA for STORY-001 (minor change). Allow?"
Header: "Skip QA?"
Options:
  - "No, enforce QA (recommended)"
  - "Yes, allow skip with documentation"
  - "Run light validation only"
multiSelect: false

IF "No": Enforce normal workflow
IF "Yes": Document exception, proceed to release
IF "Light": Run light validation only
```

**Pattern 3: Blocked Story Resolution**
```
SCENARIO: Story blocked on external dependency

AskUserQuestion:
Question: "STORY-001 blocked on API endpoint from Team B. How to proceed?"
Header: "Blocker"
Options:
  - "Wait for dependency (keep blocked)"
  - "Create mock/stub to unblock"
  - "De-prioritize, start different story"
  - "Escalate to tech lead"
multiSelect: false
```

#### Section 6: Success Criteria (~500 tokens)

**Orchestration Success:**
- [x] Story progresses through all workflow stages
- [x] Quality gates enforced
- [x] Skills invoked in correct sequence
- [x] Story status always accurate
- [x] No workflow stages skipped
- [x] All checkboxes completed before release
- [x] Workflow history documented

### File Structure

```
.claude/skills/devforgeai-orchestration/
├── SKILL.md                           # Main skill file (~12,000 tokens)
├── README.md                          # Usage guide (~1,000 tokens)
├── INTEGRATION_GUIDE.md               # Integration with other skills (~1,500 tokens)
├── references/
│   ├── workflow-states.md             # State definitions (~1,000 tokens)
│   ├── state-transitions.md           # Transition rules (~1,500 tokens)
│   └── quality-gates.md               # Gate definitions (~1,000 tokens)
└── assets/
    └── templates/
        ├── epic-template.md           # Epic document template
        ├── sprint-template.md         # Sprint document template
        └── story-template.md          # Story document template
```

### Token Budget

**SKILL.md:** ~12,000 tokens
- Purpose & philosophy: 2,000
- Epic → Sprint → Story: 3,000
- Workflow orchestration: 4,000
- Quality gates: 2,000
- AskUserQuestion patterns: 1,500
- Success criteria: 500

**Total Phase 3:** ~18,000 tokens (including references and templates)

---

## Phase 4: Automation Scripts

### Overview

Python utilities for QA analysis tasks referenced in devforgeai-qa SKILL.md (lines 2189-2197).

### Scripts Directory Structure

```
.claude/skills/devforgeai-qa/scripts/
├── __init__.py                        # Package initialization
├── generate_coverage_report.py       # Coverage HTML report
├── analyze_complexity.py              # Cyclomatic complexity
├── detect_duplicates.py               # Code duplication
├── validate_spec_compliance.py       # Acceptance criteria validation
├── security_scan.py                   # Security vulnerability scanning
├── generate_test_stubs.py            # Auto-generate test templates
├── requirements.txt                   # Python dependencies
└── README.md                          # Usage documentation
```

### Script 1: generate_coverage_report.py

**Purpose:** Parse coverage data and generate HTML report with visualizations

**Input:** coverage.json, coverage.xml, or .coverage file
**Output:** HTML report with coverage visualization

**Functionality:**
1. Read coverage file (JSON/XML/SQLite)
2. Parse line/branch coverage data
3. Calculate coverage percentages by file/module/layer
4. Identify uncovered code blocks
5. Generate HTML report with:
   - Overall coverage summary
   - Coverage by layer (domain/application/infrastructure)
   - File-by-file breakdown
   - Uncovered line highlighting
   - Coverage trends (if historical data available)

**Key Features:**
- Support multiple coverage formats (.NET, Python, JavaScript)
- Color-coded visualization (green >80%, yellow 60-80%, red <60%)
- Drill-down capability (project → module → file → line)
- Export to JSON for integration

**Implementation (~300 lines):**

```python
#!/usr/bin/env python3
"""
Coverage Report Generator

Parses coverage data from various formats and generates comprehensive HTML reports.
"""

import json
import xml.etree.ElementTree as ET
import sqlite3
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass
from jinja2 import Template

@dataclass
class FileCoverage:
    file_path: str
    total_lines: int
    covered_lines: int
    uncovered_lines: List[int]
    coverage_percentage: float
    layer: str  # domain, application, infrastructure

@dataclass
class LayerCoverage:
    layer_name: str
    total_lines: int
    covered_lines: int
    coverage_percentage: float
    files: List[FileCoverage]

class CoverageReportGenerator:
    def __init__(self, coverage_file: str, source_tree_file: str = None):
        self.coverage_file = Path(coverage_file)
        self.source_tree_file = Path(source_tree_file) if source_tree_file else None
        self.layer_mapping = self._load_layer_mapping()

    def _load_layer_mapping(self) -> Dict[str, str]:
        """Load layer mapping from source-tree.md"""
        if not self.source_tree_file or not self.source_tree_file.exists():
            return {
                "Domain": "domain",
                "Application": "application",
                "Infrastructure": "infrastructure"
            }

        # Parse source-tree.md to extract layer paths
        # Return mapping: {path_pattern: layer_name}
        # Example: {"src/Domain/": "domain", ...}
        pass

    def parse_coverage(self) -> Dict[str, FileCoverage]:
        """Parse coverage file based on format"""
        suffix = self.coverage_file.suffix

        if suffix == '.json':
            return self._parse_coverage_json()
        elif suffix == '.xml':
            return self._parse_coverage_xml()
        elif suffix == '.coverage':
            return self._parse_coverage_sqlite()
        else:
            raise ValueError(f"Unsupported coverage format: {suffix}")

    def _parse_coverage_json(self) -> Dict[str, FileCoverage]:
        """Parse JSON coverage (Python pytest-cov, JavaScript Istanbul)"""
        with open(self.coverage_file) as f:
            data = json.load(f)

        # Parse based on format structure
        # Istanbul: data.files[file].lines, .branches
        # pytest-cov: data.files[file].summary.covered_lines
        pass

    def _parse_coverage_xml(self) -> Dict[str, FileCoverage]:
        """Parse XML coverage (Cobertura format - .NET, Java)"""
        tree = ET.parse(self.coverage_file)
        root = tree.getroot()

        # Parse <packages><package><classes><class> structure
        # Extract line coverage from <lines><line> elements
        pass

    def _parse_coverage_sqlite(self) -> Dict[str, FileCoverage]:
        """Parse SQLite coverage (.NET coverage binary)"""
        # Use coverage.py to read .coverage file
        pass

    def calculate_layer_coverage(self, file_coverage: Dict[str, FileCoverage]) -> List[LayerCoverage]:
        """Group files by layer and calculate layer-level coverage"""
        layers = {}

        for file_path, coverage in file_coverage.items():
            layer = self._identify_layer(file_path)

            if layer not in layers:
                layers[layer] = {
                    "total_lines": 0,
                    "covered_lines": 0,
                    "files": []
                }

            layers[layer]["total_lines"] += coverage.total_lines
            layers[layer]["covered_lines"] += coverage.covered_lines
            layers[layer]["files"].append(coverage)

        # Calculate percentages
        layer_coverage = []
        for layer_name, data in layers.items():
            percentage = (data["covered_lines"] / data["total_lines"] * 100) if data["total_lines"] > 0 else 0
            layer_coverage.append(LayerCoverage(
                layer_name=layer_name,
                total_lines=data["total_lines"],
                covered_lines=data["covered_lines"],
                coverage_percentage=percentage,
                files=data["files"]
            ))

        return layer_coverage

    def _identify_layer(self, file_path: str) -> str:
        """Identify layer from file path"""
        for pattern, layer in self.layer_mapping.items():
            if pattern in file_path:
                return layer
        return "other"

    def generate_html_report(self, output_file: str):
        """Generate HTML report with coverage visualization"""
        file_coverage = self.parse_coverage()
        layer_coverage = self.calculate_layer_coverage(file_coverage)

        # Calculate overall coverage
        total_lines = sum(fc.total_lines for fc in file_coverage.values())
        covered_lines = sum(fc.covered_lines for fc in file_coverage.values())
        overall_percentage = (covered_lines / total_lines * 100) if total_lines > 0 else 0

        # Render HTML template
        template = self._get_html_template()
        html = template.render(
            overall_coverage=overall_percentage,
            layer_coverage=layer_coverage,
            file_coverage=file_coverage,
            timestamp=datetime.now()
        )

        Path(output_file).write_text(html)

    def _get_html_template(self) -> Template:
        """Return Jinja2 HTML template"""
        template_str = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Coverage Report</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                .summary { background: #f0f0f0; padding: 20px; border-radius: 5px; }
                .coverage-high { color: green; }
                .coverage-medium { color: orange; }
                .coverage-low { color: red; }
                table { width: 100%; border-collapse: collapse; margin-top: 20px; }
                th, td { padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }
                th { background: #4CAF50; color: white; }
            </style>
        </head>
        <body>
            <h1>Test Coverage Report</h1>
            <div class="summary">
                <h2>Overall Coverage: {{ "%.2f"|format(overall_coverage) }}%</h2>
                <p>Generated: {{ timestamp }}</p>
            </div>

            <h2>Coverage by Layer</h2>
            <table>
                <tr>
                    <th>Layer</th>
                    <th>Coverage</th>
                    <th>Lines Covered</th>
                    <th>Total Lines</th>
                </tr>
                {% for layer in layer_coverage %}
                <tr>
                    <td>{{ layer.layer_name }}</td>
                    <td class="{% if layer.coverage_percentage >= 80 %}coverage-high{% elif layer.coverage_percentage >= 60 %}coverage-medium{% else %}coverage-low{% endif %}">
                        {{ "%.2f"|format(layer.coverage_percentage) }}%
                    </td>
                    <td>{{ layer.covered_lines }}</td>
                    <td>{{ layer.total_lines }}</td>
                </tr>
                {% endfor %}
            </table>

            <!-- File details... -->
        </body>
        </html>
        """
        return Template(template_str)

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Generate coverage report')
    parser.add_argument('coverage_file', help='Coverage data file (.json, .xml, .coverage)')
    parser.add_argument('--source-tree', help='Path to source-tree.md for layer mapping')
    parser.add_argument('--output', default='coverage-report.html', help='Output HTML file')
    args = parser.parse_args()

    generator = CoverageReportGenerator(args.coverage_file, args.source_tree)
    generator.generate_html_report(args.output)
    print(f"Coverage report generated: {args.output}")

if __name__ == '__main__':
    main()
```

### Script 2: analyze_complexity.py

**Purpose:** Calculate cyclomatic complexity for codebase
**Input:** Source directory path
**Output:** JSON complexity report

**Token Budget:** ~250 lines

### Script 3: detect_duplicates.py

**Purpose:** Find code duplication across codebase
**Input:** Source directory path
**Output:** JSON duplication report

**Token Budget:** ~200 lines

### Script 4: validate_spec_compliance.py

**Purpose:** Check implementation against story spec
**Input:** Story file path, test directory
**Output:** JSON compliance report

**Token Budget:** ~250 lines

### Script 5: security_scan.py

**Purpose:** Scan for security vulnerabilities
**Input:** Source directory path
**Output:** JSON security report

**Token Budget:** ~300 lines

### Script 6: generate_test_stubs.py

**Purpose:** Auto-generate test stubs for untested code
**Input:** Source file path, test framework
**Output:** Generated test file

**Token Budget:** ~200 lines

### requirements.txt

```txt
# Coverage parsing
coverage>=7.0.0
lxml>=4.9.0

# Complexity analysis
radon>=6.0.0
lizard>=1.17.0

# Code duplication
jscpd>=3.5.0

# Security scanning
bandit>=1.7.0
safety>=2.3.0

# Report generation
jinja2>=3.1.0
markdown>=3.5.0

# Utilities
pytest>=7.4.0
pytest-cov>=4.1.0
```

### README.md

Usage documentation for all scripts with examples.

### Total Token Budget Phase 4: ~2,000 tokens

---

## Implementation Timeline

### Phase 3: Orchestration Skill
**Estimated Time:** 2-3 hours
**Token Budget:** ~18,000 tokens

**Steps:**
1. Create SKILL.md with all workflow logic
2. Create reference materials (states, transitions, gates)
3. Create templates (epic, sprint, story)
4. Document integration points
5. Test workflow with mock story

### Phase 4: Automation Scripts
**Estimated Time:** 1-2 hours
**Token Budget:** ~2,000 tokens

**Steps:**
1. Create scripts directory structure
2. Implement each script with core functionality
3. Create requirements.txt
4. Document usage in README.md
5. Test scripts with sample data

### Total Estimated Budget: ~20,000 tokens (well under 136k remaining)

---

## Success Criteria

### Phase 3 Success
- [x] Orchestration SKILL.md created with complete workflow
- [x] All workflow states documented
- [x] State transitions validated
- [x] Quality gates defined
- [x] Integration with dev/QA/architecture skills clear
- [x] Story templates created
- [x] AskUserQuestion patterns included

### Phase 4 Success
- [x] All 6 scripts created and functional
- [x] Scripts integrate with QA skill
- [x] requirements.txt complete
- [x] README.md with usage examples
- [x] Scripts tested with sample data

---

## Next Steps

After Phases 3 & 4 complete:

1. **Integration Testing:** Test full workflow with real story
2. **Documentation:** Update main README with complete framework
3. **User Guide:** Create end-to-end usage guide
4. **Validation:** Run through sample Epic → Sprint → Story → Release
5. **Iteration:** Refine based on real-world usage

---

**End of Phases 3 & 4 Plan**
