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
        v-if="visible"
        class="fixed inset-0 z-50 flex items-center justify-center p-4"
        role="dialog"
        aria-modal="true"
        :aria-labelledby="formTitleId"
      >
        <!-- Backdrop -->
        <div
          class="absolute inset-0 bg-black/50 dark:bg-black/70"
          @click="handleCancel"
        ></div>

        <!-- Dialog panel -->
        <Transition
          enter-active-class="transition-all duration-200 ease-out"
          leave-active-class="transition-all duration-150 ease-in"
          enter-from-class="opacity-0 scale-95"
          enter-to-class="opacity-100 scale-100"
          leave-from-class="opacity-100 scale-100"
          leave-to-class="opacity-0 scale-95"
        >
          <div
            v-if="visible"
            class="relative w-full max-w-lg bg-white dark:bg-secondary-800 rounded-xl shadow-xl p-6 max-h-[90vh] overflow-y-auto"
          >
            <!-- Header -->
            <div class="flex items-center justify-between mb-6">
              <h2
                :id="formTitleId"
                class="text-xl font-semibold text-secondary-900 dark:text-white"
              >
                {{ isEditing ? 'Edit Todo' : 'Create Todo' }}
              </h2>
              <button
                type="button"
                class="text-secondary-400 hover:text-secondary-600 dark:hover:text-secondary-300 transition-colors duration-200"
                aria-label="Close"
                @click="handleCancel"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            <!-- Form -->
            <form @submit.prevent="handleSubmit" novalidate>
              <!-- Title field -->
              <div class="mb-4">
                <label for="todo-title" class="block text-sm font-medium text-secondary-700 dark:text-secondary-300 mb-1.5">
                  Title <span class="text-red-500">*</span>
                </label>
                <input
                  id="todo-title"
                  v-model="form.title"
                  type="text"
                  class="input-field"
                  :class="{ 'border-red-500 focus:ring-red-500 focus:border-red-500': errors.title }"
                  placeholder="What needs to be done?"
                  maxlength="200"
                  :disabled="submitting"
                />
                <p v-if="errors.title" class="mt-1.5 text-sm text-red-600 dark:text-red-400" role="alert">
                  {{ errors.title }}
                </p>
              </div>

              <!-- Description field -->
              <div class="mb-4">
                <label for="todo-description" class="block text-sm font-medium text-secondary-700 dark:text-secondary-300 mb-1.5">
                  Description
                </label>
                <textarea
                  id="todo-description"
                  v-model="form.description"
                  class="input-field resize-none"
                  :class="{ 'border-red-500 focus:ring-red-500 focus:border-red-500': errors.description }"
                  placeholder="Add more details (optional)"
                  rows="3"
                  maxlength="2000"
                  :disabled="submitting"
                ></textarea>
                <p v-if="errors.description" class="mt-1.5 text-sm text-red-600 dark:text-red-400" role="alert">
                  {{ errors.description }}
                </p>
              </div>

              <!-- Priority and Status row -->
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
                <!-- Priority field -->
                <div>
                  <label for="todo-priority" class="block text-sm font-medium text-secondary-700 dark:text-secondary-300 mb-1.5">
                    Priority
                  </label>
                  <select
                    id="todo-priority"
                    v-model="form.priority"
                    class="input-field"
                    :disabled="submitting"
                  >
                    <option value="low">Low</option>
                    <option value="medium">Medium</option>
                    <option value="high">High</option>
                  </select>
                </div>

                <!-- Status field -->
                <div>
                  <label for="todo-status" class="block text-sm font-medium text-secondary-700 dark:text-secondary-300 mb-1.5">
                    Status
                  </label>
                  <select
                    id="todo-status"
                    v-model="form.status"
                    class="input-field"
                    :disabled="submitting"
                  >
                    <option value="pending">Pending</option>
                    <option value="in-progress">In Progress</option>
                    <option value="done">Done</option>
                  </select>
                </div>
              </div>

              <!-- Due date field -->
              <div class="mb-4">
                <label for="todo-due-date" class="block text-sm font-medium text-secondary-700 dark:text-secondary-300 mb-1.5">
                  Due Date
                </label>
                <input
                  id="todo-due-date"
                  v-model="form.due_date"
                  type="date"
                  class="input-field"
                  :class="{ 'border-red-500 focus:ring-red-500 focus:border-red-500': errors.due_date }"
                  :disabled="submitting"
                />
                <p v-if="errors.due_date" class="mt-1.5 text-sm text-red-600 dark:text-red-400" role="alert">
                  {{ errors.due_date }}
                </p>
              </div>

              <!-- Reminder field -->
              <div class="mb-6">
                <label for="todo-reminder" class="block text-sm font-medium text-secondary-700 dark:text-secondary-300 mb-1.5">
                  Reminder
                </label>
                <input
                  id="todo-reminder"
                  v-model="form.reminder_at"
                  type="datetime-local"
                  class="input-field"
                  :disabled="submitting"
                  data-testid="todo-form-reminder-input"
                />
                <p class="mt-1 text-xs text-secondary-500 dark:text-secondary-400">
                  Set a date and time to be reminded about this todo
                </p>
              </div>

              <!-- General error -->
              <div
                v-if="errors.general"
                class="mb-4 p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg"
                role="alert"
              >
                <p class="text-sm text-red-700 dark:text-red-400">{{ errors.general }}</p>
              </div>

              <!-- Actions -->
              <div class="flex gap-3 justify-end">
                <button
                  type="button"
                  class="btn-secondary"
                  :disabled="submitting"
                  @click="handleCancel"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  class="btn-primary flex items-center gap-2"
                  :disabled="submitting"
                >
                  <svg
                    v-if="submitting"
                    class="animate-spin h-4 w-4 text-white"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    aria-hidden="true"
                  >
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  <span>{{ submitting ? 'Saving...' : (isEditing ? 'Save Changes' : 'Create Todo') }}</span>
                </button>
              </div>
            </form>
          </div>
        </Transition>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { reactive, watch, computed } from 'vue'
