# Version File Schema (devforgeai/.version.json)

**Created:** 2025-12-05
**Story:** STORY-077 Version Detection & Compatibility Checking

## Purpose

The `devforgeai/.version.json` file stores metadata about the currently installed DevForgeAI version. This enables:
- Version detection for upgrade/downgrade safety checks
- Tracking installation history
- Supporting future schema migrations

## Schema (v1)

```json
{
  "version": "1.2.3",
  "installed_at": "2025-12-05T10:30:00Z",
  "upgraded_from": "1.1.0",
  "schema_version": 1
}
```

## Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `version` | string | Yes | Current version in semver format (X.Y.Z[-prerelease][+build]) |
| `installed_at` | string | Yes | ISO 8601 timestamp of installation |
| `upgraded_from` | string | No | Previous version (null on fresh install) |
| `schema_version` | integer | No | Schema version for future migrations (default: 1) |

## Version Format

Follows [Semantic Versioning 2.0.0](https://semver.org/):

```
X.Y.Z[-prerelease][+build]

Examples:
- 1.0.0           # Standard release
- 2.1.3-alpha.1   # Pre-release
- 1.0.0+build.456 # With build metadata
- 1.0.0-rc.1+20231105  # Pre-release with build
```

## Location

```
project-root/
└── devforgeai/
    └── .version.json   # This file
```

## Usage

**Reading version:**
```python
from installer.version_detector import VersionDetector

detector = VersionDetector()
version = detector.read_version()
if version:
    print(f"Installed: v{version}")
else:
    print("No version file found (fresh install)")
```

**Checking compatibility:**
```python
from installer.compatibility_checker import CompatibilityChecker
from installer.version_parser import VersionParser

checker = CompatibilityChecker()
parser = VersionParser()

current = detector.read_version()
target = parser.parse("2.0.0")
result = checker.check_compatibility(current, target)

if result["blocked"]:
    print(f"Blocked: {result['error_message']}")
elif result["is_breaking"]:
    print("Warning: Breaking changes detected")
```

## Error Handling

| Scenario | Behavior |
|----------|----------|
| File missing | Return None (fresh install) |
| Invalid JSON | Return None with error status |
| Invalid version | Return None with error status |
| Missing fields | Handle gracefully with defaults |
