/**
 * router/index.ts
 */
import { createRouter, createWebHistory } from 'vue-router'
import Index      from '@/pages/landingPage.vue'
import Register   from '@/pages/RegisterPage.vue'
import Login      from '@/pages/LoginPage.vue'

// Lazy-loaded authenticated pages
const AppShell         = () => import('@/components/layout/AppShell.vue')
const DashboardPage    = () => import('@/pages/DashboardPage.vue')
const VerifyEmail      = () => import('@/pages/VerifyEmailView.vue')
const ResetPasswordPage = () => import('@/pages/ResetPasswordPage.vue')

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // ── Public ──────────────────────────────────────────────────────────────
    { path: '/',              component: Index },
    { path: '/register',      component: Register },
    { path: '/login',         component: Login },
    { path: '/verify-email',  component: VerifyEmail },
    { path: '/reset-password', component: ResetPasswordPage },

    // ── Authenticated (AppShell wraps all inner pages) ────────────────────
    {
      path: '/dashboard',
      component: AppShell,
      meta: { requiresAuth: true },
      children: [
        {
          path: '',
          name: 'dashboard',
          component: DashboardPage,
        },
        // Future routes: /dashboard/transactions, /dashboard/goals, etc.
      ],
    },
  ],
})

export default router