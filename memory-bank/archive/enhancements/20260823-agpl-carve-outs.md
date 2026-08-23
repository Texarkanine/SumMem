---
task_id: agpl-carve-outs
complexity_level: 3
date: 2026-08-23
status: completed
---

# TASK ARCHIVE: agpl-carve-outs

## SUMMARY

Two carve-outs on an AGPL program, with [`summem`](../../../summem) as the only authoritative grant: §7 additional permissions for invocation, and 0BSD terms for the agent prompt template. [`LICENSE`](../../../LICENSE) stays verbatim AGPL. [`README.md`](../../../README.md) License section is a premise plus pointer at that header. [`surgery.py`](../../../surgery.py) stays stock AGPL (operator override; Niko had planned a subset echo). No REUSE, no `COPYING`, no SPDX `WITH`. Draft [PR #32](https://github.com/Texarkanine/SumMem/pull/32) on `licensing-2`. 262 pytest. QA PASS.

## REQUIREMENTS

- The program stays AGPL. Do not dual-license it.
- The agent prompt template (`prompt_text()` / `init` / `docs/agents-prompt.md`) is 0BSD. Pasting it into someone else’s `AGENTS.md` carries no copyright claim and no notice-retention duty.
- Invocation by an AI agent (developer-machine or customer-facing) is permitted even if a reviewer would call it conveyance or AGPL §13 network performance.
- Publishing a modified or forked SumMem still fires AGPL.
- A typical install copies only the script. That file must carry the whole grant. Repo-root files must not add a grant the script lacks.
- If REUSE were adopted: drop `LICENSE` for `COPYING`. REUSE was not adopted.
- TDD does not govern license or prompt prose. No change-detector tests on header wording.

## IMPLEMENTATION

### Legal instrument

Options considered: interpretation-only rider (Linux-syscall-note style); AGPL §7 additional permissions in the source; dual-license the program; SPDX `WITH LicenseRef-` exception.

Selected: §7 additional permissions. It is the license’s own way to grant “even if it is.” The file stays AGPL for scanners. Dual-license was forbidden. An unlisted SPDX exception would hide AGPL. A later conveyor may strip the additional permissions; they get AGPL without the carve-out, not a permissive program.

Prompt instrument changed after Creative: the draft was a part-of-program no-copyright claim. The operator chose 0BSD in the `summem` header — a separately licensed template, not a dual-license of the Program.

### Authority and echoes

Options considered: script-complete with no REUSE (verbatim `LICENSE`, README pointer); `COPYING` replaces `LICENSE` without REUSE; full REUSE.

Selected: script-complete, no REUSE. Rank 1 is a script-only install. Rank 2 is keeping `LICENSE` verbatim so GitHub / SCA still say AGPL. A `LICENSE` preamble can break detection. `COPYING` was tied to the unused REUSE branch.

Creative also planned an invocation-only echo on `surgery.py` (pre-mortem: someone copies that file alone). The operator rejected that third path after Reflect: vanilla stock AGPL, or an exact match of the `summem` header. Vanilla shipped. The grant lives only in `summem`.

### Live grant (operator-settled)

After the FSF short notice (AGPL-first; preflight’s capsule-before-notice advisory was not applied):

1. Invocation is not an intimate §1 link. The invoking program is not a covered work by reason of that invocation. “Your organization” is common control; “your personnel” are persons acting for it. Autonomous agents acting for the org are covered; they are not themselves “entities under common control.”
2. Invocation directed by you, your personnel, or an agent acting for your organization — including over a network — is not §13 remote interaction.
3. If a modified version is made available outside the organization (distribute, or offer remote interaction), paragraph 2 does not apply and §13 does. Paragraph 3 must not revoke paragraph 1.

Dropped from the Creative draft: literal “even if” / “not conveyance” sentences, “must retain” carve-outs, an unmodified-no-Corresponding-Source paragraph, and a network-only §13 trigger. The live cut is organizational: §13’s own “users / remotely / network” words would catch employees on a VPN.

`version` and the paste files were not edited.

## TESTING

No new tests (prose/policy). Existing `tests/test_init.py` lockstep and `tests/test_version.py` stayed as the accidental-edit net. `uvx --with tox tox`: 262 passed on py311–py314. `/niko-preflight` PASS WITH ADVISORY (capsule-first; `init` rejects substring “paste”). `/niko-qa` PASS. Advisories: Creative-vs-live wording (do not reopen); README restates two header conclusions (caller is not a covered work; outside-org modified availability stays AGPL).

## LESSONS LEARNED

- §7 plus a §1 / covered-work paragraph is the “even if” instrument. The brief’s extra sentence is not load-bearing once that paragraph exists.
- Verbatim root `LICENSE` plus a complete script header is how a typical-install grant stays self-contained without breaking AGPL detection.
- `surgery.py` is not the product. A subset echo is worse than vanilla or a byte-for-byte copy of the `summem` header; it will drift (it already did: singular “permission” vs plural).
- Recipients may strip additional permissions. A stripped fork is still AGPL.

## PROCESS IMPROVEMENTS

- For license L3s, Creative draft terms are a starting copy. The operator-settled header is the artifact. Plan steps that say “copy the Creative paragraph” will disagree with QA after the copyright holder rewrites the grant.
- Preflight advisories about skimmability (capsule first) are optional. Do not apply them over an AGPL-first operator choice.
- Do not invent an echo on a non-product file to answer a copy-alone case the brief did not ask to solve.

## TECHNICAL IMPROVEMENTS

Nothing further. The live header is the operator-owned grant. Do not reopen wording unless asked.

## NEXT STEPS

- Draft [PR #32](https://github.com/Texarkanine/SumMem/pull/32) on `licensing-2`. This archive commit should land on that branch so the PR drops `memory-bank/active/`.
