# UI Component Anatomy Standards

**Purpose:** Enforce consistent component structure following Atomic Design principles.
**Version:** 1.0
**Loaded by:** Phase 04, Step 4.4c
**Applies to:** Web UI, Desktop GUI (skip for Terminal UI)

---

Generated UI components must not be monolithic single-file dumps. Follow these structural patterns to ensure maintainability, testability, and separation of concerns.

## 1. Smart vs. Dumb Components

Every component should be classified as either Smart or Dumb:

| Type | Also Called | Responsibility | Side Effects? |
|------|-----------|---------------|---------------|
| **Smart** | Container | Data fetching, state management, event coordination | Yes |
| **Dumb** | Presentational | Receives props, renders UI, fires callbacks | No |

**Rules:**
- Dumb components must be pure functions — same props always produce the same output
- Smart components handle data and pass it down as props to Dumb components
- Never mix data fetching logic with UI rendering in the same component

## 2. File Structure (Web UI — React/JSX)

For any component more complex than a basic button, generate a folder structure:

```text
ComponentName/
├── index.ts              (Exports the component — barrel file)
├── ComponentName.tsx     (The UI layout — Dumb component)
├── ComponentName.hooks.ts(Custom hooks — state & logic)
└── ComponentName.module.css (Scoped styles, if using CSS Modules)
```

**When to use flat file vs. folder:**
- **Flat file** (single `.tsx`): Simple, stateless components with < 50 lines (buttons, badges, icons)
- **Folder structure**: Any component with state, data fetching, or > 50 lines

## 3. File Structure (Desktop GUI)

**WPF (C#):**
```text
ComponentName/
├── ComponentNameView.xaml       (XAML layout)
├── ComponentNameView.xaml.cs    (Code-behind — minimal, UI events only)
└── ComponentNameViewModel.cs    (MVVM ViewModel — state & logic)
```

**Tkinter (Python):**
```text
component_name/
├── __init__.py                  (Exports the component)
├── component_name_view.py       (UI layout — frames, widgets)
└── component_name_controller.py (Event handling, state management)
```

## 4. Component Composition Patterns

### Props Interface (TypeScript)
Every component must define an explicit props interface:

```typescript
export interface ComponentNameProps {
  /** Brief description of what this prop does */
  title: string;
  isLoading?: boolean;
  onAction?: () => void;
}
```

### Loading & Error States
Every component that fetches data must handle three states:

1. **Loading** — Render a skeleton loader (not a spinner) with `aria-busy="true"`
2. **Error** — Render an error banner with retry action and `aria-live="polite"`
3. **Success** — Render the content

### Base Component Template (React)

```tsx
import React from 'react';

export interface ComponentNameProps {
  title: string;
  isLoading?: boolean;
}

export const ComponentName: React.FC<ComponentNameProps> = ({
  title,
  isLoading = false,
}) => {
  if (isLoading) {
    return <div aria-busy="true" className="skeleton">Loading...</div>;
  }

  return (
    <section>
      <h2>{title}</h2>
      {/* Component content */}
    </section>
  );
};
```

## 5. When to Apply These Standards

During Phase 05 (Code Generation), use this document to:

1. **Classify** each component in the COMPONENTS list as Smart or Dumb
2. **Structure** files according to the patterns above (folder for complex, flat for simple)
3. **Define** explicit props interfaces for all components
4. **Implement** loading/error/success states for data-fetching components
5. **Separate** concerns — never mix data logic with presentation rendering
