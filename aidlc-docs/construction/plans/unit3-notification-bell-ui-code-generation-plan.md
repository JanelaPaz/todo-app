# Code Generation Plan — Unit 3: Notification Bell UI

## Unit Context

**Responsibility**: Bell icon in navbar, unread count badge, dropdown panel showing recent notifications with read/clear actions.

**Stories Implemented**:
- US-5: Bell icon with unread count badge
- US-6: Dropdown panel with notification list
- US-7: Mark individual notification as read (UI + API call)
- US-8: Mark all as read button (UI + API call)
- US-9: Clear all button (UI + API call)
- US-10: 30-second polling via useNotifications composable

**Dependencies**: Unit 1's API contracts (HTTP endpoints — already implemented and tested)

**API Endpoints Consumed**:
- `GET /api/notifications` → `{ notifications: [...], unread_count: N }`
- `PATCH /api/notifications/{id}/read` → updated notification
- `POST /api/notifications/read-all` → `{ message, count }`
- `DELETE /api/notifications` → `{ message, count }`

---

## Code Generation Steps

### Step 1: Add Notification TypeScript Interface
- [x] Modify `frontend/types/index.ts`
- Add `Notification` interface matching backend `NotificationResponse`
- Add `NotificationsListResponse` interface
- Add `NotificationType` type

### Step 2: Add Notifications API Client
- [x] Modify `frontend/utils/api.ts`
- Add `notificationsApi` object with 4 methods: list, markAsRead, markAllAsRead, clearAll
- Follow existing `todosApi` pattern

### Step 3: Create useNotifications Composable
- [x] Create `frontend/composables/useNotifications.ts`
- Reactive state: notifications, unreadCount, loading
- Methods: fetchNotifications, markAsRead, markAllAsRead, clearAll, startPolling, stopPolling
- 30-second polling interval
- Optimistic UI updates

### Step 4: Create NotificationPanel Component
- [x] Create `frontend/components/NotificationPanel.vue`
- Notification list with type icon, message, relative time
- Read/unread visual distinction
- Mark as read on click
- Mark all as read button
- Clear all button
- Empty state when no notifications
- Accessible (aria-labels, keyboard navigation)

### Step 5: Create NotificationBell Component
- [x] Create `frontend/components/NotificationBell.vue`
- Bell icon SVG
- Unread count badge (hidden when 0)
- Click toggles panel open/close
- Close on outside click / Escape key
- data-testid attributes for automation

### Step 6: Integrate NotificationBell into Dashboard
- [x] Modify `frontend/pages/dashboard.vue`
- Add NotificationBell to navbar (right side actions, before DarkModeToggle)
- Import useNotifications, start/stop polling on mount/unmount

### Step 7: Code Summary Documentation
- [x] Create `aidlc-docs/construction/unit3-notification-bell-ui/code/code-summary.md`
- Document all files created/modified
- Document component hierarchy and data flow

---

## Acceptance Criteria Checklist

- [ ] Bell icon visible in navbar
- [ ] Badge shows unread count (hidden when 0)
- [ ] Panel opens on bell click, closes on outside click / Escape
- [ ] Notifications display type icon, message, relative time
- [ ] Read/unread visual distinction
- [ ] Mark as read updates UI optimistically
- [ ] Mark all as read clears badge
- [ ] Clear all empties panel
- [ ] Polling starts on mount, stops on unmount
- [ ] Accessible (aria-labels, keyboard navigation)
- [ ] data-testid attributes on interactive elements
