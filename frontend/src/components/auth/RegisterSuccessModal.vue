<template>
    <SovModal
      :model-value="modelValue"
      @update:model-value="$emit('update:modelValue', $event)"
      title="Vault Created"
      description="// CHECK YOUR INBOX"
      tag="// REGISTRATION COMPLETE"
      variant="success"
      size="md"
      :closable="true"
      :persistent="false"
    >
      <template #icon>
        <!-- Animated envelope icon -->
        <svg width="28" height="28" viewBox="0 0 28 28" fill="none" class="success-icon">
          <rect x="2" y="6" width="24" height="17" rx="3" stroke="var(--color-grn, #4CAF50)" stroke-width="1.5"/>
          <path d="M2 9l12 8 12-8" stroke="var(--color-grn, #4CAF50)" stroke-width="1.5" stroke-linecap="round"/>
          <path d="M18 16l4 4M10 16l-4 4" stroke="var(--color-grn, #4CAF50)" stroke-width="1.2" stroke-linecap="round" opacity=".4"/>
        </svg>
      </template>
  
      <!-- Info block -->
      <div class="reg-success-body">
        <p class="reg-success-name t-display">Welcome, {{ firstName }}.</p>
        <p class="reg-success-sub t-body">
          Your vault is live. We sent a verification email to:
        </p>
        <div class="reg-success-email-chip">
          <svg width="10" height="10" viewBox="0 0 13 13" fill="none" style="flex-shrink:0">
            <rect x="1" y="3" width="11" height="8" rx="1.5" stroke="currentColor" stroke-width="1.2"/>
            <path d="M1 4.5L6.5 8L12 4.5" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/>
          </svg>
          <span class="t-mono">{{ maskedEmail }}</span>
        </div>
        <p class="reg-success-note t-mono">
          Click the link in the email to verify your account. Link expires in 24 hours.
        </p>
  
        <!-- What you can do now -->
        <div class="reg-unverified-notice">
          <span class="sov-chip sov-chip--amber" style="font-size:7.5px;margin-bottom:10px;display:inline-flex">
            ⚡ UNVERIFIED — LIMITED ACCESS
          </span>
          <p class="t-mono" style="font-size:9px;color:rgba(224,224,224,0.5);line-height:1.6">
            You can explore the vault now. Some features (like data export and API access)
            require email verification.
          </p>
        </div>
      </div>
  
      <template #actions>
        <button class="sov-btn sov-btn--primary sov-btn--lg" style="justify-content:center" @click="goToDashboard">
          Enter Vault
          <svg width="12" height="12" viewBox="0 0 13 13" fill="none" style="margin-left:2px">
            <path d="M2.5 6.5h8M6.5 2.5l4 4-4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
        <button
          class="sov-btn sov-btn--ghost"
          style="justify-content:center;font-size:9.5px"
          :disabled="resendCooldown > 0"
          @click="resendEmail"
        >
          <span v-if="resendCooldown > 0">Resend in {{ resendCooldown }}s</span>
          <span v-else-if="resendSent">✓ Sent</span>
          <span v-else>Resend verification email</span>
        </button>
      </template>
  
      <template #footer>
        <span class="t-mono" style="font-size:8px;color:var(--color-gun);letter-spacing:.5px">
          Check your spam folder if you don't see it within 2 minutes.
        </span>
      </template>
    </SovModal>
  </template>
  
  <script setup lang="ts">
  import { computed, ref, onUnmounted } from 'vue'
  import { useRouter } from 'vue-router'
  import SovModal from '@/components/common/SovModal.vue'
  import { useAuth } from '@/composables/useAuth'
  
  const props = defineProps<{
    modelValue: boolean
    fullName: string
    email: string
  }>()
  
  defineEmits<{
    (e: 'update:modelValue', value: boolean): void
  }>()
  
  const router = useRouter()
  const { resendVerification } = useAuth()
  
  const firstName = computed(() => props.fullName.split(' ')[0] || props.fullName)
  
  const maskedEmail = computed(() => {
    const [local, domain] = props.email.split('@')
    if (!local || !domain) return props.email
    const visible = local.slice(0, 2)
    const masked = '*'.repeat(Math.max(local.length - 2, 3))
    return `${visible}${masked}@${domain}`
  })
  
  // Resend cooldown
  const resendCooldown = ref(0)
  const resendSent = ref(false)
  let cooldownTimer: ReturnType<typeof setInterval> | null = null
  
  function startCooldown(seconds = 60) {
    resendCooldown.value = seconds
    cooldownTimer = setInterval(() => {
      resendCooldown.value--
      if (resendCooldown.value <= 0 && cooldownTimer) {
        clearInterval(cooldownTimer)
      }
    }, 1000)
  }
  
  async function resendEmail() {
    if (resendCooldown.value > 0) return
    await resendVerification(props.email)
    resendSent.value = true
    startCooldown(60)
    setTimeout(() => { resendSent.value = false }, 4000)
  }
  
  function goToDashboard() {
    router.push('/dashboard')
  }
  
  onUnmounted(() => {
    if (cooldownTimer) clearInterval(cooldownTimer)
  })
  </script>
  
  <style scoped>
  .success-icon {
    animation: iconPop 0.4s cubic-bezier(0.22, 1, 0.36, 1) forwards;
  }
  @keyframes iconPop {
    from { transform: scale(0.6); opacity: 0; }
    to   { transform: scale(1);   opacity: 1; }
  }
  
  .reg-success-body {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
    padding-top: 4px;
  }
  
  .reg-success-name {
    font-size: 1.15rem;
    color: var(--color-plat, #E0E0E0);
    margin: 0;
  }
  
  .reg-success-sub {
    font-size: 13px;
    color: rgba(224, 224, 224, 0.55);
    text-align: center;
    margin: 0;
    line-height: 1.6;
  }
  
  .reg-success-email-chip {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    padding: 6px 14px;
    background: rgba(224, 224, 224, 0.05);
    border: 1px solid rgba(224, 224, 224, 0.1);
    border-radius: 100px;
    font-family: var(--font-mono, 'DM Mono', monospace);
    font-size: 10px;
    color: rgba(224, 224, 224, 0.7);
    letter-spacing: 0.5px;
  }
  
  .reg-success-note {
    font-size: 9px;
    letter-spacing: 0.3px;
    color: var(--color-gun, #757575);
    text-align: center;
    line-height: 1.7;
    max-width: 300px;
    text-transform: none;
  }
  
  .reg-unverified-notice {
    width: 100%;
    padding: 14px 16px;
    background: rgba(251, 140, 0, 0.05);
    border: 1px solid rgba(251, 140, 0, 0.15);
    border-radius: 8px;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 6px;
    margin-top: 4px;
  }
  </style>