---
task_id: note-ack-surgery
complexity_level: 4
date: 2026-08-21
status: completed
---

# TASK ARCHIVE: note-ack-surgery

## SUMMARY

Parent-operated L4: two parallel niko-in-worktree agents closed [#27](https://github.com/Texarkanine/SumMem/issues/27) and [#28](https://github.com/Texarkanine/SumMem/issues/28). Merged [PR #29](https://github.com/Texarkanine/SumMem/pull/29) prints `Saved.` after a successful `note` and coaches that a nap means the note is already stored. Merged [PR #30](https://github.com/Texarkanine/SumMem/pull/30) adds emergency-only repo-root `surgery.py` that zipper-excises one raw note from HEAD. Parent did not implement product code.

## REQUIREMENTS

- `#27` as written: ACK before any fold request; reword the baked prompt so a nap cannot be read as a failed `note`; do not delay the write.
- `#28` as rewritten: separate `surgery.py`, not a shipped CLI; zipper break-out, unlink one note, `heal_view`; HEAD must not still embed the sentence; no git history rewrite; no invented nap captions.
- Primary surgery case: sensitive content at tip, then operator history rewrite. Secondary: duplicates / misformatted lines.
- After excision, surgery may print the first fold request so an agent can start the nap cascade (`wake` does not demand a nap).
- Parent: isolated builders, OptMem allowed for direct reports, standing consent through archive + draft PR. Parent L4 files stay off workers' base.

## MILESTONE LIST

Original list; none added, removed, or reordered.

1. Print a recorded ACK on `note` before any fold request and reword the baked prompt so a nap cannot be read as a failed note (#27) — estimated L2, classified L2
2. Add emergency-only repo-root `surgery.py` that zipper-excises one raw note from HEAD without shipping delete on the summem CLI (#28) — estimated L3, classified L2

Both ran in parallel. Parent preflight of this list was PASS WITH ADVISORY; each worker preflighted its own plan.

## SUB-RUN SUMMARIES

### note-ack (L2, PR #29)

Successful `note` writes first, then prints `Saved.`, then maybe `fold_request`. ACK is on `main`'s `note` branch, not inside `fold_request` (`nap` shares that helper). Not a `notes/` path or a content-id prefix. Silent-stdout tests were the bug encoding and were retargeted. `tox` 238 passed py311–py314. First builder died `resource_exhausted` after preflight; resume from BUILD finished it. QA PASS.

Review follow-up: dropped "do not retry" from `prompt_text()` / `docs/agents-prompt.md` / `AGENTS.md` / README so a real failed `note` can be tried again. Kept "the note is already stored."

Leftover: ACK is still after the store lock; a heal hang after write can look silent.

### surgery (L2, PR #30)

Repo-root `surgery.py` loads sibling `summem` via `SourceFileLoader`. Locate by `--contains` (note text only) or filename/seq; `--dry-run` prints the rematerialize chain and writes nothing. Split every containing view nap, unlink that one loose note, then `heal_view`. No `write_nap`. Operator docs at `docs/surgery.md`. Did not edit `summem`. `tox` 252 then 260 passed py311–py314 after review follow-ups. QA PASS.

Review follow-ups: `surgery.py version` prints `__version__` in lockstep with `summem` (Release Please extra-files; not enforced at runtime). After a real excision, stdout includes the first `fold_request` so an agent can start the nap cascade; `--dry-run` omits it.

Lessons: `heal_view` while the target is still under a larger overlapping pack subset-drops the loose note and leaves the sentence in a `.tree` — split every containing nap first. Dry-run and mutate are two `list_view` walks; keep them aligned.

## IMPLEMENTATION

Parent stayed on `niko/note-ack-surgery` and did not implement product code. Workers: `cursor-grok-4.6-xhigh` (Other Models quota blocked mix-family preflight/QA). Issue #28 was rewritten on GitHub before the surgery builder started so `surgery.py` could not be read as a shipped command. File ownership held: #27 owned `note` stdout and the prompt lockstep; #28 owned `surgery.py` and its docs. Worker worktrees were removed after merge so `feat/note-ack` and `feat/surgery` could be checked out in this clone.

## TESTING

Each sub-run: TDD, full `tox` py311–py314, Niko preflight + QA. Parent did not re-run the suite. Capstone is documentary.

## SYSTEM STATE

On `main` after #29 and #30: `summem note` prints `Saved.` then maybe a fold request; the baked prompt says a nap after `note` means the line is already stored. `surgery.py` exists at repo root, is not a `summem` subcommand, prints the same version string as `summem`, and after a real excision may print the first nap pair. Living docs remain README + `docs/architecture/` + `docs/notes.md` + `docs/surgery.md` + persistent memory-bank. Sub-run archives: `memory-bank/archive/bug-fixes/20260821-note-ack.md` and `memory-bank/archive/features/20260821-surgery.md`.

## CROSS-RUN INSIGHTS

Other Models quota was still exhausted; both builders fell back to Grok for preflight/QA. Parent L4 files stayed off `origin/main` so workers classified as standalone. Parallel file ownership (`summem` vs `surgery.py`) avoided a merge collision. `wake` still never asks for a nap — that is why surgery had to print `fold_request` itself.

## LESSONS LEARNED

- Empty `note` stdout is the #27 bug; this session observed it and did not retry.
- "Do not retry" in the prompt would also block retrying a real failure. Reassure that the note is stored; do not ban retry.
- A parent L4 that only orchestrates should not merge its `milestones.md` history onto `main`. Land the capstone archive as its own commit.
- `resource_exhausted` after preflight is a resume-from-BUILD, not a re-plan.

## PROCESS IMPROVEMENTS

Rewrite the GitHub issue before spawning when the operator override would otherwise be missed (`surgery.py` vs shipped delete). Standing consent through archive+PR still keeps workers from stopping at `/niko-build`. Mix-family preflight is dead while Other Models quota is exhausted — say so in the spawn prompt.

## TECHNICAL IMPROVEMENTS

ACK inside `note_locked` immediately after `write_note` if a heal hang should not look like a failed note. Optional later fold-in of `surgery.py` into the shipped CLI. `surgery.py` is still outside `tox -e coverage --cov=summem`.

## NEXT STEPS

- Leftover: ACK after lock; dual `list_view` walks in surgery dry-run vs mutate; leftover old worktrees (ops/recall/tox/noting-ratchet/versioning).
- Secrets from earlier waves: helper-bot app id/key, `CODECOV_TOKEN`.
