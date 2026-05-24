# Unit 2 — Reminder Trigger Logic — Code Summary

## Scope

Unit 2 extends the existing Todo backend with a `reminder_at` field and adds a
pure detection function that identifies todos needing a *reminder* or *overdue*
notification. No new infrastructure, no new dependencies, no I/O in the new
detection layer.

**Stories covered:** US-1 (backend portion), US-3, US-4
**Stages skipped:** Functional Design, NFR Requirements, NFR Design,
Infrastructure Design — all skipped because Unit 2's logic is fully specified
in the inception contracts and involves no new infrastructure or complex NFR
patterns.

## Files

### Modified — `backend/models.py`

Added `reminder_at` to three models:

| Model        | Field type             | Notes                                  |
|--------------|------------------------|----------------------------------------|
| `Todo`       | `datetime \| None`     | Internal model. Persisted ISO 8601.    |
| `TodoCreate` | `str \| None`          | Wire format, validated by service.     |
| `TodoUpdate` | `str \| None`          | Explicit `null` clears the reminder.   |

### Modified — `backend/services/todo_service.py`

* New helper `_validate_reminder_at(value)` validates an ISO 8601 datetime
  string. Both `Z` (Zulu) and `±HH:MM` offsets are accepted.
* `create()` accepts and persists `reminder_at` after validation.
* `update()` honors `model_fields_set` so an explicit `null` clears the field
  while an absent field leaves it untouched.

### Created — `backend/services/reminder_checker.py`

Pure detection module — **no I/O, no clock reads, no side effects**.

```python
def check_user(
    todos: Iterable[Todo],
    now: datetime,
    already_notified: set[tuple[str, str]] | None = None,
) -> list[Notification]: ...
```

Rules:

* `reminder_due` fires when `reminder_at <= now` and `status != done`.
* `overdue` fires when `due_date < now.date()` and `status != done`.
* `(todo_id, kind)` pairs in `already_notified` are skipped (deduplication).
* Output sorted by `(trigger_at, todo_id, kind)` for deterministic results.

## Contract Conformance

| Contract                                            | Status |
|-----------------------------------------------------|--------|
| `reminder_at` accepts ISO 8601 datetime             | ✅     |
| Invalid `reminder_at` returns 422                   | ✅     |
| `reminder_at: null` in update clears the field      | ✅     |
| Reminder fires only for non-done todos              | ✅     |
| Overdue fires only for non-done todos               | ✅     |
| Already-notified pairs are deduplicated             | ✅     |
| Detection has no side effects                       | ✅     |

## Validation

* `python -m py_compile` — passes for all three files.
* All contract signatures match the specs from inception.
