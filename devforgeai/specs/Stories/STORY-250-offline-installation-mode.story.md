---
id: STORY-250
title: Offline Installation Mode
type: feature
epic: EPIC-039
sprint: Backlog
priority: Medium
points: 5
depends_on: ["STORY-249"]
status: Backlog
created: 2025-01-06
updated: 2025-01-06
format_version: "2.5"
---

# STORY-250: Offline Installation Mode

## User Story

**As an** enterprise administrator in an air-gapped network,
**I want** to install DevForgeAI without internet access,
**So that** I can deploy to secure environments with no external connectivity.

## Acceptance Criteria

### AC#1: Offline Bundle Creation

**Given** a DevForgeAI installation package
**When** the bundler runs `python -m installer bundle --output devforgeai-offline.tar.gz`
**Then** an offline bundle is created containing:
- All framework files (.claude/, devforgeai/)
- CLI tools
- Templates and examples
- Checksum manifest (SHA256)
- Bundle metadata (version, creation date)
**And** bundle size is optimized (compressed)
**And** bundle includes installation script

### AC#2: Bundle Integrity Verification

**Given** an offline bundle `devforgeai-offline.tar.gz`
**When** the installer runs with `--offline --bundle devforgeai-offline.tar.gz`
**Then** the bundle checksum is verified against manifest
**And** each file's SHA256 hash is validated
**And** corrupted files cause installation failure with error code 5
**And** validation log shows which files passed/failed

**Example Manifest:**
```yaml
version: "1.0.0"
created: "2025-01-06T12:00:00Z"
files:
  - path: ".claude/skills/devforgeai-development/skill.md"
    sha256: "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    size: 1024
  - path: "devforgeai/specs/context/tech-stack.md"
    sha256: "d8e8fca2dc0f896fd7cb4cb0031ba249"
    size: 2048
```

### AC#3: No Network Calls During Installation

**Given** an offline installation is in progress
**When** any installation step executes
**Then** no HTTP/HTTPS requests are made
**And** no DNS lookups are performed
**And** all files are sourced from the offline bundle
**And** network absence does not cause failures

**Validation Method:**
- Run installer in network-isolated container
- Monitor network syscalls (strace/dtrace)
- Confirm 0 network calls

### AC#4: Same Features as Online Mode

**Given** an offline installation completes
**When** the installation is validated
**Then** all features available in online mode are functional:
- Core framework
- CLI tools
- Templates
- Examples
**And** no functionality is degraded or missing
**And** version matches online installation

### AC#5: Bundle Metadata Display

**Given** an offline bundle exists
**When** the installer runs `python -m installer bundle-info devforgeai-offline.tar.gz`
**Then** bundle metadata is displayed:
```
DevForgeAI Offline Bundle
Version: 1.0.0
Created: 2025-01-06 12:00:00 UTC
Size: 45.2 MB (compressed), 120 MB (uncompressed)
Components:
  - core (required)
  - cli
  - templates
  - examples
Files: 1,234
Checksum: SHA256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```
**And** bundle integrity is checked
**And** expired bundles show warning (if TTL specified)

### AC#6: Incremental Bundle Updates (Optional)

**Given** a base offline bundle exists
**And** a newer version is available
**When** an incremental bundle is created with `--incremental --base v1.0.0`
**Then** only changed/new files are included
**And** delta bundle size is smaller than full bundle
**And** installer can apply delta to existing installation
**And** rollback to base version is possible

### AC#7: Bundle Transfer Verification

**Given** an offline bundle is transferred via USB/CD/network share
**When** the bundle is verified with `python -m installer verify devforgeai-offline.tar.gz`
**Then** the bundle checksum is computed and compared to manifest
**And** verification status is displayed (VALID/CORRUPTED)
**And** corrupted bundles show which files are affected
**And** verification takes <10 seconds for typical bundle

### AC#8: Air-Gapped Installation Workflow

**Given** a user in an air-gapped environment
**When** the complete offline workflow is executed:
1. Create bundle on internet-connected machine
2. Transfer bundle to air-gapped machine
3. Verify bundle integrity
4. Install from bundle
**Then** each step completes successfully without internet
**And** installation time is comparable to online mode (<5 minutes)
**And** user documentation is included in bundle

## AC Verification Checklist

### AC#1 Verification (Bundle Creation)
- [ ] Bundle contains all required files
- [ ] Checksum manifest generated
- [ ] Bundle compressed efficiently
- [ ] Installation script included

### AC#2 Verification (Integrity)
- [ ] SHA256 verification works
- [ ] Corrupted files detected
- [ ] Error code 5 on failure
- [ ] Validation log detailed

### AC#3 Verification (No Network)
- [ ] No HTTP/HTTPS calls
- [ ] No DNS lookups
- [ ] Container isolation test passes
- [ ] Network syscalls = 0

### AC#4 Verification (Feature Parity)
- [ ] Core framework functional
- [ ] CLI tools work
- [ ] Templates available
- [ ] Examples accessible

### AC#5 Verification (Metadata)
- [ ] bundle-info displays correctly
- [ ] All metadata fields present
- [ ] Integrity check included
- [ ] Expired bundle warning (if TTL)

### AC#6 Verification (Incremental)
- [ ] Delta bundle created
- [ ] Size smaller than full
- [ ] Delta application works
- [ ] Rollback functional

### AC#7 Verification (Transfer)
- [ ] Verification command works
- [ ] VALID/CORRUPTED status correct
- [ ] Affected files listed
- [ ] Performance <10 seconds

### AC#8 Verification (Workflow)
- [ ] Create → Transfer → Verify → Install
- [ ] No internet required
- [ ] Installation time <5 minutes
- [ ] Documentation in bundle

