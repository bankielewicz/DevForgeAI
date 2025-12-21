---
research_id: RESEARCH-EXAMPLE-001
epic_id: EPIC-007
story_id: null
workflow_state: Architecture
research_mode: repository-archaeology
timestamp: 2025-11-17T18:30:00Z
quality_gate_status: PASS
version: "2.0"
tags: ["authentication", "oauth2", "aws-cognito", "python", "fastapi"]
---

# Research Report: Authentication Framework Evaluation for SaaS Platform

## Executive Summary

Analyzed 5 high-quality Python authentication repositories (avg quality: 8.2/10) to evaluate OAuth 2.0 implementation patterns for multi-tenant SaaS. Top recommendation: AWS Cognito with FastAPI integration using Repository Pattern (feasibility: 8.5/10, aligns with tech-stack.md AWS preference, production-proven across 2.1K+ deployments). Critical insight: N+1 query anti-pattern identified in 3 repositories (mitigation: eager loading with SQLAlchemy selectinload).

---

## Research Scope

**Primary Questions:**
1. What are proven OAuth 2.0 implementation patterns for Python/FastAPI?
2. Which authentication provider (Auth0, AWS Cognito, Firebase) best fits AWS-native SaaS constraints?
3. What are common pitfalls in authentication implementations?

**Boundaries:**
- **In-scope:** OAuth 2.0, OIDC providers, Python backend, FastAPI framework
- **Out-of-scope:** SAML, custom cryptography, non-Python implementations
- **Technology constraints:** Python 3.9+, FastAPI (per tech-stack.md), AWS deployment preferred

**Assumptions:**
- Multi-tenant SaaS platform
- <1000 initial users, scaling to 10K within 6 months
- AWS infrastructure (per tech-stack.md preference)
- Budget: <$200/month for authentication

---

## Methodology Used

**Research Mode:** Repository Archaeology (GitHub code mining)
**Duration:** 9 minutes 15 seconds
**Tools:** GitHub API, gh CLI, git clone for deep analysis, Grep for pattern extraction

**GitHub Search Queries:**
1. `"fastapi oauth2" language:python stars:>100 pushed:>2023-01-01` (18 results)
2. `"repository pattern" "dependency injection" language:python stars:>200` (12 results)
3. `"aws cognito" "fastapi" language:python stars:>50 pushed:>2024-01-01` (7 results)

**Repositories Analyzed (5 Selected):**
1. **fastapi-users/fastapi-users** (4.5K stars, 10/10 quality)
2. **cosmic-python/code** (2.1K stars, 9/10 quality) - Domain-Driven Design focus
3. **tiangolo/full-stack-fastapi-postgresql** (19K stars, 9/10 quality)
4. **nsidnev/fastapi-realworld-example-app** (2.4K stars, 8/10 quality)
5. **aminalaee/sqladmin** (850 stars, 7/10 quality)

**Source Quality:**
- Official documentation: 6 sources (quality: 10/10) - FastAPI docs, AWS Cognito docs
- High-quality repositories: 5 repos (avg quality: 8.6/10)
- Implementation guides: 4 sources (quality: 7/10) - Real Python, TestDriven.io

**Methodology Steps:**
1. Formulated 3 GitHub search queries based on research questions
2. Quality-scored 37 candidate repositories (filtered to 5 with score ≥7)
3. Cloned repositories to `/tmp/research/auth-patterns/` for deep analysis
4. Extracted 12 code patterns using Grep (repository pattern, dependency injection, OAuth flows)
5. Identified 6 architectural insights (layered architecture, async SQLAlchemy, JWT handling)
6. Documented 5 common pitfalls from issues/PR discussions
7. Validated patterns against 6 DevForgeAI context files (tech-stack.md, architecture-constraints.md, etc.)
8. Synthesized top 3 recommendations ranked by quality score + framework compliance

---

## Findings

### Repository Quality Scores

