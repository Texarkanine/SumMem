---
task_id: noting-ratchet
complexity_level: 2
date: 2026-08-20
status: completed
---

# TASK ARCHIVE: noting-ratchet

## SUMMARY

[SumMem#16](https://github.com/Texarkanine/SumMem/issues/16): over-long `note` and `nap` print OptMem’s ratchet footer (`Too long: N bytes, limit L. Accented characters cost 2 bytes. Compress it further.`) using the store’s `ENTRY_CHARS`. Other agent-facing errors add a next step only at raise sites where that step is known and not obvious. Draft [PR #17](https://github.com/Texarkanine/SumMem/pull/17). 221 pytest. QA passed.

## REQUIREMENTS

- Replace `note is too long` for both `summem note` and `summem nap`.
- Footer: actual UTF-8 bytes, configured limit, accented-character hint, compress further.
- Other CLI errors: state the problem; add a next step only when known and not obvious. Do not invent a repair.
- STE100 / ISO 24495: short, one meaning per word. No store paths, hashes as paths, or git in agent-facing text.
- Empty and multi-line stay rejections. Limit and store format unchanged.

## IMPLEMENTATION

`require_entry` interpolates `limit` (not a hardcoded 280). Multi-line is `One line only. Merge the lines.` (true for nap; not “note each line”). Empty stays `note is empty`.

Raise-site copy, not a unique-string table: identity-miss `unknown id` (`resolve_id`, `_adjacent_nodes`, `zoom_text` final raise) and range tokens say to copy an id from wake; ambiguous says to give a longer prefix; not-adjacent says to nap neighbors in wake. Missing-`.tree` `unknown id` and `unreadable pack` stay problem-only.

Standing contract added to `memory-bank/systemPatterns.md`. Atlas not edited.

## TESTING

TDD on existing files (`test_store`, `test_nap`, `test_cli`, `test_scopes`, `test_zoom`, `test_wake`, `test_proof_reject`). Six new tests plus extensions: footer facts, 94 × `你` → `282`, tight-store `toolong` (7 bytes) with `capsys` drain, identity-miss vs missing-tree split. `tox` 221 passed on py311–py314. `/niko-qa` PASS (advisories only).

## LESSONS LEARNED

- A unique error string is not a unique cause. Attach the next step at the raise site, not with a global replace.
- Shared `require_entry` copy must be true for both `note` and `nap`.
- If ratchets had been the rule from the start, `note is too long` and one shared `unknown id` sentence would not have existed. Per-site strings in one script are that design.

## PROCESS IMPROVEMENTS

The first plan keyed Unit 2 on unique strings. Preflight FAIL (fixable) caught the nap-false multi-line next step and the missing-tree wake hint. Raise-site tables belong in the first plan when one phrase has two causes.

## TECHNICAL IMPROVEMENTS

A helper or exception type for (problem, next-step-or-none) would only pay off when the raise list grows again. Left as per-site strings.

## NEXT STEPS

- Draft [PR #17](https://github.com/Texarkanine/SumMem/pull/17) on `feat/noting-ratchet`. Push this archive commit onto that branch if the PR should drop `memory-bank/active/`.
