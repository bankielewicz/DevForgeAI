# ARCH-014 (draft): Ferrymap live vessel positions

Synthetic fixture. Invented project, invented decisions, invented numbers.

- Artifact: ARCH-014
- Revision: 2
- Status: **draft** - proposed, not accepted
- Project: ferrymap

## Accepted constraints this draft sits under

| ID | Constraint | Status |
| --- | --- | --- |
| ARCH-011.s3 | The mobile client is offline-tolerant; a stale position is shown with its age rather than hidden. | accepted |
| ARCH-009.s1 | PostgreSQL 16 is the only datastore. No additional storage engine without a change request. | accepted |

## The open question

The proposed design pushes vessel positions to the phone over a persistent connection so
the map updates continuously. Nobody has established that the update path can keep up.

- **Uncertain requirement:** ARCH-014.s4 - "a position change is visible on the client
  within 250 ms of the vessel reporting it, at 400 concurrent viewers of the same route."
- **Why it is uncertain:** the fan-out approach has not been built here, the 250 ms figure
  came from a design workshop rather than a measurement, and the accepted single-datastore
  rule (ARCH-009.s1) rules out the obvious cache.
- **What is waiting on it:** whether ARCH-014 is accepted as written, softened to a larger
  budget with an age indicator, or replaced by client polling.

## Not in question

The map rendering, the route model and the vessel identity scheme are settled and are not
part of any experiment.
