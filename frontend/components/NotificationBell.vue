<template>
  <div class="relative" ref="bellContainer" data-testid="notification-bell">
    <!-- Bell button -->
    <button
      type="button"
      class="relative p-2 rounded-md text-secondary-500 hover:text-secondary-700 dark:text-secondary-400 dark:hover:text-secondary-200 hover:bg-secondary-100 dark:hover:bg-secondary-700 transition-colors focus:outline-none focus:ring-2 focus:ring-primary-500"
      :aria-expanded="panelOpen"
      aria-haspopup="true"
      aria-label="Notifications"
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
        v-if="panelOpen"
        :notifications="notifications"
        :unread-count="unreadCount"
        @mark-read="handleMarkRead"
        @mark-all-read="handleMarkAllRead"
        @clear-all="handleClearAll"
      />
    </Transition>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useNotifications } from '~/composables/useNotifications'

const bellContainer = ref<HTMLElement | null>(null)
const panelOpen = ref(false)

const {
  notifications,
  unreadCount,
  markAsRead,
  markAllAsRead,
  clearAll,
  startPolling,
  stopPolling,
} = useNotifications()

function togglePanel(): void {
  panelOpen.value = !panelOpen.value
}

function closePanel(): void {
  panelOpen.value = false
}

function handleMarkRead(id: string): void {
  markAsRead(id)
}

function handleMarkAllRead(): void {
  markAllAsRead()
}

function handleClearAll(): void {
  clearAll()
  closePanel()
}

// Close on outside click
function handleOutsideClick(event: MouseEvent): void {
  if (bellContainer.value && !bellContainer.value.contains(event.target as Node)) {
    closePanel()
  }
}

// Close on Escape key
function handleKeydown(event: KeyboardEvent): void {
  if (event.key === 'Escape' && panelOpen.value) {
    closePanel()
  }
}

onMounted(() => {
  startPolling()
  document.addEventListener('click', handleOutsideClick)
  document.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  stopPolling()
  document.removeEventListener('click', handleOutsideClick)
  document.removeEventListener('keydown', handleKeydown)
})
</script>
