<template>
  <div class="min-h-screen w-full overflow-x-hidden bg-secondary-50 dark:bg-secondary-900 transition-colors duration-200">
    <NuxtPage />
    <Toast />
  </div>
</template>

<script setup lang="ts">
// Apply dark mode class on initial load to prevent flash
if (import.meta.client) {
  const stored = localStorage.getItem('todo-app-dark-mode')
  if (stored === 'dark') {
    document.documentElement.classList.add('dark')
  }
}
</script>
