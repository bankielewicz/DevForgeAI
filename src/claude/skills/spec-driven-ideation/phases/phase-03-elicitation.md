# Phase 03: Requirements Elicitation

## Contract

| Attribute | Value |
|-----------|-------|
| **PURPOSE** | Systematically extract functional requirements, data requirements, integration requirements, and non-functional requirements through progressive questioning. Apply domain-specific patterns and MoSCoW prioritization. |
| **REFERENCE** | `.claude/skills/spec-driven-ideation/references/requirements-elicitation-workflow.md`, `requirements-elicitation-guide.md`, `domain-specific-patterns.md`, `user-interaction-patterns.md` |
| **STEP COUNT** | 8 mandatory steps (3.1 through 3.8) |
| **MINIMUM QUESTIONS** | 10 |

## Phase Exit Criteria

Before this phase can complete, ALL of the following MUST be true:

- [ ] functional_requirements captured (at least 5 as user stories)
- [ ] nfr_requirements captured (at least 1 with quantified target)
- [ ] data_entities identified (at least 1 with attributes)
- [ ] integrations documented (list, can be empty)
- [ ] All requirements have MoSCoW priority assigned
- [ ] No vague NFR terms remain (no "fast", "scalable", "secure" without metrics)
- [ ] Checkpoint updated with phase data
- [ ] Context window check completed

**IF any criterion is unmet: HALT. Do NOT proceed to Phase 04.**

---

## Reference Loading [MANDATORY]

```
Read(file_path=".claude/skills/spec-driven-ideation/references/requirements-elicitation-workflow.md")
Read(file_path=".claude/skills/spec-driven-ideation/references/requirements-elicitation-guide.md")
Read(file_path=".claude/skills/spec-driven-ideation/references/domain-specific-patterns.md")
Read(file_path=".claude/skills/spec-driven-ideation/references/user-interaction-patterns.md")
```

IF any Read fails: HALT -- "Phase 03 reference files not loaded. Cannot proceed without reference material."

Do NOT rely on memory of previous reads. Load ALL FOUR references fresh every time this phase executes.

---

## Mandatory Steps

### Step 3.1: Domain Detection & Pattern Loading

**Condition:** Uses `session.completed_outputs.complexity_assessment` and `session.completed_outputs.problem_statement` from Phase 02 to identify the applicable domain.

EXECUTE:
```
# Analyze problem statement and complexity assessment for domain signals
domain_signals = analyze_for_domain_keywords(
  session.completed_outputs.problem_statement,
  session.completed_outputs.complexity_assessment,
  session.completed_outputs.business_goals
)

# Build domain options from detected signals
# Domains from domain-specific-patterns.md:
#   E-commerce, SaaS, Fintech, Healthcare, Content Management,
#   Workflow/Automation, General/Custom

detected_domain = infer_primary_domain(domain_signals)

AskUserQuestion:
  questions:
    - question: "Based on your project description, this appears to be a {detected_domain} application. Which domain best describes your project?"
      header: "Domain"
      multiSelect: false
      options:
        - label: "E-commerce"
          description: "Product discovery, payment, inventory, shipping, refunds"
        - label: "SaaS"
          description: "Multi-tenancy, subscriptions, usage tracking, billing"
        - label: "Fintech"
          description: "Financial operations, accounts, compliance, AML/KYC, fraud"
        - label: "Healthcare"
          description: "Patient data, clinical workflows, HIPAA compliance"
        - label: "Content Management"
          description: "Authoring, versioning, publishing, media management"
        - label: "Workflow/Automation"
          description: "Process automation, triggers, integrations, approvals"
        - label: "General/Custom"
          description: "No specific domain pattern applies"
```

Decision Logic:
```
IF response in ["E-commerce", "SaaS", "Fintech", "Healthcare", "Content Management", "Workflow/Automation"]:
  session.domain = response
  # Domain-specific patterns from domain-specific-patterns.md are now active
  # These inform feature options in Steps 3.2 and 3.3

ELSE IF response == "General/Custom":
  session.domain = "General/Custom"
  # Use generic feature categories, no domain-specific pattern enrichment
```

VERIFY: User response captured and non-empty. `session.domain` is set to one of the 7 domain values.
IF response is null or empty: HALT -- "Step 3.1: Domain Detection response not captured."
IF `session.domain` is null after processing: HALT -- "Step 3.1: Domain not set after user response."

RECORD: Update checkpoint: `session.phases["03"].questions_answered += 1`; `session.completed_outputs.domain = session.domain`

---

### Step 3.2: Functional Requirements Discovery (Level 1 - Broad)

This step applies Progressive Narrowing Level 1 (Broad Discovery) from requirements-elicitation-workflow.md. The goal is to identify major feature categories before drilling into specifics.

