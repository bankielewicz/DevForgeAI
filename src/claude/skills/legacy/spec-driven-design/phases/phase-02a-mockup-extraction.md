# Phase 02a: Mockup Extraction (Extract Mode Only)

**Purpose:** Read existing mockup code (React, Vue, HTML, WPF, etc.) and extract a complete UI Design Source of Truth (design.md) by analyzing the code structure.

**Entry Gate:** MODE == "extract" AND EXTRACT_PATH is set AND validated in Phase 00.

**Skip Condition:** This phase ONLY executes when MODE == "extract". For "story" or "standalone" modes, skip entirely and proceed to Phase 02 (Story Analysis) or Phase 03 (Interactive Discovery).

---

## Reference Loading [MANDATORY]

```
Read(file_path=".claude/skills/spec-driven-design/references/design-source-of-truth-population.md")
Read(file_path=".claude/skills/spec-driven-design/references/design-source-of-truth-schema.md")
```

IF any Read fails: HALT -- "Phase 02a reference files not loaded."

---

## Step 2a.1: Load Extraction References

**EXECUTE:**
```
Read(file_path=".claude/skills/spec-driven-design/references/design-source-of-truth-population.md")
```

Also load:
```
Read(file_path=".claude/skills/spec-driven-design/references/design-source-of-truth-schema.md")
Read(file_path=".claude/skills/spec-driven-design/assets/templates/design-source-of-truth-template.md")
```

**VERIFY:**
- Population reference loaded (contains "Extraction Pipeline")
- Schema reference loaded (contains "Section Schema Definitions")
- Template loaded (contains "UI Design Source of Truth")

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} ${WORKFLOW_FLAG} --phase=02a --step=2a.1 --project-root=. 2>&1")
```

---

## Step 2a.2: Discover and Classify Source Files

**EXECUTE:**
```
# Discover all UI-relevant files at the extract path
component_files = Glob(pattern="${EXTRACT_PATH}/**/*.{jsx,tsx,vue}")
style_files = Glob(pattern="${EXTRACT_PATH}/**/*.{css,scss,less,module.css}")
config_files = Glob(pattern="${EXTRACT_PATH}/**/tailwind.config.*")
config_files += Glob(pattern="${EXTRACT_PATH}/**/package.json")
config_files += Glob(pattern="${EXTRACT_PATH}/**/theme.*")
markup_files = Glob(pattern="${EXTRACT_PATH}/**/*.{html,htm}")
xaml_files = Glob(pattern="${EXTRACT_PATH}/**/*.xaml")
python_files = Glob(pattern="${EXTRACT_PATH}/**/*.py")
```

Classify the project type:
- Has .jsx/.tsx files → React project
- Has .vue files → Vue project
- Has .html files (no .jsx/.vue) → Vanilla HTML project
- Has .xaml files → WPF project
- Has .py files with tkinter/curses imports → Python GUI/TUI project

Set `MOCKUP_FRAMEWORK` based on classification.

Present discovery to user:
```
AskUserQuestion:
  Question: "Found ${N} source files at ${EXTRACT_PATH}. Detected framework: ${MOCKUP_FRAMEWORK}. Is this correct?"
  Header: "Source Files"
  Options:
    - label: "Correct"
      description: "Proceed with extraction using detected framework"
    - label: "Different framework"
      description: "Let me specify the correct framework"
    - label: "Wrong path"
      description: "The path needs correction"
```

**VERIFY:**
- At least 1 source file discovered
- User confirmed framework detection (or provided correction)

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} ${WORKFLOW_FLAG} --phase=02a --step=2a.2 --project-root=. 2>&1")
```

---

## Step 2a.2.5: Cluster Partitioning

**EXECUTE:** Partition the discovered source files into clusters for per-cluster mockup-extractor invocations.

