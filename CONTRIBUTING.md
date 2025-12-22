# Contributing to DevForgeAI

Thank you for contributing to DevForgeAI! This document provides guidelines for contributing to the project.

## Release Process

### Prerequisites

Before creating a release, ensure:
1. All tests passing: `npm test`
2. Code coverage meets thresholds (≥80%)
3. Story status is "QA Approved"
4. NPM_TOKEN secret configured in GitHub repository

### Version Management

DevForgeAI follows [Semantic Versioning](https://semver.org/):
- **MAJOR** (v2.0.0): Breaking changes
- **MINOR** (v1.1.0): New features, backward compatible
- **PATCH** (v1.0.1): Bug fixes, backward compatible
- **Pre-release** (v1.1.0-beta.1, v2.0.0-rc.1): Testing versions

### Creating a Release

#### Step 1: Update Version

Update `package.json` version:
```bash
# For patch release (bug fixes)
npm version patch

# For minor release (new features)
npm version minor

# For major release (breaking changes)
npm version major

# For pre-release
npm version prepatch --preid=beta  # v1.0.1-beta.0
npm version preminor --preid=rc    # v1.1.0-rc.0
```

#### Step 2: Create Git Tag

The `npm version` command automatically creates a git tag. Alternatively, create manually:

```bash
# Ensure version matches package.json
VERSION=$(node -p "require('./package.json').version")
git tag -a "v${VERSION}" -m "Release v${VERSION}"
```

#### Step 3: Push Tag to GitHub

```bash
# Push tag to trigger GitHub Actions workflow
git push origin v1.0.0

# The workflow will automatically:
# - Run tests (npm test)
# - Validate version matches tag
# - Publish to NPM registry with provenance
# - Assign appropriate dist-tag (latest/beta/rc)
```

#### Step 4: Verify Publication

After workflow completes (~5 minutes):

```bash
# Check NPM registry
npm view devforgeai

# Verify version is published
npm view devforgeai@1.0.0

# Install and test
npm install -g devforgeai@1.0.0
devforgeai --version
```

### Dist-Tag Management

The workflow automatically assigns dist-tags:

- **Stable versions** (`v1.0.0`, `v2.1.0`): Published to `latest` tag
  ```bash
  npm install devforgeai        # Installs latest stable
  npm install devforgeai@latest # Explicit latest
  ```

- **Beta versions** (`v1.1.0-beta.1`): Published to `beta` tag
  ```bash
  npm install devforgeai@beta
  npm install devforgeai@1.1.0-beta.1
  ```

- **RC versions** (`v2.0.0-rc.1`): Published to `rc` tag
  ```bash
  npm install devforgeai@rc
  npm install devforgeai@2.0.0-rc.1
  ```

### Troubleshooting

#### Version Already Published

If you push a tag for a version already on NPM:
- Workflow will detect duplicate and skip publish
- Exit with success (idempotent behavior)
- No error - this is expected

#### NPM_TOKEN Authentication Failed

If publish fails with 401/403 error:
1. Verify NPM_TOKEN secret exists in GitHub repository settings
2. Check token has "Automation" access level (publish permissions)
3. Regenerate token if expired
4. Update GitHub secret with new token

#### Version Mismatch Error

If tag doesn't match package.json:
```
Error: Version mismatch: tag is "1.0.1" but package.json is "1.0.0"
```

**Fix:**
```bash
# Update package.json to match tag
npm version 1.0.1 --no-git-tag-version

# Or delete incorrect tag and recreate
git tag -d v1.0.1
git push origin :refs/tags/v1.0.1
npm version patch  # Creates correct tag
```

#### Workflow Not Triggering

Verify tag matches pattern `v*.*.*`:
```bash
# Valid tags
git tag v1.0.0  ✓
git tag v2.1.3  ✓
git tag v1.0.0-beta.1  ✓

# Invalid tags (won't trigger workflow)
git tag 1.0.0   ✗ (missing 'v' prefix)
git tag release-1.0.0  ✗ (doesn't match pattern)
```

### Rollback a Release

To unpublish a version (use sparingly - breaks users):
```bash
# Unpublish specific version (within 72 hours of publish)
npm unpublish devforgeai@1.0.0

# Deprecate instead (recommended - doesn't break users)
npm deprecate devforgeai@1.0.0 "Version deprecated, use v1.0.1+"
```

### NPM Registry Setup (First-Time Only)

#### 1. Create NPM Account
- Sign up at https://www.npmjs.com/
- Verify email address

#### 2. Generate Automation Token
1. Log into npmjs.com
2. Click profile → "Access Tokens"
3. Click "Generate New Token" → "Automation" (not "Publish" or "Read-only")
4. Copy token (starts with `npm_`)

#### 3. Configure GitHub Secret
1. Go to GitHub repository → Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Name: `NPM_TOKEN`
4. Value: (paste token from step 2)
5. Click "Add secret"

### Pre-Release Testing

Test workflow before releasing to `latest` tag:

```bash
# Create test tag
git tag v0.0.0-test.1
git push origin v0.0.0-test.1

# Workflow will:
# - Run all validations
# - Publish to NPM with 'test' dist-tag
# - NOT affect 'latest' tag

# Verify test publish
npm view devforgeai@0.0.0-test.1

# Clean up test version (optional)
npm unpublish devforgeai@0.0.0-test.1
```

## Line Ending Normalization

This project uses `.gitattributes` to normalize all text files to LF line endings. This prevents CRLF/LF inconsistencies when developing on Windows/WSL.

### How It Works

- **Text files:** Automatically normalized to LF on commit (`* text=auto eol=lf`)
- **Shell scripts:** Explicitly set to LF (`*.sh text eol=lf`) - critical for WSL execution
- **Binary files:** Marked as binary to prevent corruption (`.png`, `.jpg`, `.pdf`, `.zip`, etc.)

### For Developers on Windows

No special configuration needed. Git will automatically:
- Convert CRLF to LF when you commit
- Keep your working copy with your preferred line endings

### If You See Line Ending Issues

If you encounter `$'\r': command not found` errors when running shell scripts on WSL/Linux, the file has CRLF line endings. Fix with:

```bash
# Fix single file
sed -i 's/\r$//' script.sh

# Renormalize entire repository
git add --renormalize .
git commit -m "chore: normalize line endings to LF"
```

### Technical Details

See `.gitattributes` at project root for the complete rule set. Implemented in STORY-122.

## Development Workflow

For general development workflow, see:
- [README.md](./README.md) - Project overview and setup
- [ROADMAP.md](./ROADMAP.md) - Feature roadmap
- Story files in `devforgeai/specs/Stories/` - Detailed implementation specs

## Questions?

- Open an issue for bugs or feature requests
- Check existing stories in `devforgeai/specs/Stories/` for planned work
- Review ADRs in `devforgeai/adrs/` for architectural decisions
