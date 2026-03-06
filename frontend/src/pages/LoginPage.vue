<template>
  <div class="page-root">

    <AuthAmbient />
    <AuthNav link-href="/register" link-label="Create Account" />

    <section class="auth-section">
      <div class="auth-layout">

        <!-- LEFT PANEL -->
        <div class="auth-panel auth-panel--left auth-fade-left">
          <div class="panel-badge">
            <span class="sov-pulse" />
            <span class="t-mono" style="font-size:9px;letter-spacing:2px">VAULT ACCESS TERMINAL</span>
          </div>
          <h1 class="panel-h1 t-display">
            Re-enter<br />
            <span class="t-accent">Your Ledger.</span>
          </h1>
          <p class="panel-body t-body">
            Your financial vault awaits. Every session continues where you left off — net worth, nudges, and your 10-year projection.
          </p>
          <div class="panel-stats">
            <div class="panel-stat">
              <span class="stat-val t-display">RM 0</span>
              <span class="stat-label t-label">fees charged</span>
            </div>
            <div class="panel-divider" />
            <div class="panel-stat">
              <span class="stat-val t-display">7yr</span>
              <span class="stat-label t-label">receipt retention</span>
            </div>
            <div class="panel-divider" />
            <div class="panel-stat">
              <span class="stat-val t-display">AES-256</span>
              <span class="stat-label t-label">encryption</span>
            </div>
          </div>
          <div class="panel-chips">
            <span class="sov-chip sov-chip--green">PDPA 2010</span>
            <span class="sov-chip sov-chip--ghost">BNM RMIT</span>
            <span class="sov-chip sov-chip--ghost">LHDN 2026</span>
          </div>
        </div>

        <!-- RIGHT PANEL -->
        <div class="auth-panel auth-panel--right auth-fade-right">
          <div class="sov-card auth-card">

            <div class="auth-card-header">
              <div class="auth-header-row">
                <span class="modal-dot" />
                <span class="t-mono" style="font-size:9px;letter-spacing:2.5px;color:var(--gun)">// VAULT LOGIN</span>
              </div>
              <span class="sov-chip sov-chip--green">
                <span style="width:5px;height:5px;background:var(--grn);border-radius:50%;display:inline-block;" />
                Secure
              </span>
            </div>

            <h2 class="auth-title t-display">Sign In</h2>
            <p class="auth-sub t-mono">Access your personal wealth system.</p>

            <form class="auth-form" @submit.prevent="handleLogin" novalidate>

              <AuthField
                id="email"
                label="// Email Address"
                type="email"
                v-model="form.email"
                placeholder="you@example.com"
                autocomplete="email"
                :error="errors.email"
                @blur="validateEmail"
              >
                <template #icon>
                  <svg width="13" height="13" viewBox="0 0 13 13" fill="none">
                    <rect x="1" y="3" width="11" height="8" rx="1.5" stroke="currentColor" stroke-width="1.2"/>
                    <path d="M1 4.5L6.5 8L12 4.5" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/>
                  </svg>
                </template>
              </AuthField>

              <AuthField
                id="password"
                label="// Password"
                type="password"
                v-model="form.password"
                placeholder="••••••••••••"
                autocomplete="current-password"
                :error="errors.password"
                :show-value="showPassword"
                @blur="validatePassword"
              >
                <template #icon>
                  <svg width="13" height="13" viewBox="0 0 13 13" fill="none">
                    <rect x="3" y="6" width="7" height="6" rx="1" stroke="currentColor" stroke-width="1.2"/>
                    <path d="M4.5 6V4.5a2 2 0 0 1 4 0V6" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/>
                  </svg>
                </template>
                <template #toggle>
                  <AuthPasswordToggle :show="showPassword" @toggle="showPassword = !showPassword" />
                </template>
              </AuthField>

              <div class="auth-meta">
                <AuthCheckbox v-model="form.remember">
                  <span style="font-size:9.5px;color:var(--gun)">Keep me logged in</span>
                </AuthCheckbox>
                <!-- Forgot password — opens modal instead of navigating -->
                <button type="button" class="auth-link t-mono" @click="openForgotModal">
                  Forgot password?
                </button>
              </div>

              <AuthError :message="serverError" />

              <button
                type="submit"
                class="sov-btn sov-btn--primary sov-btn--lg auth-submit"
                :class="{ loading }"
                :disabled="loading"
              >
                <span v-if="!loading">
                  Enter Vault
                  <svg width="13" height="13" viewBox="0 0 13 13" fill="none" style="margin-left:4px">
                    <path d="M2.5 6.5h8M6.5 2.5l4 4-4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </span>
                <span v-else class="auth-spinner" />
              </button>

            </form>

            <div class="auth-footer-row">
              <span class="t-mono" style="font-size:9.5px;color:var(--gun)">No account yet?</span>
              <a href="/register" class="auth-link t-mono">Create one free →</a>
            </div>

          </div>
        </div>

      </div>
    </section>

    <AuthFooter />

    <!-- ── Forgot Password Modal ─────────────────────────────────────── -->
    <Teleport to="body">
      <Transition name="modal-fade">
        <div v-if="forgotModal.open" class="modal-backdrop" @click.self="closeForgotModal">
          <div class="modal-box sov-card">

            <!-- Header -->
            <div class="modal-header">
              <div class="auth-header-row">
                <span class="modal-dot" />
                <span class="t-mono" style="font-size:9px;letter-spacing:2.5px;color:var(--gun)">// PASSWORD RESET</span>
              </div>
              <button class="modal-close" @click="closeForgotModal" aria-label="Close">
                <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
                  <path d="M1 1l10 10M11 1L1 11" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                </svg>
              </button>
            </div>

            <!-- Sent state -->
            <template v-if="forgotModal.sent">
              <div class="modal-sent">
                <div class="sent-icon">
                  <svg width="28" height="28" viewBox="0 0 28 28" fill="none">
                    <circle cx="14" cy="14" r="13" stroke="rgba(76,175,80,0.5)" stroke-width="1.2"/>
                    <path d="M8 14l4 4 8-8" stroke="rgba(76,175,80,0.9)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </div>
                <h3 class="modal-title t-display">Check Your Inbox</h3>
                <p class="modal-body t-body">
                  If <strong>{{ forgotModal.email }}</strong> is registered, a reset link is on its way.
                  The link expires in <strong>1 hour</strong>.
                </p>
                <p class="modal-hint t-mono">Check your spam folder if you don't see it.</p>
                <button class="sov-btn sov-btn--primary sov-btn--lg modal-cta" @click="closeForgotModal">
                  Back to Login
                </button>
              </div>
            </template>

            <!-- Form state -->
            <template v-else>
              <h3 class="modal-title t-display">Forgot Password?</h3>
              <p class="modal-body t-body">
                Enter your vault email and we'll send a secure reset link.
              </p>

              <div class="modal-form">
                <AuthField
                  id="reset-email"
                  label="// Vault Email"
                  type="email"
                  v-model="forgotModal.email"
                  placeholder="you@example.com"
                  autocomplete="email"
                  :error="forgotModal.emailError"
                  @blur="validateForgotEmail"
                  @keydown.enter.prevent="handleForgotSubmit"
                >
                  <template #icon>
                    <svg width="13" height="13" viewBox="0 0 13 13" fill="none">
                      <rect x="1" y="3" width="11" height="8" rx="1.5" stroke="currentColor" stroke-width="1.2"/>
                      <path d="M1 4.5L6.5 8L12 4.5" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/>
                    </svg>
                  </template>
                </AuthField>

                <AuthError :message="forgotModal.serverError" />

                <button
                  class="sov-btn sov-btn--primary sov-btn--lg modal-cta"
                  :class="{ loading: forgotModal.loading }"
                  :disabled="forgotModal.loading"
                  @click="handleForgotSubmit"
                >
                  <span v-if="!forgotModal.loading">
                    Send Reset Link
                    <svg width="13" height="13" viewBox="0 0 13 13" fill="none" style="margin-left:4px">
                      <path d="M2.5 6.5h8M6.5 2.5l4 4-4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                  </span>
                  <span v-else class="auth-spinner" />
                </button>
              </div>
            </template>

          </div>
        </div>
      </Transition>
    </Teleport>

  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { useAuth } from '@/composables/useAuth'
