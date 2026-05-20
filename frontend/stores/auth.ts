import { defineStore } from 'pinia'
import type { User } from '~/types'
import { authApi } from '~/utils/api'

interface AuthState {
  user: User | null
  isAuthenticated: boolean
  loading: boolean
  error: string | null
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    user: null,
    isAuthenticated: false,
    loading: false,
    error: null,
  }),

  actions: {
    async login(identifier: string, password: string) {
      this.loading = true
      this.error = null

      try {
        const user = await authApi.login({ identifier, password })
        this.user = user
        this.isAuthenticated = true
      } catch (err: any) {
        this.isAuthenticated = false
        this.user = null
        this.error = extractErrorMessage(err)
        throw err
      } finally {
        this.loading = false
      }
    },

    async register(email: string, username: string, password: string, password_confirm: string) {
      this.loading = true
      this.error = null

      try {
        const user = await authApi.register({ email, username, password, password_confirm })
        this.user = user
        this.isAuthenticated = true
      } catch (err: any) {
        this.isAuthenticated = false
        this.user = null
        this.error = extractErrorMessage(err)
        throw err
      } finally {
        this.loading = false
      }
    },

    async logout() {
      this.loading = true
      this.error = null

      try {
        await authApi.logout()
      } catch {
        // Even if the API call fails, clear local state
      } finally {
        this.user = null
        this.isAuthenticated = false
        this.loading = false
      }
    },

    async fetchUser() {
      this.loading = true
      this.error = null

      try {
        const user = await authApi.me()
        this.user = user
        this.isAuthenticated = true
      } catch {
        this.user = null
        this.isAuthenticated = false
      } finally {
        this.loading = false
      }
    },
  },
})

function extractErrorMessage(err: any): string {
  // Handle $fetch error responses from Nuxt/ofetch
  const statusCode = err?.response?.status || err?.statusCode || err?.status
  const data = err?.response?._data || err?.data

  if (statusCode === 401) {
    return data?.detail || 'Invalid credentials'
  }

  if (statusCode === 409) {
    return data?.detail || 'Account already exists'
  }

  if (statusCode === 422) {
    // Handle field-level validation errors
    if (data?.detail && Array.isArray(data.detail)) {
      return data.detail.map((e: any) => e.message || e.msg).join('. ')
    }
    return data?.detail || 'Validation error'
  }

  if (err?.message === 'Request timed out. Please try again.') {
    return err.message
  }

  return 'Something went wrong. Please try again.'
}
