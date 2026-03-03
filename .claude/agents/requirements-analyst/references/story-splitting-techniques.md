# Story Splitting Techniques

**Version**: 1.0
**Parent Agent**: requirements-analyst

This reference documents systematic techniques for splitting large user stories into smaller, independently deliverable units. Apply these when a story exceeds 5 story points or cannot be completed within a single sprint.

---

## Split by Operations

**Large**: "Manage users"
**Split into**:
- Create new user
- Update user profile
- Delete user account
- List all users

## Split by Roles

**Large**: "User authentication"
**Split into**:
- User login (end user)
- Admin login (administrator)
- Service authentication (system)

## Split by Data

**Large**: "Import data"
**Split into**:
- Import from CSV
- Import from JSON
- Import from API

## Split by Business Rules

**Large**: "Calculate shipping cost"
**Split into**:
- Calculate domestic shipping
- Calculate international shipping
- Apply shipping discounts

## Split by Happy Path vs Exceptions

**Large**: "Process payment"
**Split into**:
- Process successful payment (happy path)
- Handle payment failure (exception)
- Handle payment timeout (exception)

---

## When to Split

A story should be split when:
1. **Estimation exceeds 5 points** - Too large for a single sprint
2. **Multiple user roles** - Different roles imply different workflows
3. **Multiple data sources** - Each source may have unique handling
4. **Complex business rules** - Each rule branch deserves its own story
5. **Mixed happy path and error handling** - Separate core flow from exception handling
