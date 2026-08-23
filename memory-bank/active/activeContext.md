# Active Context

## Current Task: agpl-carve-outs
**Phase:** BUILD - COMPLETE

## What Was Done
- Program stays AGPL. Prompt template is 0BSD (full terms in the `summem` header). No REUSE. `LICENSE` stays verbatim AGPL. Script is the authoritative source; `surgery.py` echoes invocation only; README points at the header.
- Invocation is three paragraphs under §7: (1) §1 intimate-link denial + caller is not a covered work; org/personnel definitions (common control); (2) §13 carve-out for invocation directed by you, personnel, or an agent acting for the org, including over a network; (3) if a modified version is made available outside the org (distribute or offer remote interaction), paragraph 2 does not apply and §13 does. Paragraph 3 must not revoke paragraph 1.
- Prompt template block is 0BSD, after the invocation grant.
- Operator likes the current header as-is after manual revision. Do not reopen wording.
- Full suite: 262 pytest on py311–py314.

## Next Step
- QA review.

## Operator decisions after preflight
- Dual-license refusal is the **program** only. Prompt is 0BSD.
- Script must stay self-contained. REUSE does not travel and is not required.
- Verbatim `LICENSE` does not revoke file carve-outs.
- AGPL-first header (no capsule above the FSF notice).
- Autonomous agents acting for the org are covered; they are not “entities under common control.”
- Paragraph 3 (outside the org) stays: otherwise a customer-facing agent “acting for the org” would swallow the modified-SaaS case.
