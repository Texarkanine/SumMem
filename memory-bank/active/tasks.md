# Task: nap-ack

* Task ID: nap-ack
* Complexity: Level 2
* Type: simple enhancement

Successful `nap` prints `Saved.` then either the next fold prompt or `Nothing left to compress.` The over-long ratchet still does not ACK. `fold_request` stays a prompt builder.

## Test Plan (TDD)

### Behaviors to Verify

- Mid-cascade `nap` → stdout starts with `Saved.`, then a blank line, then the next equal-grain pair and `Run:` (same prompt `fold_request` already builds).
- Mid-cascade `nap` when more folds remain after the next one → that prompt still includes `N compression(s) remain after this one.`
- Last `nap` of a cascade (view at or under budget, or no equal-grain pair) → `Saved.\n\nNothing left to compress.\n`
- Over-long `nap` caption (ENTRY_CHARS ratchet) → exit 1, stderr has `Compress it further.`, stdout has no `Saved.`
- Over-long `note` → still no `Saved.` (existing test).
- Under-budget `note` → still `Saved.\n` only; no `Nothing left to compress.`
- `fold_request()` itself still returns `""` when at budget (no ACK, no idle inside the helper).

### Test Infrastructure

- Framework: pytest as configured in `pytest.ini` (`testpaths = tests`)
- Test location: `tests/`
- Conventions: `test_<behavior>` functions, `tmp_path` + `init_repo`, `monkeypatch.chdir`, `capsys` for CLI stdout, `summem` session fixture; iterate with `tox -e py311 -- tests/test_fold.py::…`
- New test files: none

## Implementation Plan

### 1. Nap CLI stdout — executable

- Files: `tests/test_fold.py`, `tests/test_cli.py`, `summem`

1. Stub tests: in `tests/test_fold.py`, keep `test_nap_prints_remaining_ones_not_parent_plus_one` and `test_nap_prints_nothing_when_at_or_under_budget` (rename the second to `test_nap_prints_saved_and_idle_when_at_or_under_budget`); add `test_nap_prints_remaining_count_after_saved` (five notes, budget 2, first nap). In `tests/test_cli.py`, add `test_rejected_nap_does_not_print_saved` beside `test_rejected_note_does_not_print_saved`. Empty bodies.
2. Stub interface: no new public function. `main`'s `nap` arm already returns `fold_request` text; leave a comment on that arm that success stdout is ACK then fold or idle. Do not change `fold_request`.
3. Write tests and run red: mid-cascade `assert out.startswith("Saved.\n")` and `out.index("Saved.") < out.index("Compress these two")`; remaining-count line present after ACK; at-budget `assert out == "Saved.\n\nNothing left to compress.\n"`; over-long nap `assert "Saved." not in captured.out`; strengthen `test_under_budget_note_prints_saved` with `assert "Nothing left to compress." not in out`. Run `tox -e py311 -- tests/test_fold.py tests/test_cli.py::test_rejected_nap_does_not_print_saved tests/test_cli.py::test_rejected_note_does_not_print_saved tests/test_cli.py::test_cli_nap_overlong_prints_ratchet`. Expect red on empty/missing ACK and idle.
4. Write code and run green: in `main`'s successful `nap` path (`summem`, after `with_store_lock`), print `Saved.\n`; if `out` is non-empty, blank line then `out`; else blank line then `Nothing left to compress.\n`. Same spacing as `note`. Reject paths unchanged (`require_entry` still returns 1 before lock). Re-run the same tox posargs, then `tox -e py311` for the file set.

### 2. Operator and briefing copy — prose/policy

- Files: `README.md`, `memory-bank/systemPatterns.md`
- No tests: prose/policy artifact

1. README Example: the `nap` invocation currently shows empty stdout; show `Saved.` then `Nothing left to compress.` for that at-budget fold.
2. `systemPatterns.md` How This System Works: replace “`nap` prints only the fold request” with successful `nap` prints `Saved.` then maybe the fold request or `Nothing left to compress.` Keep “Do not put the ACK inside `fold_request`.”

## Technology Validation

No new technology - validation not required

## Dependencies

- Existing `fold_request` remaining-count line (`1 compression remains after this one.` / `N compressions remain after this one.`)
- OptMem idle copy: `Nothing left to compress.`
- `note` ACK path in `main` as the spacing template

## Challenges & Mitigations

- Idle inside `fold_request` would make under-budget `note` print `Nothing left to compress.`: print idle only on the `nap` arm when `fold_request` returned `""`.
- Over-budget view with no equal-grain pair: `fold_request` is already `""`; idle then means “no next nap,” not “view is at WAKE_LINES.” Same honesty as `note` in `test_over_budget_note_prints_saved_when_16_plus_1`. Do not invent a second message.
- Deleting empty-stdout tests would drop remaining-pair coverage: retarget those cases.

## Pre-Mortem

- ACK bolted onto `fold_request` so `note` and `nap` share a lie: already covered by Challenge 1; plan keeps the helper a prompt builder.
- README still demos a silent `nap`, so operators copy the old contract: prose step 2.1 updates that example.
- Phrase-locking `how_to_text` / `prompt_text`: not scheduled; stdout is the contract. Do not add change-detectors on prompt files.

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [x] Preflight
- [x] Build
- [ ] QA
