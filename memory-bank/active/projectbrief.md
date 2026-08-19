# Project Brief

## User Story

As an agent waking a SumMem store, I want at most `WAKE_LINES` short lines in context and an OptMem-style nap prompt when `note`/`nap` go over budget, so wake is a reading budget and hashes stay off the document.

## Use-Case(s)

### Bounded wake

Eleven loose notes, `WAKE_LINES = 4`. `wake` prints the newest four lines. It does not print a nap request. Older notes stay on disk.

### Raw note line

A one-note file prints `YYYY-MM-DD: text`. No hash. No `x1`. No `(1 note, from …)`.

### Pack line

A 16-leaf nap prints `YYYY-MM-DD x16 a3f2c1b8: caption`. Date, grain, unique prefix (8 hex, longer if needed), caption.

### Nap prompt on write

Twelfth `note` with budget 4 prints a terse prompt: the two child bodies, invent-nothing instruction, `Run: .summem/summem nap <prefix> <prefix> "<your line>"`. If more pairs remain, one extra sentence. `wake` is unchanged by that write except the new note exists.

### Prefix on nap and zoom

`nap a3f2c1b8 …` and `zoom a3f2c1b8` resolve the unique prefix. Two matches is an error. Filenames and `.tree` identity stay 64 hex.

## Requirements

1. `wake` prints at most `WAKE_LINES` lines. Never a nap request.
2. Under budget, keep expanding newest naps in memory until the cap. Over budget, print the newest `WAKE_LINES` view files and do not open `.tree`.
3. `note` and `nap` print the OptMem-style prompt when the directory is still over budget after the write. `fold_request` is that prompt, not two bare hashes.
4. Wake line: note `YYYY-MM-DD: text`; pack `YYYY-MM-DD xN <prefix>: caption`.
5. Prefix is 8 hex, or shortest unique longer prefix in this store. Ambiguous prefix is an error.
6. Full SHA-256 stays on disk and in leaf-set identity.

## Constraints

1. Do not truncate stored hashes.
2. Do not print positional ranges (`#0-3`).
3. Do not request naps from `wake`.
4. Out of slice: aligned `cover(T)`, other backends, prompt hook, filled `README.md`.
5. Over-budget wake with no naps is a recent window, not a full cover. Accepted.

## Acceptance Criteria

1. `WAKE_LINES = 4` and 11 notes: `wake` prints 4 lines, all `YYYY-MM-DD: …`, no hashes, no nap prompt.
2. Next `note` prints the instructional nap prompt with two unique prefixes and the two child texts. `wake` still prints 4 lines and no prompt.
3. After napping that pair, a pack line is `YYYY-MM-DD x2 <prefix>: caption`.
4. `zoom <prefix>` on a pack prints children; on a raw note, the note text (no-op payload).
5. Ambiguous prefix exits non-zero and writes nothing.
6. Proofs 1–8 still hold; their wake assertions match the new line format.
