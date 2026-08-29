# Agent Operation Procedure (template)

> The per-task SOP. The minimal user prompt is *"Pick up the next ready task from
> docs/PRIORITIES.yaml."* That is sufficient — this document is the rest.

## The procedure (every task)

1. **Orient.** Read `CLAUDE.md`, this file, `docs/PRIORITIES.yaml`, and (if present)
   `docs/METHODOLOGY.md` plus the current phase/project spec. Find the lowest-`rank`
   task with `status: ready`. That is your task — do not pick another. If the task
   belongs to a phase whose spec doesn't exist yet, stop and say so (specs are
   written just-in-time; see PRIORITIES `spec_protocol`).
2. **Plan.** Post a short plan as your first message: restate the deliverable,
   approach, which standards apply, how you'll verify, anticipated follow-ups, and
   any decision that genuinely needs the user. If none, proceed without waiting.
3. **Claim it.** Set the task `status: in_progress` + `started_at` (UTC). Commit
   THIS change alone: `chore(priorities): mark <ID> in_progress`. The standalone
   commit makes task timing auditable from `git log` alone.
4. **Execute.** Build the deliverable. Tests land with the code (red→green→refactor).
5. **Verify — show the output.** Run the tests / lint / build and paste the actual
   results. Never paraphrase ("all green") — quote it.
6. **Post-task review** (full tier). Re-read the deliverable as if reviewing someone
   else's code; cross-check against your standards; note deviations honestly.
7. **Append discovered follow-ups** to `docs/PRIORITIES.yaml` per its
   `append_protocol` (including wiring them into the project's `*-CLOSE` task).
   If none: say so explicitly — silence is not the same as no findings.
8. **Mark done.** Set `status: done` + `completed_at`; flip any now-unblocked
   dependents from `blocked` to `ready`.
9. **Commit the deliverable** (code + tests + docs + the priorities update) in one
   commit: `<type>(<scope>): <subject>` with a "Closes <ID>" line.
10. **Ledger** (full tier): if the session decided or measured anything, append a
    dated entry to `DECISIONS.md` (append-only): what was decided/measured, and why.
11. **Report.** One scannable message: what shipped, commits, test status,
    follow-ups, what's next.

## When to pause

Irreversible or convention-setting decisions wait for the user (new top-level
dirs/modules, methodology deviations, destructive ops beyond the task). Reversible,
convention-following decisions proceed — surface them in the plan, don't block.

Two structural forms of "wait for the human" live in the backlog itself:

- **`owner:` tasks** — tasks marked with a human `owner` (device work, deployments,
  account actions) are never executed by agents. Prepare the code/harness, then stop.
- **Decision-gate tasks** — `<ID>-DECISION`, kept `blocked` even with satisfied
  dependencies. See PRIORITIES `decision_gate_protocol`. "What is waiting on my
  decision?" is a first-class query: list not-done decision-gate tasks on request.

**Veto window for judgment-derived constants** (full tier): when a task produces
numeric gates, thresholds, pins, or schemas by agent judgment, report each item in
the conversation — chosen value + rationale — tagged DRAFT. They bind only after
the user approves (or an explicitly stated veto window closes). Never let a
pre-committed gate bind silently.

## Project closeout (full tier)

Every project/phase carries one terminal `<PROJECT>-CLOSE` (or `Pn-EXEC`) task whose
`depends_on` lists all its other tasks. Per-task verification never certifies that
tasks *compose*; the closeout does. Its deliverable: an end-to-end validation of the
combined surface (the integration seam unit tests can't reach), a short closeout
report, and a refresh of the newcomer-facing docs (README status etc.) so the repo
never presents an exited phase as current.

## Autonomous loop mode

When running unattended over the backlog:

- Pick only loop-safe tasks: no `owner`, not decision-gated, and `autonomy` absent
  or `safe` — skip `network` / `judgment` / `heavy-compute`.
- Verification gate BETWEEN tasks: independently re-run the test suite + lint and
  confirm the deliverable commit + status flip landed before dispatching the next.
- On failure: revert the task to `ready`, do NOT build on it; one retry, then skip.
- Stop on: wall-clock budget, queue exhausted, or 2 consecutive verification failures.
- If a task turns out mid-flight to need network or a judgment call: stop, leave it
  `ready`, report, move on.

## Red flags — what NOT to do

- ❌ Skip orientation ("I already know the docs"). They change; read them every time.
- ❌ Commit the `in_progress` flip together with code — it is standalone (step 3).
- ❌ Paraphrase test results. Run them; quote the output.
- ❌ Mark `done` without the post-task review.
- ❌ Bundle multiple tasks into one session — the audit trail breaks.
- ❌ Drop discovered follow-ups because they "don't seem important." Append them;
  the human re-ranks.
- ❌ Delete done tasks from the backlog (see PRIORITIES `task_lifecycle`).
- ❌ Modify a pinned invariant (gates, schemas, protected logic) without a recorded
  decision in `DECISIONS.md`.

## Lite tier

Steps 6 and 10 are optional; everything else still applies. The backlog + commit
discipline + tests-with-code are the non-negotiable core.
