# Architect Reviewer - Architecture Review Checklist

### SOLID Principles

**Single Responsibility:**
- [ ] Each class has one reason to change
- [ ] Components have focused, clear purposes
- [ ] No God Objects (classes > 500 lines)

**Open/Closed:**
- [ ] Open for extension, closed for modification
- [ ] Use interfaces and abstractions
- [ ] Plugin architecture where appropriate

**Liskov Substitution:**
- [ ] Subtypes substitutable for base types
- [ ] No surprising behavior in derived classes
- [ ] Contracts preserved in inheritance

**Interface Segregation:**
- [ ] No fat interfaces forcing unnecessary implementations
- [ ] Clients depend only on methods they use
- [ ] Small, focused interfaces

**Dependency Inversion:**
- [ ] High-level modules don't depend on low-level modules
- [ ] Both depend on abstractions
- [ ] Abstractions don't depend on details

### Other Principles

**Separation of Concerns:**
- [ ] Clear layer boundaries (Domain, Application, Infrastructure)
- [ ] No business logic in presentation layer
- [ ] No data access logic in domain layer

**Fail-Fast:**
- [ ] Validate inputs early
- [ ] Fail immediately on invalid state
- [ ] Don't pass errors downstream

**Immutability:**
- [ ] Use immutable objects where possible
- [ ] Avoid shared mutable state
- [ ] Thread-safe by design
