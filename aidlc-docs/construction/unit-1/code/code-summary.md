# Code Summary — Unit 1: Notification Backend

## Generated/Modified Files

| File | Action | Description |
|---|---|---|
| `backend/models.py` | Modified | Added NotificationType enum, Notification, NotificationResponse, NotificationsListResponse models |
| `backend/data/notifications.json` | Created | Empty JSON array for notification persistence |
| `backend/services/notification_service.py` | Created | Full CRUD service: create, exists, list_for_user, get_unread_count, mark_as_read, mark_all_as_read, clear_all |
| `backend/routers/notifications.py` | Created | FastAPI router with 4 endpoints + reminder_checker integration |
| `backend/main.py` | Modified | Registered notifications router, added PATCH to CORS methods |

## API Endpoints Implemented

| Method | Path | Description |
|---|---|---|
| GET | `/api/notifications` | List notifications + auto-detect new via reminder_checker |
| PATCH | `/api/notifications/{id}/read` | Mark single notification as read |
| POST | `/api/notifications/read-all` | Mark all notifications as read |
| DELETE | `/api/notifications` | Clear all user notifications |

## Internal Interfaces Exposed

- `NotificationService.create(user_id, todo_id, notification_type, message) -> Notification`
- `NotificationService.exists(user_id, todo_id, notification_type) -> bool`

## Integration Points

- **GET /api/notifications** calls `reminder_checker.check_user()` (Unit 2) on each poll to detect and auto-create notifications for due reminders and overdue todos
- Uses same `JSONStore` pattern as existing services
- Authentication via `get_current_user` dependency (httpOnly cookie JWT)
- All notifications scoped to authenticated user (ownership enforced)

## Key Design Decisions

- **Deduplication**: `exists()` method prevents duplicate notifications for the same (user_id, todo_id, type) combination
- **Lazy detection**: Notifications are created on-demand during GET polling, not via background scheduler
- **Atomic writes**: Uses JSONStore's atomic write mechanism (temp file + os.replace)
- **Max 20 results**: List endpoint caps at 20 most recent notifications
- **Unread count**: Computed across ALL user notifications (not just the 20 returned)