EXECUTE (Feature Category Identification):
```
# Build domain-appropriate feature options
# Source: domain-specific-patterns.md > {session.domain} > Standard Features

IF session.domain == "E-commerce":
  feature_options = [
    {label: "Product Catalog", description: "Browse, search, filter products with inventory tracking"},
    {label: "Shopping & Checkout", description: "Cart, wishlist, guest checkout, payment processing"},
    {label: "Order Management", description: "Order tracking, fulfillment, returns, refunds"},
    {label: "Customer Accounts", description: "Profiles, order history, saved addresses, loyalty"},
    {label: "Admin & Analytics", description: "Product management, sales reports, promotions"},
    {label: "Marketing", description: "Coupons, email campaigns, abandoned cart recovery"}
  ]
ELSE IF session.domain == "SaaS":
  feature_options = [
    {label: "Multi-Tenancy", description: "Tenant isolation, data separation, tenant management"},
    {label: "Subscription & Billing", description: "Plans, pricing tiers, usage-based billing, invoicing"},
    {label: "User Management", description: "Roles, permissions, SSO, team workspaces"},
    {label: "API & Integrations", description: "REST APIs, webhooks, OAuth, third-party connectors"},
    {label: "Admin Dashboard", description: "Tenant analytics, usage monitoring, system health"},
    {label: "Collaboration", description: "Shared resources, real-time editing, notifications"}
  ]
ELSE IF session.domain == "Fintech":
  feature_options = [
    {label: "Account Management", description: "Account types, balances, statements, limits"},
    {label: "Transactions", description: "Payments, transfers, P2P, international transactions"},
    {label: "Compliance & KYC", description: "Identity verification, AML screening, regulatory reporting"},
    {label: "Fraud Prevention", description: "Transaction monitoring, risk scoring, alerts"},
    {label: "Reporting", description: "Financial statements, tax documents, audit trails"},
    {label: "Lending/Investing", description: "Loan management, investment portfolios, risk assessment"}
  ]
ELSE IF session.domain == "Healthcare":
  feature_options = [
    {label: "Patient Records", description: "Demographics, medical history, prescriptions, lab results"},
    {label: "Clinical Workflows", description: "Scheduling, check-in, charting, referrals"},
    {label: "Provider Management", description: "Physician, nurse, admin roles and permissions"},
    {label: "Telehealth", description: "Video consultations, remote monitoring, e-prescriptions"},
    {label: "Billing & Insurance", description: "Claims processing, co-pays, insurance verification"},
    {label: "Interoperability", description: "HL7, FHIR, lab/pharmacy system integration"}
  ]
ELSE IF session.domain == "Content Management":
  feature_options = [
    {label: "Content Authoring", description: "Rich text editing, media embedding, templates"},
    {label: "Workflow & Approval", description: "Draft, review, approval, publish, archive lifecycle"},
    {label: "Versioning", description: "Version history, rollback, diff viewing"},
    {label: "Media Management", description: "Image, video, document upload and organization"},
    {label: "Publishing", description: "Multi-channel publishing, scheduling, SEO tools"},
    {label: "Personalization", description: "User-based content, A/B testing, analytics"}
  ]
ELSE IF session.domain == "Workflow/Automation":
  feature_options = [
    {label: "Process Design", description: "Visual workflow builder, sequential/parallel/conditional steps"},
    {label: "Trigger Management", description: "Manual, scheduled, event-based, webhook triggers"},
    {label: "Task Management", description: "Assignments, deadlines, escalations, notifications"},
    {label: "Integration Hub", description: "Connect external systems, data mapping, transformation"},
    {label: "Monitoring", description: "Execution logs, dashboards, alerts, SLA tracking"},
    {label: "Form Builder", description: "Custom forms, dynamic fields, validation rules"}
  ]
ELSE:
  # General/Custom domain
  feature_options = [
    {label: "User Management", description: "Registration, authentication, profiles, roles"},
    {label: "Core Business Logic", description: "Primary features specific to your domain"},
    {label: "Data Management", description: "CRUD operations, search, filtering, reporting"},
    {label: "Notifications", description: "Email, in-app, push notifications"},
    {label: "Admin Panel", description: "System configuration, user management, analytics"},
    {label: "API Layer", description: "REST/GraphQL APIs for external consumption"}
  ]

AskUserQuestion:
  questions:
    - question: "What are the main features or capabilities this system needs?"
      header: "Feature Categories"
      multiSelect: true
      options: feature_options
```

EXECUTE (Clarifying Questions per Category):
```
FOR each selected_category in user_selected_features:
  AskUserQuestion:
    questions:
      - question: "For {selected_category}, what is the most important capability your users need?"
        header: "{selected_category} Priority"
        multiSelect: false
        options:
          # Options vary by domain and category - pull from domain-specific-patterns.md
          # Example for E-commerce > Product Catalog:
          - label: "Advanced search and filtering"
            description: "Users need to find products quickly"
          - label: "Product recommendations"
            description: "Suggest related products to increase sales"
          - label: "Inventory visibility"
            description: "Real-time stock status is critical"
          - label: "All of these equally"
            description: "No single capability dominates"

  Store response in session.feature_categories[selected_category].priority_capability
```

VERIFY: User response captured and non-empty. At least 3 feature categories selected from multiSelect.
IF response is null or empty: HALT -- "Step 3.2: Functional Requirements Discovery (Level 1) response not captured."
IF `len(session.feature_categories) < 3`: HALT -- "Step 3.2: At least 3 feature categories required. Only {count} selected."
Store in `session.feature_categories` with priority capabilities.

RECORD: Update checkpoint: `session.phases["03"].questions_answered += 1 + len(session.feature_categories)`; `session.completed_outputs.feature_categories = session.feature_categories`

---

### Step 3.3: Functional Requirements Deep Dive (Level 2 - Feature-Specific)

This step applies Progressive Narrowing Level 2 (Feature-Specific Probing) from requirements-elicitation-workflow.md. Drill into each feature category from Step 3.2 to extract specific user stories.

