<template>
  <div class="flex flex-col md:flex-row gap-3 items-start md:items-center">
    <!-- Status filter -->
    <div class="flex items-center gap-2">
      <label for="filter-status" class="text-sm font-medium text-secondary-600 dark:text-secondary-400 whitespace-nowrap">
        Status:
      </label>
      <select
        id="filter-status"
        :value="statusFilter"
        class="input-field text-sm py-1.5 px-2.5 w-auto min-w-[120px]"
        @change="$emit('update:statusFilter', ($event.target as HTMLSelectElement).value || undefined)"
      >
        <option value="">All</option>
        <option value="pending">Pending</option>
        <option value="in-progress">In Progress</option>
        <option value="done">Done</option>
      </select>
    </div>

    <!-- Priority filter -->
    <div class="flex items-center gap-2">
      <label for="filter-priority" class="text-sm font-medium text-secondary-600 dark:text-secondary-400 whitespace-nowrap">
        Priority:
      </label>
      <select
        id="filter-priority"
        :value="priorityFilter"
        class="input-field text-sm py-1.5 px-2.5 w-auto min-w-[120px]"
        @change="$emit('update:priorityFilter', ($event.target as HTMLSelectElement).value || undefined)"
      >
        <option value="">All</option>
        <option value="low">Low</option>
        <option value="medium">Medium</option>
        <option value="high">High</option>
      </select>
    </div>

    <!-- Sort control -->
    <div class="flex items-center gap-2 md:ml-auto">
      <label for="sort-by" class="text-sm font-medium text-secondary-600 dark:text-secondary-400 whitespace-nowrap">
        Sort by:
      </label>
      <select
        id="sort-by"
        :value="sortBy"
        class="input-field text-sm py-1.5 px-2.5 w-auto min-w-[140px]"
        @change="$emit('update:sortBy', ($event.target as HTMLSelectElement).value || undefined)"
      >
        <option value="">Default</option>
        <option value="due_date">Due Date</option>
        <option value="created_at">Created At</option>
      </select>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  statusFilter?: string
  priorityFilter?: string
  sortBy?: string
}

defineProps<Props>()

defineEmits<{
  'update:statusFilter': [value: string | undefined]
  'update:priorityFilter': [value: string | undefined]
  'update:sortBy': [value: string | undefined]
}>()
</script>
