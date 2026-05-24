<template>
  <div class="min-h-screen bg-secondary-50 dark:bg-secondary-900 transition-colors duration-200">
    <!-- Header -->
    <header class="bg-white dark:bg-secondary-800 border-b border-secondary-200 dark:border-secondary-700 sticky top-0 z-10">
      <div class="max-w-7xl mx-auto px-4 md:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">
          <!-- Logo / Title -->
          <div class="flex items-center gap-3">
            <svg class="w-8 h-8 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17V7m0 10a2 2 0 01-2 2H5a2 2 0 01-2-2V7a2 2 0 012-2h2a2 2 0 012 2m0 10a2 2 0 002 2h2a2 2 0 002-2M9 7a2 2 0 012-2h2a2 2 0 012 2m0 10V7m0 10a2 2 0 002 2h2a2 2 0 002-2V7a2 2 0 00-2-2h-2a2 2 0 00-2 2" />
            </svg>
            <h1 class="text-xl font-bold text-secondary-900 dark:text-white">Kanban Board</h1>
          </div>

          <!-- Navigation + Actions -->
          <div class="flex items-center gap-2">
            <NuxtLink
              to="/dashboard"
              class="btn-secondary text-sm flex items-center gap-1.5"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
              </svg>
              <span class="hidden sm:inline">Dashboard</span>
            </NuxtLink>
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
      <!-- Drag hint -->
      <p class="text-xs text-secondary-500 dark:text-secondary-400 mb-4 flex items-center gap-1.5">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16V4m0 0L3 8m4-4l4 4m6 0v12m0 0l4-4m-4 4l-4-4" />
        </svg>
        Drag cards between columns to change priority
      </p>

      <!-- Loading -->
      <div v-if="loading" class="flex items-center justify-center py-20">
        <svg class="animate-spin h-8 w-8 text-primary-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" aria-hidden="true">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
      </div>

      <!-- Kanban columns -->
      <div v-else class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <!-- High Priority Column -->
        <div class="flex flex-col">
          <div class="flex items-center gap-2 mb-4 px-1">
            <span class="w-3 h-3 rounded-full bg-red-500"></span>
            <h2 class="text-sm font-semibold text-secondary-900 dark:text-white uppercase tracking-wider">
              High Priority
            </h2>
            <span class="ml-auto text-xs font-medium text-secondary-500 dark:text-secondary-400 bg-secondary-100 dark:bg-secondary-700 px-2 py-0.5 rounded-full">
              {{ highTodos.length }}
            </span>
          </div>
          <div
            class="flex-1 space-y-3 rounded-xl p-3 min-h-[200px] border-2 transition-colors duration-150"
            :class="dragOverColumn === 'high'
              ? 'bg-red-100 dark:bg-red-900/30 border-red-400 dark:border-red-500'
              : 'bg-red-50/50 dark:bg-red-900/10 border-red-100 dark:border-red-900/30'"
            @dragover.prevent="onDragOver('high')"
            @dragleave="onDragLeave"
            @drop.prevent="onDrop('high')"
            data-testid="kanban-column-high"
          >
            <KanbanCard
              v-for="todo in highTodos"
              :key="todo.id"
              :todo="todo"
              @dragstart="onDragStart(todo)"
              @dragend="onDragEnd"
              @click="openDetail(todo)"
              @toggle-status="toggleStatus(todo)"
            />
            <p v-if="highTodos.length === 0" class="text-center text-sm text-secondary-400 dark:text-secondary-500 py-8">
              No high priority todos
            </p>
          </div>
        </div>

        <!-- Medium Priority Column -->
        <div class="flex flex-col">
          <div class="flex items-center gap-2 mb-4 px-1">
            <span class="w-3 h-3 rounded-full bg-yellow-500"></span>
            <h2 class="text-sm font-semibold text-secondary-900 dark:text-white uppercase tracking-wider">
              Medium Priority
            </h2>
            <span class="ml-auto text-xs font-medium text-secondary-500 dark:text-secondary-400 bg-secondary-100 dark:bg-secondary-700 px-2 py-0.5 rounded-full">
              {{ mediumTodos.length }}
            </span>
          </div>
          <div
            class="flex-1 space-y-3 rounded-xl p-3 min-h-[200px] border-2 transition-colors duration-150"
            :class="dragOverColumn === 'medium'
              ? 'bg-yellow-100 dark:bg-yellow-900/30 border-yellow-400 dark:border-yellow-500'
              : 'bg-yellow-50/50 dark:bg-yellow-900/10 border-yellow-100 dark:border-yellow-900/30'"
            @dragover.prevent="onDragOver('medium')"
            @dragleave="onDragLeave"
            @drop.prevent="onDrop('medium')"
            data-testid="kanban-column-medium"
          >
            <KanbanCard
              v-for="todo in mediumTodos"
              :key="todo.id"
              :todo="todo"
              @dragstart="onDragStart(todo)"
              @dragend="onDragEnd"
              @click="openDetail(todo)"
              @toggle-status="toggleStatus(todo)"
            />
            <p v-if="mediumTodos.length === 0" class="text-center text-sm text-secondary-400 dark:text-secondary-500 py-8">
              No medium priority todos
            </p>
          </div>
        </div>

        <!-- Low Priority Column -->
        <div class="flex flex-col">
          <div class="flex items-center gap-2 mb-4 px-1">
            <span class="w-3 h-3 rounded-full bg-green-500"></span>
            <h2 class="text-sm font-semibold text-secondary-900 dark:text-white uppercase tracking-wider">
              Low Priority
            </h2>
            <span class="ml-auto text-xs font-medium text-secondary-500 dark:text-secondary-400 bg-secondary-100 dark:bg-secondary-700 px-2 py-0.5 rounded-full">
              {{ lowTodos.length }}
            </span>
          </div>
          <div
            class="flex-1 space-y-3 rounded-xl p-3 min-h-[200px] border-2 transition-colors duration-150"
            :class="dragOverColumn === 'low'
              ? 'bg-green-100 dark:bg-green-900/30 border-green-400 dark:border-green-500'
              : 'bg-green-50/50 dark:bg-green-900/10 border-green-100 dark:border-green-900/30'"
            @dragover.prevent="onDragOver('low')"
            @dragleave="onDragLeave"
            @drop.prevent="onDrop('low')"
            data-testid="kanban-column-low"
          >
            <KanbanCard
              v-for="todo in lowTodos"
              :key="todo.id"
              :todo="todo"
              @dragstart="onDragStart(todo)"
              @dragend="onDragEnd"
              @click="openDetail(todo)"
              @toggle-status="toggleStatus(todo)"
            />
            <p v-if="lowTodos.length === 0" class="text-center text-sm text-secondary-400 dark:text-secondary-500 py-8">
              No low priority todos
            </p>
          </div>
        </div>
      </div>
    </main>

    <!-- Todo Detail Modal -->
    <TodoDetailModal
      :visible="showDetailModal"
      :todo="detailTodo"
      @update:visible="showDetailModal = $event"
      @update="handleUpdate"
      @delete="handleDeleteRequest"
    />

    <!-- Delete Confirmation -->
    <ConfirmDialog
      :visible="showDeleteConfirm"
      title="Delete Todo"
      message="Are you sure you want to delete this todo? This action cannot be undone."
      confirm-text="Delete"
      cancel-text="Cancel"
      variant="danger"
      @confirm="handleDelete"
      @cancel="showDeleteConfirm = false"
      @update:visible="showDeleteConfirm = $event"
    />
  </div>
