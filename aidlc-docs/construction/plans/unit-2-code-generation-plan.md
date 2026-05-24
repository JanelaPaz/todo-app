# Code Generation Plan — Unit 2: Reminder Trigger Logic

## Unit Context

**Unit**: Unit 2 — Reminder Trigger Logic
**Responsibility**: Extend Todo model with `reminder_at` field. Implement logic that detects when reminders are due or todos are overdue, and triggers notification creation.

**Stories Implemented**:
- US-1 (partial): Backend accepts and persists `reminder_at` in todo create/update
- US-3: `check_user()` detects todos with reminder_at <= now
- US-4: `check_user()` detects todos with due_date < today

**Dependencies**:
- Unit 1 (NotificationService) — Unit 2's `check_user()` is consumed by Unit 1's router. Unit 2 does NOT import Unit 1 code; it only provides the detection logic.

**Files to Modify/Create**:
| File | Action |
|---|---|
| `backend/models.py` | Modify — add `reminder_at` to Todo, TodoCreate, TodoUpdate |
| `backend/services/todo_service.py` | Modify — accept/persist/validate `reminder_at` |
| `backend/services/reminder_checker.py` | Create — pure function `check_user()` |

---

## Execution Steps

### Step 1: Modify backend/models.py — Add reminder_at to Todo models
- [x] Add `reminder_at: datetime | None = None` field to `Todo` model
- [x] Add `reminder_at: str | None = None` field to `TodoCreate` model
- [x] Add `reminder_at: str | None = None` field to `TodoUpdate` model
- [x] Ensure field is optional and defaults to None

### Step 2: Modify backend/services/todo_service.py — Accept and persist reminder_at
- [x] Update `create()` method to accept and persist `reminder_at` from TodoCreate
- [x] Add `_validate_reminder_at()` helper method for ISO 8601 datetime validation
- [x] Call validation in `create()` when `reminder_at` is provided
- [x] Update `update()` method to accept and persist `reminder_at` from TodoUpdate
- [x] Call validation in `update()` when `reminder_at` is provided
- [x] Support setting `reminder_at` to null (clearing the reminder)

### Step 3: Create backend/services/reminder_checker.py — Pure detection logic
- [x] Create module with `check_user()` function
- [x] Implement reminder detection: todos with `reminder_at <= now` AND status != "done" AND no existing reminder notification
- [x] Implement overdue detection: todos with `due_date < today` AND status != "done" AND no existing overdue notification
- [x] Return list of tuples: `[(todo_id, notification_type, message), ...]`
- [x] Ensure function is pure (no I/O, no side effects)

### Step 4: Generate code summary documentation
- [x] Create `aidlc-docs/construction/unit-2/code/code-summary.md` with summary of changes

---

## Acceptance Criteria Verification

After code generation, verify:
- [x] Todo model includes `reminder_at: datetime | None`
- [x] TodoCreate and TodoUpdate accept `reminder_at`
- [x] TodoService validates `reminder_at` format (ISO 8601 datetime)
- [x] `check_user()` correctly identifies due reminders
- [x] `check_user()` correctly identifies overdue todos
- [x] `check_user()` respects deduplication (skips if notification exists)
- [x] `check_user()` skips completed todos (status = done)
- [x] Existing todo endpoints return `reminder_at` in responses
