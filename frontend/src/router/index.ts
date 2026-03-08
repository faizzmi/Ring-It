/**
 * router/index.ts
 */
import { createRouter, createWebHistory } from 'vue-router'
import Index    from '@/pages/landingPage.vue'
import Register from '@/pages/RegisterPage.vue'
import Login    from '@/pages/LoginPage.vue'

const VerifyEmail       = () => import('@/pages/VerifyEmailView.vue')
const ResetPasswordPage = () => import('@/pages/ResetPasswordPage.vue')
const AppShell          = () => import('@/components/layout/AppShell.vue')
const DashboardPage     = () => import('@/pages/DashboardPage.vue')
const AccountsPage      = () => import('@/pages/AccountsPage.vue')
const AccountDetailPage = () => import('@/pages/AccountDetailPage.vue')
const TransactionsPage  = () => import('@/pages/TransactionsPage.vue')

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  scrollBehavior: () => ({ top: 0 }),
  routes: [
    { path: '/',               component: Index    },
    { path: '/register',       component: Register },
    { path: '/login',          component: Login    },
    { path: '/verify-email',   component: VerifyEmail },
    { path: '/reset-password', component: ResetPasswordPage },
    {
      path: '/dashboard',
      component: AppShell,
      meta: { requiresAuth: true },
      children: [
        { path: '',              name: 'dashboard',    component: DashboardPage    },
        { path: 'accounts',      name: 'accounts',     component: AccountsPage     },
        { path: 'accounts/:id',  name: 'account-detail', component: AccountDetailPage },
        { path: 'transactions',  name: 'transactions', component: TransactionsPage },
        // { path: '/transactions/analytics', component: Ana }
        // { path: 'budget',     name: 'budget',       component: BudgetPage },
        // { path: 'goals',      name: 'goals',        component: GoalsPage  },
        // { path: 'debt',       name: 'debt',         component: DebtPage   },
      ],
    },
  ],
})

// Auth guard is handled exclusively in router/guard.ts via setupGuards(router).
// Do NOT add another beforeEach here.

export default router