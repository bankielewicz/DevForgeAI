# UI Design Source of Truth — Schema Reference

**Purpose:** Define the schema rules, field descriptions, and validation requirements for `design.md` documents.
**Version:** 1.1
**Template:** `assets/templates/design-source-of-truth-template.md`
**Loaded by:** Phase 06 (Step 6.2.5), Phase 07 (Step 7.6-7.8), Phase 02a (Extract Mode)

---

## Overview

The UI Design Source of Truth (`design.md`) is a framework-agnostic UI specification document that captures full visual and behavioral fidelity. It uses a hybrid YAML frontmatter + structured markdown format optimized for AI LLM consumption. Schema 1.1 adds deterministic invocation applicability and generated-web review evidence. Existing schema-1.0 documents remain accepted for downstream read compatibility and MUST NOT be silently rewritten.

**Key Design Principles:**
1. **Framework-agnostic** — Describes WHAT, not framework-specific HOW
2. **Token-based** — All visual values reference semantic tokens, never raw values
3. **Complete** — An AI reading this document alone can recreate the entire UI
4. **Validated** — Schema validation catches missing or invalid fields
5. **Consumed by all skills** — Single document, multiple consumers, zero silos

## Output Location

```
devforgeai/specs/ui/design.md
```

This path is fixed and must not change. All consuming skills inspect this location before consuming design.md.

---

## Section Schema Definitions

### Section 1: Document Metadata

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `schema_version` | string | YES | "1.1" for newly generated documents; "1.0" remains read-compatible |
| `document_type` | string | YES | Always "ui-design-source-of-truth" |
| `project` | string | YES | Project name |
| `created` | date | YES | ISO 8601 date (YYYY-MM-DD) |
| `updated` | date | YES | ISO 8601 date, updated on each change |
| `source_skill` | string | YES | Always "spec-driven-design" |
| `source_mode` | enum | YES | "generated", "extracted", or "hybrid" |
| `mode` | enum | YES in 1.1 | "story", "standalone", or "extract" |
| `platform` | enum | YES in 1.1 | "web", "gui", or "tui" |
| `story_id` | string | NO | STORY-NNN or null |
| `epic_id` | string | NO | EPIC-NNN or null |

**source_mode values:**
- `generated` — Created from scratch via interactive discovery (Phase 03)
- `extracted` — Extracted from existing mockup code via `--extract` mode
- `hybrid` — Combination: extracted base + interactive refinement

### Section 2: Design Intent

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `aesthetic_vibe` | string | YES | Free-text description of visual style |
| `color_mode` | enum | YES | "dark", "light", or "system-adaptive" |
| `design_philosophy` | string | YES | Design paradigm name |
| `target_platforms` | string[] | YES | Min 1. Platform identifiers |
| `brand_identity.name` | string | NO | Brand name if applicable |
| `brand_identity.personality` | string | NO | Brand personality description |
| `brand_identity.logo_placement` | string | NO | Where logo appears |

**Valid platform values:** "web-desktop", "web-mobile", "web-tablet", "desktop-windows", "desktop-macos", "desktop-linux", "terminal"

### Section 3: Design Token Catalog

