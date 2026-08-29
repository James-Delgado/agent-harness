# Agent Operation Procedure (template)

> The per-task SOP. The minimal user prompt is *"Pick up the next ready task from
> docs/PRIORITIES.yaml."* That is sufficient — this document is the rest.

## The procedure (every task)

1. **Orient.** Read `CLAUDE.md`, this file, `docs/PRIORITIES.yaml`, and (if present)
   `docs/METHODOLOGY.md`. Find the lowest-`rank` task with `status: ready`. That is
   your task — do not pick another.
2. **Plan.** Post a short plan as your first message: restate the deliverable,
   approach, which standards apply, how you'll verify, anticipated follow-ups, and
   any decision that genuinely needs the user. If none, proceed without waiting.
3. **Claim it.** Set the task `status: in_progress` + `started_at` (UTC). Commit
   THIS change alone: `chore(priorities): mark <ID> in_progress`.
4. **Execute.** Build the deliverable. Tests land with the code (red→green→refactor).
5. **Verify — show the output.** Run the tests / lint / build and paste the actual
   results. Never paraphrase ("all green") — quote it.
6. **Post-task review** (full tier). Re-read the deliverable as if reviewing someone
   else's code; cross-check against your standards; note deviations honestly.
7. **Append discovered follow-ups** to `docs/PRIORITIES.yaml` (unique id, rank,
   status, a `notes` line linking where it surfaced). If none: say so explicitly.
8. **Mark done.** Set `status: done` + `completed_at`; flip any now-unblocked
   dependents from `blocked` to `ready`.
9. **Commit the deliverable** (code + tests + docs + the priorities update) in one
   commit: `<type>(<scope>): <subject>` with a "Closes <ID>" line.
10. **Session log** (full tier): append goal/status/commits/summary/next.
11. **Report.** One scannable message: what shipped, commits, test status,
    follow-ups, what's next.

## When to pause
Irreversible or convention-setting decisions wait for the user (new top-level
dirs/modules, methodology deviations, destructive ops beyond the task). Reversible,
convention-following decisions proceed — surface them in the plan, don't block.

## Lite tier
Steps 6 and 10 are optional; everything else still applies. The backlog + commit
discipline + tests-with-code are the non-negotiable core.
