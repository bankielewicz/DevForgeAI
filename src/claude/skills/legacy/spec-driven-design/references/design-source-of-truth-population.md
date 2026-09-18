# UI Design Source of Truth — Population Reference

**Purpose:** Define how to populate the design.md template from different sources: interactive discovery, existing mockup code extraction, or existing UI-SPEC-SUMMARY.md artifacts.
**Version:** 1.0
**Loaded by:** Phase 06 (Step 6.2.5 — generation mode), Phase 02a (extraction mode)

---

## Population Modes

The design.md can be populated from three sources:

| Mode | Trigger | Source Data | Fidelity |
|------|---------|-------------|----------|
| **Generated** | Normal `/create-design` flow | Phase 03 interactive discovery + Phase 05 code output | HIGH — user-validated choices |
| **Extracted** | `/create-design --extract <path>` | Existing component code analysis | MEDIUM-HIGH — requires user validation |
| **Hybrid** | Extraction + interactive refinement | Code analysis + user corrections | HIGHEST — machine + human |

---

## Mode 1: Generated (From Interactive Discovery)

When spec-driven-design runs its normal workflow, design.md is populated from Phase 03 and Phase 05 outputs.

### Section-by-Section Population

#### Metadata
```
project        ← Current project name (from CWD or --project flag)
created        ← Current date
source_mode    ← "generated"
story_id       ← $STORY_ID from Phase 00 (or null)
epic_id        ← Extracted from story file frontmatter (or null)
```

#### Design Intent
```
aesthetic_vibe      ← Phase 03 Step 3.7a: User's aesthetic vibe selection
color_mode          ← Derived from aesthetic_vibe:
                       "dark" if vibe contains "dark"
                       "light" if vibe contains "light/clean/minimal"
                       "system-adaptive" otherwise
design_philosophy   ← Derived from aesthetic_vibe keyword mapping:
                       "glassmorphism" if vibe contains "glass"
                       "flat" if vibe contains "flat/clean"
                       "minimal" if vibe contains "minimal/soft"
                       "material" if vibe contains "material"
                       User-provided if custom vibe
target_platforms    ← Derived from Phase 03 Step 3.1 (UI type):
                       Web → ["web-desktop", "web-mobile", "web-tablet"]
                       GUI → ["desktop-{os}"]
                       TUI → ["terminal"]
```

#### Design Tokens
```
colors         ← Load design-system-rules.md Section 2 (Semantic Color Tokens)
                  Map framework-specific tokens to hex values:
                  "slate-50" → "#f8fafc"
                  "slate-950" → "#020617"
                  "white" → "#ffffff"
                  "slate-900" → "#0f172a"
                  User's aesthetic vibe influences primary color choice

spacing        ← Load design-system-rules.md Section 1 (8-Point Grid)
                  Direct mapping: unit = "8px", scale from specification

typography     ← Load design-system-rules.md Section 3 (Typography Scale)
                  font_family from user selection or default "Inter, system-ui"
                  Map Tailwind classes to concrete values:
                  "text-4xl" → "36px"
                  "text-2xl" → "24px"
                  "text-lg" → "18px"
                  "text-base" → "16px"
                  "text-sm" → "14px"

borders        ← Load design-system-rules.md Section 4
                  Map Tailwind radius: "rounded-xl" → "12px", "rounded-md" → "6px"

shadows        ← Load design-system-rules.md Section 4
                  Map: "shadow-sm" → CSS value, "shadow-md" → CSS value

motion         ← Load design-system-rules.md Section 5
                  Map: "duration-200" → "200ms", "ease-in-out" → CSS value

responsive     ← Standard breakpoints from Tailwind defaults:
                  mobile: 640px, tablet: 1024px, desktop: 1280px
```