```
# Component files (jsx, tsx, vue, html, xaml, py) → clusters of at most 15 files each
CLUSTERS = []
component_files = [all jsx/tsx/vue/html/xaml/py files discovered in Step 2a.2]
config_and_style_files = [tailwind.config.*, *.css, *.scss, package.json, theme.* files]

# Split component files into clusters of at most 15
for i in range(0, len(component_files), 15):
    CLUSTERS.append({
        "component_files": component_files[i:i+15],
        "shared_files": config_and_style_files  # included in every cluster for token context
    })

Display: f"Partitioned {len(component_files)} component files into {len(CLUSTERS)} cluster(s) (max 15 files each). Will invoke mockup-extractor × {len(CLUSTERS)}."
```

**VERIFY:**
- `len(CLUSTERS) >= 1`
- No cluster has more than 15 component files

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} ${WORKFLOW_FLAG} --phase=02a --step=2a.2.5 --project-root=. 2>&1")
```

---

## Steps 2a.3 - 2a.5: Per-Cluster Delegated Extraction (mockup-extractor terminal subagent)

**EXECUTE:** Invoke `mockup-extractor` once per cluster (from Step 2a.2.5). Each call receives only its cluster's files, keeping the invocation under the <30K token budget. The subagent returns a `cluster_fragment` (tokens, components, flows, animations) — NOT a full design.md. The orchestrator merges all fragments after the loop.

> **Overflow recovery:** If a cluster result is truncated (missing or empty `cluster_fragment` field) or returns "Prompt is too long", apply `.claude/rules/workflow/subagent-prompt-overflow.md` Recovery Workflow (Case B or Case A respectively) before proceeding.

```python
cluster_results = []
for cluster_index, cluster in enumerate(CLUSTERS):
    result_k = Task(subagent_type="mockup-extractor", prompt=f"""
      FILE_CLUSTER: {cluster["component_files"] + cluster["shared_files"]}
      FRAMEWORK: ${MOCKUP_FRAMEWORK}
      UI_TYPE: ${UI_TYPE}
      NORMALIZATION_THRESHOLD_PCT: 70

      Execute Steps 2a.3 + 2a.4 + 2a.4.5 + 2a.5 for FILE_CLUSTER only.
      Return cluster_fragment JSON envelope per your contract. Do NOT render design.md.
    """)

    IF result_k.status == "failed":
        HALT — surface error via AskUserQuestion (retry cluster or abandon)
    IF result_k.status == "needs_correction":
        HALT — surface gate failure; offer re-extraction or hybrid mode
    IF NOT result_k.cluster_fragment OR result_k.cluster_fragment is empty:
        # Truncated return — Case B overflow
        Apply subagent-prompt-overflow.md Recovery Workflow (Case B) for this cluster

    cluster_results.append(result_k)
    Display: f"Cluster {cluster_index + 1}/{len(CLUSTERS)} complete: {len(result_k.cluster_fragment.components)} components, {len(result_k.cluster_fragment.tokens)} tokens"
```

### Step 2a.3: Design Token Extraction (aggregated from clusters)

**EXECUTE:** Merge `cluster_fragment.tokens` from all cluster_results into a unified token inventory. Deduplicate by token name.
```
tokens_inventory = {}
for r in cluster_results:
    for token in r.cluster_fragment.tokens:
        tokens_inventory[token.name] = token  # last-write wins for duplicates

Display: f"Tokens aggregated: {len(tokens_inventory)} unique tokens across {len(CLUSTERS)} cluster(s)"
Display: "  Colors: ${count by category}"
Display: "  Spacing: ${count by category}"
Display: "  Typography: ${count by category}"
```

**VERIFY:**
- `len(tokens_inventory) >= 1`
- Token categories dict populated
- All cluster_results have "2a.3" in extraction_steps_completed

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} ${WORKFLOW_FLAG} --phase=02a --step=2a.3 --project-root=. 2>&1")
```

---

### Step 2a.4: Component Hierarchy Extraction (aggregated from clusters)

