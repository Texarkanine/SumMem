# Progress

Omit catalog how-to from root wake when no nested stores exist. Leave operator help unchanged. Keep catalog teaching when catalogs are present.

**Complexity:** Level 1

## 2026-09-03 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Restated and confirmed intent: wake-only; empty catalog means no catalog text; help still documents catalogs.
    - Classified Level 1: single-component correction of misleading/wasteful agent output.
* Decisions made
    - Level 1 (quick bug fix). Q1 yes (misleading CLI/agent output is a fix); Q1a yes (root-wake Usage only).
    - Task id: `wake-omit-empty-catalog`.
* Insights
    - `catalog_text()` already returns empty when there are no other stores. The leftover is the Usage paragraph that always teaches catalogs and `wake --path`.

## 2026-09-03 - BUILD - COMPLETE

* Work completed
    - Split catalog how-to behind `how_to_text(*, catalog=False)`. Root wake passes `catalog=bool(cat)`.
    - Tests: empty root wake has no catalog/`wake --path`; cataloged wake still teaches pull; operator help unchanged.
    - `tox -e py311`: 373 passed, 1 skipped.
* Decisions made
    - Keyword-only `catalog` on `how_to_text` rather than a second helper.
    - Dropped “Ignore `--path` if the root wake had no catalog”: it is dead once the paragraph is catalog-conditional.
* Insights
    - Empty-catalog omission is a wake-assembly choice. `how_to_text()` default is the empty-catalog Usage; operator `usage_text()` still documents `--path`.
