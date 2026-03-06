<template>
  <div class="page-root">

    <AuthAmbient />
    <AuthNav link-href="/login" link-label="Sign In" />

    <section class="auth-section">
      <div class="auth-layout">

        <!-- LEFT PANEL -->
        <div class="auth-panel auth-panel--left auth-fade-left">
          <div class="panel-badge">
            <span class="sov-pulse" />
            <span class="t-mono" style="font-size:9px;letter-spacing:2px">VAULT INITIALISATION</span>
          </div>
          <h1 class="panel-h1 t-display">
            Build Your<br />
            <span class="t-accent">Wealth System.</span>
          </h1>
          <p class="panel-body t-body">
            Your vault is free, private, and built to last. Set it up once — then let behavioral architecture do the work of keeping you rich.
          </p>
          <div class="panel-perks">
            <p class="t-label" style="margin-bottom:10px">// WHAT YOU GET</p>
            <div v-for="p in perks" :key="p" class="perk-row">
              <span class="perk-dot" />
              <span class="t-mono perk-text">{{ p }}</span>
            </div>
          </div>
          <div class="panel-chips">
            <span class="sov-chip sov-chip--green">PDPA 2010</span>
            <span class="sov-chip sov-chip--ghost">BNM RMIT</span>
            <span class="sov-chip sov-chip--ghost">LHDN 2026</span>
            <span class="sov-chip sov-chip--ghost">AES-256</span>
          </div>
        </div>

        <!-- RIGHT PANEL -->
        <div class="auth-panel auth-panel--right auth-fade-right">
          <div class="sov-card auth-card">

            <!-- Step indicator -->
            <div class="step-bar">
              <div v-for="s in 2" :key="s" class="step-item">
                <div class="step-circle t-mono" :class="{ active: step === s, done: step > s }">
                  <svg v-if="step > s" width="9" height="9" viewBox="0 0 9 9" fill="none">
                    <path d="M1.5 4.5L3.5 6.5L7.5 2.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                  <span v-else>{{ s }}</span>
                </div>
                <span class="step-label t-label">{{ s === 1 ? 'Your Details' : 'Set Password' }}</span>
              </div>
              <div class="step-connector" :class="{ done: step > 1 }" />
            </div>

            <div class="auth-card-header">
              <div class="auth-header-row">
                <span class="modal-dot" />
                <span class="t-mono" style="font-size:9px;letter-spacing:2.5px;color:var(--gun)">// NEW VAULT</span>
              </div>
              <span class="sov-chip sov-chip--ox">Step {{ step }} / 2</span>
            </div>

            <h2 class="auth-title t-display">{{ step === 1 ? 'Create Account' : 'Secure Your Vault' }}</h2>
            <p class="auth-sub t-mono">{{ step === 1 ? 'Start your behavioral wealth system.' : 'Set a strong password to protect your data.' }}</p>

            <form class="auth-form" @submit.prevent="handleSubmit" novalidate>

              <!-- STEP 1 -->
              <template v-if="step === 1">

                <AuthField
                  id="name"
                  label="// Full Name"
                  type="text"
                  v-model="form.name"
                  placeholder="John Smith"
                  autocomplete="name"
                  :error="errors.name"
                  @blur="validateName"
                >
                  <template #icon>
                    <svg width="13" height="13" viewBox="0 0 13 13" fill="none">
                      <circle cx="6.5" cy="4.5" r="2" stroke="currentColor" stroke-width="1.2"/>
                      <path d="M2 11c0-2.21 2.02-4 4.5-4s4.5 1.79 4.5 4" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/>
                    </svg>
                  </template>
                </AuthField>

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
                  id="currency"
                  label="// Primary Currency"
                  type="select"
                  v-model="form.currency"
                >
                  <template #icon>
                    <svg width="13" height="13" viewBox="0 0 13 13" fill="none">
                      <circle cx="6.5" cy="6.5" r="5.5" stroke="currentColor" stroke-width="1.2"/>
                      <path d="M6.5 1v11M1 6.5h11" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" opacity=".4"/>
                    </svg>
                  </template>
                  <template #options>
                    <option value="MYR">MYR — Malaysian Ringgit</option>
                    <option value="SGD">SGD — Singapore Dollar</option>
                    <option value="USD">USD — US Dollar</option>
                    <option value="EUR">EUR — Euro</option>
                  </template>
                </AuthField>

              </template>

              <!-- STEP 2 -->
              <template v-else>

                <AuthField
                  id="password"
                  label="// Password"
                  type="password"
                  v-model="form.password"
                  placeholder="Min. 8 characters"
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

                <!-- Strength meter -->
                <div class="strength-row">
                  <div class="sov-track strength-track">
                    <div class="sov-track__fill" :class="strengthFill" :style="{ width: strengthWidth }" />
                  </div>
                  <span class="strength-label t-mono" :class="strengthTextClass">{{ strengthLabel }}</span>
                </div>

                <AuthField
                  id="confirm"
                  label="// Confirm Password"
                  type="password"
                  v-model="form.confirm"
                  placeholder="Repeat password"
                  autocomplete="new-password"
                  :error="errors.confirm"
                  :show-value="showConfirm"
                  @blur="validateConfirm"
                >
                  <template #icon>
                    <svg width="13" height="13" viewBox="0 0 13 13" fill="none">
                      <rect x="3" y="6" width="7" height="6" rx="1" stroke="currentColor" stroke-width="1.2"/>
                      <path d="M4.5 6V4.5a2 2 0 0 1 4 0V6" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/>
                      <path d="M9.5 3.5l1.5-1.5" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" opacity=".5"/>
                    </svg>
                  </template>
                  <template #toggle>
                    <AuthPasswordToggle :show="showConfirm" @toggle="showConfirm = !showConfirm" />
                  </template>
                </AuthField>

                <AuthCheckbox v-model="form.consent" :error="errors.consent">
                  I agree to the
                  <a href="/terms" class="auth-link">Terms of Service</a>,
                  <a href="/privacy" class="auth-link">Privacy Policy</a>, and
                  <a href="/pdpa" class="auth-link">PDPA Notice</a>.
                </AuthCheckbox>

              </template>

              <AuthError :message="serverError" />

              <div class="btn-row">
                <button v-if="step === 2" type="button" class="sov-btn sov-btn--ghost" @click="step = 1">← Back</button>
                <button
                  type="submit"
                  class="sov-btn sov-btn--primary sov-btn--lg auth-submit"
                  :class="{ loading, 'auth-submit--full': step === 1 }"
                  :disabled="loading"
                >
                  <span v-if="!loading">{{ step === 1 ? 'Continue →' : 'Open Vault →' }}</span>
                  <span v-else class="auth-spinner" />
                </button>
              </div>

            </form>

            <div class="auth-footer-row">
              <span class="t-mono" style="font-size:9.5px;color:var(--gun)">Already have a vault?</span>
              <a href="/login" class="auth-link t-mono">Sign in →</a>
            </div>

          </div>
        </div>

      </div>
    </section>

    <AuthFooter />


    <RegisterSuccessModal
      v-model="modals.success"
      :full-name="modalData.registeredName"
      :email="modalData.registeredEmail"
    />

    <AuthErrorModal
      v-model="modals.error"
      :message="modalData.errorMessage"
      :status-code="modalData.errorCode"
    />

  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, watch } from 'vue'