**EXECUTE:** Merge all `cluster_fragment.components` from cluster_results. Re-assign globally-unique COMP-NNN IDs (sorted by cluster order, then per-cluster component order). Enforce props_completeness + children_integrity gates on the merged inventory.
```
all_components = []
comp_counter = 1
for r in cluster_results:
    for comp in r.cluster_fragment.components:
        comp.id = f"COMP-{comp_counter:03d}"
        all_components.append(comp)
        comp_counter += 1

Display: f"Components aggregated: {len(all_components)} total (COMP-001 .. COMP-{len(all_components):03d})"

IF any component has incomplete props list:
    HALT: "Props completeness gate failed on merged inventory."
IF any component references a COMP-NNN not in all_components:
    HALT: "Children integrity gate failed — dangling reference in merged inventory."
```

**VERIFY:**
- len(all_components) >= 1
- props_completeness gate passed on merged inventory
- children_integrity gate passed on merged inventory
- All cluster_results have "2a.4" in extraction_steps_completed

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} ${WORKFLOW_FLAG} --phase=02a --step=2a.4 --project-root=. 2>&1")
```

---

### Step 2a.4.5: Token Normalization Pass (aggregated from clusters)

**EXECUTE:** Aggregate per-cluster normalization metrics into a merged-inventory normalization pct + hard gate check (RESEARCH-003 R2 — 14.4% structural-fidelity gain per arxiv.org/html/2509.07334v1). Compute the aggregate as the weighted mean of each cluster's `cluster_fragment.token_normalization_pct` (weighted by tokens per cluster).
```
total_tokens = sum(len(r.cluster_fragment.tokens) for r in cluster_results)
aggregate_normalization_pct = (
    sum(r.cluster_fragment.token_normalization_pct * len(r.cluster_fragment.tokens) for r in cluster_results)
    / total_tokens
) if total_tokens else 0

Display: f"Token normalization (aggregate): {aggregate_normalization_pct}% (threshold: 70%)"

IF aggregate_normalization_pct < 70:
    HALT: "Token normalization below 70% threshold ({aggregate_normalization_pct}%) on merged inventory. CRITICAL quality gate (RESEARCH-003 R2). Re-extract affected cluster(s) with hybrid mode."
```

**VERIFY:**
- aggregate_normalization_pct >= 70 (or configured threshold)
- aggregate normalization gate passed on merged inventory
- All cluster_results have "2a.4.5" in extraction_steps_completed

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} ${WORKFLOW_FLAG} --phase=02a --step=2a.4.5 --project-root=. 2>&1")
```

---

### Step 2a.5: Interactions and Animations (aggregated from clusters)

**EXECUTE:** Merge all `cluster_fragment.flows` and `cluster_fragment.animations` from cluster_results. Re-assign globally-unique FLOW-NNN / ANIM-NNN IDs (sorted by cluster order). Enforce the interaction completeness gate on the merged inventory.
```
all_flows = []
all_animations = []
flow_counter = 1
anim_counter = 1
for r in cluster_results:
    for flow in r.cluster_fragment.flows:
        flow.id = f"FLOW-{flow_counter:03d}"
        all_flows.append(flow)
        flow_counter += 1
    for anim in r.cluster_fragment.animations:
        anim.id = f"ANIM-{anim_counter:03d}"
        all_animations.append(anim)
        anim_counter += 1

Display: f"Flows aggregated: {len(all_flows)} (FLOW-001 .. FLOW-{len(all_flows):03d})"
Display: f"Animations aggregated: {len(all_animations)} (ANIM-001 .. ANIM-{len(all_animations):03d})"

IF any component with a handler is not represented in all_flows:
    HALT: "Interaction completeness gate failed — components with handlers not represented in merged FLOW inventory."
```

