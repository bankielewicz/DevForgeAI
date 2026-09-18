# Phase 3 Intelligence Synthesis Patterns for Internet Sleuth

**Version**: 1.0 | **Status**: Reference | **Agent**: internet-sleuth

---

## Step 3.1.1: Invoke context-validator Subagent

```python
Task(
  subagent_type="context-validator",
  description="Validate research recommendations",
  prompt=f"""
  Validate the following research recommendations against all 6 context files:

  Recommended Technologies:
  {format_recommendations(top_recommendations)}

  Recommended Patterns:
  {format_patterns(extracted_patterns)}

  Recommended Dependencies:
  {format_dependencies(suggested_packages)}

  Check for violations of:
  - tech-stack.md (locked technologies)
  - source-tree/ (project structure)
  - dependencies.md (approved packages)
  - coding-standards.md (code patterns and conventions)
  - architecture-constraints.md (layer boundaries, dependency rules)
  - anti-patterns.md (forbidden patterns)

  Return: Structured violation report with severity categorization
  """
)
```

## Step 3.1.2: Parse Validation Results

```python
validation_result = context_validator_result

# Extract violations by severity
critical_violations = [v for v in validation_result.violations if v.severity == "CRITICAL"]
high_violations = [v for v in validation_result.violations if v.severity == "HIGH"]
medium_violations = [v for v in validation_result.violations if v.severity == "MEDIUM"]
low_violations = [v for v in validation_result.violations if v.severity == "LOW"]

# Categorize quality gate status
if len(critical_violations) > 0:
    quality_gate_status = "BLOCKED"  # Requires user decision
elif len(high_violations) > 0:
    quality_gate_status = "FAIL"      # Blocking, must fix
elif len(medium_violations) > 0:
    quality_gate_status = "WARN"      # Non-blocking, log warnings
else:
    quality_gate_status = "PASS"      # Fully compliant
```

## Step 3.1.3: Handle CRITICAL Violations (BLOCKED Status)

```python
if quality_gate_status == "BLOCKED":
    for violation in critical_violations:
        # Display violation details
        display(f"❌ CRITICAL: {violation.description}")
        display(f"   Context File: {violation.context_file}")
        display(f"   Recommended: {violation.recommendation}")
        display(f"   Existing: {violation.existing_value}")

        # Trigger AskUserQuestion for user decision
        response = AskUserQuestion(
            questions=[{
                question: f"Research recommends {violation.recommendation} but {violation.context_file} specifies {violation.existing_value}. How to proceed?",
                header: "Context Conflict",
                multiSelect: false,
                options: [
                    {
                        label: f"Update {violation.context_file} + create ADR",
                        description: f"Adopt research recommendation ({violation.recommendation}), document decision"
                    },
                    {
                        label: f"Use existing ({violation.existing_value})",
                        description: "Respect current context file, adjust research scope"
                    },
                    {
                        label: "Document as technical debt",
                        description: "Defer decision, create follow-up story for resolution"
                    }
                ]
            }]
        )

        # Handle user decision
        if "Update" in response:
            display(f"✓ User approved: Update {violation.context_file}")
            display(f"  ADR required: ADR-XXX-adopt-{violation.recommendation}.md")
            # Note in report: User approved tech-stack.md update
        elif "existing" in response:
            display(f"✓ User chose: Keep {violation.existing_value}")
            # Adjust research scope - re-research with existing tech
        else:
            display(f"⚠️ Technical debt: Conflict deferred to future story")
            # Create follow-up story reference
```

## Step 3.1.4: Log Non-Critical Violations (WARN/FAIL Status)

```python
if len(high_violations) > 0:
    display(f"❌ HIGH violations: {len(high_violations)} (blocking, must resolve)")
    for v in high_violations:
        display(f"   - {v.description} ({v.context_file})")

if len(medium_violations) > 0:
    display(f"⚠️ MEDIUM violations: {len(medium_violations)} (warnings, non-blocking)")
    for v in medium_violations:
        display(f"   - {v.description} ({v.context_file})")

if len(low_violations) > 0:
    display(f"ℹ️ LOW violations: {len(low_violations)} (informational)")
```