#### Colors

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| `*.value` | string | YES | Valid hex (#XXXXXX or #XXX), rgb(), rgba(), or hsl() |
| `*.usage` | string | YES | Non-empty description of where this color is used |

**Required color tokens (minimum set):**
- `background`, `surface`, `text_primary`, `text_secondary`, `primary`, `error`, `success`, `border`

**Optional color tokens:**
- `surface_muted`, `surface_hover`, `text_disabled`, `text_inverse`, `primary_hover`, `secondary`, `warning`, `info`, `border_focus`

#### Spacing

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| `unit` | string | YES | Must be "8px" (8-point grid enforcement) |
| `scale.*` | object | YES | Min 5 entries. Each has `value` (px) and `usage` (string) |

**Validation:** All spacing values must be multiples of 4px.

#### Typography

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| `font_family.primary` | string | YES | Valid font stack |
| `font_family.mono` | string | YES | Valid monospace font stack |
| `scale.*` | object | YES | Min 4 entries: display, h1, body, caption |

**Per typography entry:**
| Field | Type | Required |
|-------|------|----------|
| `size` | string | YES |
| `weight` | number | YES |
| `line_height` | number | YES |
| `usage` | string | YES |

#### Borders

| Field | Type | Required |
|-------|------|----------|
| `radius.*` | object | YES |
| `width.default` | string | YES |

**Required radius tokens:** `sm`, `md`, `lg`

#### Shadows

| Field | Type | Required |
|-------|------|----------|
| `sm` | object | YES |
| `md` | object | YES |
| `lg` | object | YES |

Each shadow entry has `value` (CSS box-shadow string) and `usage` (description).

#### Motion

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| `duration.*` | object | YES | Min 3 entries with ms values |
| `easing.*` | object | YES | Min 1 entry with valid CSS easing |
| `transitions.default` | string | YES | Valid CSS transition shorthand |

#### Responsive

| Field | Type | Required |
|-------|------|----------|
| `breakpoints.*` | object | YES | Min 2 breakpoints |
| `container.max_width` | string | NO |
| `container.padding` | string | NO |

#### Z-Index

| Field | Type | Required |
|-------|------|----------|
| `base` | number | YES |
| `modal` | number | YES |
| `tooltip` | number | YES |

---

### Section 4: Component Inventory

Each component entry must have:

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| `id` | string | YES | Format: COMP-NNN (unique, sequential) |
| `name` | string | YES | PascalCase component name |
| `type` | enum | YES | layout, form, display, navigation, dialog, feedback, data, composite |
| `classification` | enum | YES | "smart" or "dumb" |
| `description` | string | YES | Non-empty, min 10 characters |
| `parent` | string | YES | Valid COMP-NNN or "root" |
| `children` | string[] | NO | Array of valid COMP-NNN IDs |

#### Component Visual Specification

| Field | Type | Required |
|-------|------|----------|
| `visual.dimensions` | object | YES |
| `visual.spacing` | object | YES |
| `visual.appearance` | object | YES |

**Validation:** All values must reference design tokens (e.g., "spacing.md", "colors.surface"), NOT raw CSS values.

#### Component Content Elements

| Field | Type | Required |
|-------|------|----------|
| `content[].element` | enum | YES |
| `content[].id` | string | YES |
| `content[].style` | object | NO |

**Valid element types:** heading, text, icon, image, input, button, select, checkbox, radio, toggle, list, table, chart, divider, badge, avatar, skeleton

#### Component State Machine

**Required states for ALL components:**
- `default` — Resting state (always required)

**Required states for INTERACTIVE components (buttons, inputs, links, cards with click handlers):**
- `hover` — Mouse over
- `focused` — Keyboard focus
- `disabled` — Non-interactive

**Optional states:**
- `active`, `loading`, `error`, `selected`, `expanded`, `collapsed`

#### Component Data Contract

**Required for ALL components (smart AND dumb):**
| Field | Type | Required | Validation |
|-------|------|----------|------------|
| `data.props` | array | YES | Min 1 prop for ALL components. Dumb components have props too (children, className, variant, etc.) |
| `data.events_emitted` | array | YES if component has callback props | Every prop with type containing "=>" MUST also appear as an event |
| `data.internal_state` | array | Smart only | Omit entirely for dumb components |
| `data.data_dependencies` | array | Smart only | Omit entirely for dumb components |

**Mandatory prop rules (apply to ALL components regardless of classification):**
- **`children`**: If the component renders `{children}` or `{props.children}`, `children` MUST be in `data.props`
- **`className`**: If the component accepts `className` via props or `...rest` spread, it MUST be in `data.props`
- **Callback props**: Every prop whose type includes `=>` or `void` MUST appear in BOTH `data.props` AND `data.events_emitted`
- **Variant/enum props**: Props like `variant`, `size`, `status` MUST list all valid values as a union type (e.g., `"'primary'|'secondary'|'ghost'"`)

**Validation rule**: An AI reading the `data.props` list must be able to instantiate the component correctly. If a prop exists in source code but not in the spec, the spec is incomplete.

#### Component Accessibility

| Field | Type | Required |
|-------|------|----------|
| `accessibility.role` | string | YES |
| `accessibility.label` | string | YES for interactive components |
| `accessibility.keyboard` | object | YES for interactive components |
| `accessibility.screen_reader` | object | YES |
| `accessibility.contrast` | object | YES |

#### Component Reconstruction Metadata (RESEARCH-003 R3)

Per-component metadata enabling any AI to verify its implementation matches the spec.
SpecifyUI research shows 14.4% higher structural fidelity with explicit dimension constraints
(Source: arxiv.org/html/2509.07334v1). Osmani guidance: screenshots as first-class spec
artifacts (Source: addyosmani.com/blog/good-spec/).

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `reconstruction.reference_viewport` | string | YES | Viewport dimensions used for measurement (e.g., "1280x800") |
| `reconstruction.expected_dimensions.width` | string | YES | Measured/computed width at reference viewport |
| `reconstruction.expected_dimensions.height` | string | YES | Measured/computed height at reference viewport |
| `reconstruction.visual_baseline` | string | NO | Path to per-component screenshot, or null |
| `reconstruction.bounding_box` | object | NO | Pixel coordinates {x, y, width, height} at reference viewport |
| `reconstruction.z_layer` | string | NO | z_index token reference (e.g., "z_index.base") |

**Validation:**
- `reference_viewport` must match format "NNNNxNNNN" (e.g., "1280x800")
- `expected_dimensions` must have both width and height populated (not placeholders)
- `visual_baseline` path must use forward slashes and reference `visual-capture/` directory
- `z_layer` must reference a valid z_index token from Section 2

---

### Section 5: Layout Specification

Each layout entry must have:

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| `id` | string | YES | Format: LAYOUT-NNN |
| `name` | string | YES | Descriptive page/screen name |
| `description` | string | YES | Non-empty |
| `grid` | object | YES | type, columns, gap |
| `regions` | array | YES | Min 1 region |
| `responsive` | object | YES | Min mobile behavior defined |
| `ascii_layout` | string | YES | Multi-line ASCII diagram |

**Region validation:**
- All `components[]` entries must reference valid COMP-NNN IDs from Section 3
- Regions must have `name`, `components`, `dimensions`

**ASCII layout validation:**
- Must contain at least one COMP-NNN reference
- Must use box-drawing characters (+, -, |, or Unicode variants)

---

### Section 6: Interaction Flows

**Completeness rule:** Every callback prop (`on*`) from Section 3 component `data.props` MUST be covered by at least one FLOW entry. Single-action callbacks (onChange, onRowClick, onClose) are flows too — document them.

Each interaction entry must have:

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| `id` | string | YES | Format: FLOW-NNN |
| `name` | string | YES | Descriptive flow name |
| `trigger` | string | YES | What initiates the flow |
| `steps` | array | YES | Min 1 step |
| `error_handling` | array | NO | Recommended if flow can fail. Required for form/CRUD flows. |
| `success_state` | object | NO | Recommended. Required for multi-step flows. |

**Step validation:**
- Each step must have `user_action`, `system_response`, `component` (valid COMP-NNN)
- `state_changes` must reference valid states from component's state machine

**Coverage validation:**
- Build list of all callback props from Section 3 components
- Each callback must appear in at least one FLOW step
- If uncovered callbacks exist, create minimal flows for them

---

### Section 7: Animation Specification

Each animation entry:

| Field | Type | Required |
|-------|------|----------|
| `id` | string | YES |
| `name` | string | YES |
| `trigger` | enum | YES |
| `target` | string | YES |
| `description` | string | YES |
| `properties` | array | YES |
| `duration` | string | YES |
| `easing` | string | YES |

**Valid trigger values:** mount, unmount, hover, click, scroll, state_change, route_change

---

### Section 8: Accessibility (Global)

All fields in this section are **required** and **must be true** for WCAG AA compliance.

---

### Section 9: Data Context

| Field | Type | Required |
|-------|------|----------|
| `api_endpoints` | array | NO |
| `global_state` | array | NO |
| `mock_data` | object | NO |

**Note:** In schema 1.1 this group is required but may contain empty collections when the UI has no backend data dependencies.

---

### Section 10: Design Review

This group follows `data_context` and is required only for generated web `story` and `standalone` documents. GUI, TUI, and `extract` documents omit the entire group when their explicit mode/platform metadata proves it inapplicable.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `status` | enum | YES | `pending`, `gate_passed`, or `below_threshold`; Phase 07 replaces `pending` |
| `review_path` | string | YES | Repository-relative `design-review.json` path |
| `selected_round` | integer/null | YES | Validated jury round; null only while pending |
| `composite` | number/null | YES | Validator-recomputed composite; null only while pending |
| `lint` | object | YES | Report path/hash and P0/P1/P2 counts |
| `render` | object | YES | Manifest path/hash and both screenshot paths |
| `remaining_must_fix` | string[] | YES | Empty for `gate_passed`; exact remaining gaps for `below_threshold` |

The final values MUST be copied from evidence accepted by `validate_design_review.py`; prose or model claims are not evidence.

---

## Validation Rules Summary

### Critical (HALT if violated)

1. `schema_version` must be "1.1" for newly generated documents; schema-1.0 is accepted read-only
2. All required metadata fields present
3. Minimum required color tokens present (8)
4. All spacing values are multiples of 4px
5. Every component has a unique COMP-NNN ID
6. Every COMP-NNN referenced in layouts exists in component inventory
7. Every COMP-NNN referenced in interactions exists in component inventory
8. No `${...}` template placeholders remain
9. Every component has `data.props` (smart AND dumb — dumb components have children/className/variant)
10. Component that renders `{children}` MUST have `children` in `data.props`
11. Every callback prop (`on*`) in `data.props` MUST appear in `data.events_emitted`
12. Every callback prop (`on*`) across all components MUST be covered by at least one FLOW-NNN
13. Every COMP-NNN in any `component.children[]` array MUST exist as a `component.id` in the inventory (RCA-003)
14. Every `component.parent` value (except `"root"`) MUST exist as a `component.id` in the inventory (RCA-003)
15. **Token normalization ≥ 70%**: Component visual values (background, border, shadow, padding, color, typography, etc.) MUST use semantic token references (e.g., `colors.surface`, `spacing.md`) — raw CSS values (`#hex`, `rgba(...)`) are PROHIBITED when a matching token exists. Hard gate at 70% minimum. (RESEARCH-003 R2; SpecifyUI: 14.4% higher structural fidelity — arxiv.org/html/2509.07334v1; Pandya: CSS variable audit prevents LLM hallucination — hvpandya.com/llm-design-systems)
16. Schema-1.1 groups MUST appear in this order: metadata, `design_intent`, `tokens`, `components`, `layouts`, `interactions`, `animations`, `accessibility`, `data_context`, then applicable `design_review`
17. Generated web `story`/`standalone` documents MUST include `design_review`; GUI, TUI, and `extract` documents MUST omit it

### Warning (Report but continue)

1. Component has no `content` elements defined
2. Layout has no `responsive` behavior for mobile
3. Interaction flow has no `error_handling` paths
4. Animation references non-existent COMP-NNN (may be element ID)
5. Component accepts `className` but it's not in `data.props`

---

## Cross-Skill Consumption Guide

### How Other Skills Read design.md

**Detection pattern (all skills use this):**
```
design_doc = locate "devforgeai/specs/ui/design.md"
IF design_doc exists:
  inspect "devforgeai/specs/ui/design.md"
  # Parse YAML frontmatter between first --- and second ---
  # Extract relevant sections
```

### Skill-Specific Consumption

| Skill | Sections Consumed | Purpose |
|-------|-------------------|---------|
| **spec-driven-ideation** | Metadata + Components count | Inform ui_design_context |
| **spec-driven-stories** | Components + Interactions + Accessibility | Populate story UI Specification section |
| **spec-driven-dev** | Full document | Implementation reference for frontend-developer subagent |
| **spec-driven-qa** | Components + Accessibility + Tokens | Validate implementation matches spec |
| **External AI** | Full document | Recreate UI from scratch |

---

## Versioning

When the design.md is updated:
1. Increment the `updated` date
2. Do NOT change `schema_version` unless the schema structure changes
3. Consuming skills re-read the file on each invocation — no cache invalidation needed
4. If components are added/removed, verify all COMP-NNN references in layouts and interactions

### Compatibility boundary

- Validators continue to accept schema-1.0 documents for downstream reads.
- New generation emits schema 1.1.
- No skill, hook, phase, installer, or validator may silently upgrade or rewrite a schema-1.0 document.
