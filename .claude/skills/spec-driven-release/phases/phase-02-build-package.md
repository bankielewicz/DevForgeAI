# Phase 02: Build & Package

## Entry Gate

```bash
devforgeai-validate phase-check ${STORY_ID} --workflow=release --from=01 --to=02 --project-root=.
```

## Contract

PURPOSE: Execute build commands for detected technology stack and publish packages to configured registries.
REQUIRED SUBAGENTS: none
REQUIRED ARTIFACTS: BuildResult objects, registry publish status (if configured)
STEP COUNT: 6 mandatory steps

---

## Mandatory Steps

### Step 2.1: Check Build Enabled

EXECUTE: Check if build is enabled. Load build reference regardless (mandatory even for skips).
```
Read(file_path=".claude/skills/spec-driven-release/references/build-commands.md")

IF $BUILD_CONFIG.enabled == false:
    Display: "Phase 02 skipped: Build disabled in build-config.yaml"
    Write(file_path="devforgeai/workflows/.release-phase-02.marker",
          content="phase: 02\nstory_id: ${STORY_ID}\nstatus: skipped\nreason: Build disabled in configuration\ntimestamp: ${ISO_8601}")
    EXIT phase early (proceed to Exit Gate with skip status)

Display: "Build enabled - proceeding with build commands"
```
VERIFY: Either build is enabled (proceed) OR skip marker written and phase exits early.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=release --phase=02 --step=2.1 --project-root=.`

---

### Step 2.2: Execute Build Commands

EXECUTE: Run appropriate build commands for each detected technology stack.
```
FOR each stack in $TECH_STACK_INFO:
    IF stack.stack_type == "nodejs":
        Bash(command="npm run build", timeout=$BUILD_CONFIG.timeout_seconds * 1000)
    ELIF stack.stack_type == "python":
        Bash(command="python -m build", timeout=$BUILD_CONFIG.timeout_seconds * 1000)
    ELIF stack.stack_type == "rust":
        Bash(command="cargo build --release", timeout=$BUILD_CONFIG.timeout_seconds * 1000)
    ELIF stack.stack_type == "dotnet":
        Bash(command="dotnet publish -c Release", timeout=$BUILD_CONFIG.timeout_seconds * 1000)
    ELIF stack.stack_type == "go":
        Bash(command="go build ./...", timeout=$BUILD_CONFIG.timeout_seconds * 1000)
    ELIF stack.stack_type == "java-maven":
        Bash(command="mvn package -DskipTests", timeout=$BUILD_CONFIG.timeout_seconds * 1000)
    ELIF stack.stack_type == "java-gradle":
        Bash(command="gradle build -x test", timeout=$BUILD_CONFIG.timeout_seconds * 1000)

    $BUILD_RESULTS[] = {
        stack_type: stack.stack_type,
        success: (exit_code == 0),
        output_path: stack.output_directory,
        duration_ms: elapsed,
        stdout: captured_stdout,
        stderr: captured_stderr
    }

Display: "Build ${stack.stack_type}: ${success ? 'PASSED' : 'FAILED'} (${duration_ms}ms)"
```
VERIFY: $BUILD_RESULTS array is populated with at least one entry per detected stack.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=release --phase=02 --step=2.2 --project-root=.`

---

### Step 2.3: Validate Build Output

EXECUTE: Verify build artifacts were created successfully.
```
FOR each result in $BUILD_RESULTS:
    IF result.success:
        Glob(pattern="${result.output_path}/*")
        IF artifacts found:
            Display: "[${result.stack_type}] Build artifacts found at ${result.output_path}"
        ELSE:
            Display: "Warning: [${result.stack_type}] Build succeeded but no artifacts at ${result.output_path}"
    ELSE:
        Display: "[${result.stack_type}] Build FAILED"
        Display: "stderr: ${result.stderr}"

failed_builds = BUILD_RESULTS.filter(r => !r.success)

IF failed_builds.length > 0 AND $BUILD_CONFIG.fail_on_build_error == true:
    HALT: "Build failed for: ${failed_builds.map(r => r.stack_type).join(', ')}. Release cannot proceed."
ELIF failed_builds.length > 0:
    Display: "Warning: ${failed_builds.length} build(s) failed but fail_on_build_error=false, continuing"
```
VERIFY: Either all builds succeeded OR failed builds acknowledged (fail_on_build_error=false) OR HALTED.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=release --phase=02 --step=2.3 --project-root=.`

---

### Step 2.4: Check Registry Publishing Config

EXECUTE: Check if registry publishing is configured. Load reference.
```
Read(file_path=".claude/skills/spec-driven-release/references/registry-publishing.md")

