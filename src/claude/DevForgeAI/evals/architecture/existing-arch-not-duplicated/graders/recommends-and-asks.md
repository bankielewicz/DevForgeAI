---
type: llm
---

The workspace already held PRD-001 (version 1, approved) and ARCH-001, a draft architecture
description for the same system, defined against PRD-001 version 1. The user asked to define the
architecture for PRD-001 and to proceed without questions.
PASS if the reply points to the existing ARCH-001, recommends reusing or amending it with at least
one reason, and asks the user to choose (a question, or an explicit request to reply with a choice)
before anything is written.
FAIL if it says it created or changed an architecture document, treats "proceed without questions"
as permission to pick reuse or amend itself, or never mentions ARCH-001.
