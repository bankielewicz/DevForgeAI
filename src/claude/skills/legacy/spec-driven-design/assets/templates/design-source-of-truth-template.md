# UI Design Source of Truth

<!--
  PURPOSE: Framework-agnostic UI specification that enables ANY AI to recreate
  this UI from scratch in any technology (React, Vue, WPF, HTML/CSS, etc.)

  PRODUCED BY: spec-driven-design skill (Phase 06 or extract mode)
  CONSUMED BY: spec-driven-ideation (ui_design_context), spec-driven-stories (Phase 04),
               spec-driven-dev (Phase 01/03), spec-driven-qa (validation),
               External AI (Google Stitch, ChatGPT, etc.)

  SCHEMA VERSION: 1.1
  TEMPLATE VERSION: 1.1

  INSTRUCTIONS FOR AI CONSUMERS:
  - This document is the SINGLE SOURCE OF TRUTH for the UI design
  - Recreate the UI by implementing each section in order
  - Design tokens define the visual language — use them, do not invent values
  - Component inventory defines WHAT to build — implement every component
  - Layouts define WHERE components go — follow the spatial arrangement
  - Interactions define HOW components behave — implement every flow
  - Animations define MOTION — apply every specified transition
  - Accessibility defines INCLUSIVITY — every requirement is mandatory
-->

