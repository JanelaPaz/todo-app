# Code Generation Plan — Unit 1: Notification Backend

## Unit Context

**Unit**: Unit 1 — Notification Backend
**Responsibility**: Notification data layer and CRUD endpoints. Manages notification storage, retrieval, and state changes.

**Stories Implemented**:
- US-3: Generate Reminder Notifications (provides `notification_service.create()`)
- US-4: Generate Overdue Notifications (provides `notification_service.create()`)
- US-5: View Notifications via Bell Icon (provides `GET /api/notifications`)
- US-6: View Notification Panel (provides `GET /api/notifications` returning list)
- US-7: Mark Notification as Read (provides `PATCH /api/notifications/{id}/read`)
- US-8: Mark All as Read (provides `POST /api/notifications/read-all`)
- US-9: Clear All Notifications (provides `DELETE /api/notifications`)
- US-10: Automatic Polling (provides `GET /api/notifications` endpoint)

**Dependencies**:
- Unit 2's `reminder_checker.check_user()` (already implemented) — called from GET handler
- `todo_store` access to read user's todos (already exists)

**Files to Modify/Create**:
| File | Action |
|---|---|
| `backend/models.py` | Modify — add Notification, NotificationResponse, NotificationsListResponse, NotificationType enum |
| `backend/services/notification_service.py` | Create — NotificationService class with CRUD methods |
| `backend/routers/notifications.py` | Create — FastAPI router with 4 endpoints |
| `backend/data/notifications.json` | Create — Empty JSON array |
| `backend/main.py` | Modify — Import and register notifications router |

---

## Execution Steps

### Step 1: Modify backend/models.py — Add Notification models
- [x] Add `NotificationType` enum with values "reminder" and "overdue"
- [x] Add `Notification` Pydantic model with fields: id, user_id, todo_id, type, message, is_read, created_at
- [x] Add `NotificationResponse` model (same as Notification, for single-item responses)
- [x] Add `NotificationsListResponse` model with fields: notifications (list), unread_count (int)

### Step 2: Create backend/data/notifications.json — Empty storage file
- [x] Create file with empty JSON array `[]`

### Step 3: Create backend/services/notification_service.py — NotificationService class
- [x] Create `NotificationService` class accepting a `JSONStore` instance
- [x] Implement `create(user_id, todo_id, notification_type, message) -> Notification`
- [x] Implement `exists(user_id, todo_id, notification_type) -> bool`
- [x] Implement `list_for_user(user_id) -> list[Notification]`
- [x] Implement `get_unread_count(user_id) -> int`
- [x] Implement `mark_as_read(user_id, notification_id) -> Notification`
- [x] Implement `mark_all_as_read(user_id) -> int`
- [x] Implement `clear_all(user_id) -> None`

### Step 4: Create backend/routers/notifications.py — FastAPI router with 4 endpoints
- [x] Initialize notification_store (JSONStore) and notification_service
- [x] Initialize todo_store reference
- [x] Implement `GET /api/notifications` with reminder_checker integration
- [x] Implement `PATCH /api/notifications/{notification_id}/read`
- [x] Implement `POST /api/notifications/read-all`
- [x] Implement `DELETE /api/notifications`

### Step 5: Modify backend/main.py — Register notifications router
- [x] Import notifications router
- [x] Add `app.include_router(notifications_router)`
- [x] Add "PATCH" to CORS allow_methods list

### Step 6: Generate code summary documentation
- [x] Create `aidlc-docs/construction/unit-1/code/code-summary.md`

---

## Acceptance Criteria Verification
- [x] Notification CRUD operations work correctly
- [x] Notifications are scoped to authenticated user
- [x] Responses match exact JSON shapes in unit-of-work-dependency.md
- [x] Deduplication check works (exists method)
- [x] Atomic writes to notifications.json
- [x] GET /api/notifications integrates with reminder_checker.check_user()
- [x] PATCH /api/notifications/{id}/read marks single notification
- [x] POST /api/notifications/read-all marks all as read
- [x] DELETE /api/notifications clears all user notifications
- [x] 401 returned for unauthenticated requests
- [x] 404 returned for non-existent or non-owned notifications