## Step 3.1.5: Generate Framework Compliance Section

```markdown
## Framework Compliance Check

**Validation Date:** {timestamp}
**Context Files Checked:** 6/6 ✅

| Context File | Status | Violations | Details |
|--------------|--------|------------|---------|
| tech-stack.md | {status} | {count} | {details} |
| source-tree/ | {status} | {count} | {details} |
| dependencies.md | {status} | {count} | {details} |
| coding-standards.md | {status} | {count} | {details} |
| architecture-constraints.md | {status} | {count} | {details} |
| anti-patterns.md | {status} | {count} | {details} |

**Violations Detail:**
{format_violations(all_violations)}

**Quality Gate Status:** {quality_gate_status}
**Recommendation:** {action_based_on_status}
```

**Severity Categorization Rules:**
- **CRITICAL:** Contradicts tech-stack.md locked technologies
- **HIGH:** Violates architecture-constraints.md layer boundaries or dependencies.md
- **MEDIUM:** Conflicts with coding-standards.md naming/patterns
- **LOW:** Minor style deviation or informational note

## Step 3.3.2: Assign Research ID (Gap-Aware)

```python
# Find existing research IDs in devforgeai/specs/research/shared/
existing_reports = Glob(pattern="devforgeai/specs/research/shared/RESEARCH-*.md")
existing_ids = [extract_id(report) for report in existing_reports]  # [1, 3, 5]

# Fill gaps before incrementing
for i in range(1, max(existing_ids) + 1):
    if i not in existing_ids:
        research_id = f"RESEARCH-{i:03d}"  # RESEARCH-002 (fills gap)
        break
else:
    # No gaps, increment highest
    next_id = max(existing_ids) + 1 if existing_ids else 1
    research_id = f"RESEARCH-{next_id:03d}"

display(f"✓ Research ID assigned: {research_id}")
```

## Step 3.3.5: Validate Report Completeness

```python
# Validation checklist from template
validation_checks = [
    check_yaml_frontmatter_complete(),
    check_research_id_format(),
    check_epic_story_references_exist(),
    check_all_9_sections_present(),
    check_executive_summary_max_3_sentences(),
    check_framework_compliance_validates_6_files(),
    check_recommendations_ranked_top_3(),
    check_risk_assessment_has_5_plus_risks(),
    check_adr_readiness_status_clear()
]

if all(validation_checks):
    display("✅ Report validation: PASS (all checks passed)")
else:
    display("⚠️ Report validation: INCOMPLETE")
    for check in validation_checks:
        if not check.passed:
            display(f"   - {check.name}: FAILED ({check.reason})")
```

## Step 3.3.6: Determine Output Location

```python
# Output location based on research scope
if epic_id and not story_id:
    # Epic-level feasibility research
    output_dir = "devforgeai/specs/research/feasibility/"
    filename = f"{epic_id}-{timestamp_slug}-research.md"
elif story_id:
    # Story-specific research
    output_dir = "devforgeai/specs/research/feasibility/"
    filename = f"{story_id}-{timestamp_slug}-research.md"
else:
    # Multi-epic or general research
    output_dir = "devforgeai/specs/research/shared/"
    filename = f"{research_id}-{topic_slug}.md"

output_path = output_dir + filename
```

## Step 3.3.8: Update Epic/Story YAML Frontmatter (If Applicable)

```python
if epic_id or story_id:
    # Load epic/story file
    epic_file = f"devforgeai/specs/Epics/{epic_id}.epic.md" if epic_id else None
    story_file = f"devforgeai/specs/Stories/{story_id}.story.md" if story_id else None

    target_file = epic_file or story_file
    Read(file_path=target_file)

    # Check if research_references field exists
    if "research_references:" in frontmatter:
        # Append to existing list
        Edit(
            file_path=target_file,
            old_string=f"research_references: {existing_list}",
            new_string=f"research_references: {existing_list + [research_id]}"
        )
    else:
        # Add new field after YAML frontmatter
        Edit(
            file_path=target_file,
            old_string="---\n\n# ",
            new_string=f"research_references:\n  - {research_id}\n---\n\n# "
        )

    display(f"✓ Updated {target_file} with research reference")
```
