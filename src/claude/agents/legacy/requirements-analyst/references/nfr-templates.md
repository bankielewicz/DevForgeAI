# Non-Functional Requirements Templates

**Version**: 1.0
**Parent Agent**: requirements-analyst

This reference provides standard NFR templates for common quality attributes. Include relevant NFRs in every story's Technical Specification section.

---

## Performance NFRs

```markdown
**Performance Requirements**:
- API response time < 200ms (95th percentile)
- Page load time < 2 seconds
- Support 1000 concurrent users
- Database query time < 50ms
```

## Security NFRs

```markdown
**Security Requirements**:
- Authentication required (JWT tokens)
- Authorization checks on all endpoints
- Input validation and sanitization
- HTTPS only (no HTTP)
- Secrets stored encrypted
- OWASP Top 10 compliance
```

## Scalability NFRs

```markdown
**Scalability Requirements**:
- Horizontal scaling supported
- Stateless application design
- Database connection pooling
- Caching for frequently accessed data
- Asynchronous processing for heavy tasks
```

## Reliability NFRs

```markdown
**Reliability Requirements**:
- 99.9% uptime SLA
- Automatic failover on errors
- Graceful degradation
- Data backup every 6 hours
- Disaster recovery procedures documented
```

---

## Usage Guidance

1. **Always include Performance and Security** - These are mandatory for any API story
2. **Include Scalability** when the feature involves high-traffic endpoints or data-intensive operations
3. **Include Reliability** when the feature is critical to business operations or involves data persistence
4. **Customize thresholds** based on the specific context files (`tech-stack.md`, `architecture-constraints.md`)
