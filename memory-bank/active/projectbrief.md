# Project Brief

## User Story

As an agent folding two packs, I want the nap directive to quote only the two captions so that grain and content ids do not compete with the text I am supposed to compress.

## Use-Case(s)

### Use-Case 1

The view is over budget and the oldest equal-grain pair is two packs. `fold_request` prints the usual Compress / Keep / Run block. Each quoted source line is the pack's caption. The `Run:` line still carries the two unique prefixes.

### Use-Case 2

The oldest equal-grain pair is two notes. The quoted lines stay wake-shaped (`x1 YYYY-MM-DD: text`). Wake listings are unchanged for both notes and packs.

## Requirements

1. When `fold_request` quotes two packs, each source line is the caption only: no `xN` grain and no content-id hash.
2. The `Run:` line still names both packs by unique prefix (and `--path` when walk-up would miss the store).
3. `format_wake_line` / `wake_text` keep `xN <prefix>: caption` for packs.
4. Leaf-pair fold lines stay dated wake lines.

## Constraints

1. Do not change OptMem.
2. Do not put ACK or idle inside `fold_request`.
3. Do not strip grain or hash from wake, recall, or zoom listings.
4. Empty captions stay empty text, not a reconstructed `xN <prefix>:` line, in the fold quote.

## Acceptance Criteria

1. A fold prompt for two packs with captions `e & f` and `g & h` contains those captions and does not contain `x2 ` or the packs' prefixes on the quoted lines.
2. That same prompt's `Run:` line still includes both prefixes.
3. A fold prompt for two notes still quotes `x1 YYYY-MM-DD: …` lines.
4. Wake of the same packs still prints `xN <prefix>: caption`.
