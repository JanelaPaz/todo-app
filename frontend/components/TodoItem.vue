<template>
  <div
    class="group bg-white dark:bg-secondary-800 rounded-lg border border-secondary-200 dark:border-secondary-700 p-4 transition-all duration-200 hover:shadow-md hover:border-primary-300 dark:hover:border-primary-600"
  >
    <div class="flex items-start gap-3">
      <!-- Status checkbox/toggle -->
      <button
        type="button"
        class="mt-0.5 flex-shrink-0 w-5 h-5 rounded-full border-2 transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 dark:focus:ring-offset-secondary-800"
        :class="statusClasses"
        :aria-label="todo.status === 'done' ? 'Mark as pending' : 'Mark as done'"
        @click="toggleStatus"
      >
        <svg
          v-if="todo.status === 'done'"
          class="w-3 h-3 m-auto text-white"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          aria-hidden="true"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" />
        </svg>
      </button>

      <!-- Content area -->
      <div class="flex-1 min-w-0">
        <!-- Title: inline edit mode -->
        <div v-if="isEditingTitle" class="mb-1">
          <input
            ref="titleInputRef"
            v-model="editTitle"
            type="text"
            class="input-field text-sm font-medium"
            maxlength="200"
            aria-label="Edit todo title"
            @keydown.enter="saveTitle"
            @keydown.escape="cancelEditTitle"
            @blur="saveTitle"
          />
        </div>

        <!-- Title: display mode -->
        <button
          v-else
          type="button"
          class="text-left w-full text-sm font-medium transition-colors duration-150 focus:outline-none focus:ring-2 focus:ring-primary-500 rounded px-1 -mx-1"
          :class="[
            todo.status === 'done'
              ? 'text-secondary-400 dark:text-secondary-500 line-through'
              : 'text-secondary-900 dark:text-white hover:text-primary-600 dark:hover:text-primary-400'
          ]"
          :aria-label="`Edit title: ${todo.title}`"
          @click="startEditTitle"
        >
          {{ todo.title }}
        </button>

        <!-- Meta info row -->
        <div class="flex items-center gap-2 mt-1.5 flex-wrap">
          <!-- Priority badge -->
          <span
            class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium transition-colors duration-150"
            :class="priorityClasses"
          >
            {{ todo.priority }}
          </span>

          <!-- Status badge (clickable for inline edit) -->
          <button
            type="button"
            class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium transition-colors duration-150 focus:outline-none focus:ring-2 focus:ring-primary-500"
            :class="statusBadgeClasses"
            :aria-label="`Change status: ${todo.status}`"
            @click="cycleStatus"
          >
            {{ statusLabel }}
          </button>

          <!-- Due date -->
          <span
            v-if="todo.due_date"
            class="inline-flex items-center gap-1 text-xs transition-colors duration-150"
            :class="dueDateClasses"
          >
            <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            {{ formattedDueDate }}
          </span>

          <!-- Reminder time -->
          <span
            v-if="todo.reminder_at"
            class="inline-flex items-center gap-1 text-xs text-secondary-500 dark:text-secondary-400"
          >
            <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
            </svg>
            {{ formattedReminderAt }}
          </span>

          <!-- Reminder badge -->
          <ReminderBadge :reminder-at="todo.reminder_at" :status="todo.status" />
        </div>
      </div>

      <!-- Action buttons -->
      <div class="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
        <!-- Edit button -->
        <button
          type="button"
          class="p-1.5 rounded-lg text-secondary-400 hover:text-primary-600 hover:bg-primary-50 dark:hover:text-primary-400 dark:hover:bg-primary-900/20 transition-colors duration-150 focus:outline-none focus:ring-2 focus:ring-primary-500"
          aria-label="Edit todo"
          @click="$emit('edit', todo)"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
          </svg>
        </button>

        <!-- Delete button -->
        <button
          type="button"
          class="p-1.5 rounded-lg text-secondary-400 hover:text-red-600 hover:bg-red-50 dark:hover:text-red-400 dark:hover:bg-red-900/20 transition-colors duration-150 focus:outline-none focus:ring-2 focus:ring-red-500"
          aria-label="Delete todo"
          @click="$emit('delete', todo)"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Todo } from '~/types'

