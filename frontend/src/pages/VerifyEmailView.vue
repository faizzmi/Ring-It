<template>
  <div class="page-root">
    <AuthAmbient />

    <section class="verify-section">
      <div class="verify-card sov-card">

        <div class="verify-bar" :class="stateClass" />

        <div class="verify-header">
          <span class="sov-pulse" v-if="state === 'loading'" />
          <span class="t-mono" style="font-size:8.5px;letter-spacing:2.5px;color:var(--color-gun)">
            // EMAIL VERIFICATION
          </span>
        </div>

        <!-- Loading -->
        <div v-if="state === 'loading'" class="verify-body">
          <div class="verify-spinner-wrap"><span class="verify-spinner" /></div>
          <h2 class="verify-title t-display">Verifying...</h2>
          <p class="verify-sub t-mono">Validating your vault link.</p>
        </div>

        <!-- Success -->
        <div v-else-if="state === 'success'" class="verify-body">
          <div class="verify-icon-wrap verify-icon-wrap--success">
            <svg width="28" height="28" viewBox="0 0 28 28" fill="none">
              <path d="M5 14l7 7 11-11" stroke="var(--color-grn, #4CAF50)" stroke-width="2"
                    stroke-linecap="round" stroke-linejoin="round" class="check-path" />
            </svg>
          </div>
          <h2 class="verify-title t-display">Vault Verified.</h2>
          <p class="verify-sub t-mono">Your email has been confirmed.</p>
          <p class="verify-body-text t-body">
            Full vault access is now unlocked. Your behavioral wealth system is ready.
          </p>
          <button class="sov-btn sov-btn--primary sov-btn--lg verify-cta" @click="router.push('/dashboard')">
            Open Vault →
          </button>
        </div>

        <!-- Error -->
        <div v-else-if="state === 'error'" class="verify-body">
          <div class="verify-icon-wrap verify-icon-wrap--error">
            <svg width="26" height="26" viewBox="0 0 26 26" fill="none">
              <circle cx="13" cy="13" r="11" stroke="#ef5350" stroke-width="1.4"/>
              <path d="M13 8v5.5" stroke="#ef5350" stroke-width="1.6" stroke-linecap="round"/>
              <circle cx="13" cy="18" r="1" fill="#ef5350"/>
            </svg>
          </div>
          <h2 class="verify-title t-display">Link Invalid</h2>
          <p class="verify-sub t-mono">// {{ errorCode }}</p>
          <p class="verify-body-text t-body">{{ errorMessage }}</p>

          <div class="verify-resend">
            <p class="t-mono" style="font-size:9px;color:var(--color-gun);margin-bottom:10px;letter-spacing:1px">
              REQUEST A NEW LINK
            </p>
            <div class="verify-input-row">
              <input
                v-model="resendEmailInput"
                type="email"
                class="verify-input t-mono"
                placeholder="your@email.com"
                @keyup.enter="sendResend"
              />
              <button
                class="sov-btn sov-btn--primary"
                :disabled="resendLoading || resendCooldown > 0"
                @click="sendResend"
              >
                <span v-if="resendLoading" class="auth-spinner" />
                <span v-else-if="resendCooldown > 0">{{ resendCooldown }}s</span>
                <span v-else>Send</span>
              </button>
            </div>
            <p v-if="resendDone" class="t-mono" style="font-size:9px;color:var(--color-grn);margin-top:8px">
              ✓ Check your inbox — new link sent.
            </p>
          </div>

          <a href="/login" class="auth-link t-mono" style="font-size:10px;margin-top:8px">← Back to login</a>
        </div>

      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuth } from '@/composables/useAuth'
import AuthAmbient from '@/components/auth/AuthAmbient.vue'

// ✅ All API calls go through useAuth → apiFetch → correct API_BASE
const { verifyEmail, resendVerification } = useAuth()

type State = 'loading' | 'success' | 'error'

const route  = useRoute()
const router = useRouter()

const state            = ref<State>('loading')
const errorMessage     = ref('')
const errorCode        = ref('INVALID TOKEN')
const resendEmailInput = ref('')
const resendLoading    = ref(false)
const resendCooldown   = ref(0)
const resendDone       = ref(false)

const stateClass = computed(() => ({
  'verify-bar--success': state.value === 'success',
  'verify-bar--error':   state.value === 'error',
  'verify-bar--loading': state.value === 'loading',
}))

