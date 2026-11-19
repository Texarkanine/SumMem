# Creative: Store Flag Scheme

## Question

`note`, `nap`, `zoom`, `recall` and `surgery.py` require `--root` xor `--path` (#103). `--path` resolves against `$PWD`, but printed `Run:` lines are root-relative, so they fail from sibling directories. Which flag scheme closes that hole without forcing another breaking CLI change later?

## Users and context

- **Users:** coding agents, which copy commands from wake, Usage and `Run:` lines, often turns later and from another directory. Operators come second, mostly for `start` and `surgery.py`.
- **Constraint:** the driver is pasted into every consumer repository, so it needs few lines and few concepts (`productContext.md`).
- **Constraint:** the project is pre-1.0 (`0.x`), so a clean break is allowed (niko-core).

## Options

| Criterion | A: `--root` xor `--path` (shipped) | B: one `--path`, git `:/` magic | C: one `--path`, always root-relative | D: global `-C DIR` plus `--path` |
|---|---|---|---|---|
| Printed `Run:` works from any directory | No (the hole) | Yes: `--path :/pkg` | Yes | No |
| Relative input from where the agent stands | Yes | Yes | No | Yes |
| Concepts to teach | 2 flags, xor | 1 flag, 1 prefix | 1 flag, odd base | 2 flags, ordering rules |
| Prior art agents know | Partial | git pathspec `:/` | None | git `-C`, but it doesn't fix printing |
| Driver code | xor check + 2 branches | 1 prefix check in `resolve_parent` | Change the base | Most |

## Decision: B, one `--path` with git's `:/` root anchor

Rules (each one closes a specific hole):

1. **One flag.** `--path P` is the only store selector. `--root` is removed with no alias (clean break, pre-1.0).
2. **Anchors.** If `P` starts with `:/`, it is relative to the git root, and `:/` alone means the root. Any other value is relative to `$PWD`. Absolute paths are accepted. The walk up to the nearest started store is unchanged.
3. **Required where #103 requires a store flag:** `note`, `nap`, `zoom`, `recall`, `surgery.py`. On `wake`, the flag stays optional, and bare `wake` means `:/`.
4. **Every printed path is in `:/` form**, and every printed path is a valid `--path` value:
   - `Saved to :/packages/cli`
   - `Run: nap --path :/packages/cli …`
   - catalog lines `N: :/dogfood`
   - `start` output.

   Any printed path can then be pasted from any directory. This fixes the `Run:` hole, and output no longer mixes `./x` with `--path x`.
5. **The `:` namespace is reserved.** A leading `:` other than `:/` (for example `:(top)` or `:!x`) exits 2 with `unknown path prefix`. Git magic can be adopted later without a breaking change. A file whose name really starts with `:` is written as `./:name`, the same escape git uses.
6. **No paths outside the repository.** A `:/../x` path, or any path that resolves outside the git root, exits 2.
7. **One resolver.** `wake --path`, `start <dir>`, `surgery.py --path` and `migrate.py --path` all use the same resolver, so the rule holds for every path input.

Traded away: a separate visible `--root` word. `--path :/` replaces it at the same length. `:/` must be quoted in no common shell (bash, zsh, PowerShell, cmd).

## Bootstrapping prompt wording (operator question)

Agents copy examples more reliably than they follow rules. So the shortest way to teach `:/` is:

- Say the rule once, in the language of git, which agents already know.
- Use `:/` in every example.
- Print `:/` in every output.

Suggested Usage / AGENTS.md lines:

> Every store command takes `--path`: a path from where you stand, or `:/path` from the repository root, as in git. `:/` is the root store.
>
> `.summem/summem note --path <file> "…"` records in the nearest store for that file. `.summem/summem note --path :/ "…"` records in the root store.

The output then reinforces the rule: every `Saved to`, `Run:` and catalog line the agent sees is a `:/` path that can be pasted back. Per the operator's 2026-11-19 rule, the edits to the pasted prompts stay the operator's job. The spec names only the `how_to_text()` and `usage_text()` changes.

## Implementation notes

- `resolve_parent`: if `path_arg` starts with `:/`, set `origin = root / path_arg[2:]`. If it starts with `:`, refuse. Check containment with `relative_to(root)`.
- `_root_path` returns `:/rel` (root is `:/`). `_fold_store_flag` always returns `--path :/rel`.
- `_select_store` loses the xor check: a missing `--path` gives one line, `pass --path <file> (or :/ for the root store)`.
- The tests pinning `--root` and `./` output move to `:/` (TDD: tests first).
