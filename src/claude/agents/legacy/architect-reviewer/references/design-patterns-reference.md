# Architect Reviewer - Design Patterns Reference

## Design Patterns Review

### Creational Patterns

**Factory Pattern:**
```
Use when: Object creation logic is complex
Benefit: Encapsulates creation, easier testing
Caution: Don't use for simple constructors
```

**Builder Pattern:**
```
Use when: Objects have many optional parameters
Benefit: Readable, flexible object construction
Caution: Adds complexity, use when > 4 parameters
```

**Singleton Pattern:**
```
Use when: Truly need single instance (rare)
Benefit: Global access point
Caution: Often anti-pattern, prefer dependency injection
```

### Structural Patterns

**Adapter Pattern:**
```
Use when: Need to integrate incompatible interfaces
Benefit: Reuse existing code, maintain separation
Example: Wrap third-party library with own interface
```

**Facade Pattern:**
```
Use when: Simplify complex subsystem
Benefit: Hide complexity, easier to use
Example: Provide simple API over complex library
```

**Repository Pattern:**
```
Use when: Abstract data access layer
Benefit: Testable, swappable data sources
Must: Keep repository interfaces in domain layer
```

### Behavioral Patterns

**Strategy Pattern:**
```
Use when: Multiple algorithms for same task
Benefit: Switch algorithms at runtime
Example: Different payment processors, sorting algorithms
```

**Observer Pattern:**
```
Use when: One-to-many dependency between objects
Benefit: Loose coupling, extensible
Example: Event systems, pub/sub
```

**Command Pattern:**
```
Use when: Need to parameterize, queue, or log operations
Benefit: Undo/redo, transaction support
Example: Task queues, user actions
```
