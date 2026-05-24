<template>
  <div class="relative" ref="bellContainer">
    <button
      type="button"
      class="relative p-2 rounded-md text-secondary-500 hover:text-secondary-700 dark:text-secondary-400 dark:hover:text-secondary-200 hover:bg-secondary-100 dark:hover:bg-secondary-700 transition-colors focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-1"
      :aria-label="`Notifications${unreadCount > 0 ? `, ${unreadCount} unread` : ''}`"
      aria-haspopup="true"
      :aria-expanded="isOpen"
      data-testid="notification-bell-button"
      @click="togglePanel"
    >
      <!-- Bell icon -->
      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
      </svg>

      <!-- Unread badge -->
      <span
        v-if="unreadCount > 0"
        class="absolute -top-0.5 -right-0.5 inline-flex items-center justify-center min-w-[18px] h-[18px] px-1 text-[10px] font-bold text-white bg-red-500 rounded-full"
        data-testid="notification-bell-badge"
        aria-hidden="true"
      >
        {{ unreadCount > 99 ? '99+' : unreadCount }}
      </span>
    </button>

    <!-- Panel -->
    <Transition
      enter-active-class="transition-all duration-150 ease-out"
      leave-active-class="transition-all duration-100 ease-in"
      enter-from-class="opacity-0 scale-95"
      enter-to-class="opacity-100 scale-100"
      leave-from-class="opacity-100 scale-100"
      leave-to-class="opacity-0 scale-95"
    >
      <NotificationPanel
        v-if="isOpen"
        :notifications="notifications"
        @mark-as-read="handleMarkAsRead"
        @mark-all-as-read="handleMarkAllAsRead"
        @clear-all="handleClearAll"
      />
    </Transition>
  </div>
</template>

<script setup lang="ts">
import { useNotifications } from '~/composables/useNotifications'

const { notifications, unreadCount, markAsRead, markAllAsRead, clearAll, startPolling, stopPolling } = useNotifications()

const isOpen = ref(false)
const bellContainer = ref<HTMLElement | null>(null)

function togglePanel() {
  isOpen.value = !isOpen.value
}

function closePanel() {
  isOpen.value = false
}

async function handleMarkAsRead(id: string) {
  await markAsRead(id)
}

async function handleMarkAllAsRead() {
  await markAllAsRead()
}

async function handleClearAll() {
  await clearAll()
  closePanel()
}

// Close on outside click
function handleClickOutside(event: MouseEvent) {
  if (bellContainer.value && !bellContainer.value.contains(event.target as Node)) {
    closePanel()
  }
}

// Close on Escape key
function handleKeydown(event: KeyboardEvent) {
  if (event.key === 'Escape' && isOpen.value) {
    closePanel()
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  document.addEventListener('keydown', handleKeydown)
  startPolling()
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  document.removeEventListener('keydown', handleKeydown)
  stopPolling()
})
</script>
