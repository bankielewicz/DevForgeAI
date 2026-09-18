# Claude Design Integration — Operator-Mediated Handoff Bundle Parsing

**Purpose:** Document the integration contract between Anthropic's Claude Design
(research-preview product) and DevForgeAI's `spec-driven-design` skill. Used by
`mockup-extractor` (Phase 02a) and Phase 03 Step 3.0 (fast-path detection).

**Governing decision:** ADR-078 (modernization), ADR-075 (design.md format-stay
with three trigger conditions), **RESEARCH-010** (Claude Design integration
research, 2026-05-20).

**Status:** **DEFENSIVE / DISPOSABLE.** Claude Design's bundle structure is
third-party reverse-engineered; Anthropic has not published a schema. This
adapter MUST be implemented defensively (probe for files, fail gracefully if
structure changes) and is expected to be **retired** when Anthropic ships the
promised Claude Design API or bundle schema (RESEARCH-010 REC-3).

---

## When This Integration Is Used

A user has authored a design in Claude Design's web UI (claude.ai), chosen
**"Send to Claude Code"** export, and the resulting handoff bundle is on disk
inside the worktree (or at any path the user can provide). Two entry points:

1. **Extract mode (Phase 02a):** `/create-design --extract <bundle-path>`. Phase 00
   sets `MODE=extract` and `EXTRACT_PATH=<bundle-path>`. Phase 02a invokes
   `mockup-extractor` with `FRAMEWORK="claude-design-bundle"`. Phases 03–05
   are skipped (existing extract-mode behavior).

2. **Phase 03 fast-path (new Step 3.0):** A user in `story` or `standalone`
   mode is asked at the start of Phase 03 whether they have a Claude Design
   bundle available. If yes, Step 3.0 routes to `mockup-extractor` with the
   same `FRAMEWORK="claude-design-bundle"` framework hint; Phase 03's
   8-step interactive discovery (Steps 3.1–3.8) is skipped EXCEPT for the
   minimal framework+styling questions that the bundle cannot answer.

---

## Bundle Structure (third-party reverse-engineered; defensive parsing required)

Anthropic has NOT published a schema. The following file/directory layout is
derived from multiple third-party sources (designaistack.com, claudefa.st,
newsletter.victordibia.com — all cited in RESEARCH-010 §Sources). Sources
disagree on archive format (tar vs zip) and exact filenames. **Treat every
filename below as a candidate, not a guarantee.**

```
<bundle-root>/
  PROMPT.md                      ← Anthropic-mentioned; instructions to Claude Code
  design-tokens.{json,js,ts}     ← color / spacing / typography tokens
  components.{json,md}           ← machine-readable component spec
  layout.{json,md}               ← layout hierarchy
  assets/                        ← images, icons, fonts referenced by components
  README.md                      ← optional; some sources say there's a README
```

**Candidate filenames (try in order — first match wins):**

| Purpose | Candidates |
|---------|------------|
| Instructions | `PROMPT.md`, `README.md`, `INSTRUCTIONS.md` |
| Design tokens | `design-tokens.json`, `tokens.json`, `style-dictionary.json`, `tokens.js`, `tokens.ts` |
| Components | `components.json`, `component-structure.json`, `components.md`, `component-spec.json` |
| Layout | `layout.json`, `layout-hierarchy.json`, `layout.md` |
| Assets | `assets/`, `images/`, `media/` |

If NO candidate is found for the **Instructions** category, this is NOT a
Claude Design bundle — the extractor MUST report `bundle_detected=false` and
return control to the orchestrator with a clear error message.

---

## Bundle Detection Heuristic (used by `mockup-extractor`)

```
1. Probe for any Instructions candidate at <bundle-root>:
     Glob(pattern="${bundle_root}/PROMPT.md")
     Glob(pattern="${bundle_root}/README.md")
     Glob(pattern="${bundle_root}/INSTRUCTIONS.md")
2. If NO Instructions file found:
     bundle_detected = false
     HALT — "Path does not appear to be a Claude Design handoff bundle. Expected one of: PROMPT.md, README.md, INSTRUCTIONS.md"
3. If Instructions file found:
     Read it. Check content for any of these markers:
       - "Claude Design"
       - "claude.ai/design"
       - "anthropic"
       - "design tokens"
       - "component spec"
       - "handoff bundle"
     If at least 2 markers match: bundle_detected = true.
     Otherwise: bundle_detected = INCONCLUSIVE — proceed but mark warning.
4. Probe for design-tokens candidates (in order). First match → TOKEN_FILE.
5. Probe for component candidates (in order). First match → COMPONENT_FILE.
6. Probe for layout candidates (in order). First match → LAYOUT_FILE.
7. Probe for assets/ directory.
```

The extractor MUST report which candidates matched. If TOKEN_FILE or
COMPONENT_FILE is missing, the extractor MUST emit a warning but proceed —
the bundle is partially parseable. If both are missing, the bundle is
unusable and the extractor MUST HALT with `bundle_detected=partial-unusable`.

---

## Token / Component Extraction (per-file-format)

