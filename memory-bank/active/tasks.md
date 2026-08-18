# Current Task: file-backend

**Complexity:** Level 4

## Preflight Report

**Status:** PASS WITH ADVISORY

### Findings

- **PASS — Prerequisites:** `memory-bank/active/milestones.md` contains the completed L4 plan: three sequential, unchecked milestones with L1-L3 estimates. No creative phase was flagged or required because `VISION.md` settles the architecture and `ROADMAP.md` settles the sequencing.
- **PASS — TDD plan encoding:** The L4 milestone list is a decomposition plan, not a direct build plan. Each milestone must enter its own L1-L3 Niko sub-run and receive a test-first implementation plan and preflight before production code can be written. References to first proofs 1-8 are executable acceptance gates, not assertions on document contents.
- **PASS — Convention compliance:** The milestones preserve the documented script-owned store, immutable files, SHA-256 leaf-set identity, filename sequence, wait-free wake, started-directory scopes, committed per-store knobs, and stable agent-facing CLI.
- **PASS — Dependency impact:** The milestones are correctly serial. Ingest establishes package/test infrastructure and freezes identity and format contracts; single-store memory consumes those contracts; scopes extends command resolution without changing identity or `HEAD`-based zoom.
- **PASS — Conflict detection:** The tree has no Python package, CLI, store implementation, or test harness to duplicate or contradict. The plan explicitly excludes locks, mutable indexes, custom merge drivers, git-history identity, package-manifest discovery, and `ROADMAP.md` Later items.
- **PASS — Completeness:** The three milestones map to all requirements, constraints, and first proofs: ingest covers proof 1, single-store memory covers proofs 2-6, and scopes covers proofs 7-8. The cross-milestone invariants preserve requirements that span all three.
- **ADVISORY — Format compatibility vectors:** The exact canonical `.tree` bytes are not specified in `VISION.md`, yet milestone 1 must freeze that format before milestone 2 writes naps. Test-drive a small pure codec boundary in the ingest sub-run with golden vectors for note-byte digests, sorted leaf-set IDs, and nested canonical `.tree` bytes; then make later storage and future backends consume the same vectors.

### Plan Amendment

- During the ingest sub-run's plan, put failing compatibility-vector tests before the codec implementation. Treat those vectors as the executable format contract reused by the single-store milestone; do not test wording in `VISION.md`.
