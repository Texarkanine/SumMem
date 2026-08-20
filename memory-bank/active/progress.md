# Progress

Replace the bare `note is too long` rejection with an OptMem-style ratchet for `note` and `nap`, and apply the same rule to other CLI errors that only complain when a next step is known and not obvious.

**Complexity:** Level 2

## 2026-08-20 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Restated and confirmed intent for [SumMem#16](https://github.com/Texarkanine/SumMem/issues/16) plus a bounded pass over other CLI errors
    - Determined Level 2
* Decisions made
    - Note and nap length ratchets are must-ship; other errors are a secondary walk, not a rewrite of every string
    - Do not invent a next step when we do not know one
* Insights
    - `require_entry` already serves both `note` and `nap`; one message change covers the primary path
    - OptMem's crib is `Too long: %d bytes, limit %d. Accented characters cost 2 bytes. Compress it further.`