| Repository | Stars | Last Commit | Quality Score | Key Strengths |
|------------|-------|-------------|---------------|---------------|
| **fastapi-users** | 4.5K | 3 days ago | **10/10** | Comprehensive auth library, excellent docs, active maintenance, 100% test coverage |
| **full-stack-fastapi** | 19K | 1 week ago | **9/10** | Complete full-stack example, production-ready, Alembic migrations |
| **cosmic-python** | 2.1K | 2 weeks ago | **9/10** | DDD focus, repository pattern exemplar, clean architecture |
| **fastapi-realworld** | 2.4K | 1 month ago | **8/10** | RealWorld spec implementation, JWT auth, good testing |
| **sqladmin** | 850 | 5 days ago | **7/10** | Admin panel with auth, FastAPI integration, active development |

**Quality Scoring Rubric Applied:**
- Community Health (0-3): Stars, contributors, active issues
- Maintenance (0-2): Recent commits, response to issues
- Documentation (0-2): README, docs/, examples/
- Test Coverage (0-2): Tests directory, CI badges
- Production Indicators (0-1): Docker/K8s configs, CI/CD

---

### Code Patterns Extracted

#### Pattern 1: Repository Pattern with Dependency Injection ⭐ (Quality: 9.5/10)

**Source:** cosmic-python/code (9/10 quality, 2.1K stars)
**Files:** `src/repositories/user_repository.py`, `src/infrastructure/sqlalchemy_user_repository.py`

**Pattern Description:**
Abstract repository interface defines data access contract. Concrete SQLAlchemy implementation injected via constructor. Enables testability (mock repositories) and flexibility (swap data sources).

**Code Example:**
```python
# src/repositories/user_repository.py (Abstract Interface)
from abc import ABC, abstractmethod
from typing import Optional
from src.domain.user import User

class UserRepository(ABC):
    """Abstract repository for user persistence."""

    @abstractmethod
    async def get_by_id(self, user_id: int) -> Optional[User]:
        """Retrieve user by ID."""
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        """Retrieve user by email (unique constraint)."""
        pass

    @abstractmethod
    async def save(self, user: User) -> User:
        """Persist user entity."""
        pass

    @abstractmethod
    async def delete(self, user_id: int) -> bool:
        """Delete user by ID."""
        pass


# src/infrastructure/sqlalchemy_user_repository.py (Concrete Implementation)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.user_repository import UserRepository
from src.domain.user import User
from src.infrastructure.models.user_model import UserModel

class SQLAlchemyUserRepository(UserRepository):
    """SQLAlchemy implementation of UserRepository."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: int) -> Optional[User]:
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        model = result.scalar_one_or_none()
        return User.from_orm(model) if model else None

    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        model = result.scalar_one_or_none()
        return User.from_orm(model) if model else None

    async def save(self, user: User) -> User:
        model = UserModel(**user.dict(exclude={'id'}))
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return User.from_orm(model)

    async def delete(self, user_id: int) -> bool:
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        model = result.scalar_one_or_none()
        if model:
            await self.session.delete(model)
            await self.session.commit()
            return True
        return False


# Dependency injection (in main.py or routes)
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

async def get_db() -> AsyncSession:
    """Dependency provider for database session."""
    async with async_session_maker() as session:
        yield session

async def get_user_repository(
    session: AsyncSession = Depends(get_db)
) -> UserRepository:
    """Dependency provider for UserRepository."""
    return SQLAlchemyUserRepository(session)

# Usage in route
@router.get("/users/{user_id}")
async def get_user(
    user_id: int,
    user_repo: UserRepository = Depends(get_user_repository)
):
    user = await user_repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

**Benefits:**
- ✅ Testability: Mock UserRepository in unit tests (no database required)
- ✅ Flexibility: Swap SQLAlchemy for PostgreSQL async driver without changing business logic
- ✅ Framework compliance: Aligns with architecture-constraints.md (domain layer doesn't depend on infrastructure)
- ✅ Production-proven: 2.1K stars, used in DDD Book example code

**Drawbacks:**
- ❌ Boilerplate: Abstract class + concrete class for each entity
- ❌ Complexity: May be overkill for simple CRUD apps (<5 entities)

**Applicability:**
- ✅ Multi-entity domains (>5 entities)
- ✅ Long-term projects (>6 months)
- ✅ Team size ≥3 developers
- ✅ Clean architecture / DDD projects
- ❌ Simple CRUD apps (<3 entities)
- ❌ Prototypes or MVPs (use direct ORM)

**When to Use:**
- Complex business logic requiring isolation and testability
- Multiple data sources (SQL + NoSQL)
- Long-term maintainability prioritized over rapid development

---

#### Pattern 2: OAuth 2.0 with AWS Cognito Integration (Quality: 8.5/10)

**Source:** full-stack-fastapi-postgresql (19K stars, 9/10 quality)
**Files:** `backend/app/auth/cognito.py`, `backend/app/auth/dependencies.py`

**Pattern Description:**
Integrate AWS Cognito User Pools with FastAPI using dependency injection. Verify JWT tokens from Cognito, extract user claims, inject authenticated user into routes.

**Code Example:**
```python
# app/auth/cognito.py
import boto3
from jose import jwt, JWTError
from fastapi import HTTPException, status
from typing import Dict, Optional

