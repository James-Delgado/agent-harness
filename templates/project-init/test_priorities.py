"""Backlog drift test — keeps docs/PRIORITIES.yaml structurally honest.

Ships with the agent harness (project-init, full tier). Deps: pyyaml, pytest.
Hardened across two field projects; covers the invariants the SOP relies on,
including the decision-gate allowance (blocked with satisfied deps + a note).
"""

from __future__ import annotations

from datetime import date, datetime
from pathlib import Path

import yaml

PRIORITIES_PATH = Path(__file__).resolve().parents[1] / "docs" / "PRIORITIES.yaml"


def _load() -> tuple[dict, list[dict]]:
    with PRIORITIES_PATH.open() as fh:
        data = yaml.safe_load(fh)
    assert isinstance(data, dict), "PRIORITIES.yaml top level must be a mapping"
    tasks = data.get("tasks") or []
    assert isinstance(tasks, list), "`tasks` must be a list"
    return data, tasks


def _to_date(value: object, field: str, task_id: str) -> date:
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00")).date()
        except ValueError as exc:
            raise AssertionError(f"{task_id}: unparseable {field}: {value!r}") from exc
    raise AssertionError(f"{task_id}: {field} has wrong type: {value!r}")


def test_statuses_in_enum() -> None:
    data, tasks = _load()
    enum = set(data["schema"]["task_status"])
    for t in tasks:
        assert t["status"] in enum, f"{t['id']}: unknown status {t['status']!r}"


def test_complexity_in_enum_when_present() -> None:
    data, tasks = _load()
    enum = set(data["schema"]["complexity"])
    for t in tasks:
        cx = t.get("est_complexity")
        if cx is not None:
            assert cx in enum, f"{t['id']}: unknown est_complexity {cx!r}"


def test_ids_unique() -> None:
    _, tasks = _load()
    ids = [t["id"] for t in tasks]
    dupes = {i for i in ids if ids.count(i) > 1}
    assert not dupes, f"duplicate task ids: {sorted(dupes)}"


def test_ranks_unique() -> None:
    _, tasks = _load()
    ranks = [t["rank"] for t in tasks]
    dupes = {r for r in ranks if ranks.count(r) > 1}
    assert not dupes, f"duplicate ranks: {sorted(dupes)}"


def test_dependency_references_resolve() -> None:
    _, tasks = _load()
    ids = {t["id"] for t in tasks}
    for t in tasks:
        for field in ("depends_on", "blocks"):
            for ref in t.get(field) or []:
                assert ref in ids, f"{t['id']}: {field} references unknown id {ref!r}"


def test_at_most_one_in_progress() -> None:
    _, tasks = _load()
    active = [t["id"] for t in tasks if t["status"] == "in_progress"]
    assert len(active) <= 1, f"more than one in_progress task: {active}"


def test_done_tasks_have_completed_at() -> None:
    _, tasks = _load()
    for t in tasks:
        if t["status"] == "done":
            assert t.get("completed_at"), f"{t['id']}: done without completed_at"


def test_timestamps_parse_and_order() -> None:
    _, tasks = _load()
    for t in tasks:
        started = t.get("started_at")
        completed = t.get("completed_at")
        s = _to_date(started, "started_at", t["id"]) if started else None
        c = _to_date(completed, "completed_at", t["id"]) if completed else None
        if s and c:
            assert c >= s, f"{t['id']}: completed_at {c} before started_at {s}"


def test_blocked_tasks_have_unmet_dep_or_note() -> None:
    """A blocked task must be waiting on SOMETHING: an unmet dependency, or —
    for decision-gate tasks whose deps are all done — an explanatory note."""
    _, tasks = _load()
    by_id = {t["id"]: t for t in tasks}
    for t in tasks:
        if t["status"] != "blocked":
            continue
        unmet = [
            d for d in t.get("depends_on") or [] if by_id[d]["status"] != "done"
        ]
        assert unmet or t.get("notes"), (
            f"{t['id']}: blocked with all deps done and no notes — either flip "
            "to ready or document the gate (decision_gate_protocol)"
        )