import type { Todo, TodoCreate, TodoUpdate } from '~/types'

interface Props {
  visible: boolean
  todo?: Todo | null
}

const props = withDefaults(defineProps<Props>(), {
  todo: null,
})

const emit = defineEmits<{
  submit: [data: TodoCreate | TodoUpdate]
  cancel: []
  'update:visible': [value: boolean]
}>()

const formTitleId = useId()

const isEditing = computed(() => !!props.todo)

const form = reactive({
  title: '',
  description: '',
  priority: 'medium' as 'low' | 'medium' | 'high',
  due_date: '',
  status: 'pending' as 'pending' | 'in-progress' | 'done',
  reminder_at: '',
})

const errors = reactive({
  title: '',
  description: '',
  due_date: '',
  general: '',
})

const submitting = ref(false)

// Watch for visibility changes to reset or populate form
watch(() => props.visible, (newVal) => {
  if (newVal) {
    clearErrors()
    if (props.todo) {
      // Pre-populate with current values for editing
      form.title = props.todo.title
      form.description = props.todo.description ?? ''
      form.priority = props.todo.priority
      form.due_date = props.todo.due_date ?? ''
      form.status = props.todo.status
      form.reminder_at = props.todo.reminder_at ? toLocalDatetimeString(props.todo.reminder_at) : ''
    } else {
      // Reset to defaults for creating
      form.title = ''
      form.description = ''
      form.priority = 'medium'
      form.due_date = ''
      form.status = 'pending'
      form.reminder_at = ''
    }
  }
})

// Also watch for todo prop changes while visible
watch(() => props.todo, (newTodo) => {
  if (props.visible && newTodo) {
    form.title = newTodo.title
    form.description = newTodo.description ?? ''
    form.priority = newTodo.priority
    form.due_date = newTodo.due_date ?? ''
    form.status = newTodo.status
    form.reminder_at = newTodo.reminder_at ? toLocalDatetimeString(newTodo.reminder_at) : ''
  }
})

