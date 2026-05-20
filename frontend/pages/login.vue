<template>
  <div class="min-h-screen flex">
    <!-- Decorative side panel (desktop ≥1024px) -->
    <div class="hidden lg:flex lg:w-1/2 bg-gradient-to-br from-primary-600 via-primary-700 to-primary-900 items-center justify-center p-12">
      <div class="max-w-md text-center">
        <div class="mb-8">
          <svg class="w-20 h-20 mx-auto text-white/90" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
          </svg>
        </div>
        <h2 class="text-3xl font-bold text-white mb-4">Welcome back!</h2>
        <p class="text-primary-100 text-lg leading-relaxed">
          Organize your tasks, track your progress, and stay productive with our intuitive todo manager.
        </p>
        <div class="mt-10 flex items-center justify-center gap-3">
          <div class="w-2 h-2 rounded-full bg-primary-300"></div>
          <div class="w-2 h-2 rounded-full bg-primary-400"></div>
          <div class="w-2 h-2 rounded-full bg-primary-200"></div>
        </div>
      </div>
    </div>

    <!-- Login form panel -->
    <div class="flex-1 flex items-center justify-center p-4 md:p-8 lg:p-12 bg-white dark:bg-secondary-900">
      <div class="w-full max-w-md">
        <!-- Header -->
        <div class="mb-8">
          <h1 class="text-3xl font-bold text-secondary-900 dark:text-white">Sign in</h1>
          <p class="mt-2 text-secondary-600 dark:text-secondary-400">
            Enter your credentials to access your account
          </p>
        </div>

        <!-- General/server error message -->
        <div
          v-if="errors.general"
          class="mb-6 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg"
          role="alert"
        >
          <p class="text-sm text-red-700 dark:text-red-400">{{ errors.general }}</p>
        </div>

        <!-- Login form -->
        <form @submit.prevent="handleSubmit" novalidate>
          <!-- Email/Username field -->
          <div class="mb-5">
            <label for="identifier" class="block text-sm font-medium text-secondary-700 dark:text-secondary-300 mb-1.5">
              Email or Username
            </label>
            <input
              id="identifier"
              v-model="form.identifier"
              type="text"
              class="input-field"
              :class="{ 'border-red-500 focus:ring-red-500 focus:border-red-500': errors.identifier }"
              placeholder="you@example.com or username"
              autocomplete="username"
              :disabled="loading"
            />
            <p v-if="errors.identifier" class="mt-1.5 text-sm text-red-600 dark:text-red-400" role="alert">
              {{ errors.identifier }}
            </p>
          </div>

          <!-- Password field -->
          <div class="mb-6">
            <label for="password" class="block text-sm font-medium text-secondary-700 dark:text-secondary-300 mb-1.5">
              Password
            </label>
            <input
              id="password"
              v-model="form.password"
              type="password"
              class="input-field"
              :class="{ 'border-red-500 focus:ring-red-500 focus:border-red-500': errors.password }"
              placeholder="Enter your password"
              autocomplete="current-password"
              :disabled="loading"
            />
            <p v-if="errors.password" class="mt-1.5 text-sm text-red-600 dark:text-red-400" role="alert">
              {{ errors.password }}
            </p>
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
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <span>{{ loading ? 'Signing in...' : 'Sign in' }}</span>
          </button>
        </form>

        <!-- Register link -->
        <p class="mt-6 text-center text-sm text-secondary-600 dark:text-secondary-400">
          Don't have an account?
          <NuxtLink to="/register" class="font-medium text-primary-600 hover:text-primary-500 dark:text-primary-400 dark:hover:text-primary-300 transition-colors duration-200">
            Create one
          </NuxtLink>
        </p>
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

const router = useRouter()
const { login, loading, errors, clearErrors } = useAuth()

const form = reactive({
  identifier: '',
  password: '',
})

async function handleSubmit() {
  clearErrors()

  const success = await login(form)

  if (success) {
    await router.push('/dashboard')
  }
}
</script>