import { useAuth } from '@/composables/useAuth'
import AuthAmbient        from '@/components/auth/AuthAmbient.vue'
import AuthNav            from '@/components/auth/AuthNav.vue'
import AuthFooter         from '@/components/auth/AuthFooter.vue'
import AuthField          from '@/components/auth/AuthField.vue'
import AuthPasswordToggle from '@/components/auth/AuthPasswordToggle.vue'
import AuthCheckbox       from '@/components/auth/AuthCheckbox.vue'
import AuthError          from '@/components/auth/AuthError.vue'
import RegisterSuccessModal from '@/components/auth/RegisterSuccessModal.vue'
import AuthErrorModal       from '@/components/auth/AuthErrorModal.vue'

const { register, loading, error, modals, modalData  } = useAuth()
const serverError = error

const step        = ref(1)
const showPassword = ref(false)
const showConfirm  = ref(false)

const form = reactive({
  name: '', email: '', currency: 'MYR', password: '', confirm: '', consent: false,
})
const errors = reactive({
  name: '', email: '', password: '', confirm: '', consent: '',
})

const perks = [
  'Live DSR + daily budget tracker',
  'LHDN receipt vault — 7yr encrypted',
  'Buy / No-Buy behavioral advisor',
  '10-year compound wealth projection',
  'EPF RIA benchmarking + Zakat calc',
  'No ads. No data selling. Ever.',
]