onMounted(async () => {
  const token = route.query.token as string | undefined
  if (!token) {
    state.value        = 'error'
    errorMessage.value = 'No verification token found in the URL.'
    errorCode.value    = 'MISSING TOKEN'
    return
  }
  try {
    await verifyEmail(token)   // ✅ goes to http://localhost:8000/api/v1/auth/verify-email
    state.value = 'success'
  } catch (e: unknown) {
    state.value        = 'error'
    const err          = e as Error & { status?: number }
    errorMessage.value = err.message || 'Verification failed.'
    errorCode.value    = err.status === 400 ? 'EXPIRED OR USED' : `HTTP ${err.status ?? 'ERR'}`
  }
})

async function sendResend() {
  if (!resendEmailInput.value || resendLoading.value || resendCooldown.value > 0) return
  resendLoading.value = true
  try {
    await resendVerification(resendEmailInput.value)  // ✅ goes to correct API_BASE
    resendDone.value = true
    let s = 60
    resendCooldown.value = s
    const t = setInterval(() => {
      resendCooldown.value = --s
      if (s <= 0) clearInterval(t)
    }, 1000)
  } catch {
    // backend always returns 200 — this only fires on network errors
  } finally {
    resendLoading.value = false
  }
}
</script>

<style scoped>
.page-root { position: relative; min-height: 100vh; display: flex; flex-direction: column; background: var(--color-void, #080808); }
.verify-section { flex: 1; display: flex; align-items: center; justify-content: center; padding: 40px 20px; }
.verify-card { width: 100%; max-width: 420px; overflow: hidden; }
.verify-bar { height: 2px; width: 100%; transition: background 0.4s; }
.verify-bar--loading { background: linear-gradient(90deg, rgba(128,0,32,0.6), rgba(128,0,32,0.1)); }
.verify-bar--success { background: linear-gradient(90deg, rgba(76,175,80,0.9), rgba(76,175,80,0.1)); }
.verify-bar--error   { background: linear-gradient(90deg, rgba(176,0,32,0.8), rgba(176,0,32,0.1)); }
.verify-header { display: flex; align-items: center; gap: 8px; padding: 16px 24px 0; }
.verify-body { display: flex; flex-direction: column; align-items: center; padding: 28px 28px 32px; gap: 10px; text-align: center; }
.verify-spinner-wrap { width: 64px; height: 64px; display: flex; align-items: center; justify-content: center; background: rgba(128,0,32,0.08); border: 1px solid rgba(128,0,32,0.2); border-radius: 50%; }
.verify-spinner { width: 24px; height: 24px; border: 2px solid rgba(128,0,32,0.2); border-top-color: var(--color-ox, #800020); border-radius: 50%; animation: spin 0.7s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
.verify-icon-wrap { width: 64px; height: 64px; display: flex; align-items: center; justify-content: center; border-radius: 50%; }
.verify-icon-wrap--success { background: rgba(76,175,80,0.1); border: 1px solid rgba(76,175,80,0.2); }
.verify-icon-wrap--error   { background: rgba(176,0,32,0.1);  border: 1px solid rgba(176,0,32,0.22); }
.check-path { stroke-dasharray: 28; stroke-dashoffset: 28; animation: drawCheck 0.4s 0.1s ease forwards; }
@keyframes drawCheck { to { stroke-dashoffset: 0; } }
.verify-title { font-size: 1.5rem; color: var(--color-plat, #E0E0E0); margin: 0; }
.verify-sub   { font-size: 9px; letter-spacing: 2px; color: var(--color-gun, #757575); margin: 0; }
.verify-body-text { font-size: 13px; color: rgba(224,224,224,0.55); line-height: 1.7; margin: 0; max-width: 300px; }
.verify-cta { width: 100%; max-width: 240px; justify-content: center; margin-top: 6px; }
.verify-resend { width: 100%; padding: 14px 16px; background: rgba(224,224,224,0.03); border: 1px solid rgba(224,224,224,0.08); border-radius: 8px; text-align: left; }
.verify-input-row { display: flex; gap: 8px; }
.verify-input { flex: 1; padding: 9px 12px; background: rgba(8,8,8,0.6); border: 1px solid rgba(224,224,224,0.1); border-radius: 6px; color: var(--color-plat, #E0E0E0); font-size: 11px; letter-spacing: 0.3px; outline: none; transition: border-color 0.18s; }
.verify-input:focus { border-color: rgba(128,0,32,0.5); }
.verify-input::placeholder { color: var(--color-gun, #757575); }
.auth-spinner { display: inline-block; width: 12px; height: 12px; border: 2px solid rgba(224,224,224,0.2); border-top-color: rgba(224,224,224,0.8); border-radius: 50%; animation: spin .7s linear infinite; }
.auth-link { color: var(--color-ox, #800020); transition: color .18s; }
.auth-link:hover { color: rgba(200,50,80,0.9); }
</style>