class CognitoAuthenticator:
    """AWS Cognito JWT token validation."""

    def __init__(self, region: str, user_pool_id: str, app_client_id: str):
        self.region = region
        self.user_pool_id = user_pool_id
        self.app_client_id = app_client_id
        self.jwks_url = f"https://cognito-idp.{region}.amazonaws.com/{user_pool_id}/.well-known/jwks.json"

    async def verify_token(self, token: str) -> Dict:
        """Verify JWT token from Cognito."""
        try:
            # Decode token (will verify signature against JWKS)
            payload = jwt.decode(
                token,
                self.jwks_url,
                algorithms=["RS256"],
                audience=self.app_client_id,
                options={"verify_aud": True}
            )
            return payload
        except JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

# app/auth/dependencies.py
from fastapi import Depends, Header, HTTPException
from app.auth.cognito import CognitoAuthenticator
from app.models.user import User

# Global authenticator (initialized in main.py)
authenticator = CognitoAuthenticator(
    region=os.getenv("AWS_REGION"),
    user_pool_id=os.getenv("COGNITO_USER_POOL_ID"),
    app_client_id=os.getenv("COGNITO_APP_CLIENT_ID")
)

async def get_current_user(
    authorization: str = Header(...)
) -> User:
    """Extract authenticated user from JWT token."""
    # Extract token from "Bearer {token}"
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")

    token = authorization.replace("Bearer ", "")

    # Verify token with Cognito
    claims = await authenticator.verify_token(token)

    # Extract user info from claims
    user = User(
        id=claims["sub"],
        email=claims["email"],
        username=claims.get("cognito:username")
    )
    return user

# Usage in route
@router.get("/me")
async def get_current_user_profile(
    current_user: User = Depends(get_current_user)
):
    """Get authenticated user's profile."""
    return {
        "id": current_user.id,
        "email": current_user.email,
        "username": current_user.username
    }
```

**Benefits:**
- ✅ AWS-native: Integrates with existing AWS infrastructure
- ✅ Secure: Cognito handles user management, password policies, MFA
- ✅ Scalable: Cognito scales to millions of users automatically
- ✅ Cost-effective: $0.0055/MAU (vs Auth0 $0.05/MAU = 9x cheaper)

**Drawbacks:**
- ❌ Complex setup: Cognito User Pools require IAM, CloudFormation/Terraform
- ❌ AWS lock-in: Migration to alternative provider challenging
- ❌ Limited UI customization: Hosted UI has constraints

**Applicability:**
- ✅ AWS-first teams (already on AWS, familiar with IAM)
- ✅ Cost-sensitive (Auth0 too expensive at scale)
- ✅ Standard OAuth flows (no exotic authentication requirements)
- ❌ Highly customized auth flows (Auth0 more flexible)

---

#### Pattern 3: FastAPI Async SQLAlchemy Session Management (Quality: 8.0/10)

**Source:** tiangolo/full-stack-fastapi-postgresql (19K stars, 9/10 quality)
**Files:** `backend/app/db/session.py`, `backend/app/api/dependencies.py`

**Pattern Description:**
Async SQLAlchemy session management with FastAPI dependency injection. Ensures proper session lifecycle (create → use → close) and transaction handling.

**Code Example:**
```python
# app/db/session.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Async engine (created once at startup)
async_engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True,
    pool_size=10,
    max_overflow=20
)

# Async session factory
async_session_maker = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# app/api/dependencies.py
from app.db.session import async_session_maker

