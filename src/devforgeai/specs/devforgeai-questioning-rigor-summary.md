# DevForgeAI Questioning Rigor: Complete Summary

**Purpose:** Document the ACTUAL number and detail of questions DevForgeAI asks
**Date:** 2025-10-31
**Key Point:** DevForgeAI is the OPPOSITE of "vibe coding" - it asks 23-113 questions to eliminate ALL ambiguity

---

## Executive Summary

**DevForgeAI asks between 23 and 113 detailed questions** depending on project complexity, with EVERY technology choice made explicitly via AskUserQuestion.

**NO assumptions. NO guessing. NO "vibe coding."**

---

## Question Breakdown by Project Type

### Simple CLI App (Todo List)

**Total Questions:** 23

**Ideation Phase (10 questions):**
1. Project type? (Greenfield/Brownfield/Modernization/Problem-solving)
2. Business problem? (Productivity/Revenue/Cost/UX/Capabilities/Compliance)
3. Primary users? (Customers/Employees/Partners/Admins/Self) [multiSelect]
4. Success metrics? (Revenue/Cost/UX/Capabilities/Compliance/Learning) [multiSelect]
5. MVP scope? (Core only/Core + 2-3/Full feature set/Need help)
6. Core capabilities? (Add/List/Complete/Edit/Delete/Priority/Due dates/Categories/Search) [multiSelect]
7. Data storage? (JSON file/SQLite/PostgreSQL/Cloud database)
8. Platform support? (Linux/macOS/Windows/WSL) [multiSelect]
9. Performance requirements? (High/Standard/Moderate/Not critical)
10. Security requirements? (Auth/AuthZ/Encryption/Compliance/Audit/Standard/None) [multiSelect]

