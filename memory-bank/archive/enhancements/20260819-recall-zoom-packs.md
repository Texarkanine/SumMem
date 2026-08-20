---
task_id: recall-zoom-packs
complexity_level: 2
date: 2026-08-19
status: completed
---

# TASK ARCHIVE: recall-zoom-packs

## SUMMARY

`recall` matches nested nap captions (`NapChild.sum`) that have left the view, in the same children-file walk that already searches original notes. Zoom and recall print one agent-safe stderr line (`skipped a pack`) when they skip an unreadable sibling children file, and still succeed if another pack answered. Wake stays silent. Closes [#8](https://github.com/Texarkanine/SumMem/issues/8) and [#7](https://github.com/Texarkanine/SumMem/issues/7).

## REQUIREMENTS

- Nested captions as well as view captions and original note sentences.
- No store paths or git in recall output.
- One stderr line on sibling skip; do not fail if another pack answered.
- Asked-for unreadable zoom still `unreadable pack`.
- Do not change wake, note/nap identity, or `_note_children`.

## IMPLEMENTATION

`summem`: `_recall_nested` walks notes (`{cid}  text`) and nested naps (`{id}  caption`); `_note_children` left note-only for `_nap_stem`. `_warn_skipped_pack` writes `skipped a pack\n` on `recall_text` and `zoom_text`'s sibling `continue` only. Atlas § Zoom and recall updated. Persistent briefing files unchanged.

## TESTING

pytest (`uv run --python 3.11 --with pytest pytest`): 211 passed (4 new). Preflight PASS WITH ADVISORY (gpt-5.6; walker consolidation deferred). `/niko-qa` PASS (gemini-3.1-pro).

## LESSONS LEARNED

`_note_children` is a rematerialize/leftmost-leaf walker, not a search API. An omit-paths assertion on empty stdout is not a red; require the hit first.

## PROCESS IMPROVEMENTS

When a test asserts the absence of habitat words, also assert the behavior that produces output. Empty success is a vacuous pass.

## TECHNICAL IMPROVEMENTS

Preflight advisory: one typed depth-first walk of a children file could feed recall, zoom find, and `named_ids`. Out of this task's scope. `named_ids` still skips unreadable trees silently.

## NEXT STEPS

None. Do not expand into sqlite, hooks, or `cover(T)`.
