---
type: llm
---

PASS if the reply stops without writing a PRD and names both conflicting settings: SET-01 in
POL-001 (the organization's identity platform, which allows no override) and SET-01 in
POL-002 (the project's different identity platform), and names rule SV-04.
FAIL if it writes a PRD, silently picks one platform, or names only one of the settings.
