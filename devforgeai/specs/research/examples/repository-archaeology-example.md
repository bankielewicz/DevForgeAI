---
research_id: RESEARCH-EXAMPLE-003
epic_id: null
story_id: STORY-042
workflow_state: Ready for Dev
research_mode: repository-archaeology
timestamp: 2025-11-17T19:30:00Z
quality_gate_status: PASS
version: "2.0"
tags: ["repository-archaeology", "fastapi", "oauth2", "implementation-patterns", "github"]
---

# Research Report: OAuth 2.0 Implementation Patterns for FastAPI

## Executive Summary

Mined 8 GitHub repositories (avg quality: 7.9/10) to extract production-ready OAuth 2.0 implementation patterns for Python/FastAPI. Top pattern: Password + Refresh Token flow with Repository abstraction (quality: 9/10, production-proven in 3.2K+ deployments). Critical finding: 60% of repositories have JWT secret management anti-pattern (hardcoded secrets or weak keys) - mitigated via environment variables + key rotation. Architectural insight: Hexagonal architecture with auth ports/adapters provides best testability vs complexity trade-off.

---

## Research Scope

**Primary Questions:**
1. How do production FastAPI apps implement OAuth 2.0 password grant + refresh token flows?
2. What are proven repository patterns for user/token persistence?
3. What common pitfalls exist in JWT handling and session management?
4. What architectural patterns work well at scale (>10K users)?

**Boundaries:**
- **In-scope:** OAuth 2.0, JWT, FastAPI, Python 3.9+, SQLAlchemy async
- **Out-of-scope:** SAML, custom crypto, synchronous frameworks (Flask, Django), non-Python implementations
- **Technology constraints:** Python + FastAPI (per tech-stack.md), async patterns (per coding-standards.md)

**Assumptions:**
- Multi-tenant SaaS application
- PostgreSQL or MySQL database (relational DB)
- Deployment: AWS or cloud-agnostic (Docker/K8s)
- User scale: 1K-50K MAU initially

---

## Methodology Used

**Research Mode:** Repository Archaeology (deep GitHub code mining)
**Duration:** 11 minutes 38 seconds
**Tools:** GitHub API, gh CLI, git clone for analysis, Grep for pattern extraction

**GitHub Search Queries:**
1. `"fastapi oauth2" "refresh token" language:python stars:>100 pushed:>2023-01-01 archived:false` (14 results)
2. `"repository pattern" "fastapi" "sqlalchemy" language:python stars:>200 pushed:>2024-01-01` (9 results)
3. `"jwt" "fastapi" "security" language:python stars:>500` (21 results)

**Repository Selection Criteria:**
- Quality score ≥7/10 (using rubric: community 0-3, maintenance 0-2, docs 0-2, tests 0-2, production 0-1)
- Active maintenance (commits within last 90 days)
- Test coverage indicators (tests/ directory + CI badges)
- Production indicators (Docker, K8s configs, or >1K stars)

**Repositories Analyzed (8 Selected):**

| Repository | Stars | Quality | Last Commit | Key Strengths |
|------------|-------|---------|-------------|---------------|
| **fastapi-users** | 4.5K | 10/10 | 3 days | Comprehensive auth library, 100% coverage, excellent docs |
| **full-stack-fastapi** | 19K | 9/10 | 1 week | Complete full-stack, production-ready, JWT refresh flow |
| **fastapi-realworld** | 2.4K | 8/10 | 1 month | RealWorld spec, clean code, good JWT example |
| **fastapi-sqlalchemy** | 1.8K | 8/10 | 2 weeks | SQLAlchemy patterns, async best practices |
| **awesome-fastapi** | 6.2K | 7/10 | 1 month | Curated list, pattern references, OAuth examples |
| **fastapi-boilerplate** | 950 | 7/10 | 3 weeks | Production boilerplate, JWT + refresh tokens |
| **fastapi-auth-jwt** | 680 | 7/10 | 2 months | Focused on JWT auth, refresh flow, revocation |
| **fastapi-microservices** | 1.2K | 8/10 | 1 week | Microservices architecture, distributed auth |

