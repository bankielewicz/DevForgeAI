### Phase 5: Release Documentation

**Objective**: Document release for audit trail and communication

#### Step 1: Generate Release Notes

```
Read(file_path=".claude/skills/devforgeai-release/assets/templates/release-notes-template.md")

release_notes = populate_template(
    version, story_id, story_title, changes, qa_status,
    coverage, deployment_strategy, timestamps, metrics, rollback_command
)

Write(file_path=".devforgeai/releases/release-{version}.md", content=release_notes)
```

#### Step 2: Update Story Status

```
Read(file_path=".ai_docs/Stories/{story_id}.story.md")

Edit(file_path=".ai_docs/Stories/{story_id}.story.md",
     old_string="status: QA Approved",
     new_string="status: Released")

Edit(file_path=".ai_docs/Stories/{story_id}.story.md",
     old_string="- [ ] Released",
     new_string="- [x] Released")

# Append workflow history
history_entry = """
### {timestamp} - Released
- **Previous Status:** QA Approved
- **Action Taken:** Production deployment via {strategy}
- **Version:** {version}
- **Smoke Tests:** PASS
- **Metrics:** Within acceptable thresholds
"""

Append to workflow history section
```

#### Step 3: Update Changelog

```
IF file_exists("CHANGELOG.md"):
    changelog_entry = """## [{version}] - {date}

### {change_type}
{story_changes}

### Deployment
- Story: {story_id}
- QA Coverage: {coverage}%
- Strategy: {deployment_strategy}
"""

    Edit(file_path="CHANGELOG.md",
         old_string="## [Unreleased]",
         new_string="## [Unreleased]\n\n{changelog_entry}")
```

---