#### Component Inventory
```
FOR each component in Phase 03 Step 3.8 (component list):
  Create COMP-NNN entry:
    name           ← Component name from user definition
    type           ← Classify by component elements:
                      Has form elements → "form"
                      Is page wrapper → "layout"
                      Shows data → "display"
                      Navigation elements → "navigation"
                      Modal/dialog → "dialog"
    classification ← Classify per component-anatomy.md rules:
                      Has data fetching/state → "smart"
                      Pure display/props only → "dumb"
    visual         ← Derive from Phase 05 generated code:
                      Extract className/style attributes
                      Map to token references
    content        ← Extract from Phase 05 generated JSX/markup:
                      Each JSX element → content entry
    states         ← Extract from Phase 05 code:
                      className containing "hover:" → hover state
                      className containing "focus:" → focused state
                      className containing "disabled:" → disabled state
                      Loading/error handling code → loading/error states
    data           ← Extract from Phase 05 code:
                      Props interface → data.props
                      useState/useReducer → data.internal_state
                      Event handler props → data.events_emitted

                      MANDATORY PROP CHECKS (apply to ALL components):
                      1. children: If component renders {children} or {props.children},
                         MUST include { name: "children", type: "ReactNode", required: true }
                      2. className: If component accepts className (via props or ...rest),
                         MUST include { name: "className", type: "string", required: false }
                      3. Callback props: Every prop whose type contains "=>" or "void"
                         MUST appear in both data.props AND events_emitted
                      4. Variant props: Props like variant, size, status that control visual
                         MUST be documented with all valid values (union type)

    accessibility  ← Extract from Phase 05 code:
                      role="" attributes → accessibility.role
                      aria-label → accessibility.label
                      onKeyDown handlers → accessibility.keyboard
```

#### Layouts
```
FOR each unique page/screen implied by component hierarchy:
  Create LAYOUT-NNN entry:
    regions        ← Group components by spatial relationship:
                      Top-level components → separate regions
                      Nested components → within parent region
    ascii_layout   ← Generate from component hierarchy:
                      Use box-drawing characters
                      Reference COMP-NNN IDs
    responsive     ← Derive from breakpoint-specific classes in generated code
```

#### Interactions
```
# EVERY callback prop MUST be covered by at least one FLOW-NNN.
# Do NOT filter to "multi-step flows only" — single-action callbacks
# (onChange, onRowClick, onClose) are interactions too.

# Step 1: Build callback inventory from ALL component data.events_emitted
callback_inventory = collect all events_emitted from all components

# Step 2: Group into flows by category
FOR each callback category (navigation, toggle, selection, CRUD, responsive, error):
  Create FLOW-NNN entry:
    trigger     ← The initiating event (onClick, onChange, onSubmit, etc.)
    steps       ← Trace the handler logic into sequential steps
                   Include: user action → system response → visual feedback → state change
    error_paths ← Extract from try/catch or error state handling
    success     ← Final state after flow completes

# Step 3: Completeness gate
FOR each callback in inventory:
  IF NOT referenced in any FLOW: Create minimal FLOW for it

# PROHIBITED: Skipping a callback because "it's a simple one-liner"
# Every callback is a user interaction that an AI needs to reproduce.
```

#### Animations
```
FOR each transition/animation class in Phase 05 generated code:
  Create ANIM-NNN entry:
    Extract CSS transition properties
    Map Tailwind classes to concrete values
    Derive trigger from the element's interaction context
```

---

## Mode 2: Extracted (From Existing Mockup Code)

When running `/create-design --extract <path>`, the skill reads existing code and reverse-engineers the design.md.

### Extraction Pipeline

#### Step 1: Discover Source Files
```
source_path = user-provided path
file_list = Glob(pattern="${source_path}/**/*.{jsx,tsx,vue,html,css,scss,py,xaml}")

# Classify files
component_files = files matching *.jsx, *.tsx, *.vue
style_files = files matching *.css, *.scss, *.module.css
config_files = files matching tailwind.config.*, theme.*, package.json
```

#### Step 2: Extract Design Tokens

**Step 2.0 — Detect the styling system (route token extraction):**

Before extracting, detect which styling system the mockup uses so the correct extraction branch runs. A React (or any JS) codebase may forbid Tailwind and theme entirely via a JS token object + CSS variables — in that case the Tailwind branches below match nothing and produce an empty catalog. Route as follows:

