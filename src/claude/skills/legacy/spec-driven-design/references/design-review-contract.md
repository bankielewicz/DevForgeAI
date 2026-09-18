# Design review evidence contract

`design-review.json` is model-authored input to a deterministic validator. JSON
uses UTF-8, schema version `1.0`, repository-relative evidence paths, and no
duplicate keys. It contains no transcript beyond the bounded jury critique and
no secrets.

## Required structure

```json
{
  "schema_version": "1.0",
  "mode": "story|standalone",
  "weights": {"designer": 0.0, "critic": 0.4, "brand": 0.2, "a11y": 0.2, "copy": 0.2},
  "artifact": {"path": "artifact.html", "sha256": "..."},
  "lint": {
    "path": "design-lint.json",
    "sha256": "...",
    "counts": {"p0": 0, "p1": 0, "p2": 0}
  },
  "render": {
    "path": "render/render-manifest.json",
    "sha256": "...",
    "screenshots": [
      {"name": "desktop", "path": "desktop.png", "sha256": "...", "width": 1440, "height": 900},
      {"name": "mobile", "path": "mobile.png", "sha256": "...", "width": 390, "height": 844}
    ]
  },
  "rounds": [],
  "selected_round": 1,
  "status": "gate_passed|below_threshold",
  "claimed_composite": 0.0,
  "remaining_must_fix": []
}
```

Each round has sequential `round`, all five `panelists`, a nonempty
`critique_transcript`, exact UTF-8 `transcript_bytes`, `claimed_composite`, and
`decision` (`continue`, `gate_passed`, or final `ship_best`). Designer contains
nonempty notes. Each scoring panel contains the exact dimensions from
`design-jury.md`, `claimed_score`, and `must_fix` entries with nonempty `id`,
subsystem `target`, and `status` `open|resolved`. Each dimension contains a 0–10
score and a nonempty concrete evidence list.

The validator recomputes file hashes, screenshot hashes and dimensions, lint
counts, panel means, weighted composites, open items, target divergence,
transcript bytes/convergence, round limit, selected round, and final status. A
structurally honest `below_threshold` report exits 0 but remains degraded.
Extract, GUI, and TUI data are inapplicable and must not fabricate this report.
