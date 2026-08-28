# Progress

When `fold_request` quotes two packs, show captions only. Grain and hash stay on wake and on the `Run:` line.

**Complexity:** Level 2

## 2026-08-28 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Restated intent: pack-pair fold quotes are captions only; wake and `Run:` prefixes unchanged; leaf-pair quotes stay dated
    - Classified Level 2
* Decisions made
    - Enhancement, not a bug: wake formatting is correct; the fold prompt was reusing it
    - Self-contained: `fold_request` source lines for packs with grain > 1
* Insights
    - Grain-1 packs already print caption-only via `format_wake_line`; the noise is `xN <prefix>:` on larger packs

## 2026-08-28 - PLAN - COMPLETE

* Work completed
    - Test plan: pack-pair caption quotes plus missing-`.summ` blank quotes in `tests/test_fold.py`; keep leaf-pair dated lines
    - Implementation: `fold_request` quotes `node.caption` for naps with grain > 1; `format_wake_line` unchanged; atlas and systemPatterns surgical
* Decisions made
    - No new public helper; two quoted lines in `fold_request` are the whole executable change
    - Empty caption is a missing `.summ`, not `write_nap("")` (`require_entry` rejects empty)
* Insights
    - `note` / `nap` / surgery already print `fold_request` verbatim, so they inherit the new quotes with no extra printers