- **Tailwind path:** `tailwind.config.js` / `tailwind.config.ts` exists → use the *From Tailwind config* and *From inline styles/Tailwind classes* branches below.
- **CSS-variable path (non-Tailwind):** `--[a-z-]+:` declarations exist in `.css` / `.scss` files AND no Tailwind config → use the *From CSS/SCSS files* branch plus the *From JS token objects / CSS variables (non-Tailwind)* branch below.
- **JS token-object path (non-Tailwind):** a `theme.{js,ts,jsx,tsx}` / `tokens.{js,ts,json}` / `design-tokens.*` module exists → use the *From JS token objects / CSS variables (non-Tailwind)* branch below.
- **Fallback:** if detection is ambiguous, apply all branches and merge/deduplicate by semantic token name.

**From CSS/SCSS files:**
```
Grep for CSS custom properties:
  pattern: "--[a-z-]+:\\s*[^;]+"
  Map: --color-primary → colors.primary
  Map: --spacing-* → spacing.scale
  Map: --font-* → typography

Grep for color values:
  pattern: "#[0-9a-fA-F]{3,8}"
  Deduplicate and classify by usage context
```

**From Tailwind config:**
```
Read tailwind.config.js/ts:
  Extract: theme.extend.colors → colors tokens
  Extract: theme.extend.spacing → spacing tokens
  Extract: theme.extend.fontFamily → typography.font_family
  Extract: theme.extend.borderRadius → borders.radius
  Extract: theme.extend.boxShadow → shadows
```

**From inline styles/Tailwind classes:**
```
Grep for Tailwind color classes:
  pattern: "(?:bg|text|border)-[a-z]+-[0-9]+"
  Deduplicate and map to hex values using Tailwind palette

Grep for spacing classes:
  pattern: "(?:p|m|gap|space)-[a-z]?-?[0-9]+"
  Map to px values using Tailwind scale
```