**Source Quality:**
- High-quality repositories: 8 repos (avg quality: 8.0/10)
- Official documentation: FastAPI Security docs (10/10), OAuth 2.0 RFC 6749 (10/10)
- Implementation guides: Real Python (8/10), TestDriven.io (7/10)

**Methodology Steps:**
1. Formulated 3 GitHub search queries targeting OAuth 2.0 + refresh token implementations
2. Quality-scored 44 candidate repositories (filtered to 8 with score ≥7)
3. Cloned 8 repositories to `/tmp/research/oauth-patterns/` for deep analysis
4. Extracted 15 code patterns using Grep:
   - JWT creation/validation: 8 patterns
   - Refresh token flow: 6 patterns
   - Repository abstraction: 5 patterns
5. Identified 8 architectural insights (hexagonal architecture, dependency injection, async patterns)
6. Documented 7 common pitfalls from GitHub issues/PRs (JWT expiration bugs, secret management, token revocation)
7. Validated extracted patterns against 6 context files (architecture-constraints.md, anti-patterns.md)
8. Ranked patterns by quality score + framework compliance + production usage

---

## Findings

### Repository Quality Scores

*(Detailed table showing all 8 repositories - see above)*

**Quality Distribution:**
- Exemplary (9-10): 2 repositories
- High quality (7-8): 6 repositories
- Total avg: 8.0/10 (strong sample set)

---

### Extracted Code Patterns

#### Pattern 1: Password Grant + Refresh Token Flow ⭐ (Quality: 9/10)

**Source:** full-stack-fastapi-postgresql (19K stars, 9/10 quality)
**Files:** `backend/app/auth/oauth2.py`, `backend/app/models/token.py`

**Pattern Description:**
OAuth 2.0 password grant flow with refresh token rotation. User authenticates with email/password, receives access token (15 min TTL) + refresh token (7 day TTL). Refresh token used to obtain new access token without re-authentication.

**Code Example:**
```python
# app/auth/oauth2.py
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict, expires_delta: timedelta = None):
    """Create JWT access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict):
    """Create JWT refresh token (7 day expiration)."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=7)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, REFRESH_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# app/routes/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.repositories.user_repository import UserRepository

router = APIRouter()

@router.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_repo: UserRepository = Depends(get_user_repository)
):
    """OAuth 2.0 password grant - exchange credentials for tokens."""
    # Validate credentials
    user = await user_repo.get_by_email(form_data.username)  # OAuth spec uses 'username' field
    if not user or not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create tokens
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    # Store refresh token in database (for revocation capability)
    await user_repo.save_refresh_token(user.id, refresh_token)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": 900  # 15 minutes (900 seconds)
    }

@router.post("/refresh")
async def refresh_access_token(
    refresh_token: str,
    user_repo: UserRepository = Depends(get_user_repository)
):
    """Refresh flow - exchange refresh token for new access token."""
    try:
        # Decode and validate refresh token
        payload = jwt.decode(refresh_token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])

        # Verify token type
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")

        user_id = int(payload.get("sub"))

        # Verify refresh token exists in database (not revoked)
        is_valid = await user_repo.is_refresh_token_valid(user_id, refresh_token)
        if not is_valid:
            raise HTTPException(status_code=401, detail="Refresh token revoked")

        # Create new access token
        new_access_token = create_access_token(data={"sub": str(user_id)})

        return {
            "access_token": new_access_token,
            "token_type": "bearer",
            "expires_in": 900
        }

    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
```

**Benefits:**
- ✅ Security: Short-lived access tokens (15 min) limit breach window
- ✅ UX: Refresh tokens allow seamless re-authentication (no re-login for 7 days)
- ✅ Revocation: Storing refresh tokens in DB enables logout/revocation
- ✅ Production-proven: 19K stars, used in dozens of SaaS products

**Drawbacks:**
- ❌ Complexity: Two token types, two endpoints, refresh logic
- ❌ Storage: Refresh tokens in database (growth over time, cleanup needed)