EXECUTE:
```
# Determine question depth based on complexity tier from Phase 02
complexity_tier = session.completed_outputs.complexity_assessment.tier

# Question count per category scales with complexity
IF complexity_tier == "Tier 1" OR complexity_tier == "Simple":
  questions_per_category = 2
ELSE IF complexity_tier == "Tier 2" OR complexity_tier == "Standard":
  questions_per_category = 3
ELSE IF complexity_tier == "Tier 3" OR complexity_tier == "Complex":
  questions_per_category = 5
ELSE IF complexity_tier == "Tier 4" OR complexity_tier == "Enterprise":
  questions_per_category = 8
ELSE:
  questions_per_category = 3  # Default to standard

functional_requirements = []

FOR each category in session.feature_categories:

  # Question A: Specific user actions
  AskUserQuestion:
    questions:
      - question: "For {category}, what specific actions should users be able to perform?"
        header: "{category} Actions"
        multiSelect: true
        options:
          # Domain-specific action options from requirements-elicitation-guide.md
          # These are dynamically constructed based on session.domain + category
          - label: "{action_1}"
            description: "{action_1_description}"
          - label: "{action_2}"
            description: "{action_2_description}"
          - label: "{action_3}"
            description: "{action_3_description}"
          - label: "Other actions (let me describe)"
            description: "I have specific actions not listed"

  IF "Other actions" selected:
    Capture free-form description from user
    Parse into individual actions

  # Question B: Business rules and validation
  AskUserQuestion:
    questions:
      - question: "For {category}, what business rules or validation rules apply?"
        header: "{category} Rules"
        multiSelect: true
        options:
          - label: "Data validation rules"
            description: "Required fields, format checks, ranges"
          - label: "Business logic rules"
            description: "Calculations, conditions, workflows"
          - label: "Authorization rules"
            description: "Who can do what"
          - label: "Timing/deadline rules"
            description: "Time-based constraints or triggers"
          - label: "No special rules"
            description: "Standard CRUD behavior is sufficient"

  # Question C (Tier 2+): Edge cases
  IF questions_per_category >= 3:
    AskUserQuestion:
      questions:
        - question: "For {category}, what should happen when something goes wrong?"
          header: "{category} Edge Cases"
          multiSelect: true
          options:
            - label: "Retry automatically"
              description: "System retries failed operations"
            - label: "Notify user and allow manual recovery"
              description: "Alert the user, let them fix it"
            - label: "Fail gracefully with error message"
              description: "Show clear error, no data loss"
            - label: "Escalate to admin/support"
              description: "Auto-create support ticket"
            - label: "Rollback to previous state"
              description: "Undo partial changes"

  # Convert collected answers to user story format
  # Template: "As a {persona}, I want to {action} so that {benefit}"
  # Use personas from Phase 02: session.completed_outputs.personas

  FOR each action in selected_actions:
    persona = determine_primary_persona(action, session.completed_outputs.personas)
    benefit = infer_business_benefit(action, category, session.completed_outputs.business_goals)

    user_story = {
      id: "FR-{sequential_number}",
      story: "As a {persona.name}, I want to {action} so that {benefit}",
      category: category,
      acceptance_criteria: derive_from_business_rules(action, selected_rules),
      edge_cases: selected_edge_cases or [],
      priority: null  # Assigned in Step 3.7
    }
    functional_requirements.append(user_story)

session.functional_requirements = functional_requirements
```

VERIFY: At least 5 functional requirements documented as user stories.
IF `len(session.functional_requirements) < 5`: HALT -- "Step 3.3: At least 5 functional requirements required. Only {count} captured."
IF any user story is missing `story` or `category` field: HALT -- "Step 3.3: Incomplete user story detected: {user_story.id}."
All user stories follow "As a {persona}, I want to {action} so that {benefit}" format.

RECORD: Update checkpoint: `session.phases["03"].questions_answered += (2 * len(session.feature_categories)) + additional_edge_case_questions`; `session.completed_outputs.functional_requirements = session.functional_requirements`

---

### Step 3.4: Data Requirements Discovery

