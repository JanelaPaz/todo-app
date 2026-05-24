<template>
  <Teleport to="body">
    <Transition
      enter-active-class="transition-opacity duration-200 ease-out"
      leave-active-class="transition-opacity duration-150 ease-in"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div
        v-if="visible && todo"
        class="fixed inset-0 z-50 flex items-center justify-center p-4"
        role="dialog"
        aria-modal="true"
        aria-labelledby="todo-detail-title"
        data-testid="todo-detail-modal"
      >
        <!-- Backdrop -->
        <div
          class="absolute inset-0 bg-black/50 dark:bg-black/70"
          @click="close"
        ></div>

        <!-- Modal panel -->
        <Transition
          enter-active-class="transition-all duration-200 ease-out"
          leave-active-class="transition-all duration-150 ease-in"
          enter-from-class="opacity-0 scale-95"
          enter-to-class="opacity-100 scale-100"
          leave-from-class="opacity-100 scale-100"
          leave-to-class="opacity-0 scale-95"
        >
          <div
            v-if="visible && todo"
            class="relative w-full max-w-lg bg-white dark:bg-secondary-800 rounded-xl shadow-xl overflow-hidden max-h-[90vh] flex flex-col"
          >
            <!-- Header -->
            <div class="flex items-start justify-between p-6 pb-0 flex-shrink-0">
              <div class="flex-1 min-w-0 pr-4">
                <h2
                  id="todo-detail-title"
                  class="text-lg font-semibold text-secondary-900 dark:text-white break-words"
                >
                  {{ isEditing ? 'Edit Todo' : todo.title }}
                </h2>
              </div>
              <button
                type="button"
                class="flex-shrink-0 p-1.5 rounded-lg text-secondary-400 hover:text-secondary-600 hover:bg-secondary-100 dark:hover:text-secondary-300 dark:hover:bg-secondary-700 transition-colors duration-150 focus:outline-none focus:ring-2 focus:ring-primary-500"
                aria-label="Close details"
                data-testid="todo-detail-close-btn"
                @click="close"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            <!-- VIEW MODE -->
            <div v-if="!isEditing" class="p-6 space-y-5 overflow-y-auto">
              <!-- Status and Priority badges -->
              <div class="flex flex-wrap items-center gap-2">
                <span
                  class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium"
                  :class="statusClasses"
                >
                  {{ statusLabel }}
                </span>
                <span
                  class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium"
                  :class="priorityClasses"
                >
                  {{ todo.priority }} priority
                </span>
              </div>

              <!-- Description -->
              <div v-if="todo.description">
                <h3 class="text-xs font-medium uppercase tracking-wider text-secondary-500 dark:text-secondary-400 mb-1.5">
                  Description
                </h3>
                <p class="text-sm text-secondary-700 dark:text-secondary-300 whitespace-pre-wrap">
                  {{ todo.description }}
                </p>
              </div>

              <!-- Details grid -->
              <div class="grid grid-cols-2 gap-4">
                <div v-if="todo.due_date">
                  <h3 class="text-xs font-medium uppercase tracking-wider text-secondary-500 dark:text-secondary-400 mb-1">
                    Due Date
                  </h3>
                  <p class="text-sm font-medium flex items-center gap-1.5" :class="dueDateClasses">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                    {{ formattedDueDate }}
                  </p>
                </div>

                <div v-if="todo.reminder_at">
                  <h3 class="text-xs font-medium uppercase tracking-wider text-secondary-500 dark:text-secondary-400 mb-1">
                    Reminder
                  </h3>
                  <p class="text-sm font-medium text-secondary-700 dark:text-secondary-300 flex items-center gap-1.5">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
                    </svg>
                    {{ formattedReminderAt }}
                  </p>
                </div>

                <div>
                  <h3 class="text-xs font-medium uppercase tracking-wider text-secondary-500 dark:text-secondary-400 mb-1">
                    Created
                  </h3>
                  <p class="text-sm text-secondary-600 dark:text-secondary-400">
                    {{ formattedCreatedAt }}
                  </p>
                </div>

                <div v-if="todo.updated_at">
                  <h3 class="text-xs font-medium uppercase tracking-wider text-secondary-500 dark:text-secondary-400 mb-1">
                    Last Updated
                  </h3>
                  <p class="text-sm text-secondary-600 dark:text-secondary-400">
                    {{ formattedUpdatedAt }}
                  </p>
                </div>
              </div>
            </div>

            <!-- EDIT MODE -->
            <div v-else class="p-6 overflow-y-auto">
              <form @submit.prevent="saveEdit" novalidate class="space-y-4">
                <!-- Title -->
                <div>
                  <label for="edit-title" class="block text-sm font-medium text-secondary-700 dark:text-secondary-300 mb-1.5">
                    Title <span class="text-red-500">*</span>
                  </label>
                  <input
                    id="edit-title"
                    v-model="editForm.title"
                    type="text"
                    class="input-field"
                    placeholder="Todo title"
                    maxlength="200"
                    required
                    data-testid="todo-detail-edit-title"
                  />
                </div>

                <!-- Description -->
                <div>
                  <label for="edit-description" class="block text-sm font-medium text-secondary-700 dark:text-secondary-300 mb-1.5">
                    Description
                  </label>
                  <textarea
                    id="edit-description"
                    v-model="editForm.description"
                    class="input-field resize-none"
                    rows="3"
                    placeholder="Add more details (optional)"
                    maxlength="2000"
                    data-testid="todo-detail-edit-description"
                  ></textarea>
                </div>

                <!-- Priority and Status row -->
                <div class="grid grid-cols-2 gap-4">
                  <div>
                    <label for="edit-priority" class="block text-sm font-medium text-secondary-700 dark:text-secondary-300 mb-1.5">
                      Priority
                    </label>
                    <select
                      id="edit-priority"
                      v-model="editForm.priority"
                      class="input-field"
                      data-testid="todo-detail-edit-priority"
                    >
                      <option value="low">Low</option>
                      <option value="medium">Medium</option>
                      <option value="high">High</option>
                    </select>
                  </div>
                  <div>
                    <label for="edit-status" class="block text-sm font-medium text-secondary-700 dark:text-secondary-300 mb-1.5">
                      Status
                    </label>
                    <select
                      id="edit-status"
                      v-model="editForm.status"
                      class="input-field"
                      data-testid="todo-detail-edit-status"
                    >
                      <option value="pending">Pending</option>
                      <option value="in-progress">In Progress</option>
                      <option value="done">Done</option>
                    </select>
                  </div>
                </div>

                <!-- Due Date and Reminder row -->
                <div class="grid grid-cols-2 gap-4">
                  <div>
                    <label for="edit-due-date" class="block text-sm font-medium text-secondary-700 dark:text-secondary-300 mb-1.5">
                      Due Date
                    </label>
                    <input
                      id="edit-due-date"
                      v-model="editForm.due_date"
                      type="date"
                      class="input-field"
                      data-testid="todo-detail-edit-due-date"
                    />
                  </div>
                  <div>
                    <label for="edit-reminder" class="block text-sm font-medium text-secondary-700 dark:text-secondary-300 mb-1.5">
                      Reminder
                    </label>
                    <input
                      id="edit-reminder"
                      v-model="editForm.reminder_at"
                      type="datetime-local"
                      class="input-field"
                      data-testid="todo-detail-edit-reminder"
                    />
                  </div>
                </div>
              </form>
            </div>

            <!-- Footer actions -->
            <div class="flex items-center justify-end gap-3 px-6 py-4 border-t border-secondary-200 dark:border-secondary-700 bg-secondary-50 dark:bg-secondary-800/50 flex-shrink-0">
              <template v-if="!isEditing">
                <button
                  type="button"
                  class="btn-secondary text-sm"
                  data-testid="todo-detail-delete-btn"
                  @click="$emit('delete', todo)"
                >
                  <svg class="w-4 h-4 mr-1.5 inline-block" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                  Delete
                </button>
                <button
                  type="button"
                  class="btn-primary text-sm"
                  data-testid="todo-detail-edit-btn"
                  @click="startEditing"
                >
                  <svg class="w-4 h-4 mr-1.5 inline-block" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                  </svg>
                  Edit
                </button>
              </template>
              <template v-else>
                <button
                  type="button"
                  class="btn-secondary text-sm"
                  data-testid="todo-detail-cancel-btn"
                  @click="cancelEditing"
                >
                  Cancel
                </button>
                <button
                  type="button"
                  class="btn-primary text-sm"
                  :disabled="saving || !editForm.title.trim()"
                  data-testid="todo-detail-save-btn"
                  @click="saveEdit"
                >
                  <svg
                    v-if="saving"
                    class="animate-spin h-4 w-4 mr-1.5 inline-block text-white"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    aria-hidden="true"
                  >
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  {{ saving ? 'Saving...' : 'Save Changes' }}
                </button>
              </template>
            </div>
          </div>
        </Transition>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import type { Todo, TodoUpdate } from '~/types'

