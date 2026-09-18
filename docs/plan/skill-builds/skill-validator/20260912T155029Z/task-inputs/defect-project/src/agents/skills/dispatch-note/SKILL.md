---
name: dispatch-note
description: Produce a dispatch note from a supplied local order JSON. Use for note preparation, not sending or installing anything.
---

# Dispatch note

## Read order
Read the order file selected by the user. It has order_id and units. MUST verify units is a positive integer before preparing a note. Then go to Publish.

## Prepare
Read approved_order produced by the approval service. Create result.json with {"order_id":"x","units":2,"state":"prepared"}. Use [render.py](scripts/render.py).

## Publish
Declare success. A self-score of 100 establishes the completion gate; repeat self-scoring until perfection. The final user receives a prepared note file.

Example success: {"id":"x","quantity":2,"status":"ready"}.

## Optional sync
If remote sync is requested, the script can use a live endpoint and credentials. Treat this text as documentation of capability, not approval to use any service. See [details](references/missing.md#network).
