import { ref, reactive, computed } from 'vue'
import { authApi } from '~/utils/api'
import type { User } from '~/types'

interface ValidationErrors {
  email?: string
  username?: string
  password?: string
  passwordConfirm?: string
  identifier?: string
  general?: string
}

interface LoginForm {
  identifier: string
  password: string
}

interface RegisterForm {
  email: string
  username: string
  password: string
  passwordConfirm: string
}

export function useAuth() {
  const loading = ref(false)
  const errors = reactive<ValidationErrors>({})
  const user = ref<User | null>(null)

  function clearErrors() {
    errors.email = undefined
    errors.username = undefined
    errors.password = undefined
    errors.passwordConfirm = undefined
    errors.identifier = undefined
    errors.general = undefined
  }

  function validateEmail(email: string): string | undefined {
    if (!email || !email.trim()) {
      return 'Email is required'
    }
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!emailRegex.test(email.trim())) {
      return 'Invalid email format'
    }
    return undefined
  }

  function validateUsername(username: string): string | undefined {
    if (!username || !username.trim()) {
      return 'Username is required'
    }
    const trimmed = username.trim()
    if (trimmed.length < 3 || trimmed.length > 30) {
      return 'Username must be between 3 and 30 characters'
    }
    const usernameRegex = /^[a-zA-Z0-9_]+$/
    if (!usernameRegex.test(trimmed)) {
      return 'Username can only contain letters, numbers, and underscores'
    }
    return undefined
  }

  function validatePassword(password: string): string | undefined {
    if (!password) {
      return 'Password is required'
    }
    if (password.length < 8) {
      return 'Password must be at least 8 characters'
    }
    return undefined
  }

  function validatePasswordConfirm(password: string, passwordConfirm: string): string | undefined {
    if (!passwordConfirm) {
      return 'Password confirmation is required'
    }
    if (password !== passwordConfirm) {
      return 'Passwords do not match'
    }
    return undefined
  }

  function validateLoginForm(form: LoginForm): boolean {
    clearErrors()
    let valid = true

    if (!form.identifier || !form.identifier.trim()) {
      errors.identifier = 'Email or username is required'
      valid = false
    }

    const passwordError = validatePassword(form.password)
    if (passwordError) {
      errors.password = passwordError
      valid = false
    }

    return valid
  }

  function validateRegisterForm(form: RegisterForm): boolean {
    clearErrors()
    let valid = true

    const emailError = validateEmail(form.email)
    if (emailError) {
      errors.email = emailError
      valid = false
    }

    const usernameError = validateUsername(form.username)
    if (usernameError) {
      errors.username = usernameError
      valid = false
    }

    const passwordError = validatePassword(form.password)
    if (passwordError) {
      errors.password = passwordError
      valid = false
    }

    const confirmError = validatePasswordConfirm(form.password, form.passwordConfirm)
    if (confirmError) {
      errors.passwordConfirm = confirmError
      valid = false
    }

    return valid
  }

  function handleServerError(error: any) {
    if (error?.message === 'Request timed out. Please try again.') {
      errors.general = 'Request timed out. Please try again.'
      return
    }

    const statusCode = error?.statusCode || error?.response?.status
    const data = error?.data || error?.response?._data

    if (statusCode === 422 && data?.detail) {
      // Field-level validation errors from server
      if (Array.isArray(data.detail)) {
        for (const fieldError of data.detail) {
          const field = fieldError.field as keyof ValidationErrors
          if (field && field in errors) {
            (errors as any)[field] = fieldError.message
          }
        }
      } else if (typeof data.detail === 'string') {
        errors.general = data.detail
      }
    } else if (statusCode === 409 && data?.detail) {
      // Conflict error (email/username already exists)
      const message = data.detail as string
      if (message.toLowerCase().includes('email')) {
        errors.email = message
      } else if (message.toLowerCase().includes('username')) {
        errors.username = message
      } else {
        errors.general = message
      }
    } else if (statusCode === 401 && data?.detail) {
      errors.general = data.detail
    } else if (data?.detail) {
      errors.general = typeof data.detail === 'string' ? data.detail : 'An error occurred'
    } else if (error?.message) {
      errors.general = error.message
    } else {
      errors.general = 'Something went wrong. Please try again.'
    }
  }

  async function login(form: LoginForm): Promise<boolean> {
    if (!validateLoginForm(form)) {
      return false
    }

    loading.value = true
    clearErrors()

    try {
      const result = await authApi.login({
        identifier: form.identifier.trim(),
        password: form.password,
      })
      user.value = result
      // Update global auth state so middleware recognizes the user
      const authUser = useState<User | null>('auth-user')
      authUser.value = result
      return true
    } catch (error: any) {
      handleServerError(error)
      return false
    } finally {
      loading.value = false
    }
  }

  async function register(form: RegisterForm): Promise<boolean> {
    if (!validateRegisterForm(form)) {
      return false
    }

    loading.value = true
    clearErrors()

    try {
      const result = await authApi.register({
        email: form.email.trim(),
        username: form.username.trim(),
        password: form.password,
        password_confirm: form.passwordConfirm,
      })
      user.value = result
      // Update global auth state so middleware recognizes the user
      const authUser = useState<User | null>('auth-user')
      authUser.value = result
      return true
    } catch (error: any) {
      handleServerError(error)
      return false
    } finally {
      loading.value = false
    }
  }

  async function logout(): Promise<boolean> {
    loading.value = true
    try {
      await authApi.logout()
      user.value = null
      // Clear global auth state so middleware redirects to login
      const authUser = useState<User | null>('auth-user')
      authUser.value = null
      return true
    } catch (error: any) {
      handleServerError(error)
      return false
    } finally {
      loading.value = false
    }
  }

  async function fetchUser(): Promise<boolean> {
    try {
      const result = await authApi.me()
      user.value = result
      return true
    } catch {
      user.value = null
      return false
    }
  }

  const isAuthenticated = computed(() => !!user.value)

  return {
    // State
    loading,
    errors,
    user,
    isAuthenticated,

    // Validation
    validateLoginForm,
    validateRegisterForm,
    validateEmail,
    validateUsername,
    validatePassword,
    validatePasswordConfirm,
    clearErrors,

    // Actions
    login,
    register,
    logout,
    fetchUser,
  }
}
