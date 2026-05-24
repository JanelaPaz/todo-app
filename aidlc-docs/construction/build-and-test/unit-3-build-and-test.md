# Build and Test — Unit 3: Notification Bell UI

## Build Instructions

### Prerequisites
- Node.js 18+ installed
- Frontend dependencies installed (`npm install` in `frontend/`)
- Backend running on `http://localhost:8000` (for integration testing)

### Build Verification

```bash
cd frontend

# TypeScript type check (no emit)
npx tsc --noEmit --project tsconfig.json

# Nuxt build (full production build)
npx nuxi build
```

**Expected**: Zero errors, zero warnings.

**Verified**: TypeScript compilation passes with 0 errors after Unit 3 code generation.

---

## Unit Test Instructions

### Test Scope

Unit 3 is a frontend-only unit. Unit tests should cover:

1. **useNotifications composable** — state management, polling, optimistic updates
2. **NotificationBell component** — rendering, badge visibility, panel toggle
3. **NotificationPanel component** — notification list rendering, actions, empty state
4. **notificationsApi** — API client method signatures and calls

### Test Framework

Use Vitest + Vue Test Utils (standard for Nuxt 3 projects).

### Test Cases — useNotifications.ts

| # | Test Case | Expected Result |
|---|---|---|
| 1 | Initial state | notifications=[], unreadCount=0, loading=false, error=null |
| 2 | fetchNotifications success | Populates notifications and unreadCount from API response |
| 3 | fetchNotifications error | Sets error message, notifications unchanged |
| 4 | markAsRead optimistic | Immediately sets is_read=true, decrements unreadCount |
| 5 | markAsRead revert on failure | Reverts is_read=false, increments unreadCount on API error |
| 6 | markAllAsRead optimistic | All notifications set is_read=true, unreadCount=0 |
| 7 | markAllAsRead revert on failure | Reverts all states on API error |
| 8 | clearAll optimistic | notifications=[], unreadCount=0 |
| 9 | clearAll revert on failure | Restores previous notifications on API error |
| 10 | startPolling | Calls fetchNotifications immediately, then every 30s |
| 11 | stopPolling | Clears interval, no more fetches |
| 12 | onUnmounted cleanup | Stops polling when component unmounts |

### Test Cases — NotificationBell.vue

| # | Test Case | Expected Result |
|---|---|---|
| 1 | Renders bell icon | Bell SVG visible |
| 2 | Badge hidden when unreadCount=0 | No badge element rendered |
| 3 | Badge shows count when unreadCount>0 | Badge displays count |
| 4 | Badge shows "99+" when unreadCount>99 | Badge text is "99+" |
| 5 | Click toggles panel open | Panel component rendered |
| 6 | Click again closes panel | Panel component not rendered |
| 7 | Outside click closes panel | Panel closes |
| 8 | Escape key closes panel | Panel closes |
| 9 | aria-expanded reflects state | true when open, false when closed |
| 10 | Starts polling on mount | fetchNotifications called |

### Test Cases — NotificationPanel.vue

| # | Test Case | Expected Result |
|---|---|---|
| 1 | Empty state when no notifications | Shows "No notifications" message |
| 2 | Renders notification list | Shows all notifications with message and time |
| 3 | Type icon: reminder shows clock | Blue clock icon for type="reminder" |
| 4 | Type icon: overdue shows warning | Red warning icon for type="overdue" |
| 5 | Unread notification styling | Font-medium, darker text |
| 6 | Read notification styling | Opacity reduced |
| 7 | Mark as read button visible for unread | Blue dot button shown |
| 8 | Mark as read emits event | Emits 'mark-read' with notification id |
| 9 | Mark all read button visible | Shown when unread notifications exist |
| 10 | Mark all read emits event | Emits 'mark-all-read' |
| 11 | Clear all emits event | Emits 'clear-all' |
| 12 | Relative time formatting | "Just now", "5m ago", "2h ago", "3d ago" |

---

## Integration Test Instructions

### Prerequisites
- Backend running with Unit 1 (Notification Backend) deployed
- At least one user account with notifications in the system

### Integration Test Scenarios

| # | Scenario | Steps | Expected |
|---|---|---|---|
| 1 | Bell shows unread count | Login → Navigate to dashboard | Bell badge shows correct unread count from API |
| 2 | Panel displays notifications | Click bell | Panel shows notifications matching GET /api/notifications response |
| 3 | Mark single as read | Click read dot on unread notification | Badge decrements, notification visually marked read, PATCH API called |
| 4 | Mark all as read | Click "Mark all read" | Badge goes to 0, all notifications visually read, POST API called |
| 5 | Clear all | Click "Clear all" | Panel shows empty state, badge hidden, DELETE API called |
| 6 | Polling updates | Wait 30+ seconds with new notification created server-side | Badge updates without page refresh |

### Manual Verification Steps

1. **Start backend**: `cd backend && uvicorn main:app --reload --port 8000`
2. **Start frontend**: `cd frontend && npm run dev`
3. **Login** to the app at `http://localhost:3000`
4. **Verify bell icon** appears in the navbar (between dark mode toggle and logout)
5. **Click bell** — panel should open (empty if no notifications yet)
6. **Create a todo with reminder_at in the past** — wait 30s for poll
7. **Verify badge** shows "1" and notification appears in panel
8. **Click the blue dot** — notification marked as read, badge disappears
9. **Press Escape** — panel closes
10. **Click outside** — panel closes

---

## Summary

| Category | Status |
|---|---|
| TypeScript compilation | ✅ Pass (0 errors) |
| Unit tests | 📋 34 test cases defined |
| Integration tests | 📋 6 scenarios defined |
| Manual verification | 📋 10 steps defined |