**VERIFY:**
- len(all_flows) >= 1 (most mockups have at least one interaction)
- interaction completeness gate passed on merged inventory
- All cluster_results have "2a.5" in extraction_steps_completed

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} ${WORKFLOW_FLAG} --phase=02a --step=2a.5 --project-root=. 2>&1")
```

---

<!-- Step 2a.4 (Component Hierarchy Extraction) — AGGREGATED from per-cluster mockup-extractor fragments. See "Steps 2a.3 - 2a.5: Per-Cluster Delegated Extraction" section above. Per-step Display+VERIFY+RECORD lives under "### Step 2a.4:" subsection within the aggregation block. -->

<!-- Step 2a.4.5 (Token Normalization Pass — RESEARCH-003 R2 hard gate) — AGGREGATED from per-cluster mockup-extractor fragments. See "Steps 2a.3 - 2a.5: Per-Cluster Delegated Extraction" section above. Per-step Display+VERIFY+RECORD lives under "### Step 2a.4.5:" subsection within the aggregation block. -->

<!-- Step 2a.5 (Interactions + Animations Extraction) — AGGREGATED from per-cluster mockup-extractor fragments. See "Steps 2a.3 - 2a.5: Per-Cluster Delegated Extraction" section above. Per-step Display+VERIFY+RECORD lives under "### Step 2a.5:" subsection within the aggregation block. -->

## Step 2a.6: User Validation Gate

**EXECUTE:**

Present extraction summary to user for validation:
```
AskUserQuestion:
  Question: "Extraction complete. Here's what I found:"
  Header: "Validation"
  Options:
    - label: "Looks correct, generate design.md"
      description: "${N} components, ${N} tokens, ${N} interactions, ${N} animations extracted. Generate the Design Source of Truth."
    - label: "Needs corrections"
      description: "Let me review and correct specific details before generating"
    - label: "Cancel extraction"
      description: "Stop this invocation without pretending the standalone route completed"
```

IF "Needs corrections":
  - Ask specific questions about gaps or inaccuracies
  - Update extracted data with user corrections
  - This creates a "hybrid" source_mode

IF "Cancel extraction":
  - HALT this invocation with its ledger and phase state unfinished.
  - Explain that standalone discovery requires a new provider session and a new
    explicit `/create-design --standalone` invocation.

**VERIFY:**
- User has validated or corrected extraction results; cancellation does not satisfy this gate

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} ${WORKFLOW_FLAG} --phase=02a --step=2a.6 --project-root=. 2>&1")
```

---

## Step 2a.7: Design Source of Truth Generation (orchestrator-owned)

**EXECUTE:** The orchestrator renders the design.md template from the merged inventory (tokens_inventory, all_components, all_flows, all_animations). The mockup-extractor no longer performs this step. The orchestrator then writes design.md to disk and runs validation (orchestrator owns Write permission + validation feedback loop).

If user chose "Needs corrections" in Step 2a.6, the source_mode is "hybrid" — apply the user-corrected fields to the merged inventory (tokens_inventory / all_components / all_flows / all_animations) before rendering.

```
Read(file_path=".claude/skills/spec-driven-design/assets/templates/design-source-of-truth-template.md")

state.design_md_content = populate_template(
    tokens=tokens_inventory,
    components=all_components,
    flows=all_flows,
    animations=all_animations,
    metadata={
        "framework": MOCKUP_FRAMEWORK,
        "ui_type": UI_TYPE,
        "source_mode": "extracted",
        "components_count": len(all_components),
        "tokens_count": len(tokens_inventory),
        "flows_count": len(all_flows),
        "animations_count": len(all_animations)
    }
)

Display: f"design.md rendered: {len(state.design_md_content)} characters, {len(all_components)} components"

# Confirm we have rendered content before Writing
IF state.design_md_content is empty or null:
    HALT: "Template population produced empty design.md. Cannot Write. Check merged inventory."

# Write design.md to disk (orchestrator owns this)
Write(file_path="devforgeai/specs/ui/design.md", content=${state.design_md_content})

# Run validation script (hard enforcement — deterministic pass/fail)
validation_result = Bash(command="python3 src/claude/skills/spec-driven-design/scripts/validate_design_md.py devforgeai/specs/ui/design.md --expected-components=${len(all_components)} 2>&1")

IF validation_result.exit_code != 0:
    Display: "design.md validation failed (exit ${validation_result.exit_code}):"
    Display: validation_result.stdout
    AskUserQuestion:
      Question: "design.md validation failed. Re-extract or accept the issues?"
      Options:
        - label: "Re-invoke mockup-extractor (re-cluster) with fixes"
        - label: "Accept warnings and continue"
        - label: "Abandon extraction"
```