import AuthAmbient        from '@/components/auth/AuthAmbient.vue'
import AuthNav            from '@/components/auth/AuthNav.vue'
import AuthFooter         from '@/components/auth/AuthFooter.vue'
import AuthField          from '@/components/auth/AuthField.vue'
import AuthPasswordToggle from '@/components/auth/AuthPasswordToggle.vue'
import AuthCheckbox       from '@/components/auth/AuthCheckbox.vue'
import AuthError          from '@/components/auth/AuthError.vue'

const { login, forgotPassword, loading, error } = useAuth()
const serverError  = computed(() => error.value || '')
const showPassword = ref(false)
const form   = reactive({ email: '', password: '', remember: false })
const errors = reactive({ email: '', password: '' })

// ── Login ─────────────────────────────────────────────────────────────────────
function validateEmail() {
  if (!form.email) { errors.email = 'Email is required.'; return false }
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) { errors.email = 'Enter a valid email address.'; return false }
  errors.email = ''; return true
}
function validatePassword() {
  if (!form.password) { errors.password = 'Password is required.'; return false }
  if (form.password.length < 8) { errors.password = 'Minimum 8 characters.'; return false }
  errors.password = ''; return true
}
async function handleLogin() {
  error.value = ''
  if (!validateEmail() || !validatePassword()) return
  await login({ email: form.email, password: form.password })
}