interface Props {
  todo: Todo
}

const props = defineProps<Props>()

const emit = defineEmits<{
  edit: [todo: Todo]
  delete: [todo: Todo]
  update: [id: string, data: Partial<Todo>]
}>()

// Inline title editing
const isEditingTitle = ref(false)
const editTitle = ref('')
const titleInputRef = ref<HTMLInputElement | null>(null)

function startEditTitle() {
  editTitle.value = props.todo.title
  isEditingTitle.value = true
  nextTick(() => {
    titleInputRef.value?.focus()
    titleInputRef.value?.select()
  })
}

function saveTitle() {
  const trimmed = editTitle.value.trim()
  if (trimmed && trimmed !== props.todo.title) {
    emit('update', props.todo.id, { title: trimmed })
  }
  isEditingTitle.value = false
}

function cancelEditTitle() {
  isEditingTitle.value = false
}

// Status toggling
function toggleStatus() {
  const newStatus = props.todo.status === 'done' ? 'pending' : 'done'
  emit('update', props.todo.id, { status: newStatus })
}

function cycleStatus() {
  const statusOrder: Array<'pending' | 'in-progress' | 'done'> = ['pending', 'in-progress', 'done']
  const currentIndex = statusOrder.indexOf(props.todo.status)
  const nextIndex = (currentIndex + 1) % statusOrder.length
  emit('update', props.todo.id, { status: statusOrder[nextIndex] })
}

// Computed styles
const statusClasses = computed(() => {
  if (props.todo.status === 'done') {
    return 'bg-green-500 border-green-500 hover:bg-green-600 hover:border-green-600'
  }
  if (props.todo.status === 'in-progress') {
    return 'border-primary-400 dark:border-primary-500 hover:border-primary-500 dark:hover:border-primary-400'
  }
  return 'border-secondary-300 dark:border-secondary-600 hover:border-primary-400 dark:hover:border-primary-500'
})

const priorityClasses = computed(() => {
  switch (props.todo.priority) {
    case 'high':
      return 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400'
    case 'medium':
      return 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400'
    case 'low':
      return 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400'
    default:
      return 'bg-secondary-100 text-secondary-700 dark:bg-secondary-700 dark:text-secondary-300'
  }
})

const statusBadgeClasses = computed(() => {
  switch (props.todo.status) {
    case 'done':
      return 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400 hover:bg-green-200 dark:hover:bg-green-900/50'
    case 'in-progress':
      return 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400 hover:bg-blue-200 dark:hover:bg-blue-900/50'
    case 'pending':
      return 'bg-secondary-100 text-secondary-700 dark:bg-secondary-700 dark:text-secondary-300 hover:bg-secondary-200 dark:hover:bg-secondary-600'
    default:
      return 'bg-secondary-100 text-secondary-700 dark:bg-secondary-700 dark:text-secondary-300'
  }
})

const statusLabel = computed(() => {
  switch (props.todo.status) {
    case 'done': return 'Done'
    case 'in-progress': return 'In Progress'
    case 'pending': return 'Pending'
    default: return props.todo.status
  }
})

const dueDateClasses = computed(() => {
  if (!props.todo.due_date || props.todo.status === 'done') {
    return 'text-secondary-500 dark:text-secondary-400'
  }
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  const dueDate = new Date(props.todo.due_date + 'T00:00:00')
  if (dueDate < today) {
    return 'text-red-600 dark:text-red-400'
  }
  return 'text-secondary-500 dark:text-secondary-400'
})

const formattedDueDate = computed(() => {
  if (!props.todo.due_date) return ''
  const date = new Date(props.todo.due_date + 'T00:00:00')
  return date.toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' })
})

const formattedReminderAt = computed(() => {
  if (!props.todo.reminder_at) return ''
  const date = new Date(props.todo.reminder_at)
  if (isNaN(date.getTime())) return ''
  return date.toLocaleString(undefined, {
    month: 'short',
    day: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
  })
})
</script>
