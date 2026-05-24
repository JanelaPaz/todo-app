# Code Generation Plan — Unit 3: Notification Bell UI

## Unit Context

**Responsibility**: Bell icon in navbar, unread count badge, dropdown panel with notification list, read/clear actions, 30-second polling.

**Stories Implemented**:
- US-5: View Notifications via Bell Icon
- US-6: View Notification Panel
- US-7: Mark Notification as Read
- US-8: Mark All as Read
- US-9: Clear All Notifications
- US-10: Automatic Polling

**Dependencies**: Unit 1's HTTP API contracts (GET /api/notifications, PATCH /api/notifications/{id}/read, POST /api/notifications/read-all, DELETE /api/notifications)

**Existing Files to Modify**:
- `frontend/types/index.ts` — Add Notification and NotificationsListResponse interfaces
- `frontend/utils/api.ts` — Add notificationsApi object
- `frontend/pages/dashboard.vue` — Add NotificationBell to navbar

**New Files to Create**:
- `frontend/composables/useNotifications.ts` — State management + polling
- `frontend/components/NotificationBell.vue` — Bell icon + badge + panel toggle
- `frontend/components/NotificationPanel.vue` — Dropdown with list and actions

---

## Execution Steps

### Step 1: Add TypeScript Interfaces
- [x] Add `Notification` interface to `frontend/types/index.ts`
- [x] Add `NotificationsListResponse` interface to `frontend/types/index.ts`
- [x] Ensure non-overlapping with existing types (Todo already has reminder_at from Unit 4)

### Step 2: Add Notifications API Client
- [x] Add `notificationsApi` object to `frontend/utils/api.ts`
- [x] Implement `list()` → GET /api/notifications
- [x] Implement `markAsRead(id)` → PATCH /api/notifications/{id}/read
- [x] Implement `markAllAsRead()` → POST /api/notifications/read-all
- [x] Implement `clearAll()` → DELETE /api/notifications
- [x] Import Notification types

### Step 3: Create useNotifications Composable
- [x] Create `frontend/composables/useNotifications.ts`
- [x] Implement reactive state: notifications array, unreadCount, loading, error
- [x] Implement `fetchNotifications()` — calls notificationsApi.list()
- [x] Implement `markAsRead(id)` — optimistic UI update + API call
- [x] Implement `markAllAsRead()` — optimistic UI update + API call
- [x] Implement `clearAll()` — optimistic UI update + API call
- [x] Implement polling: start on call, 30-second interval, stop on cleanup
- [x] Implement `startPolling()` and `stopPolling()` functions
- [x] Use `onUnmounted` or return cleanup function for lifecycle management

### Step 4: Create NotificationPanel Component
- [x] Create `frontend/components/NotificationPanel.vue`
- [x] Display list of notifications with type icon, message, relative time
- [x] Visual distinction between read/unread notifications
- [x] "Mark all as read" button
- [x] "Clear all" button
- [x] Empty state when no notifications
- [x] Add `data-testid` attributes for automation
- [x] Accessible: aria-labels, role attributes

### Step 5: Create NotificationBell Component
- [x] Create `frontend/components/NotificationBell.vue`
- [x] Bell SVG icon button
- [x] Unread count badge (hidden when 0)
- [x] Toggle panel open/close on click
- [x] Close panel on outside click
- [x] Close panel on Escape key
- [x] Integrate useNotifications composable (start/stop polling)
- [x] Add `data-testid` attributes for automation
- [x] Accessible: aria-expanded, aria-haspopup, aria-label

### Step 6: Integrate Bell into Dashboard
- [x] Modify `frontend/pages/dashboard.vue`
- [x] Add `<NotificationBell />` to header right-side actions (before DarkModeToggle)
- [x] No other changes needed (component is self-contained)

### Step 7: Documentation Summary
- [x] Create `aidlc-docs/construction/unit-3/code/code-summary.md`
- [x] Document all files created/modified with descriptions

---

## Acceptance Criteria Verification

After generation, verify:
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
