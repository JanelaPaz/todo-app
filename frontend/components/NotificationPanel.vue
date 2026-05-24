<template>
  <div
    class="absolute right-0 top-full mt-2 w-80 sm:w-96 bg-white dark:bg-secondary-800 rounded-lg shadow-xl border border-secondary-200 dark:border-secondary-700 z-50 overflow-hidden"
    role="region"
    aria-label="Notifications panel"
    data-testid="notification-panel"
  >
    <!-- Header -->
    <div class="flex items-center justify-between px-4 py-3 border-b border-secondary-200 dark:border-secondary-700">
      <h2 class="text-sm font-semibold text-secondary-900 dark:text-white">
        Notifications
      </h2>
      <div class="flex items-center gap-2">
        <button
          v-if="notifications.length > 0"
          type="button"
          class="text-xs text-primary-600 dark:text-primary-400 hover:text-primary-700 dark:hover:text-primary-300 font-medium transition-colors"
          data-testid="notification-panel-mark-all-read"
          aria-label="Mark all notifications as read"
          @click="$emit('markAllAsRead')"
        >
          Mark all read
        </button>
        <button
          v-if="notifications.length > 0"
          type="button"
          class="text-xs text-red-600 dark:text-red-400 hover:text-red-700 dark:hover:text-red-300 font-medium transition-colors"
          data-testid="notification-panel-clear-all"
          aria-label="Clear all notifications"
          @click="$emit('clearAll')"
        >
          Clear all
        </button>
      </div>
    </div>

    <!-- Notification List -->
    <div class="max-h-80 overflow-y-auto">
      <!-- Empty state -->
      <div
        v-if="notifications.length === 0"
        class="px-4 py-8 text-center"
        data-testid="notification-panel-empty"
      >
        <svg class="w-10 h-10 mx-auto text-secondary-300 dark:text-secondary-600 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
        </svg>
        <p class="text-sm text-secondary-500 dark:text-secondary-400">No notifications</p>
      </div>

      <!-- Notification items -->
      <ul v-else role="list" aria-label="Notification list">
        <li
          v-for="notification in notifications"
          :key="notification.id"
          class="border-b border-secondary-100 dark:border-secondary-700 last:border-b-0"
        >
          <button
            type="button"
            class="w-full px-4 py-3 flex items-start gap-3 text-left transition-colors hover:bg-secondary-50 dark:hover:bg-secondary-750 focus:outline-none focus:bg-secondary-50 dark:focus:bg-secondary-750"
            :class="notification.is_read ? 'opacity-60' : ''"
            :aria-label="`${notification.is_read ? 'Read' : 'Unread'} notification: ${notification.message}`"
            :data-testid="`notification-item-${notification.id}`"
            @click="$emit('markAsRead', notification.id)"
          >
            <!-- Type icon -->
            <div class="flex-shrink-0 mt-0.5">
              <!-- Reminder icon -->
              <svg
                v-if="notification.type === 'reminder'"
                class="w-5 h-5 text-blue-500 dark:text-blue-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                aria-hidden="true"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <!-- Overdue icon -->
              <svg
                v-else
                class="w-5 h-5 text-red-500 dark:text-red-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                aria-hidden="true"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z" />
              </svg>
            </div>

            <!-- Content -->
            <div class="flex-1 min-w-0">
              <p
                class="text-sm truncate"
                :class="notification.is_read
                  ? 'text-secondary-500 dark:text-secondary-400'
                  : 'text-secondary-900 dark:text-white font-medium'"
              >
                {{ notification.message }}
              </p>
              <p class="text-xs text-secondary-400 dark:text-secondary-500 mt-0.5">
                {{ formatRelativeTime(notification.created_at) }}
              </p>
            </div>

            <!-- Unread indicator -->
            <div
              v-if="!notification.is_read"
              class="flex-shrink-0 w-2 h-2 mt-2 rounded-full bg-primary-500"
              aria-hidden="true"
            ></div>
          </button>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Notification } from '~/types'

defineProps<{
  notifications: Notification[]
}>()

defineEmits<{
  markAsRead: [id: string]
  markAllAsRead: []
  clearAll: []
}>()

function formatRelativeTime(dateStr: string): string {
  const date = new Date(dateStr)
  const now = new Date()
  const diffMs = now.getTime() - date.getTime()
  const diffSeconds = Math.floor(diffMs / 1000)
  const diffMinutes = Math.floor(diffSeconds / 60)
  const diffHours = Math.floor(diffMinutes / 60)
  const diffDays = Math.floor(diffHours / 24)

  if (diffSeconds < 60) return 'Just now'
  if (diffMinutes < 60) return `${diffMinutes}m ago`
  if (diffHours < 24) return `${diffHours}h ago`
  if (diffDays < 7) return `${diffDays}d ago`

  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
}
</script>