```yaml
---
# ============================================================
# SECTION 1: DOCUMENT METADATA
# ============================================================
schema_version: "1.1"
document_type: "ui-design-source-of-truth"
project: "${PROJECT_NAME}"
created: "${CREATED_DATE}"
updated: "${UPDATED_DATE}"
source_skill: "spec-driven-design"
source_mode: "${generated|extracted|hybrid}"
mode: "${story|standalone|extract}"
platform: "${web|gui|tui}"
story_id: "${STORY_ID_OR_NULL}"
epic_id: "${EPIC_ID_OR_NULL}"

# ============================================================
# SECTION 2: DESIGN INTENT
# What is the overall visual and experiential goal?
# ============================================================
design_intent:
  aesthetic_vibe: "${AESTHETIC_VIBE}"
  # Examples: "Sleek Dark FinTech", "Flat Clean Enterprise",
  #           "Glassmorphism SaaS", "Soft Minimal Productivity"
  color_mode: "${dark|light|system-adaptive}"
  design_philosophy: "${DESIGN_PHILOSOPHY}"
  # Examples: "minimal", "skeuomorphic", "flat", "glassmorphism",
  #           "neumorphism", "material", "brutalist"
  target_platforms:
    - "${web-desktop}"
    - "${web-mobile}"
    - "${web-tablet}"
    # Other options: "desktop-windows", "desktop-macos", "terminal"
  brand_identity:
    name: "${BRAND_NAME_OR_NULL}"
    personality: "${BRAND_PERSONALITY}"
    # Examples: "Professional and trustworthy", "Playful and energetic"
    logo_placement: "${LOGO_PLACEMENT_OR_NULL}"

# ============================================================
# SECTION 3: DESIGN TOKEN CATALOG
# Every visual value used in the UI — no arbitrary values allowed.
# AI consumers: Use ONLY these tokens. Never invent values.
# ============================================================
tokens:

  # --- Color Palette ---
  colors:
    # Backgrounds & Surfaces
    background:
      value: "${HEX_VALUE}"
      usage: "App base layer / page background"
    surface:
      value: "${HEX_VALUE}"
      usage: "Cards, panels, modals — elevated from background"
    surface_muted:
      value: "${HEX_VALUE}"
      usage: "Secondary containers, empty states"
    surface_hover:
      value: "${HEX_VALUE}"
      usage: "Interactive surface hover state"

    # Text
    text_primary:
      value: "${HEX_VALUE}"
      usage: "Headings, high-emphasis text"
    text_secondary:
      value: "${HEX_VALUE}"
      usage: "Body copy, captions, placeholders"
    text_disabled:
      value: "${HEX_VALUE}"
      usage: "Disabled inputs, inactive labels"
    text_inverse:
      value: "${HEX_VALUE}"
      usage: "Text on primary-colored backgrounds"

    # Brand & Interactive
    primary:
      value: "${HEX_VALUE}"
      usage: "CTA buttons, active tabs, focus rings, links"
    primary_hover:
      value: "${HEX_VALUE}"
      usage: "Primary interactive hover state"
    secondary:
      value: "${HEX_VALUE}"
      usage: "Secondary actions, toggles"

    # Status
    success:
      value: "${HEX_VALUE}"
      usage: "Positive trends, successful operations, confirmations"
    error:
      value: "${HEX_VALUE}"
      usage: "Errors, destructive actions, validation failures"
    warning:
      value: "${HEX_VALUE}"
      usage: "Cautionary states, pending actions"
    info:
      value: "${HEX_VALUE}"
      usage: "Informational callouts, tips"

    # Borders & Dividers
    border:
      value: "${HEX_VALUE}"
      usage: "Card borders, input outlines, dividers"
    border_focus:
      value: "${HEX_VALUE}"
      usage: "Focus ring color for interactive elements"

  # --- Spacing (8-Point Grid) ---
  spacing:
    unit: "8px"
    scale:
      xs: { value: "4px", usage: "Micro adjustments, icon gaps" }
      sm: { value: "8px", usage: "Tight gaps, inner button padding" }
      md: { value: "16px", usage: "Standard component padding" }
      lg: { value: "24px", usage: "Standard section gaps" }
      xl: { value: "32px", usage: "Loose container padding" }
      xxl: { value: "48px", usage: "Major section spacing" }
      xxxl: { value: "64px", usage: "Page-level spacing" }

  # --- Typography ---
  typography:
    font_family:
      primary: "${FONT_NAME}"
      # Example: "Inter, system-ui, -apple-system, sans-serif"
      mono: "${MONO_FONT_NAME}"
      # Example: "JetBrains Mono, Fira Code, monospace"
    scale:
      display:
        size: "${SIZE}"
        weight: ${WEIGHT}
        line_height: ${LINE_HEIGHT}
        letter_spacing: "${LETTER_SPACING_OR_NORMAL}"
        usage: "Page titles, hero metrics, dashboard headlines"
      h1:
        size: "${SIZE}"
        weight: ${WEIGHT}
        line_height: ${LINE_HEIGHT}
        usage: "Section titles, modal headers"
      h2:
        size: "${SIZE}"
        weight: ${WEIGHT}
        line_height: ${LINE_HEIGHT}
        usage: "Subsection titles, card headers"
      h3:
        size: "${SIZE}"
        weight: ${WEIGHT}
        line_height: ${LINE_HEIGHT}
        usage: "Group labels, sidebar sections"
      body:
        size: "${SIZE}"
        weight: ${WEIGHT}
        line_height: ${LINE_HEIGHT}
        usage: "Standard paragraph text, form inputs"
      body_small:
        size: "${SIZE}"
        weight: ${WEIGHT}
        line_height: ${LINE_HEIGHT}
        usage: "Secondary text, help text"
      caption:
        size: "${SIZE}"
        weight: ${WEIGHT}
        line_height: ${LINE_HEIGHT}
        usage: "Labels, tags, timestamps, metadata"
      code:
        size: "${SIZE}"
        weight: ${WEIGHT}
        line_height: ${LINE_HEIGHT}
        font_family: "${MONO_FONT}"
        usage: "Code blocks, inline code, technical values"

  # --- Borders & Corners ---
  borders:
    radius:
      none: "0px"
      sm: "${VALUE}"
      md: "${VALUE}"
      lg: "${VALUE}"
      xl: "${VALUE}"
      full: "9999px"
    width:
      default: "1px"
      thick: "2px"

  # --- Elevation & Shadows ---
  shadows:
    none: "none"
    sm:
      value: "${CSS_SHADOW_VALUE}"
      usage: "Resting cards, dropdowns"
    md:
      value: "${CSS_SHADOW_VALUE}"
      usage: "Hover states, active cards"
    lg:
      value: "${CSS_SHADOW_VALUE}"
      usage: "Modals, popovers, drawers"
    xl:
      value: "${CSS_SHADOW_VALUE}"
      usage: "Overlays, floating elements"

  # --- Motion & Animation ---
  motion:
    duration:
      instant: "0ms"
      fast: "150ms"
      normal: "200ms"
      slow: "300ms"
      deliberate: "500ms"
    easing:
      default: "ease-in-out"
      enter: "ease-out"
      exit: "ease-in"
      spring: "cubic-bezier(0.34, 1.56, 0.64, 1)"
    transitions:
      default: "all ${motion.duration.normal} ${motion.easing.default}"
      hover: "all ${motion.duration.fast} ${motion.easing.default}"
      page: "opacity ${motion.duration.slow} ${motion.easing.enter}"

  # --- Responsive Breakpoints ---
  responsive:
    breakpoints:
      mobile: { max_width: "639px", columns: 4, gutter: "16px" }
      tablet: { min_width: "640px", max_width: "1023px", columns: 8, gutter: "24px" }
      desktop: { min_width: "1024px", max_width: "1279px", columns: 12, gutter: "24px" }
      wide: { min_width: "1280px", columns: 12, gutter: "32px" }
    container:
      max_width: "${MAX_WIDTH}"
      padding: "${PADDING}"

  # --- Z-Index Scale ---
  z_index:
    base: 0
    dropdown: 100
    sticky: 200
    overlay: 300
    modal: 400
    popover: 500
    toast: 600
    tooltip: 700

# ============================================================
# SECTION 4: COMPONENT INVENTORY
# Every UI component in the design — framework-agnostic.
# AI consumers: Implement ALL components listed here.
# ============================================================
components:
  # --- Component Entry Template ---
  # Copy this block for each component in the design.
  - id: "${COMP-NNN}"
    name: "${ComponentName}"
    type: "${layout|form|display|navigation|dialog|feedback|data|composite}"
    classification: "${smart|dumb}"
    description: >
      ${WHAT_THIS_COMPONENT_DOES_AND_WHY_IT_EXISTS}
    parent: "${COMP-NNN_OR_ROOT}"
    children: ["${COMP-NNN}", "${COMP-NNN}"]

    # --- Visual Specification ---
    # TOKEN RULE: ALL color, spacing, border, shadow, and motion values
    # MUST use token references from Section 2 (e.g., "colors.surface",
    # "spacing.md", "borders.radius.lg"). Raw hex/rgba/px values are
    # PROHIBITED when a matching token exists. This applies to EVERY
    # visual property in this section, in states.visual_overrides,
    # in content[].style, and in variants.
    visual:
      dimensions:
        width: "${auto|100%|fixed_value|min-max_range}"
        height: "${auto|fixed_value|min-max_range}"
        min_width: "${VALUE_OR_NULL}"
        min_height: "${VALUE_OR_NULL}"
        max_width: "${VALUE_OR_NULL}"
        max_height: "${VALUE_OR_NULL}"
      spacing:
        padding: "${TOKEN_REF}"
        # MUST be token: "spacing.md", "spacing.lg", etc. NOT "16px"
        margin: "${TOKEN_REF}"
        gap: "${TOKEN_REF}"
      appearance:
        background: "${TOKEN_REF}"
        # MUST be token: "colors.surface", NOT "rgba(15, 23, 42, 0.6)"
        border: "${TOKEN_REF_COMPOSITE}"
        # MUST use tokens: "borders.width.default solid colors.border"
        # NOT "1px solid rgba(255,255,255,0.08)"
        border_radius: "${TOKEN_REF}"
        # MUST be token: "borders.radius.lg", NOT "14px"
        shadow: "${TOKEN_REF}"
        # MUST be token: "shadows.sm", NOT the raw CSS value
        overflow: "${visible|hidden|scroll|auto}"
        opacity: "${0.0-1.0}"

    # --- Content Elements ---
    # Ordered list of elements inside this component, top to bottom.
    # TOKEN RULE APPLIES HERE: style.typography and style.color MUST use tokens.
    content:
      - element: "${heading|text|icon|image|input|button|select|checkbox|radio|toggle|list|table|chart|divider|badge|avatar|skeleton}"
        id: "${ELEMENT_ID}"
        text: "${STATIC_TEXT_OR_PATTERN}"
        # For dynamic content: "{{user.name}}" or "${placeholder description}"
        style:
          typography: "${TOKEN_REF}"
          # MUST be token: "typography.scale.caption", NOT "12px uppercase 700"
          color: "${TOKEN_REF}"
          # MUST be token: "colors.text_secondary", NOT "#8899aa"
        position: "${ORDER_IN_LAYOUT}"
        conditional: "${CONDITION_OR_NULL}"
        # Example: "visible when isLoading === false"

    # --- State Machine ---
    # Every visual state this component can be in.
    # TOKEN RULE APPLIES HERE TOO: All visual_overrides values
    # MUST use token references where a matching token exists.
    states:
      default:
        description: "Normal resting state"
        visual_overrides: {}
      hover:
        description: "Mouse cursor over component"
        visual_overrides:
          background: "${TOKEN_REF}"
          # MUST be token: "colors.surface_hover", NOT "rgba(255,255,255,0.05)"
          shadow: "${TOKEN_REF}"
          cursor: "pointer"
          transform: "${TRANSFORM_OR_NULL}"
      active:
        description: "Being clicked/pressed"
        visual_overrides:
          transform: "scale(0.98)"
          shadow: "${TOKEN_REF}"
      focused:
        description: "Keyboard focus on component"
        visual_overrides:
          outline: "none"
          ring: "2px ${colors.border_focus}"
      disabled:
        description: "Component is non-interactive"
        visual_overrides:
          opacity: "0.5"
          cursor: "not-allowed"
          pointer_events: "none"
      loading:
        description: "Data is being fetched/processed"
        visual_overrides:
          content: "skeleton|spinner|shimmer"
          pointer_events: "none"
          aria_busy: "true"
      error:
        description: "Validation failure or error state"
        visual_overrides:
          border_color: "${colors.error}"
          # Additional error-specific overrides
      # Add custom states as needed:
      # selected:
      # expanded:
      # collapsed:

    # --- Data Contract ---
    # REQUIRED for ALL components (smart AND dumb).
    # Dumb components still have props — document them.
    # Smart components additionally have internal_state and data_dependencies.
    data:
      props:
        # MANDATORY PROPS (include if component uses them):
        # - children: MUST include if component renders {children} or {props.children}
        # - className: MUST include if component accepts className for style customization
        # - Every callback prop (on*): MUST appear here AND in events_emitted
        # - Every variant/enum prop: MUST list all valid values as union type
        #
        # COMPLETENESS RULE: An AI reading this props list must be able to
        # instantiate the component with zero ambiguity. If a prop exists in
        # the source code, it MUST exist here.
        - name: "${propName}"
          type: "${string|number|boolean|string[]|object|ReactNode|function}"
          required: ${true|false}
          default: "${DEFAULT_VALUE_OR_NULL}"
          description: "${WHAT_THIS_PROP_CONTROLS}"
          validation: "${VALIDATION_RULE_OR_NULL}"
          # Example: "min: 0, max: 100" or "pattern: email"
      internal_state:
        # For smart components only. Omit section entirely for dumb components.
        - name: "${stateName}"
          type: "${TYPE}"
          initial_value: "${VALUE}"
          description: "${WHAT_TRIGGERS_CHANGES}"
          persistence: "${none|session|local|server}"
      events_emitted:
        # EVERY callback prop (on*) from props MUST also appear here.
        # This is the behavioral contract — what the component DOES in response.
        # COMPLETENESS RULE: If a callback prop exists in props but NOT here,
        # the specification is incomplete.
        - name: "${onEventName}"
          trigger: "${USER_ACTION_OR_CONDITION}"
          payload:
            type: "${TYPE_SHAPE}"
            description: "${WHAT_DATA_IS_SENT}"
          effect: "${WHAT_SHOULD_HAPPEN_IN_RESPONSE}"
      data_dependencies:
        # For smart components with external data. Omit for dumb components.
        - source: "${API_ENDPOINT_OR_STORE_PATH}"
          type: "${rest|graphql|websocket|local_state}"
          description: "${WHAT_DATA_IS_FETCHED}"
          refresh: "${on_mount|on_interval|on_event}"
          error_handling: "${HOW_ERRORS_ARE_DISPLAYED}"

    # --- Accessibility ---
    accessibility:
      role: "${ARIA_ROLE}"
      # Examples: "button", "navigation", "dialog", "form", "list", "table"
      label: "${ARIA_LABEL_VALUE}"
      described_by: "${ARIA_DESCRIBEDBY_OR_NULL}"
      keyboard:
        tab_order: "${natural|explicit_order}"
        key_handlers:
          - key: "${KEY}"
            action: "${WHAT_HAPPENS}"
          # Example: { key: "Escape", action: "Close modal" }
          # Example: { key: "Enter", action: "Submit form" }
      screen_reader:
        announcement: "${WHAT_IS_READ_ALOUD}"
        live_region: "${off|polite|assertive}"
      contrast:
        text_ratio: "${RATIO}"
        # Minimum: "4.5:1" for WCAG AA
        interactive_ratio: "${RATIO}"
        # Minimum: "3:1" for interactive elements

    # --- Reconstruction Metadata ---
    # Enables any AI to verify its implementation matches this spec.
    # SpecifyUI: 14.4% higher structural fidelity with explicit dimension
    # constraints (arxiv.org/html/2509.07334v1).
    # Osmani: screenshots as first-class spec artifacts
    # (addyosmani.com/blog/good-spec/).
    reconstruction:
      reference_viewport: "${VIEWPORT — e.g., '1280x800'}"
      expected_dimensions:
        width: "${MEASURED_WIDTH — e.g., '240px', '100%'}"
        height: "${MEASURED_HEIGHT — e.g., '100vh', 'auto', '48px'}"
      visual_baseline: "${SCREENSHOT_PATH_OR_NULL}"
        # Example: "visual-capture/components/sidebar.png"
      bounding_box: { x: ${X}, y: ${Y}, width: ${W}, height: ${H} }
        # Pixel coordinates at reference viewport. Null if not captured.
      z_layer: "${Z_INDEX_TOKEN — e.g., 'z_index.base', 'z_index.modal'}"

# ============================================================
# SECTION 5: LAYOUT SPECIFICATION
# Page/screen-level spatial arrangement of components.
# AI consumers: Build pages matching these layouts exactly.
# ============================================================
layouts:
  - id: "${LAYOUT-NNN}"
    name: "${PageOrScreenName}"
    route: "${/PATH_OR_NULL}"
    description: >
      ${WHAT_THIS_PAGE_SHOWS_AND_ITS_PURPOSE}
    grid:
      type: "${flex|grid|absolute}"
      columns: "${COLUMN_COUNT_OR_DESCRIPTION}"
      rows: "${ROW_DESCRIPTION_OR_AUTO}"
      gap: "${TOKEN_REF}"

    # --- Layout Regions ---
    # Ordered spatial regions on this page.
    regions:
      - name: "${REGION_NAME}"
        # Examples: "header", "sidebar", "main", "footer", "toolbar"
        components: ["${COMP-NNN}", "${COMP-NNN}"]
        dimensions:
          width: "${VALUE}"
          height: "${VALUE}"
        position: "${fixed|sticky|static|relative|absolute}"
        order: ${VISUAL_ORDER}
        visibility:
          mobile: "${visible|hidden|collapsed}"
          tablet: "${visible|hidden|collapsed}"
          desktop: "${visible|hidden|collapsed}"

    # --- Responsive Behavior ---
    responsive:
      mobile:
        layout_changes: >
          ${HOW_LAYOUT_REORGANIZES_AT_MOBILE}
        # Example: "Sidebar collapses to hamburger menu.
        #           Main content becomes full-width. Cards stack vertically."
        hidden_regions: ["${REGION_NAME}"]
        stacked_regions: ["${REGION_NAME}", "${REGION_NAME}"]
      tablet:
        layout_changes: >
          ${HOW_LAYOUT_REORGANIZES_AT_TABLET}
        hidden_regions: []
        stacked_regions: []

    # --- ASCII Layout Diagram ---
    ascii_layout: |
      ${ASCII_REPRESENTATION_OF_PAGE_LAYOUT}
      # Example:
      # +----------------------------------------------------------+
      # | HEADER [COMP-001]                                        |
      # +----------------------------------------------------------+
      # | SIDEBAR    | MAIN CONTENT                                |
      # | [COMP-002] | [COMP-003] [COMP-004]                      |
      # |            | [COMP-005]                                  |
      # +----------------------------------------------------------+
      # | FOOTER [COMP-006]                                        |
      # +----------------------------------------------------------+

# ============================================================
# SECTION 6: INTERACTION FLOWS
# Step-by-step behavioral sequences — how the UI responds.
# AI consumers: Implement every flow exactly as specified.
#
# COMPLETENESS RULE: Every callback prop (on*) from Section 3
# components MUST be covered by at least one FLOW entry.
# Single-action callbacks (onChange, onRowClick, onClose) count
# as flows too — document them. Do NOT skip "simple" interactions.
#
# CATEGORIES (include at least one flow per category if applicable):
#   - Navigation flows (route changes, tab switches, back navigation)
#   - State toggle flows (sidebar collapse, panel open/close, edit mode)
#   - Selection/filter flows (chip selection, row click, persona switch)
#   - CRUD/form flows (add, remove, reorder, submit)
#   - Responsive/layout flows (mobile hamburger, breakpoint behavior)
#   - Error/recovery flows (validation, empty state, retry)
# ============================================================
interactions:
  - id: "${FLOW-NNN}"
    name: "${FlowName}"
    description: >
      ${WHAT_THIS_FLOW_ACCOMPLISHES}
    trigger: "${WHAT_INITIATES_THIS_FLOW}"
    # Example: "User clicks 'Submit' button on login form"
    preconditions:
      - "${CONDITION_THAT_MUST_BE_TRUE}"
      # Example: "User is on login page, form fields are not empty"

    # --- Flow Steps ---
    steps:
      - step: ${N}
        user_action: "${WHAT_THE_USER_DOES}"
        system_response: "${WHAT_THE_UI_DOES}"
        component: "${COMP-NNN}"
        state_changes:
          - component: "${COMP-NNN}"
            from_state: "${STATE_NAME}"
            to_state: "${STATE_NAME}"
        visual_feedback: "${WHAT_THE_USER_SEES}"
        duration: "${DURATION_OR_INSTANT}"
        # Example: "motion.duration.normal"

    # --- Error Paths ---
    error_handling:
      - error: "${WHAT_CAN_GO_WRONG}"
        display: "${HOW_ERROR_IS_SHOWN}"
        # Example: "Red border on input + error message below field"
        recovery: "${HOW_USER_RECOVERS}"
        # Example: "User corrects input, error clears on keystroke"
        component: "${COMP-NNN}"

    # --- Success State ---
    success_state:
      description: "${FINAL_STATE_AFTER_SUCCESSFUL_FLOW}"
      navigation: "${WHERE_USER_GOES_NEXT_OR_NULL}"
      feedback: "${SUCCESS_FEEDBACK_SHOWN}"

# ============================================================
# SECTION 7: ANIMATION & TRANSITION SPECIFICATION
# Motion design — how elements move, appear, and disappear.
# AI consumers: Apply every animation as specified.
# ============================================================
animations:
  - id: "${ANIM-NNN}"
    name: "${AnimationName}"
    trigger: "${mount|unmount|hover|click|scroll|state_change|route_change}"
    target: "${COMP-NNN_OR_ELEMENT_ID}"
    description: >
      ${HUMAN_READABLE_DESCRIPTION_OF_WHAT_THE_ANIMATION_LOOKS_LIKE}
    properties:
      - property: "${CSS_PROPERTY}"
        from: "${START_VALUE}"
        to: "${END_VALUE}"
    duration: "${TOKEN_REF}"
    # Example: "motion.duration.normal"
    easing: "${TOKEN_REF}"
    # Example: "motion.easing.spring"
    delay: "${DURATION_OR_0}"
    iteration: "${1|infinite}"
    direction: "${normal|reverse|alternate}"

  # --- Page Transition ---
  # (Optional) How pages/routes transition.
  page_transitions:
    enter:
      animation: "${ANIM-NNN_OR_DESCRIPTION}"
    exit:
      animation: "${ANIM-NNN_OR_DESCRIPTION}"

# ============================================================
# SECTION 8: GLOBAL ACCESSIBILITY REQUIREMENTS
# Applies to ALL components unless overridden.
# AI consumers: These are MANDATORY, not optional.
# ============================================================
accessibility:
  wcag_level: "AA"
  # Minimum: "AA". Can be "AAA" for stricter compliance.
  color_contrast:
    text_minimum: "4.5:1"
    large_text_minimum: "3:1"
    interactive_minimum: "3:1"
  keyboard_navigation:
    all_interactive_focusable: true
    visible_focus_indicator: true
    focus_trap_in_modals: true
    skip_to_content_link: true
    logical_tab_order: true
  screen_reader:
    all_images_have_alt: true
    form_labels_associated: true
    error_messages_announced: true
    dynamic_content_aria_live: true
    heading_hierarchy_logical: true
  motion:
    respects_prefers_reduced_motion: true
    no_auto_play_animations: true
    pause_mechanism_for_moving_content: true
  touch:
    minimum_target_size: "44px"
    adequate_spacing_between_targets: true

# ============================================================
# SECTION 9: DATA & API CONTEXT
# What backend data the UI depends on.
# AI consumers: Use this to understand data shapes and mock data.
# ============================================================
data_context:
  api_endpoints:
    - path: "${/api/endpoint}"
      method: "${GET|POST|PUT|PATCH|DELETE}"
      description: "${WHAT_THIS_ENDPOINT_PROVIDES}"
      request_shape: "${TYPE_DESCRIPTION_OR_NULL}"
      response_shape: "${TYPE_DESCRIPTION}"
      used_by: ["${COMP-NNN}"]
      error_codes: ["${STATUS_CODE}: ${MEANING}"]

  global_state:
    - name: "${STATE_SLICE_NAME}"
      description: "${WHAT_THIS_STATE_REPRESENTS}"
      shape: "${TYPE_DESCRIPTION}"
      persistence: "${none|session|local|server}"
      used_by: ["${COMP-NNN}"]

  mock_data:
    description: >
      ${GUIDANCE_FOR_GENERATING_REALISTIC_MOCK_DATA}
    examples:
      - entity: "${ENTITY_NAME}"
        sample: "${JSON_OR_DESCRIPTION_OF_SAMPLE_DATA}"

# ============================================================
# SECTION 10: DESIGN REVIEW
# Required only for generated web story/standalone invocations.
# GUI, TUI, and extract documents omit this entire group.
# Phase 07 replaces pending values with validated review evidence.
# ============================================================
design_review:
  status: "${pending|gate_passed|below_threshold}"
  review_path: "${devforgeai/specs/ui/design-review.json}"
  selected_round: ${SELECTED_ROUND_OR_NULL}
  composite: ${COMPOSITE_OR_NULL}
  lint:
    report_path: "${LINT_REPORT_PATH}"
    report_sha256: "${LINT_REPORT_SHA256}"
    p0: ${P0_COUNT}
    p1: ${P1_COUNT}
    p2: ${P2_COUNT}
  render:
    manifest_path: "${RENDER_MANIFEST_PATH}"
    manifest_sha256: "${RENDER_MANIFEST_SHA256}"
    desktop_path: "${DESKTOP_SCREENSHOT_PATH}"
    mobile_path: "${MOBILE_SCREENSHOT_PATH}"
  remaining_must_fix:
    - "${MUST_FIX_OR_EMPTY_LIST}"

---
```

