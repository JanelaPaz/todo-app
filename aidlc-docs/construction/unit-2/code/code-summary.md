# Code Summary — Unit 2: Reminder Trigger Logic

## Files Modified

### backend/models.py
- Added `reminder_at: datetime | None = None` to `Todo` model
- Added `reminder_at: str | None = None` to `TodoCreate` model
- Added `reminder_at: str | None = None` to `TodoUpdate` model

### backend/services/todo_service.py
- Updated `create()` to accept and persist `reminder_at` from TodoCreate
- Updated `update()` to accept and persist `reminder_at` from TodoUpdate
- Added support for clearing `reminder_at` by explicitly sending `null` (uses `model_fields_set` detection)
- Added `_validate_reminder_at()` method for ISO 8601 datetime validation

## Files Created

### backend/services/reminder_checker.py
- Pure function `check_user(user_id, todos, existing_notifications) -> list[tuple[str, str, str]]`
- Detects todos with `reminder_at <= now` AND status != "done" AND no existing reminder notification
- Detects todos with `due_date < today` AND status != "done" AND no existing overdue notification
- Returns list of `(todo_id, notification_type, message)` tuples
- No I/O, no side effects — fully testable in isolation

## Contract Compliance

| Contract | Status |
|---|---|
| Contract 3: `check_user()` signature matches spec | ✅ Compliant |
| Contract 4: Todo model includes `reminder_at` in responses | ✅ Compliant |
| Contract 4: POST/PUT /api/todos accept `reminder_at` | ✅ Compliant |
| Contract 4: `reminder_at` can be set to null to clear | ✅ Compliant |

## Stories Implemented

| Story | Status |
|---|---|
| US-1 (backend): Accept and persist `reminder_at` | ✅ |
| US-3: `check_user()` detects due reminders | ✅ |
| US-4: `check_user()` detects overdue todos | ✅ |
