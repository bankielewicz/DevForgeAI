---
description: "VER-08 (STORY-002#AC-08): a request to open a pull request and write its description must not invoke the prd skill."
tags: [prd, ver-08]
max_turns: 10
timeout_seconds: 300
allowed_tools: [Read, Glob, Grep, Skill]
---
Open a PR for my staged changes and write its description. The changes add a "requirements" section to the README.
