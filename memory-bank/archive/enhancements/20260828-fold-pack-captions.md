---
task_id: fold-pack-captions
complexity_level: 2
date: 2026-08-28
status: completed
---

# TASK ARCHIVE: fold-pack-captions

## SUMMARY

When `fold_request` quotes two packs (grain > 1), each source line is the caption only. Grain and content-id stay on wake listings and on the `Run:` line. Leaf-pair quotes remain dated wake lines. Merged as [PR #72](https://github.com/Texarkanine/SumMem/pull/72). QA passed. py311: 369 passed, 1 skipped.

## REQUIREMENTS

From the project brief:

- When `fold_request` quotes two packs, each source line is the caption only: no `xN` grain and no content-id hash.
- The `Run:` line still names both packs by unique prefix (and `--path` when walk-up would miss the store).
- `format_wake_line` / `wake_text` keep `xN <prefix>: caption` for packs.
- Leaf-pair fold lines stay dated wake lines.
- Do not change OptMem. Do not put ACK or idle inside `fold_request`. Do not strip grain or hash from wake, recall, or zoom listings.
- Empty captions stay empty text, not a reconstructed `xN <prefix>:` line, in the fold quote.

## IMPLEMENTATION

In `fold_request` (`summem`), each quoted source line uses `node.caption` when `node.kind != "note" and node.leaves > 1`; otherwise it keeps `format_wake_line`. `format_wake_line`, `wake_text`, `short_id`, and the `Run:` line are unchanged. `note`, `nap`, and `surgery.py` print `fold_request` verbatim and needed no edits.

Prose: `docs/architecture/index.md` now distinguishes fold pack quotes from wake/recall/zoom formatting. `memory-bank/systemPatterns.md` notes that `fold_request` quotes pack captions without grain or prefix (ids live on `Run:`).

## TESTING

TDD in `tests/test_fold.py`. Added `test_fold_request_pack_pair_quotes_captions_only` and `test_fold_request_empty_pack_caption_is_blank_quote`. Existing `test_fold_request_mentions_remaining` still pins dated leaf-pair lines. Pack-pair wake assertion pins `WAKE_LINES` at 2 so the listing stays packed (default budget expands under-budget packs). Preflight: PASS WITH ADVISORY. `/niko-qa`: PASS. py311: 369 passed, 1 skipped.

## LESSONS LEARNED

- Wake listings orient; fold quotes are the writing task. If that split had been the original contract, `fold_request` would never have called `format_wake_line` for grain>1 packs.
- `wake_text` expands packs when the view is under `WAKE_LINES`. A test that wants packed wake lines must pin the budget at or over the view size.
- Two local quote selections are the design; a shared `_fold_quote_line` helper still waits for a second caller.

## PROCESS IMPROVEMENTS

No process change. Preflight advisories (explicit `monkeypatch.chdir`, optional helper) were noted but did not alter the plan.

## TECHNICAL IMPROVEMENTS

Extract `_fold_quote_line(node, ids)` if a second surface (batch fold, surgery) needs the same caption-only quoting rule. Keep the two ternaries until then.

## NEXT STEPS

None. Shipped via PR #72.
