# Framework-Specific Patterns for Frontend Developer

**Version**: 1.0 | **Status**: Reference | **Agent**: frontend-developer

---

## React (with Hooks)

**Functional Component:**
```typescript
import React, { useState, useEffect } from 'react';

interface UserProfileProps {
  userId: string;
}

export const UserProfile: React.FC<UserProfileProps> = ({ userId }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        setLoading(true);
        const response = await fetch(`/api/users/${userId}`);
        if (!response.ok) throw new Error('Failed to fetch user');
        const data = await response.json();
        setUser(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchUser();
  }, [userId]);

  if (loading) return <Spinner aria-label="Loading user profile" />;
  if (error) return <ErrorMessage message={error} />;
  if (!user) return null;

  return (
    <section aria-labelledby="profile-heading">
      <h1 id="profile-heading">{user.name}</h1>
      <p>{user.email}</p>
    </section>
  );
};
```

**Custom Hook:**
```typescript
function useApi<T>(url: string) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const controller = new AbortController();
    fetch(url, { signal: controller.signal })
      .then(res => res.json())
      .then(setData)
      .catch(setError)
      .finally(() => setLoading(false));
    return () => controller.abort();
  }, [url]);

  return { data, loading, error };
}
```

---

## Vue 3 (Composition API)

```vue
<template>
  <section aria-labelledby="profile-heading">
    <div v-if="loading" role="status">Loading...</div>
    <div v-else-if="error" role="alert">{{ error }}</div>
    <div v-else>
      <h1 id="profile-heading">{{ user.name }}</h1>
      <p>{{ user.email }}</p>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';

const props = defineProps<{ userId: string }>();
const user = ref<User | null>(null);
const loading = ref(true);
const error = ref<string | null>(null);

onMounted(async () => {
  try {
    const response = await fetch(`/api/users/${props.userId}`);
    if (!response.ok) throw new Error('Failed to fetch user');
    user.value = await response.json();
  } catch (err) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
});
</script>
```

---

## Angular

```typescript
import { Component, Input, OnInit } from '@angular/core';
import { UserService } from './user.service';

@Component({
  selector: 'app-user-profile',
  templateUrl: './user-profile.component.html',
  styleUrls: ['./user-profile.component.css']
})
export class UserProfileComponent implements OnInit {
  @Input() userId!: string;
  user: User | null = null;
  loading = true;
  error: string | null = null;

  constructor(private userService: UserService) {}

  ngOnInit(): void {
    this.userService.getUser(this.userId).subscribe({
      next: (data) => { this.user = data; this.loading = false; },
      error: (err) => { this.error = err.message; this.loading = false; }
    });
  }
}
```

---

## State Management Patterns

### Local State (React)
```typescript
const [isOpen, setIsOpen] = useState(false);
const [selectedTab, setSelectedTab] = useState('overview');
```

### Global State (Zustand)
```typescript
import create from 'zustand';

interface UserState {
  user: User | null;
  setUser: (user: User) => void;
  logout: () => void;
}

export const useUserStore = create<UserState>((set) => ({
  user: null,
  setUser: (user) => set({ user }),
  logout: () => set({ user: null })
}));
```

### Server State (React Query)
```typescript
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

function useUser(userId: string) {
  return useQuery({
    queryKey: ['user', userId],
    queryFn: () => fetch(`/api/users/${userId}`).then(res => res.json())
  });
}
```

---

## Component Design Principles

- **Single Responsibility**: Each component does one thing well
- **Composition over Inheritance**: Build complex UIs from simple components
- **Props Down, Events Up**: Unidirectional data flow
- **Presentational vs Container**: Separate logic from presentation
- **Controlled Components**: Explicit state management
- **Local state** for UI-only concerns (modals, dropdowns)
- **Global state** for shared data (user auth, app settings)
- **Server state** separate from client state (React Query, SWR)
- **Immutable updates** (never mutate state directly)
