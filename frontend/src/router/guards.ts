/**
 * router/guard.ts
 * Navigation guard — redirects unauthenticated users away from protected routes.
 * Import and call setupGuards(router) in main.ts after createRouter().
 */
import type { Router } from 'vue-router'

export function setupGuards(router: Router) {
  router.beforeEach((to, _from, next) => {
    const requiresAuth = to.matched.some(r => r.meta?.requiresAuth)
    const token = localStorage.getItem('vault_access')

    if (requiresAuth && !token) {
      return next({ path: '/login', query: { redirect: to.fullPath } })
    }

    // Already logged in — don't let them see login/register again
    if (token && (to.path === '/login' || to.path === '/register')) {
      return next('/dashboard')
    }

    next()
  })
}