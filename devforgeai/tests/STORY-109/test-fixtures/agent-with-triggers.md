---
name: test-agent-full
description: A test agent with all fields including proactive triggers. Use proactively after code changes.
tools: Read, Write, Grep
model: haiku
proactive_triggers:
  - "after code changes"
  - "when reviewing pull requests"
  - "before git commit"
---

# Test Agent Full

This is a test agent with all frontmatter fields populated.

## Purpose

Used for testing the subagent registry generator.