**Applicability:**
- ✅ Multi-device apps (refresh tokens work across devices)
- ✅ Security-conscious (short access token TTL)
- ✅ SaaS with logout requirement (token revocation needed)
- ❌ Simple apps with long sessions (single token sufficient)

**Framework Compliance:**
- ✅ Repository pattern (aligns with architecture-constraints.md)
- ✅ No hardcoded secrets (uses environment variables per anti-patterns.md)
- ✅ Async patterns (per coding-standards.md FastAPI conventions)

---

#### Pattern 2: Hexagonal Architecture for Auth Service ⭐ (Quality: 9/10)

**Source:** cosmic-python/code (2.1K stars, 9/10 quality - DDD Book example)
**Files:** `src/domain/`, `src/infrastructure/`, `src/service_layer/`

**Pattern Description:**
Hexagonal (Ports & Adapters) architecture isolates business logic from infrastructure. Domain layer defines interfaces (ports), infrastructure layer provides implementations (adapters), service layer orchestrates use cases.

**Directory Structure:**
```
src/
├── domain/                      # Business logic (pure Python, zero external deps)
│   ├── user.py                 # User entity (value objects)
│   ├── token.py                # Token entity (access + refresh)
│   └── repositories/           # Repository interfaces (ports)
│       ├── user_repository.py  # Abstract UserRepository
│       └── token_repository.py # Abstract TokenRepository
│
├── service_layer/              # Use cases (orchestration)
│   ├── authentication_service.py  # Login, refresh, logout use cases
│   └── unit_of_work.py         # Transaction boundary abstraction
│
├── infrastructure/             # External adapters (infrastructure details)
│   ├── database/
│   │   ├── sqlalchemy_user_repository.py    # UserRepository implementation
│   │   └── sqlalchemy_token_repository.py   # TokenRepository implementation
│   ├── security/
│   │   ├── jwt_handler.py      # JWT encode/decode
│   │   └── password_hasher.py  # bcrypt password hashing
│   └── aws/
│       └── cognito_client.py   # AWS Cognito integration (optional)
│
└── presentation/               # FastAPI routes (UI/API layer)
    └── routes/
        └── auth.py             # HTTP endpoints
```

**Code Example:**
```python
# src/domain/repositories/user_repository.py (Port - Interface)
from abc import ABC, abstractmethod
from typing import Optional
from src.domain.user import User

class UserRepository(ABC):
    """Abstract user repository interface."""

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    async def save(self, user: User) -> User:
        pass


# src/infrastructure/database/sqlalchemy_user_repository.py (Adapter - Implementation)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.repositories.user_repository import UserRepository
from src.domain.user import User
from src.infrastructure.database.models import UserModel

class SQLAlchemyUserRepository(UserRepository):
    """SQLAlchemy adapter for UserRepository."""

    def __init__(self, session: AsyncSession):
        self.session = session

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


# src/service_layer/authentication_service.py (Use Case - Business Logic)
from src.domain.repositories.user_repository import UserRepository
from src.infrastructure.security.jwt_handler import JWTHandler
from src.infrastructure.security.password_hasher import PasswordHasher

class AuthenticationService:
    """Authentication use case orchestration."""

    def __init__(
        self,
        user_repo: UserRepository,
        jwt_handler: JWTHandler,
        password_hasher: PasswordHasher
    ):
        self.user_repo = user_repo
        self.jwt_handler = jwt_handler
        self.password_hasher = password_hasher

    async def login(self, email: str, password: str):
        """Authenticate user and issue tokens."""
        # Load user from repository
        user = await self.user_repo.get_by_email(email)
        if not user:
            raise AuthenticationError("Invalid credentials")

        # Verify password
        if not self.password_hasher.verify(password, user.hashed_password):
            raise AuthenticationError("Invalid credentials")

        # Issue tokens
        access_token = self.jwt_handler.create_access_token(user.id)
        refresh_token = self.jwt_handler.create_refresh_token(user.id)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user_id": user.id
        }


# src/presentation/routes/auth.py (Presentation - HTTP Layer)
from fastapi import APIRouter, Depends, HTTPException
from src.service_layer.authentication_service import AuthenticationService

router = APIRouter()

@router.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthenticationService = Depends(get_auth_service)
):
    """OAuth 2.0 password grant endpoint."""
    try:
        result = await auth_service.login(form_data.username, form_data.password)
        return {
            "access_token": result["access_token"],
            "refresh_token": result["refresh_token"],
            "token_type": "bearer"
        }
    except AuthenticationError:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
```

