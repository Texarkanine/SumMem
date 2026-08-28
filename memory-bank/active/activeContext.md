# Active Context

## Current Task: fold-pack-captions
**Phase:** QA - COMPLETE (PASS)

## What Was Done
- `fold_request` quotes `node.caption` when kind is nap and grain > 1; `format_wake_line` unchanged
- Tests: `test_fold_request_pack_pair_quotes_captions_only`, `test_fold_request_empty_pack_caption_is_blank_quote`
- Atlas and systemPatterns: fold pack quotes are captions; ids on `Run:`
- py311: 369 passed, 1 skipped

## Next Step
- Reflection

## Files modified
- `/Users/tex/git/SumMem/summem`
- `/Users/tex/git/SumMem/tests/test_fold.py`
- `/Users/tex/git/SumMem/docs/architecture/index.md`
- `/Users/tex/git/SumMem/memory-bank/systemPatterns.md`

## Decisions
- Inline the quote condition twice in `fold_request`; no new public helper
- Pack-pair wake assertion sets `WAKE_LINES` to 2 so `wake_text` does not expand the packs

## Deviations
- The pack-pair test needed `monkeypatch.setattr(m, "WAKE_LINES", 2)` for the `wake_text` assertion; under default 32, `expand_frontier` rematerializes the packs into notes
