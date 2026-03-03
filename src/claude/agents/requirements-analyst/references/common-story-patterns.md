# Common Story Patterns

**Version**: 1.0
**Parent Agent**: requirements-analyst

This reference contains reusable story patterns for common feature types. Use these as starting points when generating stories for CRUD operations, search/filter features, and authentication flows.

---

## CRUD Operations

### Create Resource

```
As a [user role],
I want to create a new [resource],
So that I can [business value].

Acceptance Criteria:
- Given valid input data
- When I submit the create form
- Then the resource is created and I see confirmation

- Given invalid input data
- When I submit the create form
- Then I see validation errors
```

### Read/View Resource

```
As a [user role],
I want to view [resource] details,
So that I can review its information.

Acceptance Criteria:
- Given the resource exists
- When I navigate to the resource detail page
- Then I see all resource fields displayed

- Given the resource does not exist
- When I navigate to its URL
- Then I see a "Not Found" message
```

### Update Resource

```
As a [user role],
I want to update an existing [resource],
So that I can correct or modify its information.

Acceptance Criteria:
- Given I have edit permissions
- When I submit updated fields
- Then the resource is updated and I see confirmation

- Given I do not have edit permissions
- When I attempt to edit
- Then I see an "Access Denied" message
```

### Delete Resource

```
As a [user role],
I want to delete a [resource],
So that I can remove items I no longer need.

Acceptance Criteria:
- Given I own the resource
- When I confirm deletion
- Then the resource is removed and I see confirmation

- Given the resource has dependencies
- When I attempt to delete
- Then I see a warning about dependent items
```

---

## Search/Filter

```
As a [user role],
I want to search [resources] by [criteria],
So that I can quickly find relevant items.

Acceptance Criteria:
- Given I enter search terms
- When I click search
- Then I see matching results ranked by relevance

- Given no matches found
- When I search
- Then I see "No results found" message
```

---

## Authentication

```
As a user,
I want to log in with email and password,
So that I can access my account securely.

Acceptance Criteria:
- Given valid credentials
- When I submit login form
- Then I am authenticated and redirected to dashboard

- Given invalid credentials
- When I submit login form
- Then I see "Invalid credentials" error
- And my account is not locked (after < 5 attempts)

- Given 5 failed login attempts
- When I try to log in again
- Then my account is temporarily locked
- And I receive account lockout notification
```