**Benefits:**
- ✅ Testability: Mock UserRepository, JWTHandler, PasswordHasher in unit tests (no FastAPI, no DB)
- ✅ Flexibility: Swap SQLAlchemy for PostgreSQL asyncpg without changing business logic
- ✅ Framework independence: Domain layer has zero FastAPI dependencies
- ✅ Clear boundaries: Presentation → Service → Domain → Infrastructure (unidirectional)

**Drawbacks:**
- ❌ Boilerplate: More files/classes than monolithic approach
- ❌ Complexity: May be overkill for simple auth (3-5 endpoints)

**Applicability:**
- ✅ Complex business logic (custom auth flows, multi-tenancy)
- ✅ Long-term projects (>6 months, maintainability prioritized)
- ✅ Team size ≥3 devs (architecture investment pays off)
- ❌ Simple CRUD auth (direct FastAPI routes sufficient)
- ❌ Prototypes/MVPs (architecture overhead not justified)

**DevForgeAI Alignment:**
- ✅ Matches architecture-constraints.md (domain/service/infrastructure layers)
- ✅ Repository pattern per coding-standards.md
- ✅ No anti-patterns (no God Objects, no hardcoded values)

---

#### Pattern 3: JWT Blacklist for Logout/Revocation (Quality: 7.5/10)

**Source:** fastapi-auth-jwt (680 stars, 7/10 quality)
**Files:** `app/auth/jwt_blacklist.py`, `app/auth/dependencies.py`

**Pattern Description:**
Implement logout by blacklisting JWTs. Store revoked token JTIs (JWT ID claim) in Redis with TTL matching token expiration. On each request, check if token JTI is blacklisted.

**Code Example:**
```python
# app/auth/jwt_blacklist.py
import aioredis
from datetime import timedelta

class JWTBlacklist:
    """JWT revocation via Redis blacklist."""

    def __init__(self, redis_url: str):
        self.redis = aioredis.from_url(redis_url)

    async def revoke_token(self, jti: str, expires_in_seconds: int):
        """Add token JTI to blacklist with TTL."""
        await self.redis.setex(
            f"blacklist:{jti}",
            expires_in_seconds,
            "revoked"
        )

    async def is_revoked(self, jti: str) -> bool:
        """Check if token JTI is blacklisted."""
        return await self.redis.exists(f"blacklist:{jti}") > 0


# app/auth/dependencies.py
from fastapi import Depends, HTTPException, Header
from jose import jwt, JWTError
from app.auth.jwt_blacklist import JWTBlacklist

blacklist = JWTBlacklist(redis_url=REDIS_URL)

async def get_current_user(authorization: str = Header(...)):
    """Extract authenticated user, checking blacklist."""
    token = authorization.replace("Bearer ", "")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        jti = payload.get("jti")  # JWT ID claim
        user_id = payload.get("sub")

        # Check if token revoked
        if await blacklist.is_revoked(jti):
            raise HTTPException(status_code=401, detail="Token revoked")

        return User(id=user_id, email=payload.get("email"))

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# app/routes/auth.py
@router.post("/logout")
async def logout(
    current_user: User = Depends(get_current_user),
    authorization: str = Header(...)
):
    """Logout by revoking current access token."""
    token = authorization.replace("Bearer ", "")
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    jti = payload.get("jti")
    exp = payload.get("exp")

    # Calculate remaining TTL
    expires_in = exp - int(datetime.utcnow().timestamp())

    # Revoke token
    await blacklist.revoke_token(jti, expires_in)

    return {"message": "Logged out successfully"}
```

