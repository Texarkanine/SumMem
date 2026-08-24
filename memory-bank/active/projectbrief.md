# Project Brief

## User Story

As an agent reading `wake`, I want each leaf to print as its own dated row so I can tell notes apart and see when they were recorded, without burning date characters in the sentence and without a single day stamped on a nap that may span months.

## Use-Case(s)

### Wake lists recent leaves

The agent runs `wake` and sees each loose note as `x1 (YYYY-MM-DD): text`. The day comes from the note’s filename stamp (UTC). Stacked leaves read as separate memories, not one paragraph.

### Wake lists naps

A pack still prints `xN <prefix>: caption` with no date. Grain and hash stay the zoom signal. A large pack is not dated with its leftmost child.

### Fold prompt shows the same leaf shape

When `fold_request` quotes two leaf view nodes, those lines use the same `format_wake_line` as wake. The day sits in parentheses before the colon, not in the caption slot, so it is less likely to be copied into `note` or a nap caption.

## Requirements

1. A leaf wake line is `x1 (YYYY-MM-DD): <text>`.
2. The day is the UTC calendar date of the note’s existing filename stamp, assigned by the script. It is not taken from note prose and not from the host’s local date.
3. Nap lines (`leaves > 1`) stay `xN <prefix>: caption` (or `xN <prefix>:` with no caption). No date on packs.
4. The date is not written after the colon as if it were part of the note.
5. `format_wake_line` is the one printer: wake, under-budget expand, and `fold_request` all show the new leaf shape.
6. Store files, hashes, and nap identity do not change. This is a print contract.
7. Agent prompt and briefing docs name the new leaf line and keep `x<N> <hash>:` as the zoomable nap signal.

## Constraints

1. Do not date nap lines. A single day on an `x1024` would lie about span.
2. Do not restore positional `#a-b` ids.
3. Do not put the date in the caption/body slot (`x1: YYYY-MM-DD - text` is out).
4. Do not write the date into stored note bytes.
5. Grain-1 packs keep today’s print behavior (caption only). Date only `kind == "note"`.
6. CLI output still does not mention store files, hashes as paths, or git.

## Acceptance Criteria

1. A note written at `2026-08-24T12:30:05Z` wakes as `x1 (2026-08-24): <text>`, and `<text>` is exactly the stored sentence.
2. Two notes print as two prefixed lines, not two bare sentences.
3. A pack wake line has no `YYYY-MM-DD` and still matches `xN <prefix>: caption`.
4. `zoom` still accepts the unique prefix of a pack; `x1 (YYYY-MM-DD)` is not treated as a pack id.
5. Existing proofs still hold under the new line format.
6. `systemPatterns.md`, `docs/architecture/index.md`, and the baked prompt (`prompt_text` / `docs/agents-prompt.md`) describe dated leaves and undated packs.

## Rework

Operator after reflect: parentheses optimize for human eyes. Optimize for agents. Drop them.

Leaf line is `x1 YYYY-MM-DD: text` — the same `xN TOKEN: body` grammar as a pack. TOKEN is a day on a leaf and a hash prefix on a nap. The colon still keeps the day out of the stored sentence. Do not put the date after the colon. Do not date packs.

Acceptance: a note at `2026-08-24T12:30:05Z` wakes as `x1 2026-08-24: <text>`. Prompt and briefing name `x1 YYYY-MM-DD:`, not parenthetical days.
