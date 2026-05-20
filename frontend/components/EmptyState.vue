<template>
  <div class="flex flex-col items-center justify-center py-12 px-4 text-center">
    <!-- Illustration -->
    <div class="mb-6">
      <svg
        class="w-32 h-32 text-secondary-300 dark:text-secondary-600"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
        aria-hidden="true"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="1"
          d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
        />
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="1"
          d="M9 14l2 2 4-4"
          class="text-primary-400 dark:text-primary-500"
          stroke="currentColor"
          opacity="0.5"
        />
      </svg>
    </div>

    <!-- Title -->
    <h3 class="text-lg font-semibold text-secondary-900 dark:text-white mb-2">
      {{ title }}
    </h3>

    <!-- Description -->
    <p class="text-sm text-secondary-500 dark:text-secondary-400 max-w-sm mb-6">
      {{ description }}
    </p>

    <!-- Action slot -->
    <slot name="action">
      <button
        v-if="actionText"
        type="button"
        class="btn-primary"
        @click="$emit('action')"
      >
        {{ actionText }}
      </button>
    </slot>
  </div>
</template>

<script setup lang="ts">
interface Props {
  title?: string
  description?: string
  actionText?: string
}

withDefaults(defineProps<Props>(), {
  title: 'No todos yet',
  description: 'Get started by creating your first todo. Stay organized and track your tasks effortlessly.',
  actionText: '',
})

defineEmits<{
  action: []
}>()
</script>
