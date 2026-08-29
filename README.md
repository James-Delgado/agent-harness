# agent-harness

A minimal, file-based operating harness for autonomous coding agents (built for
[Claude Code](https://claude.com/claude-code), portable to any agent that reads
markdown). One slash command — `/project-init` — scaffolds any repo so that the
standing prompt

> *"Pick up the next ready task from `docs/PRIORITIES.yaml`."*

is sufficient for an agent to execute real work end-to-end: orient, plan, claim
a task, build it with tests, verify with visible output, review its own work,
capture discovered follow-ups, and commit — with an audit trail a human can
check asynchronously instead of supervising in real time.

## The idea

Most agent friction comes from two places: the agent not knowing *what* to do
next, and the human not trusting *how* it was done. The harness attacks both
with three small files committed to the repo:

| File | Role |
|---|---|
| `CLAUDE.md` | Entry point: codebase map, environment commands, skill routing. What a fresh-context agent reads first. |
| `docs/AGENT_OPERATION.md` | The per-task SOP. Plan → claim (standalone status commit) → execute with tests → verify with quoted output → post-task review → append follow-ups → one deliverable commit. |
| `docs/PRIORITIES.yaml` | Ranked living backlog. Next action = lowest-`rank` task with `status: ready`. Dependencies (`depends_on`/`blocks`) are the hard ordering; rank is the tiebreak. Discovered work is appended, never dropped. |

The **full tier** adds `docs/METHODOLOGY.md` (binding standards the project
holds itself to) and a **backlog drift test** (`tests/test_priorities.py`) that
CI-enforces backlog integrity: statuses in enum, dependency references resolve,
at most one task `in_progress`, `done` tasks carry timestamps.

Key design choices, learned the hard way:

- **The backlog is code.** It lives in git, is schema-checked by a test, and
  every status flip is a commit. `git log` *is* the timeline; the YAML is the
  current state.
- **The in-progress commit is standalone.** A one-line commit when a task is
  claimed makes task duration and ordering auditable from history alone.
- **Verification is quoted, never paraphrased.** "All green" is banned; the
  agent pastes the actual test output.
- **Follow-ups are appended, not decided.** Agents capture discovered work with
  a provenance note; the human re-ranks. Human judgment calls get explicit
  `blocked` decision-gate tasks that an autonomous loop can never auto-pick, and
  human-*executed* work (device deploys, account actions) carries an `owner:`
  field agents must never claim — they prepare the harness for it and stop.
- **Judgment-derived constants get a veto window.** Numeric gates, thresholds,
  pins, and schemas an agent chose are reported item-by-item in conversation,
  tagged DRAFT, and bind only after explicit human approval — never silently.
- **Done tasks never leave the backlog.** The YAML records current state; git
  history records the timeline. Deleting done tasks breaks every forward
  dependency reference.
- **Projects end with a closeout task.** A terminal `<PROJECT>-CLOSE` task,
  dependent on all others, validates that the tasks *compose* (the integration
  seam unit tests can't reach) and refreshes newcomer-facing docs. Both field
  projects invented this independently before it was templated.
- **Single-threaded by default.** Serial execution from the top of the ranked
  list avoids multi-writer conflicts on shared files; parallelism is something
  you add deliberately, not a default.

## Field results

The harness has run two real projects end-to-end:

- A private quant-research monorepo, through five project phases with minimal
  intervention — including a 9-hour autonomous loop that completed 23 queued
  tasks across 46 commits, every task passing an independent verification gate
  (full pytest suite + lint re-run between tasks), zero failures. The
  task-curation rules that made that safe are now the SOP's "Autonomous loop
  mode" section, and the `autonomy:` task tag makes the curation mechanical.
- A Metal/Swift on-device LLM inference engine, where the harness picked up
  `owner:` tasks (on-phone work only a human can run), just-in-time phase
  specs, the veto-window protocol for pre-committed numeric gates, and the
  in-repo `DECISIONS.md` ledger — all now folded back into the templates.

The backlog drift test shipped here runs green against both projects' live
backlogs.

## Install

```bash
git clone https://github.com/James-Delgado/agent-harness
cd agent-harness
cp commands/project-init.md ~/.claude/commands/
mkdir -p ~/.claude/templates
cp -r templates/project-init ~/.claude/templates/
```

Then in any repo, run `/project-init [lite|full] [project name]` inside Claude
Code. The command detects the stack (Python/Node/Rust/Go/C++), writes a broad
personal permission allowlist *first* so the rest of setup doesn't prompt,
fills the templates from the actual file tree, and seeds the backlog with a
single bootstrap task: run a deep code audit to populate it with verified
findings rather than guessed ones.

## Tiers

- **lite** — backlog + tests-with-code + one-commit-per-task discipline. For
  apps and scripts where the full audit trail is overkill.
- **full** — adds the methodology contract, the drift test, per-task post-task
  review, and session logs. For research or anything where "did this actually
  work?" must survive scrutiny.

## Layout

```
commands/project-init.md          the slash command (the installer/scaffolder)
templates/project-init/
├── CLAUDE.md                     repo entry-point template
├── AGENT_OPERATION.md            per-task SOP template
├── PRIORITIES.yaml               ranked backlog template + schema
├── test_priorities.py            backlog drift test (full tier; copied verbatim)
├── DECISIONS.md                  append-only decision/measurement ledger stub (full tier)
├── settings.json                 project permission-allowlist skeleton
└── README.md                     meta-guidance for the scaffolding agent
```

## License

MIT
