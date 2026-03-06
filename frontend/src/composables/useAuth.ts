/**
 * composables/useAuth.ts
 * Wraps all Ring-It auth API calls.
 */
import { ref, computed, reactive } from 'vue'
import { useRouter } from 'vue-router'

// ── Types ─────────────────────────────────────────────────────────────────────

export interface IUser {
  id: string
  email: string
  full_name: string
  currency: string
  is_active: boolean
  is_verified: boolean
  created_at: string
  last_login_at: string | null
}

export interface ITokens {
  access_token: string
  refresh_token: string
  token_type: string
  expires_in: number
}

export interface IAuthResponse {
  user: IUser
  tokens: ITokens
}

export interface IRegisterPayload {
  full_name: string
  email: string
  password: string
  currency?: string
}

export interface ILoginPayload {
  email: string
  password: string
}

// Add to interfaces section
export interface IForgotPasswordPayload {
  email: string
}

export interface IResetPasswordPayload {
  token: string
  new_password: string
}

// ── Constants ─────────────────────────────────────────────────────────────────

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'

const ACCESS_TOKEN_KEY  = 'ringit_access_token'
const REFRESH_TOKEN_KEY = 'ringit_refresh_token'
const USER_KEY          = 'ringit_user'

// ── Shared singleton state ────────────────────────────────────────────────────

const user    = ref<IUser | null>(JSON.parse(localStorage.getItem(USER_KEY) ?? 'null'))
const token   = ref<string | null>(localStorage.getItem(ACCESS_TOKEN_KEY))
const loading = ref(false)
const error   = ref<string | null>(null)

// Modal state — drives RegisterSuccessModal + AuthErrorModal
const modals = reactive({
  success: false,
  error:   false,
})
const modalData = reactive({
  registeredName:  '',
  registeredEmail: '',
  errorMessage:    '',
  errorCode:       0,
})

// ── Helpers ───────────────────────────────────────────────────────────────────

function persistSession(tokens: ITokens, userData: IUser) {
  localStorage.setItem(ACCESS_TOKEN_KEY,  tokens.access_token)
  localStorage.setItem(REFRESH_TOKEN_KEY, tokens.refresh_token)
  localStorage.setItem(USER_KEY, JSON.stringify(userData))
  token.value = tokens.access_token
  user.value  = userData
}

function clearSession() {
  localStorage.removeItem(ACCESS_TOKEN_KEY)
  localStorage.removeItem(REFRESH_TOKEN_KEY)
  localStorage.removeItem(USER_KEY)
  token.value = null
  user.value  = null
}

async function apiFetch<T>(
  path: string,
  options: RequestInit = {},
  withAuth = false,
): Promise<T> {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options.headers as Record<string, string> ?? {}),
  }
  if (withAuth && token.value) {
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

export function useAuth() {
  const router = useRouter()

  const isAuthenticated = computed(() => !!token.value && !!user.value)

  async function register(payload: IRegisterPayload): Promise<void> {
    loading.value = true
    error.value   = null
    try {
      const data = await apiFetch<IAuthResponse>('/auth/register', {
        method: 'POST',
        body: JSON.stringify({ currency: 'MYR', ...payload }),
      })
      persistSession(data.tokens, data.user)
      modalData.registeredName  = payload.full_name
      modalData.registeredEmail = payload.email
      modals.success = true
    } catch (e: unknown) {
      const status = (e as Error & { status?: number }).status ?? 0
      error.value            = e instanceof Error ? e.message : 'Registration failed.'
      modalData.errorMessage = error.value
      modalData.errorCode    = status
      modals.error = true
      throw e
    } finally {
      loading.value = false
    }
  }

  async function login(payload: ILoginPayload): Promise<void> {
    loading.value = true
    error.value   = null
    try {
      const data = await apiFetch<IAuthResponse>('/auth/login', {
        method: 'POST',
        body: JSON.stringify(payload),
      })
      persistSession(data.tokens, data.user)
      await router.push('/dashboard')
    } catch (e: unknown) {
      const status = (e as Error & { status?: number }).status ?? 0
      error.value            = e instanceof Error ? e.message : 'Login failed.'
      modalData.errorMessage = error.value
      modalData.errorCode    = status
      modals.error = true
      throw e
    } finally {
      loading.value = false
    }
  }

  async function refreshToken(): Promise<string | null> {
    const storedRefresh = localStorage.getItem(REFRESH_TOKEN_KEY)
    if (!storedRefresh) { clearSession(); return null }
    try {
      const data = await apiFetch<ITokens>('/auth/refresh', {
        method: 'POST',
        body: JSON.stringify({ refresh_token: storedRefresh }),
      })
      localStorage.setItem(ACCESS_TOKEN_KEY,  data.access_token)
      localStorage.setItem(REFRESH_TOKEN_KEY, data.refresh_token)
      token.value = data.access_token
      return data.access_token
    } catch {
      clearSession()
      return null
    }
  }

  async function fetchMe(): Promise<IUser> {
    const data = await apiFetch<IUser>('/auth/me', {}, true)
    user.value = data
    localStorage.setItem(USER_KEY, JSON.stringify(data))
    return data
  }

  async function logout(): Promise<void> {
    try {
      await apiFetch('/auth/logout', { method: 'POST' }, true)
    } catch { /* ignore — clear session regardless */ }
    clearSession()
    await router.push('/login')
  }

  async function verifyEmail(token: string): Promise<void> {
    await apiFetch(`/auth/verify-email?token=${encodeURIComponent(token)}`, {
      method: 'POST',
    })
  }

  async function resendVerification(email: string): Promise<void> {
    await apiFetch(`/auth/resend-verification?email=${encodeURIComponent(email)}`, {
      method: 'POST',
    })
  }

  async function forgotPassword(payload: IForgotPasswordPayload): Promise<void> {
    loading.value = true
    error.value   = null
    try {
      await apiFetch('/auth/forgot-password', {
        method: 'POST',
        body: JSON.stringify(payload),
      })
    } finally {
      loading.value = false
    }
  }

  async function resetPassword(payload: IResetPasswordPayload): Promise<void> {
    loading.value = true
    error.value   = null
    try {
      await apiFetch('/auth/reset-password', {
        method: 'POST',
        body: JSON.stringify(payload),
      })
    } catch (e: unknown) {
      error.value = e instanceof Error ? e.message : 'Reset failed.'
      throw e
    } finally {
      loading.value = false
    }
  }
  return {
    user,
    token,
    loading,
    error,
    isAuthenticated,
    modals,
    modalData,

    register,
    login,
    refreshToken,
    fetchMe,
    logout,
    verifyEmail,
    resendVerification,
    forgotPassword,
    resetPassword,
  }
}