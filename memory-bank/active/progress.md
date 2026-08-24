# Progress

Move the versioned agent how-to from the committed `AGENTS.md` prefix onto the root `wake` document, leaving a small bootstrap that does not move when the script's usage details change.

**Complexity:** Level 3

## 2026-08-24 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Restated intent; operator approved.
    - Branched `feat/wake-usage-prompt` from `main`.
    - Classified Level 3.
* Decisions made
    - Not a bug (Q1 no). Enhancement to existing activation (Q2 yes) that is not self-contained (Q2a no): prompt text, root-wake document, `init`, lockstep tests, and the skip/re-wake rule must move together (Q2b yes) → Level 3.
    - Not Level 4: store, fold, and ingest do not change; one design, one feature branch.
* Insights
    - The original activation feature (`agents-prompt`, issue #2) was Level 2. Relocating HOW is the same subsystem with a real design fork, which is why this is Level 3 rather than another Level 2 wording pass.

## 2026-08-24 - CREATIVE - COMPLETE

* Work completed
    - Explored agent-document split (architecture).
    - Wrote `memory-bank/active/creative/creative-agent-document-split.md`.
* Decisions made
    - Stable verbs: bootstrap keeps wake-if-needed, note, and writer-only. Versioned HOW is `how_to_text()` on root `wake` under `== SumMem Usage ==`.
    - Skip keys off a readable Usage block, not “a prior wake” or `You are up to speed.`
    - Pointer-only rejected (drops always-on note duty). Dual-publish rejected (does not remove the upgrade tax).
* Insights
    - Existing consumers need one shrink of the old fat prefix. After that, script copies leave `AGENTS.md` alone.
    - Root-wake tests that forbid `.summem/summem` and `wake --path` in the whole stdout will fight Usage. Those pins belong on the catalog section only.