**VERIFY:**
- `state.design_md_content` is a non-empty string
- Contains all COMP-NNN IDs from `all_components`
- File exists at devforgeai/specs/ui/design.md
- Validation script exits with code 0 (all hard checks pass), OR user explicitly accepted warnings

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} ${WORKFLOW_FLAG} --phase=02a --step=2a.7 --project-root=. 2>&1")
```

---

## Step 2a.7.5: Auto-Serve Mockup for Screenshot Capture (when --url not provided)

**Skip Condition:** IF EXTRACT_URL is already set (user provided --url), skip this step entirely.

**EXECUTE:**
```
IF EXTRACT_URL is null:
  # design.md has been generated. Offer to capture screenshots via local server.

  # Detect serve strategy from MOCKUP_FRAMEWORK (set in Step 2a.2)
  package_json = Glob(pattern="${EXTRACT_PATH}/package.json")

  IF package_json found:
    Read(file_path=package_json[0])
    # Extract "scripts" field from package.json content

    IF scripts contains "dev" key:
      serve_command = "npm run dev"
      serve_label = "npm run dev (project's dev server)"
    ELIF scripts contains "start" key:
      serve_command = "npm start"
      serve_label = "npm start (project's start script)"
    ELSE:
      serve_command = "npx serve ${EXTRACT_PATH}"
      serve_label = "npx serve (static file server)"

    # Detect expected port from framework dependencies
    IF package.json dependencies or devDependencies contains "next":
      expected_port = 3000
    ELIF package.json dependencies contains "vite" or "@vitejs":
      expected_port = 5173
    ELIF package.json dependencies contains "@angular/core":
      expected_port = 4200
    ELSE:
      expected_port = 3000

    # Check if node_modules exists (need npm install?)
    node_modules = Glob(pattern="${EXTRACT_PATH}/node_modules/.package-lock.json")
    needs_install = (len(node_modules) == 0)

  ELSE:
    # No package.json — vanilla HTML/CSS/JS
    serve_command = "npx serve ${EXTRACT_PATH}"
    serve_label = "npx serve (static file server)"
    expected_port = 3000
    needs_install = false

  # Ask user — MUST use AskUserQuestion tool
  AskUserQuestion(
    questions: [{
      question: "No --url provided. Want me to start a local server to capture screenshots? Detected: '${serve_label}' on port ${expected_port}.",
      header: "Screenshots",
      multiSelect: false,
      options: [
        { label: "Yes, auto-serve (Recommended)", description: "Run '${serve_label}' on port ${expected_port}, capture 3 viewport screenshots via Playwright, then stop the server automatically" },
        { label: "Skip screenshots", description: "Continue without visual capture — design.md is already generated and complete" },
        { label: "I'll provide a URL", description: "I'll start the server manually and give you the URL to capture from" }
      ]
    }]
  )

  IF response == "Yes, auto-serve":
    # Install dependencies if needed (framework projects only)
    IF needs_install:
      Display: "Installing dependencies (npm install)..."
      Bash(command="cd ${EXTRACT_PATH} && npm install 2>&1", timeout=120000)

    # Start server in background
    Display: "Starting server: ${serve_command} on port ${expected_port}..."
    Bash(command="cd ${EXTRACT_PATH} && ${serve_command}", run_in_background=true)

    # Wait for server to be ready (poll for up to 30 seconds)
    server_ready = false
    FOR attempt in 1..15:
      Bash(command="sleep 2")
      # Check if port is listening
      port_check = Bash(command="ss -tlnp 2>/dev/null | grep :${expected_port} || lsof -i :${expected_port} 2>/dev/null || echo 'not ready'")
      IF port_check does NOT contain "not ready":
        server_ready = true
        BREAK

    IF server_ready:
      EXTRACT_URL = "http://localhost:${expected_port}"
      session.url_validation = true
      session.auto_served = true
      session.auto_serve_port = expected_port
      Display: "Server ready at ${EXTRACT_URL}"
      Display: "Proceeding to Playwright screenshot capture..."
      # Step 2a.8 will now execute with EXTRACT_URL set
    ELSE:
      Display: "WARNING: Server did not respond on port ${expected_port} within 30 seconds."
      Display: "Try starting it manually, then re-run with: --url=http://localhost:${expected_port}"
      session.auto_served = false

  ELIF response == "Skip screenshots":
    Display: "Skipping visual capture. design.md is the source of truth."
    session.auto_served = false

  ELIF response == "I'll provide a URL":
    AskUserQuestion(
      questions: [{
        question: "Enter the URL where the mockup is running:",
        header: "URL",
        multiSelect: false,
        options: [
          { label: "http://localhost:3000", description: "Common default for Next.js, CRA, Express" },
          { label: "http://localhost:5173", description: "Common default for Vite (Vue, Svelte, React+Vite)" },
          { label: "http://localhost:4200", description: "Common default for Angular CLI" }
        ]
      }]
    )
    EXTRACT_URL = user's response (selected option or "Other" free text)
    session.url_validation = true
    session.auto_served = false
