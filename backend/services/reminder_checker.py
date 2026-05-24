"""Pure detection logic for reminder and overdue notifications (Unit 2).

This module is intentionally side-effect free: no file I/O, no network, no
clock reads. The caller passes ``now`` and ``already_notified`` so the
function is fully deterministic and trivial to unit-test.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timezone
from typing import Iterable

from models import Status, Todo


@dataclass(frozen=True)
class Notification:
    """A notification candidate emitted by ``check_user``.

    Attributes:
        todo_id: The id of the todo the notification refers to.
        kind: Either ``"reminder_due"`` or ``"overdue"``.
        title: A snapshot of the todo title at the time of detection.
        trigger_at: The datetime that caused the notification to fire
            (``reminder_at`` for reminders, midnight UTC of the due date
            for overdue todos).
    """

    todo_id: str
    kind: str
    title: str
    trigger_at: datetime


REMINDER_DUE = "reminder_due"
OVERDUE = "overdue"


def _ensure_aware(dt: datetime) -> datetime:
    """Treat naive datetimes as UTC for stable comparison."""
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt


def check_user(
    todos: Iterable[Todo],
    now: datetime,
    already_notified: frozenset[tuple[str, str]] | set[tuple[str, str]] | None = None,
) -> list[Notification]:
    """Detect todos that need a reminder or overdue notification.

    Pure function: no I/O, no side effects, no mutation of inputs.

    Detection rules:

    * ``reminder_due`` fires when ``reminder_at <= now`` and ``status != done``.
    * ``overdue`` fires when ``due_date < now.date()`` and ``status != done``.
    * A ``(todo_id, kind)`` pair present in ``already_notified`` is skipped
      to deduplicate against previously delivered notifications.

    The returned list is sorted by ``(trigger_at, todo_id, kind)`` so output
    is deterministic across runs.

    Args:
        todos: The user's todos. Any iterable of :class:`Todo` is accepted.
        now: Reference datetime. Naive datetimes are treated as UTC.
        already_notified: Set of ``(todo_id, kind)`` pairs to suppress.

    Returns:
        A new sorted list of :class:`Notification` instances.
    """
    seen: frozenset[tuple[str, str]] = (
        frozenset(already_notified) if already_notified else frozenset()
    )
    now = _ensure_aware(now)
    today = now.date()

    notifications: list[Notification] = []

    for todo in todos:
        if todo.status == Status.DONE:
            continue

        # Reminder detection
        if todo.reminder_at is not None:
            reminder_at = _ensure_aware(todo.reminder_at)
            if reminder_at <= now and (todo.id, REMINDER_DUE) not in seen:
                notifications.append(
                    Notification(
                        todo_id=todo.id,
                        kind=REMINDER_DUE,
                        title=todo.title,
                        trigger_at=reminder_at,
                    )
                )

        # Overdue detection
        if todo.due_date is not None:
            try:
                due = date.fromisoformat(todo.due_date)
            except (ValueError, TypeError):
                continue
            if due < today and (todo.id, OVERDUE) not in seen:
                notifications.append(
                    Notification(
                        todo_id=todo.id,
                        kind=OVERDUE,
                        title=todo.title,
                        trigger_at=datetime.combine(
                            due, datetime.min.time(), tzinfo=timezone.utc
                        ),
                    )
                )

    notifications.sort(key=lambda n: (n.trigger_at, n.todo_id, n.kind))
    return notifications
