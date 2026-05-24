# Code Summary — Unit 3: Notification Bell UI

## Files Modified

| File | Change Description |
|---|---|
| `frontend/types/index.ts` | Added `Notification` and `NotificationsListResponse` interfaces |
| `frontend/utils/api.ts` | Added `notificationsApi` object with list, markAsRead, markAllAsRead, clearAll methods |
| `frontend/pages/dashboard.vue` | Added `<NotificationBell />` component to header navbar |

## Files Created

| File | Description |
|---|---|
| `frontend/composables/useNotifications.ts` | State management composable with 30-second polling, optimistic updates, and lifecycle cleanup |
| `frontend/components/NotificationBell.vue` | Bell icon button with unread badge, panel toggle, outside-click/Escape close handling |
| `frontend/components/NotificationPanel.vue` | Dropdown panel with notification list, type icons, relative time, mark-read/clear actions |

## Stories Implemented

| Story | Implementation |
|---|---|
| US-5: View Notifications via Bell Icon | Bell icon with unread count badge in navbar |
| US-6: View Notification Panel | Dropdown panel with notification list, type icons, relative time |
| US-7: Mark Notification as Read | Click dot button on individual notification, optimistic UI update |
| US-8: Mark All as Read | "Mark all read" button in panel header |
| US-9: Clear All Notifications | "Clear all" button in panel header |
| US-10: Automatic Polling | 30-second interval via useNotifications composable, starts on mount, stops on unmount |

## Key Design Decisions

- **Optimistic updates**: All mutation actions (mark read, mark all, clear) update UI immediately and revert on API failure
- **Self-contained component**: NotificationBell manages its own polling lifecycle — no parent coordination needed
- **Accessibility**: aria-expanded, aria-haspopup, aria-label on bell; role="menu" on panel; sr-only text for read buttons
- **Automation**: data-testid attributes on all interactive elements
- **Relative time**: Displays "Just now", "Xm ago", "Xh ago", "Xd ago", or date for older notifications
