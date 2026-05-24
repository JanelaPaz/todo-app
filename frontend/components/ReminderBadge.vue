<template>
  <span
    v-if="badgeState"
    class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-medium"
    :class="badgeClasses"
    :data-testid="'reminder-badge-' + badgeState"
  >
    <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
    </svg>
    {{ badgeLabel }}
  </span>
</template>

<script setup lang="ts">
interface Props {
  reminderAt: string | null
  status: string
}

const props = defineProps<Props>()

const badgeState = computed<'upcoming' | 'due' | null>(() => {
  if (!props.reminderAt || props.status === 'done') {
    return null
  }

  const now = new Date()
  const reminderDate = new Date(props.reminderAt)

  if (isNaN(reminderDate.getTime())) {
    return null
  }

  return reminderDate > now ? 'upcoming' : 'due'
})

const badgeLabel = computed(() => {
  switch (badgeState.value) {
    case 'upcoming':
      return 'Upcoming'
    case 'due':
      return 'Due'
    default:
      return ''
  }
})

const badgeClasses = computed(() => {
  switch (badgeState.value) {
    case 'upcoming':
      return 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400'
    case 'due':
      return 'bg-orange-100 text-orange-700 dark:bg-orange-900/30 dark:text-orange-400'
    default:
      return ''
  }
})
</script>
