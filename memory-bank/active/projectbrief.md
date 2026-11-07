# Project Brief: PR 99 Review Fixes

## User Story

As the operator of [PR #99](https://github.com/Texarkanine/SumMem/pull/99), I want the docs site's inaccuracies found in review fixed on branch `docsite`, without making the prose longer or less elegant than it is.

## Requirements

1. **Zipper example** (`docs/how-it-works/no-conflicts.md`): when two naps of the same grain overlap, heal opens the one whose file name sorts first. With these labels that is `ABCD1234`; the repair ends with `ABCDEFGH` beside `1234`. Redraw the last two diagrams and fix their sentences. State the same-size rule there and in the Overlap section of `docs/architecture/merges-and-healing.md`. ([review](https://github.com/Texarkanine/SumMem/pull/99#discussion_r4504023314))
2. **Nap pair rule** (`docs/user-guide/commands.md`): `nap` does not refuse every pair other than the requested one. Say what it accepts. ([review](https://github.com/Texarkanine/SumMem/pull/99#discussion_r4504023316))
3. **Test-first rule** (`docs/contributing/index.md`): remove the link to the agent rule file. Tech docs do not link to Cursor rules. Restate the rule briefly instead. ([review](https://github.com/Texarkanine/SumMem/pull/99#discussion_r4504023321))
4. **Unreadable children files** (`docs/architecture/zoom-and-recall.md`): zoom of a broken nap fails with `unreadable pack`. `skipped a pack` prints once per unreadable file passed while zoom searches inside naps or recall searches. ([review](https://github.com/Texarkanine/SumMem/pull/99#discussion_r4504023324))
5. **Surgery check** (`docs/advanced/surgery.md`): the final `recall` uses the same `--path`, escapes regex characters, and says what a remaining hit means. ([review](https://github.com/Texarkanine/SumMem/pull/99#discussion_r4504025804))

## Constraints

- Keep items 4 and 5 short. Plain language (ISO 24495, Orwell's six rules, ASD-STE100 in spirit). Fix inaccuracies without adding bulk.
- `properdocs build --strict` passes.

## Out of Scope

- README Pages links (dismissed in review).
- GitHub settings: `v*` tag policy on the `github-pages` environment; PR body text. Operator handles these.
- A `surgery.py` way to remove text held in a nap caption.
