<template>
  <div></div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: false,
})

// Redirect to dashboard (auth middleware will handle sending to login if not authenticated)
await navigateTo('/dashboard', { redirectCode: 302 })
</script>