### `design-tokens.json` / `tokens.json` / `style-dictionary.json`

These follow no fixed schema, but typical shape (style-dictionary convention):

```json
{
  "color": {
    "primary": { "value": "#3b82f6" },
    "neutral": { "100": { "value": "#f4f4f5" }, "900": { "value": "#18181b" } }
  },
  "spacing": { "1": { "value": "4px" }, "2": { "value": "8px" } },
  "typography": { "heading": { "fontSize": { "value": "24px" } } }
}
```

**Extraction strategy:**
- Flatten nested keys into `<category>.<name>` semantic token names (e.g., `color.primary`, `spacing.1`).
- Map each leaf `.value` field to the `design.md` token catalog under the appropriate section (Design Token Catalog → colors / spacing / typography).
- If the file is `.js` / `.ts`, attempt JSON-comment-stripping + JSON5 parse fallback. If that fails, emit `tokens_parse_failed=true` warning and skip.

### `components.json` / `component-structure.json`

Typical shape:

```json
{
  "components": [
    { "name": "Header", "props": [...], "children": ["Logo", "Nav", "ProfileMenu"], "tokens_used": ["color.primary", "spacing.4"] }
  ]
}
```

**Extraction strategy:**
- Map each `components[N]` entry to a `COMP-NNN` block in `design.md` Component Inventory.
- Children IDs are reconciled against the components list to satisfy the children-integrity gate (per `design-source-of-truth-schema.md`).
- If `props` is missing for a component, mark `props_completeness_gate=false` for that component but continue.

### `layout.json` / `layout-hierarchy.json`

**Extraction strategy:**
- Map to `design.md` Layout Specification (LAYOUT-NNN blocks).
- If the bundle ships a grid spec, populate `grid` / `regions` / `responsive`. If only ASCII / nested-component-tree is present, emit `ascii_layout` only.

### `PROMPT.md` / `README.md`

**Extraction strategy:**
- Treat as Design Intent narrative source.
- Map to `design.md` `intent.design_philosophy` and `intent.aesthetic_vibe` (free-text).
- Do NOT use it to override extracted structured data; it is narrative reinforcement.

---

## Validation Gates Specific to Bundle-Sourced design.md

The Python validator (`scripts/validate_design_md.py`) runs identically on
bundle-sourced and codebase-sourced `design.md`. The validator does not know
or care which source produced the file. Hard gates:

- Token normalization ≥70% (RESEARCH-003 R2).
- Min 40 lines per component (average).
- Required component sections: visual, data, accessibility.
- Props completeness per component.
- Children integrity (no dangling COMP-NNN refs).

When the bundle source is partial (missing tokens or components), the
extractor SHOULD pad missing sections with `"_source": "bundle_missing"`
markers so the validator can distinguish bundle-source-gaps from
implementation defects.

---

## What This Adapter Does NOT Do

- **It does not call any Claude Design API.** No such API exists as of
  2026-05-20 (RESEARCH-010 Finding 4). All integration is via files on disk.
- **It does not modify the Claude Design bundle on disk.** Read-only.
- **It does not validate that the bundle came from Claude Design specifically.**
  Bundle detection is a heuristic; a directory with a `PROMPT.md` mentioning
  "Claude Design" passes detection regardless of whether Anthropic produced
  it. This is intentional — the format itself is the integration surface.
- **It does not replace `design.md`.** Per ADR-075 and RESEARCH-010 Finding 5,
  the bundle is "product-level memory"; `design.md` is "a portable contract."
  This adapter consumes the bundle to produce `design.md`.

---

## Retirement Triggers

This adapter is **disposable** and should be retired when:

1. Anthropic publishes a Claude Design bundle schema (ADR-075 TR-1). At that
   point, replace heuristic file-probing with schema-driven parsing.
2. Anthropic ships a Claude Design API / MCP / Agent SDK surface (ADR-075
   TR-2). At that point, replace this file-disk adapter with an
   API-based integration (no operator handoff needed).
3. The bundle structure changes incompatibly (third-party reports indicate
   this; the adapter starts failing on new bundles). At that point, decide
   whether to maintain the adapter or wait for TR-1/TR-2.

The 90-day review trigger in ADR-075 (2026-08-20) will check whether any
of these conditions has fired.

---

## References

- **RESEARCH-010** (`devforgeai/specs/research/RESEARCH-010-claude-design-integration.research.md`) — full Claude Design research; Anthropic primary citation; third-party bundle-internals citations (cited as DERIVED).
- **ADR-075** (`devforgeai/specs/adrs/ADR-075-design-md-format-stay-decision.md`) — format-stay decision with three trigger conditions.
- **ADR-078** (`devforgeai/specs/adrs/ADR-078-spec-driven-design-modernization.md`) — modernization umbrella.
- **`design-source-of-truth-schema.md`** — the design.md schema this adapter must produce.
- **`design-source-of-truth-population.md`** — the population procedure this adapter follows.
- **`mockup-extractor.md`** (`.claude/agents/`) — the subagent that uses this reference.
