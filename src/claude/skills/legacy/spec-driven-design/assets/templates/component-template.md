# Component Specification Template

Fill in this template for EVERY component in the design.md component inventory.
Every field must be populated — blank or placeholder fields indicate the spec is incomplete.

Two examples of fully completed components are in `references/component-examples.md`.

---

```yaml
  - id: "${COMP-NNN}"
    name: "${ComponentName}"
    type: "${layout|form|display|navigation|dialog|feedback|data|composite}"
    classification: "${smart|dumb}"
    description: >
      ${2-3 sentences explaining what this component does, why it exists,
       what content it contains, and how users interact with it.}
    parent: "${COMP-NNN_OR_ROOT}"
    children: ["${COMP-NNN}", "${COMP-NNN}"]

    # ── VISUAL SPECIFICATION ──────────────────────────────────
    # Describe the component's visual appearance using token references.
    # Use Section 2 token names (e.g., "colors.surface"), not raw values.
    visual:
      dimensions:
        width: "${token ref or value with context — e.g., '100%', 'spacing.sidebar_width'}"
        height: "${token ref or value — e.g., 'spacing.topbar_height', 'auto'}"
      spacing:
        padding: "${token ref — e.g., 'spacing.lg' (24px)}"
        margin: "${token ref or description}"
        gap: "${token ref — gap between child elements}"
      appearance:
        background: "${token ref — e.g., 'colors.surface' for glass card}"
        backdrop_filter: "${blur value if glass effect — e.g., 'blur(20px)'}"
        border: "${composite — e.g., 'borders.width.default solid colors.border'}"
        border_radius: "${token ref — e.g., 'borders.radius.lg' (14px)}"
        shadow: "${token ref — e.g., 'shadows.card' with inset highlight}"
        overflow: "${visible|hidden|scroll|auto}"
        position: "${static|relative|fixed|sticky|absolute}"
        z_index: "${z_index token if positioned}"

    # ── CONTENT ELEMENTS ──────────────────────────────────────
    # Every visible element inside the component, ordered top-to-bottom.
    # Use token refs for style properties. At least 3 elements per component.
    content:
      - element: "${heading|text|icon|image|input|button|badge|list|table|chart|divider}"
        id: "${unique-element-id}"
        text: "${static text, dynamic pattern like '{{user.name}}', or null}"
        style:
          typography: "${token ref — e.g., 'typography.scale.h3'}"
          color: "${token ref — e.g., 'colors.text_primary'}"
        conditional: "${visibility condition or null}"
      - element: "${type}"
        id: "${id}"
        text: "${text}"
        style: { typography: "${ref}", color: "${ref}" }
      - element: "${type}"
        id: "${id}"
        text: "${text}"
        style: { typography: "${ref}", color: "${ref}" }

    # ── STATE MACHINE ─────────────────────────────────────────
    # Every visual state. Minimum: default + 2 interactive states.
    # Use token refs in overrides (not raw values).
    states:
      default:
        description: "${Normal resting appearance}"
        visual_overrides: {}
      hover:
        description: "${Mouse cursor over component}"
        visual_overrides:
          background: "${token ref — hover surface}"
          shadow: "${token ref — elevated shadow}"
          cursor: "pointer"
          transform: "${e.g., 'translateY(-2px)' for lift effect}"
      focused:
        description: "${Keyboard focus on component}"
        visual_overrides:
          outline: "none"
          ring: "${token ref — e.g., '2px colors.primary'}"
      disabled:
        description: "${Non-interactive state}"
        visual_overrides:
          opacity: "0.5"
          cursor: "not-allowed"
          pointer_events: "none"
      # Add loading, error, active, selected, expanded, collapsed as applicable

    # ── DATA CONTRACT ─────────────────────────────────────────
    # Required for ALL components (smart AND dumb).
    # Minimum 2 props. Include children if renders children.
    data:
      props:
        - name: "${propName}"
          type: "${string|number|boolean|ReactNode|function|enum values}"
          required: ${true|false}
          default: "${default value or null}"
          description: "${what this prop controls}"
        - name: "${propName}"
          type: "${type}"
          required: ${true|false}
          description: "${description}"
        # If component renders children: MUST include children prop
        # If component accepts className: MUST include className prop
        # If component has variant: MUST list all valid values as union type
      events_emitted:
        - name: "${onEventName}"
          trigger: "${user action that fires this event}"
          payload: { type: "${data shape}", description: "${what data}" }
          effect: "${what should happen in response}"
        # Every on* callback prop MUST also appear here
      internal_state:
        # For smart components only — omit for dumb components
        - name: "${stateName}"
          type: "${type}"
          initial_value: "${value}"
          description: "${what triggers changes}"
      data_dependencies:
        # For components that fetch/consume external data
        - source: "${API endpoint, Redux store path, or context}"
          type: "${rest|graphql|local_state|redux}"
          description: "${what data is consumed}"

    # ── ACCESSIBILITY ─────────────────────────────────────────
    # WCAG 2.1 AA compliance. Required for all components.
    accessibility:
      role: "${ARIA role — e.g., 'navigation', 'button', 'dialog', 'list'}"
      label: "${aria-label value for screen readers}"
      described_by: "${aria-describedby reference or null}"
      keyboard:
        tab_order: "${natural|explicit}"
        key_handlers:
          - key: "${key — e.g., 'Enter', 'Escape', 'ArrowDown'}"
            action: "${what happens when this key is pressed}"
      screen_reader:
        announcement: "${what is read aloud when focused}"
        live_region: "${off|polite|assertive}"
      contrast:
        text_ratio: "${minimum contrast ratio — e.g., '4.5:1'}"

    # ── RECONSTRUCTION METADATA ────────────────────────────────
    # Enables any AI to verify its implementation matches this spec.
    # SpecifyUI: 14.4% higher structural fidelity with explicit dimension
    # constraints (Source: arxiv.org/html/2509.07334v1).
    # Osmani: screenshots as first-class spec artifacts
    # (Source: addyosmani.com/blog/good-spec/).
    reconstruction:
      reference_viewport: "${viewport dimensions — e.g., '1280x800'}"
      expected_dimensions:
        width: "${measured or computed width at reference viewport — e.g., '240px', '100%'}"
        height: "${measured or computed height at reference viewport — e.g., '100vh', 'auto', '48px'}"
      visual_baseline: "${path to per-component screenshot or null}"
        # Example: "visual-capture/components/sidebar.png"
      bounding_box: { x: "${N}", y: "${N}", width: "${N}", height: "${N}" }
        # Pixel coordinates at reference viewport. Use null if not captured.
      z_layer: "${z_index token reference — e.g., 'z_index.base', 'z_index.modal'}"
```
