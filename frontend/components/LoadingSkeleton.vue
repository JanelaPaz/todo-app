<template>
  <div class="animate-pulse" role="status" :aria-label="ariaLabel">
    <span class="sr-only">{{ ariaLabel }}</span>

    <!-- Card variant -->
    <template v-if="variant === 'card'">
      <div
        v-for="i in count"
        :key="i"
        class="bg-white dark:bg-secondary-800 rounded-lg p-4 mb-3 border border-secondary-200 dark:border-secondary-700"
      >
        <div class="flex items-center gap-3">
          <div class="h-5 w-5 bg-secondary-200 dark:bg-secondary-700 rounded"></div>
          <div class="flex-1 space-y-2">
            <div class="h-4 bg-secondary-200 dark:bg-secondary-700 rounded w-3/4"></div>
            <div class="h-3 bg-secondary-200 dark:bg-secondary-700 rounded w-1/2"></div>
          </div>
          <div class="h-6 w-16 bg-secondary-200 dark:bg-secondary-700 rounded-full"></div>
        </div>
      </div>
    </template>

    <!-- Stats variant -->
    <template v-else-if="variant === 'stats'">
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div
          v-for="i in 4"
          :key="i"
          class="bg-white dark:bg-secondary-800 rounded-lg p-4 border border-secondary-200 dark:border-secondary-700"
        >
          <div class="h-3 bg-secondary-200 dark:bg-secondary-700 rounded w-1/2 mb-3"></div>
          <div class="h-8 bg-secondary-200 dark:bg-secondary-700 rounded w-1/3"></div>
        </div>
      </div>
    </template>

    <!-- Text variant (default) -->
    <template v-else>
      <div
        v-for="i in count"
        :key="i"
        class="mb-3"
      >
        <div class="h-4 bg-secondary-200 dark:bg-secondary-700 rounded" :class="lineWidth(i)"></div>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
interface Props {
  variant?: 'text' | 'card' | 'stats'
  count?: number
  ariaLabel?: string
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'text',
  count: 3,
  ariaLabel: 'Loading content',
})

function lineWidth(index: number): string {
  const widths = ['w-full', 'w-5/6', 'w-4/6', 'w-3/4', 'w-2/3']
  return widths[(index - 1) % widths.length]
}
</script>
