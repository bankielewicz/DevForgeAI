# Accessibility Patterns for Frontend Developer

**Version**: 1.0 | **Status**: Reference | **Agent**: frontend-developer

---

## Semantic HTML

```html
<!-- GOOD: Semantic structure -->
<nav aria-label="Main navigation">
  <ul>
    <li><a href="/">Home</a></li>
    <li><a href="/about">About</a></li>
  </ul>
</nav>

<main>
  <article>
    <h1>Article Title</h1>
    <p>Content...</p>
  </article>
</main>

<!-- BAD: Div soup -->
<div class="nav">
  <div class="link">Home</div>
  <div class="link">About</div>
</div>
```

## ARIA Attributes

```tsx
// Modal with proper ARIA
<div
  role="dialog"
  aria-labelledby="modal-title"
  aria-describedby="modal-description"
  aria-modal="true"
>
  <h2 id="modal-title">Confirm Action</h2>
  <p id="modal-description">Are you sure you want to proceed?</p>
  <button onClick={onConfirm}>Confirm</button>
  <button onClick={onCancel}>Cancel</button>
</div>

// Loading state
<div role="status" aria-live="polite">
  {loading ? 'Loading...' : 'Content loaded'}
</div>

// Form with labels
<form>
  <label htmlFor="email">Email Address</label>
  <input
    id="email"
    type="email"
    aria-required="true"
    aria-invalid={hasError}
    aria-describedby={hasError ? 'email-error' : undefined}
  />
  {hasError && (
    <span id="email-error" role="alert">
      Please enter a valid email
    </span>
  )}
</form>
```

## Keyboard Navigation

```typescript
function Dropdown() {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedIndex, setSelectedIndex] = useState(0);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    switch (e.key) {
      case 'Enter':
      case ' ':
        setIsOpen(!isOpen);
        break;
      case 'Escape':
        setIsOpen(false);
        break;
      case 'ArrowDown':
        setSelectedIndex(i => Math.min(i + 1, items.length - 1));
        break;
      case 'ArrowUp':
        setSelectedIndex(i => Math.max(i - 1, 0));
        break;
    }
  };

  return (
    <div
      role="combobox"
      aria-expanded={isOpen}
      aria-haspopup="listbox"
      onKeyDown={handleKeyDown}
      tabIndex={0}
    >
      {/* Dropdown content */}
    </div>
  );
}
```

## Focus Management

- Trap focus within modals (prevent tabbing outside)
- Restore focus when modal closes
- Manage focus during SPA route changes
- Skip navigation links for keyboard users

## Color Contrast

- Normal text: minimum 4.5:1 contrast ratio
- Large text (18px+ or 14px+ bold): minimum 3:1 contrast ratio
- Use tools: WebAIM Contrast Checker, axe-core
