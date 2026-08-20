# Active Context

## Current Task: noting-ratchet
**Phase:** PREFLIGHT - COMPLETE (PASS WITH ADVISORY)

## What Was Done
- Preflight [FAIL (fixable)](1b1f8b7c-d52d-4955-891e-a5fc3b443028): shared multi-line copy was note-only; `unknown id` next step would have hit missing-tree raises.
- Plan rewrite: `One line only. Merge the lines.`; wake hint only at identity-miss sites; leave `note is empty`; UTF-8 282-byte assert; extend existing CLI note leak test; drain `capsys` on the tight store.

## Next Step
- Build the length ratchet, then the other raise-site ratchets.
