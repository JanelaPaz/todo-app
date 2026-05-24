<template>
  <div class="min-h-screen bg-secondary-50 dark:bg-secondary-900 transition-colors duration-200">
    <!-- Header -->
    <header class="bg-white dark:bg-secondary-800 border-b border-secondary-200 dark:border-secondary-700 sticky top-0 z-10">
      <div class="max-w-7xl mx-auto px-4 md:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">
          <!-- Logo / Title -->
          <div class="flex items-center gap-3">
            <svg class="w-8 h-8 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
            </svg>
            <h1 class="text-xl font-bold text-secondary-900 dark:text-white">Todo Dashboard</h1>
          </div>

          <!-- Right side actions -->
          <div class="flex items-center gap-2">
            <NotificationBell />
            <DarkModeToggle />
            <button
              type="button"
              class="btn-secondary text-sm flex items-center gap-1.5"
              @click="handleLogout"
              :disabled="loggingOut"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
              <span class="hidden sm:inline">Logout</span>
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- Main content -->
    <main class="max-w-7xl mx-auto px-4 md:px-6 lg:px-8 py-6">
      <!-- Stats Cards -->
      <section aria-label="Todo statistics" class="mb-6">
        <LoadingSkeleton v-if="loading && !stats" variant="stats" aria-label="Loading statistics" />
        <StatsCards v-else :stats="stats" />
      </section>

      <!-- Filter Bar -->
      <section aria-label="Filters and sorting" class="mb-6">
        <div class="bg-white dark:bg-secondary-800 rounded-lg p-4 border border-secondary-200 dark:border-secondary-700">
          <FilterBar
            :status-filter="statusFilter"
            :priority-filter="priorityFilter"
            :sort-by="sortBy"
            @update:status-filter="handleStatusFilter"
            @update:priority-filter="handlePriorityFilter"
            @update:sort-by="handleSortBy"
          />
        </div>
      </section>

      <!-- Todo List -->
      <section aria-label="Todo list">
        <!-- Loading state -->
        <LoadingSkeleton v-if="loading && todos.length === 0" variant="card" :count="5" aria-label="Loading todos" />

        <!-- Empty state -->
        <EmptyState
          v-else-if="!loading && todos.length === 0"
          title="No todos yet"
          description="Get started by creating your first todo. Stay organized and track your tasks effortlessly."
          action-text="Create Todo"
          @action="showCreateForm = true"
        />

        <!-- Todo items -->
        <div v-else class="space-y-3">
          <TransitionGroup
            enter-active-class="transition-all duration-200 ease-out"
            leave-active-class="transition-all duration-200 ease-in"
            enter-from-class="opacity-0 translate-y-2"
            enter-to-class="opacity-100 translate-y-0"
            leave-from-class="opacity-100 translate-y-0"
            leave-to-class="opacity-0 translate-y-2"
          >
            <div
              v-for="todo in todos"
              :key="todo.id"
              class="bg-white dark:bg-secondary-800 rounded-lg p-4 border border-secondary-200 dark:border-secondary-700 transition-colors duration-200 hover:border-primary-300 dark:hover:border-primary-700"
            >
              <div class="flex items-start gap-3">
                <!-- Status checkbox -->
                <button
                  type="button"
                  class="flex-shrink-0 mt-0.5 w-5 h-5 rounded border-2 flex items-center justify-center transition-colors duration-150 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-1"
                  :class="todo.status === 'done'
                    ? 'bg-green-500 border-green-500 text-white'
                    : 'border-secondary-300 dark:border-secondary-600 hover:border-primary-500'"
                  :aria-label="todo.status === 'done' ? 'Mark as pending' : 'Mark as done'"
                  @click="toggleTodoStatus(todo)"
                >
                  <svg v-if="todo.status === 'done'" class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" />
                  </svg>
                </button>

                <!-- Todo content -->
                <div class="flex-1 min-w-0">
                  <p
                    class="text-sm font-medium transition-colors duration-150"
                    :class="todo.status === 'done'
                      ? 'text-secondary-400 dark:text-secondary-500 line-through'
                      : 'text-secondary-900 dark:text-white'"
                  >
                    {{ todo.title }}
                  </p>
                  <p v-if="todo.description" class="mt-1 text-xs text-secondary-500 dark:text-secondary-400 truncate">
                    {{ todo.description }}
                  </p>
                  <div class="mt-2 flex flex-wrap items-center gap-2">
                    <!-- Priority badge -->
                    <span
                      class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium"
                      :class="priorityClasses(todo.priority)"
                    >
                      {{ todo.priority }}
                    </span>
                    <!-- Status badge -->
                    <span
                      class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium"
                      :class="statusClasses(todo.status)"
                    >
                      {{ formatStatus(todo.status) }}
                    </span>
                    <!-- Due date -->
                    <span
                      v-if="todo.due_date"
                      class="text-xs"
                      :class="isOverdue(todo) ? 'text-red-600 dark:text-red-400 font-medium' : 'text-secondary-500 dark:text-secondary-400'"
                    >
                      Due: {{ formatDate(todo.due_date) }}
                    </span>
                    <!-- Reminder badge -->
                    <ReminderBadge :reminder-at="todo.reminder_at" :status="todo.status" />
                  </div>
                </div>

                <!-- Actions -->
                <div class="flex-shrink-0 flex items-center gap-1">
                  <button
                    type="button"
                    class="p-1.5 rounded-md text-secondary-400 hover:text-primary-600 hover:bg-secondary-100 dark:hover:text-primary-400 dark:hover:bg-secondary-700 transition-colors duration-150 focus:outline-none focus:ring-2 focus:ring-primary-500"
                    aria-label="Delete todo"
                    @click="confirmDelete(todo)"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </TransitionGroup>
        </div>
      </section>

      <!-- Floating create button -->
      <button
        type="button"
        class="fixed bottom-6 right-6 w-14 h-14 bg-primary-600 hover:bg-primary-700 text-white rounded-full shadow-lg flex items-center justify-center transition-all duration-200 hover:scale-105 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2"
        aria-label="Create new todo"
        @click="showCreateForm = true"
      >
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
      </button>
    </main>

    <!-- Create Todo Modal -->
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
          v-if="showCreateForm"
          class="fixed inset-0 z-50 flex items-center justify-center p-4"
          role="dialog"
          aria-modal="true"
          aria-labelledby="create-todo-title"
        >
          <!-- Backdrop -->
          <div class="absolute inset-0 bg-black/50 dark:bg-black/70" @click="showCreateForm = false"></div>

          <!-- Modal panel -->
          <div class="relative w-full max-w-md bg-white dark:bg-secondary-800 rounded-xl shadow-xl p-6">
            <h2 id="create-todo-title" class="text-lg font-semibold text-secondary-900 dark:text-white mb-4">
              Create New Todo
            </h2>

            <form @submit.prevent="handleCreateTodo" novalidate>
              <!-- Title -->
              <div class="mb-4">
                <label for="todo-title" class="block text-sm font-medium text-secondary-700 dark:text-secondary-300 mb-1.5">
                  Title <span class="text-red-500">*</span>
                </label>
                <input
                  id="todo-title"
                  v-model="createForm.title"
                  type="text"
                  class="input-field"
                  placeholder="What needs to be done?"
                  maxlength="200"
                  required
                />
              </div>

              <!-- Description -->
              <div class="mb-4">
                <label for="todo-description" class="block text-sm font-medium text-secondary-700 dark:text-secondary-300 mb-1.5">
                  Description
                </label>
                <textarea
                  id="todo-description"
                  v-model="createForm.description"
                  class="input-field resize-none"
                  rows="3"
                  placeholder="Add more details (optional)"
                  maxlength="2000"
                ></textarea>
              </div>

              <!-- Priority and Due Date row -->
              <div class="grid grid-cols-2 gap-4 mb-4">
                <div>
                  <label for="todo-priority" class="block text-sm font-medium text-secondary-700 dark:text-secondary-300 mb-1.5">
                    Priority
                  </label>
                  <select id="todo-priority" v-model="createForm.priority" class="input-field">
                    <option value="low">Low</option>
                    <option value="medium">Medium</option>
                    <option value="high">High</option>
                  </select>
                </div>
                <div>
                  <label for="todo-due-date" class="block text-sm font-medium text-secondary-700 dark:text-secondary-300 mb-1.5">
                    Due Date
                  </label>
                  <input
                    id="todo-due-date"
                    v-model="createForm.due_date"
                    type="date"
                    class="input-field"
                  />
                </div>
              </div>

              <!-- Reminder field -->
              <div class="mb-4">
                <label for="todo-reminder-at" class="block text-sm font-medium text-secondary-700 dark:text-secondary-300 mb-1.5">
                  Reminder
                </label>
                <input
                  id="todo-reminder-at"
                  v-model="createForm.reminder_at"
                  type="datetime-local"
                  class="input-field"
                  data-testid="dashboard-create-reminder-input"
                />
                <p class="mt-1 text-xs text-secondary-500 dark:text-secondary-400">
                  Set a date and time to be reminded
                </p>
              </div>

              <!-- Actions -->
              <div class="flex gap-3 justify-end mt-6">
                <button
                  type="button"
                  class="btn-secondary"
                  @click="showCreateForm = false"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  class="btn-primary flex items-center gap-2"
                  :disabled="creating"
                >
                  <svg
                    v-if="creating"
                    class="animate-spin h-4 w-4 text-white"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    aria-hidden="true"
                  >
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  <span>{{ creating ? 'Creating...' : 'Create Todo' }}</span>
                </button>
              </div>
            </form>
          </div>
        </div>
      </Transition>
    </Teleport>

    <!-- Delete Confirmation Dialog -->
    <ConfirmDialog
      :visible="showDeleteConfirm"
      title="Delete Todo"
      message="Are you sure you want to delete this todo? This action cannot be undone."
      confirm-text="Delete"
      cancel-text="Cancel"
      variant="danger"
      @confirm="handleDeleteTodo"
      @cancel="showDeleteConfirm = false"
      @update:visible="showDeleteConfirm = $event"
    />

  </div>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import { useTodos } from '~/composables/useTodos'