</template>

<script setup lang="ts">
import { useTodos } from '~/composables/useTodos'
import { useAuth } from '~/composables/useAuth'
import { useToast } from '~/composables/useToast'
import type { Todo, TodoUpdate } from '~/types'

definePageMeta({
  layout: false,
})

const router = useRouter()
const { logout } = useAuth()
const { success: toastSuccess, error: toastError } = useToast()
const {
  todos,
  loading,
  error: todosError,
  fetchTodos,
  updateTodo,
  deleteTodo,
  setFilter,
  setSortBy,
} = useTodos()

// Local state
const showDetailModal = ref(false)
const detailTodo = ref<Todo | null>(null)
const showDeleteConfirm = ref(false)
const todoToDelete = ref<Todo | null>(null)
const loggingOut = ref(false)

// Drag and drop state
const draggedTodo = ref<Todo | null>(null)
const dragOverColumn = ref<string | null>(null)

// Computed columns by priority
const highTodos = computed(() => todos.value.filter(t => t.priority === 'high'))
const mediumTodos = computed(() => todos.value.filter(t => t.priority === 'medium'))
const lowTodos = computed(() => todos.value.filter(t => t.priority === 'low'))

// Fetch on mount — clear filters to get all todos for kanban view
onMounted(async () => {
  setFilter('status', undefined)
  setFilter('priority', undefined)
  setSortBy(undefined)
  await fetchTodos()
})

// Drag and drop handlers
function onDragStart(todo: Todo) {
  draggedTodo.value = todo
}

function onDragEnd() {
  draggedTodo.value = null
  dragOverColumn.value = null
}

function onDragOver(priority: string) {
  dragOverColumn.value = priority
}

function onDragLeave() {
  dragOverColumn.value = null
}

async function onDrop(newPriority: 'high' | 'medium' | 'low') {
  dragOverColumn.value = null

  if (!draggedTodo.value) return

  // Skip if dropped on the same column
  if (draggedTodo.value.priority === newPriority) {
    draggedTodo.value = null
    return
  }

  const todo = draggedTodo.value
  draggedTodo.value = null

  const result = await updateTodo(todo.id, { priority: newPriority })
  if (result) {
    toastSuccess(`Moved to ${newPriority} priority`)
  } else {
    toastError(todosError.value || 'Failed to update priority')
  }
}

// Actions
function openDetail(todo: Todo) {
  // Don't open detail if we were dragging
  if (draggedTodo.value) return
  detailTodo.value = todo
  showDetailModal.value = true
}

async function toggleStatus(todo: Todo) {
  const newStatus = todo.status === 'done' ? 'pending' : 'done'
  const result = await updateTodo(todo.id, { status: newStatus })
  if (result) {
    toastSuccess(newStatus === 'done' ? 'Todo completed' : 'Todo reopened')
  } else {
    toastError(todosError.value || 'Failed to update todo')
  }
}

async function handleUpdate(id: string, data: TodoUpdate) {
  const result = await updateTodo(id, data)
  if (result) {
    toastSuccess('Todo updated successfully')
    detailTodo.value = result
  } else {
    toastError(todosError.value || 'Failed to update todo')
  }
}

function handleDeleteRequest(todo: Todo) {
  showDetailModal.value = false
  todoToDelete.value = todo
  showDeleteConfirm.value = true
}

async function handleDelete() {
  if (!todoToDelete.value) return
  const success = await deleteTodo(todoToDelete.value.id)
  showDeleteConfirm.value = false
  if (success) {
    toastSuccess('Todo deleted successfully')
  } else {
    toastError(todosError.value || 'Failed to delete todo')
  }
  todoToDelete.value = null
}

async function handleLogout() {
  loggingOut.value = true
  const success = await logout()
  loggingOut.value = false
  if (success) {
    await router.push('/login')
  }
}
</script>
