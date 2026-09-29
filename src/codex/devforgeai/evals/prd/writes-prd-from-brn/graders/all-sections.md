---
type: regex
target: {source: file, path: docs/specs/prd/PRD-001.md}
match: contains
flags: m
---
^id: PRD-001\n^type: prd\n[\s\S]*^## 1\. Summary\n[\s\S]*^## 2\. Problem and opportunity\n[\s\S]*^## 3\. Users and personas\n[\s\S]*^## 4\. Goals and non-goals\n[\s\S]*^## 5\. Success metrics\n[\s\S]*^## 6\. Functional requirements\n[\s\S]*^## 7\. Non-functional requirements\n[\s\S]*^## 8\. User experience\n[\s\S]*^## 9\. Constraints and dependencies\n[\s\S]*^## 10\. Assumptions and risks\n[\s\S]*^## 11\. Release and rollout\n[\s\S]*^## 12\. Open questions\n[\s\S]*^## 13\. Epic map\n[\s\S]*^## Change Log\n
