# Unit Test Instructions — Unit 2: Reminder Trigger Logic

## Test Framework
- **Framework**: pytest
- **Install**: `pip install pytest`

## Test Files to Create

### tests/test_reminder_checker.py

Tests for the pure `check_user()` function:

```python
"""Unit tests for reminder_checker.check_user() function."""

import pytest
from datetime import datetime, date, timezone, timedelta
from services.reminder_checker import check_user


class TestCheckUserReminderDetection:
    """Tests for reminder_at detection logic."""

    def test_detects_due_reminder(self):
        """Should detect a todo with reminder_at in the past."""
        past_time = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()
        todos = [
            {
                "id": "todo-1",
                "user_id": "user-1",
                "title": "Buy groceries",
                "status": "pending",
                "due_date": None,
                "reminder_at": past_time,
            }
        ]
        existing_notifications = []

        results = check_user("user-1", todos, existing_notifications)

        assert len(results) == 1
        assert results[0] == ("todo-1", "reminder", "Reminder: Buy groceries")

    def test_skips_future_reminder(self):
        """Should not detect a todo with reminder_at in the future."""
        future_time = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
        todos = [
            {
                "id": "todo-1",
                "user_id": "user-1",
                "title": "Buy groceries",
                "status": "pending",
                "due_date": None,
                "reminder_at": future_time,
            }
        ]
        existing_notifications = []

        results = check_user("user-1", todos, existing_notifications)

        assert len(results) == 0

    def test_skips_done_todo_reminder(self):
        """Should not detect reminder for completed todo."""
        past_time = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()
        todos = [
            {
                "id": "todo-1",
                "user_id": "user-1",
                "title": "Buy groceries",
                "status": "done",
                "due_date": None,
                "reminder_at": past_time,
            }
        ]
        existing_notifications = []

        results = check_user("user-1", todos, existing_notifications)

        assert len(results) == 0

    def test_skips_existing_reminder_notification(self):
        """Should not create duplicate reminder notification."""
        past_time = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()
        todos = [
            {
                "id": "todo-1",
                "user_id": "user-1",
                "title": "Buy groceries",
                "status": "pending",
                "due_date": None,
                "reminder_at": past_time,
            }
        ]
        existing_notifications = [
            {
                "id": "notif-1",
                "user_id": "user-1",
                "todo_id": "todo-1",
                "type": "reminder",
                "is_read": False,
            }
        ]

        results = check_user("user-1", todos, existing_notifications)

        assert len(results) == 0

    def test_skips_null_reminder_at(self):
        """Should skip todos with no reminder_at set."""
        todos = [
            {
                "id": "todo-1",
                "user_id": "user-1",
                "title": "Buy groceries",
                "status": "pending",
                "due_date": None,
                "reminder_at": None,
            }
        ]
        existing_notifications = []

        results = check_user("user-1", todos, existing_notifications)

        assert len(results) == 0


class TestCheckUserOverdueDetection:
    """Tests for overdue (due_date) detection logic."""

    def test_detects_overdue_todo(self):
        """Should detect a todo with due_date in the past."""
        past_date = (date.today() - timedelta(days=1)).isoformat()
        todos = [
            {
                "id": "todo-1",
                "user_id": "user-1",
                "title": "Submit report",
                "status": "pending",
                "due_date": past_date,
                "reminder_at": None,
            }
        ]
        existing_notifications = []

        results = check_user("user-1", todos, existing_notifications)

        assert len(results) == 1
        assert results[0] == ("todo-1", "overdue", "Overdue: Submit report")

    def test_skips_future_due_date(self):
        """Should not detect a todo with due_date in the future."""
        future_date = (date.today() + timedelta(days=1)).isoformat()
        todos = [
            {
                "id": "todo-1",
                "user_id": "user-1",
                "title": "Submit report",
                "status": "pending",
                "due_date": future_date,
                "reminder_at": None,
            }
        ]
        existing_notifications = []

        results = check_user("user-1", todos, existing_notifications)

        assert len(results) == 0

    def test_skips_today_due_date(self):
        """Should not detect a todo due today (only strictly past)."""
        today_str = date.today().isoformat()
        todos = [
            {
                "id": "todo-1",
                "user_id": "user-1",
                "title": "Submit report",
                "status": "pending",
                "due_date": today_str,
                "reminder_at": None,
            }
        ]
        existing_notifications = []

        results = check_user("user-1", todos, existing_notifications)

        assert len(results) == 0

    def test_skips_done_todo_overdue(self):
        """Should not detect overdue for completed todo."""
        past_date = (date.today() - timedelta(days=1)).isoformat()
        todos = [
            {
                "id": "todo-1",
                "user_id": "user-1",
                "title": "Submit report",
                "status": "done",
                "due_date": past_date,
                "reminder_at": None,
            }
        ]
        existing_notifications = []

        results = check_user("user-1", todos, existing_notifications)

        assert len(results) == 0

    def test_skips_existing_overdue_notification(self):
        """Should not create duplicate overdue notification."""
        past_date = (date.today() - timedelta(days=1)).isoformat()
        todos = [
            {
                "id": "todo-1",
                "user_id": "user-1",
                "title": "Submit report",
                "status": "pending",
                "due_date": past_date,
                "reminder_at": None,
            }
        ]
        existing_notifications = [
            {
                "id": "notif-1",
                "user_id": "user-1",
                "todo_id": "todo-1",
                "type": "overdue",
                "is_read": False,
            }
        ]

        results = check_user("user-1", todos, existing_notifications)

        assert len(results) == 0


class TestCheckUserCombined:
    """Tests for combined reminder + overdue scenarios."""

    def test_detects_both_reminder_and_overdue(self):
        """Should detect both reminder and overdue for same todo."""
        past_time = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()
        past_date = (date.today() - timedelta(days=1)).isoformat()
        todos = [
            {
                "id": "todo-1",
                "user_id": "user-1",
                "title": "Submit report",
                "status": "pending",
                "due_date": past_date,
                "reminder_at": past_time,
            }
        ]
        existing_notifications = []

        results = check_user("user-1", todos, existing_notifications)

        assert len(results) == 2
        types = {r[1] for r in results}
        assert types == {"reminder", "overdue"}

    def test_multiple_todos_mixed(self):
        """Should handle multiple todos with different states."""
        past_time = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()
        future_time = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
        past_date = (date.today() - timedelta(days=1)).isoformat()

        todos = [
            {"id": "t1", "user_id": "u1", "title": "A", "status": "pending", "due_date": past_date, "reminder_at": None},
            {"id": "t2", "user_id": "u1", "title": "B", "status": "done", "due_date": past_date, "reminder_at": past_time},
            {"id": "t3", "user_id": "u1", "title": "C", "status": "in-progress", "due_date": None, "reminder_at": past_time},
            {"id": "t4", "user_id": "u1", "title": "D", "status": "pending", "due_date": None, "reminder_at": future_time},
        ]
        existing_notifications = []

        results = check_user("u1", todos, existing_notifications)

        # t1: overdue (past due_date, pending)
        # t2: skipped (done)
        # t3: reminder (past reminder_at, in-progress)
        # t4: skipped (future reminder_at)
        assert len(results) == 2
        result_ids = {r[0] for r in results}
        assert result_ids == {"t1", "t3"}

    def test_empty_todos_list(self):
        """Should return empty list for no todos."""
        results = check_user("user-1", [], [])
        assert results == []

    def test_handles_invalid_datetime_gracefully(self):
        """Should skip todos with invalid datetime values."""
        todos = [
            {
                "id": "todo-1",
                "user_id": "user-1",
                "title": "Bad date",
                "status": "pending",
                "due_date": "not-a-date",
                "reminder_at": "not-a-datetime",
            }
        ]
        existing_notifications = []

        results = check_user("user-1", todos, existing_notifications)

        assert len(results) == 0
```

