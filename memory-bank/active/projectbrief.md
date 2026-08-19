# Project Brief

## User Story

As an agent using SumMem, I want `.tree` JSON and `wake` lines to be short and unambiguous so that identity bytes are not padded with unused versioning, kind letters do not collide with `kids`, and the listing is not dated on every row.

## Use-Case(s)

### Use-Case 1

An agent runs `wake` and copies pack lines of the form `xN <prefix>: caption` (notes: caption only). No `YYYY-MM-DD`.

### Use-Case 2

`nap` writes a `.tree` whose canonical JSON is `{c:[…]}` with children `{type:"note", name, text}` or `{type:"nap", id, sum, tree}`. Nested trees use the same shape. Unknown fields are ignored. Old `kids`/`k`/`v` blobs fail (missing `c` or `type`).

## Requirements

1. Drop schema versioning: no `v` on write; no `Tree.v`; unknown fields ignored on read (stdlib JSON, not XML).
2. Tree array key is `c`. Python stays `Tree.kids`. Clean cut: do not accept `kids`.
3. Discriminator is `type` with values `"note"` and `"nap"`. Drop `k`/`n`/`p`.
4. Note payload keys stay `name` and `text`. Nap payload keys stay `id`, `sum`, `tree`.
5. Wake note line is the caption only. Wake pack line (`leaves > 1`) is `xN <prefix>: caption` (`xN` omitted is existing grain-1 behavior). No date prefix.
6. Update `VISION.md` schema and wake-line contract. Rewrite byte-lock tests. Zoom/nap/zipper behavior unchanged aside from payload identity.

## Constraints

1. No dual-read of old keys. Pre-v0; existing on-disk trees are not a compatibility surface.
2. Do not rename `name`, `text`, or `sum`. Do not introduce protobuf/Avro/XML.
3. Out of scope: pack-size cap, zipper behavior, a real v2, renaming `k` as a separate issue.

## Acceptance Criteria

1. Golden `dumps_tree` bytes in `tests/test_codec.py` have `c` and `type`, and no `"v"`, `"kids"`, or `"k"`.
2. `loads_tree` round-trips the new dump. Extra unknown fields on a valid tree do not fail.
3. A blob that only has `"kids"`/`"v"` does not load as a tree.
4. Nested nap children omit `v` and use `c`/`type`.
5. `wake` note lines have no date; pack lines match `xN <prefix>: caption`. Fold prompts inherit that (they call `format_wake_line`).
6. Zoom, nap, and zipper proofs still pass after byte-lock rewrites.