async def get_db() -> AsyncSession:
    """FastAPI dependency providing database session."""
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()  # Auto-commit on success
        except Exception:
            await session.rollback()  # Auto-rollback on error
            raise
        finally:
            await session.close()  # Always close session

# Usage in repository
class SQLAlchemyUserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: int):
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        return result.scalar_one_or_none()

# Usage in route
@router.post("/users/")
async def create_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
    user_repo: UserRepository = Depends(get_user_repository)
):
    """Create new user (transaction managed by get_db dependency)."""
    user = await user_repo.save(User(**user_data.dict()))
    # Automatic commit on success, rollback on exception
    return user
```

**Benefits:**
- ✅ Automatic transaction management (commit on success, rollback on error)
- ✅ Proper session lifecycle (always closed via context manager)
- ✅ Connection pooling (10 base, 20 overflow = handles burst traffic)
- ✅ Framework compliance: Async pattern aligns with FastAPI best practices

**Drawbacks:**
- ❌ Complexity: Async SQLAlchemy has learning curve vs sync ORM
- ❌ Debugging: Async stack traces harder to read

**Applicability:**
- ✅ FastAPI projects (async framework requires async DB)
- ✅ High concurrency (async handles 1000+ concurrent requests)
- ✅ Modern Python (3.9+, async/await support)

---

### Common Pitfalls Identified

#### Pitfall 1: N+1 Query Problem with Lazy Loading

**Source:** fastapi-realworld-example-app Issue #42

**Problem:**
```python
# BAD: Lazy loading triggers N+1 queries
users = await session.execute(select(User))
for user in users.scalars():
    # Each iteration triggers separate query for posts
    posts = user.posts  # Lazy load! N queries
    print(f"{user.name} has {len(posts)} posts")
```

**Impact:** 1 query for users + N queries for posts = N+1 total (slow at scale)

**Solution:**
```python
# GOOD: Eager loading with single JOIN query
users = await session.execute(
    select(User).options(selectinload(User.posts))
)
for user in users.scalars():
    posts = user.posts  # Already loaded, no extra query
    print(f"{user.name} has {len(posts)} posts")
```

**Impact:** 2 queries total (1 for users, 1 JOIN for all posts)
**Fix:** [PR #47](https://github.com/nsidnev/fastapi-realworld-example-app/pull/47) - Added selectinload
**Evidence:** Documented in 3 repositories (cosmic-python, fastapi-realworld, fastapi-users)

---

#### Pitfall 2: Missing JWT Token Expiration Validation

**Source:** full-stack-fastapi-postgresql Issue #1234

**Problem:**
```python
# BAD: No expiration check
payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
user_id = payload["sub"]  # May be expired token!
```

**Impact:** Accepts expired tokens (security vulnerability)

**Solution:**
```python
# GOOD: Verify expiration
from jose import jwt, JWTError, ExpiredSignatureError

try:
    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=["HS256"],
        options={"verify_exp": True}  # Check expiration
    )
    user_id = payload["sub"]
except ExpiredSignatureError:
    raise HTTPException(status_code=401, detail="Token expired")
except JWTError:
    raise HTTPException(status_code=401, detail="Invalid token")
```

**Fix:** [Commit d4f5a8c](https://github.com/tiangolo/full-stack-fastapi-postgresql/commit/d4f5a8c)
**Evidence:** 2 repositories had this issue, both fixed in 2023

---

#### Pitfall 3: Hardcoded Secrets in Code

**Source:** Multiple repositories (security audit findings)

**Problem:**
```python
# BAD: Hardcoded secret key
SECRET_KEY = "super-secret-key-do-not-share"  # ❌ Security vulnerability!
JWT_ALGORITHM = "HS256"
```

**Impact:** Secret exposed in version control (GitHub leak)

**Solution:**
```python
# GOOD: Environment variables
import os

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable required")

JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
```

**Evidence:** Flagged in anti-patterns.md (DevForgeAI context file)
**Severity:** CRITICAL (automated security scans detect this)

---

### Architectural Insights

#### Insight 1: Layered Architecture (Hexagonal/Clean Architecture)

**Observation:** 4 out of 5 high-quality repositories use layered architecture (domain/application/infrastructure separation).

**Directory Structure:**
```
src/
├── domain/         # Business logic, entities, value objects (no external dependencies)
│   ├── user.py
│   └── repositories/  # Abstract repository interfaces
├── application/    # Use cases, orchestration
│   └── services/
│       └── authentication_service.py
├── infrastructure/ # External integrations (DB, AWS, external APIs)
│   ├── database/
│   │   └── sqlalchemy_user_repository.py
│   └── aws/
│       └── cognito_client.py
└── presentation/   # FastAPI routes, DTOs
    └── routes/
        └── auth.py
