# Code Summary — Unit 3: Notification Bell UI

## Files Created

| File | Purpose |
|---|---|
| `frontend/composables/useNotifications.ts` | Reactive state management + 30s polling for notifications |
| `frontend/components/NotificationBell.vue` | Bell icon with unread badge, toggles panel, handles outside click/Escape |
| `frontend/components/NotificationPanel.vue` | Dropdown panel with notification list, mark read, mark all, clear all |

## Files Modified

| File | Changes |
|---|---|
| `frontend/types/index.ts` | Added `Notification`, `NotificationsListResponse`, `NotificationType` types |
| `frontend/utils/api.ts` | Added `notificationsApi` object (list, markAsRead, markAllAsRead, clearAll) |
| `frontend/pages/dashboard.vue` | Added `<NotificationBell />` to navbar header |

## Component Hierarchy

```
dashboard.vue
  └── NotificationBell.vue (manages open/close state, polling lifecycle)
        └── NotificationPanel.vue (renders notification list + actions)
```

## Data Flow

1. `NotificationBell` mounts → calls `startPolling()` from `useNotifications`
2. `useNotifications.startPolling()` → immediate `fetchNotifications()` + 30s interval
3. `fetchNotifications()` → `GET /api/notifications` → updates reactive `notifications` + `unreadCount`
4. User clicks bell → `isOpen` toggles → `NotificationPanel` renders
5. User clicks notification → `markAsRead(id)` → optimistic update + `PATCH /api/notifications/{id}/read`
6. User clicks "Mark all read" → `markAllAsRead()` → optimistic update + `POST /api/notifications/read-all`
7. User clicks "Clear all" → `clearAll()` → optimistic update + `DELETE /api/notifications`
8. `NotificationBell` unmounts → calls `stopPolling()` → clears interval

## Accessibility

- Bell button has dynamic `aria-label` including unread count
- `aria-haspopup="true"` and `aria-expanded` on bell button
- Panel has `role="region"` with `aria-label`
- Notification list uses `<ul role="list">` with `<li>` items
- Each notification button has descriptive `aria-label`
- Panel closes on Escape key
- All interactive elements are keyboard-focusable

## Automation Test IDs

- `notification-bell-button` — bell toggle button
- `notification-bell-badge` — unread count badge
- `notification-panel` — dropdown panel container
- `notification-panel-mark-all-read` — mark all as read button
- `notification-panel-clear-all` — clear all button
- `notification-panel-empty` — empty state container
- `notification-item-{id}` — individual notification item
