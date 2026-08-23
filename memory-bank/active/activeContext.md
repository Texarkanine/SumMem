# Active Context

## Current Task: agpl-carve-outs
**Phase:** REFLECT COMPLETE

## What Was Done
- Program stays AGPL. Prompt template is 0BSD (full terms in the `summem` header). No REUSE. `LICENSE` stays verbatim AGPL. Script is the authoritative source; `surgery.py` echoes invocation only; README points at the header.
- Invocation is three paragraphs under §7: (1) §1 intimate-link denial + caller is not a covered work; org/personnel definitions (common control); (2) §13 carve-out for invocation directed by you, personnel, or an agent acting for the org, including over a network; (3) if a modified version is made available outside the org (distribute or offer remote interaction), paragraph 2 does not apply and §13 does. Paragraph 3 must not revoke paragraph 1.
- QA PASS (advisories only). Reflection written. Operator-settled header was not reopened.

## Next Step
- Run `/niko-archive` to create the archive document and finalize the current project.
