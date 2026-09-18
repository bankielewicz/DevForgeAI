## Integration with spec-driven-stories

**Invocation (from parent skill):**
```
# Step 2.1 in requirements-analysis.md

Task(
    subagent_type="story-requirements-analyst",  # Skill-specific (not general-purpose)
    description="Generate user story content",
    prompt="""
    {Enhanced prompt with 4-section template from Phase 1}

    Feature Description: {feature_description}
    Story Context: {story_metadata}

    Generate markdown content (NOT files)
    """
)
```

**Output usage (in parent skill Phase 5):**
```
# Phase 5: Story File Creation

# Load template
template = Read(".claude/skills/spec-driven-stories/assets/templates/story-template.md")

# Insert subagent output
user_story_section = extract_section(subagent_output, "User Story")
ac_section = extract_section(subagent_output, "Acceptance Criteria")
edge_cases_section = extract_section(subagent_output, "Edge Cases")
nfr_section = extract_section(subagent_output, "Non-Functional Requirements")

# Assemble into template
complete_story = template.format(
    user_story=user_story_section,
    acceptance_criteria=ac_section,
    edge_cases=edge_cases_section,
    nfrs=nfr_section,
    ...
)

# Write single file
Write(file_path=f"devforgeai/specs/Stories/{story_id}-{slug}.story.md", content=complete_story)
```

---
