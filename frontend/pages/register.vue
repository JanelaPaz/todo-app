<template>
  <div class="min-h-screen flex">
    <!-- Decorative side panel (desktop ≥1024px) -->
    <div class="hidden lg:flex lg:w-1/2 bg-gradient-to-br from-primary-600 via-primary-700 to-primary-900 items-center justify-center p-12">
      <div class="max-w-md text-center">
        <div class="mb-8">
          <svg class="w-20 h-20 mx-auto text-white/90" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <h2 class="text-3xl font-bold text-white mb-4">Start organizing your life</h2>
        <p class="text-primary-100 text-lg leading-relaxed">
          Create an account to manage your tasks, set priorities, and stay on top of your goals.
        </p>
      </div>
    </div>

    <!-- Registration form panel -->
    <div class="flex-1 flex items-center justify-center p-4 md:p-8 lg:p-12 bg-white dark:bg-secondary-900">
      <div class="w-full max-w-md">
        <div class="text-center mb-8">
          <h1 class="text-3xl font-bold text-secondary-900 dark:text-white">Create an account</h1>
          <p class="mt-2 text-secondary-600 dark:text-secondary-400">
            Already have an account?
            <NuxtLink to="/login" class="text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300 font-medium transition-colors duration-200">
              Sign in
            </NuxtLink>
          </p>
        </div>

        <!-- General error message -->
        <div
          v-if="errors.general"
          class="mb-6 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg"
          role="alert"
        >
          <p class="text-sm text-red-700 dark:text-red-400">{{ errors.general }}</p>
        </div>

        <form @submit.prevent="handleSubmit" novalidate>
          <!-- Email field -->
          <div class="mb-4">
            <label for="email" class="block text-sm font-medium text-secondary-700 dark:text-secondary-300 mb-1">
              Email
            </label>
            <input
              id="email"
              v-model="form.email"
              type="email"
              autocomplete="email"
              class="input-field"
              :class="{ 'border-red-500 dark:border-red-500 focus:ring-red-500 focus:border-red-500': errors.email }"
              placeholder="you@example.com"
            />
            <p v-if="errors.email" class="mt-1 text-sm text-red-600 dark:text-red-400">{{ errors.email }}</p>
          </div>

          <!-- Username field -->
          <div class="mb-4">
            <label for="username" class="block text-sm font-medium text-secondary-700 dark:text-secondary-300 mb-1">
              Username
            </label>
            <input
              id="username"
              v-model="form.username"
              type="text"
              autocomplete="username"
              class="input-field"
              :class="{ 'border-red-500 dark:border-red-500 focus:ring-red-500 focus:border-red-500': errors.username }"
              placeholder="john_doe"
            />
            <p v-if="errors.username" class="mt-1 text-sm text-red-600 dark:text-red-400">{{ errors.username }}</p>
          </div>

          <!-- Password field -->
          <div class="mb-4">
            <label for="password" class="block text-sm font-medium text-secondary-700 dark:text-secondary-300 mb-1">
              Password
            </label>
            <input
              id="password"
              v-model="form.password"
              type="password"
              autocomplete="new-password"
              class="input-field"
              :class="{ 'border-red-500 dark:border-red-500 focus:ring-red-500 focus:border-red-500': errors.password }"
              placeholder="At least 8 characters"
            />
            <p v-if="errors.password" class="mt-1 text-sm text-red-600 dark:text-red-400">{{ errors.password }}</p>
          </div>

          <!-- Password confirmation field -->
          <div class="mb-6">
            <label for="passwordConfirm" class="block text-sm font-medium text-secondary-700 dark:text-secondary-300 mb-1">
              Confirm Password
            </label>
            <input
              id="passwordConfirm"
              v-model="form.passwordConfirm"
              type="password"
              autocomplete="new-password"
              class="input-field"
              :class="{ 'border-red-500 dark:border-red-500 focus:ring-red-500 focus:border-red-500': errors.passwordConfirm }"
              placeholder="Repeat your password"
            />
            <p v-if="errors.passwordConfirm" class="mt-1 text-sm text-red-600 dark:text-red-400">{{ errors.passwordConfirm }}</p>
          </div>

          <!-- Submit button -->
          <button
            type="submit"
            class="btn-primary w-full flex items-center justify-center gap-2"
            :disabled="loading"
          >
            <svg
              v-if="loading"
              class="animate-spin h-5 w-5 text-white"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              aria-hidden="true"
            >
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
            </svg>
            <span>{{ loading ? 'Creating account...' : 'Create account' }}</span>
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import { useAuth } from '~/composables/useAuth'

definePageMeta({
  layout: false,
})

const { loading, errors, register } = useAuth()

const form = reactive({
  email: '',
  username: '',
  password: '',
  passwordConfirm: '',
})

async function handleSubmit() {
  const success = await register(form)
  if (success) {
    await navigateTo('/dashboard')
  }
}
</script>
