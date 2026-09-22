---
description: "VER-06 (STORY-001#AC-05): a request that mentions ideas but asks for a review must not invoke the brainstorm skill."
tags: [brainstorm, ver-06, negative-trigger]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---
Review the ideas in this pull request description and tell me which ones are risky:

"This PR moves session tokens from localStorage to an httpOnly cookie, adds a 15-minute idle timeout, and caches the account balance in the service worker so the dashboard loads offline."
