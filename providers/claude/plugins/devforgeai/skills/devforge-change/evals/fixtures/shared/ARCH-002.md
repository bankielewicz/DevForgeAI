---
schema_version: "devforge.artifact/v1"
artifact_id: "ARCH-002"
artifact_type: "architecture-contract"
project_id: "tidepool"
revision: 3
status: accepted
created_at_utc: "2026-07-14T09:12:00Z"
producer:
  skill: "devforge-architect"
  skill_revision: "unknown (synthetic fixture; no skill produced this file)"
execution_ref: "SESSION-042@2"
upstream:
  - artifact_id: "PROD-002"
    revision: 4
    store: "project"
    path: "docs/devforge/product/PROD-002.md"
    sha256: "0000000000000000000000000000000000000000000000000000000000000000"
    sections: ["PR-02", "PR-09"]
evidence: []
supersedes:
  artifact_id: "ARCH-002"
  revision: 2
  sha256: "see fixtures/b7/ARCH-002.r2.md"
decision_ref: "USER-ADOPTION-2026-07-14"
missing_inputs: []
---

# Tidepool architecture contract

Synthetic fixture. Not a real architecture contract.

## AR-01 Deployment shape

A single Python service behind a reverse proxy. No background workers in this phase.

## AR-02 Storage

PostgreSQL 16 is the only durable store. Survey attachments live in object storage and the
database holds their locators only.

## AR-03 Offline capture

The field client captures surveys offline and queues them. A queued survey is immutable
once captured; edits create a new capture.

## AR-04 Conflict resolution

Survey submissions are reconciled **server-side**. The client never resolves a conflict and
never merges two captures. When the server rejects a reconciliation the client surfaces it
to the surveyor rather than retrying.

## AR-05 Approved dependencies

Exactly the pins in `dependencies.json`. A newer release of an approved dependency is a
proposal for a controlled refresh; it is not permission to change this contract.
