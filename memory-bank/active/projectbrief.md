# Project Brief

## User Story

As an operator of a consuming repository, I want SumMem’s write rule (what to remember, and when) to live in the `init`-emitted `AGENTS.md` prefix as an editable default, so I can choose a different gate without forking the script, while command recipes stay versioned with the running script and cannot stamp over that choice.

## Use-Case(s)

### Use-Case 1

A repo keeps the shipped default: lore and tree-affecting in-flight work, not process telemetry, not personal/machine/preference facts.

### Use-Case 2

A repo edits the prefix so agents record a work log, or only PR-review feedback. Root wake still teaches argv, grammar, and writer-only. Usage does not reassert the shipped membership paragraph.

### Use-Case 3

A consumer copies a newer `summem`. Usage updates. Their existing write rule in `AGENTS.md` does not.

## Requirements

1. Implement the disjoint split in `memory-bank/active/creative/creative-entry-gate-split.md` on branch `who-gates-entry`.
2. `prompt_text()` / committed prefix: write rule (WHAT) and when to wake / when to consider recording (WHEN). Skip-if-already-woke stays. The only argv is root `wake`. The recording verb `note` may be named without a command line.
3. `how_to_text()` / root-wake Usage: command recipes only (note/nap/recall/zoom argv, pack/leaf grammar, writer-only, fold follow-ups, catalog pull). No membership probe, genre list, denylist, personal/machine stay-out, or skip-if-nothing-qualifies.
4. `init_text()` operator wrapper: the printed block is a starting write rule the operator may edit; command syntax comes from root wake and should not be copied into the prefix. Still no “paste.” Do not put that demotion in `prompt_text()`.
5. This repository’s `AGENTS.md` stays lockstep with `prompt_text()` as dogfood of the shipped default, not as a consumer contract.
6. The shipped default write rule stays the current membership probe, genre list, denylist, and personal/machine stay-out. This task does not change what this repository remembers.

## Constraints

1. `init` writes nothing. No `summem upgrade`. No new store file or overlay.
2. Do not name Usage or footer flags in the bootstrap (wake-usage-prompt leftover-pin class).
3. Do not change the store, CLI verbs, or nap/zoom/recall mechanics.
4. Prompt template remains 0BSD. Writer-only and command recipes stay in versioned how-to output.
5. Work on `who-gates-entry`. Do not invent a test that a foreign `AGENTS.md` must match `prompt_text()`.

## Acceptance Criteria

1. Write-rule phrases are absent from `how_to_text()`. Mechanical phrases (writer-only, `wake --path`, pack grammar) are absent from `prompt_text()` except the wake handoff.
2. `summem init` still prints an insert recipe plus `prompt_text()`, and the recipe tells the operator the block is a starting write rule they may edit.
3. This repo’s `AGENTS.md` starts with `prompt_text()`.
4. Root wake still prepends Usage; pulls still omit it.
5. A consumer who edited only the write-rule section of their prefix is not contradicted by Usage.
