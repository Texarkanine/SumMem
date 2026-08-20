---
task_id: agents-prompt
complexity_level: 2
date: 2026-08-19
status: completed
---

# TASK ARCHIVE: agents-prompt

## SUMMARY

Shipped issue #2: a baked `summem init` prompt at the top of `AGENTS.md`, and a root wake that catalogs other stores without reading as a script. The branch also stopped `ensure_store` from copying the driver, labeled the catalog as `== Additional SumMem Catalogs ==` with `./path` lines, omitted `== Project-root Memories ==` when the root document is empty, and (from PR review) made `fold_request`'s `Run:` line use `.summem/summem` via `AGENT_BIN`. `VISION.md` and `ROADMAP.md` were left as directional leftovers (sunset next). Draft PR #10. pytest 207 on Python 3.11.

## REQUIREMENTS

- `summem init` prints a baked prompt plus a paste-at-top-of-`AGENTS.md` recipe. `init` does not write `AGENTS.md`.
- This repo's `AGENTS.md` starts with that prompt. `CLAUDE.md` stays `@AGENTS.md`.
- Wake once at session start; skip if a root wake is already in the conversation. Never “before any other tool call.”
- Notes are stranger-clone public facts. Personal, machine, and preference facts stay out.
- Agents invoke `.summem/summem`. `--path` aims at a store, not the driver.
- Presence of the driver is not activation; the `AGENTS.md` block is.
- `ensure_store` must not place the driver (rework). Operator places `.summem/summem`.
- Root wake: labeled catalog of `./path` lines, not `wake --path` command lines (post-reflect rework).
- Omit `== Project-root Memories ==` when the root decaying document is empty (L1 slice).
- Nap `Run:` line must be the same invoke path the prompt teaches (PR #10 LlamaPReview).

## IMPLEMENTATION

`prompt_text()` is the single prompt source. `init_text()` wraps the paste recipe. `AGENTS.md` lockstep-tested against `prompt_text()`. Catalog `usage_text` names `init` like other commands and still uses `CLI_NAME = "summem"`.

`ensure_store` creates `notes/`, `naps/`, and default config only. Struck `copy2` of `__file__`. This repo: repo-root `summem` is the record; `.summem/summem` and dogfood’s driver are symlinks.

Root `wake`: `== Additional SumMem Catalogs ==` then `./path` lines first; `== Project-root Memories ==` only when catalog and root document are both non-empty. Pull wakes omit the catalog. Config comment is settings/values; `knobs()` unchanged.

`AGENT_BIN = ".summem/summem"` feeds `prompt_text()` and `fold_request`'s `Run:` line. Help catalog stays `summem`.

## TESTING

Composer 2.5 (not fast) probes: root wake via `.summem/summem wake`; skip second root wake. Catalog-as-command over-pull was treated as a prompt miss until catalog lines became labeled paths.

pytest: 204 after first build, 205 after no-copy rework, 206 after catalog headers, 207 after empty-root header and again after `AGENT_BIN`. `/niko-qa` PASS on the L2 and on the empty-root L1 (operator filter: VISION/ROADMAP directional, not blocking). TDD red for this last fix: `Run: .summem/summem nap ` vs `Run: summem nap `.

## LESSONS LEARNED

- Store, driver, and activation are three objects. `ensure_store` copying `__file__` collapsed the first two and made “store exists” look like “an agent can run the script.”
- A substring invariant that forbids `.summem/summem` will fight the next policy correction. Encode the positive command.
- A catalog line that is only a shell command will be executed by a cheap agent. Label it and print paths. The pull recipe belongs in `AGENTS.md`.
- The empty-root memories header is a splitter, not a label for an empty section. `cat + doc + footer` already covers the empty-document case.
- `usage_text` is a static catalog; `fold_request`'s `Run:` is an imperative instruction. They must not share `CLI_NAME` once the prompt teaches a path that is not on PATH. Same cheap-agent lesson as the catalog.
- First-pass Composer probes do not count after the prompt is rewritten.

## PROCESS IMPROVEMENTS

L1 empty-root-header had no reflect/archive by design; folding it into this L2 archive was an operator request so the journey stays one document. VISION/ROADMAP lockstep burned QA cycles until the operator ruled them directional.

## TECHNICAL IMPROVEMENTS

`main()` wake still nests three branches where two suffice. Wake header capitalization still disagrees (operator-chosen). Nested-store driver symlinks were a preflight advisory, not built.

## NEXT STEPS

- Sunset `VISION.md` / `ROADMAP.md` in favor of README + memory-bank (operator-planned next task).
- Land or continue draft PR #10.
- Nested-store driver symlinks remain unbuilt (advisory, not promised).