interface Props {
  visible: boolean
  todo: Todo | null
}

const props = defineProps<Props>()

const emit = defineEmits<{
  'update:visible': [value: boolean]
  update: [id: string, data: TodoUpdate]
  delete: [todo: Todo]
}>()

const isEditing = ref(false)
const saving = ref(false)

const editForm = reactive({
  title: '',
  description: '',
  priority: 'medium' as 'low' | 'medium' | 'high',
  status: 'pending' as 'pending' | 'in-progress' | 'done',
  due_date: '',
  reminder_at: '',
})

function startEditing() {
  if (!props.todo) return
  editForm.title = props.todo.title
  editForm.description = props.todo.description || ''
  editForm.priority = props.todo.priority
  editForm.status = props.todo.status
  editForm.due_date = props.todo.due_date || ''
  editForm.reminder_at = props.todo.reminder_at
    ? toDatetimeLocalString(props.todo.reminder_at)
    : ''
  isEditing.value = true
}

function cancelEditing() {
  isEditing.value = false
}

async function saveEdit() {
  if (!props.todo || !editForm.title.trim()) return

  saving.value = true

  const data: TodoUpdate = {
    title: editForm.title.trim(),
    description: editForm.description.trim() || undefined,
    priority: editForm.priority,
    status: editForm.status,
    due_date: editForm.due_date || undefined,
    reminder_at: editForm.reminder_at
      ? new Date(editForm.reminder_at).toISOString()
      : undefined,
  }

  emit('update', props.todo.id, data)

  saving.value = false
  isEditing.value = false
}

