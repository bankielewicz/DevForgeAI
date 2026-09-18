# Architect Reviewer - Scalability Assessment Reference

## Scalability Assessment

### Horizontal Scaling

**Requirements:**
- Stateless application design
- Session data in external store (Redis, database)
- Shared filesystem or object storage
- Load balancer distributes requests

**Red Flags:**
- In-memory session storage
- File uploads to local disk
- Server-specific state
- No load balancing strategy

### Vertical Scaling

**When Appropriate:**
- Monolithic applications
- Single-threaded workloads
- Database-bound operations
- Short-term solution

**Limitations:**
- Hardware limits (CPU, RAM)
- Higher cost per unit
- Downtime during upgrades
- Not elastic

### Database Scaling

**Read Scaling:**
- Read replicas
- Caching (Redis, Memcached)
- Materialized views
- Eventual consistency acceptable

**Write Scaling:**
- Sharding by key (user ID, tenant ID)
- Partitioning by date/time
- CQRS (Command Query Responsibility Segregation)
- Event sourcing

**Red Flags:**
- N+1 query problems
- No connection pooling
- Missing indexes
- No query optimization

### Caching Strategy

**What to Cache:**
- Expensive computations
- Frequently accessed data
- Slow external API responses
- Session data

**Cache Invalidation:**
- Time-based expiration (TTL)
- Event-based invalidation
- Cache-aside pattern
- Write-through vs write-behind

**Red Flags:**
- No caching for expensive operations
- Cache never invalidated (stale data)
- Caching everything (memory waste)
- No cache hit rate monitoring
