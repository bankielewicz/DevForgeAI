# Enterprise Design System Rules (The Stitch Standard)

**Purpose:** Enforce consistent spatial, color, typography, and motion standards across all generated UI components.
**Version:** 1.0
**Loaded by:** Phase 04, Step 4.4a
**Applies to:** Web UI, Desktop GUI (skip for Terminal UI)

---

This document is the source of truth for all UI generation. Never use arbitrary values (e.g., `margin-top: 15px` or `text-[#4287f5]`). Every value must map to the semantic tokens and spatial rules defined below.

## 1. The Spatial System (8-Point Grid)

Strict adherence to the 8-point grid is mandatory. All spatial values (padding, margin, gap, width, height) must be multiples of 4 or 8.

* **Base Unit:** 8px (0.5rem in Tailwind)
* **Scale Mapping (Tailwind-compatible):**
  * `1` = 4px (micro adjustments only)
  * `2` = 8px (tight gaps, inner button padding)
  * `4` = 16px (standard component padding)
  * `6` = 24px (standard section gap)
  * `8` = 32px (loose container padding)
  * `12` = 48px (minimum mobile tap target size)
  * `16` = 64px (major section spacing)

## 2. Semantic Color Tokens

Do not use raw hex codes or raw framework colors (e.g., `blue-500`). Use these semantic definitions to ensure proper contrast and theme-ability.

### Background & Surfaces
* **Background (`bg-background`):** The app's base layer. Use `slate-50` (Light) or `slate-950` (Dark).
* **Surface Default (`bg-surface`):** Cards, containers, and modals. Must be slightly elevated from the background. Use `white` (Light) or `slate-900` (Dark).
* **Surface Muted (`bg-surface-muted`):** Secondary containers or empty states.
* **Surface Hover (`hover:bg-surface-hover`):** Interactive state for surface elements.

### Text & Typography
* **Primary Text (`text-primary`):** High-emphasis (Headings, active states).
* **Secondary Text (`text-muted`):** Medium-emphasis (Body copy, captions, placeholders).
* **Disabled Text (`text-disabled`):** Low-emphasis (Disabled inputs).
* **Inverse Text (`text-inverse`):** Text on top of brand primary colors (usually pure white).

### Brand & Status
* **Brand Primary (`bg-primary`, `text-primary-600`):** Primary buttons, active tabs, focus rings.
* **Success (`text-emerald-600`, `bg-emerald-50`):** Positive trends, successful saves.
* **Destructive (`text-rose-600`, `bg-rose-50`):** Delete actions, errors.
* **Warning (`text-amber-600`, `bg-amber-50`):** Cautionary actions.

## 3. Typography Scale

Use a clean, modern sans-serif stack (e.g., Inter or system-ui).

* **Display (`text-4xl font-bold tracking-tight`):** Page titles, hero metrics.
* **Heading (`text-2xl font-semibold tracking-tight`):** Section titles, modal headers.
* **Body Large (`text-lg font-medium leading-relaxed`):** Introductory text.
* **Body Base (`text-base font-normal leading-relaxed`):** Standard paragraph text, form inputs.
* **Caption (`text-sm font-medium uppercase tracking-wider text-muted`):** Labels, tags, timestamps.

## 4. Borders, Elevation & Depth

Use subtle borders and shadows to create a tactile hierarchy.

* **Border Default (`border border-border/50`):** Use on all cards and inputs to define boundaries.
* **Radius:** Use `rounded-xl` for large cards/modals, `rounded-md` for buttons/inputs, `rounded-full` for badges/avatars.
* **Shadow Base (`shadow-sm`):** Resting state for cards and dropdowns.
* **Shadow Hover (`hover:shadow-md`):** Hover state for interactive cards.
* **Shadow Modal (`shadow-xl`):** High elevation for popovers, drawers, and modals.

## 5. Motion & Micro-interactions

No interactive element should be static.

* **Transitions:** Apply `transition-all duration-200 ease-in-out` to all buttons, links, and interactive cards.
* **Hover State:** Buttons should slightly brighten or change background. Interactive cards should lift (`hover:-translate-y-0.5`).
* **Active State:** Buttons should scale down slightly (`active:scale-[0.98]`) to feel tactile.
* **Focus Rings:** All interactive elements must have `focus-visible:ring-2 focus-visible:ring-primary focus-visible:outline-none`.

## 6. How to Apply These Rules

During Phase 05 (Code Generation), use the AESTHETIC_VIBE selected in Phase 03 to guide the emotional tone, then apply these rules as hard constraints:

1. **Spatial values** — Every margin, padding, and gap must be from the 8-point grid scale above
2. **Colors** — Use semantic tokens, never raw hex or framework utility colors
3. **Typography** — Use the defined scale hierarchy
4. **Borders/Shadows** — Use the defined elevation tokens
5. **Motion** — Apply transition and interaction rules to all interactive elements

If the user's aesthetic vibe conflicts with these rules (e.g., requesting a value not on the grid), the grid wins. Explain the constraint to the user via AskUserQuestion.
