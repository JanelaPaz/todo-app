"""Reminder checker module — pure detection logic for due notifications.

This module contains a pure function that detects todos needing reminder
or overdue notifications. It performs no I/O and has no side effects.
"""

from datetime import date, datetime, timezone


def check_user(
    user_id: str,
    todos: list[dict],
    existing_notifications: list[dict],
) -> list[tuple[str, str, str]]:
    """Detect todos that need notifications generated.

    Pure function — no I/O, no side effects.

    Args:
        user_id: UUID4 string of the user to check.
        todos: List of todo dicts for this user. Each dict has keys:
            - "id": str (UUID4)
            - "user_id": str (UUID4)
            - "title": str
            - "status": str ("pending" | "in-progress" | "done")
            - "due_date": str | None (ISO date "YYYY-MM-DD")
            - "reminder_at": str | None (ISO datetime "YYYY-MM-DDTHH:MM:SSZ")
        existing_notifications: List of notification dicts for this user. Each dict has keys:
            - "id": str (UUID4)
            - "user_id": str (UUID4)
            - "todo_id": str (UUID4)
            - "type": str ("reminder" | "overdue")
            - "is_read": bool

    Returns:
        List of tuples: [(todo_id, notification_type, message), ...]
        - todo_id: str (UUID4) — the todo that triggered the notification
        - notification_type: str — "reminder" or "overdue"
        - message: str — e.g., "Reminder: Buy groceries" or "Overdue: Submit report"
    """
    now = datetime.now(timezone.utc)
    today = date.today()

    # Build a set of existing (todo_id, type) pairs for fast deduplication lookup
    existing_pairs: set[tuple[str, str]] = set()
    for notif in existing_notifications:
        todo_id = notif.get("todo_id", "")
        notif_type = notif.get("type", "")
        if todo_id and notif_type:
            existing_pairs.add((todo_id, notif_type))

    results: list[tuple[str, str, str]] = []

    for todo in todos:
        todo_id = todo.get("id", "")
        status = todo.get("status", "")
        title = todo.get("title", "")

        # Skip completed todos
        if status == "done":
            continue

        # Check for due reminders: reminder_at <= now
        reminder_at_str = todo.get("reminder_at")
        if reminder_at_str:
            if (todo_id, "reminder") not in existing_pairs:
                try:
                    reminder_at = datetime.fromisoformat(
                        reminder_at_str.replace("Z", "+00:00")
                    )
                    if reminder_at <= now:
                        message = f"Reminder: {title}"
                        results.append((todo_id, "reminder", message))
                except (ValueError, TypeError):
                    # Skip invalid datetime values
                    pass

        # Check for overdue todos: due_date < today
        due_date_str = todo.get("due_date")
        if due_date_str:
            if (todo_id, "overdue") not in existing_pairs:
                try:
                    due_date = date.fromisoformat(due_date_str)
                    if due_date < today:
                        message = f"Overdue: {title}"
                        results.append((todo_id, "overdue", message))
                except (ValueError, TypeError):
                    # Skip invalid date values
                    pass

    return results
