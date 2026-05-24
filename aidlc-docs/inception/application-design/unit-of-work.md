# Units of Work

## Decomposition: 4 Units for Parallel Development

This feature is decomposed into exactly 4 units of work. Each unit can be developed by an independent engineer. Units communicate through well-defined API contracts (see `unit-of-work-dependency.md`).

---

## Unit 1: Notification Backend

**Responsibility**: Notification data layer and CRUD endpoints. Manages notification storage, retrieval, and state changes.

**Owns**:
- Notification Pydantic model and response models
- NotificationService (CRUD operations)
- NotificationRouter (HTTP endpoints)
- `data/notifications.json` storage file
- Registration of notification router in `main.py`

**Files**:
| File | Action | Description |
|---|---|---|
| `backend/models.py` | Modify | Add Notification, NotificationResponse, NotificationsListResponse, NotificationType enum |
| `backend/services/notification_service.py` | Create | NotificationService class with CRUD methods |
| `backend/routers/notifications.py` | Create | FastAPI router with 4 endpoints; GET endpoint integrates with Unit 2's `reminder_checker.check_user()` to detect and create notifications on each poll |
| `backend/data/notifications.json` | Create | Empty JSON array `[]` |
| `backend/main.py` | Modify | Import and register notifications router |

**API Contracts Exposed** (consumed by Unit 2 and Unit 3):
- `GET /api/notifications` — returns user's notifications + unread_count
- `PATCH /api/notifications/{id}/read` — marks one as read
- `POST /api/notifications/read-all` — marks all as read
- `DELETE /api/notifications` — clears all

**Internal Interface Exposed** (consumed by Unit 2 via import):
- `notification_service.create(user_id, todo_id, notification_type, message) -> Notification`
- `notification_service.exists(user_id, todo_id, notification_type) -> bool`

**Dependencies**: Unit 2 (imports `reminder_checker.check_user()` to detect due notifications during GET /api/notifications; also requires `todo_store` access to read user's todos)

---

## Unit 2: Reminder Trigger Logic

**Responsibility**: Extend Todo model with `reminder_at` field. Implement the logic that detects when reminders are due or todos are overdue, and triggers notification creation.

**Owns**:
- Todo model extension (add `reminder_at` field)
- TodoService modification (accept/persist `reminder_at`)
- ReminderChecker module (pure detection logic)

**Files**:
| File | Action | Description |
|---|---|---|
| `backend/models.py` | Modify | Add `reminder_at: datetime \| None` to Todo, TodoCreate, TodoUpdate |
| `backend/services/todo_service.py` | Modify | Accept reminder_at in create/update, validate format |
| `backend/services/reminder_checker.py` | Create | Pure function `check_user()` for detecting due notifications |

**API Contracts Exposed** (consumed by Unit 4):
- Existing `POST /api/todos` and `PUT /api/todos/{id}` now accept `reminder_at` field
- Existing `GET /api/todos` and `GET /api/todos/{id}` now return `reminder_at` field

**Internal Interface Exposed** (consumed by Unit 1's router):
- `reminder_checker.check_user(user_id, todos, existing_notifications) -> list[tuple[str, str, str]]`

**Dependencies**: Unit 1 (calls `notification_service.create()` from within the GET /api/notifications handler)

**Integration Note**: The `GET /api/notifications` endpoint in Unit 1's router will import and call `reminder_checker.check_user()`. This means Unit 1's router file has a runtime dependency on Unit 2's `reminder_checker` module. The integration point is in `routers/notifications.py`.

---

## Unit 3: Notification Bell UI

**Responsibility**: The bell icon in the navbar, unread count badge, and dropdown panel showing recent notifications with read/clear actions.

**Owns**:
- NotificationBell.vue component
- NotificationPanel.vue component
- useNotifications.ts composable
- Notifications API client functions
- Notification TypeScript interface

**Files**:
| File | Action | Description |
|---|---|---|
| `frontend/components/NotificationBell.vue` | Create | Bell icon + badge + panel toggle |
| `frontend/components/NotificationPanel.vue` | Create | Dropdown with notification list and actions |
| `frontend/composables/useNotifications.ts` | Create | State management + polling logic |
| `frontend/utils/api.ts` | Modify | Add `notificationsApi` object |
| `frontend/types/index.ts` | Modify | Add `Notification` interface |
| `frontend/pages/dashboard.vue` | Modify | Add NotificationBell to navbar |

**Depends On**: Unit 1's API contracts (HTTP endpoints)

**Polling Behavior**:
- Polls `GET /api/notifications` every 30 seconds
- First poll on dashboard mount
- Stops on unmount / logout

---

## Unit 4: Reminder Form Integration

**Responsibility**: Add reminder time input to the todo form. Display reminder time on todo cards. Visual indicator when a todo has an upcoming or overdue reminder.

**Owns**:
- Reminder datetime input in TodoForm
- Reminder display on TodoItem/TodoCard
- ReminderBadge.vue component
- Todo TypeScript interface extension

**Files**:
| File | Action | Description |
|---|---|---|
| `frontend/components/TodoForm.vue` | Modify | Add datetime-local input for reminder_at |
| `frontend/components/TodoItem.vue` | Modify | Display reminder time + ReminderBadge |
| `frontend/components/ReminderBadge.vue` | Create | Visual badge (upcoming/due) |
| `frontend/types/index.ts` | Modify | Add `reminder_at` to Todo interface |
| `frontend/pages/dashboard.vue` | Modify | Pass reminder_at in create form |

**Depends On**: Unit 2's API contracts (Todo model includes `reminder_at` in responses)

---

## Unit Ownership Summary

| File | Unit 1 | Unit 2 | Unit 3 | Unit 4 |
|---|---|---|---|---|
| backend/models.py | Notification models | reminder_at on Todo | — | — |
| backend/services/notification_service.py | ✓ owns | — | — | — |
| backend/services/reminder_checker.py | — | ✓ owns | — | — |
| backend/services/todo_service.py | — | ✓ modifies | — | — |
| backend/routers/notifications.py | ✓ owns | — | — | — |
| backend/main.py | ✓ modifies | — | — | — |
| backend/data/notifications.json | ✓ owns | — | — | — |
| frontend/components/NotificationBell.vue | — | — | ✓ owns | — |
| frontend/components/NotificationPanel.vue | — | — | ✓ owns | — |
| frontend/composables/useNotifications.ts | — | — | ✓ owns | — |
| frontend/components/ReminderBadge.vue | — | — | — | ✓ owns |
| frontend/components/TodoForm.vue | — | — | — | ✓ modifies |
| frontend/components/TodoItem.vue | — | — | — | ✓ modifies |
| frontend/utils/api.ts | — | — | ✓ modifies | — |
| frontend/types/index.ts | — | — | ✓ modifies | ✓ modifies |
| frontend/pages/dashboard.vue | — | — | ✓ modifies | ✓ modifies |

**Shared File Conflict Resolution**:
- `backend/models.py`: Unit 1 adds Notification models; Unit 2 adds reminder_at to Todo. Non-overlapping sections.
- `frontend/types/index.ts`: Unit 3 adds Notification interface; Unit 4 adds reminder_at to Todo. Non-overlapping.
- `frontend/pages/dashboard.vue`: Unit 3 adds bell to navbar; Unit 4 adds reminder_at to create form. Non-overlapping sections.