**Benefits:**
- ✅ Immediate logout (token revoked instantly)
- ✅ Scalable (Redis in-memory, fast lookups)
- ✅ Auto-expiry (TTL matches token expiration, no cleanup needed)

**Drawbacks:**
- ❌ Redis dependency (additional infrastructure)
- ❌ Latency: Extra Redis call on every authenticated request (+5-10ms)
- ❌ Blacklist growth (if many concurrent users logging out)

**Applicability:**
- ✅ Apps requiring immediate logout (security requirement)
- ✅ Multi-device support (revoke on one device affects all)
- ❌ Stateless-only architecture (blacklist adds state)

**Alternative:** Don't implement logout (rely on short token TTL, accept 15 min grace period after "logout")

---

### Common Pitfalls from GitHub Issues

#### Pitfall 1: Missing JTI Claim in JWT

**Source:** fastapi-realworld-example-app Issue #78

**Problem:**
```python
# BAD: JWT without JTI (cannot blacklist for revocation)
payload = {"sub": user_id, "exp": expiration}
token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
```

**Impact:** Cannot implement logout (no unique token identifier for blacklist)

**Solution:**
```python
# GOOD: Include JTI claim (UUID for uniqueness)
import uuid

payload = {
    "sub": user_id,
    "exp": expiration,
    "jti": str(uuid.uuid4())  # Unique token ID
}
token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
```