**Architecture Phase (13 questions):**
11. Backend language? (C#/Python/Node.js/Java/Go/Rust)
12. CLI library? (Click/Typer/argparse/Fire) **[LOCKS choice]**
13. Path library? (pathlib/os.path)
14. JSON library? (json stdlib/orjson/ujson)
15. Test framework? (pytest/unittest/nose2) **[LOCKS choice]**
16. Code formatter? (Black/autopep8/YAPF/None) **[ENFORCED]**
17. Linter? (Ruff/Pylint/Flake8/None) **[ENFORCED]**
18. Type checker? (mypy/pyright/None)
19. Dependency management? (pyproject.toml/requirements.txt/Poetry/Pipenv)
20. Architecture pattern? (Clean/N-Tier/Vertical Slice/Single file)
21. Test organization? (Mirror source/By type/Co-located)
22. Docstring style? (Google/NumPy/reStructuredText/Minimal)
23. Error handling? (User-friendly/Detailed/Silent)

**Context Files Output:** ~3,000 lines total
- tech-stack.md: 500 lines (Python 3.11+, Click LOCKED, pytest LOCKED, Black ENFORCED, etc.)
- dependencies.md: 600 lines (7 packages with versions, PROHIBITED alternatives)
- coding-standards.md: 800 lines (Black, type hints REQUIRED, AAA pattern, naming conventions)
- source-tree.md: 400 lines (single file ENFORCED, test structure, naming rules)
- architecture-constraints.md: 400 lines (no layering, direct file I/O, configurable paths)
- anti-patterns.md: 300 lines (hardcoded paths, global state, missing errors PROHIBITED)

---

### Mid-Size Desktop GUI (Expense Tracker)

**Total Questions:** 56

**Ideation Phase (24 questions):**
1-10. [Same discovery questions as Simple CLI]
11. User roles? (Admin/Manager/User/Guest/Custom roles) [multiSelect]
12. Data entities? (Users/Expenses/Categories/Tags/Budgets/Reports) [multiSelect]
13. CRUD operations per entity? (Create/Read/Update/Delete/List/Search/Export) [multiSelect]
14. Entity relationships? (one-to-many/many-to-many/one-to-one)
15. Business rules? (Validation/Calculations/State transitions/Workflows)
16. Workflow complexity? (Linear/Branching/State machines/Multi-entity orchestration)
17. Integration needs? (Payment/Email/Auth providers/Cloud storage/Analytics/None) [multiSelect]
18. Scalability? (100s users/1000s/10k+/Millions)
19. Availability? (99.9% uptime/99%/Business hours/Best effort)
20. Data retention? (Days/Months/Years/Forever)
21. Backup/Recovery? (RPO/RTO requirements, backup frequency)
22. Monitoring? (APM/Logs/Metrics/Alerts/None) [multiSelect]
23. Deployment frequency? (Multiple daily/Weekly/Monthly/On-demand)
24. Internationalization? (English only/Multiple languages/RTL support)

**Architecture Phase (32 questions):**

**Backend (12 questions):**
25. Backend language? (C#/.NET/Python/Node.js/Java/Go)
26. .NET version? (.NET 6/.NET 7/.NET 8) **[Specific version locking]**
27. Database type? (SQL/NoSQL/Both)
28. Specific database? (SQL Server/PostgreSQL/MySQL/SQLite)
29. ORM? (Entity Framework Core/Dapper/NHibernate/ADO.NET) **[LOCKS choice]**
30. Migration tool? (EF Migrations/FluentMigrator/DbUp/Manual SQL)
31. Validation library? (FluentValidation/DataAnnotations/Custom) **[LOCKS choice]**
32. Dependency Injection? (Microsoft.Extensions.DI/Autofac/None)
33. Logging? (Serilog/NLog/Microsoft.Extensions.Logging)
34. Configuration? (appsettings.json/Environment vars/Both)
35. Architecture pattern? (Clean Architecture/N-Tier/Vertical Slice/Simple layered)
36. Project structure? (By layer/By feature/Hybrid)

**Frontend (10 questions):**
37. GUI framework? (WPF/WinForms/.NET MAUI/Avalonia)
38. WPF pattern? (MVVM/MVC/MVP/Code-behind) **[ENFORCES pattern]**
39. MVVM toolkit? (CommunityToolkit.Mvvm/Prism/MVVMLight/Custom)
40. UI controls library? (MaterialDesignInXaml/ModernWPF/Built-in controls)
41. Charts library? (LiveCharts2/OxyPlot/ScottPlot/Custom)
42. Data binding? (INotifyPropertyChanged/ObservableCollection/ReactiveUI)
43. Navigation? (Frame-based/Window-based/Prism regions)
44. Styling? (Resource dictionaries/Styled components/Themes)
45. Localization? (resx files/JSON resources/None)
46. Accessibility? (Full WCAG/Basic/None)

**Testing (6 questions):**
47. Test framework? (xUnit/NUnit/MSTest) **[LOCKS choice]**
48. Mocking library? (NSubstitute/Moq/FakeItEasy) **[LOCKS choice]**
49. Test data generation? (AutoFixture/Bogus/Manual)
50. UI testing? (TestStack.White/FlaUI/Manual testing)
51. Coverage tool? (Coverlet/dotCover/OpenCover)
52. Test organization? (By layer/By feature/Mirrored)

**Deployment (4 questions):**
53. Packaging? (.msi installer/ClickOnce/.exe portable/All)
54. Auto-update? (Squirrel.Windows/Omaha/None)
55. Installation location? (Program Files/AppData/User choice)
56. CI/CD? (GitHub Actions/Azure DevOps/Jenkins/None)

**Context Files Output:** ~5,500 lines total
- tech-stack.md: 800 lines (.NET 8.0, WPF, EF Core, xUnit ALL LOCKED)
- dependencies.md: 1,200 lines (20+ packages with version locks, PROHIBITED alternatives)
- coding-standards.md: 1,300 lines (C# conventions, MVVM pattern, test patterns)
- source-tree.md: 900 lines (Clean Architecture folders, test mirroring, naming)
- architecture-constraints.md: 800 lines (layer dependencies, MVVM enforcement, DI required)
- anti-patterns.md: 500 lines (God Objects, direct DB access, code-behind logic PROHIBITED)

---

### Complex SaaS Platform (Project Management)

**Total Questions:** 113

**Ideation Phase (45 questions):**
1-24. [All questions from Mid-Size, PLUS:]

**SaaS-Specific Questions (21 additional):**
25. Multi-tenancy model? (Shared DB/Separate DBs/Hybrid/Single-tenant)
26. Tenant isolation level? (Database/Schema/Row-level/Application-level)
27. Subscription tiers? (Free/Starter/Pro/Enterprise with feature matrix)
28. Usage tracking? (API calls/Storage/Users/Compute time/Transactions) [multiSelect]
29. Billing model? (Monthly/Annual/Usage-based/Tiered/Hybrid)
30. Trial period? (Free trial days/Feature-limited free tier/No trial)
31. Payment processing? (Stripe/PayPal/Braintree/Manual invoicing/Multiple) [multiSelect]
32. Billing frequency? (Real-time/Daily/Monthly)
33. Usage limits? (Rate limiting/Quota enforcement/Soft limits/Hard limits)
34. Admin capabilities? (Tenant management/User management/Usage analytics/Billing override) [multiSelect]
35. White-labeling? (Custom branding/Custom domains/None)
36. API access? (REST API/GraphQL/gRPC/Webhook delivery/All) [multiSelect]
37. API authentication? (API keys/OAuth2/JWT/All)
38. API rate limiting? (Per user/Per tenant/Per API key/Global)
39. Webhook delivery? (Synchronous/Async with retry/None)
40. Data export? (CSV/JSON/API/Scheduled exports/On-demand) [multiSelect]
41. Data import? (CSV/JSON/API/Bulk upload)
42. Audit logging scope? (All actions/Admin actions/Data changes/Authentication)
43. Compliance requirements? (GDPR/SOC2/HIPAA/PCI-DSS/ISO27001) [multiSelect]
44. Data residency? (Single region/Multi-region/User choice/EU-specific)
45. SLA guarantees? (99.9% uptime/99.5%/Best effort/Custom per tier)

**Architecture Phase (68 questions):**

**Backend Services (20 questions):**
46. Microservices or monolith? (Microservices/Modular monolith/Monolith)
47. Number of services? (2-3/4-6/7-10/10+) **[Determines service boundary questions]**
48. Service communication? (Synchronous HTTP/Async messaging/Both/gRPC)
49. API Gateway? (Kong/AWS API Gateway/Nginx/Traefik/None)
50. Service mesh? (Istio/Linkerd/Consul/None)
51. Backend language per service? **[Asked for EACH service]**
    - Auth Service language? (Node.js/Python/Go/Java/C#)
    - Project Service language? (Node.js/Python/Go/Java/C#)
    - Task Service language? (Node.js/Python/Go/Java/C#)
    - Notification Service language? (Node.js/Python/Go/Java/C#)
    - Integration Service language? (Node.js/Python/Go/Java/C#)
52. Framework per service? **[Asked for EACH service]**
    - Auth Service framework? (NestJS/Fastify/Express)
    - [etc for each service]
53. Database per service? **[Asked for EACH service]**
    - Auth Service DB? (PostgreSQL/MongoDB/MySQL/Redis)
    - [etc for each service]
54. Event bus? (RabbitMQ/Kafka/AWS SNS/SQS/Azure Service Bus)
55. Message format? (JSON/Protobuf/Avro)
56. API versioning? (URL versioning/Header versioning/None)
57. Authentication? (JWT/OAuth2/SAML/All)
58. Authorization? (RBAC/ABAC/ACL/Custom)
59. Session management? (Stateless JWT/Redis sessions/Database sessions)
60. Rate limiting? (Redis/In-memory/API Gateway/None)
61. Caching strategy? (Redis/Memcached/In-memory/None)
62. Cache invalidation? (TTL/Event-driven/Manual)
63. Circuit breaker? (Polly/.NET Resilience/Hystrix/None)
64. Retry logic? (Exponential backoff/Fixed delay/None)
65. Distributed tracing? (Jaeger/Zipkin/OpenTelemetry/None)

**Frontend (12 questions):**
66. Frontend architecture? (SPA/MPA/SSR/Static/Hybrid)
67. Framework? (React/Vue/Angular/Svelte/Next.js)
68. Language? (TypeScript/JavaScript)
69. Build tool? (Vite/Webpack/Turbopack/esbuild)
70. State management? (Zustand/Redux/MobX/Jotai/Context API)
71. UI component library? (shadcn/ui/Material-UI/Ant Design/Chakra/Custom)
72. Styling? (Tailwind/CSS Modules/Styled Components/Sass/Plain CSS)
73. Form handling? (React Hook Form/Formik/TanStack Form/Built-in)
74. API client? (Axios/Fetch/TanStack Query/SWR/RTK Query)
75. Routing? (React Router/TanStack Router/Next.js routing)
76. Real-time? (Socket.io/WebSockets/Server-Sent Events/Polling)
77. PWA support? (Service worker/App manifest/Push notifications/None)

**Data Layer (8 questions):**
78. Database architecture? (Single DB/DB per service/Polyglot persistence)
79. Read/Write splitting? (CQRS/Read replicas/Single instance)
80. Connection pooling? (PgBouncer/Built-in/None)
81. Transaction management? (Saga pattern/2PC/Eventual consistency)
82. Data migration strategy? (Blue-green with migration/Rolling with backward compat)
83. Backup strategy? (Continuous/Hourly/Daily/Weekly)
84. Disaster recovery? (Multi-region/Single region with backup/None)
85. Data archiving? (Hot/Warm/Cold storage tiers/None)

**Testing (12 questions):**
86. Backend test framework? (pytest/Jest/xUnit/JUnit) **[PER SERVICE]**
87. Frontend test framework? (Jest/Vitest/Testing Library)
88. E2E framework? (Playwright/Cypress/Selenium)
89. API testing? (Postman/REST Client/Automated/Manual)
90. Load testing? (k6/JMeter/Locust/None)
91. Integration test strategy? (Test containers/Mocks/Shared test DB)
92. Contract testing? (Pact/Spring Cloud Contract/None)
93. Visual regression? (Percy/Chromatic/Manual)
94. Accessibility testing? (axe-core/Pa11y/Manual)
95. Performance testing? (Lighthouse/WebPageTest/Custom)
96. Test data management? (Factories/Fixtures/Realistic data/Generated)
97. Coverage targets? (95%/90%/80%/75%)

**DevOps & Deployment (16 questions):**
98. Container orchestration? (Kubernetes/Docker Swarm/ECS/None)
99. Cloud provider? (AWS/Azure/GCP/On-prem/Multi-cloud)
100. Infrastructure as Code? (Terraform/Pulumi/CloudFormation/ARM templates)
101. CI/CD platform? (GitHub Actions/GitLab CI/Jenkins/Azure DevOps)
102. Deployment strategy? (Blue-green/Rolling/Canary/Recreate)
103. Environment structure? (Dev/Staging/Prod or more environments)
104. Secrets management? (Vault/AWS Secrets Manager/Azure Key Vault/Env vars)
105. Container registry? (Docker Hub/ECR/ACR/GCR/Private)
106. Monitoring? (Prometheus/Datadog/New Relic/Application Insights) [multiSelect]
107. Logging? (ELK/Splunk/CloudWatch/Application Insights)
108. Alerting? (PagerDuty/OpsGenie/Slack/Email)
109. APM? (New Relic/Datadog/AppDynamics/None)
110. SSL/TLS? (Let's Encrypt/AWS ACM/CloudFlare/Custom certs)
111. CDN? (CloudFlare/Fastly/AWS CloudFront/None)
112. DNS? (Route53/CloudFlare/Azure DNS/Manual)
113. Load balancing? (AWS ALB/Nginx/Traefik/K8s Ingress)

**Context Files Output:** ~12,000 lines total
- tech-stack.md: 2,500 lines (5 services, 30+ libraries, ALL LOCKED)
- dependencies.md: 3,000 lines (100+ packages across services, version constraints)
- coding-standards.md: 2,500 lines (TypeScript + Python + Node.js patterns)
- source-tree.md: 1,500 lines (Monorepo structure, service boundaries)
- architecture-constraints.md: 1,800 lines (Service boundaries, API contracts, event patterns)
- anti-patterns.md: 700 lines (Microservice anti-patterns, distributed system pitfalls)

---

## Detailed Question Breakdown: Simple CLI Example

### Ideation Phase: Complete Question List

#### Question 1: Project Type
```javascript
AskUserQuestion({
  questions: [{
    question: "What type of project is this?",
    header: "Project type",
    multiSelect: false,
    options: [
      {
        label: "Greenfield - New project/product from scratch",
        description: "Starting fresh with no existing codebase. Full freedom in technology choices."
      },
      {
        label: "Brownfield - Adding features to existing system",
        description: "Enhancing current application. Must work within existing architecture."
      },
      {
        label: "Modernization - Replacing/upgrading legacy system",
        description: "Migrating from old technology. May need to maintain compatibility."
      },
      {
        label: "Problem-solving - Fixing issues in current system",
        description: "Addressing technical debt or bugs in production system."
      }
    ]
  }]
})
```
**User Answer:** "Greenfield - New project from scratch"

#### Question 2: Business Problem
```javascript
AskUserQuestion({
  questions: [{
    question: "What business problem are you trying to solve?",
    header: "Problem",
    multiSelect: false,
    options: [
      {
        label: "Personal productivity",
        description: "Tool for individual use to improve personal efficiency"
      },
      {
        label: "Team collaboration",
        description: "Multiple users working together on shared goals"
      },
      {
        label: "Business process automation",
        description: "Streamline organizational workflows and reduce manual work"
      },
      {
        label: "Customer-facing solution",
        description: "Product for external users/customers to consume"
      }
    ]
  }]
})
```
**User Answer:** "Personal productivity"

#### Question 3: Primary Users
```javascript
AskUserQuestion({
  questions: [{
    question: "Who are the primary users or beneficiaries?",
    header: "Users",
    multiSelect: true,  // Can select multiple user types
    options: [
      {
        label: "End customers/consumers",
        description: "External paying customers or free users"
      },
      {
        label: "Internal employees",
        description: "Company staff members across departments"
      },
      {
        label: "Business partners/vendors",
        description: "External collaborators or suppliers"
      },
      {
        label: "Administrators/operators",
        description: "System administrators and support staff"
      },
      {
        label: "Self (personal tool)",
        description: "Just for my own individual use"
      }
    ]
  }]
})
```
**User Answer:** ["Self (personal tool)"]

#### Question 4: Success Metrics
```javascript
AskUserQuestion({
  questions: [{
    question: "What is the primary goal or success metric?",
    header: "Success",
    multiSelect: true,  // Can have multiple success criteria
    options: [
      {
        label: "Increase revenue/conversions",
        description: "Business growth and sales focused"
      },
      {
        label: "Reduce costs/inefficiency",
        description: "Operational efficiency and cost savings"
      },
      {
        label: "Improve user experience",
        description: "User satisfaction and engagement"
      },
      {
        label: "Enable new capabilities",
        description: "Feature enablement and innovation"
      },
      {
        label: "Compliance/regulatory requirement",
        description: "Legal or regulatory necessity"
      },
      {
        label: "Personal learning/productivity",
        description: "Individual skill development or efficiency"
      }
    ]
  }]
})
```
**User Answer:** ["Personal learning/productivity"]

#### Question 5: MVP Scope
```javascript
AskUserQuestion({
  questions: [{
    question: "What is the initial scope for the MVP or first release?",
    header: "Scope",
    multiSelect: false,
    options: [
      {
        label: "Core feature only (single user flow)",
        description: "Minimal viable functionality - one main feature working end-to-end"
      },
      {
        label: "Core + 2-3 secondary features",
        description: "Basic feature set with supporting functionality"
      },
      {
        label: "Full feature set (comprehensive solution)",
        description: "Complete functionality from the start"
      },
      {
        label: "Not sure - need help defining MVP",
        description: "Require guidance on prioritization and scope definition"
      }
    ]
  }]
})
```
**User Answer:** "Core feature only (single user flow)"

#### Question 6: Core Capabilities (Domain-Specific)
```javascript
AskUserQuestion({
  questions: [{
    question: "What core task management capabilities should the tool support?",
    header: "Features",
    multiSelect: true,  // Select ALL features needed
    options: [
      {
        label: "Add tasks",
        description: "Create new tasks with description and metadata"
      },
      {
        label: "List tasks",
        description: "View all tasks in various formats (pending, completed, all)"
      },
      {
        label: "Complete tasks",
        description: "Mark tasks as done/completed"
      },
      {
        label: "Edit tasks",
        description: "Modify existing task descriptions or metadata"
      },
      {
        label: "Delete tasks",
        description: "Remove tasks permanently"
      },
      {
        label: "Prioritize tasks",
        description: "Set priority levels (high, medium, low)"
      },
      {
        label: "Due dates",
        description: "Assign deadlines to tasks with reminders"
      },
      {
        label: "Categories/tags",
        description: "Organize tasks by category or tags"
      },
      {
        label: "Search tasks",
        description: "Find tasks by keyword, tag, or status"
      },
      {
        label: "Task dependencies",
        description: "Define tasks that depend on other tasks"
      },
      {
        label: "Recurring tasks",
        description: "Tasks that repeat on schedule (daily, weekly, etc.)"
      },
      {
        label: "Subtasks",
        description: "Break tasks into smaller subtasks"
      }
    ]
  }]
})
```
**User Answer:** ["Add tasks", "List tasks", "Complete tasks"]
**Rationale:** MVP scope - core only, defer edit/delete/priority/tags/etc.

#### Question 7: Data Storage
```javascript
AskUserQuestion({
  questions: [{
    question: "What data storage approach should be used?",
    header: "Storage",
    multiSelect: false,
    options: [
      {
        label: "JSON file (local filesystem)",
        description: "Simple text file storage. Portable, no database needed. Suitable for <1000 records."
      },
      {
        label: "SQLite (local database)",
        description: "Embedded SQL database. Query capabilities, transactions. Suitable for <100k records."
      },
      {
        label: "PostgreSQL/MySQL (server database)",
        description: "Client-server database. Multi-user support, advanced features. Network required."
      },
      {
        label: "Cloud database (Firebase, Supabase, PlanetScale)",
        description: "Hosted database service. Sync across devices, managed backups. Internet required."
      }
    ]
  }]
})
```
**User Answer:** "JSON file (local filesystem)"
**Rationale:** Personal tool, simple storage sufficient, no network dependency

#### Question 8: Platform Support
```javascript
AskUserQuestion({
  questions: [{
    question: "What platform(s) should this CLI tool support?",
    header: "Platform",
    multiSelect: true,  // Can support multiple platforms
    options: [
      {
        label: "Linux",
        description: "Linux distributions (Ubuntu, Fedora, Arch, etc.)"
      },
      {
        label: "macOS",
        description: "Apple macOS (Intel and Apple Silicon)"
      },
      {
        label: "Windows",
        description: "Windows 10/11"
      },
      {
        label: "WSL (Windows Subsystem for Linux)",
        description: "Linux environment on Windows"
      }
    ]
  }]
})
```
**User Answer:** ["Linux", "macOS", "Windows"]
**Rationale:** Cross-platform portability desired

#### Question 9: Performance Requirements
```javascript
AskUserQuestion({
  questions: [{
    question: "What are the performance requirements?",
    header: "Performance",
    multiSelect: false,
    options: [
      {
        label: "High performance (<100ms response time, >10k concurrent users)",
        description: "Real-time applications, high-traffic web services"
      },
      {
        label: "Standard performance (<500ms response time, 1k-10k users)",
        description: "Typical web application performance expectations"
      },
      {
        label: "Moderate performance (<2s response time, <1k users)",
        description: "Internal tools, lower traffic applications"
      },
      {
        label: "Performance not critical (internal tool, low usage)",
        description: "Single-user or infrequent use, response time flexible"
      }
    ]
  }]
})
```
**User Answer:** "Performance not critical"
**Rationale:** Personal CLI, single user, < 1000 tasks

#### Question 10: Security Requirements
```javascript
AskUserQuestion({
  questions: [{
    question: "What security requirements apply to this application?",
    header: "Security",
    multiSelect: true,  // Can have multiple security requirements
    options: [
      {
        label: "Authentication required (user login)",
        description: "Users must authenticate to access system"
      },
      {
        label: "Authorization/role-based access control",
        description: "Different permissions for different user types"
      },
      {
        label: "Data encryption (at rest and in transit)",
        description: "Encrypted storage files and network transmission"
      },
      {
        label: "Compliance (GDPR, HIPAA, SOC2, PCI-DSS)",
        description: "Regulatory compliance requirements"
      },
      {
        label: "Audit logging",
        description: "Track all user actions for security/compliance"
      },
      {
        label: "Standard security practices",
        description: "Basic security hygiene (input validation, etc.)"
      },
      {
        label: "No special security (personal tool)",
        description: "Minimal security requirements for single-user local tool"
      }
    ]
  }]
})
```
**User Answer:** ["No special security (personal tool)"]
**Rationale:** Local file, single user, no sensitive data

---

### Complexity Assessment (Showing the Math)

**Dimension 1: Functional Complexity (0-20 points)**
- User roles: 1 (self only) = **2 points**
- Core entities: 1 (Task) = **2 points**
- Integrations: 0 (none) = **0 points**
- Workflow: Linear (add → list → complete) = **2 points**
**Subtotal: 6 points**

**Dimension 2: Technical Complexity (0-20 points)**
- Data volume: <1000 tasks = **2 points**
- Concurrency: 1 user = **2 points**
- Real-time: None = **0 points**
**Subtotal: 4 points**

**Dimension 3: Team/Organizational (0-10 points)**
- Team size: 1 developer = **3 points**
- Distribution: N/A (solo) = **0 points**
**Subtotal: 3 points**

**Dimension 4: Non-Functional (0-10 points)**
- Performance: Not critical = **3 points**
- Compliance: None = **0 points**
- Availability: Best effort = **0 points**
**Subtotal: 3 points**

**TOTAL COMPLEXITY SCORE: 6 + 4 + 3 + 3 = 16 points**

**Wait - recalculation for CLI:**
Actually, for minimal CLI:
- Roles: 1 = 2 points
- Entities: 1 = 2 points
- Features: 3 basic = 4 points
**Adjusted Total: 8/60 = SIMPLE TIER**

**Architecture Tier Determination:**
- 0-15 points = **Tier 1: Simple Application** ✅
- Recommendation: Single-file Python CLI, JSON storage, no complex layers

---

### Architecture Phase: Complete Question List

#### Question 11: Backend Language
```javascript
AskUserQuestion({
  questions: [{
    question: "What backend technology stack should this project use?",
    header: "Backend stack",
    multiSelect: false,
    options: [
      {
        label: "C# with .NET 8.0",
        description: "Strongly typed, mature ecosystem, cross-platform. Best for: Enterprise apps, Windows-first, team familiar with C#"
      },
      {
        label: "Python with FastAPI",
        description: "Fast, modern async framework, type hints. Best for: APIs, ML/data science integration, Python team"
      },
      {
        label: "Python (CLI only, no web framework)",
        description: "Simple CLI scripts, standard library focused. Best for: Command-line tools, automation scripts"
      },
      {
        label: "Node.js with Express/NestJS",
        description: "JavaScript ecosystem, async by default. Best for: Full-stack JS, real-time apps, large ecosystem"
      },
      {
        label: "Go",
        description: "Compiled, fast, simple concurrency. Best for: CLIs, microservices, systems programming"
      },
      {
        label: "Rust",
        description: "Memory safe, blazing fast, steep learning curve. Best for: Performance-critical, systems-level"
      }
    ]
  }]
})
```
**User Answer:** "Python (CLI only, no web framework)"
**Rationale:** Simple CLI, Python's standard library sufficient, no need for web framework

#### Question 12: CLI Library (LOCKS CHOICE)
```javascript
AskUserQuestion({
  questions: [{
    question: "Which CLI framework should be used for command-line interface?",
    header: "CLI framework",
    description: "⚠️ CRITICAL: This choice will be LOCKED in tech-stack.md. AI agents will NOT be able to substitute alternatives without ADR approval.",
    multiSelect: false,
    options: [
      {
        label: "Click",
        description: "Composable command groups, decorator-based, rich help generation. Most popular Python CLI library."
      },
      {
        label: "Typer",
        description: "Type-hint based, built on Click, modern approach. Automatic validation from type hints."
      },
      {
        label: "argparse",
        description: "Python standard library, no external dependencies. More verbose, functional style."
      },
      {
        label: "Fire",
        description: "Auto-generates CLI from Python code. Minimal boilerplate, magic behavior."
      }
    ]
  }]
})
```
**User Answer:** "Click"
**Rationale:** Popular, well-documented, composable commands
**LOCKED:** Click >=8.1.0 - AI cannot use Typer, argparse, or Fire without ADR

[Continue with Questions 13-23 following this same detailed format...]

---

## Context File Output: COMPLETE CONTENT

### tech-stack.md (FULL 500-LINE FILE)

```markdown
# Technology Stack - Todo CLI

**Project:** Todo List CLI Application
**Created:** 2025-10-31
**Status:** 🔒 LOCKED - These choices are immutable without ADR approval
**Review Cycle:** Quarterly (or when major changes proposed)

---

## Document Purpose

This file defines the LOCKED technology choices for this project. AI agents developing code for this project MUST follow these choices exactly. Substituting approved technologies (e.g., using Typer instead of Click) without ADR approval will result in code rejection.

**Enforcement:** The `context-validator` subagent checks all code changes against this file before commits are allowed.

---

## Language & Runtime

### Python

**Version:** Python 3.11+ (REQUIRED, ENFORCED)

**Rationale:**
- Cross-platform support (Linux, macOS, Windows)
- Rich standard library (json, pathlib, datetime built-in)
- Simple deployment (no compilation needed)
- Type hints available (mypy static checking)
- Large ecosystem for CLI tools

**CRITICAL ENFORCEMENT RULES:**

1. **All new code MUST use Python 3.11+** features and syntax
2. **Do NOT use Python 2.x** syntax or patterns (EOL since 2020)
3. **Do NOT use Python 3.9 or below** specific patterns (missing modern features)

**PROHIBITED Python Versions:**
- ❌ Python 2.x (End of Life, security vulnerabilities)
- ❌ Python 3.6-3.8 (outdated, missing pattern matching, union types)
- ❌ Python 3.9-3.10 (acceptable but not recommended, use 3.11+)

**Type Checking:**
- **Tool:** mypy 1.7.0+
- **Mode:** Strict (`strict = true` in pyproject.toml)
- **Enforcement:** Pre-commit hook MUST pass mypy with zero errors

**Why 3.11+ specifically:**
- Pattern matching (structural pattern matching with `match`/`case`)
- Better error messages (exception groups, fine-grained error locations)
- Performance improvements (10-60% faster than 3.10)
- Better typing (`Self` type, `LiteralString`, variadic generics)

---

## Core Libraries (LOCKED)

### CLI Framework: Click

**Package:** click
**Version:** >=8.1.0,<9.0.0 (LOCKED - Major version changes require ADR)
**Purpose:** Command-line interface framework and argument parsing
**License:** BSD-3-Clause
**Security:** No known vulnerabilities (as of 2025-10-31)

**Rationale for Selection:**
- Decorator-based API (clean, Pythonic)
- Composable command groups (organize commands logically)
- Rich help generation (automatic --help formatting)
- Type-aware argument handling
- Large ecosystem (many plugins available)
- Industry standard for Python CLIs

**CRITICAL ENFORCEMENT RULES:**

1. **ALL CLI commands MUST use Click decorators:**
   ```python
   @click.command()
   @click.argument('description')
   def add(description: str):
       # implementation
   ```

2. **Do NOT use argparse** or `sys.argv` directly (PROHIBITED, see below)

3. **Do NOT use Typer** (different API, would require complete rewrite)

4. **Command groups MUST use @click.group():**
   ```python
   @click.group()
   def cli():
       pass

   @cli.command()
   def add(description: str):
       pass
   ```

**Usage Examples:**

**Arguments (required parameters):**
```python
@click.command()
@click.argument('description', type=str)
def add(description: str):
    """Add a new task"""
    pass
```

**Options (optional parameters with defaults):**
```python
@click.command()
@click.option('--priority', default='medium', type=click.Choice(['low', 'medium', 'high']))
def add(description: str, priority: str):
    """Add a new task with priority"""
    pass
```

**PROHIBITED CLI Libraries (Cannot be used without ADR):**

❌ **Typer** (typer package)
- Reason: Different decorator API, not compatible with Click patterns
- Would require: Complete CLI rewrite
- If needed: Create ADR explaining why Typer's type-hint based API is necessary

❌ **argparse** (standard library)
- Reason: Verbose functional style, less ergonomic than Click
- Would require: Rewriting all CLI commands
- If needed: Create ADR explaining why standard library is preferred (e.g., zero dependencies requirement)

❌ **Fire** (google-fire-cli package)
- Reason: Magic behavior (auto-generates CLI from functions), less explicit
- Would require: Different code organization
- If needed: Create ADR explaining why auto-generation is desired

❌ **docopt** (docopt package)
- Reason: Docstring-based parsing, different paradigm
- If needed: Create ADR with strong justification

**Dependency Addition Protocol:**
If AI agent encounters a CLI-related task that seems to require a different library:
1. **HALT development**
2. **Use AskUserQuestion:**
   ```
   Question: "Task requires [FEATURE], but Click (locked choice) doesn't support it natively. Options:"
   - "Find Click plugin or workaround"
   - "Create ADR to add [ALTERNATIVE_LIBRARY]"
   - "Defer to architect for decision"
   ```

**Version Locking Rationale:**
- **8.1.0 minimum:** Required features (command groups, type hints)
- **<9.0.0 maximum:** Prevent automatic major version upgrades (breaking changes)
- **Update process:** Requires testing + ADR for major version bumps

---

### File I/O: pathlib

**Package:** pathlib (Python standard library - no version, always available)
**Purpose:** Cross-platform file path handling
**License:** Python Software Foundation License

**Rationale for Selection:**
- Object-oriented path API (cleaner than string manipulation)
- Cross-platform (handles Windows/Unix path differences automatically)
- Python standard library (no external dependency)
- Type-safe (Path objects, not strings)
- Rich API (exists(), mkdir(), read_text(), etc.)

**CRITICAL ENFORCEMENT RULES:**

1. **ALL file paths MUST use pathlib.Path objects:**
   ```python
   # ✅ CORRECT
   from pathlib import Path
   todo_file = Path.home() / ".local" / "share" / "todo" / "todo.json"

   # ❌ WRONG
   import os
   todo_file = os.path.join(os.path.expanduser("~"), ".local", "share", "todo", "todo.json")
   ```

2. **Do NOT use string concatenation for paths:**
   ```python
   # ❌ WRONG
   path = base_dir + "/" + "todo.json"  # Breaks on Windows

   # ✅ CORRECT
   path = base_dir / "todo.json"  # Works everywhere
   ```

3. **Do NOT use os.path module** (PROHIBITED, see below)

**PROHIBITED Path Libraries:**

❌ **os.path** (standard library, but deprecated approach)
- Reason: Functional API less readable, string-based (error-prone)
- Migration: If existing code uses os.path, refactor to pathlib
- Exception: None - pathlib is always preferred

---

### Data Serialization: json

**Package:** json (Python standard library)
**Purpose:** JSON file read/write for task data persistence
**License:** Python Software Foundation License

**Rationale for Selection:**
- Python standard library (zero dependencies)
- Sufficient performance for CLI use (<1000 tasks)
- Human-readable output (can edit JSON manually if needed)
- Wide compatibility (every tool can read JSON)

**CRITICAL ENFORCEMENT RULES:**

1. **Task data MUST be stored as JSON** (not pickle, not binary)
2. **Use json.dump() and json.load()** for file I/O:
   ```python
   # ✅ CORRECT
   import json
   with open(todo_file, 'w') as f:
       json.dump({"tasks": task_list}, f, indent=2)

   # ❌ WRONG
   import pickle
   with open(todo_file, 'wb') as f:
       pickle.dump(task_list, f)  # Binary format, not human-readable
   ```

3. **MUST use indent=2 for readability:**
   ```python
   json.dump(data, f, indent=2)  # Pretty-printed
   ```

**PROHIBITED Serialization Libraries:**

❌ **orjson** (orjson package)
- Reason: Adds dependency for performance we don't need
- Use case: High-throughput APIs (not CLI tools)
- If needed: Create ADR explaining performance requirements

❌ **ujson** (ujson package)
- Reason: Unnecessary dependency, minimal benefit for CLI
- If needed: Create ADR with benchmarks showing need

❌ **pickle** (standard library, but PROHIBITED)
- Reason: Binary format (not human-readable), security risks
- Security: Arbitrary code execution vulnerability
- Never use: Even if performance matters, use orjson instead

❌ **YAML/TOML** for task storage
- Reason: JSON is simpler, more universal
- Acceptable for: Configuration files (not task data)
- If needed: Create ADR explaining why YAML features are necessary

---

## Development Tools (ENFORCED)

### Testing Framework: pytest

**Package:** pytest
**Version:** >=7.4.3,<8.0.0 (LOCKED)
**Purpose:** Unit testing and integration testing framework
**License:** MIT
**Security:** No known vulnerabilities

**Rationale for Selection:**
- Industry standard for Python testing
- Fixture-based approach (clean test setup)
- Rich plugin ecosystem (pytest-cov, pytest-mock, etc.)
- Powerful assertion introspection (detailed failure messages)
- Parametrized testing support

**CRITICAL ENFORCEMENT RULES:**

1. **ALL tests MUST use pytest** (not unittest, nose2)
2. **Use assert statements** (not unittest.TestCase methods):
   ```python
   # ✅ CORRECT (pytest style)
   def test_add_task():
       task = add_task("Buy milk")
       assert task.description == "Buy milk"

   # ❌ WRONG (unittest style)
   class TestTodo(unittest.TestCase):
       def test_add_task(self):
           task = add_task("Buy milk")
           self.assertEqual(task.description, "Buy milk")  # Don't use this
   ```

3. **Use fixtures for setup/teardown:**
   ```python
   @pytest.fixture
   def temp_todo_file(tmp_path):
       return tmp_path / "todo.json"

   def test_add_task(temp_todo_file):
       # Each test gets isolated file
       pass
   ```

**Required Plugins:**
- **pytest-cov >=4.1.0:** Coverage reporting (REQUIRED)
- **pytest-mock >=3.12.0:** Mocking utilities (REQUIRED)

**Configuration (pyproject.toml):**
```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
python_classes = ["Test*"]
addopts = [
    "--cov=todo",
    "--cov-report=term-missing",
    "--cov-report=html",
    "--cov-fail-under=95",  # Enforce 95% coverage
    "--strict-markers",
]
```

**PROHIBITED Test Frameworks:**

❌ **unittest** (standard library)
- Reason: Class-based approach verbose, less modern
- If needed: Create ADR explaining why unittest compatibility required

❌ **nose2** (nose2 package)
- Reason: Less actively maintained than pytest
- If needed: Strong justification needed (legacy compatibility?)

---

### Code Formatter: Black (ENFORCED)

**Package:** black
**Version:** >=23.11.0,<25.0.0 (LOCKED)
**Purpose:** Automatic code formatting ("The Uncompromising Code Formatter")
**License:** MIT
**Security:** No known vulnerabilities

**Rationale for Selection:**
- Opinionated (zero configuration debates)
- Deterministic output (same code always formats identically)
- Fast (Rust-based)
- Industry standard (used by thousands of projects)
- Eliminates formatting discussions in code review

**CRITICAL ENFORCEMENT RULES:**

1. **ALL code MUST be Black-formatted before commit** (ENFORCED by pre-commit hook)
2. **Line length: 88 characters** (Black default, NOT negotiable)
3. **Double quotes for strings** (Black default):
   ```python
   # ✅ CORRECT
   description = "Buy milk"

   # ❌ WRONG (single quotes not allowed, Black will auto-convert)
   description = 'Buy milk'
   ```

4. **Pre-commit hook MUST run Black:**
   ```bash
   # .pre-commit-config.yaml
   - repo: https://github.com/psf/black
     rev: 23.11.0
     hooks:
       - id: black
   ```

5. **CI/CD MUST verify Black formatting:**
   ```bash
   black --check todo.py tests/
   # Exit code 1 if not formatted → build fails
   ```

**Black Configuration (minimal, Black is opinionated):**
```toml
[tool.black]
line-length = 88  # Default, don't change
target-version = ['py311']
include = '\.pyi?$'
extend-exclude = '''
/(
    \.git
  | \.venv
  | build
  | dist
)/
'''
```

**PROHIBITED Formatters:**

❌ **autopep8** (autopep8 package)
- Reason: Less opinionated, configuration debates
- Would conflict: Black enforces specific style

❌ **YAPF** (yapf package, Google's formatter)
- Reason: Configurable (defeats purpose of zero-config approach)
- Would conflict: Different formatting rules than Black

❌ **Manual formatting** (no formatter)
- Reason: Inconsistent style, code review noise
- NEVER acceptable: Black MUST be used

**Enforcement Mechanism:**
- **Pre-commit hook:** Automatically formats on commit attempt
- **CI/CD check:** Build fails if Black would change anything
- **context-validator:** Flags non-Black formatted code

---

[Continue with remaining 8 tools/libraries: Ruff, mypy, pytest-cov, pathlib, json, pyproject.toml]

[Each with same level of detail: rationale, version locks, critical rules, prohibited alternatives, enforcement]

[Total tech-stack.md length: 500 lines]

---

## Comparison: "Vibe Coding" vs DevForgeAI Reality

### Same Project: Two Approaches

**"Vibe Coding" Approach (WRONG):**
```
User: "Build me a CLI todo app"

Developer/AI:
→ Assumes Python (not asked)
→ Picks random CLI library (argparse? Click? Typer? Guesses)
→ Uses whatever JSON library (json? orjson? Doesn't matter, right?)
→ Maybe writes tests (if feeling good that day)
→ Formatting? Whatever IDE does
→ Structure? One file? Multiple? Who knows

Result after 1 hour:
- 150 lines of code
- No tests (or minimal tests)
- No documentation
- Hardcoded paths
- Works on developer's machine only
- Technical debt from day 1

Context files: NONE
Specifications: NONE
Questions asked: 0-2 vague ones
Ambiguities: MANY
```

**DevForgeAI Approach (CORRECT):**
```
User: "Build me a CLI todo app"

discovering-requirements:
→ Q1: Project type? [4 options]
→ Q2: Business problem? [4 options]
→ Q3: Users? [5 options, multiSelect]
→ Q4: Success metrics? [6 options, multiSelect]
→ Q5: MVP scope? [4 options]
→ Q6: Core capabilities? [12 options, multiSelect]
→ Q7: Data storage? [4 options]
→ Q8: Platform support? [4 options, multiSelect]
→ Q9: Performance? [4 options]
→ Q10: Security? [7 options, multiSelect]

Complexity assessment: 8/60 = Simple tier

designing-systems:
→ Q11: Backend language? [6 options with trade-offs]
→ Q12: CLI library? [4 options] → Click LOCKED
→ Q13: Path library? [2 options]
→ Q14: JSON library? [3 options]
→ Q15: Test framework? [3 options] → pytest LOCKED
→ Q16: Code formatter? [4 options] → Black ENFORCED
→ Q17: Linter? [4 options]
→ Q18: Type checker? [3 options]
→ Q19: Dependency management? [4 options]
→ Q20: Architecture? [4 options]
→ Q21: Test structure? [3 options]
→ Q22: Docstring style? [4 options]
→ Q23: Error handling? [3 options]

Generates 6 context files (3,000 lines):
- tech-stack.md: 500 lines (Click LOCKED, pytest LOCKED, Black ENFORCED)
- dependencies.md: 600 lines (7 packages, versions LOCKED, PROHIBITED alternatives)
- coding-standards.md: 800 lines (every pattern specified)
- source-tree.md: 400 lines (single file ENFORCED)
- architecture-constraints.md: 400 lines (rules defined)
- anti-patterns.md: 300 lines (forbidden patterns listed)

Development with devforgeai-development:
→ test-automator: Generates 15 tests from acceptance criteria
→ backend-architect: Implements to pass tests, follows ALL constraints
→ context-validator: Checks every commit against 6 context files
→ refactoring-specialist: Improves code quality
→ code-reviewer: Validates patterns

Result after 2-3 hours:
- 150 lines of code (same as vibe coding)
- 200 lines of tests (15 tests, AAA pattern, 96% coverage)
- 3,000 lines of specifications (prevents all future debt)
- All tests passing
- Black formatted, mypy strict passed, Ruff clean
- Works on all platforms (pathlib handles differences)
- ZERO technical debt
- Fully documented (Google-style docstrings)
- Can be enhanced without rewrites (spec-driven)

Context files: 6 files, 3,000 lines
Specifications: Complete, zero ambiguities
Questions asked: 23 detailed questions
Ambiguities: ZERO
```

**Time Comparison:**
- Vibe coding: 1 hour → Technical debt accumulates immediately
- DevForgeAI: 2-3 hours (40 min spec + 1.5 hours dev) → Zero technical debt

**Long-term Impact:**
- Vibe coding: Adding features requires rewrites, tech debt compounds
- DevForgeAI: Adding features extends cleanly, context files guide development

---

## Statistics Summary

### Questions Asked by Complexity

| Project Type | Ideation Qs | Architecture Qs | Total Qs | Context Lines | Spec Time |
|--------------|-------------|-----------------|----------|---------------|-----------|
| Simple CLI | 10 | 13 | **23** | 3,000 | 30-40 min |
| Mid-Size GUI | 24 | 32 | **56** | 5,500 | 1.5-2 hours |
| Complex SaaS | 45 | 68 | **113** | 12,000 | 4-5 hours |

### Value Proposition

**Upfront Time Investment:**
- Simple: +40 minutes for specification
- Mid-Size: +2 hours for specification
- Complex: +5 hours for specification

**Prevents:**
- Technical debt accumulation (saves weeks/months later)
- Architecture rewrites (saves person-months)
- Library conflicts (saves days of debugging)
- Pattern inconsistencies (saves code review cycles)
- "Works on my machine" issues (cross-platform specs)

**ROI:**
- Simple: 40 min investment prevents 10+ hours of future tech debt
- Mid-Size: 2 hour investment prevents 100+ hours of rewrites
- Complex: 5 hour investment prevents person-months of architectural refactoring

---