```

**VERIFY:**
- IF user chose auto-serve: server_ready == true AND EXTRACT_URL is set
- IF user chose skip: session.auto_served == false
- IF user provided URL: EXTRACT_URL is set

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} ${WORKFLOW_FLAG} --phase=02a --step=2a.7.5 --project-root=. 2>&1")
```

---

## Step 2a.8: URL Visual Capture (when EXTRACT_URL is set — via --url OR auto-serve)

**Skip Condition:** IF EXTRACT_URL is null, skip this step entirely.

**EXECUTE:**
```
IF EXTRACT_URL is not null:
  # Create visual capture directory
  Bash(command="mkdir -p devforgeai/specs/ui/visual-capture")

  # Generate Playwright capture script
  Write(file_path="tmp/visual-capture.js", content="""
  const { chromium } = require('playwright');
  const fs = require('fs');
  const path = require('path');

  const URL = '${EXTRACT_URL}';
  const OUT = 'devforgeai/specs/ui/visual-capture';

  (async () => {
    const browser = await chromium.launch({ headless: true });
    const page = await browser.newPage();

    // Desktop screenshot (1280x800)
    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto(URL, { waitUntil: 'networkidle', timeout: 30000 });
    await page.screenshot({ path: path.join(OUT, 'desktop.png'), fullPage: true });
    console.log('Desktop screenshot captured');

    // Extract computed CSS custom properties
    const computedTokens = await page.evaluate(() => {
      const root = getComputedStyle(document.documentElement);
      const tokens = {};
      try {
        for (const sheet of document.styleSheets) {
          try {
            for (const rule of sheet.cssRules) {
              if (rule.selectorText === ':root') {
                for (const prop of rule.style) {
                  if (prop.startsWith('--')) {
                    tokens[prop] = root.getPropertyValue(prop).trim();
                  }
                }
              }
            }
          } catch (e) { /* cross-origin stylesheet, skip */ }
        }
      } catch (e) { /* no stylesheets, skip */ }
      return tokens;
    });
    fs.writeFileSync(path.join(OUT, 'computed-tokens.json'), JSON.stringify(computedTokens, null, 2));
    console.log('Computed tokens extracted: ' + Object.keys(computedTokens).length + ' properties');

    // Tablet screenshot (768x1024)
    await page.setViewportSize({ width: 768, height: 1024 });
    await page.waitForTimeout(500);
    await page.screenshot({ path: path.join(OUT, 'tablet.png'), fullPage: true });
    console.log('Tablet screenshot captured');

    // Mobile screenshot (375x812)
    await page.setViewportSize({ width: 375, height: 812 });
    await page.waitForTimeout(500);
    await page.screenshot({ path: path.join(OUT, 'mobile.png'), fullPage: true });
    console.log('Mobile screenshot captured');

    // Extract simplified DOM structure (depth 4)
    const domStructure = await page.evaluate(() => {
      function simplify(el, depth) {
        if (depth > 4 || !el) return null;
        const children = [...(el.children || [])].map(c => simplify(c, depth + 1)).filter(Boolean);
        return {
          tag: el.tagName ? el.tagName.toLowerCase() : undefined,
          id: el.id || undefined,
          classes: el.className && typeof el.className === 'string' ? el.className.split(' ').filter(c => c).slice(0, 5) : undefined,
          childCount: el.children ? el.children.length : 0,
          children: children.length > 0 ? children : undefined
        };
      }
      return simplify(document.body, 0);
    });
    fs.writeFileSync(path.join(OUT, 'dom-structure.json'), JSON.stringify(domStructure, null, 2));
    console.log('DOM structure extracted');

    // Discover same-origin links
    const links = await page.evaluate(() => {
      return [...new Set(
        [...document.querySelectorAll('a[href]')]
          .map(a => a.href)
          .filter(h => h.startsWith(location.origin) && !h.includes('#'))
      )];
    });
    fs.writeFileSync(path.join(OUT, 'discovered-links.json'), JSON.stringify(links, null, 2));
    console.log('Discovered ' + links.length + ' same-origin links');

    await browser.close();
    console.log('Visual capture complete');
  })().catch(err => {
    console.error('Capture failed:', err.message);
    process.exit(1);
  });
  """)

  # Execute Playwright capture
  Bash(command="npx playwright install chromium 2>&1", timeout=120000)
  capture_result = Bash(command="node tmp/visual-capture.js 2>&1", timeout=60000)

  IF capture_result exit code != 0:
    Display: "WARNING: Playwright capture failed: ${capture_result}"
    Display: ""
    Display: "Fallback options:"
    Display: "  1. Claude Chrome Extension: Run 'claude --chrome' and navigate to ${EXTRACT_URL}"
    Display: "  2. Manual screenshots: Save screenshots to devforgeai/specs/ui/visual-capture/"
    Display: ""
    Display: "Continuing without visual capture..."
    session.url_validation = false

  ELSE:
    Display: "Visual capture complete:"
    Display: "  Screenshots: desktop.png, tablet.png, mobile.png"
    Display: "  Computed tokens: computed-tokens.json"
    Display: "  DOM structure: dom-structure.json"
    Display: "  Discovered links: discovered-links.json"
```

