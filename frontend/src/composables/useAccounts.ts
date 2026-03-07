/**
 * composables/useAccount.ts
 *
 * Centralised state + API layer for the Accounts resource.
 *
 * Design decisions:
 * ─ Uses the same raw fetch() + Bearer pattern as useAuth.ts.
 *   No Axios dependency — keeps the auth strategy consistent.
 * ─ Module-level refs so state is shared as a singleton across
 *   every component that calls useAccount() in the same app session.
 */

import { ref, computed } from 'vue'
import { useAuth } from './useAuth'

// ── Constants ─────────────────────────────────────────────────────────────────
const API_BASE = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000/api/v1'

// ── Types ─────────────────────────────────────────────────────────────────────
export type AccountType  = 'bank' | 'ewallet' | 'cash'
export type CurrencyCode = 'MYR' | 'USD' | 'EUR' | 'SGD' | 'GBP'

export interface IAccount {
  id:           string
  user_id:      string
  name:         string
  account_type: AccountType
  currency:     CurrencyCode
  balance:      number
  institution:  string | null
  notes:        string | null
  is_active:    boolean
  theme:        string
  last4:        string
  created_at:   string
  updated_at:   string
}

export interface ICreateAccountPayload {
  name:             string
  account_type:     AccountType
  currency:         CurrencyCode
  institution?:     string | null
  notes?:           string | null
  opening_balance?: number
}

export interface IUpdateAccountPayload {
  name?:         string
  account_type?: AccountType
  currency?:     CurrencyCode
  institution?:  string | null
  notes?:        string | null
  is_active?:    boolean
}

export interface IAccountListResponse {
  items:         IAccount[]
  total:         number
  active_count:  number
  total_balance: number
}

export interface IDeleteAccountResponse {
  deleted:    boolean
  account_id: string
  message:    string
}

// ── Helpers ───────────────────────────────────────────────────────────────────
function normalise(a: IAccount): IAccount {
  return { ...a, balance: Number(a.balance) }
}

// ── Singleton state ───────────────────────────────────────────────────────────
const accounts     = ref<IAccount[]>([])
const loading      = ref(false)
const error        = ref<string | null>(null)
const totalBalance = ref<number>(0)
const activeCount  = ref<number>(0)

// ── Internal fetch helper ─────────────────────────────────────────────────────
async function accountFetch<T>(path: string, options: RequestInit = {}): Promise<T> {
  const { token } = useAuth()
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options.headers as Record<string, string> ?? {}),
  }
  if (token.value) {
    headers['Authorization'] = `Bearer ${token.value}`
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
export function useAccount() {
  const activeAccounts  = computed(() => accounts.value.filter(a => a.is_active))
  const bankAccounts    = computed(() => activeAccounts.value.filter(a => a.account_type === 'bank'))
  const ewalletAccounts = computed(() => activeAccounts.value.filter(a => a.account_type === 'ewallet'))
  const cashAccounts    = computed(() => activeAccounts.value.filter(a => a.account_type === 'cash'))

  async function fetchAccounts(includeInactive = false): Promise<void> {
    loading.value = true
    error.value   = null
    try {
      const params = includeInactive ? '?include_inactive=true' : ''
      const data   = await accountFetch<IAccountListResponse>(`/accounts${params}`)
      accounts.value     = data.items.map(normalise)
      totalBalance.value = Number(data.total_balance)
      activeCount.value  = data.active_count
    } catch (e: unknown) {
      error.value = e instanceof Error ? e.message : 'Failed to load accounts.'
    } finally {
      loading.value = false
    }
  }

  async function createAccount(payload: ICreateAccountPayload): Promise<IAccount> {
    const data = normalise(await accountFetch<IAccount>('/accounts', {
      method: 'POST',
      body:   JSON.stringify(payload),
    }))
    accounts.value.push(data)
    activeCount.value  += 1
    totalBalance.value += data.balance
    return data
  }

  async function updateAccount(id: string, payload: IUpdateAccountPayload): Promise<IAccount> {
    const data = normalise(await accountFetch<IAccount>(`/accounts/${id}`, {
      method: 'PATCH',
      body:   JSON.stringify(payload),
    }))
    const idx = accounts.value.findIndex(a => a?.id === id)
    const old = accounts.value[idx]
    if (idx !== -1 && old) {
      totalBalance.value = totalBalance.value - old.balance + data.balance
      accounts.value[idx] = data
    }
    return data
  }

  async function deleteAccount(id: string): Promise<IDeleteAccountResponse> {
    const data = await accountFetch<IDeleteAccountResponse>(`/accounts/${id}`, {
      method: 'DELETE',
    })
    const idx = accounts.value.findIndex(a => a.id === id)
    if (idx !== -1 && accounts.value[idx]) {
      const target = accounts.value[idx]
      totalBalance.value = Math.max(0, totalBalance.value - target.balance)
      activeCount.value  = Math.max(0, activeCount.value - 1)
      accounts.value[idx] = { ...target, is_active: false }
    }
    return data
  }

  async function getAccount(id: string): Promise<IAccount> {
    return accountFetch<IAccount>(`/accounts/${id}`)
  }

  function clearError(): void {
    error.value = null
  }

  return {
    accounts,
    loading,
    error,
    totalBalance,
    activeCount,
    activeAccounts,
    bankAccounts,
    ewalletAccounts,
    cashAccounts,
    fetchAccounts,
    createAccount,
    updateAccount,
    deleteAccount,
    getAccount,
    clearError,
  }
}