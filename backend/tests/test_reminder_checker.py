"""Unit tests for the pure detection function ``check_user`` (Unit 2).

12 tests covering reminder detection, overdue detection, status filtering,
deduplication, naive datetime handling, and deterministic ordering.
"""

from datetime import datetime, timedelta, timezone

import pytest

from models import Priority, Status, Todo
from services.reminder_checker import OVERDUE, REMINDER_DUE, check_user


def _make_todo(
    *,
    todo_id: str = "t1",
    title: str = "Task",
    status: Status = Status.PENDING,
    due_date: str | None = None,
    reminder_at: datetime | None = None,
) -> Todo:
    return Todo(
        id=todo_id,
        user_id="u1",
        title=title,
        priority=Priority.MEDIUM,
        status=status,
        due_date=due_date,
        reminder_at=reminder_at,
        created_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
    )


@pytest.fixture
def now() -> datetime:
    return datetime(2026, 5, 24, 12, 0, tzinfo=timezone.utc)


# 1
def test_no_todos_returns_empty(now):
    assert check_user([], now) == []


# 2
def test_reminder_in_future_no_notification(now):
    todo = _make_todo(reminder_at=now + timedelta(hours=1))
    assert check_user([todo], now) == []


# 3
def test_reminder_at_now_fires(now):
    todo = _make_todo(reminder_at=now)
    out = check_user([todo], now)
    assert len(out) == 1
    assert out[0].kind == REMINDER_DUE
    assert out[0].todo_id == "t1"


# 4
def test_reminder_in_past_fires(now):
    todo = _make_todo(reminder_at=now - timedelta(minutes=5))
    out = check_user([todo], now)
    assert [n.kind for n in out] == [REMINDER_DUE]


# 5
def test_done_todo_never_fires_reminder(now):
    todo = _make_todo(reminder_at=now - timedelta(hours=1), status=Status.DONE)
    assert check_user([todo], now) == []


# 6
def test_overdue_due_date_yesterday_fires(now):
    todo = _make_todo(due_date="2026-05-23")  # one day before `now`
    out = check_user([todo], now)
    assert [n.kind for n in out] == [OVERDUE]


# 7
def test_overdue_today_does_not_fire(now):
    todo = _make_todo(due_date="2026-05-24")  # same date as `now`
    assert check_user([todo], now) == []


# 8
def test_done_todo_never_fires_overdue(now):
    todo = _make_todo(due_date="2026-05-01", status=Status.DONE)
    assert check_user([todo], now) == []


# 9
def test_dedup_skips_already_notified(now):
    todo = _make_todo(reminder_at=now - timedelta(minutes=1))
    out = check_user([todo], now, already_notified={("t1", REMINDER_DUE)})
    assert out == []


# 10
def test_dedup_independent_per_kind(now):
    todo = _make_todo(
        reminder_at=now - timedelta(minutes=1),
        due_date="2026-05-23",
    )
    out = check_user([todo], now, already_notified={("t1", REMINDER_DUE)})
    kinds = [n.kind for n in out]
    assert kinds == [OVERDUE]


# 11
def test_naive_datetime_treated_as_utc():
    naive_now = datetime(2026, 5, 24, 12, 0)
    naive_reminder = datetime(2026, 5, 24, 11, 0)
    todo = _make_todo(reminder_at=naive_reminder)
    out = check_user([todo], naive_now)
    assert [n.kind for n in out] == [REMINDER_DUE]


# 12
def test_output_is_sorted_deterministically(now):
    todos = [
        _make_todo(todo_id="b", reminder_at=now - timedelta(minutes=1)),
        _make_todo(todo_id="a", reminder_at=now - timedelta(minutes=1)),
        _make_todo(todo_id="c", due_date="2026-05-22"),
    ]
    first = check_user(todos, now)
    second = check_user(list(reversed(todos)), now)
    assert first == second
    # earliest trigger first; among ties (the two reminders share the same
    # trigger_at) ordering is by todo_id
    assert [(n.todo_id, n.kind) for n in first] == [
        ("c", OVERDUE),
        ("a", REMINDER_DUE),
        ("b", REMINDER_DUE),
    ]