EXECUTE (Entity Identification):
```
# Build entity options based on domain
# Source: domain-specific-patterns.md > {session.domain} > Data Model > Core Entities

IF session.domain == "E-commerce":
  entity_options = [
    {label: "Users/Customers", description: "Customer info, addresses, payment methods"},
    {label: "Products", description: "SKU, name, description, price, images, inventory"},
    {label: "Categories", description: "Hierarchical product categories and subcategories"},
    {label: "Orders", description: "Order status, totals, line items, shipping info"},
    {label: "Payments", description: "Transaction records, payment methods, refunds"},
    {label: "Reviews", description: "Customer ratings, review text, verified purchase flag"}
  ]
ELSE IF session.domain == "SaaS":
  entity_options = [
    {label: "Tenants/Organizations", description: "Company info, subscription plan, billing"},
    {label: "Users", description: "Login credentials, roles, preferences, team membership"},
    {label: "Subscriptions", description: "Plan type, billing cycle, usage limits, renewal"},
    {label: "Usage Records", description: "API calls, storage, compute, tracked metrics"},
    {label: "Invoices", description: "Billing periods, line items, payment status"},
    {label: "Audit Logs", description: "User actions, system events, compliance trail"}
  ]
ELSE IF session.domain == "Fintech":
  entity_options = [
    {label: "Accounts", description: "Account types, balances, limits, status"},
    {label: "Transactions", description: "Debits, credits, transfers, transaction metadata"},
    {label: "Users/Customers", description: "KYC data, verification status, risk profile"},
    {label: "Compliance Records", description: "AML checks, SAR filings, audit trail"},
    {label: "Payment Methods", description: "Bank accounts, cards, digital wallets"},
    {label: "Notifications", description: "Alerts, statements, regulatory notices"}
  ]
ELSE IF session.domain == "Healthcare":
  entity_options = [
    {label: "Patients", description: "Demographics, insurance, emergency contacts"},
    {label: "Medical Records", description: "Diagnoses, prescriptions, lab results, notes"},
    {label: "Providers", description: "Physicians, nurses, specialties, schedules"},
    {label: "Appointments", description: "Scheduling, check-in, visit type, duration"},
    {label: "Claims/Billing", description: "Insurance claims, co-pays, billing codes"},
    {label: "Medications", description: "Drug formulary, dosages, interactions, refills"}
  ]
ELSE:
  # General/Custom, Content Management, Workflow/Automation
  entity_options = [
    {label: "Users", description: "User accounts, profiles, roles, preferences"},
    {label: "Core Business Object", description: "Primary entity your system manages"},
    {label: "Transactions/Events", description: "Records of actions or changes"},
    {label: "Configuration", description: "System settings, rules, templates"},
    {label: "Files/Media", description: "Uploaded documents, images, attachments"},
    {label: "Audit Trail", description: "Action logs, change history, compliance"}
  ]

AskUserQuestion:
  questions:
    - question: "What are the main things (entities) your system needs to track?"
      header: "Data Entities"
      multiSelect: true
      options: entity_options
```

EXECUTE (Attribute Probing):
```
FOR each entity in selected_entities:
  AskUserQuestion:
    questions:
      - question: "What information (attributes) needs to be stored for a {entity}?"
        header: "{entity} Attributes"
        multiSelect: true
        options:
          # Domain-specific attributes from domain-specific-patterns.md
          - label: "{attribute_1}"
            description: "{attribute_1_description}"
          - label: "{attribute_2}"
            description: "{attribute_2_description}"
          - label: "{attribute_3}"
            description: "{attribute_3_description}"
          - label: "Other attributes (let me list)"
            description: "I have specific attributes not shown"

  IF "Other attributes" selected:
    Capture free-form attribute list from user

  Store in session.data_entities[entity].attributes = selected_attributes
```

EXECUTE (Relationship Probing):
```
IF len(selected_entities) >= 2:
  # Ask about relationships between entity pairs
  # Only probe the most likely relationships (not all permutations)

  AskUserQuestion:
    questions:
      - question: "How do these entities relate to each other?"
        header: "Relationships"
        multiSelect: true
        options:
          # Generate relationship options for likely pairs
          - label: "One {entity_1} has many {entity_2}"
            description: "Example: One customer has many orders"
          - label: "Many {entity_1} have many {entity_2}"
            description: "Example: Many users belong to many groups"
          - label: "One {entity_1} has one {entity_2}"
            description: "Example: One user has one profile"

  Store in session.data_entities.relationships = selected_relationships
```

EXECUTE (Data Rules):
```
AskUserQuestion:
  questions:
    - question: "Any special data rules for these entities?"
      header: "Data Rules"
      multiSelect: true
      options:
        - label: "Unique values required"
          description: "Email addresses, usernames, or IDs must be unique"
        - label: "Required fields"
          description: "Some fields cannot be left empty"
        - label: "Calculated fields"
          description: "Values derived from other data (totals, averages)"
        - label: "Soft delete"
          description: "Records are archived, not permanently deleted"
        - label: "Versioning"
          description: "Track changes to records over time"
        - label: "No special rules"
          description: "Standard behavior is fine"
```

VERIFY: At least 1 data entity identified with attributes.
IF `len(session.data_entities) < 1`: HALT -- "Step 3.4: At least 1 data entity required. None captured."
IF any entity is missing attributes: HALT -- "Step 3.4: Entity '{entity}' has no attributes defined."
Store in `session.data_entities` with attributes, relationships, and data rules.

RECORD: Update checkpoint: `session.phases["03"].questions_answered += 1 + len(selected_entities) + (1 if relationships_asked else 0) + 1`; `session.completed_outputs.data_entities = session.data_entities`

---

### Step 3.5: Integration Requirements

EXECUTE (Integration Identification):
```
AskUserQuestion:
  questions:
    - question: "Does this system need to connect with any external services or APIs?"
      header: "Integrations"
      multiSelect: true
      options:
        - label: "Payment gateway"
          description: "Stripe, PayPal, Square, Braintree"
        - label: "Email service"
          description: "SendGrid, AWS SES, Mailgun, Postmark"
        - label: "Authentication provider"
          description: "Auth0, Okta, OAuth, SAML, Firebase Auth"
        - label: "Cloud storage"
          description: "S3, Azure Blob, Google Cloud Storage"
        - label: "Analytics"
          description: "Google Analytics, Mixpanel, Amplitude, Segment"
        - label: "SMS/Push notifications"
          description: "Twilio, AWS SNS, Firebase Cloud Messaging"
        - label: "Maps/Geolocation"
          description: "Google Maps, Mapbox, HERE"
        - label: "CRM/ERP"
          description: "Salesforce, HubSpot, SAP, NetSuite"
        - label: "Other external service"
          description: "A service not listed above"
        - label: "No external integrations"
          description: "System is standalone"
```

