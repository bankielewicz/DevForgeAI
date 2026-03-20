---
description: Scan for orphaned files, duplicate templates, backup artifacts, and sync drift
argument-hint: "[--category=all|backups|duplicates|orphans|drift|agents|context] [--output=console|file]"
model: opus
allowed-tools: Glob, Grep, Read, Bash(wc:*), Bash(ls:*), Bash(du:*), Write
---

# /audit-orphans - Orphaned File & Duplicate Detection Audit

(Backup of original before spec-driven-lifecycle migration)

Key reference on line 105:
    - sprint-template.md (canonical: .claude/skills/devforgeai-orchestration/assets/templates/)

**BACKUP:** Pre-spec-driven-lifecycle migration backup (2026-03-20)