**Evidence:** 3 repositories had this issue, fixed in 2023-2024
**Fix:** [PR #82](https://github.com/nsidnev/fastapi-realworld-example-app/pull/82)

---

#### Pitfall 2: Refresh Token Reuse Vulnerability

**Source:** full-stack-fastapi-postgresql Issue #892

**Problem:**
```python
# BAD: Refresh token can be used multiple times (security risk)
@router.post("/refresh")
async def refresh(refresh_token: str):
    payload = jwt.decode(refresh_token, SECRET_KEY)
    # Create new access token
    new_access_token = create_access_token({"sub": payload["sub"]})
    # ❌ Refresh token NOT rotated (can be reused if stolen)
    return {"access_token": new_access_token}
```

**Impact:** If refresh token stolen, attacker can create unlimited access tokens

**Solution:**
```python
# GOOD: Rotate refresh token on each use (one-time use)
@router.post("/refresh")
async def refresh(refresh_token: str, user_repo: UserRepository = Depends()):
    payload = jwt.decode(refresh_token, REFRESH_SECRET_KEY)
    user_id = payload["sub"]

    # Verify refresh token valid (not already used)
    is_valid = await user_repo.is_refresh_token_valid(user_id, refresh_token)
    if not is_valid:
        raise HTTPException(status_code=401, detail="Refresh token already used or revoked")

    # Revoke old refresh token
    await user_repo.revoke_refresh_token(refresh_token)

    # Issue NEW access + refresh tokens
    new_access_token = create_access_token({"sub": user_id})
    new_refresh_token = create_refresh_token({"sub": user_id})

    # Store new refresh token
    await user_repo.save_refresh_token(user_id, new_refresh_token)

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token  # ✅ Rotated!
    }
```

**Evidence:** OAuth 2.0 RFC 6749 Section 10.4 recommends refresh token rotation
**Fix:** [PR #894](https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/894)

---

#### Pitfall 3: Weak JWT Secret Key

**Source:** Multiple repositories (security audit findings)

**Problem:**
```python
# BAD: Weak secret key (easily brute-forced)
SECRET_KEY = "mysecretkey"  # ❌ Only 11 characters, no special chars
```

**Impact:** JWT can be forged if secret compromised via brute force

**Solution:**
```python
# GOOD: Strong secret key (256-bit random)
import secrets

# Generate once and store in environment variable
SECRET_KEY = secrets.token_urlsafe(32)  # 256-bit random key
# Example: "dGhpc2lzYXZlcnlsb25nc2VjcmV0a2V5dGhhdGlzaGFyZHRvZ3Vlc3M"

# In production: Load from environment variable
import os
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not SECRET_KEY or len(SECRET_KEY) < 32:
    raise ValueError("JWT_SECRET_KEY must be at least 32 characters")
```

**Evidence:** OWASP Top 10 2021 (A02:2021 - Cryptographic Failures)
**Severity:** CRITICAL (anti-patterns.md violation)

---

### Architectural Insights

#### Insight 1: Domain Layer Purity (Zero Infrastructure Dependencies)

**Observation:** Top 3 repositories (cosmic-python, full-stack-fastapi, fastapi-microservices) all have pure domain layer with zero external dependencies.

**Pattern:**
```python
# src/domain/user.py (Pure Python - No FastAPI, No SQLAlchemy imports)
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class User:
    """User domain entity (pure business logic)."""

    id: Optional[int]
    email: str
    hashed_password: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    def activate(self):
        """Business rule: Activate user account."""
        self.is_active = True
        self.updated_at = datetime.utcnow()

    def change_password(self, new_hashed_password: str):
        """Business rule: Update password."""
        self.hashed_password = new_hashed_password
        self.updated_at = datetime.utcnow()

    @classmethod
    def from_orm(cls, model):
        """Factory: Create domain entity from ORM model."""
        return cls(
            id=model.id,
            email=model.email,
            hashed_password=model.hashed_password,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
```

**Benefits:**
- ✅ Business logic testable without framework (pure Python unit tests)
- ✅ Framework swaps possible (change FastAPI to Flask, keep domain logic)
- ✅ Clear separation of concerns (domain = business, infrastructure = tech)

**DevForgeAI Alignment:**
- ✅ Matches architecture-constraints.md: "Domain layer must not depend on infrastructure"
- ✅ Supports test pyramid (70% unit tests in domain layer)

---

#### Insight 2: Dependency Injection via FastAPI Depends

**Observation:** All 8 repositories use FastAPI Depends for dependency injection (not manual instantiation).

**Pattern:**
```python
# Dependency providers (in app/api/dependencies.py)
async def get_db() -> AsyncSession:
    """Database session dependency."""
    async with async_session_maker() as session:
        yield session

async def get_user_repository(db: AsyncSession = Depends(get_db)) -> UserRepository:
    """UserRepository dependency."""
    return SQLAlchemyUserRepository(db)

async def get_jwt_handler() -> JWTHandler:
    """JWTHandler dependency."""
    return JWTHandler(
        secret_key=os.getenv("JWT_SECRET_KEY"),
        algorithm="HS256",
        access_token_ttl=900,  # 15 minutes
        refresh_token_ttl=604800  # 7 days
    )

async def get_auth_service(
    user_repo: UserRepository = Depends(get_user_repository),
    jwt_handler: JWTHandler = Depends(get_jwt_handler),
    password_hasher: PasswordHasher = Depends(get_password_hasher)
) -> AuthenticationService:
    """AuthenticationService dependency (composed of other deps)."""
    return AuthenticationService(user_repo, jwt_handler, password_hasher)

# Usage in routes
@router.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthenticationService = Depends(get_auth_service)
):
    """Dependency injection: auth_service auto-injected with all deps."""
    result = await auth_service.login(form_data.username, form_data.password)
    return result
```

**Benefits:**
- ✅ Testability: Override dependencies in tests (inject mocks)
- ✅ Lifecycle management: FastAPI handles cleanup (yield pattern)
- ✅ Composition: Complex dependencies auto-wired (get_auth_service composes 3 deps)

**Rationale:** FastAPI Depends is declarative dependency injection (similar to Spring, ASP.NET Core)

---

## Framework Compliance Check

**Validation Date:** 2025-11-17 19:42:55
**Context Files Checked:** 6/6 ✅

| Context File | Status | Violations | Details |
|--------------|--------|------------|---------|
| **tech-stack.md** | ✅ PASS | 0 | Extracted patterns use Python + FastAPI (locked in tech-stack.md) |
| **source-tree.md** | ✅ PASS | 0 | Hexagonal architecture matches recommended structure |
| **dependencies.md** | ✅ PASS | 0 | All libraries (python-jose, passlib, aioredis) are standard FastAPI ecosystem |
| **coding-standards.md** | ✅ PASS | 0 | Async patterns, type hints, PEP 8 naming all followed |
| **architecture-constraints.md** | ✅ PASS | 0 | Domain layer purity maintained (zero infrastructure deps) |
| **anti-patterns.md** | ✅ PASS | 0 | No God Objects, secrets from env vars, no SQL concatenation |

**Quality Gate Status:** ✅ PASS (zero violations, exemplary framework compliance)
**Recommendation:** All extracted patterns are framework-compliant. Hexagonal architecture and repository pattern should be adopted as DevForgeAI standards for authentication implementation.

---

## Workflow State

**Current State:** Ready for Dev
**Research Focus:** Implementation patterns and code examples (appropriate for pre-development research)
**Staleness Check:** ✅ CURRENT (research completed 2025-11-17 for STORY-042, story status Ready for Dev)

**Research Timing:**
- ✅ Ready for Dev phase ideal for repository archaeology (need concrete code examples)
- ✅ Findings directly inform TDD Red phase (test patterns)
- ✅ Code patterns guide Green phase implementation

---

## Recommendations

### 1. Hexagonal Architecture + Repository Pattern ⭐ (Quality: 9.2/10)

**Approach:** Ports & Adapters with Repository abstraction for auth service
**Evidence:** cosmic-python (9/10 quality, DDD Book), full-stack-fastapi (9/10), fastapi-microservices (8/10)

**Implementation:**
- Domain layer: User, Token entities (pure Python)
- Service layer: AuthenticationService use case (orchestration)
- Infrastructure: SQLAlchemyUserRepository, JWTHandler adapters
- Presentation: FastAPI routes (thin HTTP layer)

**Benefits:**
- ✅ Testability (domain 100% unit testable without DB/framework)
- ✅ Flexibility (swap FastAPI, swap SQLAlchemy independently)
- ✅ Framework compliance (perfect alignment with architecture-constraints.md)
- ✅ Proven at scale (19K stars, production usage documented)

**Implementation Effort:** 1-2 weeks (4 layers, 8-12 files, comprehensive tests)
**Recommendation:** **ADOPT** (high confidence for STORY-042 implementation)

---

### 2. Password + Refresh Token Flow (Quality: 9.0/10)

**Approach:** OAuth 2.0 password grant with refresh token rotation
**Evidence:** full-stack-fastapi (19K stars), fastapi-users (4.5K stars)

**Implementation:**
- /token endpoint: Exchange email/password for access + refresh tokens
- /refresh endpoint: Exchange refresh token for new access token (rotate refresh)
- 15 min access token TTL, 7 day refresh token TTL
- Store refresh tokens in DB for revocation

**Benefits:**
- ✅ Security (short access tokens, refresh rotation)
- ✅ UX (seamless re-auth for 7 days)
- ✅ Revocation (logout invalidates refresh token)

**Implementation Effort:** 3-5 days (token creation, refresh flow, revocation, tests)
**Recommendation:** **ADOPT** (OAuth 2.0 standard pattern)

---

### 3. JWT Blacklist for Logout (Quality: 7.5/10)

**Approach:** Redis-backed JWT revocation via JTI blacklist
**Evidence:** fastapi-auth-jwt (680 stars, 7/10 quality)

**Implementation:**
- Redis instance for blacklist storage
- Add JTI claim to JWTs
- Check blacklist on each authenticated request
- Auto-expiry via Redis TTL

**Benefits:**
- ✅ Immediate logout (no 15 min grace period)
- ✅ Multi-device support (revoke across all devices)

**Drawbacks:**
- ❌ Redis dependency (ops complexity)
- ❌ Performance overhead (+5-10ms per request)

**Implementation Effort:** 2-3 days (Redis integration, blacklist logic, tests)
**Recommendation:** **DEFER** (implement in Phase 2 after MVP, use short TTL for MVP)

---

## Risk Assessment

| Risk | Severity | Probability | Impact | Mitigation |
|------|----------|-------------|--------|------------|
| **Hexagonal architecture over-engineering** | MEDIUM | MEDIUM | Development slower (2 weeks vs 1 week for simpler approach) | Team has DDD experience (low learning curve), long-term project justifies investment |
| **JWT secret compromise** | CRITICAL | LOW | All tokens can be forged (complete auth bypass) | Use 256-bit random secrets, rotate quarterly, store in AWS Secrets Manager, audit access |
| **Refresh token theft** | HIGH | LOW | Attacker can maintain access for 7 days (until rotation) | Implement rotation on each use, detect suspicious refresh patterns (IP changes), optional: bind refresh token to device fingerprint |
| **Redis blacklist failure** | HIGH | LOW | Logout fails silently (revoked tokens still accepted) | Monitor Redis health, fallback to DB blacklist, alert on Redis downtime, maintain dual-write for critical revocations |
| **SQLAlchemy async misuse** | MEDIUM | MEDIUM | Blocking calls in async code (performance degradation) | Code review focuses on async/await, linting rules (ruff detect blocking), integration tests measure latency |
| **Missing token expiration** | CRITICAL | MEDIUM | Tokens valid forever (security vulnerability) | Require "exp" claim in all JWTs, validate expiration in get_current_user, automated tests check expiration |
| **N+1 query on user fetch** | HIGH | MEDIUM | API latency >500ms at 1K users (SLA breach) | Use selectinload for eager loading, add query logging, APM monitoring (DataDog), integration tests with >100 user load |

---

## ADR Readiness

**ADR Required:** Yes (Architecture pattern + OAuth flow decisions)
**ADR Titles:**
1. **ADR-XXX:** Adopt Hexagonal Architecture for Authentication Service
2. **ADR-XXY:** Implement OAuth 2.0 Password Grant + Refresh Token Flow

**Evidence Collected:** ✅ Complete

**Evidence Summary:**
- **Code patterns:** ✅ 3 patterns extracted with file paths, quality scores
- **GitHub repositories:** ✅ 8 repos analyzed (avg quality: 8.0/10)
- **Common pitfalls:** ✅ 7 pitfalls documented with fixes from issues/PRs
- **Architectural insights:** ✅ 2 major insights (domain purity, dependency injection)
- **Framework compliance:** ✅ Zero violations across all 6 context files
- **Production evidence:** ✅ 19K stars (full-stack-fastapi), 2.1K stars (cosmic-python)

**ADR 1: Hexagonal Architecture**

**Next Steps:**
1. Create `devforgeai/adrs/ADR-XXX-hexagonal-architecture-auth.md`
2. Document context: STORY-042 requires OAuth implementation, multiple patterns available
3. Record decision: Hexagonal architecture with ports/adapters
4. Document alternatives:
   - **Alternative 1:** Monolithic routes (rejected: hard to test, tight coupling)
   - **Alternative 2:** Simple 3-layer (rejected: domain depends on ORM models)
5. Note consequences: More files (12 vs 3), better testability, maintainability
6. Include evidence: cosmic-python (9/10), full-stack-fastapi (9/10), DDD Book reference
7. Reference research: RESEARCH-EXAMPLE-003

**ADR 2: OAuth 2.0 Flow**

**Next Steps:**
1. Create `devforgeai/adrs/ADR-XXY-oauth-refresh-token-flow.md`
2. Document context: Need secure authentication with logout capability
3. Record decision: Password grant + refresh token with rotation
4. Document alternatives:
   - **Alternative 1:** Single long-lived token (rejected: security risk)
   - **Alternative 2:** Session-based auth (rejected: stateful, doesn't scale)
5. Note consequences: Complexity (two tokens, rotation logic), but secure
6. Include evidence: OAuth 2.0 RFC 6749, full-stack-fastapi example (19K stars)
7. Reference research: RESEARCH-EXAMPLE-003

---

**Report Generated:** 2025-11-17 19:48:22
**Report Location:** devforgeai/research/examples/repository-archaeology-example.md
**Research ID:** RESEARCH-EXAMPLE-003
**Version:** 2.0 (template version)
