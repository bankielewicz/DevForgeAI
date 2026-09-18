# Component Examples — Quality Bar

Two complete component specifications that demonstrate the minimum quality standard.
Every component in design.md must match or exceed this level of detail.

**Template:** `assets/templates/component-template.md`

---

## Example 1: Smart Component (GlobalSearch)

A smart component with internal state, event handling, and full accessibility.
Target: ~85 lines. Every field populated, every section present.

```yaml
  - id: "COMP-006"
    name: "GlobalSearch"
    type: "form"
    classification: "smart"
    description: >
      Global search input centered in the topbar. Glass-styled input with leading
      search icon, placeholder text showing keyboard shortcut (Ctrl+K), and trailing
      clear button. Focus state activates brand-colored border glow. Manages its own
      query state and emits debounced search events to the parent.
    parent: "COMP-002"
    children: []

    visual:
      dimensions:
        width: "100%"
        max_width: "520px"
        height: "auto"
      spacing:
        padding: "0 spacing.md"
        margin: "0 spacing.lg"
        gap: "spacing.sm"
      appearance:
        background: "rgba(255,255,255,0.04)"
        backdrop_filter: "blur(10px)"
        border: "borders.width.default solid colors.border"
        border_radius: "borders.radius.md"
        shadow: "shadows.none"
        overflow: "hidden"
        position: "relative"

    content:
      - element: "icon"
        id: "search-icon"
        text: "Search magnifying glass (16x16)"
        style:
          color: "colors.text_disabled"
        position: "left"
      - element: "input"
        id: "search-input"
        text: "Search endpoints, alerts, assets... (Ctrl+K)"
        style:
          typography: "typography.scale.body_small"
          color: "colors.text_primary"
        position: "center"
      - element: "button"
        id: "clear-btn"
        text: "× clear icon (14x14)"
        style:
          color: "colors.text_secondary"
        position: "right"
        conditional: "visible when query.length > 0"

    states:
      default:
        description: "Unfocused search input, placeholder visible"
        visual_overrides: {}
      hover:
        description: "Mouse cursor over input container"
        visual_overrides:
          background: "rgba(255,255,255,0.06)"
          cursor: "text"
      focused:
        description: "Input has keyboard focus"
        visual_overrides:
          border_color: "colors.border_focus"
          background: "rgba(255,255,255,0.06)"
          shadow: "0 0 0 3px colors.primary_glow"
      disabled:
        description: "Search unavailable"
        visual_overrides:
          opacity: "0.5"
          cursor: "not-allowed"
          pointer_events: "none"

    data:
      props:
        - name: "onSearch"
          type: "(query: string) => void"
          required: false
          description: "Debounced search handler — receives query text after 300ms idle"
        - name: "placeholder"
          type: "string"
          required: false
          default: "'Search endpoints, alerts, assets... (Ctrl+K)'"
          description: "Input placeholder text"
        - name: "className"
          type: "string"
          required: false
          description: "Additional CSS classes for container"
      events_emitted:
        - name: "onSearch"
          trigger: "User types in search input (debounced 300ms)"
          payload:
            type: "string"
            description: "Current query text"
          effect: "Filter dashboard results or open search overlay"
      internal_state:
        - name: "query"
          type: "string"
          initial_value: "''"
          description: "Current search input value, updated on every keystroke"

    accessibility:
      role: "search"
      label: "Global search"
      described_by: "null"
      keyboard:
        tab_order: "natural"
        key_handlers:
          - key: "Ctrl+K"
            action: "Focus search input from anywhere on page"
          - key: "Escape"
            action: "Clear query text and blur input"
      screen_reader:
        announcement: "Global search input. Type to search endpoints, alerts, and assets."
        live_region: "off"
      contrast:
        text_ratio: "4.5:1"
        interactive_ratio: "3:1"

    # ── RECONSTRUCTION METADATA (RESEARCH-003 R3) ──────────────
    reconstruction:
      reference_viewport: "1280x800"
      expected_dimensions:
        width: "520px"
        height: "40px"
      visual_baseline: null
      bounding_box: { x: 380, y: 12, width: 520, height: 40 }
      z_layer: "z_index.base"
```

**Why this is complete:**
- Description: 4 sentences covering purpose, appearance, interaction, and data flow
- Visual: 10 properties with token references (no raw hex except rgba for glass)
- Content: 3 elements (icon, input, button) with conditional visibility
- States: 4 states (default + 3 interactive) with meaningful overrides
- Data: 3 props, 1 event, 1 internal_state — all with descriptions
- Accessibility: role, label, 2 keyboard handlers, screen reader announcement, contrast ratios
- Reconstruction: viewport, expected dimensions, bounding box — enables fidelity verification (RESEARCH-003 R3)

---

