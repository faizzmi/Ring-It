/**
 * composables/useTransactions.ts
 * Manages transactions: fetch, create, update, delete, bulk import.
 * Field names match backend schema exactly (TxnResponse, CreateTxnRequest).
 */
import { ref, computed } from 'vue'

// ── Types ─────────────────────────────────────────────────────────────────────

export interface IAccountSummary {
  id:           string
  name:         string
  institution:  string | null
  account_type: string
}

export interface ITransaction {
  id:                     string
  user_id:                string
  account_id:             string
  account:                IAccountSummary
  txn_type:               'income' | 'expense' | 'transfer'
  amount:                 string
  category:               string
  subcategory:            string | null
  division:               string | null
  txn_date:               string
  description:            string | null
  store:                  string | null
  notes:                  string | null
  is_tax_deductible:      boolean
  cloudinary_url:         string | null
  transfer_to_account_id: string | null
  created_at:             string
  updated_at:             string
}

export interface ITransactionCreate {
  account_id:              string
  amount:                  number
  txn_type:                'income' | 'expense' | 'transfer'
  category:                'commitment' | 'want' | 'savings' | 'income'
  subcategory?:            string | null
  division:                'commitment' | 'want' | 'savings' | 'income'
  txn_date:                string
  description?:            string | null
  store?:                  string | null
  notes?:                  string | null
  is_tax_deductible?:      boolean
  idempotency_key:         string
  transfer_to_account_id?: string | null
  cloudinary_url?:         string | null
}

export interface ITransactionUpdate {
  description?:    string | null
  store?:          string | null
  notes?:          string | null
  is_tax_deductible?: boolean
  cloudinary_url?: string | null
  category?:       'commitment' | 'want' | 'savings' | 'income'
  subcategory?:    string | null
  division?:       'commitment' | 'want' | 'savings' | 'income'
}

export interface ITransactionFilters {
  account_id?: string
  txn_type?:   'income' | 'expense' | 'transfer'
  category?:   string
  division?:   string
  date_from?:  string
  date_to?:    string
  limit?:      number
  offset?:     number
}

export interface IBulkImportResponse {
  imported: number
  skipped:  number
  errors:   { row: number; reason: string }[]
  message:  string
}

interface TxnListResponse {
  total:  number
  limit:  number
  offset: number
  items:  ITransaction[]
}

// ── Constants ─────────────────────────────────────────────────────────────────

const API_BASE         = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000/api/v1'
const ACCESS_TOKEN_KEY = 'ringit_access_token'

// ── Singleton state ───────────────────────────────────────────────────────────

const transactions = ref<ITransaction[]>([])
const loading      = ref(false)
const error        = ref<string | null>(null)

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