import { useAuth } from '~/composables/useAuth'
import { useToast } from '~/composables/useToast'
import type { Todo, TodoCreate } from '~/types'

definePageMeta({
  layout: false,
})

const router = useRouter()
const { logout } = useAuth()
const { success: toastSuccess, error: toastError } = useToast()
const {
  todos,
  stats,
  loading,
  error: todosError,
  fetchTodos,
  fetchStats,
  createTodo,
  updateTodo,
  deleteTodo,
  setFilter,
  setSortBy,
} = useTodos()

// Local state
const showCreateForm = ref(false)
const showDeleteConfirm = ref(false)
const todoToDelete = ref<Todo | null>(null)
const creating = ref(false)
const loggingOut = ref(false)

const statusFilter = ref<string | undefined>(undefined)
const priorityFilter = ref<string | undefined>(undefined)
const sortBy = ref<string | undefined>(undefined)

const createForm = reactive<TodoCreate>({
  title: '',
  description: undefined,
  priority: 'medium',
  due_date: undefined,
  reminder_at: undefined,
})

// Fetch data on mount
onMounted(async () => {
  await Promise.all([fetchTodos(), fetchStats()])
})

// Filter handlers
async function handleStatusFilter(value: string | undefined) {
  statusFilter.value = value
  setFilter('status', value)
  await fetchTodos()
}