## Example 2: Dumb Component (NavItem)

A dumb/presentational component with no internal state but a rich state machine.
Target: ~85 lines. Shows how to handle multiple visual states and enum props.

```yaml
  - id: "COMP-005"
    name: "NavItem"
    type: "navigation"
    classification: "dumb"
    description: >
      Individual navigation link within a sidebar section. Contains an SVG icon,
      label text, and optional count badge. Supports active, emphasized, disabled,
      hover, and focused states. 170+ instances across the application — each section
      group (CORE, MONITORING, APM, etc.) contains 8-15 NavItems.
    parent: "COMP-004"
    children: []

    visual:
      dimensions:
        width: "100%"
        height: "auto"
      spacing:
        padding: "spacing.sm spacing.md"
        margin: "0"
        gap: "spacing.sm"
      appearance:
        background: "transparent"
        border: "none"
        border_left: "3px solid transparent"
        border_radius: "borders.radius.sm"
        shadow: "shadows.none"
        overflow: "hidden"

    content:
      - element: "icon"
        id: "nav-icon"
        text: "SVG icon (18x18)"
        style:
          color: "colors.text_secondary"
        position: "left"
      - element: "text"
        id: "nav-label"
        text: "Navigation label"
        style:
          typography: "typography.scale.body_small"
          color: "colors.text_secondary"
        position: "center"
      - element: "badge"
        id: "nav-count"
        text: "Count badge (e.g., 42)"
        style:
          typography: "typography.scale.caption"
          color: "colors.text_secondary"
        position: "right"
        conditional: "visible when count > 0"

    states:
      default:
        description: "Inactive navigation item"
        visual_overrides: {}
      hover:
        description: "Mouse cursor over item"
        visual_overrides:
          background: "colors.surface_hover"
          color: "colors.text_primary"
          cursor: "pointer"
      active:
        description: "Currently selected page — brand accent with left border"
        visual_overrides:
          color: "colors.primary"
          background: "colors.primary_glow"
          border_left_color: "colors.primary"
          shadow: "inset 0 0 20px rgba(0,212,170,0.05)"
          font_weight: "600"
      focused:
        description: "Keyboard focus via Tab navigation"
        visual_overrides:
          outline: "none"
          ring: "2px colors.border_focus"
      disabled:
        description: "Coming soon / not available"
        visual_overrides:
          opacity: "0.4"
          cursor: "not-allowed"
          pointer_events: "none"

    data:
      props:
        - name: "icon"
          type: "ReactNode"
          required: true
          description: "SVG icon element rendered at 18x18"
        - name: "label"
          type: "string"
          required: true
          description: "Navigation label text"
        - name: "page"
          type: "string"
          required: true
          description: "Page identifier for routing"
        - name: "count"
          type: "number"
          required: false
          description: "Optional count badge value — hidden when 0 or undefined"
        - name: "active"
          type: "boolean"
          required: false
          default: "false"
          description: "Whether this is the currently active page"
        - name: "disabled"
          type: "boolean"
          required: false
          default: "false"
          description: "Whether item is disabled / coming soon"
        - name: "onClick"
          type: "(page: string) => void"
          required: true
          description: "Click handler — receives page identifier"
      events_emitted:
        - name: "onClick"
          trigger: "User clicks the nav item (not disabled)"
          payload:
            type: "string"
            description: "Page identifier from props"
          effect: "Navigate to the specified page"

    accessibility:
      role: "link"
      label: "Navigate to {label}"
      described_by: "null"
      keyboard:
        tab_order: "natural"
        key_handlers:
          - key: "Enter"
            action: "Navigate to page (fires onClick)"
          - key: "Space"
            action: "Navigate to page (fires onClick)"
      screen_reader:
        announcement: "{label}, {count} items"
        live_region: "off"
      contrast:
        text_ratio: "4.5:1"
        interactive_ratio: "3:1"

    # ── RECONSTRUCTION METADATA (RESEARCH-003 R3) ──────────────
    reconstruction:
      reference_viewport: "1280x800"
      expected_dimensions:
        width: "100%"
        height: "36px"
      visual_baseline: null
      bounding_box: null
      z_layer: "z_index.base"
```

**Why this is complete:**
- Description: 4 sentences covering purpose, content, states, and scale (170+ instances)
- Visual: 8 properties with token references throughout
- Content: 3 elements (icon, text, badge) with conditional visibility
- States: 5 states (default + 4 interactive) with rich visual overrides
- Data: 7 props (including boolean variant controls), 1 event — all with descriptions
- Accessibility: role, label, 2 keyboard handlers, screen reader announcement, contrast ratios
- Reconstruction: viewport, expected dimensions — enables fidelity verification (RESEARCH-003 R3)
- No internal_state section (correct for dumb classification)
