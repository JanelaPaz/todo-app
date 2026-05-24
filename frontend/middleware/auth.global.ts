import { authApi } from '~/utils/api'
import type { User } from '~/types'

export default defineNuxtRouteMiddleware(async (to) => {
  // Define route classifications
  const publicPages = ['/login', '/register']
  const protectedPages = ['/dashboard', '/kanban']

  const isPublicPage = publicPages.includes(to.path)
  const isProtectedPage = protectedPages.includes(to.path) || to.path.startsWith('/dashboard')

  // Use useState to persist auth state across navigations
  const user = useState<User | null>('auth-user', () => null)
  const authChecked = useState<boolean>('auth-checked', () => false)

  // Check auth state on initial load (only once)
  if (!authChecked.value) {
    try {
      const currentUser = await authApi.me()
      user.value = currentUser
    } catch {
      user.value = null
    }
    authChecked.value = true
  }

  const isAuthenticated = !!user.value

  // Redirect unauthenticated users from protected pages to login
  if (isProtectedPage && !isAuthenticated) {
    return navigateTo('/login')
  }

  // Redirect authenticated users from login/register to dashboard
  if (isPublicPage && isAuthenticated) {
    return navigateTo('/dashboard')
  }
})