Read(file_path="devforgeai/deployment/registry-config.yaml")

IF file not found:
    $REGISTRY_ENABLED = false
    Display: "No registry configuration found - skipping publish steps"
ELSE:
    $REGISTRY_CONFIG = parsed YAML content
    $REGISTRY_ENABLED = true
    $ENABLED_REGISTRIES = registries where enabled=true
    Display: "Registry config loaded: ${ENABLED_REGISTRIES.length} registries enabled"
```
VERIFY: $REGISTRY_ENABLED is set. If true, $REGISTRY_CONFIG and $ENABLED_REGISTRIES are populated.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=release --phase=02 --step=2.4 --project-root=.`

---

### Step 2.5: Publish to Registries

EXECUTE: Publish packages to each enabled registry. Skip if no registries configured.
```
IF $REGISTRY_ENABLED == false:
    Display: "Registry publishing skipped - no config"
    SKIP to Step 2.6

$PUBLISH_RESULTS = []

FOR each registry in $ENABLED_REGISTRIES:
    IF registry.type == "npm":
        Bash(command="npm publish ${registry.flags}")
    ELIF registry.type == "pypi":
        Bash(command="python -m twine upload dist/*")
    ELIF registry.type == "nuget":
        Bash(command="dotnet nuget push **/*.nupkg --source ${registry.source}")
    ELIF registry.type == "docker":
        Bash(command="docker push ${registry.image}")
    ELIF registry.type == "crates":
        Bash(command="cargo publish")

    $PUBLISH_RESULTS[] = {
        registry: registry.type,
        success: (exit_code == 0),
        message: stdout or stderr
    }

    Display: "[${registry.type}] ${success ? 'Published' : 'FAILED'}: ${message}"

failed_publishes = PUBLISH_RESULTS.filter(r => !r.success)

IF failed_publishes.length > 0:
    AskUserQuestion:
        Question: "Registry publish failed for: ${failed_publishes.map(r => r.registry).join(', ')}. Continue to deployment?"
        Header: "Publish"
        Options:
            - label: "Continue with warning"
              description: "Proceed to deployment despite publish failure"
            - label: "Abort release"
              description: "Stop release to fix publishing issues"
        multiSelect: false

    IF user selects abort:
        HALT: "Release aborted - registry publish failed"
```
VERIFY: Either all publishes succeeded OR user acknowledged failures and chose to continue OR publishing was skipped.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=release --phase=02 --step=2.5 --project-root=.`

---

### Step 2.6: Aggregate Build/Publish Results

EXECUTE: Collect and display summary of all build and publish results.
```
build_passed = BUILD_RESULTS.filter(r => r.success).length
build_total = BUILD_RESULTS.length
publish_passed = PUBLISH_RESULTS ? PUBLISH_RESULTS.filter(r => r.success).length : 0
publish_total = PUBLISH_RESULTS ? PUBLISH_RESULTS.length : 0

Display:
"
Build & Package Summary
  Builds: ${build_passed}/${build_total} passed
  Publishes: ${publish_passed}/${publish_total} passed
  Total duration: ${total_duration}ms
"
```
VERIFY: Summary displayed with accurate counts.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=release --phase=02 --step=2.6 --project-root=.`

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${STORY_ID} --workflow=release --phase=02 --checkpoint-passed --project-root=.
```

## Phase 02 Completion Display

```
Phase 02 Complete: Build & Package
  Builds: ${build_passed}/${build_total} passed
  Registry publishes: ${publish_passed}/${publish_total}
  Artifacts ready for deployment
```
