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
