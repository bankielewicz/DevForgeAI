# Git Repository Validation

## Purpose

Validate that the current working directory is a valid Git repository suitable for GitHub Actions workflow generation.

## Validation Steps

### 1. Git Directory Exists

Check for `.git/` directory:

```
Glob(pattern=".git/HEAD")
```

**Pass:** `.git/HEAD` file exists
**Fail:** HALT with "Not a Git repository. Initialize git before running CI setup."

### 2. Working Tree Status

Check for uncommitted changes:

```bash
git status --porcelain
```

**Clean (empty output):** Proceed normally
**Dirty (non-empty output):** Display warning:
```
Warning: Uncommitted changes detected.
Generated workflow files will need to be committed separately.
Consider committing current changes first.
```

Do NOT halt on dirty working tree -- this is a warning only. The user may intentionally want to generate workflows alongside other changes.

### 3. Remote Configuration (Informational)

Check if a remote is configured:

```bash
git remote -v
```

**Has remote:** Workflows can be pushed and will function on GitHub
**No remote:** Display informational message:
```
Note: No Git remote configured.
Add a remote before pushing workflow files:
  git remote add origin https://github.com/{owner}/{repo}.git
```

This is informational only -- do NOT halt.

## Error Messages

| Condition | Message | Severity |
|-----------|---------|----------|
| No .git/ directory | "Not a Git repository" | HALT |
| Dirty working tree | "Uncommitted changes detected" | WARNING |
| No remote configured | "No Git remote configured" | INFO |
