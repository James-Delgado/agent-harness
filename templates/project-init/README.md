# Personal project-init template

Scaffold for a new repo that runs the "ranked backlog + clean-context agent per
task" workflow. Copy these into a new project and fill the `<placeholders>`:

    <repo>/CLAUDE.md              <- from CLAUDE.md (entry point + skill routing)
    <repo>/docs/AGENT_OPERATION.md
    <repo>/docs/PRIORITIES.yaml
    <repo>/docs/METHODOLOGY.md    <- only for the "full" tier; write your binding rules
    <repo>/tests/test_priorities.py  <- the backlog drift test (full tier)

## Tiers
- **lite**: CLAUDE.md + AGENT_OPERATION.md + PRIORITIES.yaml. Backlog + tests-with-code.
- **full**: add METHODOLOGY.md, the drift test, a trial/decision ledger, post-task
  reviews, and session logs. Use for research / long-lived / high-stakes repos.

## Recommended ecc footprint (lean — drop the niche verticals)
The full ecc install loads ~230 skills incl. healthcare / networking / supply-chain
/ media verticals you won't use. For an engineering+research harness, prefer:

    install.sh --profile developer \
      --with agentic-patterns --with machine-learning --with research-apis \
      --dry-run        # inspect first, then drop --dry-run to apply

`developer` already drops the business/supply-chain/social/media/operator verticals;
the `--with` flags re-add the agentic + ML + research modules you do use.

NOTE on duplication: if ecc is installed BOTH as a plugin (`ecc@ecc` in
settings.json) AND via install.sh, skills/agents appear twice (bare + `ecc:`).
Pick ONE source. Rules (global memory) come only from the install.sh `rules/ecc/`
tree; hooks come only from the plugin — so a clean setup keeps whichever provides
the pieces you rely on and removes the other's duplicates.

## Global vs project precedence
Everything (global `~/.claude/CLAUDE.md`, ecc rules, this project's CLAUDE.md) is in
context at once. On conflict, **more specific wins** — this project's SOP overrides
global defaults. Skill routing is per-project; restate it in each repo's CLAUDE.md.

## Project settings.json (optional but recommended)
`settings.json` here is a **project** scaffold for `<repo>/.claude/settings.json`
(committed, team-shared). Distinct from the **global** `~/.claude/settings.json`
(plugins/hooks for all projects) and from `<repo>/.claude/settings.local.json`
(personal, gitignored).

The skeleton allowlists read-only git/ls so you stop getting prompted for them.
Add your stack's test/lint commands once they're stable, e.g.
`"Bash(.venv/bin/pytest:*)"`, `"Bash(.venv/bin/ruff:*)"`, `"Bash(npm test:*)"`.
Keep mutating/destructive commands OUT of `allow` (let them prompt).
