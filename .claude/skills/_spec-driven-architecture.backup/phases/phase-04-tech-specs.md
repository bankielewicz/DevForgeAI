# Phase 04: Technical Specifications

## Contract

| Attribute | Value |
|-----------|-------|
| **PURPOSE** | Create technical specifications (functional, API, NFR). This is a CONDITIONAL phase -- skip if project scope does not warrant it. |
| **REFERENCES** | `designing-systems/references/technical-specification-workflow.md`, `designing-systems/references/system-design-patterns.md` |
| **STEP COUNT** | 4 mandatory steps (Step 4.0 is a gate that may skip Steps 4.1-4.3) |

## Phase Exit Criteria

Before this phase can complete, ALL of the following MUST be true:
- [ ] Step 4.0 gate executed and user responded
- [ ] IF proceeding: all requested spec files written and verified
- [ ] IF skipped: `phase_skipped` recorded with user confirmation
- [ ] Checkpoint updated with phase data

**IF any criterion is unmet: HALT. Do NOT proceed to Phase 05.**

---

## Reference Loading [MANDATORY]

```
Read(file_path=".claude/skills/designing-systems/references/technical-specification-workflow.md")
Read(file_path=".claude/skills/designing-systems/references/system-design-patterns.md")
```

Do NOT rely on memory of previous reads. Load fresh every time this phase executes.

---

## Mandatory Steps

### Step 4.0: Scope Check (GATE)

**EXECUTE:**
```
AskUserQuestion:
  Question: "Does this project need detailed technical specifications? These include API contracts, database schemas, and non-functional requirement targets. Smaller projects or MVPs often skip this."
  Header: "Technical Specification Scope Gate"
  Options:
    - label: "Yes, create technical specifications"
      description: "Proceed with functional spec, API spec, and NFR document creation"
    - label: "No, skip this phase"
      description: "Project scope does not require formal technical specifications"
  multiSelect: false
```

**VERIFY:**
- User response is non-empty
- Response maps to either "proceed" or "skip"
- If skip: no further steps execute in this phase

**RECORD:**
```json
{
  "step": "4.0",
  "gate_decision": "<proceed|skip>",
  "user_response_raw": "<verbatim response>"
}
```

**IF `gate_decision` is "skip":**
```json
{
  "phase": "04",
  "phase_skipped": true,
  "skip_reason": "user_declined_technical_specifications",
  "phases_skipped": ["04"]
}
```
Jump directly to Phase Transition Display. Do NOT execute Steps 4.1-4.3.

---

### Step 4.1: Functional Specification

**CONDITIONAL:** Only if Step 4.0 gate_decision is "proceed".

**EXECUTE:**
Query user for functional requirements:
```
AskUserQuestion:
  Question: "Define the functional specification. Describe: (1) Primary use cases or user flows, (2) Business rules and validation logic, (3) Data models and entity relationships, (4) External system integrations."
  Header: "Functional Specification Input"
```

Combine user input with architecture style from Phase 01 checkpoint and context files from Phase 02. Write the specification:
```
Write(file_path="devforgeai/specs/functional-spec.md", content=<functional_spec_content>)
```

**VERIFY:**
```
Glob(pattern="devforgeai/specs/functional-spec.md")
```
- File exists (Glob returns 1 match)
- Content length > 200 characters
- Content references the architecture style recorded in Phase 01

**RECORD:**
```json
{
  "step": "4.1",
  "file": "functional-spec.md",
  "created": true,
  "content_length": "<char_count>",
  "use_cases_count": "<number extracted from user input>",
  "architecture_style_referenced": "<from Phase 01 checkpoint>"
}
```

---

### Step 4.2: API Specification

**CONDITIONAL:** Only if Step 4.0 gate_decision is "proceed".

**EXECUTE:**
Query user for API design:
```
AskUserQuestion:
  Question: "Define the API specification. Describe: (1) API style (REST, GraphQL, gRPC), (2) Authentication method (JWT, OAuth2, API keys), (3) Key endpoints or operations, (4) Request/response contract format (JSON, Protobuf), (5) Versioning strategy (URL path, header)."
  Header: "API Specification Input"
```

Generate API specification document from user input. Write:
```
Write(file_path="devforgeai/specs/api-spec.md", content=<api_spec_content>)
```

**VERIFY:**
```
Glob(pattern="devforgeai/specs/api-spec.md")
```
- File exists (Glob returns 1 match)
- Content length > 200 characters
- Content includes authentication method and at least one endpoint

**RECORD:**
```json
{
  "step": "4.2",
  "file": "api-spec.md",
  "created": true,
  "content_length": "<char_count>",
  "api_style": "<from user input>",
  "auth_method": "<from user input>",
  "endpoint_count": "<number>"
}
```

---

### Step 4.3: Non-Functional Requirements

**CONDITIONAL:** Only if Step 4.0 gate_decision is "proceed".

**EXECUTE:**
Query user for NFR targets:
```
AskUserQuestion:
  Question: "Define non-functional requirements. Specify targets for: (1) Response time (p50, p95, p99), (2) Throughput (requests/sec), (3) Availability target (e.g., 99.9%), (4) Security requirements (encryption, audit logging, compliance), (5) Scalability expectations (concurrent users, data volume growth)."
  Header: "Non-Functional Requirements Input"
```

Generate NFR document. Write:
```
Write(file_path="devforgeai/specs/nfr-spec.md", content=<nfr_spec_content>)
```

**VERIFY:**
```
Glob(pattern="devforgeai/specs/nfr-spec.md")
```
- File exists (Glob returns 1 match)
- Content length > 150 characters
- Content includes at least one measurable target (numeric value)

**RECORD:**
```json
{
  "step": "4.3",
  "file": "nfr-spec.md",
  "created": true,
  "content_length": "<char_count>",
  "has_measurable_targets": true,
  "categories_covered": ["<list: performance, security, scalability, etc.>"]
}
```

---

## Phase Transition Display

**If phase was executed:**
```
Display:
  "Phase 04 Complete: Technical Specifications"
  "Created: functional-spec.md, api-spec.md, nfr-spec.md"
  "Architecture foundation is complete. Ready for story creation."
```

**If phase was skipped:**
```
Display:
  "Phase 04 Skipped: Technical Specifications"
  "User elected to skip formal technical specifications."
  "Architecture foundation is complete. Ready for story creation."
```
