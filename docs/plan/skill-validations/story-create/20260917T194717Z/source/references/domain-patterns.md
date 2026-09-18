# Behavioral pattern prompts

Load only rows relevant to selected outcomes. These prompts preserve the source's domain coverage without prescribing a stack, vendor, UI, legal standard or numeric product policy. Derive concrete values from current project requirements and sources; unresolved values remain decisions. For changing external standards or technical claims, consult their current primary documentation when needed and cite the actual source.

| Family | Successful behavior | Boundaries and failures to consider |
| --- | --- | --- |
| Create | Authorized valid record is persisted once; response identifies it | Required fields, duplicates/uniqueness, invalid relationships, rollback and retried creation |
| Read | Authorized list/detail uses current contract and correct filters | Missing object, empty state, unauthorized records, stale/deleted data and pagination boundaries |
| Update | Allowed fields change with the declared concurrency rule | Lost updates, immutable fields, partial updates, invalid state and competing writers |
| Delete | Selected soft/hard deletion behavior and related-data policy | Confirmation when required, foreign dependencies, repeated deletion, recovery and retention rules |
| Registration | Eligible user is registered under actual verification policy | Duplicate identifiers, invalid credentials, verification expiry/reuse and partial registration |
| Login/logout | Valid credentials establish the selected session; logout revokes it as specified | Invalid credentials, configured throttling/lockout, revoked sessions, enumeration and recovery |
| Authorization | Permitted role/owner performs the selected action | Missing permission, cross-tenant access, direct API bypass, unchanged state on denial |
| State transitions | Legal transition produces its output once | Forbidden transitions, concurrent events, cancellation boundaries, atomicity and retry |
| Approval | Correct actor submits/approves/rejects with a reason and trace | Unauthorized reviewer, duplicate decisions, separation of duties where required and withdrawn requests |
| Validation | Valid field/range/format accepted with clear feedback | Empty/null, limits, Unicode, dates/time zones, numeric overflow and schema mismatch |
| Search/filter | Correct matching and combined filters over selected scope | No results, invalid filters, escaping, stale indexes, permission filtering and cancellation |
| Pagination/sort | Stable order and navigation across pages | Empty/last page, tie ordering, data changes, invalid cursors and retained filter state |
| Upload | Accepted file is stored and usable under declared limits | Type/content mismatch, size/count boundaries, malicious names, partial transfer, cleanup and duplicates |
| Real-time events | Authorized subscribers see ordered/current state | Disconnect, reconnect, duplicate/out-of-order events, backpressure and missed updates |
| Async work | Accepted job reports meaningful status and final result | Cancellation, retry limits, timeout, stale progress, restart recovery and idempotency |
| Reporting | Correct aggregates/filters/units/time windows and drill-down | Missing/partial data, empty results, permission scope and consistency with detail records |
| Export | Selected records/columns/encoding are preserved | Escaping, spreadsheet formula injection where relevant, size, partial delivery and privacy filters |
| External API | Correct request/response, authentication and data mapping | Timeout, rate limit, bad response, retry budget, partial failure and secrets handling |
| Payment | Selected amount/currency and transaction outcome | Duplicate charge, declined payment, interrupted response, reconciliation and sensitive-data handling |
| Webhook | Verified event is processed once and acknowledged | Invalid signature, replay, unknown event, duplicate/out-of-order delivery and recovery |
| Performance | Source-defined latency/throughput/resources under a stated workload | Percentiles, saturation, realistic data size, warm/cold state and measurement method |
| Security | Concrete threat mitigations and permission invariants | Injection, script execution, request forgery, credential leakage, abuse limits and denial side effects |
| Accessibility | Selected users can complete the entire interaction | Keyboard/focus, accessible names, error announcements, contrast, zoom/reflow and assistive technology |
| Documentation | Selected reader can find and follow accurate instructions | Broken/stale references, missing prerequisites, examples mistaken for available commands |

For instance, a cancellation race criterion should state the allowed final states and prohibit contradictory dispatch/cancellation results. “Handle races” gives no test oracle. An upload criterion should name the selected byte/count/type limits and cleanup outcome; selecting a limit from an example would change the product without a source decision.
