/**
 * composables/useLedger.ts
 * Aggregated financial ledger: net worth, DSR, monthly summary, budgets, goals.
 * Mirrors useAuth.ts exactly: module-level singleton refs, apiFetch(path, options, withAuth),
 * useRouter() inside the composable, errors thrown + surfaced via shared error ref.
 */
import { ref, computed } from 'vue'
import { useTheme } from 'vuetify'

// ── Types ─────────────────────────────────────────────────────────────────────

export interface ILedgerSummary {
  netWorth:      number
  netWorthDelta: number
  dsr:           number
  dsrStatus:     string
  dsrLabel:      string
  dsrMessage:    string
  income:        number
  expenses:      number
  savings:       number
  incomeTrend:   number
  expenseTrend:  number
  savingsTrend:  number
}

export interface IBudget {
  id:           string
  label:        string
  category_id?: string
  total:        number
  spent:        number
  color:        string
  period:       'monthly' | 'weekly'
}

export interface IGoal {
  id:        string
  label:     string
  target:    number
  current:   number
  pct:       number
  deadline?: string | null
  icon_svg?: string
  color?:    string
}

// ── Constants ─────────────────────────────────────────────────────────────────

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000/api/v1'
const ACCESS_TOKEN_KEY = 'ringit_access_token'

// ── Singleton state ───────────────────────────────────────────────────────────

const summary = ref<ILedgerSummary>({
  netWorth: 0, netWorthDelta: 0,
  dsr: 0, dsrStatus: '', dsrLabel: '', dsrMessage: '',
  income: 0, expenses: 0, savings: 0,
  incomeTrend: 0, expenseTrend: 0, savingsTrend: 0,
})
const budgets = ref<IBudget[]>([])
const goals   = ref<IGoal[]>([])
const loading = ref(false)
const error   = ref<string | null>(null)

// ── apiFetch ──────────────────────────────────────────────────────────────────

async function apiFetch<T>(
  path: string,
  options: RequestInit = {},
  withAuth = false,
): Promise<T> {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options.headers as Record<string, string> ?? {}),
  }
  if (withAuth) {
    const token = localStorage.getItem(ACCESS_TOKEN_KEY)
    if (token) headers['Authorization'] = `Bearer ${token}`
  }
  const res = await fetch(`${API_BASE}${path}`, { ...options, headers })
  if (!res.ok) {
    const body = await res.json().catch(() => ({}))
    const err  = new Error(body?.detail ?? `Request failed: ${res.status}`) as Error & { status: number }
    err.status = res.status
    throw err
  }
  if (res.status === 204) return undefined as T
  return res.json() as Promise<T>
}

// ── Composable ────────────────────────────────────────────────────────────────

export function useLedger() {
  const theme = useTheme()

  const dsrColor = computed(() => {
    const c = theme.current.value.colors
    switch (summary.value.dsrStatus) {
      case 'healthy':  return c.success
      case 'good':     return c.warning
      case 'danger':   return c.warning
      case 'critical': return c.error
      default:         return c.secondary
    }
  })

  const dsrLabel = computed(() => summary.value.dsrLabel ?? '')

  const budgetDaysLeft = computed(() => {
    const now = new Date()
    const end = new Date(now.getFullYear(), now.getMonth() + 1, 0)
    return end.getDate() - now.getDate()
  })

  const overspentBudgets = computed(() =>
    budgets.value.filter(b => b.spent > b.total)
  )

  const savingsRate = computed(() => {
    if (!summary.value.income) return 0
    return Math.round((summary.value.savings / summary.value.income) * 100)
  })

  async function fetchSummary(): Promise<void> {
    loading.value = true
    error.value   = null
    try {
      summary.value = await apiFetch<ILedgerSummary>('/ledger/summary', {}, true)
    } catch (e: unknown) {
      error.value = e instanceof Error ? e.message : 'Failed to load summary.'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function fetchBudgets(): Promise<void> {
    try {
      budgets.value = await apiFetch<IBudget[]>('/budgets', {}, true)
    } catch (e: unknown) {
      console.warn('[useLedger] fetchBudgets failed:', e)
    }
  }

  async function fetchGoals(): Promise<void> {
    try {
      const raw = await apiFetch<Omit<IGoal, 'pct'>[]>('/goals', {}, true)
      goals.value = raw.map(g => ({
        ...g,
        pct: g.target > 0 ? Math.round((g.current / g.target) * 100) : 0,
      }))
    } catch (e: unknown) {
      console.warn('[useLedger] fetchGoals failed:', e)
    }
  }

  async function fetchAll(): Promise<void> {
    await Promise.all([fetchSummary(), fetchBudgets(), fetchGoals()])
  }

  return {
    summary,
    budgets,
    goals,
    loading,
    error,
    dsrColor,
    dsrLabel,
    budgetDaysLeft,
    overspentBudgets,
    savingsRate,
    fetchSummary,
    fetchBudgets,
    fetchGoals,
    fetchAll,
  }
}