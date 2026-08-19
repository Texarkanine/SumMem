---
task_id: zipper-heal
date: 2026-08-19
complexity_level: 3
---

# Reflection: zipper-heal

## Summary

Zipper-heal landed on `.summem/summem`: overlapping nap leaf-sets after merge are rematerialized on the next `note` or `nap` into a cover of unique leaves; `write_nap` refuses overlapping packs; wake stays wait-free. 134 tests. First QA failed on an unreachable unique-cover assert in the merge proof; rework then passed.

## Requirements vs Outcome

The brief is met: issue #3's zipper on `note`/`nap` only; ⊆ drop; split-smaller rematerialize from `.tree`; skip note-note; vanished nap ids succeed; remainder keeps grain (`8+2+1` does not concat); `fcntl.flock` of `naps/` for one mutating invocation; crash order is write-children-then-unlink, recovery is ⊆. Out of milestone as planned: containment pass, aligned `cover(T)`, flatten-as-normal, zipper inside wake, a lock file, scopes. No requirement was dropped. Requirement 6's "Wake projection still bounds the listing" was already the at/over-budget list-files rule; the plan's "two lines via expand" at budget 2 contradicted `VISION.md` and the build followed the contract.

## Plan Accuracy

The five-unit split (leaf-sets, heal_view, `write_nap` guards, flock+CLI, contract wording) was the right sequence. File lists held. The plan itself was rewritten twice before a passing preflight: first it still had a containment pass, an action-list return, and a lock file; then TDD order for merge/crash/budget tests sat after production code, `Action` was undefined, and termination was not a decreasing measure. The locked third plan is what got built. Two surprises were not in the unit lists: `8+2+1` at `WAKE_LINES=2` prints three files, and the flagship merge proof's unique-cover assert was indented under `continue`.

## Creative Phase Review

No creative phase. The operator locked remainder grain, local flock, and "do not zipper inside wake" before plan; later locks (flock the `naps/` directory, ⊆ only, `require_entry` before lock) arrived as preflight/plan amendments. That was the right skip: the unknowns were encoding, not a fork of product shape.

## Build & QA Observations

Leaf-sets, ⊆ drop, ABD/ABE rematerialize, overlap guards, and `naps/` flock went green against the locked tests. Same-process `flock` succeeds again; the lock test needed a second process. First QA (claude-opus-5-thinking-high) reproduced no product bug: heal already yielded a disjoint cover, but `assert sa.isdisjoint(sb)` never ran. Second QA ([Zipper-heal QA review](30dad4e9-9b46-4f2c-9a76-b3972401fa2d), gemini-3.1-pro) passed the helper promotion, the `while True` loop, and `_TREE_PARSE_ERRORS`. Finding 8 stands: `VISION.md` First proof item 6 still names only disjoint packs. The overlapping case is covered by tests and by the Long-lived branches paragraph, not by a numbered proof.

## Cross-Phase Analysis

Issue #3's "containment pass" is why the first plan built a pass that ⊆ already covers; the operator lock after first preflight is why crash leftovers are a retry of drop-subset, not a second algorithm. Second preflight's Action/YAGNI finding is why `heal_view` returns `None` and tests assert store state. The plan vs `VISION.md` fight on `8+2+1` is why the accepted wake deviation exists: unit 2 wrote "two lines via expand" after equal-grain had already defined at-budget as list-files. The unreachable unique-cover assert is a copy-paste of `test_zipper.py`'s helper into the proof; first QA's AST scan for statements after `continue` is the only reason that hole was not archived as green. Promoting the helper is the actual fix. `_HEAL_PASS_LIMIT` was unplanned production code that turned a hang into a silent overlapping store; the plan had already put the cap in tests.

## Insights

### Technical

- A note that intersects a nap is a subset. After the ⊆ branch, split always rematerializes a nap; an `isinstance(..., NapChild)` return there is dead, and if it fired it would abort the whole heal.
- Same-process `flock` is not contention. A lock test that opens `naps/` twice in one interpreter will pass; the second acquire has to be another process.
- `WAKE_LINES` is a printed-line budget, not a shrink-to-fit. Heal to `8, 2, 1` at budget 2 lists three files and prints no fold request.

### Process

- An acceptance proof that copies a helper can go green while the copy's assert is unreachable. Put the unique-cover oracle in `tests/gitutil.py` and scan for statements after `continue`/`return` before calling a proof done.
- Do not encode a lock file, an action-list API, or a production iteration ceiling that the locked design did not ask for. Two preflights were spent stripping those.
- When the headline behavior is a new merge case, either add a First proof item in the same unit that edits Long-lived branches, or write down that the existing disjoint item still stands and overlapping is a test. Leaving the checklist unchanged will keep failing documentation QA.
