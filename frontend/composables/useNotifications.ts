import { ref, onUnmounted } from 'vue'
import { notificationsApi } from '~/utils/api'
import type { Notification } from '~/types'

const POLL_INTERVAL_MS = 30000

export function useNotifications() {
  const notifications = ref<Notification[]>([])
  const unreadCount = ref(0)
  const loading = ref(false)
  const error = ref<string | null>(null)

  let pollTimer: ReturnType<typeof setInterval> | null = null

  async function fetchNotifications(): Promise<void> {
    loading.value = true
    error.value = null

    try {
      const response = await notificationsApi.list()
      notifications.value = response.notifications
      unreadCount.value = response.unread_count
    } catch (err: any) {
      error.value = err?.message || 'Failed to fetch notifications'
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
    } catch (err: any) {
      // Revert on failure
      if (notification) {
        notification.is_read = false
        unreadCount.value += 1
      }
      error.value = err?.message || 'Failed to mark notification as read'
    }
  }

  async function markAllAsRead(): Promise<void> {
    // Optimistic update
    const previousStates = notifications.value.map((n) => ({ id: n.id, is_read: n.is_read }))
    const previousUnread = unreadCount.value

    notifications.value.forEach((n) => {
      n.is_read = true
    })
    unreadCount.value = 0

    try {
      await notificationsApi.markAllAsRead()
    } catch (err: any) {
      // Revert on failure
      notifications.value.forEach((n) => {
        const prev = previousStates.find((p) => p.id === n.id)
        if (prev) {
          n.is_read = prev.is_read
        }
      })
      unreadCount.value = previousUnread
      error.value = err?.message || 'Failed to mark all as read'
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
    } catch (err: any) {
      // Revert on failure
      notifications.value = previousNotifications
      unreadCount.value = previousUnread
      error.value = err?.message || 'Failed to clear notifications'
    }
  }

  function startPolling(): void {
    // Fetch immediately on start
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

  // Auto-cleanup on component unmount
  onUnmounted(() => {
    stopPolling()
  })

  return {
    // State
    notifications,
    unreadCount,
    loading,
    error,

    // Actions
    fetchNotifications,
    markAsRead,
    markAllAsRead,
    clearAll,
    startPolling,
    stopPolling,
  }
}