/* ── Password strength ── */
const strengthScore = ref(0)
watch(() => form.password, (p) => {
  let s = 0
  if (p.length >= 8) s++
  if (p.length >= 12) s++
  if (/[A-Z]/.test(p)) s++
  if (/[0-9]/.test(p)) s++
  if (/[^A-Za-z0-9]/.test(p)) s++
  strengthScore.value = s
})
const strengthWidth     = computed(() => ['0%','25%','50%','75%','100%'][strengthScore.value])
const strengthFill      = computed(() => ['','sov-track__fill--ox','sov-track__fill--amber','sov-track__fill--amber','sov-track__fill--green'][strengthScore.value])
const strengthLabel     = computed(() => ['','Weak','Fair','Good','Strong'][strengthScore.value] || '')
const strengthTextClass = computed(() => strengthScore.value >= 4 ? 't-green' : strengthScore.value >= 3 ? 't-amber' : 't-red')

/* ── Validators ── */
function validateName()    { if (!form.name.trim() || form.name.trim().length < 2) { errors.name = 'Enter your full name.'; return false } errors.name = ''; return true }
function validateEmail()   { if (!form.email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) { errors.email = 'Enter a valid email.'; return false } errors.email = ''; return true }
function validatePassword(){ if (!form.password || form.password.length < 8) { errors.password = 'Minimum 8 characters.'; return false } errors.password = ''; return true }
function validateConfirm() { if (form.confirm !== form.password) { errors.confirm = 'Passwords do not match.'; return false } errors.confirm = ''; return true }
function validateConsent() { if (!form.consent) { errors.consent = 'You must accept the terms to continue.'; return false } errors.consent = ''; return true }

async function handleSubmit() {
  serverError.value = ''
  if (step.value === 1) {
    if (validateName() && validateEmail()) step.value = 2
    return
  }
  if (!validatePassword() || !validateConfirm() || !validateConsent()) return
  await register({ full_name: form.name, email: form.email, password: form.password, currency: form.currency })
}
</script>

