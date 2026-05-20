<template>
  <div>
    <!-- Loading state -->
    <LoadingSkeleton v-if="loading" variant="card" :count="5" aria-label="Loading todos" />

    <!-- Empty state -->
    <EmptyState
      v-else-if="todos.length === 0"
      title="No todos yet"
      description="Get started by creating your first todo. Stay organized and track your tasks effortlessly."
      action-text="Create Todo"
      @action="$emit('create')"
    />

    <!-- Todo list -->
    <TransitionGroup
      v-else
      name="todo-list"
      tag="div"
      class="space-y-3"
    >
      <TodoItem
        v-for="todo in todos"
        :key="todo.id"
        :todo="todo"
        @edit="(t) => $emit('edit', t)"
        @delete="handleDeleteRequest"
        @update="handleUpdate"
      />
    </TransitionGroup>

    <!-- Confirm delete dialog -->
    <ConfirmDialog
      :visible="showDeleteDialog"
      title="Delete Todo"
      message="Are you sure you want to delete this todo? This action cannot be undone."
      confirm-text="Delete"
      cancel-text="Cancel"
      variant="danger"
      @confirm="confirmDelete"
      @cancel="cancelDelete"
      @update:visible="showDeleteDialog = $event"
    />
  </div>
</template>

<script setup lang="ts">
import type { Todo, TodoUpdate } from '~/types'

interface Props {
  todos: Todo[]
  loading?: boolean
}

withDefaults(defineProps<Props>(), {
  loading: false,
})

const emit = defineEmits<{
  create: []
  edit: [todo: Todo]
  delete: [id: string]
  update: [id: string, data: TodoUpdate]
}>()

// Delete confirmation state
const showDeleteDialog = ref(false)
const todoToDelete = ref<Todo | null>(null)

function handleDeleteRequest(todo: Todo) {
  todoToDelete.value = todo
  showDeleteDialog.value = true
}

function confirmDelete() {
  if (todoToDelete.value) {
    emit('delete', todoToDelete.value.id)
  }
  todoToDelete.value = null
  showDeleteDialog.value = false
}

function cancelDelete() {
  todoToDelete.value = null
  showDeleteDialog.value = false
}

function handleUpdate(id: string, data: TodoUpdate) {
  emit('update', id, data)
}
</script>

<style scoped>
/* List enter/leave transitions (150-300ms range) */
.todo-list-enter-active {
  transition: all 250ms ease-out;
}

.todo-list-leave-active {
  transition: all 200ms ease-in;
}

.todo-list-enter-from {
  opacity: 0;
  transform: translateY(-10px);
}

.todo-list-leave-to {
  opacity: 0;
  transform: translateX(20px);
}

/* Ensure smooth reordering */
.todo-list-move {
  transition: transform 250ms ease;
}
</style>
