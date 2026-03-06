<template>
    <div class="page-root">
  
      <AuthAmbient />
      <AuthNav link-href="/login" link-label="Back to Login" />
  
      <section class="auth-section">
        <div class="auth-layout">
  
          <!-- LEFT PANEL -->
          <div class="auth-panel auth-panel--left auth-fade-left">
            <div class="panel-badge">
              <span class="sov-pulse" />
              <span class="t-mono" style="font-size:9px;letter-spacing:2px">VAULT RECOVERY TERMINAL</span>
            </div>
            <h1 class="panel-h1 t-display">
              Reclaim<br />
              <span class="t-accent">Your Access.</span>
            </h1>
            <p class="panel-body t-body">
              Set a new password for your vault. Choose something strong — your financial data deserves it.
            </p>
            <div class="panel-stats">
              <div class="panel-stat">
                <span class="stat-val t-display">AES-256</span>
                <span class="stat-label t-label">encryption</span>
              </div>
              <div class="panel-divider" />
              <div class="panel-stat">
                <span class="stat-val t-display">1hr</span>
                <span class="stat-label t-label">link expiry</span>
              </div>
              <div class="panel-divider" />
              <div class="panel-stat">
                <span class="stat-val t-display">1×</span>
                <span class="stat-label t-label">single use</span>
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
                  <span class="t-mono" style="font-size:9px;letter-spacing:2.5px;color:var(--gun)">// PASSWORD RESET</span>
                </div>
                <span class="sov-chip sov-chip--green">
                  <span style="width:5px;height:5px;background:var(--grn);border-radius:50%;display:inline-block;" />
                  Secure
                </span>
              </div>
  
              <!-- Invalid / expired token state -->
              <template v-if="tokenError">
                <div class="status-block">
                  <div class="status-icon status-icon--error">
                    <svg width="28" height="28" viewBox="0 0 28 28" fill="none">
                      <circle cx="14" cy="14" r="13" stroke="rgba(180,40,60,0.5)" stroke-width="1.2"/>
                      <path d="M9 9l10 10M19 9L9 19" stroke="rgba(180,40,60,0.9)" stroke-width="1.5" stroke-linecap="round"/>
                    </svg>
                  </div>
                  <h2 class="auth-title t-display">Link Invalid</h2>
                  <p class="auth-sub-body t-body">
                    This reset link is invalid or has expired. Reset links are single-use and expire after 1 hour.
                  </p>
                  <a href="/login" class="sov-btn sov-btn--primary sov-btn--lg auth-submit" style="text-decoration:none;display:flex;align-items:center;justify-content:center;gap:6px;">
                    Back to Login
                  </a>
                </div>
              </template>
  
              <!-- Success state -->
              <template v-else-if="success">
                <div class="status-block">
                  <div class="status-icon status-icon--success">
                    <svg width="28" height="28" viewBox="0 0 28 28" fill="none">
                      <circle cx="14" cy="14" r="13" stroke="rgba(76,175,80,0.5)" stroke-width="1.2"/>
                      <path d="M8 14l4 4 8-8" stroke="rgba(76,175,80,0.9)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                  </div>
                  <h2 class="auth-title t-display">Password Reset</h2>
                  <p class="auth-sub-body t-body">
                    Your vault password has been updated. You can now sign in with your new credentials.
                  </p>
                  <a href="/login" class="sov-btn sov-btn--primary sov-btn--lg auth-submit" style="text-decoration:none;display:flex;align-items:center;justify-content:center;gap:6px;">
                    Enter Vault
                    <svg width="13" height="13" viewBox="0 0 13 13" fill="none">
                      <path d="M2.5 6.5h8M6.5 2.5l4 4-4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                  </a>
                </div>
              </template>
  
              <!-- Form state -->
              <template v-else>
                <h2 class="auth-title t-display">New Password</h2>
                <p class="auth-sub t-mono">Choose a strong password for your vault.</p>
  
                <form class="auth-form" @submit.prevent="handleSubmit" novalidate>
  
                  <AuthField
                    id="password"
                    label="// New Password"
                    type="password"
                    v-model="form.password"
                    placeholder="••••••••••••"
                    autocomplete="new-password"
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
  
                  <AuthField
                    id="confirm-password"
                    label="// Confirm Password"
                    type="password"
                    v-model="form.confirmPassword"
                    placeholder="••••••••••••"
                    autocomplete="new-password"
                    :error="errors.confirmPassword"
                    :show-value="showConfirm"
                    @blur="validateConfirm"
                  >
                    <template #icon>
                      <svg width="13" height="13" viewBox="0 0 13 13" fill="none">
                        <rect x="3" y="6" width="7" height="6" rx="1" stroke="currentColor" stroke-width="1.2"/>
                        <path d="M4.5 6V4.5a2 2 0 0 1 4 0V6" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/>
                      </svg>
                    </template>
                    <template #toggle>
                      <AuthPasswordToggle :show="showConfirm" @toggle="showConfirm = !showConfirm" />
                    </template>
                  </AuthField>
  
                  <!-- Password strength indicator -->
                  <div class="strength-wrap" v-if="form.password">
                    <div class="strength-bars">
                      <span
                        v-for="i in 4"
                        :key="i"
                        class="strength-bar"
                        :class="{ active: strength >= i, [`s${strength}`]: strength >= i }"
                      />
                    </div>
                    <span class="strength-label t-mono">{{ strengthLabel }}</span>
                  </div>
  
                  <AuthError :message="serverError" />
  
                  <button
                    type="submit"
                    class="sov-btn sov-btn--primary sov-btn--lg auth-submit"
                    :class="{ loading }"
                    :disabled="loading"
                  >
                    <span v-if="!loading">
                      Set New Password
                      <svg width="13" height="13" viewBox="0 0 13 13" fill="none" style="margin-left:4px">
                        <path d="M2.5 6.5h8M6.5 2.5l4 4-4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                      </svg>
                    </span>
                    <span v-else class="auth-spinner" />
                  </button>
  
                </form>
  
                <div class="auth-footer-row">
                  <span class="t-mono" style="font-size:9.5px;color:var(--gun)">Remember your password?</span>
                  <a href="/login" class="auth-link t-mono">Back to login →</a>
                </div>
              </template>
  
            </div>
          </div>
  
        </div>
      </section>
  
      <AuthFooter />
  
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref, reactive, computed, onMounted } from 'vue'
  import { useRoute } from 'vue-router'
  import { useAuth } from '@/composables/useAuth'
  import AuthAmbient        from '@/components/auth/AuthAmbient.vue'
  import AuthNav            from '@/components/auth/AuthNav.vue'
  import AuthFooter         from '@/components/auth/AuthFooter.vue'
  import AuthField          from '@/components/auth/AuthField.vue'
  import AuthPasswordToggle from '@/components/auth/AuthPasswordToggle.vue'
  import AuthError          from '@/components/auth/AuthError.vue'
  
  const route = useRoute()
  const { resetPassword, loading, error } = useAuth()
  
  const token       = ref('')
  const tokenError  = ref(false)
  const success     = ref(false)
  const serverError = computed(() => error.value || '')
  const showPassword = ref(false)
  const showConfirm  = ref(false)
  
  const form   = reactive({ password: '', confirmPassword: '' })
  const errors = reactive({ password: '', confirmPassword: '' })
  
  onMounted(() => {
    const t = route.query.token
    if (!t || typeof t !== 'string') {
      tokenError.value = true
    } else {
      token.value = t
    }
  })
  
  // ── Password strength ─────────────────────────────────────────────────────────
  const strength = computed(() => {
    const p = form.password
    if (!p) return 0
    let score = 0
    if (p.length >= 8)  score++
    if (p.length >= 12) score++
    if (/[A-Z]/.test(p) && /[a-z]/.test(p)) score++
    if (/[0-9]/.test(p) && /[^A-Za-z0-9]/.test(p)) score++
    return score
  })
  
  const strengthLabel = computed(() => {
    return ['', 'Weak', 'Fair', 'Good', 'Strong'][strength.value] || ''
  })
  
  // ── Validation ────────────────────────────────────────────────────────────────
  function validatePassword() {
    if (!form.password) { errors.password = 'Password is required.'; return false }
    if (form.password.length < 8) { errors.password = 'Minimum 8 characters.'; return false }
    errors.password = ''; return true
  }
  
  function validateConfirm() {
    if (!form.confirmPassword) { errors.confirmPassword = 'Please confirm your password.'; return false }
    if (form.confirmPassword !== form.password) { errors.confirmPassword = 'Passwords do not match.'; return false }
    errors.confirmPassword = ''; return true
  }
  
  // ── Submit ────────────────────────────────────────────────────────────────────
  async function handleSubmit() {
    error.value = ''
    if (!validatePassword() || !validateConfirm()) return
    try {
      await resetPassword({ token: token.value, new_password: form.password })
      success.value = true
    } catch (e: any) {
      const status = e?.response?.status
      if (status === 400) {
        tokenError.value = true
      }
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
  .auth-sub-body    { font-size: .86rem; color: rgba(224,224,224,.6); line-height: 1.75; margin-bottom: 24px; }
  .auth-form        { display: flex; flex-direction: column; gap: 18px; margin-bottom: 20px; }
  .auth-submit      { width: 100%; justify-content: center; margin-top: 4px; position: relative; }
  .auth-submit.loading { pointer-events: none; opacity: .7; }
  .auth-spinner     { display: inline-block; width: 14px; height: 14px; border: 2px solid rgba(224,224,224,.2); border-top-color: rgba(224,224,224,.8); border-radius: 50%; animation: spin .7s linear infinite; }
  @keyframes spin   { to { transform: rotate(360deg); } }
  .auth-footer-row  { display: flex; align-items: center; justify-content: center; gap: 8px; padding-top: 18px; border-top: 1px solid rgba(224,224,224,.06); }
  .auth-link        { font-size: 9.5px; letter-spacing: .5px; color: var(--ox); background: none; border: none; cursor: pointer; padding: 0; transition: color .18s; text-decoration: none; }
  .auth-link:hover  { color: rgba(200,50,80,0.9); }
  .auth-fade-left   { opacity: 0; transform: translateY(14px); animation: authFadeIn 0.38s cubic-bezier(0.22,1,0.36,1) 0.05s forwards; }
  .auth-fade-right  { opacity: 0; transform: translateY(14px); animation: authFadeIn 0.38s cubic-bezier(0.22,1,0.36,1) 0.18s forwards; }
  @keyframes authFadeIn { to { opacity: 1; transform: translateY(0); } }
  
  /* ── Status blocks (success / error) ── */
  .status-block      { display: flex; flex-direction: column; align-items: center; text-align: center; gap: 8px; padding: 8px 0; }
  .status-icon       { margin-bottom: 8px; }
  
  /* ── Password strength ── */
  .strength-wrap  { display: flex; align-items: center; gap: 10px; margin-top: -6px; }
  .strength-bars  { display: flex; gap: 4px; }
  .strength-bar   { width: 32px; height: 3px; border-radius: 2px; background: rgba(224,224,224,.1); transition: background .25s; }
  .strength-bar.active.s1 { background: rgba(180,40,60,0.8); }
  .strength-bar.active.s2 { background: rgba(220,150,40,0.8); }
  .strength-bar.active.s3 { background: rgba(100,180,80,0.7); }
  .strength-bar.active.s4 { background: rgba(76,175,80,0.9); }
  .strength-label { font-size: 9px; letter-spacing: 1.5px; color: var(--gun); }
  </style>