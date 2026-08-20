# Milestones: open-issue-wave

```mermaid
graph TD
    M1["Product: #8 then #7"]
    M2["Infra: #6 then #9"]
```

## Cross-milestone invariants

- Start from `185c686`. Do not recreate `VISION.md` or `ROADMAP.md`. Living docs are README, `docs/architecture/index.md`, `docs/notes.md`, and persistent memory-bank.
- Note/nap identity, wait-free wake, and the agent-facing CLI (no store paths, hashes-as-paths, or git) stay put.
- Python floor remains 3.11. `ensure_store` does not place the driver.
- Product owns `summem` recall/zoom. Infra owns the test runner. Neither rewrites the other's files.
- Archive before the draft PR so `memory-bank/active/` is not in the merge.

## Execution Order

Either milestone may run first. They may run in parallel.

- [x] Search nested nap captions in recall, then warn on unreadable sibling packs in zoom/recall (#8 then #7)
- [x] Tox matrix 3.11–current non-EOL plus a reliable pytest command; off-the-shelf cache only if solid (#6 then #9)
