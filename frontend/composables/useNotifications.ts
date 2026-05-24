import { ref, readonly } from 'vue'
import { notificationsApi } from '~/utils/api'
import type { Notification } from '~/types'

const POLL_INTERVAL_MS = 30_000

const notifications = ref<Notification[]>([])
const unreadCount = ref(0)
const loading = ref(false)

let pollTimer: ReturnType<typeof setInterval> | null = null

export function useNotifications() {
  async function fetchNotifications(): Promise<void> {
    loading.value = true
    try {
      const response = await notificationsApi.list()
      notifications.value = response.notifications
      unreadCount.value = response.unread_count
    } catch {
      // Silently fail on polling errors — don't disrupt user experience
    } finally {
      loading.value = false
    }
  }

  async function markAsRead(id: string): Promise<void> {
    // Optimistic update
    const notification = notifications.value.find((n) => n.id === id)
    if (notification && !notification.is_read) {
      notification.is_read = true
      unreadCount.value = Math.max(0, unreadCount.value - 1)
    }

    try {
      await notificationsApi.markAsRead(id)
    } catch {
      // Revert on failure
      if (notification) {
        notification.is_read = false
        unreadCount.value += 1
      }
    }
  }

  async function markAllAsRead(): Promise<void> {
    // Optimistic update
    const previousNotifications = notifications.value.map((n) => ({ ...n }))
    const previousUnread = unreadCount.value

    notifications.value.forEach((n) => {
      n.is_read = true
    })
    unreadCount.value = 0

    try {
      await notificationsApi.markAllAsRead()
    } catch {
      // Revert on failure
      notifications.value = previousNotifications
      unreadCount.value = previousUnread
    }
  }

  async function clearAll(): Promise<void> {
    // Optimistic update
    const previousNotifications = [...notifications.value]
    const previousUnread = unreadCount.value

    notifications.value = []
    unreadCount.value = 0

    try {
      await notificationsApi.clearAll()
    } catch {
      // Revert on failure
      notifications.value = previousNotifications
      unreadCount.value = previousUnread
    }
  }

  function startPolling(): void {
    // Fetch immediately
    fetchNotifications()

    // Set up interval
    if (pollTimer === null) {
      pollTimer = setInterval(fetchNotifications, POLL_INTERVAL_MS)
    }
  }

  function stopPolling(): void {
    if (pollTimer !== null) {
      clearInterval(pollTimer)
      pollTimer = null
    }
  }

  return {
    // State (readonly refs for consumers)
    notifications: readonly(notifications),
    unreadCount: readonly(unreadCount),
    loading: readonly(loading),

    // Actions
    fetchNotifications,
    markAsRead,
    markAllAsRead,
    clearAll,
    startPolling,
    stopPolling,
  }
}
