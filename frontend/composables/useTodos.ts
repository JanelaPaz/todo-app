import { ref, computed } from 'vue'
import { useTodosStore } from '~/stores/todos'
import { todosApi } from '~/utils/api'
import type { Todo, TodoCreate, TodoUpdate, TodoStats } from '~/types'

export function useTodos() {
  const store = useTodosStore()
  const error = ref<string | null>(null)

  const todos = computed<Todo[]>(() => store.filteredTodos)
  const stats = computed<TodoStats | null>(() => store.todoStats)
  const loading = computed<boolean>(() => store.loading)

  function clearError() {
    error.value = null
  }

  async function fetchTodos(): Promise<void> {
    clearError()
    try {
      await store.fetchTodos()
    } catch (err: any) {
      error.value = extractErrorMessage(err)
    }
  }

  async function fetchStats(): Promise<void> {
    clearError()
    try {
      await store.fetchStats()
    } catch (err: any) {
      error.value = extractErrorMessage(err)
    }
  }

  async function createTodo(data: TodoCreate): Promise<Todo | null> {
    clearError()

    // Optimistic update: add a temporary todo to the list
    const tempId = `temp-${Date.now()}`
    const optimisticTodo: Todo = {
      id: tempId,
      user_id: '',
      title: data.title,
      description: data.description ?? null,
      priority: data.priority ?? 'medium',
      due_date: data.due_date ?? null,
      status: data.status ?? 'pending',
      reminder_at: data.reminder_at ?? null,
      created_at: new Date().toISOString(),
      updated_at: null,
    }

    // Add optimistic todo to the store
    store.todos.unshift(optimisticTodo)

    try {
      const created = await todosApi.create(data)
      // Replace the optimistic todo with the real one from the server
      const index = store.todos.findIndex((t) => t.id === tempId)
      if (index !== -1) {
        store.todos[index] = created
      } else {
        store.todos.unshift(created)
      }
      return created
    } catch (err: any) {
      // Rollback: remove the optimistic todo
      store.todos = store.todos.filter((t) => t.id !== tempId)
      error.value = extractErrorMessage(err)
      return null
    }
  }

  async function updateTodo(id: string, data: TodoUpdate): Promise<Todo | null> {
    clearError()

    // Optimistic update: save original and apply changes immediately
    const index = store.todos.findIndex((t) => t.id === id)
    if (index === -1) {
      error.value = 'Todo not found'
      return null
    }

    const originalTodo = { ...store.todos[index] }
    const optimisticTodo: Todo = {
      ...originalTodo,
      ...data,
      updated_at: new Date().toISOString(),
    }
    store.todos[index] = optimisticTodo

    try {
      const updated = await todosApi.update(id, data)
      // Replace with the server response
      const currentIndex = store.todos.findIndex((t) => t.id === id)
      if (currentIndex !== -1) {
        store.todos[currentIndex] = updated
      }
      return updated
    } catch (err: any) {
      // Rollback: restore the original todo
      const rollbackIndex = store.todos.findIndex((t) => t.id === id)
      if (rollbackIndex !== -1) {
        store.todos[rollbackIndex] = originalTodo
      } else {
        // If the todo was removed during the request, re-add it
        store.todos.splice(index, 0, originalTodo)
      }
      error.value = extractErrorMessage(err)
      return null
    }
  }

  async function deleteTodo(id: string): Promise<boolean> {
    clearError()

    // Optimistic update: remove the todo immediately
    const index = store.todos.findIndex((t) => t.id === id)
    if (index === -1) {
      error.value = 'Todo not found'
      return false
    }

    const originalTodo = { ...store.todos[index] }
    const originalIndex = index
    store.todos.splice(index, 1)

    try {
      await todosApi.delete(id)
      return true
    } catch (err: any) {
      // Rollback: re-insert the todo at its original position
      store.todos.splice(originalIndex, 0, originalTodo)
      error.value = extractErrorMessage(err)
      return false
    }
  }

  function setFilter(key: 'status' | 'priority', value: string | undefined) {
    store.setFilter(key, value)
  }

  function setSortBy(value: string | undefined) {
    store.setSortBy(value)
  }

  return {
    // State
    todos,
    stats,
    loading,
    error,

    // Actions
    fetchTodos,
    fetchStats,
    createTodo,
    updateTodo,
    deleteTodo,
    setFilter,
    setSortBy,
    clearError,
  }
}

function extractErrorMessage(err: any): string {
  const statusCode = err?.response?.status || err?.statusCode || err?.status
  const data = err?.response?._data || err?.data

  if (statusCode === 422) {
    if (data?.detail && Array.isArray(data.detail)) {
      return data.detail.map((e: any) => e.message || e.msg).join('. ')
    }
    return data?.detail || 'Validation error'
  }

  if (statusCode === 404) {
    return data?.detail || 'Todo not found'
  }

  if (err?.message === 'Request timed out. Please try again.') {
    return err.message
  }

  if (err?.message) {
    return err.message
  }

  return 'Something went wrong. Please try again.'
}
