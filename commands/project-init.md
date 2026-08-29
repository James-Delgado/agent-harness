---
description: Scaffold the current repo with the personal agentic harness (CLAUDE.md + AGENT_OPERATION + ranked PRIORITIES backlog)
argument-hint: "[lite|full] [project name]"
---

You are bootstrapping the personal agentic-workflow harness into the **current
repository** (cwd). Template source: `~/.claude/templates/project-init/`.

Arguments (optional): `$ARGUMENTS` — first token may be the tier (`lite` or `full`),
the rest is the project name. If the tier or name is missing, ask the user (one
concise question; default tier = `lite` for an app/script, `full` for research or
anything long-lived/high-stakes).

Do this:

1. **Safety check.** Confirm cwd is the intended repo. If it is NOT a git repo, ask
   before proceeding (offer `git init`). If `CLAUDE.md` already exists, DO NOT
   overwrite it — show a diff-style summary of what you'd add and ask first.

2. **Permissions FIRST — before writing anything else.** Write
   `.claude/settings.local.json` (personal, **git-ignored**, NOT committed) with a
   **broad** allowlist so the rest of init doesn't trigger a prompt on every step.
   Include read-only git + common dev commands and the detected test runner, e.g.
   `Bash(git *)`, `Bash(python:*)`/`Bash(python3:*)`, `Bash(pip:*)`, `Bash(pytest:*)`,
   `Bash(ls:*)`, `Bash(cat:*)`, `Bash(find:*)`, `Bash(grep:*)`, `Bash(mkdir:*)`,
   `Bash(mv:*)`, `Bash(touch:*)` (adapt to the stack). Then ensure
   `.claude/settings.local.json` is in `.gitignore` (append it; create `.gitignore`
   if absent). Do **not** create a committed `.claude/settings.json` — a team-wide
   allowlist is premature for a fresh repo; `settings.local.json` is per-developer.
   Note: this allowlist only covers Bash — it does not silence Write/Edit prompts or
   hooks (e.g. GateGuard), so some prompts may still appear.

3. **Detect the stack** (do not assume): look for `pyproject.toml`/`requirements.txt`
   (python), `package.json` (node/ts; note framework — next/vite/etc.),
   `Cargo.toml` (rust), `go.mod` (go), `CMakeLists.txt` (c++), a `.venv/`, the test
   runner (pytest/jest/vitest/cargo test/go test), and the package manager. Record
   the exact invocations (e.g. `.venv/bin/pytest tests/`, `npm test`).

4. **Scaffold from the template** (read each file, fill the `<placeholders>`, write
   into the repo):
   - `CLAUDE.md` → repo root. Fill: project name, the chosen **Tier** (delete the
     other), a one-line **Project status**, a **Codebase map** built from the actual
     top-level source tree, **Environment & running** from the detected stack, and
     prune the **Skill routing** table to the rows this project will actually use
     (include `/code-audit` for deep code/MLE auditing).
   - `docs/AGENT_OPERATION.md` and `docs/PRIORITIES.yaml` → `docs/`. In PRIORITIES,
     set `last_updated`. **Do not infer analysis tasks** (bugs, design/MLE issues) —
     that is `/code-audit`'s job. Seed only: (a) setup/scaffolding gaps that are
     trivially true from the file tree (e.g. no `requirements.txt`, no test dir), and
     (b) one bootstrap task **"Run `/code-audit` to populate the backlog with verified
     findings."** If neither applies, leave the example with a clear "replace me".
   - **full tier only:** also create `docs/METHODOLOGY.md` (a short stub: list the
     binding rules this project will hold itself to — keep it the checklist an agent
     re-reads at post-task review, with detail delegated to specs), copy
     `test_priorities.py` → `tests/` **verbatim** (the hardened backlog drift test;
     needs `pyyaml` + `pytest` — wire into the repo's test runner, adapting only the
     `PRIORITIES_PATH` if the repo's layout differs), and copy `DECISIONS.md` →
     repo root (the append-only decision/measurement ledger).

5. **Do not** copy the template README into the repo (it's meta-guidance for you).

6. **Report**: list every file created, the chosen tier, and the exact next step —
   normally *"Run `/code-audit` to populate the backlog, then pick up the next ready
   task from docs/PRIORITIES.yaml."* Do not commit unless the user asks.

Keep edits minimal and idiomatic to the detected stack. The project's
`AGENT_OPERATION.md` becomes authoritative for that repo and overrides global
defaults (per `~/.claude/CLAUDE.md`).