### tests/test_todo_service_reminder.py

Tests for TodoService reminder_at handling:

```python
"""Unit tests for TodoService reminder_at field handling."""

import pytest
import os
import json
import tempfile
from services.todo_service import TodoService
from models import TodoCreate, TodoUpdate
from store import JSONStore
from exceptions import ValidationError


@pytest.fixture
def todo_service(tmp_path):
    """Create a TodoService with a temporary store."""
    store_path = str(tmp_path / "todos.json")
    store = JSONStore(store_path)
    return TodoService(store)


class TestTodoServiceCreateWithReminder:
    """Tests for creating todos with reminder_at."""

    def test_create_with_valid_reminder_at(self, todo_service):
        """Should create todo with valid ISO 8601 reminder_at."""
        data = TodoCreate(title="Test", reminder_at="2026-05-24T09:00:00Z")
        todo = todo_service.create("user-1", data)

        assert todo.reminder_at is not None
        assert "2026-05-24" in str(todo.reminder_at)

    def test_create_without_reminder_at(self, todo_service):
        """Should create todo with reminder_at as None when not provided."""
        data = TodoCreate(title="Test")
        todo = todo_service.create("user-1", data)

        assert todo.reminder_at is None

    def test_create_with_invalid_reminder_at_raises(self, todo_service):
        """Should raise ValidationError for invalid reminder_at format."""
        data = TodoCreate(title="Test", reminder_at="not-a-datetime")

        with pytest.raises(ValidationError):
            todo_service.create("user-1", data)

    def test_create_with_timezone_offset(self, todo_service):
        """Should accept reminder_at with timezone offset."""
        data = TodoCreate(title="Test", reminder_at="2026-05-24T09:00:00+08:00")
        todo = todo_service.create("user-1", data)

        assert todo.reminder_at is not None


class TestTodoServiceUpdateWithReminder:
    """Tests for updating todos with reminder_at."""

    def test_update_sets_reminder_at(self, todo_service):
        """Should update todo with new reminder_at value."""
        create_data = TodoCreate(title="Test")
        todo = todo_service.create("user-1", create_data)

        update_data = TodoUpdate(reminder_at="2026-06-01T10:00:00Z")
        updated = todo_service.update("user-1", todo.id, update_data)

        assert updated.reminder_at is not None
        assert "2026-06-01" in str(updated.reminder_at)

    def test_update_clears_reminder_at_with_null(self, todo_service):
        """Should clear reminder_at when explicitly set to null."""
        create_data = TodoCreate(title="Test", reminder_at="2026-05-24T09:00:00Z")
        todo = todo_service.create("user-1", create_data)

        # Simulate explicit null by using model_fields_set
        update_data = TodoUpdate.model_validate({"reminder_at": None})
        updated = todo_service.update("user-1", todo.id, update_data)

        assert updated.reminder_at is None

    def test_update_invalid_reminder_at_raises(self, todo_service):
        """Should raise ValidationError for invalid reminder_at on update."""
        create_data = TodoCreate(title="Test")
        todo = todo_service.create("user-1", create_data)

        update_data = TodoUpdate(reminder_at="bad-format")

        with pytest.raises(ValidationError):
            todo_service.update("user-1", todo.id, update_data)
```

## Run Unit Tests

### 1. Install Test Dependencies
```bash
pip install pytest
```

### 2. Execute All Unit Tests
```bash
cd backend
python -m pytest tests/ -v
```

### 3. Run Only Unit 2 Tests
```bash
cd backend
python -m pytest tests/test_reminder_checker.py tests/test_todo_service_reminder.py -v
```

### 4. Expected Results
- **test_reminder_checker.py**: 13 tests pass
- **test_todo_service_reminder.py**: 7 tests pass
- **Total**: 20 tests, 0 failures

### 5. Fix Failing Tests
If tests fail:
1. Review test output for assertion errors
2. Check that `reminder_at` field is properly persisted in JSONStore
3. Verify datetime parsing handles both `Z` suffix and `+00:00` offset
4. Rerun tests until all pass