```

**Rationale:** Isolates business logic from frameworks, improves testability, enables technology swaps.

**DevForgeAI Alignment:** ✅ Matches architecture-constraints.md pattern (domain → application → infrastructure dependency flow)

---

#### Insight 2: Async Everywhere Pattern

**Observation:** All FastAPI + SQLAlchemy repositories use async/await throughout (no blocking sync calls).

**Pattern:**
- Async database sessions (`AsyncSession`)
- Async repository methods (`async def get_by_id`)
- Async route handlers (`async def create_user`)
- Async Cognito/external API calls (`async with httpx.AsyncClient`)

**Rationale:** FastAPI async runtime requires non-blocking I/O. Mixing sync DB calls in async routes blocks event loop (performance degradation).

**Best Practice:**
```python
# ✅ CORRECT: Async throughout
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()

# ❌ WRONG: Sync DB call in async route
async def get_user(user_id: int):
    # Blocks event loop!
    user = sync_session.query(User).filter(User.id == user_id).first()
    return user
```

---

## Framework Compliance Check

**Validation Date:** 2025-11-17 18:45:33
**Context Files Checked:** 6/6 ✅

| Context File | Status | Violations | Details |
|--------------|--------|------------|---------|
| **tech-stack.md** | ✅ PASS | 0 | Recommended tech (AWS Cognito, FastAPI, SQLAlchemy) aligns with Python + AWS preferences |
| **source-tree.md** | ✅ PASS | 0 | Layered architecture matches recommended structure (domain/application/infrastructure) |
| **dependencies.md** | ⚠️ WARN | 1 MEDIUM | Suggests `python-jose` package (not in approved list, but commonly used for JWT) |
| **coding-standards.md** | ✅ PASS | 0 | Async/await pattern, PEP 8 naming, type hints all aligned |
| **architecture-constraints.md** | ✅ PASS | 0 | Repository pattern respects layer boundaries (domain defines interface, infrastructure implements) |
| **anti-patterns.md** | ✅ PASS | 0 | No God Objects, no SQL concatenation, no hardcoded secrets in examples |

**Violations Detail:**

**MEDIUM (dependencies.md):**
- **Issue:** Research recommends `python-jose[cryptography]` for JWT handling
- **Context:** dependencies.md does not explicitly list `python-jose` in approved packages
- **Resolution:** Add `python-jose` to dependencies.md with rationale ("Industry-standard JWT library for FastAPI, maintained by Sebastián Ramírez - FastAPI author")
- **User Action Required:** No (proceed with warning, add during architecture phase)

**Quality Gate Status:** ⚠️ WARN (1 MEDIUM violation - non-blocking)
**Recommendation:** Proceed with research findings. Add `python-jose` to dependencies.md during Phase 2 file creation with rationale from research.

---

## Workflow State

**Current State:** Architecture
**Research Focus:** Technology evaluation and implementation pattern selection
**Staleness Check:** ✅ CURRENT (research completed 2025-11-17, workflow state unchanged)

**Research Alignment:**
- ✅ Architecture phase requires technology decisions (research provides evidence)
- ✅ Repository archaeology findings support tech-stack.md creation (code patterns + quality scores)
- ✅ Implementation patterns guide coding-standards.md (async patterns, dependency injection)

**Staleness Criteria:**
- Report age: 0 days (just generated) < 30 day threshold ✅
- Workflow state distance: 0 states (Architecture → Architecture) < 2 state threshold ✅
- **Status:** CURRENT (no re-research needed)

---

## Recommendations

### 1. AWS Cognito with FastAPI (Recommended) ⭐ (Feasibility: 8.5/10)

**Approach:** AWS Cognito User Pools + FastAPI + Repository Pattern + Async SQLAlchemy
**Evidence:** 3 high-quality repositories (avg: 9/10), official AWS + FastAPI docs

**Benefits:**
- ✅ AWS-native (aligns with tech-stack.md AWS preference)
- ✅ Cost-effective ($5.50/mo for 1K MAU vs Auth0 $535/mo)
- ✅ Production-proven (19K stars on full-stack-fastapi example)
- ✅ Framework compliant (layered architecture, repository pattern)
- ✅ Scalable (handles millions of users)

**Drawbacks:**
- ❌ Complex initial setup (Cognito User Pools, IAM roles, JWKS validation)
- ❌ AWS vendor lock-in (migration to Auth0/Firebase challenging)
- ❌ Steeper learning curve (AWS-specific knowledge required)

**Applicability:**
- ✅ AWS-first teams (already on AWS, familiar with IAM)
- ✅ Budget-conscious (Auth0 too expensive)
- ✅ Long-term projects (complexity pays off over time)
- ✅ Scalability required (anticipate >10K users)
- ❌ Simple prototypes (Cognito overkill for MVP)
- ❌ Non-AWS teams (steep AWS learning curve)

**Implementation:**
- **Effort:** 1-2 weeks (Cognito setup, FastAPI integration, testing)
- **Complexity:** Medium-High (AWS infrastructure, JWT validation, async patterns)
- **Prerequisites:** AWS account, Terraform/CloudFormation (IaC recommended), python-jose library

**Repository Examples:**
- [full-stack-fastapi-postgresql](https://github.com/tiangolo/full-stack-fastapi-postgresql) (19K stars, 9/10 quality)
- [aws-cognito-fastapi-example](https://github.com/example/aws-cognito-fastapi) (Quality: 7/10, 850 stars)

---

### 2. Auth0 with FastAPI (Alternative - Requires ADR) (Feasibility: 7.8/10)

**Approach:** Auth0 Universal Login + FastAPI + JWT Verification
**Evidence:** Auth0 official docs (10/10), 2 implementation repos (avg: 6/10)

**Benefits:**
- ✅ Excellent developer experience (simplest integration, <1 day setup)
- ✅ Comprehensive features (social logins, MFA, custom flows, extensibility)
- ✅ Managed service (zero ops overhead, Auth0 handles scaling/security)
- ✅ Great documentation (official guides, SDKs, community support)

**Drawbacks:**
- ❌ Expensive at scale ($535/mo for 10K MAU vs Cognito $55/mo)
- ❌ Vendor lock-in (Okta acquisition, proprietary platform)
- ❌ Requires tech-stack.md update (not currently approved)
- ❌ Hidden costs (add-ons, enterprise features, custom domains)

**Applicability:**
- ✅ Developer experience prioritized (fast time-to-market)
- ✅ Budget allows ($500+/mo acceptable)
- ✅ Complex auth flows (rules, hooks, custom UI)
- ❌ Budget-constrained (<$100/mo)
- ❌ AWS-native preference (Cognito better fit)

**Implementation:**
- **Effort:** 2-4 days (Auth0 setup, FastAPI integration, testing)
- **Complexity:** Low-Medium (well-documented, straightforward)
- **Prerequisites:** Auth0 account ($0 free tier for development), auth0-python SDK

**ADR Required:** Yes (tech-stack.md currently specifies AWS preference, Auth0 is non-AWS SaaS)

---

### 3. Supertokens (Open-Source, Self-Hosted) (Feasibility: 6.5/10)

**Approach:** Supertokens Core (self-hosted) + FastAPI integration
**Evidence:** Supertokens official docs (10/10), 1 repo (quality: 7/10)

**Benefits:**
- ✅ Free (self-hosted, no per-user cost)
- ✅ Open-source (full control, can fork/modify)
- ✅ FastAPI SDK available (official integration)
- ✅ No vendor lock-in (can migrate or extend freely)

**Drawbacks:**
- ❌ Maintenance overhead (~1 dev week/month for updates, security patches)
- ❌ Smaller community (10K stars vs Auth0/Cognito ecosystems)
- ❌ Infrastructure costs (servers, database, CDN for hosted UI)
- ❌ Less mature (newer project, fewer battle-tested deployments)

**Applicability:**
- ✅ Budget absolutely constrained ($0 SaaS spend)
- ✅ Team has DevOps capacity (can maintain self-hosted service)
- ✅ Custom auth requirements (need to modify source code)
- ❌ Limited team (no capacity for maintenance)
- ❌ Enterprise needs (managed service preferred)

**Implementation:**
- **Effort:** 1-2 weeks (Docker deployment, FastAPI integration, PostgreSQL setup, testing)
- **Complexity:** Medium (self-hosting complexity, less documentation than Auth0/Cognito)
- **Prerequisites:** Docker/Kubernetes, PostgreSQL database, CDN (optional for hosted UI)

---

## Risk Assessment

| Risk | Severity | Probability | Impact | Mitigation |
|------|----------|-------------|--------|------------|
| **AWS Cognito vendor lock-in** | MEDIUM | HIGH | Migration to Auth0/Firebase costly (JWT format changes, user export/import) | Abstract auth behind interface (UserRepository), use OIDC standards, document migration path in ADR |
| **Complex Cognito setup** | MEDIUM | MEDIUM | 1-2 week delay in integration, potential misconfiguration | Allocate dedicated sprint, use Terraform IaC (infrastructure as code), follow official AWS tutorials, peer review IAM policies |
| **N+1 query performance** | HIGH | MEDIUM | API latency >500ms at 1K users (triggers SLA breach) | Use selectinload for eager loading, add query logging, monitor with APM (DataDog/NewRelic), add integration tests |
| **JWT token security** | CRITICAL | LOW | Token compromise allows unauthorized access | Verify token expiration, validate signature against JWKS, use short expiration (15 min access, 7 day refresh), rotate secrets quarterly |
| **Auth0 cost escalation** | HIGH | LOW | If choose Auth0: Cost grows to $5K+/mo at 100K users (budget breach) | Choose Cognito instead (linear $550/mo at 100K MAU), or negotiate Auth0 volume discount if selecting Auth0 |

---

## ADR Readiness

**ADR Required:** Yes (Backend framework + Authentication provider selection)
**ADR Title:** ADR-XXX: Adopt AWS Cognito + FastAPI + Repository Pattern for Authentication
**Evidence Collected:** ✅ Complete

**Evidence Summary:**
- **Comparison matrix:** ✅ 5 repositories analyzed (avg quality: 8.6/10)
- **Code patterns:** ✅ 3 patterns extracted (Repository, OAuth 2.0 + Cognito, Async SQLAlchemy)
- **Cost analysis:** ✅ AWS Cognito $5.50/mo vs Auth0 $535/mo at 1K MAU (90% cheaper)
- **Performance benchmarks:** ✅ Query optimization data (Dapper 15ms, EF 147ms from prior research)
- **Risk assessment:** ✅ 5 risks identified with severity + mitigation
- **Framework compliance:** ✅ Validated against 6 context files (1 MEDIUM violation - add python-jose to dependencies.md)
- **Repository examples:** ✅ GitHub URLs, quality scores, code snippets with file paths

**Next Steps:**
1. Create ADR: `devforgeai/adrs/ADR-XXX-adopt-cognito-fastapi-auth.md`
2. Document decision context (SaaS authentication requirement, multi-tenancy, AWS-native preference)
3. Record decision (AWS Cognito + FastAPI selected)
4. Document alternatives (Auth0 rejected due to cost, Supertokens rejected due to maintenance overhead)
5. Note consequences (vendor lock-in accepted, complex setup mitigated with IaC)
6. Update tech-stack.md:
   ```markdown
   ## Authentication
   - **Provider:** AWS Cognito User Pools
   - **Framework:** FastAPI with python-jose (JWT validation)
   - **Pattern:** Repository Pattern with dependency injection
   - **Research:** [RESEARCH-EXAMPLE-001](devforgeai/research/examples/technology-evaluation-example.md)
   ```
7. Update dependencies.md:
   ```markdown
   - python-jose[cryptography]: ^3.3.0 (JWT token validation for AWS Cognito)
   - boto3: ^1.34.0 (AWS SDK for Cognito API calls if needed)
   ```

---

**Report Generated:** 2025-11-17 18:52:30
**Report Location:** devforgeai/research/examples/technology-evaluation-example.md
**Research ID:** RESEARCH-EXAMPLE-001
**Version:** 2.0 (template version)
