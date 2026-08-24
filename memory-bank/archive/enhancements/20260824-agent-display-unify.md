---
task_id: agent-display-unify
complexity_level: 2
date: 2026-08-24
status: completed
---

# TASK ARCHIVE: agent-display-unify

## SUMMARY

Wake, recall, and zoom share one listing grammar: dated leaves (`x1 YYYY-MM-DD: text`) and unique-prefix packs (`xN <short_id>: caption`). Recall matches note text and nap captions, not grain, day, or id prefix. Proof walkers enqueue nested pack ids from `Tree.kids`, not zoom stdout tokens. Register Memories membership is clone-portability, not eternal currency. [PR #37](https://github.com/Texarkanine/SumMem/pull/37) on `labelling`. 275 pytest. QA PASS.

## REQUIREMENTS

- One agent-facing grammar for wake, recall hits, and zoom children. Nested packs keep `xN <prefix>:` as the zoom handle; nested leaves have no hash.
- Agent stdout never prefers 64-hex. Prefixes are `short_id` among `named_ids`. Full hashes stay on disk.
- Recall regexes the sentence (loose-note text, nap caption). It does not match formatted-line fields.
- Prompt: write-time truth plus clone-portability; not “must still be true after a fresh clone.” Lockstep `prompt_text()`, `docs/agents-prompt.md`, `AGENTS.md`.
- Follow-on on PR #37. Do not reopen the dated-leaf-wake printer. Do not add a second addressing scheme.

## IMPLEMENTATION

Preflight FAIL (fixable) on the first plan: `reaches` / `zoom_reaches` treated `line.split()[0]` as a content id (that token becomes grain after `format_wake_line`), and leftover zoom/nap/recall tests still asserted `{id}  text`. Re-plan put tree walkers first and retargeted those tests.

- [`tests/gitutil.py`](../../../tests/gitutil.py): `reaches` and `zoom_reaches` enqueue `_nap_child_ids` (`NapChild.id` from the children tree). `zoom_reaches` loads the driver as `summem_gitutil` via `SourceFileLoader` so it does not import `conftest`. Zoom stdout is only the sentence check.
- [`summem`](../../../summem): `_zoom_kids` and `_recall_nested` print `format_wake_line(_projected_child(...), named_ids)`. Dropped `_zoom_note_line`. `_find_in_tree` returns `NoteChild | NapChild`. View recall searches `node.caption`; nested recall searches `child.text` / `child.sum`.
- Prompt: replaced the eternal-currency clause; lockstep documents copied the same bytes.
- Atlas § Zoom and recall and `memory-bank/systemPatterns.md` wake-dates-leaves paragraph updated in Build.

Did not reopen the wake printer (preflight advisory: recall/zoom `named_ids` can print a longer prefix than wake’s view unique-prefix for the same pack).

## TESTING

`uvx --with tox tox`: 275 passed on py311–py314 after Build and again at QA. `/niko-preflight` PASS WITH ADVISORY. `/niko-qa` PASS (advisories only). First QA spawn on gpt-5.6 hit Other Models quota; retried on grok.

New/retargeted coverage: `tests/test_gitutil.py` (reaches under a `zoom_text` monkeypatch to wake grammar); zoom/nap/recall success tests on dated leaves and pack prefixes; `test_prompt_text_invariants` forbids `must still be true after a fresh clone`.

## LESSONS LEARNED

- Changing agent stdout means walking `Tree.kids` for nested ids. Parsing `line.split()[0]` enqueues grain (`x1` / `xN`).
- One printer (`format_wake_line`) is the invariant. Match haystack (caption/text) stays separate from print.
- Overlapping plan/preflight in this workspace restored uncommitted product files to HEAD more than once. Stage as soon as a slice is green.
- Other Models quota was already spent; niko-qa/preflight on gpt fails at launch. Use a Cursor-native model until it recovers.

## PROCESS IMPROVEMENTS

- When a printer change would make `split()[0]` a grain token, schedule walker retarget in the first plan unit — do not wait for preflight to discover it.
- Do not leave implementation unstaged across a preflight or QA spawn.

## TECHNICAL IMPROVEMENTS

QA advisories left as follow-ups: dedicated `zoom_reaches` wake-grammar unit test; prompt Other-commands still labels pack prefixes `<hash>`; monkeypatch test duplicates tree helpers that `gitutil` already has.

## NEXT STEPS

- [PR #37](https://github.com/Texarkanine/SumMem/pull/37) on `labelling` is open (not draft). This archive commit should land on that branch so the PR drops `memory-bank/active/`.
- Push `labelling` (ahead of origin by the archive commits).