Decision Logic:
```
IF "No external integrations" selected:
  session.integrations = []
  Display: "No external integrations needed. Proceeding."
  SKIP integration detail probing below

ELSE:
  selected_integrations = user_selected_options (excluding "No external integrations")
```

EXECUTE (Integration Details - for each selected integration):
```
IF len(selected_integrations) > 0:

  FOR each integration in selected_integrations:

    AskUserQuestion:
      questions:
        - question: "For {integration}, what data flows between your system and the service?"
          header: "{integration} Data Flow"
          multiSelect: false
          options:
            - label: "Send data to service"
              description: "One-way outbound (e.g., send emails, push payments)"
            - label: "Receive data from service"
              description: "One-way inbound (e.g., receive webhooks, import data)"
            - label: "Bidirectional sync"
              description: "Two-way data exchange (e.g., CRM sync, real-time updates)"

    Store in session.integrations[integration] = {
      service: integration,
      data_flow: response,
      protocol: null,  # Inferred or asked in architecture phase
      frequency: null   # Inferred or asked in architecture phase
    }
```

EXECUTE (Third-Party Services Follow-Up):
```
IF "Other external service" was selected:
  AskUserQuestion:
    questions:
      - question: "What third-party services need to integrate with your system?"
        header: "Other Services"
        multiSelect: false
        options:
          - label: "Let me describe them"
            description: "I'll list the services and their purpose"

  Capture free-form service descriptions from user.
  Parse each service into session.integrations[] with data flow TBD.
```

VERIFY: Integration list captured (can be empty if standalone system).
IF response is null or empty: HALT -- "Step 3.5: Integration Requirements response not captured."
`session.integrations` is set (either populated list or empty array).

RECORD: Update checkpoint: `session.phases["03"].questions_answered += 1 + len(selected_integrations)`; `session.completed_outputs.integrations = session.integrations`

---

### Step 3.6: Non-Functional Requirements (Quantified)

**Critical Rule:** Every NFR captured in this step MUST have a measurable, quantified target. Vague terms like "fast", "scalable", "secure", or "reliable" without metrics are FORBIDDEN. If the user provides vague terms, probe until a numeric target is obtained or document as an ASSUMPTION with a specific assumed value.

EXECUTE (Performance Requirements):
```
AskUserQuestion:
  questions:
    - question: "What response time is acceptable for your system?"
      header: "Performance"
      multiSelect: false
      options:
        - label: "High performance (<100ms API response)"
          description: "Real-time applications, trading, gaming"
        - label: "Interactive (<500ms API response)"
          description: "E-commerce, dashboards, interactive apps"
        - label: "Standard (<2s API response)"
          description: "Content sites, internal tools, forms"
        - label: "Batch processing acceptable"
          description: "Background jobs, reports, data pipelines"

Store in session.nfr.performance.response_time = {
  target: "<100ms" | "<500ms" | "<2s" | "batch",
  quantified: true
}
```

EXECUTE (Concurrent Users):
```
AskUserQuestion:
  questions:
    - question: "How many concurrent users should the system support?"
      header: "Concurrency"
      multiSelect: false
      options:
        - label: "Small (<100 concurrent users)"
          description: "Internal tool, small team"
        - label: "Medium (100-1,000 concurrent users)"
          description: "Department-level or mid-size app"
        - label: "Large (1,000-10,000 concurrent users)"
          description: "Company-wide or popular app"
        - label: "Massive (10,000+ concurrent users)"
          description: "Public-facing, high-traffic platform"

Store in session.nfr.performance.concurrent_users = {
  target: "<100" | "100-1000" | "1000-10000" | "10000+",
  quantified: true
}
```

EXECUTE (Availability Requirements):
```
AskUserQuestion:
  questions:
    - question: "What uptime is required for your system?"
      header: "Availability"
      multiSelect: false
      options:
        - label: "99% uptime (3.65 days downtime/year)"
          description: "Internal tools, non-critical apps"
        - label: "99.9% uptime (8.77 hours downtime/year)"
          description: "Business-critical applications"
        - label: "99.99% uptime (52.6 minutes downtime/year)"
          description: "High-availability, mission-critical systems"
        - label: "Best effort (no SLA)"
          description: "Prototype, MVP, or internal experiment"

Store in session.nfr.availability = {
  target: "99%" | "99.9%" | "99.99%" | "best_effort",
  quantified: true
}
```

EXECUTE (Compliance Requirements):
```
AskUserQuestion:
  questions:
    - question: "Are there any compliance or regulatory requirements?"
      header: "Compliance"
      multiSelect: true
      options:
        - label: "GDPR"
          description: "EU data protection (user consent, right to erasure, data portability)"
        - label: "HIPAA"
          description: "US healthcare data protection (PHI handling, BAAs, audit controls)"
        - label: "SOC 2"
          description: "Service organization security controls (Type I or Type II)"
        - label: "PCI-DSS"
          description: "Payment card data security (credit card handling)"
        - label: "Section 508 / WCAG 2.1 AA"
          description: "Accessibility requirements for web applications"
        - label: "No specific compliance requirements"
          description: "Standard security practices are sufficient"

Store in session.nfr.compliance = selected_compliance_standards
```

