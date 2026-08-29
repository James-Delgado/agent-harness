# CLAUDE.md — <PROJECT NAME>

> **Entry point for any agent or contributor. Read in this order:**
> 1. [`docs/AGENT_OPERATION.md`](docs/AGENT_OPERATION.md) — the standard operating
>    procedure (the per-task workflow). **This project's SOP overrides global defaults.**
> 2. [`docs/PRIORITIES.yaml`](docs/PRIORITIES.yaml) — the task backlog. The next
>    action is the **lowest-`rank` task with `status: ready`**.
> 3. [`docs/METHODOLOGY.md`](docs/METHODOLOGY.md) — binding standards (optional; keep
>    for research/long-lived projects, drop for small ones — see "Tier" below).

## Tier
<!-- Pick one and delete the other. Governs how much ceremony each task carries. -->
- **lite** — task backlog + tests-with-code + a one-commit-per-task discipline. For
  apps/scripts where the full audit trail is overkill.
- **full** — the above plus pre-committed gates (with a human veto window), the
  backlog drift test, an append-only `DECISIONS.md` ledger, per-task post-task
  review, and project-closeout tasks. For research or anything where "did this
  actually work?" needs to survive scrutiny.

## Project status
<!-- One short paragraph + a phase/status table. Keep this CURRENT and SHORT.
     Move completed-phase narratives to docs/historical/ and link them — do not
     accumulate prose here. -->

## Codebase map
<!-- A compact tree of the real modules + one-line purpose each. This is the
     highest-value section for a fresh-context agent. -->

## Environment & running
<!-- venv/toolchain invocation, the exact test/lint/build commands, any gotchas
     (e.g. "call binaries directly, never `source activate`"). -->

## Skill routing
When the user's request matches a capability below, invoke it as your FIRST action.
Names are disambiguated where two plugins collide (prefer the namespaced form).

| Request type | Invoke |
|---|---|
| Product ideas / brainstorming | `office-hours` (gstack) or `superpowers:brainstorming` |
| Bugs / "why is this broken" | `investigate` (gstack) or `superpowers:systematic-debugging` |
| **Code review of a diff** | **`/code-review`** (unambiguous) — *not* bare `review` (that's gstack's) |
| Deep multi-source research | `deep-research` |
| Ship / open a PR | `ship` (gstack) or `/pr` |
| QA a running web app | `qa` (gstack) |
| Architecture / plan review | `plan-eng-review` (gstack) |
| Update docs after shipping | `document-release` (gstack) |

> Routing is **per-project** — Claude Code does not carry a global routing table.
> Re-state the rows this project actually uses; delete the rest.

## Conventions that bind agents
- Tests land **with** the code, not after (see global `~/.claude/CLAUDE.md`).
- For substantive diffs, run `/code-review` (or `ecc:<lang>-reviewer`) before commit.
- Capture discovered follow-ups in `docs/PRIORITIES.yaml`; never drop them.
- Don't modify pinned invariants (split logic, gate thresholds, schemas) without a
  decision recorded in `DECISIONS.md` (full tier) or the backlog.
- Keep this file's status section current: project/phase closeouts refresh it (and
  any newcomer-facing doc); move finished-phase narratives to `docs/historical/`.