## Technical Specification

### Architecture

**Components:**
- `installer/offline.py` - Offline installation logic
- `installer/bundler.py` - Bundle creation
- `installer/verifier.py` - Integrity verification

**Dependencies:**
- `installer/silent.py` (STORY-249) - Reuse silent mode logic
- `hashlib` (stdlib) - SHA256 hashing
- `tarfile` (stdlib) - Bundle compression

### Bundle Structure

```
devforgeai-offline.tar.gz
├── manifest.yaml           # Checksum manifest
├── metadata.json           # Bundle metadata
├── install.py              # Installation script
├── installer/              # Installer modules
│   ├── offline.py
│   ├── platform_detector.py
│   ├── preflight.py
│   └── exit_codes.py
├── payload/                # Framework files
│   ├── .claude/
│   ├── devforgeai/
│   └── ...
└── docs/
    └── OFFLINE_INSTALL.md  # User documentation
```

### Bundler Implementation

```python
class OfflineBundler:
    def __init__(self, source_dir: Path, output: Path):
        self.source_dir = source_dir
        self.output = output
        self.manifest = {}

    def create_bundle(self) -> None:
        """Create offline bundle"""
        files = self._collect_files()
        self._compute_checksums(files)
        self._create_tarball(files)
        self._write_manifest()

    def _compute_checksums(self, files: List[Path]) -> None:
        """Compute SHA256 for each file"""
        for file in files:
            with open(file, 'rb') as f:
                sha256 = hashlib.sha256(f.read()).hexdigest()
            self.manifest[str(file)] = {
                'sha256': sha256,
                'size': file.stat().st_size
            }

    def _create_tarball(self, files: List[Path]) -> None:
        """Create compressed tarball"""
        with tarfile.open(self.output, 'w:gz') as tar:
            for file in files:
                tar.add(file, arcname=file.relative_to(self.source_dir))
```

### Verification Implementation

```python
class BundleVerifier:
    def __init__(self, bundle_path: Path):
        self.bundle_path = bundle_path
        self.manifest = None

    def verify(self) -> VerificationResult:
        """Verify bundle integrity"""
        with tarfile.open(self.bundle_path, 'r:gz') as tar:
            manifest_file = tar.extractfile('manifest.yaml')
            self.manifest = yaml.safe_load(manifest_file)

            results = []
            for member in tar.getmembers():
                if member.isfile():
                    file_data = tar.extractfile(member).read()
                    actual_hash = hashlib.sha256(file_data).hexdigest()
                    expected_hash = self.manifest[member.name]['sha256']
                    results.append({
                        'file': member.name,
                        'valid': actual_hash == expected_hash
                    })

        return VerificationResult(results)
```

### Offline Installation Flow

```python
class OfflineInstaller:
    def __init__(self, bundle_path: Path, target: Path):
        self.bundle_path = bundle_path
        self.target = target

    def install(self) -> int:
        """Install from offline bundle"""
        try:
            # Step 1: Verify bundle integrity
            verifier = BundleVerifier(self.bundle_path)
            result = verifier.verify()
            if not result.is_valid():
                logger.error("Bundle verification failed")
                return ExitCode.BUNDLE_CORRUPTED

            # Step 2: Extract bundle
            self._extract_bundle()

            # Step 3: Run preflight checks (no network)
            self._run_preflight()

            # Step 4: Install components
            self._install_components()

            # Step 5: Validate installation
            self._validate()

            return ExitCode.SUCCESS

        except Exception as e:
            logger.error(f"Offline installation failed: {e}")
            return ExitCode.INSTALL_ERROR
```

### Network Isolation Testing

**Docker Test Container:**
```dockerfile
FROM python:3.10
COPY devforgeai-offline.tar.gz /tmp/
RUN pip install --no-index --find-links /tmp/ pyyaml
CMD ["python", "-m", "installer", "install", "/opt/devforgeai", "--offline", "--bundle", "/tmp/devforgeai-offline.tar.gz"]
```

**Run with network disabled:**
```bash
docker run --network none offline-installer-test
```

## Implementation Notes

### Dependencies
- **STORY-249 (Silent Installer):** Offline mode uses silent installation logic
- **tarfile:** Python stdlib for tar.gz creation
- **hashlib:** Python stdlib for SHA256 checksums

### Technology Constraints
- **No External Dependencies:** Bundle must be self-contained
- **Compression:** Use gzip level 6 (balance speed/size)
- **File Permissions:** Preserve Unix permissions in bundle

### Security Considerations
- **Bundle Signing:** Consider GPG signing for authenticity (future)
- **Checksum Algorithm:** SHA256 (secure, fast)
- **Transfer Security:** User responsible for secure transfer channel

## Definition of Done

- [ ] All acceptance criteria verified and passing
- [ ] Bundle creation works
- [ ] Bundle verification works
- [ ] No network calls during offline install
- [ ] Feature parity with online mode
- [ ] Incremental bundles functional (optional)
- [ ] Air-gapped workflow tested
- [ ] Documentation included in bundle

## Notes

- Offline mode is critical for government/military/enterprise air-gapped networks
- Bundle size optimization is important for USB transfer
- Consider checksum verification progress bar for large bundles
- Future: Support for cryptographic bundle signing

## Change Log

**Current Status:** Backlog

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2025-01-06 | claude/batch-creation | Story Creation | Initial story created from EPIC-039 Feature 4 | STORY-250-offline-installation-mode.story.md |
| 2025-01-06 | claude/normalization | Template Update | Normalized to format_version 2.5 | STORY-250-offline-installation-mode.story.md |

---

**Template Version:** 2.5
**Created:** 2025-01-06 by /create-missing-stories (batch mode)