EXECUTE (Accessibility Requirements):
```
IF "Section 508 / WCAG 2.1 AA" NOT in selected_compliance_standards:
  AskUserQuestion:
    questions:
      - question: "What accessibility level should the application meet?"
        header: "Accessibility"
        multiSelect: false
        options:
          - label: "WCAG 2.1 Level AA"
            description: "Industry standard for public-facing apps"
          - label: "WCAG 2.1 Level A"
            description: "Minimum accessibility compliance"
          - label: "No formal requirement"
            description: "Best practices only, no formal standard"

  Store in session.nfr.accessibility = response
```

EXECUTE (Vague Term Detection and Resolution):
```
# Scan ALL captured NFRs for vague terms
vague_terms_detected = []
VAGUE_PATTERNS = ["fast", "scalable", "secure", "reliable", "performant", "responsive", "robust"]

FOR each nfr_field in session.nfr:
  IF any vague_term in nfr_field.value (case-insensitive):
    vague_terms_detected.append({field: nfr_field.name, term: matched_term})

IF len(vague_terms_detected) > 0:
  FOR each vague_item in vague_terms_detected:
    AskUserQuestion:
      questions:
        - question: "You mentioned '{vague_item.term}' for {vague_item.field}. Can you quantify that? For example: response time <500ms, handle 1000 concurrent users, 99.9% uptime."
          header: "Quantify: {vague_item.term}"
          multiSelect: false
          options:
            - label: "Let me specify a number"
              description: "I can provide a specific target"
            - label: "Use the standard recommendation"
              description: "Apply industry-standard targets for my domain"

    IF "Let me specify": capture and store quantified value
    IF "Use standard": apply domain-standard from requirements-elicitation-guide.md

  # Re-verify after resolution
  remaining_vague = scan_for_vague_terms(session.nfr)
  IF len(remaining_vague) > 0:
    # Document as ASSUMPTION with specific assumed value
    FOR each remaining in remaining_vague:
      remaining.assumed_value = domain_standard_for(remaining.field, session.domain)
      remaining.validation_flag = "ASSUMPTION - validate during architecture phase"
```

VERIFY: At least 1 NFR with quantified target captured.
IF `len(session.nfr) < 1`: HALT -- "Step 3.6: At least 1 non-functional requirement required. None captured."
IF any NFR value contains vague terms without quantified target or ASSUMPTION flag: HALT -- "Step 3.6: Vague NFR detected without quantification: '{nfr.field}' = '{nfr.value}'. All NFRs must have measurable targets."

Compile all NFRs into structured format:
```
session.nfr_requirements = {
  performance: {
    response_time: session.nfr.performance.response_time,
    concurrent_users: session.nfr.performance.concurrent_users
  },
  availability: session.nfr.availability,
  compliance: session.nfr.compliance,
  accessibility: session.nfr.accessibility or "best_practices_only",
  assumptions: [any items flagged as ASSUMPTION]
}
```

RECORD: Update checkpoint: `session.phases["03"].questions_answered += 4 + (1 if accessibility_asked else 0) + len(vague_terms_resolved)`; `session.completed_outputs.nfr_requirements = session.nfr_requirements`

---

### Step 3.7: MoSCoW Prioritization (Chain-of-Thought)

This step applies the Chain-of-Thought 4-Factor Prioritization from requirements-elicitation-workflow.md (Common Issues > Issue: Too Many Requirements > Chain-of-Thought Prioritization Guidance).

EXECUTE (Chain-of-Thought Analysis):
```
# Apply explicit reasoning to EVERY functional requirement

Display:
"Now let's prioritize all {len(session.functional_requirements)} requirements using MoSCoW prioritization.
I'll analyze each requirement across 4 factors and propose a priority."

FOR each requirement in session.functional_requirements:
  <thinking>
  Evaluating requirement: "{requirement.story}"
  Category: {requirement.category}

  Factor 1: Business Value
  - How critical is this to the stated business goals?
  - Business goals from Phase 02: {session.completed_outputs.business_goals}
  - Rating: [Critical | High | Medium | Low]
  - Reasoning: {explain why this rating}

  Factor 2: Technical Feasibility
  - Is this implementable within stated constraints?
  - Complexity tier: {session.completed_outputs.complexity_assessment.tier}
  - Rating: [Straightforward | Moderate | Complex | Requires Research]
  - Reasoning: {explain why this rating}

  Factor 3: Dependencies
  - Does this block other requirements?
  - Blocked by: {list of blocking requirements, if any}
  - Blocks: {list of requirements this blocks, if any}
  - Rating: [Blocks Many | Blocks Some | Independent | Blocked]

  Factor 4: User Impact
  - How many user personas benefit?
  - Personas from Phase 02: {session.completed_outputs.personas}
  - Rating: [All Personas | Primary Personas | Single Persona | Edge Case]
  - Reasoning: {explain why this rating}

  MoSCoW Assignment:
  - Must-Have: Critical business value + feasible + blocks other work OR all personas impacted
  - Should-Have: High business value + feasible + most personas benefit
  - Could-Have: Medium business value + no dependencies blocked + subset of personas
  - Won't-Have: Low value OR infeasible within constraints OR future scope

  ASSIGNED: {Must-Have | Should-Have | Could-Have | Won't-Have}
  </thinking>

  requirement.priority = assigned_priority
  requirement.priority_reasoning = {
    business_value: rating,
    feasibility: rating,
    dependencies: rating,
    user_impact: rating
  }
```