async function handlePriorityFilter(value: string | undefined) {
  priorityFilter.value = value
  setFilter('priority', value)
  await fetchTodos()
}

async function handleSortBy(value: string | undefined) {
  sortBy.value = value
  setSortBy(value)
  await fetchTodos()
}

// Create todo
async function handleCreateTodo() {
  if (!createForm.title.trim()) {
    return
  }

  creating.value = true
  const data: TodoCreate = {
    title: createForm.title.trim(),
    description: createForm.description?.trim() || undefined,
    priority: createForm.priority,
    due_date: createForm.due_date || undefined,
    reminder_at: createForm.reminder_at ? new Date(createForm.reminder_at).toISOString() : undefined,
  }

  const result = await createTodo(data)
  creating.value = false

  if (result) {
    toastSuccess('Todo created successfully')
    showCreateForm.value = false
    resetCreateForm()
    await fetchStats()
  } else {
    toastError(todosError.value || 'Failed to create todo')
  }
}

function resetCreateForm() {
  createForm.title = ''
  createForm.description = undefined
  createForm.priority = 'medium'
  createForm.due_date = undefined
  createForm.reminder_at = undefined
}

// Toggle todo status
async function toggleTodoStatus(todo: Todo) {
  const newStatus = todo.status === 'done' ? 'pending' : 'done'
  const result = await updateTodo(todo.id, { status: newStatus })

  if (result) {
    toastSuccess(newStatus === 'done' ? 'Todo completed' : 'Todo reopened')
    await fetchStats()
  } else {
    toastError(todosError.value || 'Failed to update todo')
  }
}

// Delete todo
function confirmDelete(todo: Todo) {
  todoToDelete.value = todo
  showDeleteConfirm.value = true
}

async function handleDeleteTodo() {
  if (!todoToDelete.value) return

  const success = await deleteTodo(todoToDelete.value.id)
  showDeleteConfirm.value = false

  if (success) {
    toastSuccess('Todo deleted successfully')
    await fetchStats()
  } else {
    toastError(todosError.value || 'Failed to delete todo')
  }

  todoToDelete.value = null
}

// Logout
async function handleLogout() {
  loggingOut.value = true
  const success = await logout()
  loggingOut.value = false

  if (success) {
    await router.push('/login')
  }
}

// Utility functions
function priorityClasses(priority: string): string {
  switch (priority) {
    case 'high':
      return 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400'
    case 'medium':
      return 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400'
    case 'low':
      return 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400'
    default:
      return 'bg-secondary-100 text-secondary-700 dark:bg-secondary-700 dark:text-secondary-300'
  }
}

function statusClasses(status: string): string {
  switch (status) {
    case 'done':
      return 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400'
    case 'in-progress':
      return 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400'
    case 'pending':
      return 'bg-secondary-100 text-secondary-700 dark:bg-secondary-700 dark:text-secondary-300'
    default:
      return 'bg-secondary-100 text-secondary-700 dark:bg-secondary-700 dark:text-secondary-300'
  }
}

function formatStatus(status: string): string {
  switch (status) {
    case 'in-progress':
      return 'In Progress'
    case 'done':
      return 'Done'
    case 'pending':
      return 'Pending'
    default:
      return status
  }
}

function formatDate(dateStr: string): string {
  const date = new Date(dateStr + 'T00:00:00')
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
}

function isOverdue(todo: Todo): boolean {
  if (!todo.due_date || todo.status === 'done') return false
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  const dueDate = new Date(todo.due_date + 'T00:00:00')
  return dueDate < today
}
</script>