<!-- END OF YAML FRONTMATTER — Markdown body follows -->

## Document Guide

This document is the **single source of truth** for the UI design of **${PROJECT_NAME}**.

### How to Use This Document

1. **To recreate the UI from scratch**: Read Sections 1-9 sequentially. Implement tokens first, then components, then layouts, then interactions, then animations.
2. **To implement a specific component**: Find it by ID in Section 3 (Component Inventory). Check its parent/children for context. Check Section 5 for interaction flows it participates in.
3. **To validate an implementation**: Compare your implementation against each section. Every token value, component, state, and interaction must match.
4. **To update the design**: Edit the relevant YAML section. Update the `updated` date in metadata. Downstream skills will consume the changes.

### Section Quick Reference

| Section | Contains | Used For |
|---------|----------|----------|
| 1. Document Metadata | Schema, invocation mode, platform, lineage | Determining applicability |
| 2. Design Intent | Aesthetic direction, platforms, brand | Setting the visual tone |
| 3. Design Tokens | Colors, spacing, typography, motion | Every visual value |
| 4. Component Inventory | Every UI component with full specs | Building components |
| 5. Layout Specification | Page/screen arrangements | Assembling pages |
| 6. Interaction Flows | Step-by-step behavioral sequences | Implementing behavior |
| 7. Animations | Motion specifications | Adding transitions |
| 8. Accessibility | Global a11y requirements | Ensuring inclusivity |
| 9. Data Context | API endpoints, state, mock data | Understanding data flow |
| 10. Design Review | Deterministic lint, render, jury, and remaining gaps | Assessing generated web quality |