function clearErrors() {
  errors.title = ''
  errors.description = ''
  errors.due_date = ''
  errors.general = ''
}

function validate(): boolean {
  clearErrors()
  let valid = true

  // Title validation: required, not whitespace-only, max 200 chars
  const trimmedTitle = form.title.trim()
  if (!trimmedTitle) {
    errors.title = 'Title is required'
    valid = false
  } else if (trimmedTitle.length > 200) {
    errors.title = 'Title must be 200 characters or less'
    valid = false
  }

  // Description validation: max 2000 chars
  if (form.description && form.description.length > 2000) {
    errors.description = 'Description must be 2000 characters or less'
    valid = false
  }

  // Due date validation: must be valid YYYY-MM-DD if provided
  if (form.due_date) {
    const dateRegex = /^\d{4}-\d{2}-\d{2}$/
    if (!dateRegex.test(form.due_date)) {
      errors.due_date = 'Due date must be in YYYY-MM-DD format'
      valid = false
    } else {
      // Check if it's a valid date
      const date = new Date(form.due_date + 'T00:00:00')
      if (isNaN(date.getTime())) {
        errors.due_date = 'Please enter a valid date'
        valid = false
      }
    }
  }

  return valid
}

function handleSubmit() {
  if (!validate()) return

  submitting.value = true

  if (isEditing.value) {
    // For editing, only send changed fields
    const data: TodoUpdate = {}
    const todo = props.todo!

    if (form.title.trim() !== todo.title) {
      data.title = form.title.trim()
    }

    const newDescription = form.description.trim() || null
    if (newDescription !== (todo.description ?? null)) {
      data.description = newDescription
    }

    if (form.priority !== todo.priority) {
      data.priority = form.priority
    }

    const newDueDate = form.due_date || null
    if (newDueDate !== (todo.due_date ?? null)) {
      data.due_date = newDueDate
    }

    if (form.status !== todo.status) {
      data.status = form.status
    }

    // Handle reminder_at: convert local datetime to ISO 8601 UTC
    const newReminderAt = form.reminder_at ? toISOString(form.reminder_at) : null
    const existingReminderAt = todo.reminder_at ?? null
    if (newReminderAt !== existingReminderAt) {
      data.reminder_at = newReminderAt
    }

    emit('submit', data)
  } else {
    // For creating, send all fields
    const data: TodoCreate = {
      title: form.title.trim(),
      priority: form.priority,
      status: form.status,
    }

    const description = form.description.trim()
    if (description) {
      data.description = description
    }

    if (form.due_date) {
      data.due_date = form.due_date
    }

    if (form.reminder_at) {
      data.reminder_at = toISOString(form.reminder_at)
    }

    emit('submit', data)
  }

  submitting.value = false
}

function handleCancel() {
  emit('cancel')
  emit('update:visible', false)
}

// Expose setError for parent components to set server-side errors
function setError(field: 'title' | 'description' | 'due_date' | 'general', message: string) {
  errors[field] = message
}

function setSubmitting(value: boolean) {
  submitting.value = value
}

defineExpose({
  setError,
  setSubmitting,
})

/**
 * Convert an ISO 8601 datetime string to a local datetime-local input value.
 * e.g., "2026-05-24T09:00:00Z" → "2026-05-24T17:00" (in UTC+8)
 */
function toLocalDatetimeString(isoString: string): string {
  const date = new Date(isoString)
  if (isNaN(date.getTime())) return ''
  // Format as YYYY-MM-DDTHH:mm for datetime-local input
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')
  return `${year}-${month}-${day}T${hours}:${minutes}`
}

/**
 * Convert a datetime-local input value to an ISO 8601 UTC string.
 * e.g., "2026-05-24T09:00" → "2026-05-24T01:00:00.000Z" (from UTC+8)
 */
function toISOString(localDatetime: string): string {
  const date = new Date(localDatetime)
  if (isNaN(date.getTime())) return ''
  return date.toISOString()
}
</script>
