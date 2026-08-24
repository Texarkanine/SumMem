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

## 2026-08-24 - PLAN - COMPLETE

* Work completed
    - Wrote the Level 3 plan in `memory-bank/active/tasks.md`.
    - Mapped TDD onto `how_to_text`, bootstrap `prompt_text`, root-wake composition, and briefing docs.
* Decisions made
    - `how_to_text()` includes the `== SumMem Usage ==` header (same shape as `catalog_text()`).
    - Usage does not count against `WAKE_LINES`.
    - No new test files. Extend `tests/test_init.py` and `tests/test_scopes.py`; retarget two proofs.
* Insights
    - `test_proof_scopes.py` and several `test_scopes.py` cases will fail for the right reason: they treat the whole root-wake stdout as catalog-only.

## 2026-08-24 - PREFLIGHT - FAIL (fixable)

* Work completed
    - [Preflight](d8071f20-8b3c-40b3-89be-65162e355185) wrote `FAIL (fixable)` to `memory-bank/active/.preflight-status`.
* Insights
    - Two leftover pins were not named in numbered steps: `clone` / `another machine` on `test_prompt_text_invariants`, and `set(lines[1:-1])` on the ingest proof. Surgical “retarget this test” steps that list only some tokens leave the unlisted asserts in place.

## 2026-08-24 - PLAN - COMPLETE

* Work completed
    - Re-planned those two pins. Unit 1 pins clone-portability on `how_to_text()` and forbids `git`. Unit 2 drops `clone` / `another machine` from prompt invariants. Unit 3 slices ingest from the memories header to the footer.
    - Picked README-only for the one-time fat-prefix sentence. `init_text()` stays the new-install recipe. Dropped `test_cli.py` from unit 3 files.
* Decisions made
    - Do not version-key the Usage header (preflight radical advisory, not applied).

## 2026-08-24 - PREFLIGHT - COMPLETE (PASS WITH ADVISORY)

* Work completed
    - Second preflight on the re-plan wrote `PASS WITH ADVISORY` to `memory-bank/active/.preflight-status`.
* Decisions made
    - Prior leftover pins (clone / another machine on prompt invariants; ingest `lines[1:-1]`) are named in numbered steps; no further re-plan.
* Insights
    - Advisories are implementer cautions (drop ingest `lines[0]`, keep how_to free of `git` / `notes/` / `naps/` / other section headers, teach `wake --path <path>` not `pkg`), not plan defects.
    - Radical advisory this run: named-section wake assembler plus section-keyed tests, so exact-stdout / `lines[0]` pins cannot recur. Not applied.