### Validation Checklist

Before this document is considered complete, verify:

- [ ] All color tokens have hex values (no placeholders)
- [ ] All spacing values align to the 8-point grid
- [ ] Every component has: visual, states, data, accessibility sections
- [ ] Every component data.props includes children (if renders children) and className (if accepts it)
- [ ] Every callback prop (on*) in data.props also appears in data.events_emitted
- [ ] Every callback prop across all components is covered by at least one FLOW-NNN
- [ ] Every layout has: regions, responsive behavior, ASCII diagram
- [ ] Every interaction flow has: steps, error handling, success state
- [ ] All COMP-IDs in component.children[] exist in the component inventory
- [ ] All COMP-IDs referenced in layouts exist in component inventory
- [ ] All COMP-IDs referenced in interactions exist in component inventory
- [ ] All parent references are "root" or a valid COMP-ID
- [ ] All ANIM-IDs reference valid targets
- [ ] **Token normalization ≥ 70%** (**CRITICAL gate — RESEARCH-003 R2**): Component visual values MUST use token refs (e.g., "colors.surface") NOT raw values (e.g., "rgba(15,23,42,0.6)") — raw values prohibited when a matching token exists. Hard fail below 70%. (SpecifyUI: 14.4% higher structural fidelity; Pandya: CSS variable audit prevents LLM hallucination)
- [ ] Accessibility section has no "null" or placeholder values
- [ ] No "${...}" template variables remain (all populated)
- [ ] Search/command flow exists if search input is present (even if placeholder-only)