**VERIFY:**
```
IF EXTRACT_URL was provided AND capture succeeded:
  Glob(pattern="devforgeai/specs/ui/visual-capture/desktop.png")
  Glob(pattern="devforgeai/specs/ui/visual-capture/computed-tokens.json")
  Assert: Both files exist
```

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} ${WORKFLOW_FLAG} --phase=02a --step=2a.8 --project-root=. 2>&1")
```

---

## Step 2a.9: Visual Cross-Validation (Optional — only when visual-capture exists)

**Skip Condition:** IF visual-capture/ directory does not exist, skip entirely.

**EXECUTE:**
```
visual_exists = Glob(pattern="devforgeai/specs/ui/visual-capture/desktop.png")

IF visual_exists:
  # 1. Token comparison: computed-tokens.json vs design.md Section 2
  Read(file_path="devforgeai/specs/ui/visual-capture/computed-tokens.json")

  token_matches = 0
  token_drifts = 0
  drift_details = []

  FOR each css_var, computed_value in computed_tokens:
    Find matching token in design.md Section 2 (by css_var name)
    IF found AND design.md value matches computed_value:
      token_matches += 1
    ELIF found AND design.md value != computed_value:
      token_drifts += 1
      drift_details.append("${css_var}: design.md='${design_value}' browser='${computed_value}'")

  Display: "Token Cross-Validation:"
  Display: "  Matches: ${token_matches}"
  Display: "  Drifts: ${token_drifts}"
  IF token_drifts > 0:
    Display: "  Drift details:"
    FOR each drift in drift_details[:10]:
      Display: "    - ${drift}"

  # 2. Visual inspection: Read desktop screenshot (Claude multimodal)
  Read(file_path="devforgeai/specs/ui/visual-capture/desktop.png")
  # Claude analyzes the screenshot and compares against design.md:
  # - Does the layout match LAYOUT-001 ASCII diagram?
  # - Is the brand color (#00d4aa) visible?
  # - Does the glassmorphism aesthetic match design_intent?
  # - Are the major components (topbar, sidebar, main content) visible?
  Display: "Visual inspection: [Claude provides assessment based on screenshot analysis]"

  # 3. Summary
  Display: ""
  Display: "Visual Cross-Validation Summary:"
  Display: "  Screenshots: 3 (desktop, tablet, mobile)"
  Display: "  Token comparison: ${token_matches} matches, ${token_drifts} drifts"
  Display: "  Visual fidelity: [assessment]"
  Display: "  Artifacts: devforgeai/specs/ui/visual-capture/"

