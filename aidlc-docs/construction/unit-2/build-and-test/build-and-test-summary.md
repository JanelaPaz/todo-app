# Unit 2 — Build and Test Summary

## Status

| Artifact                            | Status |
|-------------------------------------|--------|
| `models.py` modifications           | ✅     |
| `todo_service.py` modifications     | ✅     |
| `reminder_checker.py` (new)         | ✅     |
| Code summary doc                    | ✅     |
| Build instructions                  | ✅     |
| Unit test instructions (20 tests)   | ✅     |
| Integration test instructions       | ✅     |

## Build

* No new Python dependencies required.
* `python -m py_compile` succeeds for all three modified/created files.
* `from services.reminder_checker import check_user` succeeds.

## Tests

* **Unit:** 20 pytest cases — 12 against `check_user()` and 8 against
  `TodoService.create()`/`update()` `reminder_at` handling. All run without
  network or filesystem dependencies.
* **Integration:** 6 `curl` scenarios covering create, reject, update,
  clear-via-null, and field preservation through the live API.

## Stories satisfied

* **US-1** *(backend portion)* — todos accept and persist `reminder_at`.
* **US-3** — invalid datetimes are rejected with `422`; `null` clears the
  field; untouched field stays put.
* **US-4** — `check_user()` deterministically detects reminder and overdue
  conditions while suppressing already-delivered notifications.

## Risks and follow-ups

* The detection function is pure; the dispatcher that calls it on a schedule
  and persists `already_notified` state is **not** part of Unit 2 — it is the
  responsibility of a later unit (delivery / scheduler).
* Frontend display of `reminder_at` is also out of scope for Unit 2.

## Next units

Unit 2 is complete. You may proceed with Unit 1, Unit 3, or Unit 4.
