# tidepool-sync 3.0.0 release note (synthetic)

Invented package, invented release. Retrieved from nowhere; this file exists so a case can
supply an external trigger without a network call.

Published: 2026-09-02

## Breaking

- `SyncSession.reconcile()` no longer accepts `strategy="server"`. Reconciliation strategy
  is now negotiated per-session and the client must declare a strategy at connect time.
- The `ConflictRejected` exception is replaced by `ReconciliationRefused`, which carries a
  structured `reason` object instead of a string.

## Added

- Client-side merge helpers under `tidepool_sync.merge`.

## Deprecated

- `SyncSession.queue_depth` (removed in 3.1).

Current approved pin: 2.4.1.
