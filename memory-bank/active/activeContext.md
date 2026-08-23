# Active Context

## Current Task: agpl-carve-outs
**Phase:** PREFLIGHT - COMPLETE (PASS WITH ADVISORY)

## What Was Done
- Legal instruments: AGPL §7 additional permissions in the source.
- Authority: `summem` header is the full grant; no REUSE; `LICENSE` verbatim; README echo; `surgery.py` invocation echo.
- Plan: four prose/policy units; no new executable behavior.
- Preflight: PASS WITH ADVISORY (plan acceptable as-is).

## Next Step
- Talk through the prompt's permissive license (which one) before rewriting Creative/plan. Do not treat preflight as build-ready until that lands.

## Operator decisions after preflight
- Dual-license refusal is the **program** only. The prompt should be licensed under something permissive.
- The script must stay self-contained. REUSE does not travel and cannot be the grant — those points from the no-REUSE decision remain correct even if this repo later uses REUSE as an echo.
