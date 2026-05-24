<template>
  <div
    class="bg-white dark:bg-secondary-800 rounded-lg border border-secondary-200 dark:border-secondary-700 p-3 cursor-grab active:cursor-grabbing transition-all duration-200 hover:shadow-md hover:border-primary-300 dark:hover:border-primary-600 select-none"
    :class="{ 'opacity-50 scale-95': isDragging }"
    data-testid="kanban-card"
    :draggable="true"
    @dragstart="handleDragStart"
    @dragend="handleDragEnd"
    @click="$emit('click')"
  >
    <div class="flex items-start gap-2.5">
      <!-- Status checkbox -->
      <button
        type="button"
        class="flex-shrink-0 mt-0.5 w-4 h-4 rounded border-2 flex items-center justify-center transition-colors duration-150 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-1"
        :class="todo.status === 'done'
          ? 'bg-green-500 border-green-500 text-white'
          : 'border-secondary-300 dark:border-secondary-600 hover:border-primary-500'"
        :aria-label="todo.status === 'done' ? 'Mark as pending' : 'Mark as done'"
        @click.stop="$emit('toggle-status')"
      >
        <svg v-if="todo.status === 'done'" class="w-2.5 h-2.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" />
        </svg>
      </button>

      <!-- Content -->
      <div class="flex-1 min-w-0">
        <p
          class="text-sm font-medium truncate"
          :class="todo.status === 'done'
            ? 'text-secondary-400 dark:text-secondary-500 line-through'
            : 'text-secondary-900 dark:text-white'"
        >
          {{ todo.title }}
        </p>

        <!-- Meta row -->
        <div class="flex items-center gap-2 mt-1.5 flex-wrap">
          <!-- Status badge -->
          <span
            class="inline-flex items-center px-1.5 py-0.5 rounded text-[10px] font-medium"
            :class="statusClasses"
          >
            {{ statusLabel }}
          </span>

          <!-- Due date -->
          <span
            v-if="todo.due_date"
            class="text-[10px] flex items-center gap-0.5"
            :class="isOverdue ? 'text-red-600 dark:text-red-400 font-medium' : 'text-secondary-500 dark:text-secondary-400'"
          >
            <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            {{ formattedDueDate }}
          </span>
        </div>
      </div>

      <!-- Drag handle indicator -->
      <div class="flex-shrink-0 text-secondary-300 dark:text-secondary-600 mt-0.5">
        <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
          <path d="M8 6a2 2 0 1 1 0-4 2 2 0 0 1 0 4zm0 8a2 2 0 1 1 0-4 2 2 0 0 1 0 4zm0 8a2 2 0 1 1 0-4 2 2 0 0 1 0 4zm8-16a2 2 0 1 1 0-4 2 2 0 0 1 0 4zm0 8a2 2 0 1 1 0-4 2 2 0 0 1 0 4zm0 8a2 2 0 1 1 0-4 2 2 0 0 1 0 4z" />
        </svg>
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
  click: []
  'toggle-status': []
  dragstart: []
  dragend: []
}>()

const isDragging = ref(false)

function handleDragStart(event: DragEvent) {
  isDragging.value = true
  if (event.dataTransfer) {
    event.dataTransfer.effectAllowed = 'move'
    event.dataTransfer.setData('text/plain', props.todo.id)
  }
  emit('dragstart')
}

function handleDragEnd() {
  isDragging.value = false
  emit('dragend')
}

const statusLabel = computed(() => {
  switch (props.todo.status) {
    case 'done': return 'Done'
    case 'in-progress': return 'In Progress'
    case 'pending': return 'Pending'
    default: return props.todo.status
  }
})

const statusClasses = computed(() => {
  switch (props.todo.status) {
    case 'done':
      return 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400'
    case 'in-progress':
      return 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400'
    case 'pending':
      return 'bg-secondary-100 text-secondary-600 dark:bg-secondary-700 dark:text-secondary-300'
    default:
      return 'bg-secondary-100 text-secondary-600 dark:bg-secondary-700 dark:text-secondary-300'
  }
})

const isOverdue = computed(() => {
  if (!props.todo.due_date || props.todo.status === 'done') return false
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  const dueDate = new Date(props.todo.due_date + 'T00:00:00')
  return dueDate < today
})

const formattedDueDate = computed(() => {
  if (!props.todo.due_date) return ''
  const date = new Date(props.todo.due_date + 'T00:00:00')
  return date.toLocaleDateString(undefined, { month: 'short', day: 'numeric' })
})
</script>