<style scoped>
@import '@/styles/main.css';
.page-root { position: relative; min-height: 100vh; overflow-x: hidden; display: flex; flex-direction: column; }
.auth-section { flex: 1; display: flex; align-items: center; justify-content: center; padding: calc(60px + 48px) 20px 48px; min-height: 100svh; }
.auth-layout { display: grid; grid-template-columns: 1fr; gap: 40px; width: 100%; max-width: 980px; align-items: center; }
@media (min-width: 860px) { .auth-layout { grid-template-columns: 1fr 440px; gap: 64px; } }
.auth-panel--left { display: flex; flex-direction: column; gap: 28px; }
.panel-badge { display: inline-flex; align-items: center; gap: 8px; padding: 5px 14px; background: rgba(224,224,224,.04); border: 1px solid rgba(224,224,224,.08); border-radius: 100px; width: fit-content; }
.panel-h1   { font-size: clamp(2rem, 5vw, 3.4rem); line-height: 1.05; }
.panel-body { font-size: .86rem; max-width: 380px; line-height: 1.8; }
.panel-perks { padding: 16px 18px; background: rgba(18,18,20,.6); border: 1px solid var(--glass-bo); border-radius: var(--r-md); }
.perk-row  { display: flex; align-items: center; gap: 9px; padding: 5px 0; }
.perk-dot  { width: 4px; height: 4px; border-radius: 50%; background: var(--ox); flex-shrink: 0; box-shadow: 0 0 5px rgba(128,0,32,.7); }
.perk-text { font-size: 10px; color: rgba(117,117,117,.8); letter-spacing: .3px; }
.panel-chips { display: flex; flex-wrap: wrap; gap: 6px; }
.step-bar { position: relative; display: flex; align-items: center; gap: 10px; margin-bottom: 20px; padding-bottom: 18px; border-bottom: 1px solid rgba(224,224,224,.06); }
.step-item { display: flex; align-items: center; gap: 7px; z-index: 1; }
.step-circle { width: 22px; height: 22px; border-radius: 50%; border: 1px solid rgba(224,224,224,.14); background: rgba(8,8,8,.6); display: flex; align-items: center; justify-content: center; font-size: 9px; color: var(--gun); transition: all .22s; flex-shrink: 0; }
.step-circle.active { border-color: var(--ox); color: rgba(224,224,224,.9); box-shadow: 0 0 10px rgba(128,0,32,.3); }
.step-circle.done   { background: rgba(128,0,32,.15); border-color: var(--ox); color: var(--ox); }
.step-label { font-size: 8px; letter-spacing: 1.5px; text-transform: uppercase; color: var(--gun); }
.step-connector { position: absolute; left: 32px; top: 50%; transform: translateY(calc(-50% - 9px)); width: 80px; height: 1px; background: rgba(224,224,224,.08); transition: background .3s; }
.step-connector.done { background: rgba(128,0,32,.35); }
.auth-card { padding: 28px; }
.auth-card-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px; }
.auth-header-row { display: flex; align-items: center; gap: 8px; }
.modal-dot { width: 7px; height: 7px; background: var(--ox); border-radius: 50%; box-shadow: 0 0 8px rgba(128,0,32,0.9); flex-shrink: 0; }
.auth-title { font-size: clamp(1.5rem, 3vw, 2rem); margin-bottom: 4px; }
.auth-sub   { font-size: 9px; letter-spacing: 1.5px; color: var(--gun); margin-bottom: 24px; }
.auth-form  { display: flex; flex-direction: column; gap: 16px; margin-bottom: 20px; }
.strength-row { display: flex; align-items: center; gap: 10px; margin-top: -8px; }
.strength-track { flex: 1; }
.strength-label { font-size: 8.5px; letter-spacing: .5px; min-width: 38px; text-align: right; }
.auth-link { font-size: inherit; letter-spacing: .5px; color: var(--ox); transition: color .18s; }
.auth-link:hover { color: rgba(200,50,80,.9); }
.btn-row { display: flex; gap: 10px; }
.auth-submit { flex: 1; justify-content: center; position: relative; }
.auth-submit--full { width: 100%; }
.auth-submit.loading { pointer-events: none; opacity: .7; }
.auth-spinner { display: inline-block; width: 14px; height: 14px; border: 2px solid rgba(224,224,224,.2); border-top-color: rgba(224,224,224,.8); border-radius: 50%; animation: spin .7s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
.auth-footer-row { display: flex; align-items: center; justify-content: center; gap: 8px; padding-top: 18px; border-top: 1px solid rgba(224,224,224,.06); }
.auth-fade-left  { opacity: 0; transform: translateY(14px); animation: authFadeIn 0.38s cubic-bezier(0.22,1,0.36,1) 0.05s forwards; }
.auth-fade-right { opacity: 0; transform: translateY(14px); animation: authFadeIn 0.38s cubic-bezier(0.22,1,0.36,1) 0.18s forwards; }
@keyframes authFadeIn { to { opacity: 1; transform: translateY(0); } }
</style>