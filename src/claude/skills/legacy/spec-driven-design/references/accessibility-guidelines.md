# Enterprise Accessibility (a11y) Guidelines

**Purpose:** Enforce WCAG 2.1 AA compliance across all generated UI components regardless of UI type.
**Version:** 1.0
**Loaded by:** Phase 04, Step 4.4b
**Applies to:** All UI types (Web, GUI, Terminal)

---

Every generated component MUST adhere to these rules. Accessibility is not optional — it is a hard constraint enforced during code generation (Phase 05) and validated during specification validation (Phase 07).

## 1. Semantic HTML (Web UI)

Never use a `<div>` when a semantic element is appropriate:

| Instead of | Use |
|-----------|-----|
| `<div>` for clickable areas | `<button>` |
| `<div>` for navigation | `<nav>` |
| `<div>` for content sections | `<article>`, `<section>`, `<aside>` |
| `<div>` for page structure | `<header>`, `<main>`, `<footer>` |
| `<span>` for links | `<a>` |

## 2. Keyboard Navigation

All interactive elements must be fully keyboard-operable:

- All interactive elements must have a visible `:focus-visible` state (see design-system-rules.md Section 5 for focus ring tokens)
- Tab order must follow visual layout (no positive `tabindex` values)
- Modals and drawers must **trap focus** and close on `Escape`
- Dropdown menus must support arrow key navigation
- Custom components must implement appropriate keyboard patterns from WAI-ARIA Authoring Practices

## 3. ARIA Attributes

Use ARIA attributes when semantic HTML alone cannot convey the component's role or state:

- Use `aria-expanded` for accordions and dropdowns
- Use `aria-live="polite"` for dynamic content updates or error messages
- Use `aria-hidden="true"` on purely decorative icons
- Use `aria-label` or `aria-labelledby` for interactive elements without visible text labels
- Use `role` attributes only when no native HTML element provides the needed semantics

## 4. Color Contrast

Ensure minimum contrast ratios per WCAG 2.1 AA:

| Element | Minimum Ratio |
|---------|--------------|
| Normal text (< 18px) | 4.5:1 |
| Large text (≥ 18px bold or ≥ 24px) | 3:1 |
| UI components & graphical objects | 3:1 |
| Disabled elements | No minimum (but should be visually distinct) |

## 5. Form Accessibility

- Every form input must have an associated `<label>` (or `aria-label`)
- Error messages must be associated with their input via `aria-describedby`
- Required fields must use `aria-required="true"` (or the HTML `required` attribute)
- Form validation errors must be announced via `aria-live` region

## 6. GUI & Terminal Accessibility

**Desktop GUI (WPF, Tkinter):**
- Set `AutomationProperties.Name` (WPF) or equivalent for all interactive elements
- Support high contrast mode
- Respect system font size preferences

**Terminal UI:**
- Do not rely solely on color to convey meaning (use symbols: ✓, ✗, ⚠)
- Support screen reader compatibility where possible
- Provide text alternatives for box-drawing characters when conveying data

## 7. Verification Checklist

During Phase 07 (Specification Validation), verify:

- [ ] All interactive elements have visible focus states
- [ ] All images/icons have alt text or aria-hidden
- [ ] All forms have associated labels
- [ ] Color is not the sole means of conveying information
- [ ] Keyboard-only navigation works for all interactions
- [ ] ARIA attributes are used correctly (no redundant roles on semantic elements)
