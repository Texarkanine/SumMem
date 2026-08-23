# Active Context

## Current Task: agpl-carve-outs
**Phase:** BUILD - header settled, operator likes as-is

## What Was Done
- Program stays AGPL. Prompt template is 0BSD (full terms in the `summem` header). No REUSE. `LICENSE` stays verbatim AGPL. Script is authoritative; `surgery.py` echoes invocation only; README points at the header.
- Invocation is three paragraphs under §7: (1) §1 intimate-link denial + caller is not a covered work; org/personnel definitions (common control); (2) §13 carve-out for invocation directed by you, personnel, or an agent acting for the org, including over a network; (3) if a modified version is made available outside the org (distribute or offer remote interaction), paragraph 2 does not apply and §13 does. Paragraph 3 must not revoke paragraph 1.
- Dropped: capsule-before-AGPL, “must retain” carve-outs, unmodified-no-Corresponding-Source paragraph, “you may invoke” restatements, network-only §13 trigger.
- Operator likes the current header as-is. Checkpoint `b3a44df`; later header edits may still be uncommitted.

## Next Step
- Finish BUILD bookkeeping if needed, then `/niko-qa`. Do not reopen header wording unless the operator asks.

## Operator decisions after preflight
- Dual-license refusal is the **program** only. Prompt is 0BSD.
- Script must stay self-contained. REUSE does not travel and is not required.
- Verbatim `LICENSE` does not revoke file carve-outs.
- AGPL-first header (no capsule above the FSF notice).
- Autonomous agents acting for the org are covered; they are not “entities under common control.”
- Paragraph 3 (outside the org) stays: otherwise a customer-facing agent “acting for the org” would swallow the modified-SaaS case.