**From styled-components/CSS-in-JS:**
```
Grep for template literal styles:
  pattern: "styled\\.[a-z]+`[^`]+`"
  Extract CSS properties from template literals
  Map values to semantic tokens
```

**From JS token objects / CSS variables (non-Tailwind):**

For React (or any JS) mockups that style via a JS token object + `ThemeProvider`/inline styles
and/or CSS custom properties — the common enterprise pattern when Tailwind/CSS-in-JS is forbidden —
the Tailwind branches above match nothing. Use these four steps instead:

```
Step A — Read the JS token-object module:
  Read theme.{js,ts,jsx,tsx} / tokens.{js,ts,json} / design-tokens.* in full
  Extract key:value pairs:
    pattern: "['\"](?:color|background|text|border|spacing|radius|shadow|font)[^'\"]*['\"]:\\s*['\"]([^'\"]+)['\"]"
  Identify object roots:
    pattern: "^export\\s+(?:const|default)\\s+\\w+\\s*=\\s*\\{"

Step B — Build the CSS-variable map:
  Read .css / .scss files; Grep CSS custom-property declarations:
    pattern: "--[a-z][a-z0-9-]*:\\s*[^;]+"
  Record each --token-name → concrete value (hex / rgba / px / rem)

Step C — Resolve var(--token) usages back to concrete values:
  Grep "var\\(--[a-z][a-z0-9-]*\\)" usages in the JSX/TSX
  Substitute each var(--name) with its value from the Step B map

Step D — Map extracted values to the 8 required Section 2 color token categories:
  colors.primary, colors.secondary, colors.background, colors.surface,
  colors.text, colors.border, colors.accent, colors.error
  (Section 2 of design.md requires these 8 — fill each from the token object /
   CSS-variable map; flag any that cannot be resolved rather than hallucinating.)
```

#### Step 3: Extract Component Hierarchy

**From React/JSX:**
```
FOR each .jsx/.tsx file:
  Extract: Component name from export statement
  Extract: Props interface/type from TypeScript
  Extract: useState/useReducer for internal state
  Extract: useEffect for data dependencies
  Extract: Event handler props (onClick, onChange, etc.)
  Extract: Child component imports for hierarchy
  Extract: JSX tree structure for content elements
  Extract: className attributes for visual properties
  Extract: ARIA attributes for accessibility
  Extract: Conditional rendering for states (loading, error)
```

**From Vue SFC:**
```
FOR each .vue file:
  Extract: Component name from script setup / export default
  Extract: Props from defineProps
  Extract: State from ref/reactive
  Extract: Events from defineEmits
  Extract: Template structure for content elements
  Extract: Class bindings for visual/state properties
```

**From HTML:**
```
FOR each .html file:
  Extract: Semantic structure (header, nav, main, aside, footer)
  Extract: Class attributes for visual properties
  Extract: ARIA attributes for accessibility
  Extract: Event attributes (onclick, onsubmit) for interactions
  Extract: Form elements for data contracts
```

**From WPF XAML:**
```
FOR each .xaml file:
  Extract: Control types for component classification
  Extract: Properties for visual specification
  Extract: Bindings for data contracts
  Extract: Triggers/VisualStates for state machine
  Extract: Storyboard animations
```

#### Step 4: Extract Interaction Flows
```
FOR each event handler function:
  Trace the execution path:
    1. What triggers it (user action)
    2. What state changes occur
    3. What API calls are made
    4. What visual feedback is shown
    5. What error handling exists
    6. What success state results

  Group related handlers into FLOW-NNN entries:
    Form submission → complete form flow
    Navigation clicks → navigation flow
    CRUD operations → data management flow
```

#### Step 5: Extract Animations
```
Grep for CSS transitions:
  pattern: "transition[^;]+;"
  Map to ANIM-NNN entries

Grep for CSS animations:
  pattern: "@keyframes\\s+[a-z]+"
  Map to ANIM-NNN entries

Grep for Tailwind transition classes:
  pattern: "transition-[a-z]+|duration-[0-9]+|ease-[a-z]+"
  Group by element and map to ANIM-NNN entries

Grep for JS animation libraries:
  pattern: "framer-motion|react-spring|gsap|anime"
  Extract animation configurations
```

#### Step 6: User Validation Gate

After extraction completes, present findings to user via AskUserQuestion:

```
AskUserQuestion:
  Question: "I extracted the following from your mockup. Please validate:"
  Header: "Extraction Review"
  Content:
    - Components found: {N} ({list of names})
    - Design tokens: {N} colors, {N} spacing values, {N} typography entries
    - Interactions: {N} flows detected
    - Animations: {N} transitions found
    - Gaps detected: {list of sections with incomplete data}

  Options:
    - "Looks correct, generate design.md"
    - "I need to correct some details" (→ interactive refinement)
    - "Start over with interactive discovery instead"
```

---

## Mode 3: Hybrid (Extraction + Refinement)

When extraction produces incomplete data (common for CSS-in-JS or highly dynamic UIs):

1. Run extraction pipeline (Mode 2, Steps 1-5)
2. Identify gaps (sections with placeholder or missing data)
3. For each gap, use AskUserQuestion to fill:
   - Missing color tokens → "What is the primary brand color?"
   - Missing typography → "What font family does the design use?"
   - Unclear interactions → "What happens when user clicks {element}?"
   - Missing accessibility → "What ARIA role should {component} have?"
4. Merge extracted + user-provided data
5. Generate final design.md

---

## Token Normalization (MANDATORY — All Modes)

**Applies to:** Generated, Extracted, AND Hybrid modes.
**Execution:** As a **SEPARATE STEP** (Step 2a.4.5 in extract mode, Step 6.2.4 in generated mode) — NOT inline with component extraction.

Component `visual` sections MUST use semantic token references (e.g., `colors.surface`) instead of raw values (e.g., `rgba(15, 23, 42, 0.6)`). This ensures any AI recreating the UI uses the design system tokens, not hardcoded values.

### Why Separate Step (RCA from OmniWatchAI Round 3)

Token normalization was originally an inline rule within component extraction. Result: 16.5% normalization rate — the extraction step's complexity caused the LLM to deprioritize normalization. Making it a SEPARATE step with its own Execute-Verify-Record triplet enforces it independently.

### Process (3 Phases)

**Phase A: Print prohibited values checklist**
Before normalizing, display the COMPLETE reverse lookup table as a visual checklist. This forces the LLM to see every value that must be replaced.

**Phase B: Scan and replace**
For each component's visual properties (background, border, shadow, spacing, dimensions, content styles, state overrides, variants), look up each raw value in the reverse lookup table. Replace with token reference. Count normalized vs raw.

**Phase C: Verify threshold**
```
normalization_pct = normalized / (normalized + raw) * 100

IF normalization_pct < 50%:
  HALT — "Token normalization below 50%. Re-check reverse lookup table."
IF normalization_pct >= 50% but < 70%:
  WARNING — acceptable but improvement needed
IF normalization_pct >= 70%:
  PASS
```

### Why This Matters

Without token normalization:
- An AI sees `background: "rgba(15, 23, 42, 0.6)"` and hardcodes that value
- If the design system changes (e.g., surface becomes lighter), every component breaks
- The design.md becomes a snapshot, not a system

With token normalization:
- An AI sees `background: "colors.surface"` and uses the token
- Design system changes propagate automatically through all components
- The design.md is a true design SYSTEM document, not a values dump

---

## Tailwind Class to Concrete Value Mapping

This reference table enables extraction from Tailwind-heavy codebases.

### Colors
| Tailwind | Hex |
|----------|-----|
| `slate-50` | `#f8fafc` |
| `slate-100` | `#f1f5f9` |
| `slate-200` | `#e2e8f0` |
| `slate-300` | `#cbd5e1` |
| `slate-400` | `#94a3b8` |
| `slate-500` | `#64748b` |
| `slate-600` | `#475569` |
| `slate-700` | `#334155` |
| `slate-800` | `#1e293b` |
| `slate-900` | `#0f172a` |
| `slate-950` | `#020617` |
| `white` | `#ffffff` |
| `black` | `#000000` |
| `emerald-600` | `#059669` |
| `rose-600` | `#e11d48` |
| `amber-600` | `#d97706` |
| `blue-600` | `#2563eb` |

### Spacing
| Tailwind | Pixels |
|----------|--------|
| `1` | 4px |
| `2` | 8px |
| `3` | 12px |
| `4` | 16px |
| `5` | 20px |
| `6` | 24px |
| `8` | 32px |
| `10` | 40px |
| `12` | 48px |
| `16` | 64px |
| `20` | 80px |
| `24` | 96px |

### Typography
| Tailwind | Size |
|----------|------|
| `text-xs` | 12px |
| `text-sm` | 14px |
| `text-base` | 16px |
| `text-lg` | 18px |
| `text-xl` | 20px |
| `text-2xl` | 24px |
| `text-3xl` | 30px |
| `text-4xl` | 36px |

### Border Radius
| Tailwind | Pixels |
|----------|--------|
| `rounded-sm` | 2px |
| `rounded` | 4px |
| `rounded-md` | 6px |
| `rounded-lg` | 8px |
| `rounded-xl` | 12px |
| `rounded-2xl` | 16px |
| `rounded-full` | 9999px |

### Shadows
| Tailwind | CSS Value |
|----------|-----------|
| `shadow-sm` | `0 1px 2px 0 rgb(0 0 0 / 0.05)` |
| `shadow` | `0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)` |
| `shadow-md` | `0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)` |
| `shadow-lg` | `0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)` |
| `shadow-xl` | `0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)` |

---

## Validation After Population

After populating design.md from any mode, run these checks:

### Completeness Check
```
FOR each required field in design-source-of-truth-schema.md:
  Grep(pattern="${FIELD_NAME}:", path="devforgeai/specs/ui/design.md")
  IF not found: Report missing field

FOR each "${...}" placeholder:
  Grep(pattern="\\$\\{", path="devforgeai/specs/ui/design.md")
  IF found: Report unpopulated template variable
```

### Cross-Reference Check
```
Extract all COMP-NNN IDs from components section
Extract all COMP-NNN references from layouts.regions.components
Extract all COMP-NNN references from interactions.steps.component

FOR each referenced COMP-NNN:
  IF not in components section: Report dangling reference
```

### Token Consistency Check
```
Extract all token references from component visual specifications
FOR each token reference (e.g., "colors.primary", "spacing.md"):
  IF not defined in tokens section: Report undefined token
```
