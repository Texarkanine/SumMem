---
task_id: open-issue-wave
complexity_level: 4
date: 2026-08-19
status: completed
---

# TASK ARCHIVE: open-issue-wave

## SUMMARY

Parent-operated L4: two parallel niko-in-worktree agents closed the four open issues after docs-sunset #11. Product [PR #12](https://github.com/Texarkanine/SumMem/pull/12) (merged) searches nested nap captions and warns on skipped sibling packs. Infra [PR #13](https://github.com/Texarkanine/SumMem/pull/13) (merged) makes `tox` the suite command for CPython 3.11–3.14. Worker SumMem notes were left untracked, then committed and pushed; both note sets landed on `main`.

## REQUIREMENTS

- Sequence `#8` then `#7`, and `#6` then `#9`. Parallelism allowed across those pairs.
- Each worker: `/niko` + `/worktree`, OptMem (`memo`), draft PR after reflect, archive so `memory-bank/active/` is not in the merge.
- Start from `185c686`. Do not recreate `VISION.md` / `ROADMAP.md`.
- Python floor 3.11 through current non-EOL (not 3.10). Cache only if off-the-shelf and proven.
- Product owns `summem` recall/zoom. Infra owns the test runner.
- Parent decides forks; workers do not bounce.

## MILESTONE LIST

Original list; none added, removed, or reordered.

1. Search nested nap captions in recall, then warn on unreadable sibling packs in zoom/recall (#8 then #7) — estimated L2, classified L2
2. Tox matrix 3.11–current non-EOL plus a reliable pytest command; off-the-shelf cache only if solid (#6 then #9) — estimated L2, classified L2

Both ran in parallel. Parent L4 preflight of this list was skipped; each worker preflighted its own work.

## SUB-RUN SUMMARIES

### recall-zoom-packs (L2, PR #12)

`recall` matches nested `NapChild.sum` captions that have left the view, in the same children-file walk that already searches original notes. Zoom and recall print `skipped a pack` on stderr when they skip an unreadable sibling children file, and still succeed if another pack answered. Wake stays silent. Asked-for unreadable zoom is still `unreadable pack`. Atlas § Zoom and recall updated. 211 pytest. Preflight PASS WITH ADVISORY (walker consolidation deferred). QA PASS.

`_note_children` is a rematerialize/leftmost-leaf walker, not a search API. `named_ids` still skips unreadable trees silently.

### tox-pytest-runner (L2, PR #13)

`tox` is the one documented pytest command. `tox.ini` declares `py311`–`py314`, `package = skip`, `skip_missing_interpreters = true`. No `pyproject.toml`. No test-result cache (testmon not proven on this `tmp_path` / worktree / `SourceFileLoader` suite). README Developing and `techContext` Testing Process name `tox`. Four contract tests. 211 pytest on 3.11.11, 3.12.11, 3.13.7, and this machine’s 3.14.0rc3. Preflight PASS. QA PASS.

`{posargs}` needs `ConfigParser(interpolation=None)`. Do not subprocess tox from pytest.

## IMPLEMENTATION

Parent stayed on `niko/open-issue-wave` in an ops worktree and did not implement product code. Workers used `cursor-grok-4.6-xhigh-fast`, other-family preflight/QA, and standing consent through archive + draft PR. Product branch `feat/recall-zoom-packs`; infra `feat/tox-pytest-runner`. Notes the workers wrote were not in the first PR tips; they were committed later (`b788971`, `80e6dc1`) and merged with the PRs.

## TESTING

Each sub-run: TDD, full pytest, Niko preflight + QA. Parent did not re-run the suite. Capstone is documentary.

## SYSTEM STATE

After both merges: recall sees nested captions; zoom/recall warn on skipped sibling packs; `tox` is the documented runner for 3.11–3.14; living docs remain README + `docs/architecture/` + `docs/notes.md` + persistent memory-bank. Two disjoint SumMem note sets from the workers are on `main`. Neither worker napped.

## CROSS-RUN INSIGHTS

Agents ran `summem note` and left the files untracked. The baked prompt says notes are “acceptable in git forever” and “the tool manages them”; techContext still says generated store data is ignored. That is [issue #14](https://github.com/Texarkanine/SumMem/issues/14). Parallel worktrees did not collide on `summem` vs `tox.ini`. Parent L4 files lived only on the ops branch so workers would not see `milestones.md` and try to run the parent L4.

## LESSONS LEARNED

- “The tool manages them” reads as “do not `git add`.” Publish is the agent’s job; the script only writes the file.
- Instruct workers to archive before the PR, or two `memory-bank/active/` trees will conflict.
- A parent L4 that only orchestrates should not commit `milestones.md` to `main` before the children start.

## PROCESS IMPROVEMENTS

Put “`git add` the files `note`/`nap` just wrote” in `prompt_text()` (#14). Standing consent through archive+PR kept workers from stopping at `/niko-build`.

## TECHNICAL IMPROVEMENTS

Shared children-file walker (preflight advisory on #12). `named_ids` silent skip. No CI, so `skip_missing_interpreters = true` can hide a missing Python.

## NEXT STEPS

- [Issue #14](https://github.com/Texarkanine/SumMem/issues/14): prompt tells agents to commit store files.
- Leftovers not in this wave: `named_ids` silent skip; walker consolidation; CI for the tox matrix.