export function useTransactions() {
  const todayStr = new Date().toISOString().slice(0, 10)

  // ── Derived ───────────────────────────────────────────────────────────────

  const todayTransactions = computed(() =>
    transactions.value
      .filter(t => t.txn_date === todayStr)
      .sort((a, b) => b.created_at.localeCompare(a.created_at))
  )

  const recentTransactions = computed(() =>
    [...transactions.value]
      .filter(t => t.txn_date !== todayStr)
      .sort((a, b) => {
        const d = b.txn_date.localeCompare(a.txn_date)
        return d !== 0 ? d : b.created_at.localeCompare(a.created_at)
      })
      .slice(0, 10)
  )

  const todayNet = computed(() =>
    todayTransactions.value.reduce((sum, t) => {
      const amt = parseFloat(t.amount)
      return t.txn_type === 'income' ? sum + amt : sum - amt
    }, 0)
  )

  const monthlyIncome = computed(() => {
    const prefix = todayStr.slice(0, 7)
    return transactions.value
      .filter(t => t.txn_type === 'income' && t.txn_date.startsWith(prefix))
      .reduce((sum, t) => sum + parseFloat(t.amount), 0)
  })

  const monthlyExpenses = computed(() => {
    const prefix = todayStr.slice(0, 7)
    return transactions.value
      .filter(t => (t.txn_type === 'expense' || t.txn_type === 'transfer') && t.txn_date.startsWith(prefix))
      .reduce((sum, t) => sum + parseFloat(t.amount), 0)
  })

  // ── API calls ─────────────────────────────────────────────────────────────

  async function fetchTransactions(filters?: ITransactionFilters): Promise<void> {
    loading.value = true
    error.value   = null
    try {
      const params = new URLSearchParams()
      if (filters?.account_id) params.set('account_id', filters.account_id)
      if (filters?.txn_type)   params.set('txn_type',   filters.txn_type)
      if (filters?.category)   params.set('category',   filters.category)
      if (filters?.division)   params.set('division',   filters.division)
      if (filters?.date_from)  params.set('date_from',  filters.date_from)
      if (filters?.date_to)    params.set('date_to',    filters.date_to)
      if (filters?.limit)      params.set('limit',      String(filters.limit))
      if (filters?.offset)     params.set('offset',     String(filters.offset))
      const qs   = params.toString()
      const data = await apiFetch<TxnListResponse>(
        `/transactions${qs ? `?${qs}` : ''}`,
        {},
        true,
      )
      transactions.value = data.items
    } catch (e: unknown) {
      error.value = e instanceof Error ? e.message : 'Failed to load transactions.'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function fetchByAccount(accountId: string): Promise<void> {
    return fetchTransactions({ account_id: accountId, limit: 200 })
  }

  async function fetchTodayTransactions(): Promise<void> {
    return fetchTransactions({ date_from: todayStr, date_to: todayStr })
  }

  async function createTransaction(payload: ITransactionCreate): Promise<ITransaction> {
    loading.value = true
    error.value   = null
    try {
      const data = await apiFetch<ITransaction>(
        '/transactions',
        { method: 'POST', body: JSON.stringify(payload) },
        true,
      )
      transactions.value.unshift(data)
      return data
    } catch (e: unknown) {
      error.value = e instanceof Error ? e.message : 'Failed to create transaction.'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function updateTransaction(id: string, payload: ITransactionUpdate): Promise<ITransaction> {
    loading.value = true
    error.value   = null
    try {
      const data = await apiFetch<ITransaction>(
        `/transactions/${id}`,
        { method: 'PATCH', body: JSON.stringify(payload) },
        true,
      )
      const idx = transactions.value.findIndex(t => t.id === id)
      if (idx !== -1) transactions.value[idx] = data
      return data
    } catch (e: unknown) {
      error.value = e instanceof Error ? e.message : 'Failed to update transaction.'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function deleteTransaction(id: string): Promise<void> {
    loading.value = true
    error.value   = null
    try {
      await apiFetch<void>(`/transactions/${id}`, { method: 'DELETE' }, true)
      transactions.value = transactions.value.filter(t => t.id !== id)
    } catch (e: unknown) {
      error.value = e instanceof Error ? e.message : 'Failed to delete transaction.'
      throw e
    } finally {
      loading.value = false
    }
  }

  /**
   * Bulk import from CSV or XLSX.
   * Sends multipart/form-data — no Content-Type header so browser sets boundary automatically.
   * After a successful import, re-fetches the full transaction list so the UI reflects all new rows.
   */
  async function importTransactions(
    file: File,
    defaultAccountId: string,
  ): Promise<IBulkImportResponse> {
    loading.value = true
    error.value   = null
    try {
      const token = localStorage.getItem(ACCESS_TOKEN_KEY)
      const form  = new FormData()
      form.append('file', file)
      form.append('default_account_id', defaultAccountId)

      const res = await fetch(`${API_BASE}/transactions/import`, {
        method:  'POST',
        headers: token ? { Authorization: `Bearer ${token}` } : {},
        body:    form,
        // DO NOT set Content-Type — browser must set it with the multipart boundary
      })

      if (!res.ok) {
        const body = await res.json().catch(() => ({}))
        const err  = new Error(body?.detail ?? `Import failed: ${res.status}`) as Error & { status: number }
        err.status = res.status
        throw err
      }

      const result: IBulkImportResponse = await res.json()

      // Re-fetch so imported rows appear immediately
      await fetchTransactions({ limit: 200 })

      return result
    } catch (e: unknown) {
      error.value = e instanceof Error ? e.message : 'Import failed.'
      throw e
    } finally {
      loading.value = false
    }
  }

  return {
    transactions,
    loading,
    error,
    todayTransactions,
    recentTransactions,
    todayNet,
    monthlyIncome,
    monthlyExpenses,
    fetchTransactions,
    fetchByAccount,
    fetchTodayTransactions,
    createTransaction,
    updateTransaction,
    deleteTransaction,
    importTransactions,
  }
}