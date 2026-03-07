/**
 * router/guard.ts
 * Single source-of-truth navigation guard.
 * Called via setupGuards(router) in main.ts.
 * KEY must match ACCESS_TOKEN_KEY in useAuth.ts: 'ringit_access_token'
 */
import type { Router } from 'vue-router'

const ACCESS_TOKEN_KEY = 'ringit_access_token'

export function setupGuards(router: Router) {
  router.beforeEach((to, _from, next) => {
    const requiresAuth = to.matched.some(r => r.meta?.requiresAuth)
    const token = localStorage.getItem(ACCESS_TOKEN_KEY)

    if (requiresAuth && !token) {
      return next({ path: '/login', query: { redirect: to.fullPath } })
    }

    if (token && (to.path === '/login' || to.path === '/register' || to.path === '/')) {
      return next('/dashboard')
    }

    next()
  })
}