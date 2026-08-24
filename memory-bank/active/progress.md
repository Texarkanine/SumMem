# Progress

Unify agent-facing recall/zoom lines with wake’s grammar, make recall match sentences not formatted lines, and reword Register Memories so clone-portability cannot be read as eternal currency.

**Complexity:** Level 2

## 2026-08-24 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Intent restated and approved; operator added that wake short hashes are the convention and zoom’s long hashes need a reason.
    - Classified Level 2 (Q1 fix → multiple components → L2). Not L3: no new addressing scheme; `short_id` already lengthens only until unique.
* Decisions made
    - Agent stdout never prefers 64-hex. Nested packs keep `xN <prefix>:` as the zoom handle. Nested leaves are dated with no hash.
    - Do not surgery the parenthesized note; fix the prompt that caused the misreading.
* Insights
    - Wake-listing already moved agent ids to unique prefixes; zoom/nested recall were left on the old `{64hex}  text` printer.
    - LlamaPReview’s “note must remain true after clone” reading is a prompt defect, not a store defect.
