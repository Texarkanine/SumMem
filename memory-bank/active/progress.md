# Progress

Successful `nap` prints `Saved.` then either the next fold prompt or `Nothing left to compress.`; the over-long ratchet still does not ACK.

**Complexity:** Level 2

## 2026-08-28 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Restated intent: nap ACK + idle line; ratchet stays silent; retarget nap-stdout tests
    - Classified Level 2
* Decisions made
    - Enhancement, not a bug: #27 left `nap` stdout unchanged on purpose
    - Self-contained: `nap` command stdout and its tests; `fold_request` is not the ACK printer
    - `Nothing left to compress.` is nap-only; a note with no fold stays `Saved.` only
* Insights
    - `"Saved." not in` / empty-stdout nap tests encode the old contract and must be retargeted, not deleted