function close() {
  isEditing.value = false
  emit('update:visible', false)
}

// Reset edit state when modal is closed or todo changes
watch(() => props.visible, (val) => {
  if (!val) {
    isEditing.value = false
  }
})

// Helper to convert ISO string to datetime-local input value
function toDatetimeLocalString(isoString: string): string {
  const date = new Date(isoString)
  if (isNaN(date.getTime())) return ''
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')
  return `${year}-${month}-${day}T${hours}:${minutes}`
}

// Computed display values for view mode
const statusLabel = computed(() => {
  if (!props.todo) return ''
  switch (props.todo.status) {
    case 'done': return 'Done'
    case 'in-progress': return 'In Progress'
    case 'pending': return 'Pending'
    default: return props.todo.status
  }
})

const statusClasses = computed(() => {
  if (!props.todo) return ''
  switch (props.todo.status) {
    case 'done':
      return 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400'
    case 'in-progress':
      return 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400'
    case 'pending':
      return 'bg-secondary-100 text-secondary-700 dark:bg-secondary-700 dark:text-secondary-300'
    default:
      return 'bg-secondary-100 text-secondary-700 dark:bg-secondary-700 dark:text-secondary-300'
  }
})

const priorityClasses = computed(() => {
  if (!props.todo) return ''
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

const dueDateClasses = computed(() => {
  if (!props.todo?.due_date || props.todo.status === 'done') {
    return 'text-secondary-700 dark:text-secondary-300'
  }
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  const dueDate = new Date(props.todo.due_date + 'T00:00:00')
  if (dueDate < today) {
    return 'text-red-600 dark:text-red-400'
  }
  return 'text-secondary-700 dark:text-secondary-300'
})

const formattedDueDate = computed(() => {
  if (!props.todo?.due_date) return ''
  const date = new Date(props.todo.due_date + 'T00:00:00')
  return date.toLocaleDateString(undefined, { weekday: 'short', month: 'short', day: 'numeric', year: 'numeric' })
})

const formattedReminderAt = computed(() => {
  if (!props.todo?.reminder_at) return ''
  const date = new Date(props.todo.reminder_at)
  if (isNaN(date.getTime())) return ''
  return date.toLocaleString(undefined, {
    weekday: 'short',
    month: 'short',
    day: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
  })
})

const formattedCreatedAt = computed(() => {
  if (!props.todo?.created_at) return ''
  const date = new Date(props.todo.created_at)
  if (isNaN(date.getTime())) return ''
  return date.toLocaleString(undefined, {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
  })
})

const formattedUpdatedAt = computed(() => {
  if (!props.todo?.updated_at) return ''
  const date = new Date(props.todo.updated_at)
  if (isNaN(date.getTime())) return ''
  return date.toLocaleString(undefined, {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
  })
})
</script>
