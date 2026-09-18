# Performance Patterns for Frontend Developer

**Version**: 1.0 | **Status**: Reference | **Agent**: frontend-developer

---

## Code Splitting (React)

```typescript
import React, { lazy, Suspense } from 'react';

const Dashboard = lazy(() => import('./Dashboard'));
const Settings = lazy(() => import('./Settings'));

function App() {
  return (
    <Suspense fallback={<Spinner />}>
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </Suspense>
  );
}
```

## Memoization

```typescript
import React, { memo, useMemo, useCallback } from 'react';

function UserList({ users, filter }) {
  const filteredUsers = useMemo(() => {
    return users.filter(u => u.name.includes(filter));
  }, [users, filter]);

  const handleUserClick = useCallback((userId) => {
    console.log('User clicked:', userId);
  }, []);

  return (
    <ul>
      {filteredUsers.map(user => (
        <UserItem key={user.id} user={user} onClick={handleUserClick} />
      ))}
    </ul>
  );
}

const UserItem = memo(({ user, onClick }) => {
  return <li onClick={() => onClick(user.id)}>{user.name}</li>;
});
```

## Responsive Design (Mobile-First)

```css
/* Base styles (mobile) */
.container { padding: 1rem; display: block; }

/* Tablet (768px+) */
@media (min-width: 768px) {
  .container { padding: 2rem; display: flex; }
}

/* Desktop (1024px+) */
@media (min-width: 1024px) {
  .container { max-width: 1200px; margin: 0 auto; }
}
```

## Responsive Images

```tsx
<picture>
  <source srcSet="/images/hero-mobile.webp" media="(max-width: 768px)" type="image/webp" />
  <source srcSet="/images/hero-desktop.webp" media="(min-width: 769px)" type="image/webp" />
  <img src="/images/hero-desktop.jpg" alt="Hero image description" loading="lazy" />
</picture>
```

## Virtualization

For long lists (>100 items), use virtualization libraries (react-virtual, react-window) to render only visible items.

## Key Principles

- Lazy load routes and heavy components
- Code split at route boundaries
- Memoize expensive computations (useMemo)
- Memoize callbacks (useCallback)
- Prevent unnecessary re-renders (React.memo)
- Virtualize long lists
- Use responsive images with srcset
- Apply mobile-first CSS
