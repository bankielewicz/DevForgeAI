# Coding Standards - DevForgeAI Framework

**Status**: LOCKED
**Last Updated**: 2025-10-30
**Version**: 1.0

## Framework Coding Standards

### Markdown Documentation Style

**All framework components use Markdown with specific patterns**:

✅ **CORRECT Style**:
```markdown
## Phase 1: Context Validation

Read context files in PARALLEL:
- Read(file_path="devforgeai/context/tech-stack.md")
- Read(file_path="devforgeai/context/source-tree.md")

HALT if ANY file missing: "Context files incomplete"
```

❌ **FORBIDDEN Style**:
```markdown
## Phase 1: Context Validation

The system should read context files. First it validates...
[Narrative prose instead of direct instructions]
```

**Rationale**: Claude interprets direct instructions better than prose.

### Tool Usage Standards

**LOCKED: Use Native Tools Over Bash**

✅ **CORRECT**:
```markdown
Read(file_path="story.md")
Edit(file_path="config.md", old_string="v1.0", new_string="v1.1")
Glob(pattern="**/*.md")
Grep(pattern="LOCKED", glob="**/*.md")
```

❌ **FORBIDDEN**:
```markdown
Bash(command="cat story.md")
Bash(command="sed -i 's/v1.0/v1.1/' config.md")
Bash(command="find . -name '*.md'")
Bash(command="grep 'LOCKED' **/*.md")
```

**Exception**: Bash required for tests, builds, git, package managers.

### YAML Frontmatter Standards

**All skills, subagents, commands MUST have frontmatter**:

```yaml
---
name: skill-name
description: Brief description of when to use this
tools: Read, Write, Edit, Bash   # Optional, comma-separated
model: inherit                   # Optional: sonnet, haiku, opus, inherit
---
```

### Progressive Disclosure Pattern

✅ **CORRECT**:
```markdown
# SKILL.md (main file - concise)
## Phase 3: Complexity Assessment
Score complexity on 0-60 scale.
For detailed scoring rubric, see references/complexity-assessment-matrix.md

# references/complexity-assessment-matrix.md (deep details)
[1000 lines of detailed scoring criteria]
```

❌ **FORBIDDEN**:
```markdown
# SKILL.md (monolithic - verbose)
## Phase 3: Complexity Assessment
[1000 lines of detailed scoring criteria inline]
```

### AskUserQuestion Pattern

**LOCKED: Use for ALL ambiguities**:

```markdown
Question: "Which [technology/pattern/approach] should be used?"
Header: "[Category]"
Description: "This decision will be locked in [context-file]"
Options:
  - "[Option 1] (recommended for [reason])"
  - "[Option 2] (better for [use-case])"
  - "[Option 3] ([tradeoff])"
multiSelect: false
```

### File Size Standards

**LOCKED Component Size Limits**:
- Skills: Target 500-800 lines, Max 1,000 lines
- Commands: Target 200-400 lines, Max 500 lines
- Subagents: Target 100-300 lines, Max 500 lines
- Context Files: Target 200-400 lines, Max 600 lines

**Enforcement**: Extract to references/ when exceeding target.

### Naming Conventions

**Files**: lowercase-with-hyphens.md
**Skills**: devforgeai-[phase]
**Subagents**: [domain]-[role]
**Commands**: [action] or [action]-[object]

### Documentation Structure Pattern

**Standard Section Order**:
1. YAML frontmatter
2. Purpose statement
3. When to Use
4. Workflow/Process (numbered phases)
5. Reference files
6. Success criteria

---

## WSL Test Execution

### Path Handling

**Use `/mnt/c/` paths in WSL, not `C:\`**

When running tests on Windows Subsystem for Linux (WSL), always reference files using Unix-style paths with the `/mnt/c/` prefix. pytest discovers tests from Unix-style paths, and coverage reports use Unix paths.

✅ **Correct**:
```
/mnt/c/Projects/DevForgeAI2/tests/
/mnt/c/Projects/DevForgeAI2/src/
```

❌ **Incorrect**:
```
C:\Projects\DevForgeAI2\tests\
C:\Projects\DevForgeAI2\src\
```

**Rationale**: WSL mount points may not preserve file metadata or execute permissions when using Windows-style paths. Unix paths work consistently across WSL and native Linux.

---

### Environment Setup

**Set Python path and navigate to project root**

Before running tests, configure your WSL environment with these commands:

```bash
cd /mnt/c/Projects/DevForgeAI2
export PYTHONPATH=".:$PYTHONPATH"
```

**Why**: `PYTHONPATH` tells Python where to find module imports. This export adds the current directory (`.`) to the search path, allowing pytest to discover project modules. Without this, you'll get "ModuleNotFoundError" when running tests.

---

### Common Issues and Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| Module not found | PYTHONPATH not set | `export PYTHONPATH=".:$PYTHONPATH"` |
| Permission denied on .sh | Windows file locks | Close file in other programs, or `chmod +x script.sh` |
| Line ending errors (`$'\r': command not found`) | CRLF in shell scripts | `dos2unix script.sh` or `sed -i 's/\r$//' script.sh` |
| Slow file operations | Windows filesystem overhead | Run tests from WSL native filesystem if possible |
| pytest not found | Virtual env not activated | `source venv/bin/activate` or `pip install pytest` |

---

### Test Commands

**Run pytest with these commands**:

```bash
pytest tests/ -v                                          # Run all tests

pytest tests/test_validators.py -v                        # Run specific test file

pytest tests/ --cov=src --cov-report=term-missing        # Run with coverage report

pytest tests/test_validators.py::test_dod_validation -v  # Run single test
```

---

### Shell Script Testing

**Always run shell scripts with `bash`, not direct execution**

When executing shell scripts on WSL, use explicit `bash` invocation instead of direct execution.

✅ **Correct**:
```bash
bash path/to/test.sh
bash tests/run_story_tests.sh
```

❌ **Incorrect**:
```bash
./path/to/test.sh
./tests/run_story_tests.sh
```

**Why**: WSL mount points (especially when accessing Windows filesystem) may not preserve execute permissions correctly. Explicit `bash` invocation bypasses permission issues.

**Fix line endings first**: Before running, ensure scripts have Unix line endings:
```bash
dos2unix path/to/test.sh && bash path/to/test.sh
```

---

> **Note**: Projects using DevForgeAI will have their own coding-standards.md with language-specific patterns (CSharp, Python, JavaScript, etc.).
