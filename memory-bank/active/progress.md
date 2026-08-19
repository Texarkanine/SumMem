# Progress

Clean-cut `.tree` JSON (`c` / `type: note|nap`, no `v`) and undated wake lines, as specified in `projectbrief.md`.

**Complexity:** Level 2

## 2026-08-19 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Restated intent; operator confirmed and added undated wake
    - Classified Level 2 (self-contained enhancement of codec + wake formatter)
* Decisions made
    - No dual-read of `kids`/`k`/`v`
    - Stay JSON; ignore unknown fields instead of a version field
    - `type` values are the product words `note` and `nap`
    - Wake drops `YYYY-MM-DD`; packs stay `xN <prefix>: caption`
* Insights
    - `k` next to `kids` was the original hole; full-word `type` removes that clash without compact-key theater
    - A `type` field is a discriminator, not a reason to switch to XML

## 2026-08-19 - PLAN - COMPLETE

* Work completed
    - Wrote Level 2 TDD plan in `tasks.md` (codec, wake lines, contract prose)
* Decisions made
    - Catalog dates in `store_stats` stay; only `format_wake_line` drops the day
    - Zipper `{"v":1}` fixture stays; missing `c` still fails the parse
* Insights
    - Only `test_codec.py` byte-locks JSON; nap/zoom/zipper compare through `dumps_tree` or behavior

## 2026-08-19 - PREFLIGHT - COMPLETE (FAIL (fixable))

* Work completed
    - Validated the plan against the codec, wake formatter, all affected test suites, and canonical documents
    - Reordered the existing codec steps so tests run red before `Tree.v` changes
    - Wrote `.preflight-status` with the fixable findings and advisory
* Decisions made
    - Planning must add stale wake assertions in `tests/test_wake_expand.py` and `tests/test_wake.py`
    - Planning must explicitly test and reject missing or unsupported child `type` discriminators
* Insights
    - The schema and wake changes are correctly centralized, but the listed wake test files do not cover every old formatting assertion

## 2026-08-19 - PLAN - COMPLETE (replan)

* Work completed
    - Folded preflight findings into `tasks.md`: extra wake assertions, missing/unknown `type` tests, no `else`→nap
* Decisions made
    - Enumerate `endswith(": …")` in `test_wake.py`, `test_wake_expand.py`, and `test_nap.py`, not only `YYYY-MM-DD` literals
    - Missing or unsupported child `type` raises `ValueError`
* Insights
    - Preflight's rewritten plan used the wrong codec names (`dumps_tree` / `Tree.kids`); this replan keeps `dumps_tree` / `Tree.kids` / `.summem/summem`

## 2026-08-19 - PREFLIGHT - COMPLETE

* Work completed
    - Validated the replanned implementation plan against codebase conventions and TDD requirements
    - Wrote `.preflight-status` with a PASS result
* Decisions made
    - The plan correctly addresses all requirements and is ready for the Build phase
* Insights
    - The replan successfully addressed the previous fixable findings

## 2026-08-19 - BUILD - COMPLETE

* Work completed
    - Codec emits `{c, type:note|nap}`; unknown fields ignored; missing/unknown `type` is `ValueError`
    - Wake lines undated; notes are caption-only; packs are `xN <prefix>: caption`
    - Updated VISION.md and systemPatterns.md
    - 177 pytest passed
* Decisions made
    - Proof tests that locked `" xN "` / `YYYY-MM-DD: text` were rewritten like the other wake assertions
* Insights
    - Old pack lines had a date, so grain was `" xN "` with a leading space; undated lines start with `xN `

## 2026-08-19 - QA - COMPLETE (FAIL)

* Work completed
    - QA found `systemPatterns.md` wait-free sentence still mentioned date
* Decisions made
    - Drop "date, " from that sentence; re-run QA
* Insights
    - One briefing file can contradict itself when only the heading/section was updated

## 2026-08-19 - BUILD - COMPLETE (QA fix)

* Work completed
    - Wait-free caption degradation in `systemPatterns.md` no longer names a date
* Decisions made
    - Match VISION: grain and unique prefix, no date
* Insights
    - None

## 2026-08-19 - QA - COMPLETE (FAIL)

* Work completed
    - Reviewed the build diff against the plan, brief, and acceptance criteria; re-ran the suite (177 passed)
    - Swept the tree for stale `kids`/`k`/`v` and `YYYY-MM-DD` contract prose
    - Wrote `.qa-validation-status` with one blocking finding and four advisories
* Decisions made
    - `systemPatterns.md` contradicting itself on wake dates blocks acceptance; Build must make the one-line fix
    - The dead on-disk store, the `zoom` traceback, the grain-1 empty line, and the loose exception assertion are advisories, not blockers
* Insights
    - Wake's undated contract is stated in two places in `systemPatterns.md`; the "Wake is wait-free" section repeats it and was missed
    - The repo dogfoods SumMem, so a clean-cut schema change silently kills the project's own memory even when every test passes

## 2026-08-19 - QA - COMPLETE (PASS)

* Work completed
    - Re-reviewed the complete implementation and QA rework against the plan, brief, acceptance criteria, and established patterns
    - Confirmed the prior documentation contradiction is fixed and the codec, wake formatter, tests, and canonical documentation agree
    - Re-ran the full suite: 177 pytest tests passed
* Decisions made
    - Accept the implementation as-is; the remaining four findings are non-blocking advisories already recorded in `tasks.md`
* Insights
    - The surgical QA rework resolved the only acceptance blocker without changing executable behavior
