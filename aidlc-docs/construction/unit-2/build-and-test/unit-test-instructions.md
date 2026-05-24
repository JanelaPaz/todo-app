# Unit 2 — Unit Test Instructions

20 pytest tests covering `check_user()` and `TodoService` `reminder_at`
handling. Tests are pure, run without a network, and complete in under a
second.

## Setup

```bash
cd backend
source .venv/bin/activate
pip install pytest
```

## Test files to create

### `backend/tests/test_reminder_checker.py`

12 tests against the pure detection function.

| #  | Test name                                              | What it validates                                          |
|----|--------------------------------------------------------|------------------------------------------------------------|
| 1  | `test_no_todos_returns_empty`                          | Empty input → empty output.                                |
| 2  | `test_reminder_in_future_no_notification`              | `reminder_at > now` is silent.                             |
| 3  | `test_reminder_at_now_fires`                           | `reminder_at == now` fires `reminder_due`.                 |
| 4  | `test_reminder_in_past_fires`                          | `reminder_at < now` fires `reminder_due`.                  |
| 5  | `test_done_todo_never_fires_reminder`                  | `status=done` suppresses reminders.                        |
| 6  | `test_overdue_due_date_yesterday_fires`                | `due_date < today` fires `overdue`.                        |
| 7  | `test_overdue_today_does_not_fire`                     | `due_date == today` does not fire (boundary).              |
| 8  | `test_done_todo_never_fires_overdue`                   | `status=done` suppresses overdue.                          |
| 9  | `test_dedup_skips_already_notified`                    | `(id, kind)` pair in `already_notified` is skipped.        |
| 10 | `test_dedup_independent_per_kind`                      | A `reminder_due` dedup does not suppress `overdue`.        |
| 11 | `test_naive_datetime_treated_as_utc`                   | Naive `reminder_at` and `now` compare correctly.           |
| 12 | `test_output_is_sorted_deterministically`              | Two calls on the same input return identical lists.        |

### `backend/tests/test_todo_service_reminder.py`

8 tests against `TodoService` for `reminder_at` create/update behavior.

| #  | Test name                                              | What it validates                                          |
|----|--------------------------------------------------------|------------------------------------------------------------|
| 13 | `test_create_persists_reminder_at`                     | `create()` stores the field.                               |
| 14 | `test_create_invalid_reminder_at_raises_422`           | Garbage string raises `ValidationError`.                   |
| 15 | `test_create_accepts_zulu_format`                      | `2024-01-15T10:30:00Z` is accepted.                        |
| 16 | `test_create_accepts_offset_format`                    | `2024-01-15T10:30:00+02:00` is accepted.                   |
| 17 | `test_update_changes_reminder_at`                      | New ISO string overwrites the previous value.              |
| 18 | `test_update_with_null_clears_reminder_at`             | Explicit `null` removes the reminder.                      |
| 19 | `test_update_without_field_preserves_reminder_at`      | Untouched field stays as-is.                               |
| 20 | `test_update_invalid_reminder_at_raises_422`           | Garbage string raises `ValidationError`.                   |

## Running

```bash
cd backend
pytest tests/test_reminder_checker.py tests/test_todo_service_reminder.py -v
```

Expected: 20 passed.
