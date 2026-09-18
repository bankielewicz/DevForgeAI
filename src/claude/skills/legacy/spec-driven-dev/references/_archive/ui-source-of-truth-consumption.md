# UI Design Source of Truth Consumption

**Purpose:** Guide the dev workflow to detect, load, and use design.md during implementation phases.
**Version:** 1.0
**Loaded by:** Phase 01 (Pre-Flight), referenced during Phase 03 (Green/Implementation)

---

## Detection

During Phase 01 (Pre-Flight Validation), after story file is loaded:

```
# Check for Design Source of Truth
design_doc = Glob(pattern="devforgeai/specs/ui/design.md")

IF design_doc found:
  Read(file_path="devforgeai/specs/ui/design.md")

  # Parse key metadata
  session.design_source_of_truth = {
    available: true,
    path: "devforgeai/specs/ui/design.md",
    aesthetic_vibe: extract design_intent.aesthetic_vibe,
    color_mode: extract design_intent.color_mode,
    component_count: count COMP-NNN entries,
    framework_agnostic: true  # design.md is always framework-agnostic
  }

  # Extract components relevant to THIS story
  # Match by: story AC references, component names in story UI spec section
  session.story_ui_components = []
  FOR each component in design.md.components:
    IF component.id mentioned in story file UI Specification section:
      session.story_ui_components.append(component)

  # Extract design tokens for subagent context
  session.design_tokens_summary = {
    colors: extract tokens.colors (primary, background, surface, text, error, success),
    spacing_unit: extract tokens.spacing.unit,
    font_primary: extract tokens.typography.font_family.primary,
    border_radius_default: extract tokens.borders.radius.md,
    motion_duration: extract tokens.motion.duration.normal
  }

  Display: "Design Source of Truth loaded for implementation guidance"
  Display: "  Components relevant to this story: {len(session.story_ui_components)}"

  # Check for visual capture screenshots (from --url extraction)
  screenshots = Glob(pattern="devforgeai/specs/ui/visual-capture/desktop.png")
  IF screenshots found:
    session.visual_capture = {
      available: true,
      desktop: "devforgeai/specs/ui/visual-capture/desktop.png",
      tablet: "devforgeai/specs/ui/visual-capture/tablet.png",
      mobile: "devforgeai/specs/ui/visual-capture/mobile.png"
    }
    Display: "  Visual capture screenshots available (3 viewports)"
  ELSE:
    session.visual_capture = { available: false }

ELSE:
  session.design_source_of_truth = { available: false }
  session.visual_capture = { available: false }
  # No design.md — proceed normally using story UI spec section only
```

---

## Usage During Phase 03 (Green/Implementation)

When delegating to frontend-developer or backend-architect subagent:

```
IF session.design_source_of_truth.available == true:

  # Include design.md context in subagent prompt
  APPEND to task prompt:
    """
    UI Design Source of Truth is available at: devforgeai/specs/ui/design.md

    For UI components in this story, implement EXACTLY per the design specification:

    Design Tokens (use these values, do not invent):
    - Primary Color: ${session.design_tokens_summary.colors.primary}
    - Background: ${session.design_tokens_summary.colors.background}
    - Font Family: ${session.design_tokens_summary.font_primary}
    - Spacing Unit: ${session.design_tokens_summary.spacing_unit}
    - Border Radius: ${session.design_tokens_summary.border_radius_default}
    - Animation Duration: ${session.design_tokens_summary.motion_duration}

    Components to implement:
    ${FOR each comp in session.story_ui_components:
      - ${comp.id}: ${comp.name} (${comp.type}, ${comp.classification})
        Props: ${comp.data.props}
        States: ${comp.states keys}
        Accessibility: role=${comp.accessibility.role}, label=${comp.accessibility.label}
    }

    IMPORTANT:
    - Use design tokens from design.md, not arbitrary values
    - Implement ALL states (default, hover, focused, disabled, loading, error)
    - Include ALL accessibility attributes (ARIA roles, labels, keyboard handlers)
    - Match interaction flows from design.md Section 5
    - Apply animations from design.md Section 6
    """

  # Include visual target screenshots if available
  IF session.visual_capture.available == true:
    APPEND to task prompt:
      """
      TARGET SCREENSHOTS available — this is what the implemented UI should look like:
      Read the screenshot at: devforgeai/specs/ui/visual-capture/desktop.png
      (Claude is multimodal and can analyze this image)

      Match the visual layout, colors, spacing, and typography visible in the screenshot.
      Additional viewports at: tablet.png (768px), mobile.png (375px)
      """
```

---

## Fallback Behavior

When design.md is NOT available:
- Dev workflow proceeds normally using story file's UI Specification section
- ASCII mockups and text descriptions guide implementation
- No design token enforcement (developer chooses values)
- This is backward-compatible — no existing workflow breaks

---

## Cross-Reference with QA

When QA validates against design.md:
- QA checks that implemented component names match design.md inventory
- QA verifies props interfaces match design.md data contracts
- QA validates accessibility attributes match design.md specs
- QA checks design token usage in implemented code

This ensures end-to-end fidelity: design.md (source of truth) → dev (implementation) → QA (validation).