// ── Forgot Password Modal ─────────────────────────────────────────────────────
const forgotModal = reactive({
  open:        false,
  sent:        false,
  loading:     false,
  email:       '',
  emailError:  '',
  serverError: '',
})

function openForgotModal() {
  forgotModal.open        = true
  forgotModal.sent        = false
  forgotModal.email       = ''
  forgotModal.emailError  = ''
  forgotModal.serverError = ''
}

function closeForgotModal() {
  forgotModal.open = false
}

function validateForgotEmail() {
  if (!forgotModal.email) { forgotModal.emailError = 'Email is required.'; return false }
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(forgotModal.email)) {
    forgotModal.emailError = 'Enter a valid email address.'; return false
  }
  forgotModal.emailError = ''; return true
}

async function handleForgotSubmit() {
  if (!validateForgotEmail()) return
  forgotModal.loading     = true
  forgotModal.serverError = ''
  try {
    await forgotPassword({ email: forgotModal.email })
    forgotModal.sent = true   // always show success — API never reveals if email exists
  } catch {
    forgotModal.serverError = 'Something went wrong. Please try again.'
  } finally {
    forgotModal.loading = false
  }
}
</script>

<style scoped>
@import '@/styles/main.css';

/* ── Page layout ── */
.page-root    { position: relative; min-height: 100vh; overflow-x: hidden; display: flex; flex-direction: column; }
.auth-section { flex: 1; display: flex; align-items: center; justify-content: center; padding: calc(60px + 48px) 20px 48px; min-height: 100svh; }
.auth-layout  { display: grid; grid-template-columns: 1fr; gap: 40px; width: 100%; max-width: 980px; align-items: center; }
@media (min-width: 860px) { .auth-layout { grid-template-columns: 1fr 420px; gap: 64px; } }

/* ── Left panel ── */
.auth-panel--left  { display: flex; flex-direction: column; gap: 28px; }
.panel-badge       { display: inline-flex; align-items: center; gap: 8px; padding: 5px 14px; background: rgba(224,224,224,.04); border: 1px solid rgba(224,224,224,.08); border-radius: 100px; width: fit-content; }
.panel-h1          { font-size: clamp(2rem, 5vw, 3.4rem); line-height: 1.05; }
.panel-body        { font-size: .86rem; max-width: 380px; line-height: 1.8; }
.panel-stats       { display: flex; align-items: center; gap: 20px; padding: 16px 20px; background: rgba(18,18,20,.6); border: 1px solid var(--glass-bo); border-radius: var(--r-md); width: fit-content; }
.panel-stat        { display: flex; flex-direction: column; gap: 3px; }
.stat-val          { font-size: 1.1rem; font-weight: 800; letter-spacing: -.02em; line-height: 1; }
.stat-label        { font-size: 7.5px; letter-spacing: 1.5px; }
.panel-divider     { width: 1px; height: 32px; background: var(--glass-bo); }
.panel-chips       { display: flex; flex-wrap: wrap; gap: 6px; }

