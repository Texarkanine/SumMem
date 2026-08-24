# Project Brief

## User Story

As an agent, I want every SumMem listing (wake, recall, zoom) to use one compact, predictable line grammar, and I want the baked prompt to say that a note is true at write time and clone-portable, so I am not taught eternal-currency or given hashes I cannot use.

## Use-Case(s)

### Wake, recall, and zoom agree

An agent wakes a store, recalls a sentence, and zooms a pack. Leaves are always `x1 YYYY-MM-DD: text`. Packs are always `xN <unique-prefix>: caption`. The prefix is the same `short_id` wake already prints. Nested packs inside a zoom keep that pack form (the hash is the zoom handle). Nested leaves do not get a hash.

### Recall searches remembered text

`recall b` matches note bodies and nap captions that contain `b`. It does not match hex in a pack prefix, grain markers, or the script-authored day on a leaf line.

### Prompt membership is clone-portability

An agent reading Register Memories does not infer that a stored note must remain true forever, or that a superseded sentence must be deleted. The test is: would this fact belong in a fresh clone on another machine (not personal, not machine-local).

## Requirements

1. One agent-facing grammar: leaves `x1 YYYY-MM-DD: text` from the filename stamp; packs `xN <unique-prefix>: caption` with no day. Wake already does this; recall and zoom must.
2. Zoom of a pack still shows hashes, but only for nested packs, not for leaves. A two-note nap zooms to two dated leaf lines. A nap-of-naps zooms to two pack lines.
3. Agent-facing output never prefers 64-hex. Prefixes are `short_id` (floor 8, grow until unique among `named_ids`). Full 64-hex stays on disk (nap names, `.tree` identity). The longest printed prefix is only what uniqueness requires.
4. Recall regexes the sentence: loose-note text and nap caption. Not the formatted line (not prefix, not `xN`, not the day).
5. Recall still *prints* the unified grammar after a hit.
6. One or two word changes to the Register Memories sentence so write-time truth plus clone-portability cannot be read as “every note must remain true forever.” Lockstep `prompt_text()`, `docs/agents-prompt.md`, and `AGENTS.md`.
7. Do not delete the parenthesized dated-leaf note. That sentence was true when written; the prompt was the misreading.

## Constraints

1. Follow-on on `labelling` / PR #37; do not reopen dated-leaf-wake’s wake/fold printer.
2. `nap` and `zoom` already accept unique prefixes via `resolve_id`. Do not add a second addressing scheme.
3. Prompt lockstep tests stay; do not name OptMem in the prompt.
4. CLI output still does not mention store files, hashes as paths, or git.
5. A leaf line is not a zoom target; pack prefixes remain zoom handles.

## Acceptance Criteria

1. `recall` of a loose note prints `x1 YYYY-MM-DD: text` and matches only the note text.
2. `recall` of a nested original note prints that same dated form, not `{64hex}  text`.
3. `recall` of a nested nap caption prints `xN <prefix>: caption`, and that prefix resolves in `zoom`.
4. `recall` of a hex character that appears only in a pack prefix, not in any sentence, prints nothing.
5. `zoom` of a two-note nap prints two dated leaf lines and no content ids.
6. `zoom` of a nap-of-naps prints two pack lines with unique prefixes, not 64-hex by default.
7. The baked prompt no longer supports the reading “stored notes must remain true at all times.” Clone-portability and write-time truth remain.
8. Existing wake and fold_request dated-leaf behavior is unchanged.
