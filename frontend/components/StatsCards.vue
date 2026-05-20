<template>
  <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
    <!-- Total -->
    <div
      class="bg-white dark:bg-secondary-800 rounded-lg p-4 border border-secondary-200 dark:border-secondary-700 transition-colors duration-200"
    >
      <div class="flex items-center gap-3">
        <div class="flex-shrink-0 w-10 h-10 rounded-lg bg-primary-100 dark:bg-primary-900/30 flex items-center justify-center">
          <svg class="w-5 h-5 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
        </div>
        <div>
          <p class="text-xs font-medium text-secondary-500 dark:text-secondary-400 uppercase tracking-wide">Total</p>
          <p class="text-2xl font-bold text-secondary-900 dark:text-white">{{ stats?.total ?? 0 }}</p>
        </div>
      </div>
    </div>

    <!-- Completed -->
    <div
      class="bg-white dark:bg-secondary-800 rounded-lg p-4 border border-secondary-200 dark:border-secondary-700 transition-colors duration-200"
    >
      <div class="flex items-center gap-3">
        <div class="flex-shrink-0 w-10 h-10 rounded-lg bg-green-100 dark:bg-green-900/30 flex items-center justify-center">
          <svg class="w-5 h-5 text-green-600 dark:text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <div>
          <p class="text-xs font-medium text-secondary-500 dark:text-secondary-400 uppercase tracking-wide">Completed</p>
          <p class="text-2xl font-bold text-green-600 dark:text-green-400">{{ stats?.completed ?? 0 }}</p>
        </div>
      </div>
    </div>

    <!-- Pending -->
    <div
      class="bg-white dark:bg-secondary-800 rounded-lg p-4 border border-secondary-200 dark:border-secondary-700 transition-colors duration-200"
    >
      <div class="flex items-center gap-3">
        <div class="flex-shrink-0 w-10 h-10 rounded-lg bg-yellow-100 dark:bg-yellow-900/30 flex items-center justify-center">
          <svg class="w-5 h-5 text-yellow-600 dark:text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <div>
          <p class="text-xs font-medium text-secondary-500 dark:text-secondary-400 uppercase tracking-wide">Pending</p>
          <p class="text-2xl font-bold text-yellow-600 dark:text-yellow-400">{{ stats?.pending ?? 0 }}</p>
        </div>
      </div>
    </div>

    <!-- Overdue -->
    <div
      class="bg-white dark:bg-secondary-800 rounded-lg p-4 border border-secondary-200 dark:border-secondary-700 transition-colors duration-200"
    >
      <div class="flex items-center gap-3">
        <div class="flex-shrink-0 w-10 h-10 rounded-lg bg-red-100 dark:bg-red-900/30 flex items-center justify-center">
          <svg class="w-5 h-5 text-red-600 dark:text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
        </div>
        <div>
          <p class="text-xs font-medium text-secondary-500 dark:text-secondary-400 uppercase tracking-wide">Overdue</p>
          <p class="text-2xl font-bold text-red-600 dark:text-red-400">{{ stats?.overdue ?? 0 }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { TodoStats } from '~/types'

interface Props {
  stats: TodoStats | null
}

defineProps<Props>()
</script>