EXECUTE (Display Prioritized List):
```
# Group requirements by priority
must_haves = [r for r in session.functional_requirements WHERE r.priority == "Must-Have"]
should_haves = [r for r in session.functional_requirements WHERE r.priority == "Should-Have"]
could_haves = [r for r in session.functional_requirements WHERE r.priority == "Could-Have"]
wont_haves = [r for r in session.functional_requirements WHERE r.priority == "Won't-Have"]

Display:
"Proposed Prioritization:

Must-Have ({len(must_haves)} requirements):
{FOR each r in must_haves: "  - {r.id}: {r.story}"}

Should-Have ({len(should_haves)} requirements):
{FOR each r in should_haves: "  - {r.id}: {r.story}"}

Could-Have ({len(could_haves)} requirements):
{FOR each r in could_haves: "  - {r.id}: {r.story}"}

Won't-Have ({len(wont_haves)} requirements):
{FOR each r in wont_haves: "  - {r.id}: {r.story}"}"
```

EXECUTE (User Validation):
```
AskUserQuestion:
  questions:
    - question: "Does this prioritization look right? Any changes needed?"
      header: "Priority Validation"
      multiSelect: false
      options:
        - label: "Yes, looks good"
          description: "Proceed with this prioritization"
        - label: "Some adjustments needed"
          description: "I want to move some requirements between priorities"
        - label: "Major rework needed"
          description: "The priorities don't match my expectations"

IF response == "Some adjustments needed":
  AskUserQuestion:
    questions:
      - question: "Which requirements need priority changes?"
        header: "Adjustments"
        multiSelect: false
        options:
          - label: "Let me list the changes"
            description: "I'll specify which items to move"

  Capture user adjustments.
  Apply changes to session.functional_requirements[].priority.

  # Re-display updated prioritization for confirmation
  Display updated list.

  AskUserQuestion:
    questions:
      - question: "Updated prioritization correct now?"
        header: "Confirm"
        multiSelect: false
        options:
          - label: "Yes, confirmed"
            description: "Proceed with updated priorities"
          - label: "More changes needed"
            description: "Still needs adjustment"

  IF "More changes needed":
    # Allow one more round of adjustments, then proceed
    Capture and apply additional changes.

ELSE IF response == "Major rework needed":
  AskUserQuestion:
    questions:
      - question: "What is the most important capability for your MVP (minimum viable product)?"
        header: "MVP Core"
        multiSelect: false
        options:
          - label: "Let me describe the MVP scope"
            description: "I'll tell you what must be in version 1"

  Capture MVP scope description.
  Re-assign priorities: MVP items = Must-Have, everything else = Should-Have or Could-Have.
  Display updated list for confirmation.
```

VERIFY: All functional requirements have a MoSCoW priority assigned.
IF any requirement has `priority == null`: HALT -- "Step 3.7: Requirement '{requirement.id}' has no MoSCoW priority assigned."
IF user did not validate prioritization: HALT -- "Step 3.7: MoSCoW prioritization not validated by user."

RECORD: Update checkpoint: `session.phases["03"].questions_answered += 1 + (adjustment_questions if any)`; Update each requirement in `session.completed_outputs.functional_requirements` with priority field.

---

### Step 3.8: Context Window Check

EXECUTE:
```
IF estimated_context_usage > 70%:
  AskUserQuestion:
    questions:
      - question: "Context window is approximately {PERCENT}% full. Would you like to:"
        header: "Session"
        multiSelect: false
        options:
          - label: "Continue in this session"
            description: "Proceed to Phase 4 (Constitutional Compliance)"
          - label: "Save and continue later"
            description: "Create checkpoint and exit"

  IF response == "Save and continue later":
    # Write comprehensive checkpoint with ALL Phase 03 data
    Write(file_path="devforgeai/specs/ideation/${IDEATION_ID}.checkpoint.json", content=updated_checkpoint)

    # Verify checkpoint was written
    Glob(pattern="devforgeai/specs/ideation/${IDEATION_ID}.checkpoint.json")
    IF not found: HALT -- "Step 3.8: Checkpoint save failed."

    Display: "Session saved. Resume with: /ideate --resume ${IDEATION_ID}"
    EXIT skill

ELSE:
  Display: "Context window healthy. Proceeding to Phase 4."
```

VERIFY: Context window check was performed (either threshold check or healthy confirmation).
IF check was skipped: HALT -- "Step 3.8: Context Window Check not performed."

RECORD: Update checkpoint: `session.phases["03"].context_check_completed = true`

---

## Phase Exit Verification

Before transitioning to Phase 04, verify ALL exit criteria:

