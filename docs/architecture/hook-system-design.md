# Hook System Architecture

Technical architecture documentation for the DevForgeAI event-driven hook system.

## Table of Contents

1. [System Overview](#system-overview)
2. [Component Diagram](#component-diagram)
3. [Hook Invocation Sequence](#hook-invocation-sequence)
4. [Context Extraction Data Flow](#context-extraction-data-flow)
5. [Integration Points](#integration-points)
6. [Configuration Decision Tree](#configuration-decision-tree)

---

## System Overview

The hook system enables automatic callback execution when DevForgeAI operations complete. It provides event-driven triggering for feedback collection, monitoring, and automated retrospectives.

### Key Characteristics

- **Event-Driven** - Hooks trigger automatically on operation completion
- **Non-Invasive** - No modifications to existing commands required
- **Pattern-Based** - Flexible matching (exact, glob, regex)
- **Thread-Safe** - Full async support with lock protection
- **Graceful** - Hook failures isolated from primary operations

### Module Summary

| Module | Responsibility | Lines |
|--------|----------------|-------|
| `hook_system.py` | Main coordinator and public API | ~250 |
| `hook_registry.py` | YAML configuration loading | ~350 |
| `hook_patterns.py` | Pattern matching logic | ~130 |
| `hook_conditions.py` | Trigger condition evaluation | ~140 |
| `hook_invocation.py` | Hook execution orchestration | ~310 |
| `hook_circular.py` | Circular dependency detection | ~160 |

---

## Component Diagram

```mermaid
graph TB
    subgraph Operations["DevForgeAI Operations"]
        CMD[Commands]
        SKL[Skills]
        SUB[Subagents]
    end

    subgraph HookSystem["Hook System"]
        HS[HookSystem<br/>Main API]
        HR[HookRegistry<br/>Configuration]
        HI[HookInvoker<br/>Execution]
        CD[CircularDetector<br/>Loop Prevention]
        PM[PatternMatcher<br/>Name Matching]
        CE[ConditionEvaluator<br/>Trigger Logic]
    end

    subgraph Feedback["Feedback Subsystem"]
        CX[ContextExtraction<br/>TodoWrite Analysis]
        SN[Sanitization<br/>Secret Removal]
        AQ[AdaptiveQuestioning<br/>Question Selection]
        FS[FeedbackSkill<br/>User Interaction]
    end

    subgraph Storage["Storage"]
        CFG[hooks.yaml<br/>Configuration]
        FB[feedback.yaml<br/>Settings]
        SES[Sessions<br/>Feedback Data]
    end

    CMD --> HS
    SKL --> HS
    SUB --> HS

    HS --> HR
    HS --> HI
    HR --> CFG
    HR --> FB
    HI --> CD
    HI --> PM
    HI --> CE

    HI --> CX
    CX --> SN
    SN --> AQ
    AQ --> FS
    FS --> SES

    style HS fill:#e1f5fe
    style CX fill:#fff3e0
    style AQ fill:#fff3e0
```

---

## Hook Invocation Sequence

```mermaid
sequenceDiagram
    participant Op as Operation
    participant HS as HookSystem
    participant HR as HookRegistry
    participant PM as PatternMatcher
    participant CE as ConditionEvaluator
    participant CD as CircularDetector
    participant CX as ContextExtraction
    participant AQ as AdaptiveQuestioning
    participant FS as FeedbackSkill

    Op->>HS: operation_complete(context)
    HS->>HR: get_hooks_for_operation(type, pattern, status)
    HR-->>HS: List[HookEntry]

    loop For each hook
        HS->>PM: matches(operation_name, hook.pattern)
        PM-->>HS: boolean

        alt Pattern matches
            HS->>CE: evaluate(context, hook.conditions)
            CE-->>HS: boolean

            alt Conditions met
                HS->>CD: push(hook_id)
                CD-->>HS: safe (not circular)

                alt Not circular
                    HS->>CX: extract_operation_context(todowrite_state)
                    CX-->>HS: OperationContext

                    HS->>AQ: select_questions(context, feedback_type)
                    AQ-->>HS: List[Question]

                    HS->>FS: invoke(hook, questions, context)
                    FS-->>HS: FeedbackResult

                    HS->>CD: pop(hook_id)
                end
            end
        end
    end

    HS-->>Op: HookInvocationResult
```

---

## Context Extraction Data Flow

```mermaid
flowchart LR
    subgraph Input["Input Sources"]
        TW[TodoWrite State]
        ENV[Environment]
        ERR[Error Context]
    end

    subgraph Extraction["Context Extraction"]
        EX[Extract<br/>operation_context]
        PH[Extract<br/>phases]
        TM[Extract<br/>timing]
        ST[Determine<br/>status]
    end

    subgraph Sanitization["Sanitization"]
        SEC[Remove<br/>Secrets]
        PII[Remove<br/>PII]
        VAL[Validate<br/>Size]
    end

    subgraph Output["Output"]
        OC[OperationContext]
    end

    TW --> EX
    ENV --> EX
    ERR --> EX

    EX --> PH
    EX --> TM
    EX --> ST

    PH --> SEC
    TM --> SEC
    ST --> SEC

    SEC --> PII
    PII --> VAL
    VAL --> OC
```

### OperationContext Data Model

```mermaid
classDiagram
    class OperationContext {
        +string operation_id
        +string operation_type
        +string story_id
        +string start_time
        +string end_time
        +float duration_seconds
        +string status
        +List~TodoContext~ todos
        +ErrorContext error
        +List~string~ phases
        +Dict metadata
    }

    class TodoContext {
        +string content
        +string status
        +string start_time
        +string end_time
        +float duration_seconds
    }

    class ErrorContext {
        +string message
        +string failed_todo
        +string stack_trace
        +string error_type
    }

    OperationContext "1" --> "*" TodoContext
    OperationContext "1" --> "0..1" ErrorContext
```

---

## Integration Points

### Command Integration

Commands integrate with the hook system through the operation completion callback:

```mermaid
flowchart TB
    subgraph Command["Command Execution"]
        START[Command Start]
        EXEC[Execute Logic]
        TODO[TodoWrite Update]
        DONE[Command Complete]
    end

    subgraph HookTrigger["Hook Trigger"]
        DETECT[Detect Completion]
        MATCH[Match Hooks]
        INVOKE[Invoke Hooks]
    end

    START --> EXEC
    EXEC --> TODO
    TODO --> DONE
    DONE --> DETECT
    DETECT --> MATCH
    MATCH --> INVOKE

    style TODO fill:#fff3e0
    style DETECT fill:#e1f5fe
```

### Skill Integration

Skills can trigger hooks at phase completion:

| Skill | Hook Trigger Point | Status Values |
|-------|-------------------|---------------|
| devforgeai-development | After Phase 08 | success, partial, failure |
| devforgeai-qa | After validation | success, failure |
| devforgeai-release | After deployment | success, failure |
| devforgeai-orchestration | After each phase | success, partial, failure |

### Data Flow from Operation to Storage

```mermaid
flowchart LR
    OP[Operation<br/>Completes] --> HS[HookSystem<br/>Detects]
    HS --> CX[Context<br/>Extracted]
    CX --> SAN[Context<br/>Sanitized]
    SAN --> AQ[Questions<br/>Selected]
    AQ --> UI[User<br/>Interaction]
    UI --> SES[Session<br/>Stored]

    style OP fill:#c8e6c9
    style SES fill:#bbdefb
```

---

## Configuration Decision Tree

Use this decision tree to determine optimal configuration:

```mermaid
flowchart TD
    START[Configure Feedback?] --> Q1{Need automatic<br/>feedback?}

    Q1 -->|No| DISABLE[Set enabled: false]
    Q1 -->|Yes| Q2{When to collect?}

    Q2 -->|All operations| ALWAYS[trigger_mode: always]
    Q2 -->|Failures only| FAILURES[trigger_mode: failures-only]
    Q2 -->|Specific commands| SPECIFIC[trigger_mode: specific-operations]

    SPECIFIC --> LIST[List operations:<br/>- qa<br/>- dev<br/>- release]

    ALWAYS --> Q3{Question count?}
    FAILURES --> Q3
    LIST --> Q3

    Q3 -->|Few| FEW[max_questions: 3]
    Q3 -->|Standard| STD[max_questions: 5]
    Q3 -->|Comprehensive| MANY[max_questions: 10]

    FEW --> Q4{Allow skipping?}
    STD --> Q4
    MANY --> Q4

    Q4 -->|Yes| SKIP[allow_skip: true<br/>max_consecutive_skips: 3]
    Q4 -->|No| NOSKIP[allow_skip: false]

    SKIP --> DONE[Configuration Complete]
    NOSKIP --> DONE
    DISABLE --> DONE

    style START fill:#e1f5fe
    style DONE fill:#c8e6c9
```

### Quick Reference

| Scenario | trigger_mode | max_questions | allow_skip |
|----------|--------------|---------------|------------|
| Development | failures-only | 5 | true |
| Production monitoring | always | 3 | true |
| Debug session | always | 10 | false |
| Minimal overhead | never | - | - |

---

## Related Documentation

- [User Guide](../guides/feedback-system-user-guide.md) - Configuration instructions
- [Troubleshooting](../guides/feedback-troubleshooting.md) - Common issues
- [HOOK-SYSTEM.md](../../.claude/skills/devforgeai-feedback/HOOK-SYSTEM.md) - Full technical reference
