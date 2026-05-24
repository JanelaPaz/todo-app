# Unit Test Execution

## Run Unit Tests

### 1. Execute All Unit Tests
```bash
cd backend
python -m pytest tests/ -v
```

### 2. Expected Results

#### Unit 1: Notification Backend (test_notification_service.py)
- **Total Tests**: 24
- **Expected**: 24 passed, 0 failures
- **Test Classes**:
  - `TestCreate` (3 tests) — notification creation and persistence
  - `TestExists` (5 tests) — deduplication check by user/todo/type
  - `TestListForUser` (4 tests) — user scoping, sort order, limit
  - `TestGetUnreadCount` (3 tests) — unread counting and scoping
  - `TestMarkRead` (3 tests) — mark read + ownership verification
  - `TestMarkAllRead` (3 tests) — bulk mark read + user isolation
  - `TestDeleteAll` (3 tests) — bulk delete + user isolation

#### Unit 2: Reminder Trigger Logic (test_reminder_checker.py)
- **Total Tests**: 13
- **Test Classes**:
  - `TestCheckUserReminderDetection` (5 tests) — reminder_at detection logic
  - `TestCheckUserOverdueDetection` (5 tests) — overdue (due_date) detection logic
  - `TestCheckUserCombined` (4 tests) — combined reminder + overdue scenarios

#### Unit 2: TodoService Reminder (test_todo_service_reminder.py)
- **Total Tests**: 7
- **Test Classes**:
  - `TestTodoServiceCreateWithReminder` (4 tests) — creating todos with reminder_at
  - `TestTodoServiceUpdateWithReminder` (3 tests) — updating todos with reminder_at

### 3. Run with Coverage (Optional)
```bash
pip install pytest-cov
python -m pytest tests/ -v --cov=services --cov-report=term-missing
```

### 4. Run Only Unit 1 Tests
```bash
cd backend
python -m pytest tests/test_notification_service.py -v
```

### 5. Run Only Unit 2 Tests
```bash
cd backend
python -m pytest tests/test_reminder_checker.py tests/test_todo_service_reminder.py -v
```

### 6. Fix Failing Tests
If tests fail:
1. Review test output for assertion errors
2. Check that `backend/models.py` has NotificationType, Notification models and reminder_at field
3. Check that `backend/services/notification_service.py` exists and imports correctly
4. Check that `backend/services/reminder_checker.py` exists with `check_user()` function
5. Verify `backend/exceptions.py` has NotFoundError class
6. Verify datetime parsing handles both `Z` suffix and `+00:00` offset
7. Rerun tests until all pass
