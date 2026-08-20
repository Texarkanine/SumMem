---
task_id: tree-schema
complexity_level: 2
date: 2026-08-19
status: completed
---

# TASK ARCHIVE: tree-schema

## SUMMARY

Clean-cut `.tree` JSON: `{c:[{type:"note"|"nap", …}]}`, no `v`, unknown fields ignored, old `kids`/`k` blobs do not load. Wake lines dropped the date: notes print caption only; packs print `xN <prefix>: caption`. Closes [issue #4](https://github.com/Texarkanine/SumMem/issues/4) plus the undated-wake add-on. XML was considered and declined (`type` is a JSON discriminator).

## REQUIREMENTS

- No `v` on write; no `Tree.v`; ignore unknown JSON fields.
- Array key `c`; Python stays `Tree.kids`; do not accept `kids`.
- Discriminator `type` is `note` or `nap`; missing or unsupported `type` is an error.
- Keep `name`/`text` and `id`/`sum`/`tree`.
- Wake: note is caption; pack (`leaves > 1`) is `xN <prefix>: caption`; no `YYYY-MM-DD`.
- Update `VISION.md`; rewrite byte-lock tests; zoom/nap/zipper behavior unchanged aside from payload identity.

## IMPLEMENTATION

`.summem/summem`: `_tree_dict` / `_tree_from_dict` emit and read `c`/`type`; `ValueError` on missing or unknown `type` (no `else` → nap). `format_wake_line` dropped `_day_from_stamp` (helper kept for catalog `store_stats`). `VISION.md` and `memory-bank/systemPatterns.md` updated.

## TESTING

pytest (`uv run --python 3.11 --with pytest pytest`): 177 passed. `/niko-qa` failed once (`systemPatterns.md` wait-free sentence still named a date), then passed after that one-line fix. Four advisories: old `.summem/naps/*.tree` in this repo, `zoom` traceback on parse failure, empty grain-1 caption line, loose `(KeyError, ValueError)` on kids-without-c.

## LESSONS LEARNED

Pack lines used to start with a date, so tests looked for `" xN "` with a leading space. After the date dropped, that substring is gone even though grain remains. Proof tests hid the same lock. A briefing file that restates a contract twice (wake heading + wait-free paragraph) must be edited in both places.

## PROCESS IMPROVEMENTS

When rewriting a printed line format, grep the whole `tests/` tree for the old shape (`YYYY-MM-DD`, `" xN "`, `endswith(": …")`), not only the files named in the plan.

## TECHNICAL IMPROVEMENTS

`zoom` still raises a traceback on an unparseable `.tree` (pre-existing). A grain-1 pack with no caption now prints an empty line. Neither was in scope.

## NEXT STEPS

Regenerate or remove this repo’s own `.summem/naps` before dogfooding `zoom` (clean-cut; old trees will not load). None otherwise. Pack-size cap, zipper behavior, and a real v2 stay out of this task.
