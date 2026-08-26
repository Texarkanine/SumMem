# Progress

Shorten stored nap leaf-set ids to 16 hex; grow `migrate.py` so one pass rewrites four-part and five-part-64 pairs (including nested `.tree` ids) to five-part-16; rewrite this clone's root and dogfood stores; update atlas and systemPatterns. Spec: [SumMem #67](https://github.com/Texarkanine/SumMem/issues/67).

**Complexity:** Level 3

## 2026-08-26 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Intent restated from #67; operator confirmed, including breaking change and post-reflect non-draft PR with a copyable `BREAKING CHANGE:` footer.
    - Classified Level 3: multiple components (driver, migrate, stores, docs), not a new architecture.
* Decisions made
    - Level 3, not Level 2: dual-source migrate plus nested-id rewrite is the same class as #61, not a suffix rename.
    - Level 3, not Level 4: on-disk width change inside the existing file backend; no milestone decomposition.
* Insights
    - Filename-only truncate is rejected in the issue because `resolve_id` would see a 16-hex view id that is a prefix of a 64-hex nested id.