/* ── Auth card ── */
.auth-card        { padding: 28px; }
.auth-card-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px; }
.auth-header-row  { display: flex; align-items: center; gap: 8px; }
.modal-dot        { width: 7px; height: 7px; background: var(--ox); border-radius: 50%; box-shadow: 0 0 8px rgba(128,0,32,0.9); flex-shrink: 0; }
.auth-title       { font-size: clamp(1.5rem, 3vw, 2rem); margin-bottom: 4px; }
.auth-sub         { font-size: 9px; letter-spacing: 1.5px; color: var(--gun); margin-bottom: 26px; }
.auth-form        { display: flex; flex-direction: column; gap: 18px; margin-bottom: 20px; }
.auth-meta        { display: flex; align-items: center; justify-content: space-between; margin-top: -4px; }
.auth-link        { font-size: 9.5px; letter-spacing: .5px; color: var(--ox); background: none; border: none; cursor: pointer; padding: 0; transition: color .18s; }
.auth-link:hover  { color: rgba(200,50,80,0.9); }
.auth-submit      { width: 100%; justify-content: center; margin-top: 4px; position: relative; }
.auth-submit.loading { pointer-events: none; opacity: .7; }
.auth-spinner     { display: inline-block; width: 14px; height: 14px; border: 2px solid rgba(224,224,224,.2); border-top-color: rgba(224,224,224,.8); border-radius: 50%; animation: spin .7s linear infinite; }
@keyframes spin   { to { transform: rotate(360deg); } }
.auth-footer-row  { display: flex; align-items: center; justify-content: center; gap: 8px; padding-top: 18px; border-top: 1px solid rgba(224,224,224,.06); }
.auth-fade-left   { opacity: 0; transform: translateY(14px); animation: authFadeIn 0.38s cubic-bezier(0.22,1,0.36,1) 0.05s forwards; }
.auth-fade-right  { opacity: 0; transform: translateY(14px); animation: authFadeIn 0.38s cubic-bezier(0.22,1,0.36,1) 0.18s forwards; }
@keyframes authFadeIn { to { opacity: 1; transform: translateY(0); } }

/* ── Modal ── */
.modal-backdrop   { position: fixed; inset: 0; background: rgba(8,8,8,0.82); backdrop-filter: blur(6px); display: flex; align-items: center; justify-content: center; z-index: 999; padding: 20px; }
.modal-box        { width: 100%; max-width: 420px; padding: 28px; position: relative; }
.modal-header     { display: flex; align-items: center; justify-content: space-between; margin-bottom: 22px; }
.modal-close      { background: none; border: none; cursor: pointer; color: var(--gun); padding: 4px; transition: color .18s; }
.modal-close:hover { color: var(--ox); }
.modal-title      { font-size: 1.5rem; margin-bottom: 8px; }
.modal-body       { font-size: .86rem; color: rgba(224,224,224,.6); line-height: 1.75; margin-bottom: 24px; }
.modal-hint       { font-size: 9px; letter-spacing: 1px; color: var(--gun); margin-bottom: 24px; }
.modal-form       { display: flex; flex-direction: column; gap: 18px; }
.modal-cta        { width: 100%; justify-content: center; }
.modal-cta.loading { pointer-events: none; opacity: .7; }
.modal-sent       { display: flex; flex-direction: column; align-items: center; text-align: center; gap: 4px; }
.sent-icon        { margin-bottom: 12px; }

/* ── Modal transition ── */
.modal-fade-enter-active, .modal-fade-leave-active { transition: opacity .22s ease, transform .22s cubic-bezier(0.22,1,0.36,1); }
.modal-fade-enter-from, .modal-fade-leave-to       { opacity: 0; transform: scale(0.97); }
</style>