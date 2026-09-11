---
schema_version: "devforge.artifact/v1"
artifact_id: "CHANGE-011"
artifact_type: "change-request"
project_id: "riverbend-running-club"
revision: 1
status: accepted
created_at_utc: "2026-09-08T19:02:00Z"
producer:
  skill: "devforge-change"
  skill_revision: "unknown (fixture; no installed SKILL.md was hashed)"
execution_ref: null
upstream:
  - artifact_id: "PROD-001"
    revision: 2
    store: project
    path: "docs/devforge/product/PROD-001.md"
    sha256: "f7396e407445c4f401e494cca71916464a342ce5895d1c2830f13fc847987179"
    sections:
      - "REQ-002"
      - "REQ-004"
      - "Explicit non-goals"
evidence: []
supersedes: null
decision_ref: null
missing_inputs:
  - "No estimate of how many members would give a phone number for text alerts."
---

# Change request: tell people when a session is cancelled

Synthetic fixture. Invented for evaluation.

## What is being requested

Two leaders have asked for cancellations to reach members who have marked themselves in, rather than only changing the page. The suggested mechanism is a text message.

## Why

Reported by Priya (run leader), 2026-09-07: on the 6th, a session was cancelled at 05:50 and four people who had marked themselves in still travelled to the meeting point. This is one incident, self-reported, and no record was kept.

## Scope of the amendment

- Affects PROD-001 REQ-002 and REQ-004, which record who is in but do nothing with the fact.
- Directly contradicts PROD-001's explicit non-goal "push notifications of any kind (IDEA-004)".
- Would introduce a dependency on a paid messaging service. No budget has been discussed.

## Status of this document

`status: accepted` here records that the change process accepted this request **for assessment**. It is not the user adopting it into a product brief, and it is not authorisation to widen the release scope. `decision_ref` is null because no such adoption exists.