ELSE:
  Display: "No visual capture available. Skipping cross-validation."
```

**VERIFY:**
- IF visual capture exists: Token comparison report generated
- IF visual capture exists: Desktop screenshot read and assessed

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} ${WORKFLOW_FLAG} --phase=02a --step=2a.9 --project-root=. 2>&1")
```

---

## Phase 02a Completion

**EXECUTE:**

```
# Clean up auto-served server (if we started one in Step 2a.7.5)
IF session.auto_served == true:
  Bash(command="lsof -ti:${session.auto_serve_port} | xargs kill 2>/dev/null || fuser -k ${session.auto_serve_port}/tcp 2>/dev/null || true")
  Display: "Auto-served server stopped (port ${session.auto_serve_port})"
```

```
Bash(command="devforgeai-validate validate-design-phase ${IDENTIFIER} ${WORKFLOW_FLAG} --mode=${MODE} --phase=02a --project-root=. 2>&1")
Bash(command="devforgeai-validate phase-complete ${IDENTIFIER} ${WORKFLOW_FLAG} --phase=02a --project-root=. 2>&1")
```

**VERIFY:**
- Exit code 0; any non-zero result blocks completion
- IF session.auto_served was true: server process is no longer listening on the port

**Extract Mode Flow After Phase 02a:**
- Skip Phase 02 (Story Analysis — no story in extract mode)
- Skip Phase 03 (Interactive Discovery — data already extracted)
- Skip Phase 04 (Template Loading — not generating from templates)
- Skip Phase 05 (Code Generation — not generating new code, extracting from existing)
- Proceed to Phase 06 (Documentation) — Generate UI-SPEC-SUMMARY.md and finalize design.md
- Proceed to Phase 07 (Validation) — Validate design.md completeness
- Proceed to Phase 08 (Feedback & Completion) — Report results

**NEXT:** Proceed to Phase 06 (Documentation) for extract mode, or Phase 03 (Interactive Discovery) if user chose to switch modes.

## Hook-backed OUT-Attestation

This phase has Phase-D dispatch entries in `subagent_out_attestation_registry.json`. When dispatching those named subagents, instruct them to return a `subagent-result-v1` result that includes `coverage_attestation` in the normal response. Phase completion is blocked by `subagent-out-attestation-gate.sh` when the hook-owned ledger line lacks `coverage_attestation_present:true`. This Phase-D path is OUT-attestation-only and does not require `tmp/<WORK_ID>/handoffs/`.
