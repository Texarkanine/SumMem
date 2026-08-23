# Project Brief

## User Story

As the copyright holder of SumMem, I want two AGPL carve-outs — obligation-free prompt text, and a full permission for AI-agent invocation — written so that a consumer who only copies the script still has the whole grant, so companies can *use* SumMem (including in customer-facing agents) without treating that use as copyleft, while a published fork still trips AGPL.

## Use-Case(s)

### Use-Case 1

A company pastes the suggested agent prompt into `AGENTS.md`. That paste carries no copyright claim and no license notice or AGPL obligation.

### Use-Case 2

A coding agent, or an agent offered to customers, invokes `.summem/summem` on a development or service machine. That invocation is not conveyance and not AGPL §13 network performance; even if a reviewer would call it either, the author explicitly permits it outside AGPL’s terms. The company is using SumMem, not shipping it.

### Use-Case 3

Someone publishes a competing memory store that is a modified or forked SumMem (“summemv2”). AGPL applies. That is the community-theft case the copyleft is for.

### Use-Case 4

A typical install copies only the script into the target repo. The script is the full authoritative statement of license and carve-outs. Any repo-root trappings echo that statement; they do not add a grant the script lacks.

## Requirements

1. SumMem the program stays AGPL. Do not dual-license the program.
2. The “paste this” agent prompt (`prompt_text()` / `init` output / `docs/agents-prompt.md`) carries no copyright and no obligation.
3. Full invocation carve-out: an AI agent running SumMem is not conveyance and not AGPL §13 network performance; **and even if it is**, that use is explicitly permitted outside AGPL’s terms. Covers developer-machine agents and customer-facing agents that invoke SumMem to do the work.
4. Publishing a modified or forked SumMem still fires AGPL.
5. The script is the authoritative source. Anything said in the SumMem repo about these grants must also appear in the script.
6. If REUSE is adopted: drop root `LICENSE` and use a `COPYING` document that explains the premise; the script still carries the full grant.

## Constraints

1. Do not dual-license the program as Apache/MIT/etc. “AGPL code that is dual licensed is not AGPL code.”
2. Do not make the invocation note an SPDX license exception if that would force `LicenseRef-` and break scanner identification of AGPL.
3. The attached Claude conversation is background for *how*, not committed file layout.
4. TDD governs executable behavior only. License and prompt prose are not change-detector tests.

## Acceptance Criteria

1. A reader who has only the script can see AGPL on the program, the prompt carve-out, and the full invocation permission.
2. Pasting the prompt into another repo does not require keeping a copyright notice or AGPL terms for that text.
3. The carve-out states both the author’s scope judgment (not conveyance / not §13) and an explicit permission if a reviewer disagrees.
4. Forking or publishing a modified SumMem remains under AGPL.
5. Repo-root license files, if any remain, do not contradict or outrank the script.
