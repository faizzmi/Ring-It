/**
 * composables/useAccount.ts
 */

import { ref, computed } from 'vue'
import { useAuth } from './useAuth'

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000/api/v1'

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
  has_more:      boolean   // true when limit was applied and more accounts exist
}

export interface IDeleteAccountResponse {
  deleted:    boolean
  account_id: string
  message:    string
}

function normalise(a: IAccount): IAccount {
  return { ...a, balance: Number(a.balance) }
}

// ── Singleton state ───────────────────────────────────────────────────────────
const accounts     = ref<IAccount[]>([])
const loading      = ref(false)
const error        = ref<string | null>(null)
const totalBalance = ref<number>(0)
const activeCount  = ref<number>(0)
const hasMore      = ref<boolean>(false)  // server says there are more accounts than returned

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

export function useAccount() {
  const activeAccounts  = computed(() => accounts.value.filter(a => a.is_active))
  const bankAccounts    = computed(() => activeAccounts.value.filter(a => a.account_type === 'bank'))
  const ewalletAccounts = computed(() => activeAccounts.value.filter(a => a.account_type === 'ewallet'))
  const cashAccounts    = computed(() => activeAccounts.value.filter(a => a.account_type === 'cash'))

  // True when the last fetchAccounts call used a limit and more accounts exist on the server
  const hasMoreAccounts = computed(() => hasMore.value)

  /**
   * Fetch accounts from the server.
   *
   * @param limit  Optional max number of accounts to return in `items`.
   *               The server still returns the real `active_count` and sets
   *               `has_more = true` when the result was truncated.
   *               Pass `undefined` (default) to fetch all accounts.
   * @param includeInactive  Include soft-deleted accounts.
   */
  async function fetchAccounts(limit?: number, includeInactive = false): Promise<void> {
    loading.value = true
    error.value   = null
    try {
      const params = new URLSearchParams()
      if (includeInactive) params.set('include_inactive', 'true')
      if (limit !== undefined) params.set('limit', String(limit))
      const qs   = params.toString() ? `?${params.toString()}` : ''
      const data = await accountFetch<IAccountListResponse>(`/accounts${qs}`)
      accounts.value     = data.items.map(normalise)
      totalBalance.value = Number(data.total_balance)
      activeCount.value  = data.active_count
      hasMore.value      = data.has_more
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
    hasMoreAccounts,
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