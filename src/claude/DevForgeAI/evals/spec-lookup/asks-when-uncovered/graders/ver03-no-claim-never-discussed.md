---
type: llm
---

The workspace's docs/specs/ holds two specs about exports and an ADR about storing export files. Nothing in it
mentions a dark mode, a theme or colours.

Judge only the final reply.
PASS if all of these hold:
- It says a dark mode is not in any of the project's specs, so it is the user's decision.
- It marks it with [NEEDS CLARIFICATION: not in any spec ...] and leaves it unbuilt.
- It doesn't say or imply that a dark mode was never discussed or was ruled out; a search with no match is
  reported as no match, not as proof.
- It doesn't claim to have built, written or planned a dark mode as decided.
FAIL if any of these is missing.