```
VERIFY_EXIT:
  CHECK: len(session.completed_outputs.functional_requirements) >= 5
    IF FAIL: HALT -- "Exit blocked: Less than 5 functional requirements. Found {count}."

  CHECK: ALL functional requirements have user story format ("As a ... I want to ... so that ...")
    IF FAIL: HALT -- "Exit blocked: Requirement '{id}' is not in user story format."

  CHECK: ALL functional requirements have MoSCoW priority assigned (priority != null)
    IF FAIL: HALT -- "Exit blocked: Requirement '{id}' has no MoSCoW priority."

  CHECK: len(session.completed_outputs.nfr_requirements) >= 1 with quantified target
    IF FAIL: HALT -- "Exit blocked: No non-functional requirements with quantified targets."

  CHECK: NO vague NFR terms remain
    scan_result = scan_for_vague_terms(session.completed_outputs.nfr_requirements)
    IF len(scan_result) > 0 AND no ASSUMPTION flag:
      HALT -- "Exit blocked: Vague NFR term '{term}' found in '{field}' without quantification."

  CHECK: len(session.completed_outputs.data_entities) >= 1
    IF FAIL: HALT -- "Exit blocked: No data entities identified."

  CHECK: ALL data entities have at least 1 attribute
    FOR each entity in session.completed_outputs.data_entities:
      IF len(entity.attributes) < 1:
        HALT -- "Exit blocked: Entity '{entity.name}' has no attributes."

  CHECK: session.completed_outputs.integrations is not null (list, can be empty)
    IF FAIL: HALT -- "Exit blocked: Integration requirements not captured (set to null)."

  CHECK: session.phases["03"].context_check_completed == true
    IF FAIL: HALT -- "Exit blocked: Context window check not completed."

  CHECK: session.phases["03"].questions_answered >= 10
    IF FAIL: HALT -- "Exit blocked: Minimum 10 questions required, only {count} answered."
```

Update checkpoint on successful exit:
```
checkpoint.progress.current_phase = 4
checkpoint.progress.phases_completed.append("03")
checkpoint.progress.completion_percentage = round(3/7 * 100)

Write(file_path="devforgeai/specs/ideation/${IDEATION_ID}.checkpoint.json", content=checkpoint)
```

VERIFY: Checkpoint file updated on disk with `current_phase = 4`.
IF write fails: HALT -- "Phase 03 exit checkpoint not saved."

Verify via Glob:
```
Glob(pattern="devforgeai/specs/ideation/${IDEATION_ID}.checkpoint.json")
```
IF not found: HALT -- "Phase 03 checkpoint was NOT saved to disk."

---

## Phase Transition Display

```
Display:
"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Phase 3 Complete: Requirements Elicitation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Domain: {session.domain}

Requirements by Priority:
  Must-Have:   {must_have_count} requirements
  Should-Have: {should_have_count} requirements
  Could-Have:  {could_have_count} requirements
  Won't-Have:  {wont_have_count} requirements
  Total:       {total_count} functional requirements

Data Entities: {entity_count} identified
  {FOR each entity: '- {entity.name} ({len(entity.attributes)} attributes)'}

Integrations: {integration_count} external services
  {FOR each integration: '- {integration.service} ({integration.data_flow})'}

Non-Functional Requirements:
  Performance: {nfr.performance.response_time.target} response, {nfr.performance.concurrent_users.target} users
  Availability: {nfr.availability.target} uptime
  Compliance: {nfr.compliance or 'None specified'}

Questions Asked This Phase: {session.phases['03'].questions_answered}

Proceeding to Phase 4: Constitutional Compliance...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"
```

---

## Phase 03 Checkpoint Update

After all steps complete, write the following to the checkpoint:

```json
{
  "progress": {
    "current_phase": 4,
    "phases_completed": ["...", "03"],
    "completion_percentage": 43
  },
  "phases": {
    "03": {
      "questions_answered": "{total_count}",
      "context_check_completed": true,
      "domain": "{session.domain}",
      "feature_categories_count": "{len(session.feature_categories)}",
      "functional_requirements_count": "{len(session.functional_requirements)}",
      "data_entities_count": "{len(session.data_entities)}",
      "integrations_count": "{len(session.integrations)}",
      "nfr_count": "{len(session.nfr_requirements)}",
      "moscow_validated": true
    }
  },
  "completed_outputs": {
    "domain": "{session.domain}",
    "feature_categories": "{session.feature_categories}",
    "functional_requirements": "{session.functional_requirements with priorities}",
    "data_entities": "{session.data_entities with attributes and relationships}",
    "integrations": "{session.integrations with data flow directions}",
    "nfr_requirements": "{session.nfr_requirements with quantified targets}"
  }
}
```

**VERIFY checkpoint write:** `Glob(pattern="devforgeai/specs/ideation/${IDEATION_ID}.checkpoint.json")`
IF not found: HALT -- "Phase 03 checkpoint was NOT saved."

---

## Common Issues and Recovery

| Issue | Symptom | Recovery |
|-------|---------|----------|
| Too many requirements (>50 user stories) | Discovery uncovered massive scope | Group into themes, apply MoSCoW to reduce Must-Haves to <20, propose phased implementation |
| Vague NFRs ("fast", "scalable") | User cannot quantify performance targets | Provide domain-standard examples, ask for order-of-magnitude, document as ASSUMPTION |
| Conflicting requirements | Requirement A contradicts Requirement B | AskUserQuestion to resolve: keep A, keep B, modify both, or mark as architecture constraint |
| Domain mismatch | Detected domain does not match actual project | Re-run Step 3.1 with user correction, reload domain-specific patterns |
| User fatigued by questions | Long session, many feature categories | Summarize progress, offer save-and-resume, reduce follow-up depth for remaining categories |
| No data entities identified | User thinks in terms of features, not data | Rephrase: "What information does your system need to remember?" Use domain examples |
| Too few functional requirements (<5) | Scope is narrow or user is being brief | Probe deeper into selected feature categories, ask about edge cases and admin features |
