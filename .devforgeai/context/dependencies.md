# Dependencies - DevForgeAI Framework

**Status**: LOCKED
**Last Updated**: 2025-10-30
**Version**: 1.0

## Framework Dependencies

### Core Platform Dependency

**Claude Code Terminal 1.0+**
- **LOCKED**: Framework requires Claude Code Terminal
- **Version**: 1.0 or higher
- **Rationale**: Framework built on Claude Code's Skills, Subagents, and Slash Commands

### No External Package Dependencies

**CRITICAL**: DevForgeAI framework itself has ZERO external package dependencies.

**Rationale**:
- Framework is documentation-based (Markdown files)
- No code to execute = No packages to install
- Projects using DevForgeAI specify their own dependencies

### Project Dependency Pattern

When devforgeai-architecture skill creates dependencies.md for projects:

**Process**:
1. Use AskUserQuestion for each technology layer
2. Lock approved packages with versions
3. Document "FORBIDDEN" alternatives
4. Add dependency addition protocol

**Example Project dependencies.md**:
```markdown
# Backend Data Access
- Dapper 2.1.28 (LOCKED - NOT Entity Framework)
- FluentMigrator 3.3.2 (LOCKED)

# Frontend State Management  
- Zustand 4.4.1 (LOCKED - NOT Redux/MobX)

# Testing
- xUnit 2.5.0 (LOCKED - NOT NUnit/MSTest)
- NSubstitute 5.1.0 (LOCKED - NOT Moq)
```

## Dependency Addition Protocol

**Framework Constraint**: When ANY framework component needs external functionality:

1. **Check**: Is it core Claude Code functionality? (Yes → Use it, No → Continue)
2. **Evaluate**: Can it be done with Markdown documentation? (Yes → Document it, No → Continue)
3. **Question**: Use AskUserQuestion to get user approval
4. **Document**: Add to this file with rationale
5. **ADR**: Create Architecture Decision Record

## Prohibited Dependencies

❌ **NO npm packages** for framework
❌ **NO Python packages** for framework  
❌ **NO .NET packages** for framework
❌ **NO** executable code dependencies

**Rationale**: Framework must work across all language ecosystems without installation.

---

**REMEMBER**: This dependencies.md is for the framework itself. Projects using DevForgeAI will have their own dependencies.md created by devforgeai-architecture skill.
